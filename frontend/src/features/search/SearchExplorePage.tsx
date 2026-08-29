import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Star, GitFork } from 'lucide-react';
import api from '../../api/client';
import { Repository } from '../../types';

export const SearchExplorePage: React.FC = () => {
  const [repos, setRepos] = useState<Repository[]>([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadPublicRepos();
  }, []);

  const loadPublicRepos = async () => {
    try {
      const res = await api.get('/repositories');
      setRepos(res.data.data.items);
    } catch (e) {
      console.error(e);
    }
  };

  const filtered = repos.filter(
    (r) =>
      r.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 w-full space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Explore Public Repositories</h1>
        <p className="text-xs text-slate-400 mt-1">Discover open source projects, developer tools, and code libraries</p>
      </div>

      <div className="relative max-w-lg">
        <Search className="absolute left-3 top-2.5 w-4 h-4 text-slate-500" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search repositories..."
          className="w-full py-2 pl-9 pr-3 text-sm bg-surface-900 border border-surface-800 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-forge-500"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map((repo) => (
          <div key={repo.id} className="p-5 bg-surface-900 border border-surface-800 rounded-2xl hover:border-surface-700 transition-colors space-y-3">
            <div className="flex items-center justify-between">
              <Link to={`/${repo.owner}/${repo.slug}`} className="text-base font-bold text-forge-400 hover:underline">
                {repo.owner} / {repo.name}
              </Link>
              <span className="px-2 py-0.5 text-[10px] font-mono border border-surface-700 rounded-full text-slate-400">
                {repo.visibility}
              </span>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed line-clamp-2">
              {repo.description || 'No description provided.'}
            </p>

            <div className="flex items-center gap-4 text-xs text-slate-400 font-mono pt-2 border-t border-surface-800/60">
              <span className="flex items-center gap-1"><Star className="w-3.5 h-3.5" /> {repo.starCount}</span>
              <span className="flex items-center gap-1"><GitFork className="w-3.5 h-3.5" /> {repo.forkCount}</span>
              <span>{repo.openIssuesCount} issues</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
