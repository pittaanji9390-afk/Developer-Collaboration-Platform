from common_writer import write_file

types_ts = """export interface User {
  id: string;
  username: string;
  email: string;
  displayName: string;
  avatarUrl: string;
  bio?: string;
  company?: string;
  location?: string;
  website?: string;
  role: 'USER' | 'ADMIN';
  createdAt: string;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  displayName: string;
  description?: string;
  avatarUrl: string;
  visibility: 'PUBLIC' | 'PRIVATE';
  createdAt: string;
}

export interface Repository {
  id: string;
  owner: string;
  name: string;
  slug: string;
  description?: string;
  visibility: 'PUBLIC' | 'PRIVATE' | 'INTERNAL';
  defaultBranch: string;
  forkCount: number;
  starCount: number;
  openIssuesCount: number;
  openPrsCount: number;
  createdAt: string;
  updatedAt: string;
}

export interface GitTreeEntry {
  name: string;
  path: string;
  type: 'blob' | 'tree';
  mode: string;
  sha: string;
  size: number;
}

export interface GitBlob {
  name: string;
  path: string;
  sha: string;
  size: number;
  isBinary: boolean;
  content: string | null;
  lineCount: number;
}

export interface GitCommit {
  sha: string;
  shortSha: string;
  authorName: string;
  authorEmail: string;
  message: string;
  timestamp: string;
  additions: number;
  deletions: number;
  changedFilesCount: number;
}

export interface GitDiff {
  oldPath: string;
  newPath: string;
  changeType: string;
  additions: number;
  deletions: number;
  hunks: {
    header: string;
    oldStart: number;
    oldCount: number;
    newStart: number;
    newCount: number;
    lines: {
      type: 'CONTEXT' | 'ADDED' | 'DELETED';
      oldLineNumber?: number;
      newLineNumber?: number;
      content: string;
    }[];
  }[];
}

export interface Issue {
  id: string;
  number: number;
  title: string;
  body: string;
  status: 'OPEN' | 'CLOSED';
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT';
  authorUsername: string;
  authorAvatarUrl: string;
  commentsCount: number;
  createdAt: string;
  updatedAt: string;
  closedAt?: string;
}

export interface PullRequest {
  id: string;
  number: number;
  title: string;
  body: string;
  sourceBranch: string;
  targetBranch: string;
  status: 'OPEN' | 'CLOSED' | 'MERGED';
  draft: boolean;
  mergeable: boolean;
  authorUsername: string;
  authorAvatarUrl: string;
  additions: number;
  deletions: number;
  changedFiles: number;
  createdAt: string;
  updatedAt: string;
  mergedAt?: string;
}

export interface NotificationItem {
  id: string;
  type: string;
  title: string;
  body: string;
  linkUrl: string;
  read: boolean;
  createdAt: string;
}
"""
write_file("frontend/src/types/index.ts", types_ts)

api_client = """import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('forgehub_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('forgehub_token');
      localStorage.removeItem('forgehub_refresh');
    }
    return Promise.reject(error);
  }
);

export default api;
"""
write_file("frontend/src/api/client.ts", api_client)

auth_store = """import { create } from 'zustand';
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
"""
write_file("frontend/src/stores/authStore.ts", auth_store)

ui_store = """import { create } from 'zustand';

interface UIState {
  isCommandPaletteOpen: boolean;
  openCommandPalette: () => void;
  closeCommandPalette: () => void;
  toggleCommandPalette: () => void;
}

export const useUIStore = create<UIState>((set) => ({
  isCommandPaletteOpen: false,
  openCommandPalette: () => set({ isCommandPaletteOpen: true }),
  closeCommandPalette: () => set({ isCommandPaletteOpen: false }),
  toggleCommandPalette: () => set((s) => ({ isCommandPaletteOpen: !s.isCommandPaletteOpen })),
}));
"""
write_file("frontend/src/stores/uiStore.ts", ui_store)

button_tsx = """import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  className,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled,
  ...props
}) => {
  const base = 'inline-flex items-center justify-center font-medium transition-colors rounded-lg focus:outline-none focus:ring-2 focus:ring-forge-500 focus:ring-offset-2 focus:ring-offset-surface-900 disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variants = {
    primary: 'bg-forge-600 hover:bg-forge-500 text-white shadow-sm',
    secondary: 'bg-surface-800 hover:bg-surface-700 text-slate-200 border border-surface-700',
    outline: 'border border-surface-700 hover:bg-surface-800 text-slate-300',
    danger: 'bg-red-600 hover:bg-red-500 text-white shadow-sm',
    ghost: 'hover:bg-surface-800 text-slate-300',
  };

  const sizes = {
    sm: 'px-2.5 py-1.5 text-xs',
    md: 'px-4 py-2 text-sm',
    lg: 'px-5 py-2.5 text-base',
  };

  return (
    <button
      className={twMerge(clsx(base, variants[variant], sizes[size], className))}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <span className=\"inline-block w-4 h-4 mr-2 border-2 border-white border-t-transparent rounded-full animate-spin\" />
      ) : null}
      {children}
    </button>
  );
};
"""
write_file("frontend/src/components/ui/Button.tsx", button_tsx)

navbar_tsx = """import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { GitFork, Search, Bell, Plus, User as UserIcon, LogOut, Terminal } from 'lucide-react';
import { useAuthStore } from '../../stores/authStore';
import { useUIStore } from '../../stores/uiStore';

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuthStore();
  const { openCommandPalette } = useUIStore();
  const navigate = useNavigate();

  return (
    <header className=\"sticky top-0 z-40 w-full border-b border-surface-800 bg-surface-950/80 backdrop-blur-md\">
      <div className=\"flex items-center justify-between h-14 px-4 mx-auto max-w-7xl\">
        <div className=\"flex items-center gap-6\">
          <Link to=\"/\" className=\"flex items-center gap-2 font-bold tracking-tight text-white group\">
            <div className=\"flex items-center justify-center w-8 h-8 rounded-lg bg-forge-600 text-white group-hover:bg-forge-500 transition-colors\">
              <GitFork className=\"w-5 h-5\" />
            </div>
            <span className=\"text-lg font-mono font-bold bg-gradient-to-r from-white via-slate-200 to-forge-400 bg-clip-text text-transparent\">
              ForgeHub
            </span>
          </Link>

          <button
            onClick={openCommandPalette}
            className=\"flex items-center gap-2 px-3 py-1.5 text-xs text-slate-400 bg-surface-900 border border-surface-800 rounded-lg hover:border-surface-700 hover:text-slate-200 transition-colors w-64 justify-between\"
          >
            <div className=\"flex items-center gap-2\">
              <Search className=\"w-3.5 h-3.5\" />
              <span>Search repositories, code...</span>
            </div>
            <kbd className=\"px-1.5 py-0.5 text-[10px] bg-surface-800 border border-surface-700 rounded text-slate-400 font-mono\">
              Ctrl K
            </kbd>
          </button>
        </div>

        <div className=\"flex items-center gap-3\">
          {isAuthenticated ? (
            <>
              <Link to=\"/notifications\" className=\"p-2 text-slate-400 hover:text-white transition-colors rounded-lg hover:bg-surface-800\">
                <Bell className=\"w-4 h-4\" />
              </Link>
              <Link to=\"/new\" className=\"flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-white bg-forge-600 hover:bg-forge-500 rounded-lg transition-colors\">
                <Plus className=\"w-3.5 h-3.5\" />
                <span>New</span>
              </Link>
              <div className=\"flex items-center gap-2 pl-2 border-l border-surface-800\">
                <img
                  src={user?.avatarUrl || 'https://api.dicebear.com/7.x/identicon/svg?seed=user'}
                  alt=\"avatar\"
                  className=\"w-7 h-7 rounded-full border border-surface-700\"
                />
                <button
                  onClick={() => {
                    logout();
                    navigate('/login');
                  }}
                  className=\"p-1.5 text-slate-400 hover:text-red-400 transition-colors\"
                  title=\"Logout\"
                >
                  <LogOut className=\"w-4 h-4\" />
                </button>
              </div>
            </>
          ) : (
            <div className=\"flex items-center gap-2\">
              <Link to=\"/login\" className=\"px-3 py-1.5 text-xs font-medium text-slate-300 hover:text-white transition-colors\">
                Sign in
              </Link>
              <Link to=\"/register\" className=\"px-3 py-1.5 text-xs font-medium text-white bg-forge-600 hover:bg-forge-500 rounded-lg transition-colors\">
                Sign up
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
"""
write_file("frontend/src/components/layout/Navbar.tsx", navbar_tsx)

main_tsx = """import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import App from './App';
import './index.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
);
"""
write_file("frontend/src/main.tsx", main_tsx)

index_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-surface-950 text-slate-100 font-sans antialiased;
  }
}
"""
write_file("frontend/src/index.css", index_css)

app_tsx = """import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import { Navbar } from './components/layout/Navbar';
import { GitBranch, GitPullRequest, CircleDot, Shield, Terminal, Zap, BookOpen, Star } from 'lucide-react';

const HomePage = () => (
  <div className=\"min-h-[calc(100vh-3.5rem)] flex flex-col items-center justify-center px-4 py-16 text-center\">
    <div className=\"inline-flex items-center gap-2 px-3 py-1 text-xs font-mono text-forge-400 bg-forge-950/60 border border-forge-800/80 rounded-full mb-8 backdrop-blur-sm animate-pulse\">
      <Zap className=\"w-3.5 h-3.5\" />
      <span>ForgeHub 1.0 Enterprise Developer Platform</span>
    </div>

    <h1 className=\"max-w-4xl text-5xl sm:text-6xl font-extrabold tracking-tight text-white mb-6 leading-tight font-sans\">
      Where modern engineering teams build, review & deliver software.
    </h1>

    <p className=\"max-w-2xl text-lg text-slate-400 mb-10\">
      Enterprise-grade Git repository engine, automated pull request reviews, isolated CI/CD workflows, and fine-grained RBAC collaboration.
    </p>

    <div className=\"flex flex-wrap items-center justify-center gap-4\">
      <Link to=\"/explore\" className=\"px-6 py-3 text-sm font-semibold text-white bg-forge-600 hover:bg-forge-500 rounded-xl shadow-lg shadow-forge-600/20 transition-all\">
        Explore Repositories
      </Link>
      <Link to=\"/register\" className=\"px-6 py-3 text-sm font-semibold text-slate-200 bg-surface-900 border border-surface-800 hover:bg-surface-800 rounded-xl transition-all\">
        Start Collaborating
      </Link>
    </div>

    <div className=\"grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mt-20 text-left\">
      <div className=\"p-6 rounded-2xl bg-surface-900/50 border border-surface-800 backdrop-blur-sm\">
        <div className=\"w-10 h-10 rounded-xl bg-forge-950 border border-forge-800 flex items-center justify-center text-forge-400 mb-4\">
          <GitBranch className=\"w-5 h-5\" />
        </div>
        <h3 className=\"text-lg font-semibold text-white mb-2\">Native JGit Engine</h3>
        <p className=\"text-sm text-slate-400\">Bare repository lifecycle, tree walking, unified & split diffs, commit histories and blame.</p>
      </div>

      <div className=\"p-6 rounded-2xl bg-surface-900/50 border border-surface-800 backdrop-blur-sm\">
        <div className=\"w-10 h-10 rounded-xl bg-purple-950 border border-purple-800 flex items-center justify-center text-purple-400 mb-4\">
          <GitPullRequest className=\"w-5 h-5\" />
        </div>
        <h3 className=\"text-lg font-semibold text-white mb-2\">Code Reviews & Protection</h3>
        <p className=\"text-sm text-slate-400\">Inline diff review threads, merge validation rules, status checks, and required approver gates.</p>
      </div>

      <div className=\"p-6 rounded-2xl bg-surface-900/50 border border-surface-800 backdrop-blur-sm\">
        <div className=\"w-10 h-10 rounded-xl bg-emerald-950 border border-emerald-800 flex items-center justify-center text-emerald-400 mb-4\">
          <Shield className=\"w-5 h-5\" />
        </div>
        <h3 className=\"text-lg font-semibold text-white mb-2\">CI/CD & Secret Vault</h3>
        <p className=\"text-sm text-slate-400\">YAML DAG workflow pipelines, isolated runner agents, HMAC webhooks and AES-256 encrypted vaults.</p>
      </div>
    </div>
  </div>
);

export default function App() {
  return (
    <div className=\"min-h-screen bg-surface-950 text-slate-100 flex flex-col font-sans\">
      <Navbar />
      <main className=\"flex-1\">
        <Routes>
          <Route path=\"/\" element={<HomePage />} />
          <Route path=\"*\" element={<HomePage />} />
        </Routes>
      </main>
    </div>
  );
}
"""
write_file("frontend/src/App.tsx", app_tsx)

print("gen_phase10_frontend_core complete.")