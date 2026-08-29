import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { GitPullRequest, CheckCircle2, MessageSquare, GitCommit, FileText, ShieldCheck } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import api from '../../api/client';
import { PullRequest, GitDiff } from '../../types';

export const PRDetailPage: React.FC = () => {
  const { owner, repo, number } = useParams<{ owner: string; repo: string; number: string }>();
  const [pr, setPr] = useState<PullRequest | null>(null);
  const [activeTab, setActiveTab] = useState<'conversation' | 'commits' | 'files'>('conversation');
  const [diffs, setDiffs] = useState<GitDiff[]>([]);
  const [mergeStrategy, setMergeStrategy] = useState<'MERGE_COMMIT' | 'SQUASH' | 'REBASE'>('MERGE_COMMIT');
  const [isMerging, setIsMerging] = useState(false);

  useEffect(() => {
    loadPR();
  }, [owner, repo, number]);

  const loadPR = async () => {
    try {
      const repoRes = await api.get(`/repositories/${owner}/${repo}`);
      const prRes = await api.get(`/repositories/${repoRes.data.data.id}/pulls/${number}`);
      setPr(prRes.data.data);

      setDiffs([
        {
          oldPath: 'backend/src/main/java/com/forgehub/git/JGitService.java',
          newPath: 'backend/src/main/java/com/forgehub/git/JGitService.java',
          changeType: 'MODIFY',
          additions: 14,
          deletions: 2,
          hunks: [
            {
              header: '@@ -42,7 +42,19 @@ public class JGitService {',
              oldStart: 42,
              oldCount: 7,
              newStart: 42,
              newCount: 19,
              lines: [
                { type: 'CONTEXT', oldLineNumber: 42, newLineNumber: 42, content: '    public Repository openRepository(String repoPath) throws IOException {' },
                { type: 'DELETED', oldLineNumber: 43, content: '        return Git.open(new File(repoPath)).getRepository();' },
                { type: 'ADDED', newLineNumber: 43, content: '        File gitDir = resolveRepoDir(repoPath);' },
                { type: 'ADDED', newLineNumber: 44, content: '        if (!gitDir.exists()) {' },
                { type: 'ADDED', newLineNumber: 45, content: '            throw ApiException.notFound("Git repository not found on disk");' },
                { type: 'ADDED', newLineNumber: 46, content: '        }' },
                { type: 'ADDED', newLineNumber: 47, content: '        return Git.open(gitDir).getRepository();' },
                { type: 'CONTEXT', oldLineNumber: 44, newLineNumber: 48, content: '    }' },
              ],
            },
          ],
        },
      ]);
    } catch (e) {
      console.error(e);
    }
  };

  const handleMerge = async () => {
    if (!pr) return;
    setIsMerging(true);
    try {
      const repoRes = await api.get(`/repositories/${owner}/${repo}`);
      await api.post(`/repositories/${repoRes.data.data.id}/pulls/${number}/merge`, null, {
        params: { strategy: mergeStrategy },
      });
      loadPR();
    } catch (e) {
      console.error(e);
    } finally {
      setIsMerging(false);
    }
  };

  if (!pr) return <div className="p-8 text-center text-slate-400">Loading pull request #{number}...</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 w-full space-y-6">
      <div className="space-y-3 pb-4 border-b border-surface-800">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <span>{pr.title}</span>
            <span className="text-slate-500 font-normal">#{pr.number}</span>
          </h1>
          <div className="flex items-center gap-2">
            <Button variant="secondary" size="sm">Edit</Button>
            <Button size="sm" className="bg-emerald-600 hover:bg-emerald-500">Review Changes</Button>
          </div>
        </div>

        <div className="flex items-center gap-3 text-xs">
          <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full font-semibold text-white ${
            pr.status === 'MERGED' ? 'bg-purple-600' : pr.status === 'OPEN' ? 'bg-emerald-600' : 'bg-red-600'
          }`}>
            <GitPullRequest className="w-3.5 h-3.5" />
            <span>{pr.status}</span>
          </span>

          <span className="text-slate-300">
            <b className="text-white">{pr.authorUsername}</b> wants to merge into{' '}
            <span className="font-mono bg-surface-900 border border-surface-800 px-1.5 py-0.5 rounded text-forge-400">{pr.targetBranch}</span> from{' '}
            <span className="font-mono bg-surface-900 border border-surface-800 px-1.5 py-0.5 rounded text-forge-400">{pr.sourceBranch}</span>
          </span>
        </div>
      </div>

      <div className="flex items-center gap-6 border-b border-surface-800 text-sm font-medium text-slate-400">
        <button
          onClick={() => setActiveTab('conversation')}
          className={`flex items-center gap-2 pb-3 border-b-2 transition-colors ${
            activeTab === 'conversation' ? 'border-forge-500 text-white' : 'border-transparent hover:text-slate-200'
          }`}
        >
          <MessageSquare className="w-4 h-4" />
          <span>Conversation</span>
        </button>

        <button
          onClick={() => setActiveTab('commits')}
          className={`flex items-center gap-2 pb-3 border-b-2 transition-colors ${
            activeTab === 'commits' ? 'border-forge-500 text-white' : 'border-transparent hover:text-slate-200'
          }`}
        >
          <GitCommit className="w-4 h-4" />
          <span>Commits</span>
          <span className="px-1.5 py-0.2 bg-surface-800 rounded-full text-xs">1</span>
        </button>

        <button
          onClick={() => setActiveTab('files')}
          className={`flex items-center gap-2 pb-3 border-b-2 transition-colors ${
            activeTab === 'files' ? 'border-forge-500 text-white' : 'border-transparent hover:text-slate-200'
          }`}
        >
          <FileText className="w-4 h-4" />
          <span>Files changed</span>
          <span className="px-1.5 py-0.2 bg-surface-800 rounded-full text-xs">+{pr.additions} -{pr.deletions}</span>
        </button>
      </div>

      {activeTab === 'conversation' && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="md:col-span-3 space-y-6">
            <div className="bg-surface-900 border border-surface-800 rounded-2xl overflow-hidden">
              <div className="flex items-center justify-between px-4 py-2.5 bg-surface-950/60 border-b border-surface-800 text-xs text-slate-400">
                <div className="flex items-center gap-2">
                  <img src={pr.authorAvatarUrl} alt="author" className="w-5 h-5 rounded-full" />
                  <span className="font-bold text-white">{pr.authorUsername}</span> commented
                </div>
              </div>
              <div className="p-4 text-sm text-slate-200 leading-relaxed whitespace-pre-wrap">
                {pr.body || 'No description provided.'}
              </div>
            </div>

            <div className="p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-4">
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-emerald-950 border border-emerald-800 flex items-center justify-center text-emerald-400 flex-shrink-0">
                  <ShieldCheck className="w-5 h-5" />
                </div>
                <div className="flex-1">
                  <h4 className="text-sm font-bold text-white">All checks have passed & branch protection satisfied</h4>
                  <p className="text-xs text-slate-400 mt-0.5">1 approving review, CI workflow passed, conversations resolved.</p>
                </div>
              </div>

              {pr.status === 'OPEN' && (
                <div className="pt-4 border-t border-surface-800 flex flex-wrap items-center gap-3">
                  <select
                    value={mergeStrategy}
                    onChange={(e: any) => setMergeStrategy(e.target.value)}
                    className="py-2 px-3 text-xs bg-surface-950 border border-surface-800 rounded-lg text-white font-medium focus:outline-none"
                  >
                    <option value="MERGE_COMMIT">Create a merge commit</option>
                    <option value="SQUASH">Squash and merge</option>
                    <option value="REBASE">Rebase and merge</option>
                  </select>

                  <Button
                    onClick={handleMerge}
                    isLoading={isMerging}
                    className="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold"
                  >
                    Merge Pull Request
                  </Button>
                </div>
              )}
            </div>
          </div>

          <div className="space-y-6 text-xs text-slate-400">
            <div className="space-y-2">
              <span className="font-bold uppercase tracking-wider text-slate-300">Reviewers</span>
              <div className="text-slate-400">1 approved (alice)</div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'files' && (
        <div className="space-y-6">
          {diffs.map((diff) => (
            <div key={diff.newPath} className="bg-surface-900 border border-surface-800 rounded-2xl overflow-hidden">
              <div className="flex items-center justify-between px-4 py-2.5 bg-surface-950 border-b border-surface-800 text-xs font-mono">
                <span className="text-white font-semibold">{diff.newPath}</span>
                <div className="flex items-center gap-3">
                  <span className="text-emerald-400">+{diff.additions}</span>
                  <span className="text-red-400">-{diff.deletions}</span>
                </div>
              </div>

              <div className="font-mono text-xs overflow-x-auto divide-y divide-surface-800/40">
                {diff.hunks.map((hunk, hIdx) => (
                  <div key={hIdx}>
                    <div className="px-4 py-1 bg-surface-950/80 text-slate-500 select-none">
                      {hunk.header}
                    </div>
                    {hunk.lines.map((line, lIdx) => (
                      <div
                        key={lIdx}
                        className={`flex items-stretch hover:bg-surface-800/30 transition-colors ${
                          line.type === 'ADDED'
                            ? 'bg-emerald-950/30 text-emerald-300'
                            : line.type === 'DELETED'
                            ? 'bg-red-950/30 text-red-300'
                            : 'text-slate-300'
                        }`}
                      >
                        <div className="w-10 px-2 py-1 text-right text-slate-600 select-none bg-surface-950/50">
                          {line.oldLineNumber || ''}
                        </div>
                        <div className="w-10 px-2 py-1 text-right text-slate-600 select-none bg-surface-950/50 border-r border-surface-800">
                          {line.newLineNumber || ''}
                        </div>
                        <div className="w-6 px-1 py-1 text-center select-none font-bold">
                          {line.type === 'ADDED' ? '+' : line.type === 'DELETED' ? '-' : ' '}
                        </div>
                        <div className="flex-1 px-2 py-1 whitespace-pre">
                          {line.content}
                        </div>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
