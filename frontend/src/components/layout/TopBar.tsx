'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface TopBarProps {
  title: string;
  subtitle?: string;
}

const TICKER_LOGS = [
  "SYSTEM_STATUS: ALL CORE NEURAL SYSTEMS NOMINAL",
  "SECURE_GATEWAY: ACTIVE ON PORT_8080 // THREAT FILTERING ENABLED",
  "AGENT_ALPHA: MONITORING INBOUND SENSORY VECTORS",
  "RAG_ENGINE: DATA STORES MAP RE-INDEXED",
  "AUDIT_DAEMON: RATES & ESCALATIONS CALIBRATED",
  "SECURITY_PROTOCOL_L4: DETECTING MALICIOUS LOGINS [0 IN QUEUE]",
  "SENTIMENT_MODULE: REALTIME POLARITY SCORING CALIBRATED",
];

export default function TopBar({ title, subtitle }: TopBarProps) {
  const [time, setTime] = useState('');
  const [tickerIdx, setTickerIdx] = useState(0);

  useEffect(() => {
    // Clock tick
    const updateTime = () => {
      setTime(new Date().toLocaleTimeString('en-US', { hour12: false }));
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);

    // Ticker cycle
    const tickerInterval = setInterval(() => {
      setTickerIdx((prev) => (prev + 1) % TICKER_LOGS.length);
    }, 4500);

    return () => {
      clearInterval(interval);
      clearInterval(tickerInterval);
    };
  }, []);

  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.4, delay: 0.1 }}
      className="flex flex-col border-b border-white/5 bg-[#04060a]/40 backdrop-blur-md px-8 py-4 relative z-40"
    >
      <div className="flex items-center justify-between w-full">
        {/* Left: Titles & Coords */}
        <div className="flex items-center gap-5">
          <div>
            <h1 className="text-lg font-mono font-bold tracking-wider text-white uppercase flex items-center gap-2">
              <span className="text-[var(--palette-sky)]">/</span>
              {title}
            </h1>
            {subtitle && (
              <p className="text-[10px] font-mono text-[var(--text-secondary)]/50 mt-0.5 uppercase tracking-wider">
                {subtitle}
              </p>
            )}
          </div>

          <div className="hidden lg:flex flex-col border-l border-white/10 pl-5 font-mono text-[9px] text-white/20">
            <div>COORDS: 47.6062° N, 122.3321° W</div>
            <div className="text-[var(--palette-yellow)]/40">CORE: 0x9F_AGENT_V2</div>
          </div>
        </div>

        {/* Center: Live Terminal Ticker */}
        <div className="hidden md:flex flex-1 max-w-md mx-6 px-3 py-1.5 rounded bg-black/40 border border-white/5 font-mono text-[9px] text-[var(--palette-sky)]/90 items-center gap-2 overflow-hidden h-7">
          <span className="w-1.5 h-1.5 rounded-full bg-[var(--palette-sky)] animate-pulse shrink-0" />
          <span className="text-white/20 uppercase font-black tracking-widest text-[8px] shrink-0">DIAG:</span>
          <div className="relative flex-1 h-3 overflow-hidden">
            <AnimatePresence mode="wait">
              <motion.span
                key={tickerIdx}
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                exit={{ y: -10, opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="absolute inset-0 truncate whitespace-nowrap block"
              >
                {TICKER_LOGS[tickerIdx]}
              </motion.span>
            </AnimatePresence>
          </div>
        </div>

        {/* Right: Telemetry & Live Clock */}
        <div className="flex items-center gap-4 shrink-0">
          {/* Active node details */}
          <div className="hidden sm:flex flex-col text-right font-mono text-[9px] text-white/30">
            <span>SYS_SYS: OK</span>
            <span className="text-[var(--accent-green)]/70">BANDWIDTH: 942Mbps</span>
          </div>

          {/* Live indicator */}
          <div className="flex items-center gap-2 px-2.5 py-1 rounded bg-[rgba(162,248,211,0.06)] border border-[rgba(162,248,211,0.15)]">
            <div className="pulse-dot bg-[var(--accent-green)]" />
            <span className="text-[9px] font-mono font-bold text-[var(--accent-green)] tracking-wider">
              ONLINE
            </span>
          </div>

          {/* Timestamp */}
          <div className="text-xs font-mono text-[var(--text-secondary)] bg-white/5 px-2.5 py-1 rounded border border-white/5 min-w-[70px] text-center">
            {time}
          </div>
        </div>
      </div>
    </motion.header>
  );
}
