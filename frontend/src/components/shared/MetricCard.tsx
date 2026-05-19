'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface MetricCardProps {
  label: string;
  value: string | number;
  icon: string;
  trend?: { value: number; label: string };
  accentColor?: string;
  delay?: number;
}

export default function MetricCard({ 
  label, 
  value, 
  icon, 
  trend, 
  accentColor = 'var(--palette-sky)', 
  delay = 0 
}: MetricCardProps) {
  const [displayValue, setDisplayValue] = useState<string | number>(typeof value === 'number' ? 0 : value);

  useEffect(() => {
    // If it's a numeric value or percentage, we can count up
    if (typeof value === 'number') {
      let start = 0;
      const end = value;
      if (start === end) return;
      
      const duration = 1200; // ms
      const increment = end / (duration / 16); // ~60fps
      
      const timer = setInterval(() => {
        start += increment;
        if (start >= end) {
          clearInterval(timer);
          setDisplayValue(end);
        } else {
          setDisplayValue(Math.floor(start));
        }
      }, 16);
      
      return () => clearInterval(timer);
    } else if (typeof value === 'string' && value.endsWith('%')) {
      const numericVal = parseInt(value);
      if (isNaN(numericVal)) {
        setDisplayValue(value);
        return;
      }
      
      let start = 0;
      const duration = 1000;
      const increment = numericVal / (duration / 16);
      
      const timer = setInterval(() => {
        start += increment;
        if (start >= numericVal) {
          clearInterval(timer);
          setDisplayValue(`${numericVal}%`);
        } else {
          setDisplayValue(`${Math.floor(start)}%`);
        }
      }, 16);
      
      return () => clearInterval(timer);
    } else {
      setDisplayValue(value);
    }
  }, [value]);

  // Generate random path for mock sparkline
  const sparklinePath = useEffect(() => {}, []); // empty but forces render
  const pathData = "M 0 15 Q 15 5, 30 18 T 60 8 T 90 20 T 120 5";

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
      className="glass-card p-5 hover-lift corner-brackets border border-white/5 relative"
      style={{ 
        borderColor: `${accentColor}18`,
        boxShadow: `0 0 25px ${accentColor}05`
      }}
    >
      {/* HUD corner marker */}
      <div className="absolute top-1.5 left-1.5 font-mono text-[6px] text-white/20 select-none">
        [ SYS_TEL_{label.substring(0, 3).toUpperCase()} ]
      </div>

      <div className="flex items-start justify-between mb-4 mt-1 select-none">
        <span className="text-xl filter drop-shadow-[0_0_8px_rgba(255,255,255,0.2)]">{icon}</span>
        {trend && (
          <span className={cn(
            'text-[10px] font-mono font-bold px-2 py-0.5 rounded border',
            trend.value >= 0 
              ? 'bg-[rgba(162,248,211,0.06)] border-[rgba(162,248,211,0.2)] text-[var(--accent-green)]' 
              : 'bg-red-500/10 border-red-500/20 text-[var(--accent-pink)]'
          )}>
            {trend.value >= 0 ? '▲' : '▼'} {Math.abs(trend.value)}%
          </span>
        )}
      </div>

      <div className="flex items-end justify-between">
        <div>
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4, delay: delay + 0.15 }}
            className="text-2xl font-mono font-bold tracking-tight mb-1"
            style={{ 
              color: accentColor,
              textShadow: `0 0 15px ${accentColor}30`
            }}
          >
            {displayValue}
          </motion.div>

          <p className="text-[10px] font-mono tracking-wider uppercase text-[var(--text-secondary)]/50">
            {label}
          </p>
        </div>

        {/* Telemetry micro sparkline */}
        <div className="w-16 h-8 opacity-40 shrink-0 pointer-events-none">
          <svg viewBox="0 0 120 25" className="w-full h-full">
            <path
              d={pathData}
              fill="none"
              stroke={accentColor}
              strokeWidth="2"
              strokeLinecap="round"
              className="path-draw"
            />
          </svg>
        </div>
      </div>
    </motion.div>
  );
}
