from common_writer import write_file

app_router = """import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import { Navbar } from './components/layout/Navbar';
import { LoginPage } from './features/auth/LoginPage';
import { RegisterPage } from './features/auth/RegisterPage';
import { UserProfilePage } from './features/users/UserProfilePage';
import { RepoViewPage } from './features/repositories/RepoViewPage';
import { RepoSettingsPage } from './features/settings/RepoSettingsPage';
import { IssueListPage } from './features/issues/IssueListPage';
import { PRListPage } from './features/pullrequests/PRListPage';
import { KanbanBoardPage } from './features/kanban/KanbanBoardPage';
import { WorkflowRunPage } from './features/workflows/WorkflowRunPage';
import { AdminDashboardPage } from './features/admin/AdminDashboardPage';
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
      <Link to=\"/admin\" className=\"px-6 py-3 text-sm font-semibold text-slate-200 bg-surface-900 border border-surface-800 hover:bg-surface-800 rounded-xl transition-all\">
        Admin Console
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
          <Route path=\"/register\" element={<RegisterPage />} />
          <Route path=\"/admin\" element={<AdminDashboardPage />} />
          <Route path=\"/users/:username\" element={<UserProfilePage />} />
          <Route path=\"/:owner/:repo\" element={<RepoViewPage />} />
          <Route path=\"/:owner/:repo/settings\" element={<RepoSettingsPage />} />
          <Route path=\"/:owner/:repo/issues\" element={<IssueListPage />} />
          <Route path=\"/:owner/:repo/pulls\" element={<PRListPage />} />
          <Route path=\"/:owner/:repo/projects\" element={<KanbanBoardPage />} />
          <Route path=\"/:owner/:repo/actions/runs/:runId\" element={<WorkflowRunPage />} />
          <Route path=\"*\" element={<HomePage />} />
        </Routes>
      </main>
    </div>
  );
}
"""
write_file("frontend/src/App.tsx", app_router)

print("update_app_router_v2 complete.")