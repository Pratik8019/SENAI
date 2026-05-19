"""
SentinelAI — Email Ingestion Endpoint

POST /api/v1/ingest — Processes incoming emails through the full pipeline.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_database
from app.schemas.email import EmailIngestPayload, EmailBatchIngest, EmailResponse
from app.services.email_service import ingest_email

router = APIRouter(tags=["Ingestion"])


@router.post("/ingest", response_model=dict, status_code=201)
async def ingest_emails(
    payload: EmailBatchIngest,
    db: AsyncSession = Depends(get_database),
):
    """
    Ingest one or more emails into the SentinelAI processing pipeline.

    Each email goes through:
    1. Schema validation
    2. Duplicate detection
    3. Contact resolution
    4. Thread linking
    5. Heuristic analysis
    6. Priority scoring
    """
    ingested = 0
    duplicates = 0
    errors = []

    for email_payload in payload.emails:
        try:
            await ingest_email(db, email_payload)
            ingested += 1
        except ValueError as e:
            if "Duplicate" in str(e):
                duplicates += 1
            else:
                errors.append({"message_id": email_payload.message_id, "error": str(e)})
        except Exception as e:
            errors.append({"message_id": email_payload.message_id, "error": str(e)})

    await db.commit()

    return {
        "ingested": ingested,
        "duplicates": duplicates,
        "errors": errors,
        "total_submitted": len(payload.emails),
    }


@router.post("/ingest/single", response_model=EmailResponse, status_code=201)
async def ingest_single_email(
    payload: EmailIngestPayload,
    db: AsyncSession = Depends(get_database),
):
    """Ingest a single email."""
    try:
        email = await ingest_email(db, payload)
        await db.commit()
        return email
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
