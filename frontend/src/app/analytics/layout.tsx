import Sidebar from '@/components/layout/Sidebar';

export default function AnalyticsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 sidebar-offset grid-pattern">
        {children}
      </main>
    </div>
  );
}
