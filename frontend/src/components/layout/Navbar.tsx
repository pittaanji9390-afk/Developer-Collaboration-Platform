import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { GitFork, Search, Bell, Plus, User as UserIcon, LogOut, Terminal } from 'lucide-react';
import { useAuthStore } from '../../stores/authStore';
import { useUIStore } from '../../stores/uiStore';

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuthStore();
  const { openCommandPalette } = useUIStore();
  const navigate = useNavigate();

  return (
    <header className="sticky top-0 z-40 w-full border-b border-surface-800 bg-surface-950/80 backdrop-blur-md">
      <div className="flex items-center justify-between h-14 px-4 mx-auto max-w-7xl">
        <div className="flex items-center gap-6">
          <Link to="/" className="flex items-center gap-2 font-bold tracking-tight text-white group">
            <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-forge-600 text-white group-hover:bg-forge-500 transition-colors">
              <GitFork className="w-5 h-5" />
            </div>
            <span className="text-lg font-mono font-bold bg-gradient-to-r from-white via-slate-200 to-forge-400 bg-clip-text text-transparent">
              ForgeHub
            </span>
          </Link>

          <button
            onClick={openCommandPalette}
            className="flex items-center gap-2 px-3 py-1.5 text-xs text-slate-400 bg-surface-900 border border-surface-800 rounded-lg hover:border-surface-700 hover:text-slate-200 transition-colors w-64 justify-between"
          >
            <div className="flex items-center gap-2">
              <Search className="w-3.5 h-3.5" />
              <span>Search repositories, code...</span>
            </div>
            <kbd className="px-1.5 py-0.5 text-[10px] bg-surface-800 border border-surface-700 rounded text-slate-400 font-mono">
              Ctrl K
            </kbd>
          </button>
        </div>

        <div className="flex items-center gap-3">
          {isAuthenticated ? (
            <>
              <Link to="/notifications" className="p-2 text-slate-400 hover:text-white transition-colors rounded-lg hover:bg-surface-800">
                <Bell className="w-4 h-4" />
              </Link>
              <Link to="/new" className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-white bg-forge-600 hover:bg-forge-500 rounded-lg transition-colors">
                <Plus className="w-3.5 h-3.5" />
                <span>New</span>
              </Link>
              <div className="flex items-center gap-2 pl-2 border-l border-surface-800">
                <img
                  src={user?.avatarUrl || 'https://api.dicebear.com/7.x/identicon/svg?seed=user'}
                  alt="avatar"
                  className="w-7 h-7 rounded-full border border-surface-700"
                />
                <button
                  onClick={() => {
                    logout();
                    navigate('/login');
                  }}
                  className="p-1.5 text-slate-400 hover:text-red-400 transition-colors"
                  title="Logout"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            </>
          ) : (
            <div className="flex items-center gap-2">
              <Link to="/login" className="px-3 py-1.5 text-xs font-medium text-slate-300 hover:text-white transition-colors">
                Sign in
              </Link>
              <Link to="/register" className="px-3 py-1.5 text-xs font-medium text-white bg-forge-600 hover:bg-forge-500 rounded-lg transition-colors">
                Sign up
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
