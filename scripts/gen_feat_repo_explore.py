from common_writer import write_file

# 1. NEW REPO PAGE
new_repo = """import React, { useState } from 'react';
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
    <div className=\"max-w-3xl mx-auto px-4 py-10 w-full\">
      <div className=\"pb-6 border-b border-surface-800 mb-6\">
        <h1 className=\"text-2xl font-bold text-white\">Create a new repository</h1>
        <p className=\"text-xs text-slate-400 mt-1\">
          A repository contains all project files, including the revision history.
        </p>
      </div>

      <form onSubmit={handleCreate} className=\"space-y-6\">
        <div className=\"grid grid-cols-1 sm:grid-cols-2 gap-4\">
          <div>
            <label className=\"block mb-1.5 text-xs font-medium text-slate-300\">Repository Name</label>
            <input
              type=\"text\"
              value={name}
              onChange={(e) => handleNameChange(e.target.value)}
              required
              placeholder=\"my-awesome-app\"
              className=\"w-full py-2 px-3 text-sm bg-surface-900 border border-surface-800 rounded-lg text-white focus:outline-none focus:border-forge-500\"
            />
          </div>

          <div>
            <label className=\"block mb-1.5 text-xs font-medium text-slate-300\">URL Slug</label>
            <input
              type=\"text\"
              value={slug}
              onChange={(e) => setSlug(e.target.value)}
              required
              className=\"w-full py-2 px-3 text-sm bg-surface-950 border border-surface-800 rounded-lg text-slate-400 font-mono focus:outline-none\"
            />
          </div>
        </div>

        <div>
          <label className=\"block mb-1.5 text-xs font-medium text-slate-300\">Description (optional)</label>
          <input
            type=\"text\"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder=\"Short description of your project\"
            className=\"w-full py-2 px-3 text-sm bg-surface-900 border border-surface-800 rounded-lg text-white focus:outline-none focus:border-forge-500\"
          />
        </div>

        <div className=\"space-y-3 pt-4 border-t border-surface-800\">
          <label className=\"block text-xs font-medium text-slate-300\">Visibility</label>

          <div
            onClick={() => setVisibility('PUBLIC')}
            className={`p-4 rounded-xl border cursor-pointer flex items-start gap-3 transition-colors ${
              visibility === 'PUBLIC' ? 'bg-surface-900 border-forge-500' : 'bg-surface-950 border-surface-800 hover:bg-surface-900/50'
            }`}
          >
            <Globe className=\"w-5 h-5 text-forge-400 mt-0.5\" />
            <div>
              <div className=\"text-sm font-semibold text-white\">Public</div>
              <div className=\"text-xs text-slate-400\">Anyone on the internet can see this repository.</div>
            </div>
          </div>

          <div
            onClick={() => setVisibility('PRIVATE')}
            className={`p-4 rounded-xl border cursor-pointer flex items-start gap-3 transition-colors ${
              visibility === 'PRIVATE' ? 'bg-surface-900 border-forge-500' : 'bg-surface-950 border-surface-800 hover:bg-surface-900/50'
            }`}
          >
            <Lock className=\"w-5 h-5 text-amber-400 mt-0.5\" />
            <div>
              <div className=\"text-sm font-semibold text-white\">Private</div>
              <div className=\"text-xs text-slate-400\">You choose who can see and commit to this repository.</div>
            </div>
          </div>
        </div>

        <div className=\"pt-6 border-t border-surface-800\">
          <Button type=\"submit\" isLoading={isLoading} className=\"px-6\">
            Create Repository
          </Button>
        </div>
      </form>
    </div>
  );
};
"""
write_file("frontend/src/features/repositories/NewRepoPage.tsx", new_repo)

# 2. SEARCH & EXPLORE PAGE
search_page = """import React, { useState, useEffect } from 'react';
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
    <div className=\"max-w-7xl mx-auto px-4 py-8 w-full space-y-6\">
      <div>
        <h1 className=\"text-2xl font-bold text-white\">Explore Public Repositories</h1>
        <p className=\"text-xs text-slate-400 mt-1\">Discover open source projects, developer tools, and code libraries</p>
      </div>

      <div className=\"relative max-w-lg\">
        <Search className=\"absolute left-3 top-2.5 w-4 h-4 text-slate-500\" />
        <input
          type=\"text\"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder=\"Search repositories...\"
          className=\"w-full py-2 pl-9 pr-3 text-sm bg-surface-900 border border-surface-800 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-forge-500\"
        />
      </div>

      <div className=\"grid grid-cols-1 md:grid-cols-2 gap-4\">
        {filtered.map((repo) => (
          <div key={repo.id} className=\"p-5 bg-surface-900 border border-surface-800 rounded-2xl hover:border-surface-700 transition-colors space-y-3\">
            <div className=\"flex items-center justify-between\">
              <Link to={`/${repo.owner}/${repo.slug}`} className=\"text-base font-bold text-forge-400 hover:underline\">
                {repo.owner} / {repo.name}
              </Link>
              <span className=\"px-2 py-0.5 text-[10px] font-mono border border-surface-700 rounded-full text-slate-400\">
                {repo.visibility}
              </span>
            </div>

            <p className=\"text-xs text-slate-300 leading-relaxed line-clamp-2\">
              {repo.description || 'No description provided.'}
            </p>

            <div className=\"flex items-center gap-4 text-xs text-slate-400 font-mono pt-2 border-t border-surface-800/60\">
              <span className=\"flex items-center gap-1\"><Star className=\"w-3.5 h-3.5\" /> {repo.starCount}</span>
              <span className=\"flex items-center gap-1\"><GitFork className=\"w-3.5 h-3.5\" /> {repo.forkCount}</span>
              <span>{repo.openIssuesCount} issues</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
"""
write_file("frontend/src/features/search/SearchExplorePage.tsx", search_page)

# 3. BACKEND DATA INITIALIZER
data_init = """package com.forgehub.config;

import com.forgehub.git.JGitService;
import com.forgehub.identity.User;
import com.forgehub.identity.UserRepository;
import com.forgehub.identity.UserRole;
import com.forgehub.identity.UserStatus;
import com.forgehub.issues.Issue;
import com.forgehub.issues.IssueRepository;
import com.forgehub.organizations.Organization;
import com.forgehub.organizations.OrganizationMember;
import com.forgehub.organizations.OrganizationMemberRepository;
import com.forgehub.organizations.OrganizationRepository;
import com.forgehub.pullrequests.PullRequest;
import com.forgehub.pullrequests.PullRequestRepository;
import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.repositories.RepositoryRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.security.crypto.password.PasswordEncoder;

@Slf4j
@Configuration
@Profile({"dev", "prod"})
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {

    private final UserRepository userRepository;
    private final OrganizationRepository orgRepository;
    private final OrganizationMemberRepository memberRepository;
    private final RepositoryRepository repoRepository;
    private final IssueRepository issueRepository;
    private final PullRequestRepository prRepository;
    private final PasswordEncoder passwordEncoder;
    private final JGitService gitService;

    @Override
    public void run(String... args) {
        if (userRepository.count() > 0) {
            return;
        }

        log.info("Initializing ForgeHub initial seed data...");

        User alice = userRepository.save(User.builder()
                .username("alice")
                .email("alice@forgehub.dev")
                .displayName("Alice Chen")
                .passwordHash(passwordEncoder.encode("Password123!"))
                .role(UserRole.ADMIN)
                .status(UserStatus.ACTIVE)
                .avatarUrl("https://api.dicebear.com/7.x/identicon/svg?seed=alice")
                .build());

        User bob = userRepository.save(User.builder()
                .username("bob")
                .email("bob@forgehub.dev")
                .displayName("Bob Smith")
                .passwordHash(passwordEncoder.encode("Password123!"))
                .role(UserRole.USER)
                .status(UserStatus.ACTIVE)
                .avatarUrl("https://api.dicebear.com/7.x/identicon/svg?seed=bob")
                .build());

        Organization org = orgRepository.save(Organization.builder()
                .name("ForgeHub Core")
                .slug("forgehub")
                .displayName("ForgeHub Engineering")
                .description("Core platform maintainers and systems engineering team.")
                .avatarUrl("https://api.dicebear.com/7.x/identicon/svg?seed=forgehub")
                .build());

        memberRepository.save(OrganizationMember.builder()
                .organization(org)
                .user(alice)
                .role(OrganizationMember.OrgRole.OWNER)
                .build());

        String repoPath = "forgehub/developer-collaboration-platform.git";
        RepositoryEntity repo = repoRepository.save(RepositoryEntity.builder()
                .organization(org)
                .name("Developer Collaboration Platform")
                .slug("developer-collaboration-platform")
                .description("Production-ready developer collaboration platform with JGit bare storage, CI/CD DAGs, and RBAC.")
                .visibility(RepositoryEntity.RepoVisibility.PUBLIC)
                .defaultBranch("main")
                .repositoryPath(repoPath)
                .starCount(42)
                .forkCount(8)
                .openIssuesCount(1)
                .openPrsCount(1)
                .build());

        gitService.initBareRepository(repoPath, "main");

        issueRepository.save(Issue.builder()
                .repository(repo)
                .author(bob)
                .number(1)
                .title("Support fine-grained personal access tokens (PAT) with expiration")
                .body("Developers should be able to create scoped access tokens for automated CLI and CI usage.")
                .status(Issue.IssueStatus.OPEN)
                .priority(Issue.IssuePriority.HIGH)
                .build());

        prRepository.save(PullRequest.builder()
                .repository(repo)
                .author(alice)
                .number(2)
                .title("Feature: JGit bare repository tree streaming and split diff calculation")
                .body("Implements low-level object parsing with JGit RevWalk and TreeWalk for high performance.")
                .sourceBranch("feature/jgit-streaming")
                .targetBranch("main")
                .status(PullRequest.PRStatus.OPEN)
                .additionsCount(14)
                .deletionsCount(2)
                .build());

        log.info("ForgeHub seed data initialization completed successfully.");
    }
}
"""
write_file("backend/src/main/java/com/forgehub/config/DataInitializer.java", data_init)

print("gen_feat_repo_explore complete.")