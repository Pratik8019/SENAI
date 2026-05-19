export interface Email {
  id: string;
  thread_id: string;
  message_id: string;
  sender: string;
  sender_name: string | null;
  subject: string;
  body: string;
  direction: 'inbound' | 'outbound';
  heuristic_result: HeuristicResult | null;
  classification: Classification | null;
  confidence_score: number | null;
  priority_score: number | null;
  is_processed: boolean;
  requires_human: boolean;
  received_at: string;
  created_at: string;
}

export interface HeuristicResult {
  is_spam: boolean;
  is_ransomware: boolean;
  is_legal_threat: boolean;
  is_gdpr_request: boolean;
  is_internal: boolean;
  is_urgent: boolean;
  do_not_auto_reply: boolean;
  urgency_score: number;
  spam_score: number;
  flags: string[];
}

export interface Classification {
  category: string;
  sentiment: string;
  sentiment_score: number;
  urgency: string;
  confidence: number;
  requires_human: boolean;
  escalation_reason: string | null;
  suggested_reply: string | null;
  entities: Record<string, unknown>;
  summary: string;
  risk_indicators: string[];
}

export interface EmailListResponse {
  emails: Email[];
  total: number;
  page: number;
  page_size: number;
  has_next: boolean;
}
