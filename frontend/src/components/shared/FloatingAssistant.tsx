'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Cpu, X, Send, Terminal, AlertTriangle, ShieldCheck, Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Message {
  sender: 'user' | 'system' | 'assistant';
  text: string;
  isCode?: boolean;
}

export default function FloatingAssistant() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { sender: 'system', text: 'SENTINEL_CORE_V1.2 ONLINE. STANDBY FOR OPERATOR INPUT.' },
    { sender: 'assistant', text: 'Greetings, Operator. I am the SentinelAI Neural Assistant. Run diagnostics or query active telemetry nodes.' }
  ]);
  const [inputVal, setInputVal] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const handleCommand = async (cmd: string) => {
    setIsTyping(true);
    setMessages(prev => [...prev, { sender: 'user', text: cmd }]);
    
    // Simulate thinking delay
    await new Promise(resolve => setTimeout(resolve, 800));

    const commandClean = cmd.trim().toLowerCase();

    if (commandClean === '/scan') {
      setMessages(prev => [
        ...prev,
        { sender: 'system', text: 'DEPLOYING WIDEBAND SENSOR GRID...' },
        { sender: 'assistant', text: 'Scanning active threads...\n[12ms] Checked 10 email streams\n[40ms] RAG vectors verified (3 policy references)\n[95ms] AI auto-classification models response nominal (98% avg confidence)\n[STATUS] NO THREATS IDENTIFIED.' }
      ]);
    } else if (commandClean === '/diagnose') {
      setMessages(prev => [
        ...prev,
        { sender: 'system', text: 'INITIATING SYSTEM TELEMETRY DUMP...' },
        { sender: 'assistant', text: '• AI Response SLA: 2.4h (Optimal)\n• Rate Limiter Queue: 0/sec\n• Database pool: 14/50 active\n• Heuristic confidence index: 0.892\n• Active Escalate Rate: 15% (Within threshold)' }
      ]);
    } else if (commandClean === '/clearance') {
      setMessages(prev => [
        ...prev,
        { sender: 'assistant', text: 'OPERATOR ID: NODE_0x7A\nACCESS RANK: L4_SECRET_OPERATIONAL\nDEVICES: Localhost Web Terminal (3000)' }
      ]);
    } else {
      // General question AI reply
      setMessages(prev => [
        ...prev,
        { sender: 'assistant', text: `Analyzing query: "${cmd}". The neural core indicates all systems are operating normally. Let me know if you would like me to /scan or /diagnose the active threads.` }
      ]);
    }
    setIsTyping(false);
  };

  const handleSend = () => {
    if (!inputVal.trim()) return;
    const txt = inputVal;
    setInputVal('');
    handleCommand(txt);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 font-mono">
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 30 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 30 }}
            transition={{ duration: 0.25, ease: 'easeOut' }}
            className="w-80 sm:w-96 h-[400px] mb-4 flex flex-col rounded-xl border border-[rgba(140,192,235,0.2)] glass-card overflow-hidden shadow-2xl"
            style={{
              boxShadow: '0 10px 40px rgba(0,0,0,0.6), 0 0 30px rgba(140,192,235,0.08)',
              background: 'rgba(5, 8, 15, 0.88)'
            }}
          >
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 bg-white/[0.02] border-b border-white/5">
              <div className="flex items-center gap-2">
                <Sparkles className="w-3.5 h-3.5 text-[var(--palette-yellow)] animate-pulse" />
                <span className="text-[10px] tracking-widest text-white/80 font-bold uppercase">SENTINEL_NEURAL_COPROCESSOR</span>
              </div>
              <button 
                onClick={() => setIsOpen(false)}
                className="text-white/40 hover:text-white/80 p-0.5 rounded transition-colors"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Diagnostic Ticker */}
            <div className="px-4 py-1.5 bg-black/40 border-b border-white/5 flex items-center justify-between text-[8px] text-[var(--palette-sky)]/80 select-none">
              <span>STATUS: COGNITIVE_LOOP_ACTIVE</span>
              <span className="animate-pulse">NODE: 0x9F_STABLE</span>
            </div>

            {/* Messages Area */}
            <div 
              ref={scrollRef}
              className="flex-1 p-4 overflow-y-auto space-y-3 scrollbar text-[10px] leading-relaxed"
            >
              {messages.map((m, idx) => (
                <div 
                  key={idx} 
                  className={cn(
                    "flex flex-col max-w-[85%]",
                    m.sender === 'user' ? "ml-auto items-end" : "items-start"
                  )}
                >
                  <span className="text-[7px] text-white/20 mb-0.5 uppercase tracking-widest font-black">
                    {m.sender}
                  </span>
                  
                  {m.sender === 'system' ? (
                    <div className="p-2 rounded bg-amber-500/5 border border-amber-500/10 text-[var(--palette-peach)]/90 whitespace-pre-wrap font-bold">
                      {m.text}
                    </div>
                  ) : m.sender === 'user' ? (
                    <div className="p-2 rounded bg-[rgba(140,192,235,0.1)] border border-[rgba(140,192,235,0.15)] text-white whitespace-pre-wrap">
                      {m.text}
                    </div>
                  ) : (
                    <div className="p-2 rounded bg-white/[0.03] border border-white/5 text-[var(--palette-ice)] whitespace-pre-wrap">
                      {m.text}
                    </div>
                  )}
                </div>
              ))}

              {isTyping && (
                <div className="flex items-center gap-1.5 text-white/30 text-[9px]">
                  <span className="w-1.5 h-1.5 rounded-full bg-white/30 animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-1.5 h-1.5 rounded-full bg-white/30 animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-1.5 h-1.5 rounded-full bg-white/30 animate-bounce" style={{ animationDelay: '300ms' }} />
                  <span className="text-[8px] italic font-sans pl-1">coprocessor computing...</span>
                </div>
              )}
            </div>

            {/* Predefined Quick Command buttons */}
            <div className="px-4 py-2 flex gap-1.5 border-t border-white/5 bg-black/20 select-none">
              <button 
                onClick={() => handleCommand('/scan')}
                className="px-2 py-0.5 rounded text-[8px] bg-white/5 border border-white/10 hover:border-[var(--palette-sky)]/30 hover:bg-[rgba(140,192,235,0.05)] text-[var(--palette-sky)] transition-all cursor-pointer"
              >
                /scan
              </button>
              <button 
                onClick={() => handleCommand('/diagnose')}
                className="px-2 py-0.5 rounded text-[8px] bg-white/5 border border-white/10 hover:border-[var(--palette-peach)]/30 hover:bg-[rgba(255,235,204,0.05)] text-[var(--palette-peach)] transition-all cursor-pointer"
              >
                /diagnose
              </button>
              <button 
                onClick={() => handleCommand('/clearance')}
                className="px-2 py-0.5 rounded text-[8px] bg-white/5 border border-white/10 hover:border-[var(--palette-yellow)]/30 hover:bg-[rgba(255,249,210,0.05)] text-[var(--palette-yellow)] transition-all cursor-pointer"
              >
                /clearance
              </button>
            </div>

            {/* Input Footer */}
            <div className="p-3 bg-white/[0.01] border-t border-white/5 flex gap-2">
              <input
                type="text"
                value={inputVal}
                onChange={(e) => setInputVal(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="EXECUTE STATEMENT..."
                className="flex-1 bg-black/40 border border-white/8 rounded px-3 py-1.5 text-[10px] text-white focus:outline-none focus:border-[var(--palette-sky)]/40 transition-colors"
              />
              <button
                onClick={handleSend}
                className="px-3 rounded bg-[var(--palette-sky)] text-black hover:bg-[var(--palette-ice)] transition-colors flex items-center justify-center cursor-pointer"
              >
                <Send className="w-3 h-3" />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Floating Toggle Button */}
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsOpen(!isOpen)}
        className={cn(
          "w-12 h-12 rounded-full flex items-center justify-center cursor-pointer shadow-lg relative border",
          isOpen 
            ? "bg-black border-white/15 text-[var(--palette-yellow)]" 
            : "bg-[rgba(12,17,30,0.8)] border-[rgba(140,192,235,0.2)] text-[var(--palette-sky)]"
        )}
        style={{
          boxShadow: isOpen 
            ? '0 0 20px rgba(255, 249, 210, 0.25)' 
            : '0 0 25px rgba(140, 192, 235, 0.25)'
        }}
      >
        <Cpu className="w-5 h-5" />
        
        {/* Pulsing Outer Core Ring */}
        <div className="absolute inset-0 rounded-full border border-inherit animate-ping opacity-20 pointer-events-none" />
      </motion.button>
    </div>
  );
}
