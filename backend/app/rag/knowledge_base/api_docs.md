# SentinelAI API Documentation

## Base URL
- Production: `https://api.sentinelai.com/v1`
- Staging: `https://api-staging.sentinelai.com/v1`

## Authentication
All API requests require a Bearer token in the Authorization header:
```
Authorization: Bearer sk-sentinel-xxxxxxxxxxxx
```

API keys can be generated in Settings → API Keys. Each key has configurable scopes.

## Rate Limits
- Starter: 100 requests/minute
- Professional: 500 requests/minute
- Enterprise: 5,000 requests/minute

Rate limit headers are included in every response:
- `X-RateLimit-Limit`: Max requests per window
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Unix timestamp when limit resets

## Endpoints

### POST /api/v1/ingest
Ingest one or more emails into the processing pipeline.

**Request Body:**
```json
{
  "emails": [
    {
      "message_id": "<unique-id@domain.com>",
      "sender": "customer@example.com",
      "recipients": ["support@sentinelai.com"],
      "subject": "Billing question",
      "body": "I have a question about my invoice...",
      "received_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Response:** 201 Created
```json
{
  "ingested": 1,
  "duplicates": 0,
  "errors": []
}
```

### GET /api/v1/threads
List email threads with pagination.

Query params: `page`, `page_size`, `status`, `priority`

### GET /api/v1/threads/{thread_id}
Get thread details with full email history.

### POST /api/v1/agent/dry-run/{email_id}
Run the AI agent on an email without taking action.

### GET /api/v1/rag/search
Search the knowledge base.

Query params: `q` (query string), `top_k` (number of results)

## Webhooks
Configure webhooks in Settings → Integrations to receive real-time notifications:
- `email.ingested` — New email processed
- `email.classified` — Classification complete
- `email.escalated` — Escalation triggered
- `thread.resolved` — Thread marked resolved

## Error Codes
| Code | Meaning |
|------|---------|
| 400 | Bad Request — Invalid parameters |
| 401 | Unauthorized — Invalid or missing API key |
| 403 | Forbidden — Insufficient scope |
| 404 | Not Found |
| 409 | Conflict — Duplicate resource |
| 429 | Too Many Requests — Rate limited |
| 500 | Internal Server Error |
