from common_writer import write_file

kanban_page = """import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { Plus, MoreHorizontal, CircleDot, GitPullRequest, Tag } from 'lucide-react';
import { Button } from '../../components/ui/Button';

interface Card {
  id: string;
  title: string;
  type: 'issue' | 'pr' | 'note';
  number?: number;
  labels?: string[];
  assigneeAvatar?: string;
}

interface Column {
  id: string;
  name: string;
  cards: Card[];
}

export const KanbanBoardPage: React.FC = () => {
  const { owner, repo } = useParams<{ owner: string; repo: string }>();

  const [columns, setColumns] = useState<Column[]>([
    {
      id: 'backlog',
      name: 'Backlog',
      cards: [
        { id: 'c1', title: 'Implement OAuth2 PKCE social login flow', type: 'issue', number: 42, labels: ['security', 'auth'] },
        { id: 'c2', title: 'Optimize JGit diff line-by-line streaming algorithm', type: 'issue', number: 45, labels: ['performance'] },
      ],
    },
    {
      id: 'todo',
      name: 'To Do',
      cards: [
        { id: 'c3', title: 'Add dark mode toggle and Monaco theme sync', type: 'issue', number: 50, labels: ['ui'] },
      ],
    },
    {
      id: 'in-progress',
      name: 'In Progress',
      cards: [
        { id: 'c4', title: 'Feature: HMAC-SHA256 webhook delivery engine', type: 'pr', number: 52, labels: ['feature'] },
      ],
    },
    {
      id: 'review',
      name: 'In Review',
      cards: [
        { id: 'c5', title: 'Refactor RBAC SpEL permission evaluator', type: 'pr', number: 49, labels: ['security'] },
      ],
    },
    {
      id: 'done',
      name: 'Done',
      cards: [
        { id: 'c6', title: 'Flyway database schema baseline V1 to V7', type: 'pr', number: 40, labels: ['database'] },
      ],
    },
  ]);

  return (
    <div className=\"max-w-7xl mx-auto px-4 py-6 w-full space-y-6\">
      <div className=\"flex items-center justify-between\">
        <div>
          <h2 className=\"text-xl font-bold text-white\">Engineering Roadmap 2026</h2>
          <p className=\"text-xs text-slate-400 mt-1\">Kanban project board linked to {owner}/{repo}</p>
        </div>
        <Button size=\"sm\" className=\"flex items-center gap-1.5\">
          <Plus className=\"w-4 h-4\" />
          <span>Add Column</span>
        </Button>
      </div>

      <div className=\"flex gap-4 overflow-x-auto pb-6\">
        {columns.map((col) => (
          <div key={col.id} className=\"flex-shrink-0 w-80 bg-surface-900 border border-surface-800 rounded-2xl flex flex-col max-h-[75vh]\">
            <div className=\"flex items-center justify-between p-4 border-b border-surface-800\">
              <div className=\"flex items-center gap-2\">
                <span className=\"text-sm font-semibold text-white\">{col.name}</span>
                <span className=\"px-2 py-0.5 text-xs font-mono bg-surface-800 text-slate-400 rounded-full\">
                  {col.cards.length}
                </span>
              </div>
              <button className=\"p-1 text-slate-400 hover:text-white rounded\">
                <MoreHorizontal className=\"w-4 h-4\" />
              </button>
            </div>

            <div className=\"p-3 space-y-3 flex-1 overflow-y-auto\">
              {col.cards.map((card) => (
                <div
                  key={card.id}
                  className=\"p-4 bg-surface-950/80 border border-surface-800/80 hover:border-surface-700 rounded-xl shadow-sm cursor-grab transition-all space-y-2.5\"
                >
                  <div className=\"flex items-start gap-2\">
                    {card.type === 'issue' ? (
                      <CircleDot className=\"w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0\" />
                    ) : (
                      <GitPullRequest className=\"w-4 h-4 text-purple-400 mt-0.5 flex-shrink-0\" />
                    )}
                    <span className=\"text-sm font-medium text-slate-200 leading-snug\">{card.title}</span>
                  </div>

                  <div className=\"flex items-center justify-between pt-1\">
                    <span className=\"text-xs font-mono text-slate-500\">#{card.number}</span>
                    <div className=\"flex items-center gap-1.5\">
                      {card.labels?.map((l) => (
                        <span key={l} className=\"px-2 py-0.5 text-[10px] font-mono rounded bg-forge-950 border border-forge-800/60 text-forge-300\">
                          {l}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className=\"p-3 border-t border-surface-800\">
              <button className=\"w-full flex items-center justify-center gap-1.5 py-2 text-xs font-medium text-slate-400 hover:text-white hover:bg-surface-800 rounded-lg transition-colors\">
                <Plus className=\"w-3.5 h-3.5\" />
                <span>Add Item</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
"""
write_file("frontend/src/features/kanban/KanbanBoardPage.tsx", kanban_page)

workflow_run_page = """import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { CheckCircle2, CircleDot, Clock, Terminal, GitCommit, Play, RotateCw } from 'lucide-react';
import { Button } from '../../components/ui/Button';

export const WorkflowRunPage: React.FC = () => {
  const { owner, repo, runId } = useParams<{ owner: string; repo: string; runId: string }>();

  const [selectedJob, setSelectedJob] = useState('test');

  const logs = `
$ git clone https://github.com/${owner}/${repo}.git workspace
Cloning into 'workspace'...
$ cd workspace && git checkout 37353d3
HEAD is now at 37353d3 feat(core): initialize ForgeHub architecture
$ ./mvnw clean verify -B
[INFO] Scanning for projects...
[INFO] -------------------< com.forgehub:forgehub-backend >-------------------
[INFO] Building forgehub-backend 1.0.0
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] --- maven-compiler-plugin:3.13.0:compile (default-compile) @ forgehub-backend ---
[INFO] Compiling 94 source files with javac [debug target 21] to target/classes
[INFO] --- maven-surefire-plugin:3.2.5:test (default-test) @ forgehub-backend ---
[INFO] Running com.forgehub.AuthIntegrationTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1.428 s
[INFO] Running com.forgehub.AESGCMVaultTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.112 s
[INFO] Running com.forgehub.MarkdownSanitizerTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.089 s
[INFO] 
[INFO] Results:
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0
[INFO] 
[INFO] BUILD SUCCESS
[INFO] Total time:  6.412 s
`;

  return (
    <div className=\"max-w-7xl mx-auto px-4 py-6 w-full space-y-6\">
      <div className=\"flex flex-wrap items-center justify-between gap-4 p-6 bg-surface-900 border border-surface-800 rounded-2xl\">
        <div className=\"flex items-center gap-4\">
          <div className=\"w-10 h-10 rounded-xl bg-emerald-950 border border-emerald-800 flex items-center justify-center text-emerald-400\">
            <CheckCircle2 className=\"w-6 h-6\" />
          </div>
          <div>
            <div className=\"flex items-center gap-2\">
              <h2 className=\"text-xl font-bold text-white\">CI / Build & Test #104</h2>
              <span className=\"px-2 py-0.5 text-xs font-mono bg-emerald-950 border border-emerald-800 text-emerald-400 rounded-full\">
                Success
              </span>
            </div>
            <div className=\"flex items-center gap-4 text-xs text-slate-400 mt-1 font-mono\">
              <span className=\"flex items-center gap-1\"><GitCommit className=\"w-3.5 h-3.5\" /> main (37353d3)</span>
              <span>•</span>
              <span className=\"flex items-center gap-1\"><Clock className=\"w-3.5 h-3.5\" /> Duration: 24s</span>
            </div>
          </div>
        </div>

        <Button variant=\"secondary\" size=\"sm\" className=\"flex items-center gap-1.5\">
          <RotateCw className=\"w-3.5 h-3.5\" />
          <span>Re-run Jobs</span>
        </Button>
      </div>

      <div className=\"grid grid-cols-1 md:grid-cols-4 gap-6\">
        <div className=\"space-y-2\">
          <h3 className=\"text-xs font-semibold uppercase tracking-wider text-slate-400 px-2\">Pipeline Jobs</h3>
          <div className=\"bg-surface-900 border border-surface-800 rounded-xl overflow-hidden divide-y divide-surface-800\">
            <button
              onClick={() => setSelectedJob('lint')}
              className={`w-full flex items-center justify-between p-3.5 text-left text-sm transition-colors ${
                selectedJob === 'lint' ? 'bg-surface-800 font-semibold text-white' : 'hover:bg-surface-800/50 text-slate-300'
              }`}
            >
              <div className=\"flex items-center gap-2.5\">
                <CheckCircle2 className=\"w-4 h-4 text-emerald-400\" />
                <span>Frontend Lint & Typecheck</span>
              </div>
              <span className=\"text-xs font-mono text-slate-500\">8s</span>
            </button>

            <button
              onClick={() => setSelectedJob('test')}
              className={`w-full flex items-center justify-between p-3.5 text-left text-sm transition-colors ${
                selectedJob === 'test' ? 'bg-surface-800 font-semibold text-white' : 'hover:bg-surface-800/50 text-slate-300'
              }`}
            >
              <div className=\"flex items-center gap-2.5\">
                <CheckCircle2 className=\"w-4 h-4 text-emerald-400\" />
                <span>Backend Compile & JUnit Tests</span>
              </div>
              <span className=\"text-xs font-mono text-slate-500\">16s</span>
            </button>
          </div>
        </div>

        <div className=\"md:col-span-3 bg-surface-950 border border-surface-800 rounded-2xl overflow-hidden flex flex-col font-mono text-xs shadow-2xl\">
          <div className=\"flex items-center justify-between px-4 py-3 bg-surface-900 border-b border-surface-800 text-slate-400\">
            <div className=\"flex items-center gap-2\">
              <Terminal className=\"w-4 h-4 text-forge-400\" />
              <span className=\"font-semibold text-slate-200\">Runner: Linux-x64-Runner-01 (Isolated Container)</span>
            </div>
            <span className=\"text-emerald-400\">Streaming Logs Complete</span>
          </div>

          <pre className=\"p-4 text-slate-300 overflow-x-auto whitespace-pre-wrap leading-relaxed max-h-[500px]\">
            {logs}
          </pre>
        </div>
      </div>
    </div>
  );
};
"""
write_file("frontend/src/features/workflows/WorkflowRunPage.tsx", workflow_run_page)

admin_dashboard = """import React from 'react';
import { Users, Building2, GitFork, ShieldAlert, Cpu, Activity, Server } from 'lucide-react';

export const AdminDashboardPage: React.FC = () => {
  return (
    <div className=\"max-w-7xl mx-auto px-4 py-8 w-full space-y-8\">
      <div>
        <h1 className=\"text-2xl font-bold text-white\">Platform Administration Console</h1>
        <p className=\"text-sm text-slate-400 mt-1\">System health, security oversight, runner pools and audit analytics</p>
      </div>

      <div className=\"grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6\">
        <div className=\"p-6 bg-surface-900 border border-surface-800 rounded-2xl\">
          <div className=\"flex items-center justify-between text-slate-400 mb-3\">
            <span className=\"text-xs font-semibold uppercase\">Total Developers</span>
            <Users className=\"w-5 h-5 text-forge-400\" />
          </div>
          <div className=\"text-3xl font-extrabold text-white\">1,420</div>
          <div className=\"text-xs text-emerald-400 mt-2 font-medium\">+12% this month</div>
        </div>

        <div className=\"p-6 bg-surface-900 border border-surface-800 rounded-2xl\">
          <div className=\"flex items-center justify-between text-slate-400 mb-3\">
            <span className=\"text-xs font-semibold uppercase\">Organizations</span>
            <Building2 className=\"w-5 h-5 text-purple-400\" />
          </div>
          <div className=\"text-3xl font-extrabold text-white\">86</div>
          <div className=\"text-xs text-slate-400 mt-2 font-medium\">Active Enterprise Teams</div>
        </div>

        <div className=\"p-6 bg-surface-900 border border-surface-800 rounded-2xl\">
          <div className=\"flex items-center justify-between text-slate-400 mb-3\">
            <span className=\"text-xs font-semibold uppercase\">Repositories</span>
            <GitFork className=\"w-5 h-5 text-emerald-400\" />
          </div>
          <div className=\"text-3xl font-extrabold text-white\">3,892</div>
          <div className=\"text-xs text-slate-400 mt-2 font-medium\">Native JGit Bare Stores</div>
        </div>

        <div className=\"p-6 bg-surface-900 border border-surface-800 rounded-2xl\">
          <div className=\"flex items-center justify-between text-slate-400 mb-3\">
            <span className=\"text-xs font-semibold uppercase\">CI Runner Pool</span>
            <Cpu className=\"w-5 h-5 text-amber-400\" />
          </div>
          <div className=\"text-3xl font-extrabold text-white\">12 / 12</div>
          <div className=\"text-xs text-emerald-400 mt-2 font-medium\">All Agents Healthy</div>
        </div>
      </div>

      <div className=\"border border-surface-800 rounded-2xl bg-surface-900 overflow-hidden\">
        <div className=\"p-4 border-b border-surface-800 flex items-center justify-between\">
          <h3 className=\"text-sm font-bold text-white\">Recent Platform Audit Logs</h3>
        </div>
        <div className=\"divide-y divide-surface-800 font-mono text-xs\">
          <div className=\"p-4 flex items-center justify-between text-slate-300\">
            <div className=\"flex items-center gap-3\">
              <span className=\"px-2 py-0.5 rounded bg-surface-800 text-slate-400\">AUTH_LOGIN</span>
              <span>User <b>alice</b> logged in successfully</span>
            </div>
            <span className=\"text-slate-500\">2026-08-30 02:45:10</span>
          </div>

          <div className=\"p-4 flex items-center justify-between text-slate-300\">
            <div className=\"flex items-center gap-3\">
              <span className=\"px-2 py-0.5 rounded bg-forge-950 text-forge-400 border border-forge-800\">REPO_CREATE</span>
              <span>Repository <b>forgehub/forgehub-backend</b> initialized</span>
            </div>
            <span className=\"text-slate-500\">2026-08-30 02:39:35</span>
          </div>

          <div className=\"p-4 flex items-center justify-between text-slate-300\">
            <div className=\"flex items-center gap-3\">
              <span className=\"px-2 py-0.5 rounded bg-purple-950 text-purple-400 border border-purple-800\">BRANCH_PROTECT</span>
              <span>Updated protection rules on branch <b>main</b> (Approvals: 2)</span>
            </div>
            <span className=\"text-slate-500\">2026-08-30 02:30:00</span>
          </div>
        </div>
      </div>
    </div>
  );
};
"""
write_file("frontend/src/features/admin/AdminDashboardPage.tsx", admin_dashboard)

print("build_frontend_advanced_features complete.")