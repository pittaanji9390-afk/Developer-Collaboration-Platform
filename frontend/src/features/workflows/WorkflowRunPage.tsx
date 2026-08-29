import React, { useState } from 'react';
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
    <div className="max-w-7xl mx-auto px-4 py-6 w-full space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4 p-6 bg-surface-900 border border-surface-800 rounded-2xl">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 rounded-xl bg-emerald-950 border border-emerald-800 flex items-center justify-center text-emerald-400">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-bold text-white">CI / Build & Test #104</h2>
              <span className="px-2 py-0.5 text-xs font-mono bg-emerald-950 border border-emerald-800 text-emerald-400 rounded-full">
                Success
              </span>
            </div>
            <div className="flex items-center gap-4 text-xs text-slate-400 mt-1 font-mono">
              <span className="flex items-center gap-1"><GitCommit className="w-3.5 h-3.5" /> main (37353d3)</span>
              <span>•</span>
              <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" /> Duration: 24s</span>
            </div>
          </div>
        </div>

        <Button variant="secondary" size="sm" className="flex items-center gap-1.5">
          <RotateCw className="w-3.5 h-3.5" />
          <span>Re-run Jobs</span>
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="space-y-2">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 px-2">Pipeline Jobs</h3>
          <div className="bg-surface-900 border border-surface-800 rounded-xl overflow-hidden divide-y divide-surface-800">
            <button
              onClick={() => setSelectedJob('lint')}
              className={`w-full flex items-center justify-between p-3.5 text-left text-sm transition-colors ${
                selectedJob === 'lint' ? 'bg-surface-800 font-semibold text-white' : 'hover:bg-surface-800/50 text-slate-300'
              }`}
            >
              <div className="flex items-center gap-2.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>Frontend Lint & Typecheck</span>
              </div>
              <span className="text-xs font-mono text-slate-500">8s</span>
            </button>

            <button
              onClick={() => setSelectedJob('test')}
              className={`w-full flex items-center justify-between p-3.5 text-left text-sm transition-colors ${
                selectedJob === 'test' ? 'bg-surface-800 font-semibold text-white' : 'hover:bg-surface-800/50 text-slate-300'
              }`}
            >
              <div className="flex items-center gap-2.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>Backend Compile & JUnit Tests</span>
              </div>
              <span className="text-xs font-mono text-slate-500">16s</span>
            </button>
          </div>
        </div>

        <div className="md:col-span-3 bg-surface-950 border border-surface-800 rounded-2xl overflow-hidden flex flex-col font-mono text-xs shadow-2xl">
          <div className="flex items-center justify-between px-4 py-3 bg-surface-900 border-b border-surface-800 text-slate-400">
            <div className="flex items-center gap-2">
              <Terminal className="w-4 h-4 text-forge-400" />
              <span className="font-semibold text-slate-200">Runner: Linux-x64-Runner-01 (Isolated Container)</span>
            </div>
            <span className="text-emerald-400">Streaming Logs Complete</span>
          </div>

          <pre className="p-4 text-slate-300 overflow-x-auto whitespace-pre-wrap leading-relaxed max-h-[500px]">
            {logs}
          </pre>
        </div>
      </div>
    </div>
  );
};
