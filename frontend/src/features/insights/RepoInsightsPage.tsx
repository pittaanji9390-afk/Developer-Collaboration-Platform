import React from 'react';
import { useParams } from 'react-router-dom';
import { Activity, BarChart2, GitCommit, Users, TrendingUp } from 'lucide-react';

export const RepoInsightsPage: React.FC = () => {
  const { owner, repo } = useParams<{ owner: string; repo: string }>();

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 w-full space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-white">Insights & Metrics</h1>
        <p className="text-xs text-slate-400 mt-1">Activity frequency, code velocity, and contributor statistics for {owner}/{repo}</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase">Total Commits</span>
            <GitCommit className="w-5 h-5 text-forge-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">1,840</div>
          <div className="text-xs text-emerald-400 mt-1 font-medium">+48 this week</div>
        </div>

        <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase">Active Contributors</span>
            <Users className="w-5 h-5 text-purple-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">24</div>
          <div className="text-xs text-slate-400 mt-1 font-medium">Across 6 timezones</div>
        </div>

        <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase">Median Review Time</span>
            <TrendingUp className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">2.4h</div>
          <div className="text-xs text-emerald-400 mt-1 font-medium">-30% from last month</div>
        </div>
      </div>

      <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-4">
        <h3 className="text-sm font-bold text-white">Commit Frequency Punchcard (Day of Week vs Hour)</h3>
        <div className="grid grid-cols-24 gap-1 overflow-x-auto pb-2">
          {Array.from({ length: 7 * 24 }).map((_, i) => {
            const count = (i * 3 + 7) % 10;
            const bg = count > 6 ? 'bg-forge-400' : count > 3 ? 'bg-forge-600' : count > 0 ? 'bg-forge-900 border border-forge-800' : 'bg-surface-950';
            return (
              <div
                key={i}
                className={`w-3.5 h-3.5 rounded-sm ${bg}`}
                title={`Hour ${(i % 24)}: ${count} commits`}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
};
