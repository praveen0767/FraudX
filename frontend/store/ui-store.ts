import { create } from 'zustand';
import { Transaction, DecisionDetail } from '@/lib/types';

interface UIState {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  // Live Streaming Queue
  transactions: (Transaction & { decisionDetail?: DecisionDetail })[];
  addTransaction: (tx: Transaction & { decisionDetail?: DecisionDetail }) => void;
  clearTransactions: () => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  transactions: [],
  addTransaction: (tx) => set((state) => {
    const updated = [tx, ...state.transactions].slice(0, 100); // keep last 100
    return { transactions: updated };
  }),
  clearTransactions: () => set({ transactions: [] })
}));
