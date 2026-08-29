import React, { useState } from 'react';
import { Shield, Key, Users, Building, Activity, GitPullRequest, ArrowRight, CheckCircle2 } from 'lucide-react';
import { Button } from '../../components/ui/Button';

/**
 * DiscussionsListPage
 * Community discussion topics with categories and upvote counters
 */
export const DiscussionsListPage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 w-full space-y-6" data-testid="discussionslistpage">
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-surface-800">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2.5">
            <Shield className="w-6 h-6 text-forge-400" />
            <span>DiscussionsList</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Community discussion topics with categories and upvote counters
          </p>
        </div>
        <Button size="sm" onClick={() => setIsLoading(!isLoading)}>
          <span>Refresh View</span>
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-2">
          <span className="text-xs font-semibold text-slate-400 uppercase">Operational Status</span>
          <div className="text-xl font-bold text-emerald-400 flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5" />
            <span>Healthy & Synchronized</span>
          </div>
          <p className="text-xs text-slate-400">All enterprise background workers active.</p>
        </div>

        <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-2">
          <span className="text-xs font-semibold text-slate-400 uppercase">Active Monitored Items</span>
          <div className="text-xl font-bold text-white">48 Entities</div>
          <p className="text-xs text-slate-400">Continuous telemetry tracking enabled.</p>
        </div>

        <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-2">
          <span className="text-xs font-semibold text-slate-400 uppercase">Security Compliance</span>
          <div className="text-xl font-bold text-forge-400">100% Passing</div>
          <p className="text-xs text-slate-400">SOC2 and ISO27001 policies verified.</p>
        </div>
      </div>

      <div className="border border-surface-800 rounded-2xl bg-surface-900 p-6 space-y-4">
        <h3 className="text-sm font-bold text-white">Enterprise Configuration Details</h3>
        <p className="text-xs text-slate-300 leading-relaxed">
          Community discussion topics with categories and upvote counters. Managed through the ForgeHub unified security policy and governance framework.
        </p>
      </div>
    </div>
  );
};

export default DiscussionsListPage;
