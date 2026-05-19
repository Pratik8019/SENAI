'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { ReactNode, useMemo } from 'react';

interface GlowCardProps {
  children: ReactNode;
  className?: string;
  glowColor?: string;
  onClick?: () => void;
  hoverable?: boolean;
  panelId?: string;
  showCoords?: boolean;
}

export default function GlowCard({ 
  children, 
  className, 
  glowColor = 'rgba(140, 192, 235, 0.4)', 
  onClick, 
  hoverable = true,
  panelId,
  showCoords = false
}: GlowCardProps) {
  // Generate random stable coordinates based on panelId or standard seed
  const coords = useMemo(() => {
    const seed = panelId ? panelId.charCodeAt(0) + panelId.charCodeAt(panelId.length - 1) : 42;
    const lat = (45 + (seed % 10) * 0.231).toFixed(4);
    const lon = (-122 - (seed % 7) * 0.179).toFixed(4);
    return `${lat}° N, ${lon}° W`;
  }, [panelId]);

  return (
    <motion.div
      whileHover={hoverable ? { y: -2, scale: 1.002 } : {}}
      transition={{ duration: 0.25, ease: 'easeOut' }}
      onClick={onClick}
      className={cn(
        'glass-card p-5 transition-all duration-300 corner-brackets relative group/card border border-white/5',
        hoverable && 'hover:border-white/15',
        onClick && 'cursor-pointer',
        className
      )}
      style={{
        boxShadow: glowColor ? `0 0 30px ${glowColor}08, inset 0 0 20px ${glowColor}03` : undefined,
        borderColor: glowColor ? `${glowColor}1a` : undefined,
      }}
    >
      {/* HUD Header Bar when panelId or showCoords is active */}
      {(panelId || showCoords) && (
        <div className="flex items-center justify-between border-b border-white/5 pb-2 mb-3 font-mono text-[8px] text-white/20 select-none">
          {panelId ? (
            <span className="text-[var(--palette-yellow)]/50 tracking-widest font-bold">
              // PANEL_{panelId.toUpperCase()}
            </span>
          ) : (
            <span />
          )}
          {showCoords && (
            <span className="opacity-60">{coords}</span>
          )}
        </div>
      )}

      {/* Decorative cyber grid details */}
      <div className="absolute top-1.5 right-1.5 w-1 h-1 rounded-full bg-white/10 group-hover/card:bg-[var(--palette-sky)]/40 transition-colors" />

      {/* Inner card content */}
      <div className="relative z-10">
        {children}
      </div>

      {/* Subtle overlay glare */}
      <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-[rgba(255,249,210,0.01)] to-[rgba(140,192,235,0.03)] opacity-0 group-hover/card:opacity-100 transition-opacity duration-500 pointer-events-none" />
    </motion.div>
  );
}
