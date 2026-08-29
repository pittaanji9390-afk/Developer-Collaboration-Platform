from common_writer import write_file

login_page = """import React, { useState } from 'react';
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
    <div className=\"flex items-center justify-center min-h-[calc(100vh-3.5rem)] px-4\">
      <div className=\"w-full max-w-md p-8 bg-surface-900 border border-surface-800 rounded-2xl shadow-xl\">
        <div className=\"flex flex-col items-center mb-6 text-center\">
          <div className=\"flex items-center justify-center w-12 h-12 mb-3 rounded-xl bg-forge-600 text-white\">
            <GitFork className=\"w-6 h-6\" />
          </div>
          <h2 className=\"text-2xl font-bold text-white\">Sign in to ForgeHub</h2>
          <p className=\"text-sm text-slate-400 mt-1\">Enter your developer credentials to continue</p>
        </div>

        {error && (
          <div className=\"p-3 mb-4 text-xs font-medium text-red-300 bg-red-950/60 border border-red-800 rounded-lg\">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className=\"space-y-4\">
          <div>
            <label className=\"block mb-1.5 text-xs font-medium text-slate-300\">Username or Email</label>
            <div className=\"relative\">
              <UserIcon className=\"absolute left-3 top-2.5 w-4 h-4 text-slate-500\" />
              <input
                type=\"text\"
                value={usernameOrEmail}
                onChange={(e) => setUsernameOrEmail(e.target.value)}
                required
                className=\"w-full py-2 pl-9 pr-3 text-sm bg-surface-950 border border-surface-800 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-forge-500\"
                placeholder=\"alice\"
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
                placeholder=\"••••••••\"
              />
            </div>
          </div>

          <Button type=\"submit\" className=\"w-full mt-2\" isLoading={isLoading}>
            Sign In
          </Button>
        </form>

        <p className=\"mt-6 text-center text-xs text-slate-400\">
          Don't have an account?{' '}
          <Link to=\"/register\" className=\"text-forge-400 hover:text-forge-300 font-medium\">
            Create one
          </Link>
        </p>
      </div>
    </div>
  );
};
"""
write_file("frontend/src/features/auth/LoginPage.tsx", login_page)

repo_view = """import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { GitBranch, Folder, FileText, GitCommit, Shield, CircleDot, GitPullRequest, Settings, Eye, Star, GitFork } from 'lucide-react';
import Editor from '@monaco-editor/react';
import api from '../../api/client';
import { Repository, GitTreeEntry, GitBlob } from '../../types';

export const RepoViewPage: React.FC = () => {
  const { owner, repo } = useParams<{ owner: string; repo: string }>();
  const [repository, setRepository] = useState<Repository | null>(null);
  const [tree, setTree] = useState<GitTreeEntry[]>([]);
  const [selectedFile, setSelectedFile] = useState<GitBlob | null>(null);
  const [currentPath, setCurrentPath] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadRepository();
  }, [owner, repo]);

  const loadRepository = async () => {
    try {
      setIsLoading(true);
      const res = await api.get(`/repositories/${owner}/${repo}`);
      const repoData = res.data.data;
      setRepository(repoData);

      const treeRes = await api.get(`/repositories/${repoData.id}/git/tree`, {
        params: { ref: repoData.defaultBranch },
      });
      setTree(treeRes.data.data);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEntryClick = async (entry: GitTreeEntry) => {
    if (!repository) return;
    if (entry.type === 'blob') {
      const res = await api.get(`/repositories/${repository.id}/git/blob`, {
        params: { ref: repository.defaultBranch, path: entry.path },
      });
      setSelectedFile(res.data.data);
    } else {
      const res = await api.get(`/repositories/${repository.id}/git/tree`, {
        params: { ref: repository.defaultBranch, path: entry.path },
      });
      setTree(res.data.data);
      setCurrentPath(entry.path);
    }
  };

  if (isLoading || !repository) {
    return (
      <div className=\"flex items-center justify-center min-h-[60vh]\">
        <div className=\"w-8 h-8 border-4 border-forge-500 border-t-transparent rounded-full animate-spin\" />
      </div>
    );
  }

  return (
    <div className=\"max-w-7xl mx-auto px-4 py-6 w-full space-y-6\">
      {/* Header */}
      <div className=\"flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-surface-800\">
        <div className=\"flex items-center gap-2\">
          <Link to={`/users/${repository.owner}`} className=\"text-slate-400 hover:text-slate-200 text-lg\">
            {repository.owner}
          </Link>
          <span className=\"text-slate-600\">/</span>
          <span className=\"text-xl font-bold text-white\">{repository.name}</span>
          <span className=\"px-2 py-0.5 text-xs rounded-full border border-surface-700 bg-surface-900 text-slate-400 font-mono ml-2\">
            {repository.visibility}
          </span>
        </div>

        <div className=\"flex items-center gap-2\">
          <button className=\"flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-300 bg-surface-900 border border-surface-800 rounded-lg hover:bg-surface-800 transition-colors\">
            <Star className=\"w-3.5 h-3.5\" />
            <span>Star</span>
            <span className=\"px-1.5 py-0.2 bg-surface-800 rounded text-[11px]\">{repository.starCount}</span>
          </button>
          <button className=\"flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-300 bg-surface-900 border border-surface-800 rounded-lg hover:bg-surface-800 transition-colors\">
            <GitFork className=\"w-3.5 h-3.5\" />
            <span>Fork</span>
            <span className=\"px-1.5 py-0.2 bg-surface-800 rounded text-[11px]\">{repository.forkCount}</span>
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className=\"flex items-center gap-6 border-b border-surface-800 text-sm font-medium text-slate-400\">
        <Link to={`/${owner}/${repo}`} className=\"flex items-center gap-2 pb-3 border-b-2 border-forge-500 text-white\">
          <FileText className=\"w-4 h-4\" />
          <span>Code</span>
        </Link>
        <Link to={`/${owner}/${repo}/issues`} className=\"flex items-center gap-2 pb-3 hover:text-slate-200 transition-colors\">
          <CircleDot className=\"w-4 h-4\" />
          <span>Issues</span>
          <span className=\"px-1.5 py-0.5 text-xs bg-surface-800 rounded-full\">{repository.openIssuesCount}</span>
        </Link>
        <Link to={`/${owner}/${repo}/pulls`} className=\"flex items-center gap-2 pb-3 hover:text-slate-200 transition-colors\">
          <GitPullRequest className=\"w-4 h-4\" />
          <span>Pull Requests</span>
          <span className=\"px-1.5 py-0.5 text-xs bg-surface-800 rounded-full\">{repository.openPrsCount}</span>
        </Link>
        <Link to={`/${owner}/${repo}/settings`} className=\"flex items-center gap-2 pb-3 hover:text-slate-200 transition-colors\">
          <Settings className=\"w-4 h-4\" />
          <span>Settings</span>
        </Link>
      </div>

      {/* Code Browser */}
      {selectedFile ? (
        <div className=\"border border-surface-800 rounded-xl overflow-hidden bg-surface-900\">
          <div className=\"flex items-center justify-between px-4 py-2.5 bg-surface-950 border-b border-surface-800 text-xs font-mono text-slate-400\">
            <div className=\"flex items-center gap-2\">
              <button onClick={() => setSelectedFile(null)} className=\"text-forge-400 hover:underline\">
                Back to files
              </button>
              <span>/</span>
              <span className=\"text-slate-200 font-semibold\">{selectedFile.path}</span>
            </div>
            <span>{selectedFile.lineCount} lines ({selectedFile.size} bytes)</span>
          </div>
          <div className=\"h-[500px]\">
            <Editor
              height=\"100%\"
              theme=\"vs-dark\"
              path={selectedFile.name}
              value={selectedFile.content || ''}
              options={{ readOnly: true, minimap: { enabled: false }, fontSize: 13 }}
            />
          </div>
        </div>
      ) : (
        <div className=\"border border-surface-800 rounded-xl overflow-hidden bg-surface-900\">
          <div className=\"px-4 py-3 bg-surface-950/60 border-b border-surface-800 flex items-center justify-between text-xs text-slate-400\">
            <div className=\"flex items-center gap-2 font-mono\">
              <GitBranch className=\"w-3.5 h-3.5 text-forge-400\" />
              <span className=\"text-slate-200 font-semibold\">{repository.defaultBranch}</span>
            </div>
          </div>

          <div className=\"divide-y divide-surface-800\">
            {tree.map((entry) => (
              <div
                key={entry.path}
                onClick={() => handleEntryClick(entry)}
                className=\"flex items-center justify-between px-4 py-2.5 text-sm hover:bg-surface-800/60 cursor-pointer transition-colors\"
              >
                <div className=\"flex items-center gap-3\">
                  {entry.type === 'tree' ? (
                    <Folder className=\"w-4 h-4 text-forge-400\" />
                  ) : (
                    <FileText className=\"w-4 h-4 text-slate-400\" />
                  )}
                  <span className={entry.type === 'tree' ? 'font-medium text-slate-200' : 'text-slate-300'}>
                    {entry.name}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
"""
write_file("frontend/src/features/repositories/RepoViewPage.tsx", repo_view)

print("gen_phase11_frontend_features complete.")