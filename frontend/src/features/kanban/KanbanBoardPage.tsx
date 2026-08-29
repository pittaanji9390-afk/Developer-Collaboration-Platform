import React, { useState } from 'react';
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
    <div className="max-w-7xl mx-auto px-4 py-6 w-full space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white">Engineering Roadmap 2026</h2>
          <p className="text-xs text-slate-400 mt-1">Kanban project board linked to {owner}/{repo}</p>
        </div>
        <Button size="sm" className="flex items-center gap-1.5">
          <Plus className="w-4 h-4" />
          <span>Add Column</span>
        </Button>
      </div>

      <div className="flex gap-4 overflow-x-auto pb-6">
        {columns.map((col) => (
          <div key={col.id} className="flex-shrink-0 w-80 bg-surface-900 border border-surface-800 rounded-2xl flex flex-col max-h-[75vh]">
            <div className="flex items-center justify-between p-4 border-b border-surface-800">
              <div className="flex items-center gap-2">
                <span className="text-sm font-semibold text-white">{col.name}</span>
                <span className="px-2 py-0.5 text-xs font-mono bg-surface-800 text-slate-400 rounded-full">
                  {col.cards.length}
                </span>
              </div>
              <button className="p-1 text-slate-400 hover:text-white rounded">
                <MoreHorizontal className="w-4 h-4" />
              </button>
            </div>

            <div className="p-3 space-y-3 flex-1 overflow-y-auto">
              {col.cards.map((card) => (
                <div
                  key={card.id}
                  className="p-4 bg-surface-950/80 border border-surface-800/80 hover:border-surface-700 rounded-xl shadow-sm cursor-grab transition-all space-y-2.5"
                >
                  <div className="flex items-start gap-2">
                    {card.type === 'issue' ? (
                      <CircleDot className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                    ) : (
                      <GitPullRequest className="w-4 h-4 text-purple-400 mt-0.5 flex-shrink-0" />
                    )}
                    <span className="text-sm font-medium text-slate-200 leading-snug">{card.title}</span>
                  </div>

                  <div className="flex items-center justify-between pt-1">
                    <span className="text-xs font-mono text-slate-500">#{card.number}</span>
                    <div className="flex items-center gap-1.5">
                      {card.labels?.map((l) => (
                        <span key={l} className="px-2 py-0.5 text-[10px] font-mono rounded bg-forge-950 border border-forge-800/60 text-forge-300">
                          {l}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="p-3 border-t border-surface-800">
              <button className="w-full flex items-center justify-center gap-1.5 py-2 text-xs font-medium text-slate-400 hover:text-white hover:bg-surface-800 rounded-lg transition-colors">
                <Plus className="w-3.5 h-3.5" />
                <span>Add Item</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
