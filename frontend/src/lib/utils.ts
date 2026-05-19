import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (minutes < 1) return 'Just now';
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days < 7) return `${days}d ago`;
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

export function getSentimentColor(score: number): string {
  if (score >= 0.5) return '#00ff88';
  if (score >= 0.1) return '#88ff88';
  if (score >= -0.1) return '#888888';
  if (score >= -0.5) return '#ff8844';
  return '#ff3366';
}

export function getPriorityColor(priority: string): string {
  switch (priority) {
    case 'critical': return '#ff3366';
    case 'high': return '#ff8800';
    case 'medium': return '#ffaa00';
    case 'low': return '#00d4ff';
    default: return '#666666';
  }
}

export function getCategoryIcon(category: string): string {
  switch (category) {
    case 'billing': return '💳';
    case 'support': return '🔧';
    case 'legal': return '⚖️';
    case 'security': return '🛡️';
    case 'feature_request': return '✨';
    case 'complaint': return '😤';
    case 'spam': return '🚫';
    default: return '📧';
  }
}

export function truncate(str: string, len: number): string {
  return str.length > len ? str.slice(0, len) + '...' : str;
}
