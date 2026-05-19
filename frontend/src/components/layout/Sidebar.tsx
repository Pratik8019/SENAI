'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { 
  Activity, 
  BarChart3, 
  Terminal, 
  Cpu, 
  ChevronRight, 
  ShieldAlert, 
  UserCheck
} from 'lucide-react';

const navItems = [
  { 
    href: '/mission-control', 
    label: 'Mission Control', 
    subLabel: 'Real-time Threat Monitoring',
    icon: Activity,
    badge: 'LIVE'
  },
  { 
    href: '/analytics', 
    label: 'Command Center', 
    subLabel: 'AI & Node Telemetry',
    icon: BarChart3,
    badge: '98%'
  },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <motion.aside
      initial={{ x: -80, opacity: 0 }}
      animate={{ 
        x: 0, 
        opacity: 1,
        width: isExpanded ? 240 : 72
      }}
      onMouseEnter={() => setIsExpanded(true)}
      onMouseLeave={() => setIsExpanded(false)}
      transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
      className="fixed left-0 top-0 h-full flex flex-col items-stretch py-5 z-50 select-none"
      style={{
        background: 'rgba(5, 7, 12, 0.85)',
        backdropFilter: 'blur(30px)',
        borderRight: '1px solid rgba(140, 192, 235, 0.08)',
        boxShadow: isExpanded ? '10px 0 40px rgba(0, 0, 0, 0.5)' : 'none',
      }}
    >
      {/* Top Brand / Logo */}
      <div className="px-4 mb-8 flex items-center gap-3">
        <Link href="/mission-control" className="shrink-0">
          <motion.div
            whileHover={{ scale: 1.05, rotate: 90 }}
            whileTap={{ scale: 0.95 }}
            className="w-10 h-10 rounded-lg flex items-center justify-center text-sm font-mono font-black"
            style={{
              background: 'linear-gradient(135deg, var(--palette-sky) 0%, var(--palette-yellow) 100%)',
              boxShadow: '0 0 15px rgba(140, 192, 235, 0.3)',
              color: '#04060a'
            }}
          >
            Ω
          </motion.div>
        </Link>
        <motion.div
          animate={{ opacity: isExpanded ? 1 : 0, x: isExpanded ? 0 : -10 }}
          transition={{ duration: 0.2 }}
          className={cn("flex flex-col min-w-0", !isExpanded && "pointer-events-none absolute")}
        >
          <span className="text-xs font-mono font-bold tracking-wider text-white">SENTINEL_AI</span>
          <span className="text-[9px] font-mono text-[var(--palette-yellow)]/70 uppercase">SECURE NETWORK</span>
        </motion.div>
      </div>

      {/* Grid crosshair corner decorations inside sidebar */}
      <div className="absolute top-2 right-2 text-[8px] font-mono text-white/5 pointer-events-none">
        [+] SYS_LOC_01
      </div>

      {/* Navigation list */}
      <nav className="flex flex-col gap-1.5 px-3 flex-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
          
          return (
            <Link key={item.href} href={item.href} className="outline-none">
              <motion.div
                className={cn(
                  'flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-all duration-150 relative group',
                  isActive
                    ? 'bg-[rgba(140,192,235,0.06)] border-l-2 border-[var(--palette-sky)] text-white'
                    : 'text-[var(--text-secondary)]/70 hover:bg-white/3 hover:text-white'
                )}
              >
                <div className="shrink-0 flex items-center justify-center w-6 h-6">
                  <Icon className={cn("w-4 h-4 transition-transform group-hover:scale-110", isActive ? "text-[var(--palette-sky)]" : "text-white/40")} />
                </div>

                <motion.div
                  animate={{ opacity: isExpanded ? 1 : 0, x: isExpanded ? 0 : -10 }}
                  transition={{ duration: 0.2 }}
                  className={cn("flex flex-col min-w-0 flex-1", !isExpanded && "pointer-events-none absolute")}
                >
                  <span className="text-xs font-medium tracking-tight truncate">{item.label}</span>
                  <span className="text-[9px] text-white/30 truncate leading-none mt-0.5">{item.subLabel}</span>
                </motion.div>

                {/* Badge shown only when expanded */}
                {isExpanded && item.badge && (
                  <span className="text-[8px] font-mono px-1.5 py-0.5 rounded bg-white/5 border border-white/10 text-[var(--palette-yellow)] shrink-0">
                    {item.badge}
                  </span>
                )}

                {/* Hover scanline indicator */}
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-[rgba(140,192,235,0.02)] to-transparent opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity" />
              </motion.div>
            </Link>
          );
        })}
      </nav>

      {/* Footer system details */}
      <div className="px-4 mt-auto flex flex-col gap-3">
        <motion.div
          animate={{ opacity: isExpanded ? 1 : 0 }}
          className={cn("flex flex-col gap-1.5 p-2 rounded bg-white/[0.02] border border-white/5 font-mono text-[9px] text-white/40", !isExpanded && "hidden")}
        >
          <div className="flex items-center justify-between">
            <span>OPERATOR:</span>
            <span className="text-white/60">NODE_0x7A</span>
          </div>
          <div className="flex items-center justify-between">
            <span>CLEARANCE:</span>
            <span className="text-[var(--palette-peach)] font-bold">L4_SECRET</span>
          </div>
          <div className="flex items-center justify-between">
            <span>PING:</span>
            <span className="text-[var(--accent-green)]">14ms</span>
          </div>
        </motion.div>

        <div className="flex items-center gap-3 p-1">
          <div className="pulse-dot bg-[var(--accent-green)] shrink-0 ml-1.5" />
          <motion.div
            animate={{ opacity: isExpanded ? 1 : 0, x: isExpanded ? 0 : -10 }}
            className={cn("flex flex-col text-[10px] font-mono text-white/40", !isExpanded && "absolute pointer-events-none opacity-0")}
          >
            <span className="text-white/60 leading-none">SYS_ACTIVE</span>
            <span className="text-[8px] opacity-60 mt-0.5">v1.2.9-ALPHA</span>
          </motion.div>
        </div>
      </div>
    </motion.aside>
  );
}
