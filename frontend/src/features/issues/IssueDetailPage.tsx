import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { CircleDot, Send } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import api from '../../api/client';
import { Issue } from '../../types';

export const IssueDetailPage: React.FC = () => {
  const { owner, repo, number } = useParams<{ owner: string; repo: string; number: string }>();
  const [issue, setIssue] = useState<Issue | null>(null);
  const [commentText, setCommentText] = useState('');
  const [isPosting, setIsPosting] = useState(false);

  useEffect(() => {
    loadIssue();
  }, [owner, repo, number]);

  const loadIssue = async () => {
    try {
      const repoRes = await api.get(`/repositories/${owner}/${repo}`);
      const issueRes = await api.get(`/repositories/${repoRes.data.data.id}/issues/${number}`);
      setIssue(issueRes.data.data);
    } catch (e) {
      console.error(e);
    }
  };

  const handlePostComment = async () => {
    if (!issue || !commentText.trim()) return;
    setIsPosting(true);
    try {
      const repoRes = await api.get(`/repositories/${owner}/${repo}`);
      await api.post(`/repositories/${repoRes.data.data.id}/issues/${issue.id}/comments`, commentText);
      setCommentText('');
      loadIssue();
    } catch (e) {
      console.error(e);
    } finally {
      setIsPosting(false);
    }
  };

  if (!issue) return <div className="p-8 text-center text-slate-400">Loading issue #{number}...</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 w-full space-y-6">
      <div className="space-y-3 pb-4 border-b border-surface-800">
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <span>{issue.title}</span>
          <span className="text-slate-500 font-normal">#{issue.number}</span>
        </h1>

        <div className="flex items-center gap-3 text-xs">
          <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full font-semibold text-white ${
            issue.status === 'OPEN' ? 'bg-emerald-600' : 'bg-purple-600'
          }`}>
            <CircleDot className="w-3.5 h-3.5" />
            <span>{issue.status}</span>
          </span>

          <span className="text-slate-400">
            <b className="text-white">{issue.authorUsername}</b> opened this issue • {issue.commentsCount} comments
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="md:col-span-3 space-y-6">
          <div className="bg-surface-900 border border-surface-800 rounded-2xl overflow-hidden">
            <div className="flex items-center justify-between px-4 py-2.5 bg-surface-950/60 border-b border-surface-800 text-xs text-slate-400">
              <div className="flex items-center gap-2">
                <img src={issue.authorAvatarUrl} alt="author" className="w-5 h-5 rounded-full" />
                <span className="font-bold text-white">{issue.authorUsername}</span> commented
              </div>
            </div>
            <div className="p-4 text-sm text-slate-200 leading-relaxed whitespace-pre-wrap">
              {issue.body || 'No description provided.'}
            </div>
          </div>

          <div className="bg-surface-900 border border-surface-800 rounded-2xl p-4 space-y-3">
            <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Leave a comment</h4>
            <textarea
              rows={4}
              value={commentText}
              onChange={(e) => setCommentText(e.target.value)}
              placeholder="Write in Markdown..."
              className="w-full p-3 text-sm bg-surface-950 border border-surface-800 rounded-xl text-white focus:outline-none focus:border-forge-500"
            />
            <div className="flex items-center justify-between">
              <span className="text-[11px] text-slate-500">Markdown styling supported</span>
              <Button size="sm" onClick={handlePostComment} isLoading={isPosting} className="flex items-center gap-1.5">
                <Send className="w-3.5 h-3.5" />
                <span>Comment</span>
              </Button>
            </div>
          </div>
        </div>

        <div className="space-y-6 text-xs text-slate-400">
          <div className="space-y-2">
            <span className="font-bold uppercase tracking-wider text-slate-300">Assignees</span>
            <div className="text-slate-400">No one assigned</div>
          </div>

          <div className="space-y-2">
            <span className="font-bold uppercase tracking-wider text-slate-300">Labels</span>
            <div className="flex flex-wrap gap-1.5">
              <span className="px-2 py-0.5 rounded-full bg-forge-950 border border-forge-800 text-forge-400">enhancement</span>
              <span className="px-2 py-0.5 rounded-full bg-purple-950 border border-purple-800 text-purple-400">ui</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
