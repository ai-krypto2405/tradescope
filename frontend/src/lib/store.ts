/**
 * Zustand store for global state management
 */
import { create } from 'zustand';
import { User, Backtest } from '@/types';
import { api } from './api';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,

  login: async (email, password) => {
    const response = await api.login({ email, password });
    set({ user: response.user, isAuthenticated: true });
  },

  register: async (email, username, password) => {
    const response = await api.register({ email, username, password });
    set({ user: response.user, isAuthenticated: true });
  },

  logout: () => {
    api.logout();
    set({ user: null, isAuthenticated: false });
  },

  refreshUser: async () => {
    try {
      const user = await api.getCurrentUser();
      set({ user, isAuthenticated: true });
    } catch (error) {
      set({ user: null, isAuthenticated: false });
    }
  },
}));

interface BacktestState {
  backtests: Backtest[];
  selectedBacktest: Backtest | null;
  isLoading: boolean;
  fetchBacktests: () => Promise<void>;
  fetchBacktest: (id: number) => Promise<void>;
  createBacktest: (data: any) => Promise<Backtest>;
  deleteBacktest: (id: number) => Promise<void>;
}

export const useBacktestStore = create<BacktestState>((set, get) => ({
  backtests: [],
  selectedBacktest: null,
  isLoading: false,

  fetchBacktests: async () => {
    set({ isLoading: true });
    try {
      const response = await api.listBacktests();
      set({ backtests: response.backtests, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  fetchBacktest: async (id) => {
    set({ isLoading: true });
    try {
      const backtest = await api.getBacktest(id);
      set({ selectedBacktest: backtest, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  createBacktest: async (data) => {
    set({ isLoading: true });
    try {
      const backtest = await api.createBacktest(data);
      set((state) => ({
        backtests: [backtest, ...state.backtests],
        isLoading: false,
      }));
      return backtest;
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  deleteBacktest: async (id) => {
    await api.deleteBacktest(id);
    set((state) => ({
      backtests: state.backtests.filter((b) => b.id !== id),
    }));
  },
}));
