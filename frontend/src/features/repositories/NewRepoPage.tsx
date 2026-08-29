import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Globe, Lock } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import api from '../../api/client';

export const NewRepoPage: React.FC = () => {
  const [name, setName] = useState('');
  const [slug, setSlug] = useState('');
  const [description, setDescription] = useState('');
  const [visibility, setVisibility] = useState<'PUBLIC' | 'PRIVATE'>('PUBLIC');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleNameChange = (val: string) => {
    setName(val);
    setSlug(val.toLowerCase().replace(/[^a-z0-9_-]/g, '-'));
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const res = await api.post('/repositories', {
        name,
        slug,
        description,
        visibility,
      });
      const repo = res.data.data;
      navigate(`/${repo.owner}/${repo.slug}`);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-10 w-full">
      <div className="pb-6 border-b border-surface-800 mb-6">
        <h1 className="text-2xl font-bold text-white">Create a new repository</h1>
        <p className="text-xs text-slate-400 mt-1">
          A repository contains all project files, including the revision history.
        </p>
      </div>

      <form onSubmit={handleCreate} className="space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block mb-1.5 text-xs font-medium text-slate-300">Repository Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => handleNameChange(e.target.value)}
              required
              placeholder="my-awesome-app"
              className="w-full py-2 px-3 text-sm bg-surface-900 border border-surface-800 rounded-lg text-white focus:outline-none focus:border-forge-500"
            />
          </div>

          <div>
            <label className="block mb-1.5 text-xs font-medium text-slate-300">URL Slug</label>
            <input
              type="text"
              value={slug}
              onChange={(e) => setSlug(e.target.value)}
              required
              className="w-full py-2 px-3 text-sm bg-surface-950 border border-surface-800 rounded-lg text-slate-400 font-mono focus:outline-none"
            />
          </div>
        </div>

        <div>
          <label className="block mb-1.5 text-xs font-medium text-slate-300">Description (optional)</label>
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Short description of your project"
            className="w-full py-2 px-3 text-sm bg-surface-900 border border-surface-800 rounded-lg text-white focus:outline-none focus:border-forge-500"
          />
        </div>

        <div className="space-y-3 pt-4 border-t border-surface-800">
          <label className="block text-xs font-medium text-slate-300">Visibility</label>

          <div
            onClick={() => setVisibility('PUBLIC')}
            className={`p-4 rounded-xl border cursor-pointer flex items-start gap-3 transition-colors ${
              visibility === 'PUBLIC' ? 'bg-surface-900 border-forge-500' : 'bg-surface-950 border-surface-800 hover:bg-surface-900/50'
            }`}
          >
            <Globe className="w-5 h-5 text-forge-400 mt-0.5" />
            <div>
              <div className="text-sm font-semibold text-white">Public</div>
              <div className="text-xs text-slate-400">Anyone on the internet can see this repository.</div>
            </div>
          </div>

          <div
            onClick={() => setVisibility('PRIVATE')}
            className={`p-4 rounded-xl border cursor-pointer flex items-start gap-3 transition-colors ${
              visibility === 'PRIVATE' ? 'bg-surface-900 border-forge-500' : 'bg-surface-950 border-surface-800 hover:bg-surface-900/50'
            }`}
          >
            <Lock className="w-5 h-5 text-amber-400 mt-0.5" />
            <div>
              <div className="text-sm font-semibold text-white">Private</div>
              <div className="text-xs text-slate-400">You choose who can see and commit to this repository.</div>
            </div>
          </div>
        </div>

        <div className="pt-6 border-t border-surface-800">
          <Button type="submit" isLoading={isLoading} className="px-6">
            Create Repository
          </Button>
        </div>
      </form>
    </div>
  );
};
