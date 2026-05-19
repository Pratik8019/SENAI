'use client';

import { useState, useMemo, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import TopBar from '@/components/layout/TopBar';
import GlowCard from '@/components/shared/GlowCard';
import StatusPill from '@/components/shared/StatusPill';
      received_at: new Date(Date.now() - 3600000).toISOString(), sentiment_score: -0.6,
    },
  ],
  classification: { category: 'billing', sentiment: 'negative', sentiment_score: -0.6, urgency: 'high', confidence: 0.89, requires_human: false, suggested_reply: 'Dear Sarah, thank you for bringing this to our attention. I can see the billing discrepancy on invoice #INV-2024-0891. You are correct — you should be charged for 12 seats on the Professional plan. I\'ve issued a credit of $500 to your account, which will be reflected on your next invoice. I apologize for the inconvenience.', summary: 'Customer reporting $500 overcharge on invoice, asking for correction.' },
  agentTrace: [
    { step: 1, thought: 'Customer is reporting a billing discrepancy. I need to check the knowledge base for our billing and refund policies.', action: 'search_knowledge_base', input: { query: 'billing discrepancy overcharge refund' }, observation: 'Found pricing_policy.md: Professional plan is $149/seat/month. Refund policy allows corrections for billing errors.' },
    { step: 2, thought: 'Good, I have the policy context. Now let me check the customer\'s account status to verify the seat count.', action: 'check_account_status', input: { email: 'sarah.chen@acmecorp.com' }, observation: 'Account: Active, Plan: Professional, Seats: 12, MRR: $1,788/month, Payment: Up to date' },
    { step: 3, thought: 'The account shows 12 seats but they were charged for 15. This is a valid billing error. I should draft a correction response.', action: 'draft_reply', input: { context: 'Billing error: charged for 15 seats instead of 12', tone: 'apologetic' }, observation: 'Draft reply generated with apology and credit confirmation.' },
    { step: 4, thought: 'Final Answer: This is a legitimate billing error. The customer was overcharged $500 (3 extra seats × $149 + tax adjustments). Recommended actions: 1) Issue $500 credit, 2) Send drafted apology reply, 3) Flag billing system for audit. Confidence: 0.89', action: null, input: null, observation: null },
  ],
  ragContext: [
    { source: 'pricing_policy.md', relevance: 0.94, snippet: 'Professional — $149/month per seat. Up to 25 team members. Overages billed at $0.01/email beyond plan limits.' },
    { source: 'refund_policy.md', relevance: 0.87, snippet: 'Full Refund (100%): Billing error by SentinelAI. Process: Review completed within 5 business days.' },
    { source: 'sla_policy.md', relevance: 0.62, snippet: 'P3 — Medium: Minor feature issue, workaround available. Professional SLA: 24 hours response time.' },
  ],
};

export default function ThreadPage() {
  const [showAgent, setShowAgent] = useState(true);
  const [activePanel, setActivePanel] = useState<'trace' | 'rag' | 'contact'>('trace');
  const thread = DEMO_THREAD;

  return (
    <div className="pb-8">
      <TopBar title="Thread Intelligence" subtitle={thread.subject} />

      {/* Thread header bar */}
      <div className="px-8 mb-6">
        <div className="glass-card p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link href="/mission-control" className="text-white/30 hover:text-white/60 text-sm transition-colors">
              ← Back
            </Link>
            <div className="w-px h-5 bg-white/10" />
            <StatusPill status={thread.priority} size="md" />
            <StatusPill status={thread.status} size="md" />
            <span className="text-xs text-white/30 font-mono">💳 {thread.category}</span>
          </div>
          <div className="flex items-center gap-2">
            <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
              className="px-3 py-1.5 rounded-lg text-xs font-medium bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 hover:bg-cyan-500/30 transition-all">
              🤖 Run Agent
            </motion.button>
            <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
              className="px-3 py-1.5 rounded-lg text-xs font-medium bg-red-500/20 text-red-300 border border-red-500/30 hover:bg-red-500/30 transition-all">
              🚨 Escalate
            </motion.button>
          </div>
        </div>
      </div>

      <div className="px-8 grid grid-cols-5 gap-6">
        {/* Left: Conversation Timeline (3 cols) */}
        <div className="col-span-3 space-y-4">
          <h2 className="text-sm font-semibold text-white/50 uppercase tracking-wider mb-3">Conversation Timeline</h2>

          {thread.emails.map((email, idx) => (
            <motion.div
              key={email.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.15 }}
            >
              <GlowCard className="relative" glowColor={getSentimentColor(email.sentiment_score)}>
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold" style={{ background: 'linear-gradient(135deg, #7c3aed, #00d4ff)' }}>
                      {email.sender_name[0]}
                    </div>
                    <div>
                      <span className="text-sm font-medium text-white/90">{email.sender_name}</span>
                      <span className="text-xs text-white/30 ml-2">{email.sender}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full" style={{ background: getSentimentColor(email.sentiment_score) }} title={`Sentiment: ${email.sentiment_score}`} />
                    <span className="text-[11px] text-white/25 font-mono">
                      {new Date(email.received_at).toLocaleString()}
                    </span>
                  </div>
                </div>
                <p className="text-sm text-white/70 leading-relaxed whitespace-pre-wrap">{email.body}</p>
              </GlowCard>
            </motion.div>
          ))}

          {/* Suggested reply */}
          {thread.classification.suggested_reply && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }}>
              <GlowCard glowColor="#00ff88">
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-sm">🤖</span>
                  <span className="text-xs font-semibold text-green-400 uppercase tracking-wider">AI Suggested Reply</span>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-green-500/10 text-green-300 border border-green-500/20 font-mono">
                    {Math.round(thread.classification.confidence * 100)}% confidence
                  </span>
                </div>
                <p className="text-sm text-white/60 leading-relaxed">{thread.classification.suggested_reply}</p>
                <div className="flex gap-2 mt-4">
                  <motion.button whileHover={{ scale: 1.05 }} className="px-4 py-2 rounded-lg text-xs font-medium bg-green-500/20 text-green-300 border border-green-500/30">
                    ✅ Approve & Send
                  </motion.button>
                  <motion.button whileHover={{ scale: 1.05 }} className="px-4 py-2 rounded-lg text-xs font-medium bg-white/5 text-white/40 border border-white/10">
                    ✏️ Edit
                  </motion.button>
                </div>
              </GlowCard>
            </motion.div>
          )}
        </div>

        {/* Right: Intelligence Sidebar (2 cols) */}
        <div className="col-span-2 space-y-4">
          {/* Panel Tabs */}
          <div className="flex gap-1 p-1 rounded-xl bg-white/3 border border-white/5">
            {(['trace', 'rag', 'contact'] as const).map(panel => (
              <button
                key={panel}
                onClick={() => setActivePanel(panel)}
                className={`flex-1 py-2 rounded-lg text-xs font-medium transition-all ${
                  activePanel === panel ? 'bg-cyan-500/20 text-cyan-300' : 'text-white/30 hover:text-white/50'
                }`}
              >
                {panel === 'trace' ? '🧠 AI Trace' : panel === 'rag' ? '📚 RAG' : '👤 Contact'}
              </button>
            ))}
          </div>

          <AnimatePresence mode="wait">
            {/* AI Reasoning Trace */}
            {activePanel === 'trace' && (
              <motion.div key="trace" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}>
                <div className="space-y-3">
                  {thread.agentTrace.map((step, idx) => (
                    <motion.div key={idx} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: idx * 0.1 }}>
                      <GlowCard className="!p-4" glowColor={step.action ? '#7c3aed' : '#00ff88'}>
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-violet-500/20 text-violet-300 font-mono font-bold">
                            Step {step.step}
                          </span>
                          {step.action && (
                            <span className="text-[10px] px-1.5 py-0.5 rounded bg-cyan-500/15 text-cyan-300 font-mono">
                              🔧 {step.action}
                            </span>
                          )}
                        </div>

                        <p className="text-xs text-white/60 mb-2 leading-relaxed">
                          <span className="text-violet-400 font-semibold">Think: </span>
                          {step.thought}
                        </p>

                        {step.observation && (
                          <div className="mt-2 p-2 rounded-lg bg-black/20 border border-white/5">
                            <p className="text-[11px] text-white/40 font-mono leading-relaxed">
                              <span className="text-cyan-400">Observe: </span>
                              {step.observation}
                            </p>
                          </div>
                        )}
                      </GlowCard>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            )}

            {/* RAG Retrieval Panel */}
            {activePanel === 'rag' && (
              <motion.div key="rag" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}>
                <div className="space-y-3">
                  {thread.ragContext.map((ctx, idx) => (
                    <GlowCard key={idx} className="!p-4" glowColor="#ffaa00">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-xs font-medium text-amber-300 font-mono">📄 {ctx.source}</span>
                        <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-amber-500/10 text-amber-300 border border-amber-500/20 font-mono">
                          {Math.round(ctx.relevance * 100)}% match
                        </span>
                      </div>
                      <p className="text-xs text-white/50 leading-relaxed">{ctx.snippet}</p>
                    </GlowCard>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Contact Intelligence */}
            {activePanel === 'contact' && (
              <motion.div key="contact" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}>
                <GlowCard glowColor="#00d4ff">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold" style={{ background: 'linear-gradient(135deg, #00d4ff, #7c3aed)' }}>
                      {thread.contact.name[0]}
                    </div>
                    <div>
                      <h3 className="text-sm font-semibold text-white/90">{thread.contact.name}</h3>
                      <p className="text-xs text-white/40">{thread.contact.email}</p>
                    </div>
                  </div>

                  <div className="space-y-3">
                    {[
                      { label: 'Company', value: thread.contact.company },
                      { label: 'Risk Score', value: `${(thread.contact.risk_score * 100).toFixed(0)}%` },
                      { label: 'Plan', value: 'Professional' },
                      { label: 'MRR', value: '$1,788' },
                      { label: 'Member Since', value: 'Mar 2024' },
                    ].map(item => (
                      <div key={item.label} className="flex items-center justify-between py-1.5 border-b border-white/5">
                        <span className="text-xs text-white/30">{item.label}</span>
                        <span className="text-xs font-medium text-white/70">{item.value}</span>
                      </div>
                    ))}
                  </div>
                </GlowCard>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Classification Summary */}
          <GlowCard className="!p-4" glowColor="#7c3aed">
            <h4 className="text-xs font-semibold text-violet-400 uppercase tracking-wider mb-3">AI Classification</h4>
            <div className="space-y-2">
              {[
                { label: 'Category', value: thread.classification.category },
                { label: 'Sentiment', value: `${thread.classification.sentiment} (${thread.classification.sentiment_score})` },
                { label: 'Urgency', value: thread.classification.urgency },
                { label: 'Confidence', value: `${Math.round(thread.classification.confidence * 100)}%` },
                { label: 'Needs Human', value: thread.classification.requires_human ? 'Yes' : 'No' },
              ].map(item => (
                <div key={item.label} className="flex items-center justify-between">
                  <span className="text-[11px] text-white/30">{item.label}</span>
                  <span className="text-[11px] font-medium text-white/60 font-mono">{item.value}</span>
                </div>
              ))}
            </div>
            <p className="text-[11px] text-white/40 mt-3 pt-3 border-t border-white/5 leading-relaxed">
              {thread.classification.summary}
            </p>
          </GlowCard>
        </div>
      </div>
    </div>
  );
}
