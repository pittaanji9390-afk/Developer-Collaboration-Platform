import React from 'react';
import { Users, Building2, GitFork, ShieldAlert, Cpu, Activity, Server } from 'lucide-react';

export const AdminDashboardPage: React.FC = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 py-8 w-full space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-white">Platform Administration Console</h1>
        <p className="text-sm text-slate-400 mt-1">System health, security oversight, runner pools and audit analytics</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl">
          <div className="flex items-center justify-between text-slate-400 mb-3">
            <span className="text-xs font-semibold uppercase">Total Developers</span>
            <Users className="w-5 h-5 text-forge-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">1,420</div>
          <div className="text-xs text-emerald-400 mt-2 font-medium">+12% this month</div>
        </div>

        <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl">
          <div className="flex items-center justify-between text-slate-400 mb-3">
            <span className="text-xs font-semibold uppercase">Organizations</span>
            <Building2 className="w-5 h-5 text-purple-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">86</div>
          <div className="text-xs text-slate-400 mt-2 font-medium">Active Enterprise Teams</div>
        </div>

        <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl">
          <div className="flex items-center justify-between text-slate-400 mb-3">
            <span className="text-xs font-semibold uppercase">Repositories</span>
            <GitFork className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">3,892</div>
          <div className="text-xs text-slate-400 mt-2 font-medium">Native JGit Bare Stores</div>
        </div>

        <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl">
          <div className="flex items-center justify-between text-slate-400 mb-3">
            <span className="text-xs font-semibold uppercase">CI Runner Pool</span>
            <Cpu className="w-5 h-5 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">12 / 12</div>
          <div className="text-xs text-emerald-400 mt-2 font-medium">All Agents Healthy</div>
        </div>
      </div>

      <div className="border border-surface-800 rounded-2xl bg-surface-900 overflow-hidden">
        <div className="p-4 border-b border-surface-800 flex items-center justify-between">
          <h3 className="text-sm font-bold text-white">Recent Platform Audit Logs</h3>
        </div>
        <div className="divide-y divide-surface-800 font-mono text-xs">
          <div className="p-4 flex items-center justify-between text-slate-300">
            <div className="flex items-center gap-3">
              <span className="px-2 py-0.5 rounded bg-surface-800 text-slate-400">AUTH_LOGIN</span>
              <span>User <b>alice</b> logged in successfully</span>
            </div>
            <span className="text-slate-500">2026-08-30 02:45:10</span>
          </div>

          <div className="p-4 flex items-center justify-between text-slate-300">
            <div className="flex items-center gap-3">
              <span className="px-2 py-0.5 rounded bg-forge-950 text-forge-400 border border-forge-800">REPO_CREATE</span>
              <span>Repository <b>forgehub/forgehub-backend</b> initialized</span>
            </div>
            <span className="text-slate-500">2026-08-30 02:39:35</span>
          </div>

          <div className="p-4 flex items-center justify-between text-slate-300">
            <div className="flex items-center gap-3">
              <span className="px-2 py-0.5 rounded bg-purple-950 text-purple-400 border border-purple-800">BRANCH_PROTECT</span>
              <span>Updated protection rules on branch <b>main</b> (Approvals: 2)</span>
            </div>
            <span className="text-slate-500">2026-08-30 02:30:00</span>
          </div>
        </div>
      </div>
    </div>
  );
};
