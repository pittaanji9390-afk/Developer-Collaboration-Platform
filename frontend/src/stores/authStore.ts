import { create } from 'zustand';
import { User } from '../types';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User, token: string, refreshToken: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: localStorage.getItem('forgehub_token'),
  isAuthenticated: !!localStorage.getItem('forgehub_token'),
  setAuth: (user, token, refreshToken) => {
    localStorage.setItem('forgehub_token', token);
    localStorage.setItem('forgehub_refresh', refreshToken);
    set({ user, token, isAuthenticated: true });
  },
  logout: () => {
    localStorage.removeItem('forgehub_token');
    localStorage.removeItem('forgehub_refresh');
    set({ user: null, token: null, isAuthenticated: false });
  },
}));
