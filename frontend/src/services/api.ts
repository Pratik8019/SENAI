import { api } from '@/lib/api';
import type { EmailListResponse } from '@/types/email';
import type { ThreadListResponse, ThreadDetail } from '@/types/thread';
import type { AgentDryRunResponse } from '@/types/agent';
import type { AnalyticsDashboard } from '@/types/analytics';

export const emailService = {
  list: (page = 1, pageSize = 20, status?: string) =>
    api.get<EmailListResponse>('/emails', { params: { page, page_size: pageSize, status } }).then(r => r.data),
};

export const threadService = {
  list: (page = 1, pageSize = 20, status?: string, priority?: string) =>
    api.get<ThreadListResponse>('/threads', { params: { page, page_size: pageSize, status, priority } }).then(r => r.data),

  get: (id: string) =>
    api.get<ThreadDetail>(`/threads/${id}`).then(r => r.data),
};

export const agentService = {
  dryRun: (emailId: string) =>
    api.post<AgentDryRunResponse>(`/agent/dry-run/${emailId}`).then(r => r.data),
};

export const analyticsService = {
  dashboard: () =>
    api.get<AnalyticsDashboard>('/analytics/dashboard').then(r => r.data),
};

export const ragService = {
  search: (query: string, topK = 5) =>
    api.get('/rag/search', { params: { q: query, top_k: topK } }).then(r => r.data),
};
