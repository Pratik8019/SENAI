"""
SentinelAI — Database Seed Script

Generates realistic synthetic email data for development and demo.
"""

import asyncio
import uuid
import random
from datetime import datetime, timezone, timedelta
from app.db.session import async_session_factory, engine
from app.db.base import Base
from app.models import Contact, Thread, Email, Action, ThreadStatus, ThreadPriority, EmailDirection, ActionType, ActionStatus
from app.core.security import hash_message_id
from app.intelligence.heuristic_engine import analyze_email
from app.intelligence.sentiment import quick_sentiment_score

SAMPLE_CONTACTS = [
    {"email": "sarah.chen@acmecorp.com", "name": "Sarah Chen", "company": "Acme Corp", "risk_score": 0.2},
    {"email": "mike.johnson@bigretail.io", "name": "Mike Johnson", "company": "BigRetail Inc", "risk_score": 0.7},
    {"email": "lisa.park@techstart.co", "name": "Lisa Park", "company": "TechStart", "risk_score": 0.1},
    {"email": "james.wilson@legalfirm.com", "name": "James Wilson", "company": "Wilson & Associates", "risk_score": 0.9},
    {"email": "anna.martinez@healthco.org", "name": "Anna Martinez", "company": "HealthCo", "risk_score": 0.3},
    {"email": "david.kim@financeplus.com", "name": "David Kim", "company": "FinancePlus", "risk_score": 0.5},
    {"email": "rachel.green@ecommshop.com", "name": "Rachel Green", "company": "E-Comm Shop", "risk_score": 0.4},
    {"email": "tom.harris@cybersec.io", "name": "Tom Harris", "company": "CyberSec Solutions", "risk_score": 0.8},
]

SAMPLE_THREADS = [
    {
        "subject": "Billing discrepancy on latest invoice",
        "category": "billing",
        "priority": ThreadPriority.HIGH,
        "emails": [
            {"body": "Hi, I noticed a $500 overcharge on my latest invoice #INV-2024-0891. We're on the Professional plan with 12 seats but were charged for 15. Can you please correct this? This is urgent as our finance team needs to close the books by Friday.", "sentiment": -0.3},
            {"body": "Following up on this. It's been 2 days and I haven't heard back. Our CFO is asking about this discrepancy. Please prioritize.", "sentiment": -0.6},
        ],
    },
    {
        "subject": "Request for enterprise pricing and custom SLA",
        "category": "billing",
        "priority": ThreadPriority.MEDIUM,
        "emails": [
            {"body": "Hello, we're evaluating SentinelAI for our organization of 200+ employees. Could you send us enterprise pricing details and information about custom SLAs? We need 99.99% uptime and a dedicated account manager. Budget is approved for Q2.", "sentiment": 0.4},
        ],
    },
    {
        "subject": "URGENT: API rate limiting causing production issues",
        "category": "support",
        "priority": ThreadPriority.CRITICAL,
        "emails": [
            {"body": "Our production system is being rate limited by your API since 3 AM today. We're getting 429 errors on every 3rd request. This is causing our customer-facing features to fail. We need this resolved IMMEDIATELY. We're on the Enterprise plan and this violates our SLA.", "sentiment": -0.8},
            {"body": "Update: Still seeing 429s. Our customers are complaining. We need an immediate response or we'll need to escalate this to your VP of Engineering.", "sentiment": -0.9},
            {"body": "Thank you for the quick fix! The rate limits are back to normal now. Appreciate the fast response once you got on it. Can we get a post-mortem report?", "sentiment": 0.6},
        ],
    },
    {
        "subject": "Legal Notice: Cease and Desist - Patent Infringement",
        "category": "legal",
        "priority": ThreadPriority.CRITICAL,
        "emails": [
            {"body": "Dear SentinelAI Legal Department,\n\nThis letter serves as formal notice that your email classification technology infringes on Patent US-2021-0284712 held by our client, InnovateTech LLC. We demand immediate cessation of the infringing technology.\n\nFailure to respond within 30 days will result in our client pursuing legal action in the United States District Court.\n\nSincerely,\nJames Wilson, Attorney at Law\nWilson & Associates", "sentiment": -0.9},
        ],
    },
    {
        "subject": "Feature request: Custom webhook integrations",
        "category": "feature_request",
        "priority": ThreadPriority.LOW,
        "emails": [
            {"body": "Hi team! We love SentinelAI and have been using it for 6 months now. One thing that would be amazing is custom webhook integrations so we can push classified emails directly to our Slack channels. Is this on your roadmap? Happy to be a beta tester!", "sentiment": 0.8},
        ],
    },
    {
        "subject": "Requesting full data export - GDPR compliance",
        "category": "legal",
        "priority": ThreadPriority.HIGH,
        "emails": [
            {"body": "Under the General Data Protection Regulation (GDPR), I am exercising my right to data portability. Please provide a complete export of all personal data you hold about me and our organization within 30 days. This includes all email processing logs, classification data, and any AI-generated profiles.\n\nPlease confirm receipt of this data subject access request.", "sentiment": -0.2},
        ],
    },
    {
        "subject": "Cancellation request - switching to competitor",
        "category": "complaint",
        "priority": ThreadPriority.HIGH,
        "emails": [
            {"body": "We've decided to cancel our SentinelAI subscription effective immediately. We're switching to CompetitorX because their pricing is 40% lower and they offer better API documentation. Please process our refund for the remaining annual subscription period. Account ID: ACC-4521.", "sentiment": -0.7},
            {"body": "I submitted the cancellation request 3 days ago and haven't received confirmation. If this isn't processed by EOD, I'll be filing a chargeback with our credit card company.", "sentiment": -0.9},
        ],
    },
    {
        "subject": "Integration help: Connecting SentinelAI with Salesforce",
        "category": "support",
        "priority": ThreadPriority.MEDIUM,
        "emails": [
            {"body": "Hi support team, I'm trying to set up the Salesforce integration but getting an OAuth error when connecting. I've followed the API docs but keep getting 'invalid_grant' errors. Can someone help? Here are my settings: Callback URL: https://ourapp.com/callback, Scopes: full access. Screenshot attached.", "sentiment": -0.1},
            {"body": "Thanks for the guidance! The callback URL was wrong — I needed to include the /api/v1 prefix. Working perfectly now. Your docs could use an update on this though.", "sentiment": 0.5},
        ],
    },
    {
        "subject": "Security concern: Suspicious login attempts",
        "category": "security",
        "priority": ThreadPriority.CRITICAL,
        "emails": [
            {"body": "URGENT: We've detected multiple failed login attempts on our SentinelAI admin account from IP addresses in Eastern Europe. We did NOT authorize these attempts. Please immediately: 1) Lock our account, 2) Provide login audit logs, 3) Reset all API keys. We suspect our credentials may have been compromised.", "sentiment": -0.8},
        ],
    },
    {
        "subject": "Great experience - Testimonial offer",
        "category": "general",
        "priority": ThreadPriority.LOW,
        "emails": [
            {"body": "Hey SentinelAI team! Just wanted to say that your platform has transformed our customer support operations. We've reduced response times by 60% and our CSAT scores are up 25%. Would love to provide a case study or testimonial for your website. Let me know if you're interested!", "sentiment": 0.95},
        ],
    },
    {
        "subject": "Refund request for unused subscription months",
        "category": "billing",
        "priority": ThreadPriority.MEDIUM,
        "emails": [
            {"body": "Hi, we signed up for the annual Professional plan 3 months ago but haven't been able to implement it due to internal restructuring. We'd like to request a pro-rated refund for the remaining 9 months. Our account ID is PRO-2024-0122. Please advise on the process.", "sentiment": -0.2},
        ],
    },
    {
        "subject": "CRITICAL: Your files have been encrypted",
        "category": "security",
        "priority": ThreadPriority.CRITICAL,
        "emails": [
            {"body": "ATTENTION: All your files have been encrypted with military-grade encryption. To decrypt your files, you must send 5 BTC to wallet address bc1q42lja79elem0anu8q860g3uj83m8. You have 72 hours. After the deadline, the decryption key will be destroyed and your data will be permanently lost. Do not contact law enforcement.", "sentiment": -1.0},
        ],
    },
]


async def seed_database():
    """Seed the database with sample data."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        # Check if already seeded
        from sqlalchemy import select, func
        count = (await session.execute(select(func.count(Contact.id)))).scalar()
        if count and count > 0:
            print(f"Database already has {count} contacts. Skipping seed.")
            return

        print("🌱 Seeding database...")

        # Create contacts
        contacts = {}
        for c_data in SAMPLE_CONTACTS:
            contact = Contact(
                id=uuid.uuid4(),
                email=c_data["email"],
                name=c_data["name"],
                company=c_data["company"],
                domain=c_data["email"].split("@")[1],
                risk_score=c_data["risk_score"],
            )
            session.add(contact)
            contacts[c_data["email"]] = contact
        await session.flush()

        # Create threads with emails
        contact_list = list(contacts.values())
        base_time = datetime.now(timezone.utc) - timedelta(days=30)

        for i, t_data in enumerate(SAMPLE_THREADS):
            contact = contact_list[i % len(contact_list)]
            thread_time = base_time + timedelta(days=i * 2, hours=random.randint(0, 12))

            thread = Thread(
                id=uuid.uuid4(),
                subject=t_data["subject"],
                contact_id=contact.id,
                status=ThreadStatus.OPEN,
                priority=t_data["priority"],
                category=t_data["category"],
                email_count=len(t_data["emails"]),
                last_activity_at=thread_time + timedelta(hours=len(t_data["emails"])),
            )
            session.add(thread)
            await session.flush()

            # Create emails for thread
            sentiment_trend = []
            for j, e_data in enumerate(t_data["emails"]):
                email_time = thread_time + timedelta(hours=j * 4, minutes=random.randint(0, 59))
                msg_id = f"<msg-{uuid.uuid4().hex[:12]}@{contact.domain}>"

                heuristic = analyze_email(contact.email, t_data["subject"], e_data["body"])
                s_label, s_score = quick_sentiment_score(e_data["body"])

                email = Email(
                    id=uuid.uuid4(),
                    thread_id=thread.id,
                    message_id=msg_id,
                    message_id_hash=hash_message_id(msg_id),
                    sender=contact.email,
                    sender_name=contact.name,
                    recipients=["support@sentinelai.com"],
                    subject=t_data["subject"],
                    body=e_data["body"],
                    direction=EmailDirection.INBOUND,
                    heuristic_result=heuristic.to_dict(),
                    classification={"category": t_data["category"], "sentiment_score": e_data["sentiment"]},
                    confidence_score=round(random.uniform(0.6, 0.95), 2),
                    priority_score=round(random.uniform(0.2, 0.9), 2),
                    is_processed=True,
                    requires_human=heuristic.do_not_auto_reply,
                    received_at=email_time,
                )
                session.add(email)

                sentiment_trend.append({
                    "score": e_data["sentiment"],
                    "label": s_label,
                    "ts": email_time.isoformat(),
                })

            thread.sentiment_score = t_data["emails"][-1]["sentiment"]
            thread.sentiment_trend = sentiment_trend

            # Update contact email count
            contact.total_emails += len(t_data["emails"])

        await session.commit()
        print(f"✅ Seeded {len(SAMPLE_CONTACTS)} contacts, {len(SAMPLE_THREADS)} threads")


if __name__ == "__main__":
    asyncio.run(seed_database())
