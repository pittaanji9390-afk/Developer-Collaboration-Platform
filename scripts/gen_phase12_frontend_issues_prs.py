from common_writer import write_file

issue_list = """import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { CircleDot, Plus, CheckCircle2 } from 'lucide-react';
import api from '../../api/client';
import { Issue } from '../../types';

export const IssueListPage: React.FC = () => {
  const { owner, repo } = useParams<{ owner: string; repo: string }>();
  const [issues, setIssues] = useState<Issue[]>([]);
  const [status, setStatus] = useState<'OPEN' | 'CLOSED'>('OPEN');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadIssues();
  }, [owner, repo, status]);

  const loadIssues = async () => {
    try {
      setIsLoading(true);
      const repoRes = await api.get(`/repositories/${owner}/${repo}`);
      const res = await api.get(`/repositories/${repoRes.data.data.id}/issues`, {
        params: { status },
      });
      setIssues(res.data.data.items);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className=\"max-w-7xl mx-auto px-4 py-6 w-full space-y-6\">
      <div className=\"flex items-center justify-between\">
        <div className=\"flex items-center gap-4\">
          <button
            onClick={() => setStatus('OPEN')}
            className={`flex items-center gap-2 text-sm font-semibold ${
              status === 'OPEN' ? 'text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <CircleDot className=\"w-4 h-4 text-emerald-400\" />
            <span>Open</span>
          </button>
          <button
            onClick={() => setStatus('CLOSED')}
            className={`flex items-center gap-2 text-sm font-semibold ${
              status === 'CLOSED' ? 'text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <CheckCircle2 className=\"w-4 h-4 text-purple-400\" />
            <span>Closed</span>
          </button>
        </div>

        <Link
          to={`/${owner}/${repo}/issues/new`}
          className=\"flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-white bg-forge-600 hover:bg-forge-500 rounded-lg transition-colors\"
        >
          <Plus className=\"w-3.5 h-3.5\" />
          <span>New Issue</span>
        </Link>
      </div>

      <div className=\"border border-surface-800 rounded-xl overflow-hidden bg-surface-900 divide-y divide-surface-800\">
        {issues.map((issue) => (
          <div key={issue.id} className=\"flex items-start justify-between p-4 hover:bg-surface-800/40 transition-colors\">
            <div className=\"flex items-start gap-3\">
              <CircleDot className=\"w-4 h-4 text-emerald-400 mt-0.5\" />
              <div>
                <Link to={`/${owner}/${repo}/issues/${issue.number}`} className=\"text-sm font-semibold text-white hover:text-forge-400 transition-colors\">
                  {issue.title}
                </Link>
                <div className=\"text-xs text-slate-400 mt-1\">
                  #{issue.number} opened by {issue.authorUsername}
                </div>
              </div>
            </div>
            {issue.commentsCount > 0 && (
              <span className=\"text-xs text-slate-400\">{issue.commentsCount} comments</span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
"""
write_file("frontend/src/features/issues/IssueListPage.tsx", issue_list)

pr_list = """import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { GitPullRequest, Plus, CheckCircle2 } from 'lucide-react';
import api from '../../api/client';
import { PullRequest } from '../../types';

export const PRListPage: React.FC = () => {
  const { owner, repo } = useParams<{ owner: string; repo: string }>();
  const [prs, setPrs] = useState<PullRequest[]>([]);
  const [status, setStatus] = useState<'OPEN' | 'CLOSED' | 'MERGED'>('OPEN');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadPRs();
  }, [owner, repo, status]);

  const loadPRs = async () => {
    try {
      setIsLoading(true);
      const repoRes = await api.get(`/repositories/${owner}/${repo}`);
      const res = await api.get(`/repositories/${repoRes.data.data.id}/pulls`, {
        params: { status },
      });
      setPrs(res.data.data.items);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className=\"max-w-7xl mx-auto px-4 py-6 w-full space-y-6\">
      <div className=\"flex items-center justify-between\">
        <div className=\"flex items-center gap-4\">
          <button
            onClick={() => setStatus('OPEN')}
            className={`flex items-center gap-2 text-sm font-semibold ${
              status === 'OPEN' ? 'text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <GitPullRequest className=\"w-4 h-4 text-emerald-400\" />
            <span>Open</span>
          </button>
          <button
            onClick={() => setStatus('MERGED')}
            className={`flex items-center gap-2 text-sm font-semibold ${
              status === 'MERGED' ? 'text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <CheckCircle2 className=\"w-4 h-4 text-purple-400\" />
            <span>Merged</span>
          </button>
        </div>

        <Link
          to={`/${owner}/${repo}/pulls/new`}
          className=\"flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-white bg-forge-600 hover:bg-forge-500 rounded-lg transition-colors\"
        >
          <Plus className=\"w-3.5 h-3.5\" />
          <span>New Pull Request</span>
        </Link>
      </div>

      <div className=\"border border-surface-800 rounded-xl overflow-hidden bg-surface-900 divide-y divide-surface-800\">
        {prs.map((pr) => (
          <div key={pr.id} className=\"flex items-start justify-between p-4 hover:bg-surface-800/40 transition-colors\">
            <div className=\"flex items-start gap-3\">
              <GitPullRequest className={`w-4 h-4 mt-0.5 ${pr.status === 'MERGED' ? 'text-purple-400' : 'text-emerald-400'}`} />
              <div>
                <Link to={`/${owner}/${repo}/pulls/${pr.number}`} className=\"text-sm font-semibold text-white hover:text-forge-400 transition-colors\">
                  {pr.title}
                </Link>
                <div className=\"text-xs text-slate-400 mt-1 flex items-center gap-2\">
                  <span>#{pr.number} opened by {pr.authorUsername}</span>
                  <span>•</span>
                  <span className=\"font-mono bg-surface-800 px-1.5 py-0.5 rounded text-[11px]\">{pr.sourceBranch} → {pr.targetBranch}</span>
                </div>
              </div>
            </div>
            <div className=\"flex items-center gap-3 text-xs font-mono\">
              <span className=\"text-emerald-400\">+{pr.additions}</span>
              <span className=\"text-red-400\">-{pr.deletions}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
"""
write_file("frontend/src/features/pullrequests/PRListPage.tsx", pr_list)

app_router = """import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import { Navbar } from './components/layout/Navbar';
import { LoginPage } from './features/auth/LoginPage';
import { RepoViewPage } from './features/repositories/RepoViewPage';
import { IssueListPage } from './features/issues/IssueListPage';
import { PRListPage } from './features/pullrequests/PRListPage';
import { GitBranch, GitPullRequest, Shield, Zap } from 'lucide-react';

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
      <Link to=\"/register\" className=\"px-6 py-3 text-sm font-semibold text-white bg-forge-600 hover:bg-forge-500 rounded-xl shadow-lg shadow-forge-600/20 transition-all\">
        Get Started Free
      </Link>
      <Link to=\"/login\" className=\"px-6 py-3 text-sm font-semibold text-slate-200 bg-surface-900 border border-surface-800 hover:bg-surface-800 rounded-xl transition-all\">
        Sign In
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
          <Route path=\"/login\" element={<LoginPage />} />
          <Route path=\"/:owner/:repo\" element={<RepoViewPage />} />
          <Route path=\"/:owner/:repo/issues\" element={<IssueListPage />} />
          <Route path=\"/:owner/:repo/pulls\" element={<PRListPage />} />
          <Route path=\"*\" element={<HomePage />} />
        </Routes>
      </main>
    </div>
  );
}
"""
write_file("frontend/src/App.tsx", app_router)

print("gen_phase12_frontend_issues_prs complete.")