# SentinelAI Escalation Matrix

## Overview
This document defines when and how emails should be escalated based on threat type, severity, and organizational responsibility.

## Escalation Levels

### Level 1 — Auto-Handled (AI)
- General inquiries
- FAQ-type questions
- Feature requests
- Positive feedback
- Simple billing questions

**Action**: AI generates suggested reply, sends with human-in-the-loop approval (Professional) or automatically (Enterprise with auto-reply enabled).

### Level 2 — Agent Review
- Complex support issues
- Multi-step troubleshooting
- Account-specific problems
- Moderate complaints
- Unusual requests

**Action**: AI agent runs full analysis, drafts response, flags for human review.

### Level 3 — Team Lead Escalation
- Repeated complaints from same customer
- High-value customer issues (>$10k ARR)
- Service outage reports
- Churn risk indicators
- Requests for exceptions to policy

**Action**: Assigned to team lead with full context package. SLA: 4 hours.

### Level 4 — Management Escalation
- Threats to go public (social media, press)
- Requests involving executive contacts
- Compliance concerns
- Data breach reports
- Competitor poaching attempts

**Action**: Notified to management + relevant team. SLA: 2 hours.

### Level 5 — Legal/Security Critical
- Legal threats (lawsuit, cease & desist)
- Ransomware / extortion
- GDPR/CCPA formal requests
- Subpoenas or court orders
- Active security breaches

**Action**: IMMEDIATE escalation. No auto-reply. Legal team and CISO notified simultaneously. SLA: 1 hour.

## Escalation Contacts

| Level | Primary | Backup | Channel |
|-------|---------|--------|---------|
| L1 | AI System | Support Agent | Auto |
| L2 | Support Agent | Team Lead | Dashboard |
| L3 | Team Lead | Support Manager | Slack + Email |
| L4 | Support Manager | VP Support | Slack + PagerDuty |
| L5 | Legal + CISO | CEO | PagerDuty + Phone |

## Auto-Escalation Triggers
The system automatically escalates when:
1. Customer sentiment drops below -0.7 across 3+ emails
2. Same customer opens 3+ threads in 7 days
3. Email contains keywords matching Level 5 patterns
4. AI confidence score < 0.3 on classification
5. Customer is flagged as "at-risk" in CRM
