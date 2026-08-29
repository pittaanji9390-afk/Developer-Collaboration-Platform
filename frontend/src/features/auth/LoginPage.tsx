import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { GitFork, Lock, User as UserIcon } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { useAuthStore } from '../../stores/authStore';
import api from '../../api/client';

export const LoginPage: React.FC = () => {
  const [usernameOrEmail, setUsernameOrEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const setAuth = useAuthStore((s) => s.setAuth);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const res = await api.post('/auth/login', { usernameOrEmail, password });
      const { user, accessToken, refreshToken } = res.data.data;
      setAuth(user, accessToken, refreshToken);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Authentication failed. Please verify credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-3.5rem)] px-4">
      <div className="w-full max-w-md p-8 bg-surface-900 border border-surface-800 rounded-2xl shadow-xl">
        <div className="flex flex-col items-center mb-6 text-center">
          <div className="flex items-center justify-center w-12 h-12 mb-3 rounded-xl bg-forge-600 text-white">
            <GitFork className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold text-white">Sign in to ForgeHub</h2>
          <p className="text-sm text-slate-400 mt-1">Enter your developer credentials to continue</p>
        </div>

        {error && (
          <div className="p-3 mb-4 text-xs font-medium text-red-300 bg-red-950/60 border border-red-800 rounded-lg">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-1.5 text-xs font-medium text-slate-300">Username or Email</label>
            <div className="relative">
              <UserIcon className="absolute left-3 top-2.5 w-4 h-4 text-slate-500" />
              <input
                type="text"
                value={usernameOrEmail}
                onChange={(e) => setUsernameOrEmail(e.target.value)}
                required
                className="w-full py-2 pl-9 pr-3 text-sm bg-surface-950 border border-surface-800 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-forge-500"
                placeholder="alice"
              />
            </div>
          </div>

          <div>
            <label className="block mb-1.5 text-xs font-medium text-slate-300">Password</label>
            <div className="relative">
              <Lock className="absolute left-3 top-2.5 w-4 h-4 text-slate-500" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full py-2 pl-9 pr-3 text-sm bg-surface-950 border border-surface-800 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-forge-500"
                placeholder="••••••••"
              />
            </div>
          </div>

          <Button type="submit" className="w-full mt-2" isLoading={isLoading}>
            Sign In
          </Button>
        </form>

        <p className="mt-6 text-center text-xs text-slate-400">
          Don't have an account?{' '}
          <Link to="/register" className="text-forge-400 hover:text-forge-300 font-medium">
            Create one
          </Link>
        </p>
      </div>
    </div>
  );
};
