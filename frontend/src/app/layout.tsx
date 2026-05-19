import type { Metadata } from "next";
import "./globals.css";
import FloatingAssistant from "@/components/shared/FloatingAssistant";

export const metadata: Metadata = {
  title: "SentinelAI Mission Control",
  description: "AI-Powered CRM Intelligence Platform — Real-time email analysis, autonomous agents, and threat detection",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
      </head>
      <body className="animated-gradient-bg min-h-screen relative">
        {/* Futuristic scanline filter */}
        <div className="scanlines" />
        
        {children}
        
        {/* Floating Coprocessor Console */}
        <FloatingAssistant />
      </body>
    </html>
  );
}
