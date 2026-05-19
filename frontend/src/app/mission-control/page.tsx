'use client';

import { useState, useMemo, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import TopBar from '@/components/layout/TopBar';
import GlowCard from '@/components/shared/GlowCard';
import MetricCard from '@/components/shared/MetricCard';
import StatusPill from '@/components/shared/StatusPill';
import { cn, formatDate, getPriorityColor, getCategoryIcon, truncate, getSentimentColor } from '@/lib/utils';
import Link from 'next/link';
import { Radio, Search, Terminal, Database, Activity, ShieldAlert, Cpu } from 'lucide-react';

// Demo data
const DEMO_THREADS = [
  { id: '1', subject: 'Billing discrepancy on latest invoice', sender: 'Sarah Chen', sender_email: 'sarah.chen@acmecorp.com', company: 'Acme Corp', category: 'billing', priority: 'high' as const, status: 'open' as const, sentiment_score: -0.6, confidence: 0.89, email_count: 2, last_activity: new Date(Date.now() - 3600000 * 2).toISOString(), preview: 'I noticed a $500 overcharge on my latest invoice #INV-2024-0891...', flags: ['urgent'] },
  { id: '2', subject: 'URGENT: API rate limiting causing production issues', sender: 'Mike Johnson', sender_email: 'mike@bigretail.io', company: 'BigRetail Inc', category: 'support', priority: 'critical' as const, status: 'escalated' as const, sentiment_score: -0.9, confidence: 0.94, email_count: 3, last_activity: new Date(Date.now() - 3600000 * 1).toISOString(), preview: 'Our production system is being rate limited by your API since 3 AM today...', flags: ['critical', 'sla_breach'] },
  { id: '3', subject: 'Legal Notice: Cease and Desist - Patent Infringement', sender: 'James Wilson', sender_email: 'james@legalfirm.com', company: 'Wilson & Associates', category: 'legal', priority: 'critical' as const, status: 'escalated' as const, sentiment_score: -0.95, confidence: 0.97, email_count: 1, last_activity: new Date(Date.now() - 3600000 * 5).toISOString(), preview: 'This letter serves as formal notice that your email classification technology infringes...', flags: ['legal_threat', 'do_not_reply'] },
  { id: '4', subject: 'Feature request: Custom webhook integrations', sender: 'Lisa Park', sender_email: 'lisa@techstart.co', company: 'TechStart', category: 'feature_request', priority: 'low' as const, status: 'open' as const, sentiment_score: 0.8, confidence: 0.82, email_count: 1, last_activity: new Date(Date.now() - 3600000 * 8).toISOString(), preview: 'We love SentinelAI and have been using it for 6 months now...', flags: [] },
  { id: '5', subject: 'Requesting full data export - GDPR compliance', sender: 'Anna Martinez', sender_email: 'anna@healthco.org', company: 'HealthCo', category: 'legal', priority: 'high' as const, status: 'in_progress' as const, sentiment_score: -0.2, confidence: 0.91, email_count: 1, last_activity: new Date(Date.now() - 3600000 * 12).toISOString(), preview: 'Under the General Data Protection Regulation (GDPR), I am exercising my right to data portability...', flags: ['gdpr_request', 'do_not_reply'] },
  { id: '6', subject: 'Cancellation request - switching to competitor', sender: david => 'David Kim', sender_email: 'david@financeplus.com', company: 'FinancePlus', category: 'complaint', priority: 'high' as const, status: 'open' as const, sentiment_score: -0.85, confidence: 0.88, email_count: 2, last_activity: new Date(Date.now() - 3600000 * 6).toISOString(), preview: "We've decided to cancel our SentinelAI subscription effective immediately...", flags: ['churn_risk'] },
  { id: '7', subject: 'Security concern: Suspicious login attempts', sender: 'Tom Harris', sender_email: 'tom@cybersec.io', company: 'CyberSec Solutions', category: 'security', priority: 'critical' as const, status: 'escalated' as const, sentiment_score: -0.8, confidence: 0.93, email_count: 1, last_activity: new Date(Date.now() - 3600000 * 3).toISOString(), preview: "URGENT: We've detected multiple failed login attempts on our SentinelAI admin account...", flags: ['security_alert'] },
  { id: '8', subject: 'Great experience - Testimonial offer', sender: 'Rachel Green', sender_email: 'rachel@ecommshop.com', company: 'E-Comm Shop', category: 'general', priority: 'low' as const, status: 'resolved' as const, sentiment_score: 0.95, confidence: 0.86, email_count: 1, last_activity: new Date(Date.now() - 3600000 * 24).toISOString(), preview: 'Just wanted to say that your platform has transformed our customer support operations...', flags: [] },
  { id: '9', subject: 'Request for enterprise pricing and custom SLA', sender: 'Sarah Chen', sender_email: 'sarah.chen@acmecorp.com', company: 'Acme Corp', category: 'billing', priority: 'medium' as const, status: 'open' as const, sentiment_score: 0.4, confidence: 0.78, email_count: 1, last_activity: new Date(Date.now() - 3600000 * 18).toISOString(), preview: "We're evaluating SentinelAI for our organization of 200+ employees...", flags: [] },
  { id: '10', subject: 'CRITICAL: Your files have been encrypted', sender: 'Unknown', sender_email: 'anon@darkmail.xyz', company: 'Unknown', category: 'security', priority: 'critical' as const, status: 'escalated' as const, sentiment_score: -1.0, confidence: 0.99, email_count: 1, last_activity: new Date(Date.now() - 3600000 * 1.5).toISOString(), preview: 'All your files have been encrypted with military-grade encryption. Send 5 BTC...', flags: ['ransomware', 'do_not_reply', 'critical'] },
];

const FILTERS = [
  { key: 'all', label: 'ALL_THREADS', count: 10 },
  { key: 'critical', label: 'CRITICAL', count: 4 },
  { key: 'legal', label: 'LEGAL', count: 2 },
  { key: 'needs_review', label: 'REVIEW_REQ', count: 5 },
  { key: 'resolved', label: 'RESOLVED', count: 1 },
];

const INITIAL_LOGS = [
  "SEC_CORE: Booting broad-spectrum receptor...",
  "SEC_CORE: Syncing cluster metadata from Node_0x7A",
  "NEURAL_NET: Categorization weights fully updated",
  "RAG_STORE: Vector database status nominal [14 policies]",
];

export default function MissionControlPage() {
  const [activeFilter, setActiveFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [isBooting, setIsBooting] = useState(true);
  const [logs, setLogs] = useState<string[]>(INITIAL_LOGS);

  useEffect(() => {
    // Simulator boot scanning screen
    const timer = setTimeout(() => setIsBooting(false), 1400);

    // Simulator live diagnostics log stream
    const logInterval = setInterval(() => {
      const timeStr = new Date().toLocaleTimeString('en-US', { hour12: false });
      const mockLogPrefixes = ["[INFO]", "[AGENT]", "[SEC]", "[RAG]", "[LIMITER]"];
      const mockLogTexts = [
        "Thread analysis loop executed: 10/10 ok",
        "Updated category score for ACME: Billing (91% confidence)",
        "Rate limiter: checking token bucket availability",
        "Sentiment calculation complete: polarity -0.22",
        "Autonomous agent trace deployed for query 0xAF",
        "Cache flush: 12 nodes verified",
      ];
      const randomPrefix = mockLogPrefixes[Math.floor(Math.random() * mockLogPrefixes.length)];
      const randomText = mockLogTexts[Math.floor(Math.random() * mockLogTexts.length)];
      setLogs(prev => [`${timeStr} ${randomPrefix} ${randomText}`, ...prev.slice(0, 15)]);
    }, 5000);

    return () => {
      clearTimeout(timer);
      clearInterval(logInterval);
    };
  }, []);

  const filteredThreads = useMemo(() => {
    let threads = DEMO_THREADS;
    if (activeFilter === 'critical') threads = threads.filter(t => t.priority === 'critical');
    else if (activeFilter === 'legal') threads = threads.filter(t => t.category === 'legal');
    else if (activeFilter === 'needs_review') threads = threads.filter(t => t.flags.includes('do_not_reply') || t.status === 'escalated');
    else if (activeFilter === 'resolved') threads = threads.filter(t => t.status === 'resolved');
    
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      threads = threads.filter(t => 
        t.subject.toLowerCase().includes(q) || 
        t.sender.toLowerCase().includes(q) || 
        t.company.toLowerCase().includes(q)
      );
    }
    return threads;
  }, [activeFilter, searchQuery]);

  return (
    <div className="pb-12 min-h-screen relative">
      <AnimatePresence>
        {isBooting && (
          <motion.div
            initial={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.4 }}
            className="fixed inset-0 bg-[#04060a] z-50 flex flex-col items-center justify-center font-mono text-xs text-[var(--palette-sky)]"
          >
            <div className="w-64 space-y-4">
              <div className="flex justify-between items-center select-none text-[10px] tracking-widest text-[var(--palette-yellow)] font-bold">
                <span>// SENTINEL BOOT SCAN</span>
                <span className="animate-pulse">LOADING</span>
              </div>
              <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden relative border border-white/5">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: '100%' }}
                  transition={{ duration: 1.2, ease: 'easeInOut' }}
                  className="h-full bg-gradient-to-r from-[var(--palette-sky)] to-[var(--palette-yellow)]"
                />
              </div>
              <div className="text-[9px] text-white/30 uppercase leading-relaxed max-w-sm">
                Deploying security matrix...<br />
                Verifying coprocessor pipelines...<br />
                Interface locking: secure connection verified
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <TopBar title="Mission Control" subtitle="Real-time threat monitoring & telemetry" />

      {/* Dynamic Grid Background line sweep */}
      <div className="grid-overlay" />
      <div className="radar-scan-line" />

      {/* Metrics Row */}
      <div className="px-8 grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 relative z-10">
        <MetricCard label="Total Telemetry Nodes" value="127" icon="📬" trend={{ value: 12, label: 'vs last week' }} accentColor="var(--palette-sky)" delay={0} />
        <MetricCard label="Active Alerts" value="4" icon="🚨" trend={{ value: -8, label: 'vs last week' }} accentColor="var(--accent-pink)" delay={0.08} />
        <MetricCard label="Autonomous Resolve" value="68%" icon="🤖" trend={{ value: 5, label: 'improvement' }} accentColor="var(--palette-yellow)" delay={0.16} />
        <MetricCard label="Active Latency" value="2.4h" icon="⚡" trend={{ value: -15, label: 'faster' }} accentColor="var(--palette-peach)" delay={0.24} />
      </div>

      {/* Controls Container */}
      <div className="px-8 mb-5 relative z-10">
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4">
          {/* Search bar with HUD layout */}
          <div className="relative flex-1 max-w-md">
            <input
              type="text"
              placeholder="QUERY FILTERS... (press /)"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-2.5 pl-10 rounded bg-[#0a0e17]/80 border border-white/8 text-white text-xs font-mono placeholder-white/20 focus:outline-none focus:border-[var(--palette-sky)]/35 focus:ring-1 focus:ring-[var(--palette-sky)]/10 transition-all uppercase"
            />
            <Search className="w-3.5 h-3.5 text-white/25 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <kbd className="absolute right-3.5 top-1/2 -translate-y-1/2 px-1.5 py-0.5 text-[8px] font-mono rounded bg-white/5 text-white/20 border border-white/8">
              /
            </kbd>
          </div>

          {/* Filter chips (Holographic terminal look) */}
          <div className="flex flex-wrap gap-1.5 select-none">
            {FILTERS.map((filter) => (
              <motion.button
                key={filter.key}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setActiveFilter(filter.key)}
                className={cn(
                  'px-3 py-2 rounded text-[10px] font-mono tracking-wider transition-all duration-150 cursor-pointer border',
                  activeFilter === filter.key
                    ? 'bg-[rgba(140,192,235,0.12)] text-[var(--palette-sky)] border-[rgba(140,192,235,0.25)] shadow-[0_0_12px_rgba(140,192,235,0.06)]'
                    : 'bg-[#0a0e17]/40 text-white/40 border-white/5 hover:bg-white/5 hover:text-white/60'
                )}
              >
                {filter.label}
                <span className={cn(
                  "ml-2 text-[9px] px-1 py-0.2 rounded font-bold font-mono",
                  activeFilter === filter.key ? "bg-[var(--palette-sky)]/10 text-[var(--palette-sky)]" : "bg-white/5 text-white/20"
                )}>{filter.count}</span>
              </motion.button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Command Dashboard Layout */}
      <div className="px-8 grid grid-cols-1 lg:grid-cols-4 gap-6 relative z-10">
        {/* Left 3 columns: Thread tactical board */}
        <div className="lg:col-span-3 space-y-3">
          <div className="flex items-center justify-between font-mono text-[9px] text-white/20 border-b border-white/5 pb-2 mb-2 select-none">
            <span>TACTICAL_VECTOR_FEED // INCOMING_STREAMS</span>
            <span>SHOWN: {filteredThreads.length}</span>
          </div>

          <AnimatePresence mode="popLayout">
            {filteredThreads.length > 0 ? (
              filteredThreads.map((thread, idx) => (
                <motion.div
                  key={thread.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  transition={{ duration: 0.25, delay: idx * 0.03 }}
                  layout
                >
                  <Link href={`/thread/${thread.id}`} className="block">
                    <GlowCard 
                      className="hover:bg-white/[0.02] p-4 cursor-pointer group"
                      glowColor={getPriorityColor(thread.priority)}
                      panelId={thread.id}
                      showCoords
                    >
                      <div className="flex items-start justify-between gap-4">
                        {/* Left: Content details */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1.5">
                            <span className="text-sm filter drop-shadow-[0_0_5px_rgba(255,255,255,0.15)]">{getCategoryIcon(thread.category)}</span>
                            <h3 className="text-sm font-semibold font-sans text-white/90 truncate group-hover:text-[var(--palette-sky)] transition-colors">
                              {thread.subject}
                            </h3>
                          </div>
                          <div className="flex items-center gap-2 mb-2 font-mono text-[10px]">
                            <span className="text-white/60">{thread.sender}</span>
                            <span className="text-white/20">•</span>
                            <span className="text-white/40">{thread.company}</span>
                            <span className="text-white/20">•</span>
                            <span className="text-[var(--palette-sky)] bg-[rgba(140,192,235,0.06)] px-1.5 py-0.2 rounded border border-[rgba(140,192,235,0.1)]">
                              {thread.email_count} METRIC_NODES
                            </span>
                          </div>
                          <p className="text-xs text-white/45 truncate font-sans">{truncate(thread.preview, 110)}</p>
                        </div>

                        {/* Right: Meta statuses & AI Telemetry */}
                        <div className="flex flex-col items-end gap-2 shrink-0 font-mono">
                          <span className="text-[10px] text-white/30 font-bold">{formatDate(thread.last_activity)}</span>

                          <div className="flex items-center gap-1.5">
                            <StatusPill status={thread.priority} />
                            <StatusPill status={thread.status} />
                          </div>

                          {/* Confidence + Sentiment indicator */}
                          <div className="flex items-center gap-3 mt-0.5">
                            <div className="flex items-center gap-1.5">
                              <span className="text-[9px] text-white/25">AI_CONF</span>
                              <div className="confidence-bar w-14">
                                <div
                                  className="confidence-bar-fill"
                                  style={{
                                    width: `${thread.confidence * 100}%`,
                                    background: `linear-gradient(90deg, var(--palette-sky), var(--palette-yellow))`,
                                  }}
                                />
                              </div>
                              <span className="text-[9px] text-[var(--palette-sky)] font-bold">{Math.round(thread.confidence * 100)}%</span>
                            </div>

                            <div className="flex items-center gap-1">
                              <span className="text-[9px] text-white/25">POLAR</span>
                              <div
                                className="w-1.5 h-1.5 rounded-full"
                                style={{ background: getSentimentColor(thread.sentiment_score) }}
                                title={`Sentiment: ${thread.sentiment_score}`}
                              />
                            </div>
                          </div>

                          {/* Flags (High-contrast sci-fi pill) */}
                          {thread.flags.length > 0 && (
                            <div className="flex gap-1 mt-0.5">
                              {thread.flags.map(flag => (
                                <span
                                  key={flag}
                                  className="text-[8px] px-1.5 py-0.2 rounded bg-[rgba(248,162,196,0.06)] text-[var(--accent-pink)] border border-[rgba(248,162,196,0.15)] font-bold font-mono tracking-wider uppercase"
                                >
                                  {flag.replace('_', ' ')}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    </GlowCard>
                  </Link>
                </motion.div>
              ))
            ) : (
              /* Holographic Radar Empty State */
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="py-12 border border-white/5 rounded-xl bg-black/10 flex flex-col items-center justify-center text-center relative overflow-hidden"
              >
                <div className="w-48 h-48 rounded-full border border-[rgba(140,192,235,0.15)] relative overflow-hidden flex items-center justify-center mb-6 bg-black/20 select-none">
                  {/* Conic radial scanner sweep */}
                  <div className="absolute inset-0 bg-[conic-gradient(from_0deg,transparent_40%,rgba(140,192,235,0.25)_90%,rgba(140,192,235,0.4)_100%)] animate-[spin_4s_linear_infinite]" />
                  
                  {/* Coordinates Grid */}
                  <div className="absolute w-full h-[1px] bg-white/5" />
                  <div className="absolute h-full w-[1px] bg-white/5" />
                  <div className="w-36 h-36 rounded-full border border-white/5" />
                  <div className="w-24 h-24 rounded-full border border-white/5" />
                  <div className="w-12 h-12 rounded-full border border-white/5" />
                  <Radio className="w-6 h-6 text-[var(--palette-sky)] animate-pulse relative z-10" />
                </div>
                <h3 className="font-mono text-xs text-[var(--palette-yellow)] tracking-wider mb-1">NO ACTIVE CHANNELS FOUND</h3>
                <p className="font-mono text-[9px] text-white/30 max-w-sm uppercase leading-normal px-4">
                  Broadband radar scan on query "{searchQuery}" returned 0 matches. Verify transceivers or reset filters.
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Right 1 column: Telemetry Event Ticker Monitor */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 font-mono text-[9px] text-white/20 border-b border-white/5 pb-2 mb-2 select-none">
            <Terminal className="w-3 h-3 text-[var(--palette-yellow)]" />
            <span>REALTIME_DIAGNOSTICS_STREAM</span>
          </div>

          <GlowCard className="p-3 bg-[#0a0e17]/80 h-[480px] flex flex-col justify-start overflow-hidden relative" hoverable={false} glowColor="rgba(255,235,204,0.1)">
            {/* High tech diagnostic HUD header */}
            <div className="font-mono text-[8px] text-[var(--palette-peach)]/60 mb-2 border-b border-white/5 pb-1 flex justify-between select-none">
              <span>STREAM: ACTIVE_TELEMETRY</span>
              <span className="pulse-dot bg-[var(--accent-green)] scale-75" />
            </div>
            
            {/* Scroll log feed */}
            <div className="flex-1 overflow-y-auto space-y-2.5 font-mono text-[9px] text-white/40 scrollbar leading-relaxed">
              <AnimatePresence>
                {logs.map((log, index) => (
                  <motion.div
                    key={index + '-' + log.substring(0, 8)}
                    initial={{ opacity: 0, x: 10 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="border-l border-white/5 pl-2 py-0.5 hover:bg-white/[0.01] transition-all"
                  >
                    {log}
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
            
            {/* Footer log specs */}
            <div className="font-mono text-[7px] text-white/20 mt-2 border-t border-white/5 pt-1.5 select-none uppercase">
              RECEPTOR: PORT_3000 // STABLE
            </div>
          </GlowCard>
        </div>
      </div>
    </div>
  );
}
