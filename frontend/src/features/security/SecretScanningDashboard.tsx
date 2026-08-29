import React from 'react';
import { ShieldAlert, AlertTriangle, CheckCircle2, Lock, Eye, ExternalLink } from 'lucide-react';
import { Button } from '../../components/ui/Button';

export const SecretScanningDashboard: React.FC = () => {
  const findings = [
    { id: '1', rule: 'AWS_ACCESS_KEY_ID', severity: 'CRITICAL', file: 'backend/src/main/resources/application-prod.yml', line: 42, token: 'AKIA...9F8A', entropy: 4.8 },
    { id: '2', rule: 'GITHUB_PAT', severity: 'HIGH', file: 'scripts/deploy.sh', line: 15, token: 'ghp_...7kQ2', entropy: 5.2 },
    { id: '3', rule: 'STRIPE_SECRET_KEY', severity: 'CRITICAL', file: 'backend/src/main/java/com/forgehub/billing/StripeClient.java', line: 28, token: 'sk_live_...99xA', entropy: 5.1 },
    { id: '4', rule: 'SLACK_WEBHOOK', severity: 'MEDIUM', file: 'docs/integrations.md', line: 89, token: 'https://hooks.slack.com/...', entropy: 3.9 }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 w-full space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-surface-800">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2.5">
            <ShieldAlert className="w-6 h-6 text-red-400" />
            <span>Secret Scanning & Credential Exposure Dashboard</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Automated entropy and pattern analysis across all repository commits and pull requests
          </p>
        </div>
        <Button size="sm" className="bg-red-600 hover:bg-red-500">Trigger Full Repository Scan</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-5 bg-surface-900 border border-surface-800 rounded-2xl">
          <span className="text-xs text-slate-400 uppercase font-semibold">Exposed Secrets</span>
          <div className="text-2xl font-bold text-red-400 mt-1">4 Active</div>
        </div>
        <div className="p-5 bg-surface-900 border border-surface-800 rounded-2xl">
          <span className="text-xs text-slate-400 uppercase font-semibold">Scanned Commits</span>
          <div className="text-2xl font-bold text-white mt-1">1,840</div>
        </div>
        <div className="p-5 bg-surface-900 border border-surface-800 rounded-2xl">
          <span className="text-xs text-slate-400 uppercase font-semibold">Entropy Threshold</span>
          <div className="text-2xl font-bold text-forge-400 mt-1">4.5 bits</div>
        </div>
        <div className="p-5 bg-surface-900 border border-surface-800 rounded-2xl">
          <span className="text-xs text-slate-400 uppercase font-semibold">Remediation SLA</span>
          <div className="text-2xl font-bold text-emerald-400 mt-1">100% On-Time</div>
        </div>
      </div>

      <div className="border border-surface-800 rounded-2xl bg-surface-900 overflow-hidden">
        <div className="p-4 border-b border-surface-800 font-bold text-sm text-white">Detected Credentials</div>
        <div className="divide-y divide-surface-800 text-xs font-mono">
          {findings.map((f) => (
            <div key={f.id} className="p-4 flex flex-wrap items-center justify-between gap-4 hover:bg-surface-800/40 transition-colors">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${f.severity === 'CRITICAL' ? 'bg-red-950 text-red-400 border border-red-800' : 'bg-amber-950 text-amber-400 border border-amber-800'}`}>
                    {f.severity}
                  </span>
                  <span className="text-white font-bold">{f.rule}</span>
                  <span className="text-slate-500 font-sans text-xs">at {f.file}:{f.line}</span>
                </div>
                <div className="text-slate-400 text-xs">Masked Token: <span className="text-slate-200 bg-surface-950 px-1.5 py-0.5 rounded">{f.token}</span> (Entropy: {f.entropy})</div>
              </div>
              <div className="flex items-center gap-2">
                <Button size="sm" variant="secondary">Revoke & Rotate</Button>
                <Button size="sm" variant="outline">Dismiss</Button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
