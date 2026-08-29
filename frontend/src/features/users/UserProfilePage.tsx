import React from 'react';
import { useParams } from 'react-router-dom';
import { GitFork, Star, MapPin, Building, Link as LinkIcon, Calendar } from 'lucide-react';

export const UserProfilePage: React.FC = () => {
  const { username } = useParams<{ username: string }>();

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 w-full">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        {/* Sidebar */}
        <div className="space-y-4">
          <img
            src={`https://api.dicebear.com/7.x/identicon/svg?seed=${username}`}
            alt="avatar"
            className="w-48 h-48 rounded-full border-2 border-surface-700 bg-surface-900 shadow-xl"
          />
          <div>
            <h1 className="text-2xl font-bold text-white">{username}</h1>
            <p className="text-sm text-slate-400 font-mono">@{username}</p>
          </div>
          <p className="text-sm text-slate-300 leading-relaxed">
            Building distributed systems, high-performance Git engines, and modern developer tooling.
          </p>

          <div className="pt-4 border-t border-surface-800 space-y-2 text-xs text-slate-400">
            <div className="flex items-center gap-2"><Building className="w-4 h-4 text-slate-500" /> ForgeHub Labs</div>
            <div className="flex items-center gap-2"><MapPin className="w-4 h-4 text-slate-500" /> San Francisco, CA</div>
            <div className="flex items-center gap-2"><LinkIcon className="w-4 h-4 text-slate-500" /> https://forgehub.dev</div>
            <div className="flex items-center gap-2"><Calendar className="w-4 h-4 text-slate-500" /> Joined August 2026</div>
          </div>
        </div>

        {/* Repositories and Contributions Heatmap */}
        <div className="md:col-span-3 space-y-6">
          <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-white">524 Contributions in 2026</h3>
            {/* Heatmap grid */}
            <div className="grid grid-flow-col grid-rows-7 gap-1.5 overflow-x-auto pb-2">
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

          <div className="space-y-4">
            <h3 className="text-lg font-bold text-white">Popular Repositories</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="p-5 bg-surface-900 border border-surface-800 rounded-2xl hover:border-surface-700 transition-colors space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-forge-400 hover:underline cursor-pointer">developer-collaboration-platform</span>
                  <span className="px-2 py-0.5 text-[10px] font-mono border border-surface-700 rounded-full text-slate-400">Public</span>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">Production-ready enterprise developer platform with JGit, CI/CD, and RBAC.</p>
                <div className="flex items-center gap-4 text-xs text-slate-400 font-mono pt-2">
                  <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-orange-500 inline-block" /> Java</span>
                  <span className="flex items-center gap-1"><Star className="w-3.5 h-3.5" /> 1,284</span>
                  <span className="flex items-center gap-1"><GitFork className="w-3.5 h-3.5" /> 240</span>
                </div>
              </div>

              <div className="p-5 bg-surface-900 border border-surface-800 rounded-2xl hover:border-surface-700 transition-colors space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-forge-400 hover:underline cursor-pointer">forgehub-runner-isolated</span>
                  <span className="px-2 py-0.5 text-[10px] font-mono border border-surface-700 rounded-full text-slate-400">Public</span>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">Lightweight isolated CI execution daemon with streaming websocket output.</p>
                <div className="flex items-center gap-4 text-xs text-slate-400 font-mono pt-2">
                  <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-blue-500 inline-block" /> TypeScript</span>
                  <span className="flex items-center gap-1"><Star className="w-3.5 h-3.5" /> 490</span>
                  <span className="flex items-center gap-1"><GitFork className="w-3.5 h-3.5" /> 62</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
