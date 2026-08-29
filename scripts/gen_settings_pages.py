from common_writer import write_file

register_page = """import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { GitFork, Lock, User as UserIcon, Mail } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { useAuthStore } from '../../stores/authStore';
import api from '../../api/client';

export const RegisterPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const setAuth = useAuthStore((s) => s.setAuth);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const res = await api.post('/auth/register', {
        username,
        email,
        password,
        displayName: displayName || username,
      });
      const { user, accessToken, refreshToken } = res.data.data;
      setAuth(user, accessToken, refreshToken);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Registration failed.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className=\"flex items-center justify-center min-h-[calc(100vh-3.5rem)] px-4 py-8\">
      <div className=\"w-full max-w-md p-8 bg-surface-900 border border-surface-800 rounded-2xl shadow-xl\">
        <div className=\"flex flex-col items-center mb-6 text-center\">
          <div className=\"flex items-center justify-center w-12 h-12 mb-3 rounded-xl bg-forge-600 text-white\">
            <GitFork className=\"w-6 h-6\" />
          </div>
          <h2 className=\"text-2xl font-bold text-white\">Join ForgeHub</h2>
          <p className=\"text-sm text-slate-400 mt-1\">Create your developer collaboration account</p>
        </div>

        {error && (
          <div className=\"p-3 mb-4 text-xs font-medium text-red-300 bg-red-950/60 border border-red-800 rounded-lg\">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className=\"space-y-4\">
          <div>
            <label className=\"block mb-1.5 text-xs font-medium text-slate-300\">Username</label>
            <div className=\"relative\">
              <UserIcon className=\"absolute left-3 top-2.5 w-4 h-4 text-slate-500\" />
              <input
                type=\"text\"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className=\"w-full py-2 pl-9 pr-3 text-sm bg-surface-950 border border-surface-800 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-forge-500\"
                placeholder=\"octocat\"
              />
            </div>
          </div>

          <div>
            <label className=\"block mb-1.5 text-xs font-medium text-slate-300\">Email Address</label>
            <div className=\"relative\">
              <Mail className=\"absolute left-3 top-2.5 w-4 h-4 text-slate-500\" />
              <input
                type=\"email\"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className=\"w-full py-2 pl-9 pr-3 text-sm bg-surface-950 border border-surface-800 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-forge-500\"
                placeholder=\"octocat@example.com\"
              />
            </div>
          </div>

          <div>
            <label className=\"block mb-1.5 text-xs font-medium text-slate-300\">Password</label>
            <div className=\"relative\">
              <Lock className=\"absolute left-3 top-2.5 w-4 h-4 text-slate-500\" />
              <input
                type=\"password\"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className=\"w-full py-2 pl-9 pr-3 text-sm bg-surface-950 border border-surface-800 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-forge-500\"
                placeholder=\"At least 8 characters\"
              />
            </div>
          </div>

          <Button type=\"submit\" className=\"w-full mt-2\" isLoading={isLoading}>
            Create Account
          </Button>
        </form>

        <p className=\"mt-6 text-center text-xs text-slate-400\">
          Already have an account?{' '}
          <Link to=\"/login\" className=\"text-forge-400 hover:text-forge-300 font-medium\">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
};
"""
write_file("frontend/src/features/auth/RegisterPage.tsx", register_page)

user_profile_page = """import React from 'react';
import { useParams } from 'react-router-dom';
import { GitFork, Star, MapPin, Building, Link as LinkIcon, Calendar } from 'lucide-react';

export const UserProfilePage: React.FC = () => {
  const { username } = useParams<{ username: string }>();

  return (
    <div className=\"max-w-7xl mx-auto px-4 py-8 w-full\">
      <div className=\"grid grid-cols-1 md:grid-cols-4 gap-8\">
        {/* Sidebar */}
        <div className=\"space-y-4\">
          <img
            src={`https://api.dicebear.com/7.x/identicon/svg?seed=${username}`}
            alt=\"avatar\"
            className=\"w-48 h-48 rounded-full border-2 border-surface-700 bg-surface-900 shadow-xl\"
          />
          <div>
            <h1 className=\"text-2xl font-bold text-white\">{username}</h1>
            <p className=\"text-sm text-slate-400 font-mono\">@{username}</p>
          </div>
          <p className=\"text-sm text-slate-300 leading-relaxed\">
            Building distributed systems, high-performance Git engines, and modern developer tooling.
          </p>

          <div className=\"pt-4 border-t border-surface-800 space-y-2 text-xs text-slate-400\">
            <div className=\"flex items-center gap-2\"><Building className=\"w-4 h-4 text-slate-500\" /> ForgeHub Labs</div>
            <div className=\"flex items-center gap-2\"><MapPin className=\"w-4 h-4 text-slate-500\" /> San Francisco, CA</div>
            <div className=\"flex items-center gap-2\"><LinkIcon className=\"w-4 h-4 text-slate-500\" /> https://forgehub.dev</div>
            <div className=\"flex items-center gap-2\"><Calendar className=\"w-4 h-4 text-slate-500\" /> Joined August 2026</div>
          </div>
        </div>

        {/* Repositories and Contributions Heatmap */}
        <div className=\"md:col-span-3 space-y-6\">
          <div className=\"p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-4\">
            <h3 className=\"text-sm font-bold text-white\">524 Contributions in 2026</h3>
            {/* Heatmap grid */}
            <div className=\"grid grid-flow-col grid-rows-7 gap-1.5 overflow-x-auto pb-2\">
              {Array.from({ length: 52 * 7 }).map((_, i) => {
                const levels = ['bg-surface-800', 'bg-forge-950 border border-forge-800', 'bg-forge-700', 'bg-forge-500', 'bg-forge-400'];
                const lvl = (i * 7 + 3) % levels.length;
                return (
                  <div
                    key={i}
                    className={`w-3 h-3 rounded-sm ${levels[lvl]}`}
                    title={`Day ${i}: ${lvl * 2} contributions`}
                  />
                );
              })}
            </div>
          </div>

          <div className=\"space-y-4\">
            <h3 className=\"text-lg font-bold text-white\">Popular Repositories</h3>
            <div className=\"grid grid-cols-1 sm:grid-cols-2 gap-4\">
              <div className=\"p-5 bg-surface-900 border border-surface-800 rounded-2xl hover:border-surface-700 transition-colors space-y-3\">
                <div className=\"flex items-center justify-between\">
                  <span className=\"font-bold text-forge-400 hover:underline cursor-pointer\">developer-collaboration-platform</span>
                  <span className=\"px-2 py-0.5 text-[10px] font-mono border border-surface-700 rounded-full text-slate-400\">Public</span>
                </div>
                <p className=\"text-xs text-slate-400 leading-relaxed\">Production-ready enterprise developer platform with JGit, CI/CD, and RBAC.</p>
                <div className=\"flex items-center gap-4 text-xs text-slate-400 font-mono pt-2\">
                  <span className=\"flex items-center gap-1\"><span className=\"w-2.5 h-2.5 rounded-full bg-orange-500 inline-block\" /> Java</span>
                  <span className=\"flex items-center gap-1\"><Star className=\"w-3.5 h-3.5\" /> 1,284</span>
                  <span className=\"flex items-center gap-1\"><GitFork className=\"w-3.5 h-3.5\" /> 240</span>
                </div>
              </div>

              <div className=\"p-5 bg-surface-900 border border-surface-800 rounded-2xl hover:border-surface-700 transition-colors space-y-3\">
                <div className=\"flex items-center justify-between\">
                  <span className=\"font-bold text-forge-400 hover:underline cursor-pointer\">forgehub-runner-isolated</span>
                  <span className=\"px-2 py-0.5 text-[10px] font-mono border border-surface-700 rounded-full text-slate-400\">Public</span>
                </div>
                <p className=\"text-xs text-slate-400 leading-relaxed\">Lightweight isolated CI execution daemon with streaming websocket output.</p>
                <div className=\"flex items-center gap-4 text-xs text-slate-400 font-mono pt-2\">
                  <span className=\"flex items-center gap-1\"><span className=\"w-2.5 h-2.5 rounded-full bg-blue-500 inline-block\" /> TypeScript</span>
                  <span className=\"flex items-center gap-1\"><Star className=\"w-3.5 h-3.5\" /> 490</span>
                  <span className=\"flex items-center gap-1\"><GitFork className=\"w-3.5 h-3.5\" /> 62</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
"""
write_file("frontend/src/features/users/UserProfilePage.tsx", user_profile_page)

repo_settings_page = """import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { Shield, Key, Webhook, Users, Trash2, Save } from 'lucide-react';
import { Button } from '../../components/ui/Button';

export const RepoSettingsPage: React.FC = () => {
  const { owner, repo } = useParams<{ owner: string; repo: string }>();
  const [activeTab, setActiveTab] = useState<'general' | 'branches' | 'webhooks' | 'secrets'>('general');

  return (
    <div className=\"max-w-7xl mx-auto px-4 py-6 w-full space-y-6\">
      <div>
        <h2 className=\"text-xl font-bold text-white\">Repository Settings</h2>
        <p className=\"text-xs text-slate-400 mt-1\">Manage options, branch rules, webhooks, and secrets for {owner}/{repo}</p>
      </div>

      <div className=\"grid grid-cols-1 md:grid-cols-4 gap-6\">
        <div className=\"space-y-1\">
          <button
            onClick={() => setActiveTab('general')}
            className={`w-full flex items-center gap-2.5 px-3 py-2 text-sm font-medium rounded-lg text-left transition-colors ${
              activeTab === 'general' ? 'bg-surface-800 text-white' : 'text-slate-400 hover:text-white hover:bg-surface-800/50'
            }`}
          >
            <Shield className=\"w-4 h-4\" />
            <span>General</span>
          </button>

          <button
            onClick={() => setActiveTab('branches')}
            className={`w-full flex items-center gap-2.5 px-3 py-2 text-sm font-medium rounded-lg text-left transition-colors ${
              activeTab === 'branches' ? 'bg-surface-800 text-white' : 'text-slate-400 hover:text-white hover:bg-surface-800/50'
            }`}
          >
            <Shield className=\"w-4 h-4 text-purple-400\" />
            <span>Branch Protection</span>
          </button>

          <button
            onClick={() => setActiveTab('webhooks')}
            className={`w-full flex items-center gap-2.5 px-3 py-2 text-sm font-medium rounded-lg text-left transition-colors ${
              activeTab === 'webhooks' ? 'bg-surface-800 text-white' : 'text-slate-400 hover:text-white hover:bg-surface-800/50'
            }`}
          >
            <Webhook className=\"w-4 h-4 text-emerald-400\" />
            <span>Webhooks</span>
          </button>

          <button
            onClick={() => setActiveTab('secrets')}
            className={`w-full flex items-center gap-2.5 px-3 py-2 text-sm font-medium rounded-lg text-left transition-colors ${
              activeTab === 'secrets' ? 'bg-surface-800 text-white' : 'text-slate-400 hover:text-white hover:bg-surface-800/50'
            }`}
          >
            <Key className=\"w-4 h-4 text-amber-400\" />
            <span>Secrets & Vault</span>
          </button>
        </div>

        <div className=\"md:col-span-3 space-y-6\">
          {activeTab === 'general' && (
            <div className=\"p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-4\">
              <h3 className=\"text-base font-bold text-white\">Repository Name & Visibility</h3>
              <div className=\"space-y-3 max-w-md\">
                <div>
                  <label className=\"block mb-1 text-xs font-medium text-slate-300\">Repository Name</label>
                  <input
                    type=\"text\"
                    defaultValue={repo}
                    className=\"w-full py-2 px-3 text-sm bg-surface-950 border border-surface-800 rounded-lg text-white\"
                  />
                </div>
                <div>
                  <label className=\"block mb-1 text-xs font-medium text-slate-300\">Default Branch</label>
                  <input
                    type=\"text\"
                    defaultValue=\"main\"
                    className=\"w-full py-2 px-3 text-sm bg-surface-950 border border-surface-800 rounded-lg text-white\"
                  />
                </div>
              </div>
              <Button size=\"sm\" className=\"mt-2\">Save Changes</Button>
            </div>
          )}

          {activeTab === 'branches' && (
            <div className=\"p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-4\">
              <h3 className=\"text-base font-bold text-white\">Branch Protection Rules</h3>
              <div className=\"p-4 bg-surface-950 border border-surface-800 rounded-xl space-y-3 text-sm\">
                <div className=\"flex items-center justify-between\">
                  <span className=\"font-mono font-bold text-forge-400\">main</span>
                  <span className=\"text-xs text-emerald-400 font-medium\">Active</span>
                </div>
                <div className=\"space-y-2 text-xs text-slate-400\">
                  <div>✔ Require pull request before merging (Required approvals: 1)</div>
                  <div>✔ Require all conversations to be resolved</div>
                  <div>✔ Direct push blocked (Enforce admins: true)</div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'secrets' && (
            <div className=\"p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-4\">
              <div className=\"flex items-center justify-between\">
                <h3 className=\"text-base font-bold text-white\">Repository Secrets (AES-256-GCM Encrypted)</h3>
                <Button size=\"sm\">Add Secret</Button>
              </div>
              <div className=\"divide-y divide-surface-800 border border-surface-800 rounded-xl bg-surface-950\">
                <div className=\"flex items-center justify-between p-3.5 text-xs font-mono text-slate-300\">
                  <span className=\"font-bold text-forge-400\">NPM_AUTH_TOKEN</span>
                  <span className=\"text-slate-500\">Updated 2 days ago</span>
                </div>
                <div className=\"flex items-center justify-between p-3.5 text-xs font-mono text-slate-300\">
                  <span className=\"font-bold text-forge-400\">DEPLOY_SSH_KEY</span>
                  <span className=\"text-slate-500\">Updated 1 week ago</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
"""
write_file("frontend/src/features/settings/RepoSettingsPage.tsx", repo_settings_page)

print("gen_settings_pages complete.")