"""
SentinelAI — Web Intelligence Service

Async web scraping with caching, robots.txt compliance, and graceful failure handling.
"""

import asyncio
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import WebIntelligenceCache

# Default cache TTL
CACHE_TTL_HOURS = 24


async def scrape_url(url: str, session: aiohttp.ClientSession) -> str | None:
    """Scrape a URL with timeout and error handling."""
    try:
        # Check robots.txt compliance
        if not await _check_robots_txt(url, session):
            return None

        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if resp.status != 200:
                return None
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            # Remove scripts and styles
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            return soup.get_text(separator="\n", strip=True)[:5000]
    except Exception:
        return None


async def _check_robots_txt(url: str, session: aiohttp.ClientSession) -> bool:
    """Basic robots.txt compliance check."""
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    try:
        async with session.get(robots_url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
            if resp.status != 200:
                return True  # No robots.txt = allowed
            content = await resp.text()
            # Very basic check — a real impl would use robotparser
            if "Disallow: /" in content and "User-agent: *" in content:
                return False
            return True
    except Exception:
        return True


async def get_cached_or_scrape(
    db: AsyncSession, url: str, query: str | None = None
) -> dict:
    """Check cache first, scrape if expired/missing."""
    # Check cache
    result = await db.execute(
        select(WebIntelligenceCache).where(WebIntelligenceCache.url == url)
    )
    cached = result.scalar_one_or_none()

    if cached and cached.expires_at and cached.expires_at > datetime.now(timezone.utc):
        return {
            "url": url,
            "content": cached.content,
            "summary": cached.summary,
            "cached": True,
            "scraped_at": cached.scraped_at.isoformat(),
        }

    # Scrape fresh
    async with aiohttp.ClientSession(
        headers={"User-Agent": "SentinelAI/1.0 (CRM Intelligence Bot)"}
    ) as session:
        content = await scrape_url(url, session)

    if not content:
        return {"url": url, "content": None, "error": "Failed to scrape or blocked by robots.txt"}

    # Update/create cache entry
    if cached:
        cached.content = content
        cached.scraped_at = datetime.now(timezone.utc)
        cached.expires_at = datetime.now(timezone.utc) + timedelta(hours=CACHE_TTL_HOURS)
    else:
        cached = WebIntelligenceCache(
            url=url,
            query=query,
            content=content,
            scraped_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + timedelta(hours=CACHE_TTL_HOURS),
        )
        db.add(cached)

    await db.flush()

    return {
        "url": url,
        "content": content[:2000],
        "cached": False,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
    }
