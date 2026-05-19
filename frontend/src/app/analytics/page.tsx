'use client';

import { motion } from 'framer-motion';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import TopBar from '@/components/layout/TopBar';
import GlowCard from '@/components/shared/GlowCard';
import MetricCard from '@/components/shared/MetricCard';
import { Terminal, Database, Activity, ShieldAlert, Cpu } from 'lucide-react';

// Demo analytics data
const sentimentTrend = Array.from({ length: 30 }, (_, i) => ({
  date: new Date(Date.now() - (29 - i) * 86400000).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
  score: parseFloat((Math.sin(i / 5) * 0.35 + Math.random() * 0.15 - 0.05).toFixed(2)),
  count: Math.floor(Math.random() * 15 + 5),
}));

const categories = [
  { name: 'Support Operations', value: 38, color: '#8cc0eb' },
  { name: 'Billing Systems', value: 24, color: '#bfddf0' },
  { name: 'Legal Vectors', value: 8, color: '#f8a2c4' },
  { name: 'Security Audits', value: 6, color: '#fff9d2' },
  { name: 'Feature Requests', value: 15, color: '#a2f8d3' },
  { name: 'Customer Grievances', value: 9, color: '#ffebcc' },
];

const heatmapData = Array.from({ length: 7 }, (_, day) =>
  Array.from({ length: 24 }, (_, hour) => ({
    day, hour,
    count: Math.floor(Math.random() * 5 * (hour > 8 && hour < 18 ? 2.1 : 0.4) * (day < 5 ? 1.4 : 0.35)),
  }))
).flat();

const performanceData = [
  { metric: 'Autonomous Resolve Integrity', value: 68 },
  { metric: 'Avg Classification Confidence', value: 84 },
  { metric: 'SLA Vector Compliance', value: 92 },
  { metric: 'Manual Escalation Coefficient', value: 15 },
];

const atRiskCustomers = [
  { name: 'Mike Johnson', company: 'BigRetail Inc', risk: 0.87, sentiment: -0.8, threads: 5, status: 'CRITICAL_RISK' },
  { name: 'Tom Harris', company: 'CyberSec Solutions', risk: 0.82, sentiment: -0.7, threads: 3, status: 'HIGH_ALERT' },
  { name: 'David Kim', company: 'FinancePlus', risk: 0.75, sentiment: -0.85, threads: 4, status: 'EVALUATION' },
  { name: 'James Wilson', company: 'Wilson & Associates', risk: 0.91, sentiment: -0.95, threads: 1, status: 'IMMINENT_CHURN' },
];

const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

// Custom Cybernetic Tooltip Component
const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-[#05070c]/95 border border-[rgba(140,192,235,0.25)] p-3 rounded-lg shadow-xl font-mono text-[9px] text-[var(--text-secondary)] min-w-[120px] select-none">
        <div className="border-b border-white/5 pb-1 mb-1.5 font-bold text-white uppercase tracking-widest text-[8px]">
          // DATA_VECTOR: {label}
        </div>
        <div className="flex justify-between items-center gap-4">
          <span>VAL:</span>
          <span className="text-[var(--palette-yellow)] font-bold">{payload[0].value}</span>
        </div>
        <div className="text-[7px] text-white/20 mt-1 uppercase">NODE_LATENCY: 14ms</div>
      </div>
    );
  }
  return null;
};

export default function AnalyticsPage() {
  return (
    <div className="pb-12 min-h-screen relative">
      {/* Sci-fi layout grid overlays */}
      <div className="grid-overlay" />
      
      <TopBar title="Command Center" subtitle="Autonomous intelligence telemetry & diagnostics" />

      {/* Summary Metrics */}
      <div className="px-8 grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 relative z-10">
        <MetricCard label="TELEMETRY_COUNT" value="1247" icon="📧" trend={{ value: 18, label: '' }} accentColor="var(--palette-sky)" delay={0} />
        <MetricCard label="AUTONOMOUS_RESOLVED" value="68%" icon="🤖" trend={{ value: 5, label: '' }} accentColor="var(--palette-yellow)" delay={0.08} />
        <MetricCard label="CLASSIFICATION_CONF" value="84%" icon="🧠" trend={{ value: 3, label: '' }} accentColor="var(--palette-peach)" delay={0.16} />
        <MetricCard label="HIGH_RISK_VECTORS" value="4" icon="⚠️" trend={{ value: -2, label: '' }} accentColor="var(--accent-pink)" delay={0.24} />
      </div>

      <div className="px-8 grid grid-cols-1 lg:grid-cols-3 gap-6 relative z-10">
        {/* Sentiment Trend — spans 2 cols */}
        <motion.div
          className="lg:col-span-2"
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <GlowCard glowColor="var(--palette-sky)" hoverable={false} panelId="sent_trend" showCoords>
            <h3 className="text-[10px] font-mono font-bold text-white/60 uppercase tracking-widest mb-4 flex items-center gap-1.5 select-none">
              <Activity className="w-3.5 h-3.5 text-[var(--palette-sky)]" />
              SENTIMENT_DYNAMICS_30D
            </h3>
            
            <div className="h-[280px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={sentimentTrend}>
                  <defs>
                    <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="var(--palette-sky)" stopOpacity={0.25}/>
                      <stop offset="95%" stopColor="var(--palette-sky)" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(140,192,235,0.03)" />
                  <XAxis dataKey="date" tick={{ fill: 'rgba(255,255,255,0.25)', fontSize: 9, fontFamily: 'monospace' }} tickLine={false} axisLine={false} interval={4} />
                  <YAxis tick={{ fill: 'rgba(255,255,255,0.25)', fontSize: 9, fontFamily: 'monospace' }} tickLine={false} axisLine={false} domain={[-1, 1]} />
                  <Tooltip content={<CustomTooltip />} />
                  <Area
                    type="monotone"
                    dataKey="score"
                    stroke="var(--palette-sky)"
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#colorScore)"
                    dot={false}
                    activeDot={{ r: 4, fill: 'var(--palette-yellow)', stroke: '#04060a', strokeWidth: 1.5 }}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </GlowCard>
        </motion.div>

        {/* Category Donut */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.18 }}
        >
          <GlowCard glowColor="var(--palette-yellow)" hoverable={false} panelId="cat_break" showCoords>
            <h3 className="text-[10px] font-mono font-bold text-white/60 uppercase tracking-widest mb-4 flex items-center gap-1.5 select-none">
              <Database className="w-3.5 h-3.5 text-[var(--palette-yellow)]" />
              CATEGORY_DISTRIBUTION
            </h3>
            
            <div className="h-[180px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={categories}
                    cx="50%" cy="50%"
                    innerRadius={50}
                    outerRadius={72}
                    paddingAngle={3}
                    dataKey="value"
                  >
                    {categories.map((entry, index) => (
                      <Cell key={index} fill={entry.color} opacity={0.9} stroke="rgba(4,6,10,0.5)" strokeWidth={1} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ background: '#05070c', border: '1px solid rgba(140,192,235,0.2)', borderRadius: 8, fontFamily: 'monospace', fontSize: 10 }}
                    itemStyle={{ fontSize: 10 }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
            
            <div className="grid grid-cols-2 gap-1.5 mt-3 select-none font-mono text-[8px]">
              {categories.map(cat => (
                <div key={cat.name} className="flex items-center gap-1.5 text-white/45 truncate">
                  <span className="w-1.5 h-1.5 rounded-full shrink-0" style={{ background: cat.color }} />
                  <span className="truncate">{cat.name}</span>
                </div>
              ))}
            </div>
          </GlowCard>
        </motion.div>

        {/* Escalation Heatmap */}
        <motion.div
          className="lg:col-span-2"
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.26 }}
        >
          <GlowCard glowColor="var(--accent-pink)" hoverable={false} panelId="esc_map" showCoords>
            <h3 className="text-[10px] font-mono font-bold text-white/60 uppercase tracking-widest mb-4 flex items-center gap-1.5 select-none">
              <ShieldAlert className="w-3.5 h-3.5 text-[var(--accent-pink)]" />
              ESCALATION_COEFFICIENT_HEATMAP
            </h3>
            
            <div className="overflow-x-auto select-none">
              <div className="min-w-[600px] pb-1">
                {/* Hour labels */}
                <div className="flex mb-1.5 ml-10">
                  {Array.from({ length: 24 }, (_, h) => (
                    <div key={h} className="flex-1 text-center text-[8px] text-white/20 font-mono">
                      {h % 3 === 0 ? `${h}H` : ''}
                    </div>
                  ))}
                </div>
                {/* Grid rows */}
                {Array.from({ length: 7 }, (_, day) => (
                  <div key={day} className="flex items-center mb-[3px]">
                    <span className="text-[9px] text-white/25 w-10 text-right pr-3 font-mono font-bold">{DAYS[day].toUpperCase()}</span>
                    <div className="flex flex-1 gap-[3px]">
                      {Array.from({ length: 24 }, (_, hour) => {
                        const cell = heatmapData.find(c => c.day === day && c.hour === hour);
                        const count = cell?.count || 0;
                        const intensity = Math.min(count / 8, 1);
                        return (
                          <div
                            key={hour}
                            className="flex-1 aspect-square rounded-[1px] transition-all hover:scale-135 hover:z-10 cursor-pointer border border-white/[0.02]"
                            style={{
                              background: count === 0
                                ? 'rgba(255,255,255,0.02)'
                                : `rgba(248, 162, 196, ${intensity * 0.75 + 0.1})`,
                            }}
                            title={`${DAYS[day]} ${hour}:00 — ${count} anomalies`}
                          />
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </GlowCard>
        </motion.div>

        {/* AI Performance */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.32 }}
        >
          <GlowCard glowColor="var(--palette-peach)" hoverable={false} panelId="ai_perf" showCoords>
            <h3 className="text-[10px] font-mono font-bold text-white/60 uppercase tracking-widest mb-4 flex items-center gap-1.5 select-none">
              <Cpu className="w-3.5 h-3.5 text-[var(--palette-peach)]" />
              INTELLIGENCE_INTEGRITY
            </h3>
            
            <div className="space-y-4 font-mono select-none">
              {performanceData.map((item, idx) => (
                <div key={idx}>
                  <div className="flex items-center justify-between mb-1 text-[9px]">
                    <span className="text-white/40">{item.metric}</span>
                    <span className="font-bold text-[var(--palette-yellow)]">
                      {item.value}%
                    </span>
                  </div>
                  <div className="h-1.5 rounded-full bg-white/5 overflow-hidden border border-white/5">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${item.value}%` }}
                      transition={{ duration: 1, delay: 0.4 + idx * 0.08 }}
                      className="h-full rounded-full"
                      style={{
                        background: `linear-gradient(90deg, var(--palette-sky), var(--palette-peach))`
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </GlowCard>
        </motion.div>

        {/* At-Risk Customers */}
        <motion.div
          className="lg:col-span-3"
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <GlowCard glowColor="var(--palette-sky)" hoverable={false} panelId="risk_matrix" showCoords>
            <h3 className="text-[10px] font-mono font-bold text-white/60 uppercase tracking-widest mb-4 select-none">
              ⚠️ AT_RISK_NODE_CLIENTS
            </h3>
            
            <div className="overflow-x-auto select-none">
              <table className="w-full text-xs font-mono">
                <thead>
                  <tr className="border-b border-white/5 pb-2 text-white/25 uppercase text-[9px]">
                    <th className="text-left py-2 font-bold">CLIENT_IDENTIFIER</th>
                    <th className="text-left py-2 font-bold">NODE_COMPANY</th>
                    <th className="text-center py-2 font-bold">RISK_RATIO</th>
                    <th className="text-center py-2 font-bold">SENTIMENT_POLARITY</th>
                    <th className="text-center py-2 font-bold">NODES</th>
                    <th className="text-right py-2 font-bold">STATUS</th>
                  </tr>
                </thead>
                <tbody>
                  {atRiskCustomers.map((customer, idx) => (
                    <motion.tr
                      key={idx}
                      initial={{ opacity: 0, x: -5 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.45 + idx * 0.08 }}
                      className="border-b border-white/3 hover:bg-white/[0.01] transition-colors"
                    >
                      <td className="py-3 text-white/70 font-bold">{customer.name}</td>
                      <td className="py-3 text-white/40">{customer.company}</td>
                      <td className="py-3 text-center">
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold" style={{
                          color: customer.risk > 0.8 ? 'var(--accent-pink)' : 'var(--palette-peach)',
                          background: customer.risk > 0.8 ? 'rgba(248,162,196,0.06)' : 'rgba(255,235,204,0.06)',
                          border: `1px solid ${customer.risk > 0.8 ? 'rgba(248,162,196,0.15)' : 'rgba(255,235,204,0.15)'}`
                        }}>
                          {(customer.risk * 100).toFixed(0)}%
                        </span>
                      </td>
                      <td className="py-3 text-center">
                        <span className="text-[10px] font-bold" style={{ color: customer.sentiment < -0.5 ? 'var(--accent-pink)' : 'var(--palette-peach)' }}>
                          {customer.sentiment.toFixed(2)}
                        </span>
                      </td>
                      <td className="py-3 text-center text-white/40">{customer.threads}</td>
                      <td className="py-3 text-right">
                        <span className="text-[9px] font-bold px-1.5 py-0.5 bg-white/5 border border-white/10 rounded text-white/60">
                          {customer.status}
                        </span>
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          </GlowCard>
        </motion.div>
      </div>
    </div>
  );
}
