export interface AgentStep {
  step_number: number;
  thought: string;
  action: string | null;
  action_input: Record<string, unknown> | null;
  observation: string | null;
  timestamp: string | null;
}

export interface AgentResult {
  email_id: string;
  final_answer: string;
  steps: AgentStep[];
  tools_used: string[];
  total_steps: number;
  execution_time_ms: number;
  suggested_actions: string[];
  confidence: number;
}

export interface AgentDryRunResponse {
  success: boolean;
  result: AgentResult | null;
  error: string | null;
}
