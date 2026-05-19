export interface Thread {
  id: string;
  subject: string;
  contact_id: string;
  status: 'open' | 'in_progress' | 'awaiting_reply' | 'resolved' | 'escalated';
  priority: 'low' | 'medium' | 'high' | 'critical';
  category: string | null;
  sentiment_score: number;
  sentiment_trend: SentimentPoint[] | null;
  email_count: number;
  last_activity_at: string;
  created_at: string;
}

export interface SentimentPoint {
  score: number;
  label: string;
  ts: string;
}

export interface ThreadDetail extends Thread {
  emails: import('./email').Email[];
  contact: ContactBrief | null;
}

export interface ContactBrief {
  id: string;
  email: string;
  name: string | null;
  company: string | null;
  risk_score: number;
}

export interface ThreadListResponse {
  threads: Thread[];
  total: number;
  page: number;
  page_size: number;
  has_next: boolean;
}
