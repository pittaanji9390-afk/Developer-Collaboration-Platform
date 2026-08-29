import React from 'react';
import { useParams } from 'react-router-dom';
import { GitMerge, Clock, CheckCircle2, Play, Cpu, AlertCircle } from 'lucide-react';
import { Button } from '../../components/ui/Button';

export const MergeQueuePage: React.FC = () => {
  const { owner, repo } = useParams<{ owner: string; repo: string }>();

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 w-full space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-surface-800">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2.5">
            <GitMerge className="w-6 h-6 text-forge-400" />
            <span>Merge Train Queue</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Automated speculative CI pipelining for high-frequency merges to branch <b>main</b>
          </p>
        </div>

        <div className="flex items-center gap-3">
          <span className="px-3 py-1 text-xs font-mono rounded-full bg-emerald-950 border border-emerald-800 text-emerald-400">
            Train Status: Running
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-2">
          <span className="text-xs font-semibold text-slate-400 uppercase">Currently Testing (Position 1)</span>
          <div className="text-xl font-bold text-white">#108: Feat - AST Vulnerability Parser</div>
          <div className="flex items-center gap-2 text-xs text-forge-400 font-mono">
            <Cpu className="w-4 h-4 animate-spin" />
            <span>Speculative build on top of main...</span>
          </div>
        </div>

        <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-2">
          <span className="text-xs font-semibold text-slate-400 uppercase">Queued Behind</span>
          <div className="text-xl font-bold text-white">2 PRs in Line</div>
          <div className="text-xs text-slate-400 font-mono">Estimated queue flush: 12 mins</div>
        </div>

        <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-2">
          <span className="text-xs font-semibold text-slate-400 uppercase">Merge Velocity</span>
          <div className="text-xl font-bold text-white">100% Green Merges</div>
          <div className="text-xs text-emerald-400 font-mono">Zero broken trunk incidents</div>
        </div>
      </div>
    </div>
  );
};
