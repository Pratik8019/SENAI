'use client';

import { cn } from '@/lib/utils';

interface StatusPillProps {
  status: string;
  size?: 'sm' | 'md';
}

const statusConfig: Record<string, { color: string; bg: string; label: string }> = {
  open: { color: '#00d4ff', bg: 'rgba(0,212,255,0.1)', label: 'Open' },
  in_progress: { color: '#ffaa00', bg: 'rgba(255,170,0,0.1)', label: 'Processing' },
  awaiting_reply: { color: '#7c3aed', bg: 'rgba(124,58,237,0.1)', label: 'Awaiting' },
  resolved: { color: '#00ff88', bg: 'rgba(0,255,136,0.1)', label: 'Resolved' },
  escalated: { color: '#ff3366', bg: 'rgba(255,51,102,0.1)', label: 'Escalated' },
  critical: { color: '#ff3366', bg: 'rgba(255,51,102,0.1)', label: 'Critical' },
  high: { color: '#ff8800', bg: 'rgba(255,136,0,0.1)', label: 'High' },
  medium: { color: '#ffaa00', bg: 'rgba(255,170,0,0.1)', label: 'Medium' },
  low: { color: '#00d4ff', bg: 'rgba(0,212,255,0.1)', label: 'Low' },
};

export default function StatusPill({ status, size = 'sm' }: StatusPillProps) {
  const config = statusConfig[status] || statusConfig.open;

  return (
    <span
      className={cn(
        'status-pill',
        size === 'sm' ? 'text-[10px] px-2 py-0.5' : 'text-xs px-3 py-1'
      )}
      style={{
        color: config.color,
        background: config.bg,
        border: `1px solid ${config.color}30`,
      }}
    >
      <span
        className="w-1.5 h-1.5 rounded-full inline-block"
        style={{ background: config.color }}
      />
      {config.label}
    </span>
  );
}
