"""
SentinelAI — Contact Endpoints
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_database
from app.schemas.contact import ContactListResponse, ContactResponse
from app.services.contact_service import get_contacts_paginated

router = APIRouter(tags=["Contacts"])


@router.get("/contacts", response_model=ContactListResponse)
async def list_contacts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_database),
):
    contacts, total = await get_contacts_paginated(db, page, page_size)
    return ContactListResponse(
        contacts=[ContactResponse.model_validate(c) for c in contacts],
        total=total,
        page=page,
        page_size=page_size,
    )
