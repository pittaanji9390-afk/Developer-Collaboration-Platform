import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { Shield, Key, Webhook, Users, Trash2, Save } from 'lucide-react';
import { Button } from '../../components/ui/Button';

export const RepoSettingsPage: React.FC = () => {
  const { owner, repo } = useParams<{ owner: string; repo: string }>();
  const [activeTab, setActiveTab] = useState<'general' | 'branches' | 'webhooks' | 'secrets'>('general');

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 w-full space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white">Repository Settings</h2>
        <p className="text-xs text-slate-400 mt-1">Manage options, branch rules, webhooks, and secrets for {owner}/{repo}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="space-y-1">
          <button
            onClick={() => setActiveTab('general')}
            className={`w-full flex items-center gap-2.5 px-3 py-2 text-sm font-medium rounded-lg text-left transition-colors ${
              activeTab === 'general' ? 'bg-surface-800 text-white' : 'text-slate-400 hover:text-white hover:bg-surface-800/50'
            }`}
          >
            <Shield className="w-4 h-4" />
            <span>General</span>
          </button>

          <button
            onClick={() => setActiveTab('branches')}
            className={`w-full flex items-center gap-2.5 px-3 py-2 text-sm font-medium rounded-lg text-left transition-colors ${
              activeTab === 'branches' ? 'bg-surface-800 text-white' : 'text-slate-400 hover:text-white hover:bg-surface-800/50'
            }`}
          >
            <Shield className="w-4 h-4 text-purple-400" />
            <span>Branch Protection</span>
          </button>

          <button
            onClick={() => setActiveTab('webhooks')}
            className={`w-full flex items-center gap-2.5 px-3 py-2 text-sm font-medium rounded-lg text-left transition-colors ${
              activeTab === 'webhooks' ? 'bg-surface-800 text-white' : 'text-slate-400 hover:text-white hover:bg-surface-800/50'
            }`}
          >
            <Webhook className="w-4 h-4 text-emerald-400" />
            <span>Webhooks</span>
          </button>

          <button
            onClick={() => setActiveTab('secrets')}
            className={`w-full flex items-center gap-2.5 px-3 py-2 text-sm font-medium rounded-lg text-left transition-colors ${
              activeTab === 'secrets' ? 'bg-surface-800 text-white' : 'text-slate-400 hover:text-white hover:bg-surface-800/50'
            }`}
          >
            <Key className="w-4 h-4 text-amber-400" />
            <span>Secrets & Vault</span>
          </button>
        </div>

        <div className="md:col-span-3 space-y-6">
          {activeTab === 'general' && (
            <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-4">
              <h3 className="text-base font-bold text-white">Repository Name & Visibility</h3>
              <div className="space-y-3 max-w-md">
                <div>
                  <label className="block mb-1 text-xs font-medium text-slate-300">Repository Name</label>
                  <input
                    type="text"
                    defaultValue={repo}
                    className="w-full py-2 px-3 text-sm bg-surface-950 border border-surface-800 rounded-lg text-white"
                  />
                </div>
                <div>
                  <label className="block mb-1 text-xs font-medium text-slate-300">Default Branch</label>
                  <input
                    type="text"
                    defaultValue="main"
                    className="w-full py-2 px-3 text-sm bg-surface-950 border border-surface-800 rounded-lg text-white"
                  />
                </div>
              </div>
              <Button size="sm" className="mt-2">Save Changes</Button>
            </div>
          )}

          {activeTab === 'branches' && (
            <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-4">
              <h3 className="text-base font-bold text-white">Branch Protection Rules</h3>
              <div className="p-4 bg-surface-950 border border-surface-800 rounded-xl space-y-3 text-sm">
                <div className="flex items-center justify-between">
                  <span className="font-mono font-bold text-forge-400">main</span>
                  <span className="text-xs text-emerald-400 font-medium">Active</span>
                </div>
                <div className="space-y-2 text-xs text-slate-400">
                  <div>✔ Require pull request before merging (Required approvals: 1)</div>
                  <div>✔ Require all conversations to be resolved</div>
                  <div>✔ Direct push blocked (Enforce admins: true)</div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'secrets' && (
            <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-base font-bold text-white">Repository Secrets (AES-256-GCM Encrypted)</h3>
                <Button size="sm">Add Secret</Button>
              </div>
              <div className="divide-y divide-surface-800 border border-surface-800 rounded-xl bg-surface-950">
                <div className="flex items-center justify-between p-3.5 text-xs font-mono text-slate-300">
                  <span className="font-bold text-forge-400">NPM_AUTH_TOKEN</span>
                  <span className="text-slate-500">Updated 2 days ago</span>
                </div>
                <div className="flex items-center justify-between p-3.5 text-xs font-mono text-slate-300">
                  <span className="font-bold text-forge-400">DEPLOY_SSH_KEY</span>
                  <span className="text-slate-500">Updated 1 week ago</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
