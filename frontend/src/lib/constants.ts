export const APP_NAME = 'SentinelAI';
export const APP_SUBTITLE = 'Mission Control';

export const STATUS_LABELS: Record<string, string> = {
  open: 'Open',
  in_progress: 'In Progress',
  awaiting_reply: 'Awaiting Reply',
  resolved: 'Resolved',
  escalated: 'Escalated',
};

export const PRIORITY_LABELS: Record<string, string> = {
  low: 'Low',
  medium: 'Medium',
  high: 'High',
  critical: 'Critical',
};

export const KEYBOARD_SHORTCUTS = {
  SEARCH: '/',
  NEW: 'n',
  REFRESH: 'r',
  ESCAPE: 'Escape',
};
