import React, { useState, useEffect } from 'react';
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
    <div className="max-w-7xl mx-auto px-4 py-6 w-full space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={() => setStatus('OPEN')}
            className={`flex items-center gap-2 text-sm font-semibold ${
              status === 'OPEN' ? 'text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <CircleDot className="w-4 h-4 text-emerald-400" />
            <span>Open</span>
          </button>
          <button
            onClick={() => setStatus('CLOSED')}
            className={`flex items-center gap-2 text-sm font-semibold ${
              status === 'CLOSED' ? 'text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <CheckCircle2 className="w-4 h-4 text-purple-400" />
            <span>Closed</span>
          </button>
        </div>

        <Link
          to={`/${owner}/${repo}/issues/new`}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-white bg-forge-600 hover:bg-forge-500 rounded-lg transition-colors"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>New Issue</span>
        </Link>
      </div>

      <div className="border border-surface-800 rounded-xl overflow-hidden bg-surface-900 divide-y divide-surface-800">
        {issues.map((issue) => (
          <div key={issue.id} className="flex items-start justify-between p-4 hover:bg-surface-800/40 transition-colors">
            <div className="flex items-start gap-3">
              <CircleDot className="w-4 h-4 text-emerald-400 mt-0.5" />
              <div>
                <Link to={`/${owner}/${repo}/issues/${issue.number}`} className="text-sm font-semibold text-white hover:text-forge-400 transition-colors">
                  {issue.title}
                </Link>
                <div className="text-xs text-slate-400 mt-1">
                  #{issue.number} opened by {issue.authorUsername}
                </div>
              </div>
            </div>
            {issue.commentsCount > 0 && (
              <span className="text-xs text-slate-400">{issue.commentsCount} comments</span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
