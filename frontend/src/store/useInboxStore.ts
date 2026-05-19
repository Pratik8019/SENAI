import { create } from 'zustand';
import type { Thread } from '@/types/thread';
import type { Email } from '@/types/email';

interface InboxState {
  threads: Thread[];
  selectedThreadId: string | null;
  searchQuery: string;
  activeFilter: string;
  isLoading: boolean;
  total: number;
  page: number;

  setThreads: (threads: Thread[], total: number) => void;
  selectThread: (id: string | null) => void;
  setSearchQuery: (query: string) => void;
  setActiveFilter: (filter: string) => void;
  setLoading: (loading: boolean) => void;
  setPage: (page: number) => void;
}

export const useInboxStore = create<InboxState>((set) => ({
  threads: [],
  selectedThreadId: null,
  searchQuery: '',
  activeFilter: 'all',
  isLoading: false,
  total: 0,
  page: 1,

  setThreads: (threads, total) => set({ threads, total }),
  selectThread: (id) => set({ selectedThreadId: id }),
  setSearchQuery: (query) => set({ searchQuery: query }),
  setActiveFilter: (filter) => set({ activeFilter: filter }),
  setLoading: (loading) => set({ isLoading: loading }),
  setPage: (page) => set({ page }),
}));
