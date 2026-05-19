export interface AnalyticsDashboard {
  sentiment_trend: SentimentTrendPoint[];
  categories: CategoryCount[];
  escalation_heatmap: EscalationHeatmapCell[];
  ai_performance: AIPerformanceMetrics;
  at_risk_customers: AtRiskCustomer[];
  total_emails: number;
  total_threads: number;
  total_contacts: number;
}

export interface SentimentTrendPoint {
  date: string;
  score: number;
  count: number;
}

export interface CategoryCount {
  category: string;
  count: number;
  percentage: number;
}

export interface EscalationHeatmapCell {
  day: number;
  hour: number;
  count: number;
}

export interface AIPerformanceMetrics {
  total_processed: number;
  auto_resolved: number;
  auto_resolve_rate: number;
  avg_confidence: number;
  avg_processing_time_ms: number;
  requires_human_count: number;
  escalation_count: number;
}

export interface AtRiskCustomer {
  contact_id: string;
  email: string;
  name: string | null;
  company: string | null;
  risk_score: number;
  recent_sentiment: number;
  total_threads: number;
  last_activity: string;
}
