import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { Building2, Users, GitFork, Shield, Settings, Plus, Star } from 'lucide-react';
import { Button } from '../../components/ui/Button';

export const OrgDetailPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 w-full space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-surface-800">
        <div className="flex items-center gap-4">
          <img
            src={`https://api.dicebear.com/7.x/identicon/svg?seed=${slug}`}
            alt="org avatar"
            className="w-16 h-16 rounded-2xl border border-surface-700 bg-surface-900"
          />
          <div>
            <h1 className="text-2xl font-bold text-white">{slug?.toUpperCase()} Engineering</h1>
            <p className="text-xs text-slate-400 font-mono">@{slug} • Verified Enterprise Organization</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Link to={`/orgs/${slug}/settings`}>
            <Button variant="secondary" size="sm" className="flex items-center gap-1.5">
              <Settings className="w-4 h-4" />
              <span>Org Settings</span>
            </Button>
          </Link>
          <Button size="sm" className="flex items-center gap-1.5">
            <Plus className="w-4 h-4" />
            <span>New Repository</span>
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-4">
          <h3 className="text-base font-bold text-white">Repositories</h3>
          <div className="p-5 bg-surface-900 border border-surface-800 rounded-2xl space-y-3">
            <div className="flex items-center justify-between">
              <Link to={`/${slug}/developer-collaboration-platform`} className="font-bold text-forge-400 hover:underline">
                {slug}/developer-collaboration-platform
              </Link>
              <span className="px-2 py-0.5 text-[10px] font-mono border border-surface-700 rounded-full text-slate-400">Public</span>
            </div>
            <p className="text-xs text-slate-300">Production-grade developer collaboration platform inspired by GitHub and GitLab.</p>
            <div className="flex items-center gap-4 text-xs text-slate-400 font-mono pt-1">
              <span className="flex items-center gap-1"><Star className="w-3.5 h-3.5" /> 42</span>
              <span className="flex items-center gap-1"><GitFork className="w-3.5 h-3.5" /> 8</span>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <h3 className="text-base font-bold text-white">Teams & Members</h3>
          <div className="p-5 bg-surface-900 border border-surface-800 rounded-2xl space-y-3 text-xs text-slate-300">
            <div className="flex items-center justify-between pb-2 border-b border-surface-800">
              <span className="font-semibold text-white">@forgehub/maintainers</span>
              <span className="text-slate-500">6 members</span>
            </div>
            <div className="flex items-center justify-between pb-2 border-b border-surface-800">
              <span className="font-semibold text-white">@forgehub/security-team</span>
              <span className="text-slate-500">4 members</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="font-semibold text-white">@forgehub/core-engineers</span>
              <span className="text-slate-500">18 members</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
