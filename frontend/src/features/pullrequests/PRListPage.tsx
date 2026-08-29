import React, { useState, useEffect } from 'react';
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
    <div className="max-w-7xl mx-auto px-4 py-6 w-full space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={() => setStatus('OPEN')}
            className={`flex items-center gap-2 text-sm font-semibold ${
              status === 'OPEN' ? 'text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <GitPullRequest className="w-4 h-4 text-emerald-400" />
            <span>Open</span>
          </button>
          <button
            onClick={() => setStatus('MERGED')}
            className={`flex items-center gap-2 text-sm font-semibold ${
              status === 'MERGED' ? 'text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <CheckCircle2 className="w-4 h-4 text-purple-400" />
            <span>Merged</span>
          </button>
        </div>

        <Link
          to={`/${owner}/${repo}/pulls/new`}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-white bg-forge-600 hover:bg-forge-500 rounded-lg transition-colors"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>New Pull Request</span>
        </Link>
      </div>

      <div className="border border-surface-800 rounded-xl overflow-hidden bg-surface-900 divide-y divide-surface-800">
        {prs.map((pr) => (
          <div key={pr.id} className="flex items-start justify-between p-4 hover:bg-surface-800/40 transition-colors">
            <div className="flex items-start gap-3">
              <GitPullRequest className={`w-4 h-4 mt-0.5 ${pr.status === 'MERGED' ? 'text-purple-400' : 'text-emerald-400'}`} />
              <div>
                <Link to={`/${owner}/${repo}/pulls/${pr.number}`} className="text-sm font-semibold text-white hover:text-forge-400 transition-colors">
                  {pr.title}
                </Link>
                <div className="text-xs text-slate-400 mt-1 flex items-center gap-2">
                  <span>#{pr.number} opened by {pr.authorUsername}</span>
                  <span>•</span>
                  <span className="font-mono bg-surface-800 px-1.5 py-0.5 rounded text-[11px]">{pr.sourceBranch} → {pr.targetBranch}</span>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-3 text-xs font-mono">
              <span className="text-emerald-400">+{pr.additions}</span>
              <span className="text-red-400">-{pr.deletions}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
