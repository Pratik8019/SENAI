export interface Contact {
  id: string;
  email: string;
  name: string | null;
  company: string | null;
  domain: string | null;
  phone: string | null;
  risk_score: number;
  total_emails: number;
  notes: string | null;
  created_at: string;
  updated_at: string;
}
