export interface User {
  id: string;
  username: string;
  email: string;
  displayName: string;
  avatarUrl: string;
  bio?: string;
  company?: string;
  location?: string;
  website?: string;
  role: 'USER' | 'ADMIN';
  createdAt: string;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  displayName: string;
  description?: string;
  avatarUrl: string;
  visibility: 'PUBLIC' | 'PRIVATE';
  createdAt: string;
}

export interface Repository {
  id: string;
  owner: string;
  name: string;
  slug: string;
  description?: string;
  visibility: 'PUBLIC' | 'PRIVATE' | 'INTERNAL';
  defaultBranch: string;
  forkCount: number;
  starCount: number;
  openIssuesCount: number;
  openPrsCount: number;
  createdAt: string;
  updatedAt: string;
}

export interface GitTreeEntry {
  name: string;
  path: string;
  type: 'blob' | 'tree';
  mode: string;
  sha: string;
  size: number;
}

export interface GitBlob {
  name: string;
  path: string;
  sha: string;
  size: number;
  isBinary: boolean;
  content: string | null;
  lineCount: number;
}

export interface GitCommit {
  sha: string;
  shortSha: string;
  authorName: string;
  authorEmail: string;
  message: string;
  timestamp: string;
  additions: number;
  deletions: number;
  changedFilesCount: number;
}

export interface GitDiff {
  oldPath: string;
  newPath: string;
  changeType: string;
  additions: number;
  deletions: number;
  hunks: {
    header: string;
    oldStart: number;
    oldCount: number;
    newStart: number;
    newCount: number;
    lines: {
      type: 'CONTEXT' | 'ADDED' | 'DELETED';
      oldLineNumber?: number;
      newLineNumber?: number;
      content: string;
    }[];
  }[];
}

export interface Issue {
  id: string;
  number: number;
  title: string;
  body: string;
  status: 'OPEN' | 'CLOSED';
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT';
  authorUsername: string;
  authorAvatarUrl: string;
  commentsCount: number;
  createdAt: string;
  updatedAt: string;
  closedAt?: string;
}

export interface PullRequest {
  id: string;
  number: number;
  title: string;
  body: string;
  sourceBranch: string;
  targetBranch: string;
  status: 'OPEN' | 'CLOSED' | 'MERGED';
  draft: boolean;
  mergeable: boolean;
  authorUsername: string;
  authorAvatarUrl: string;
  additions: number;
  deletions: number;
  changedFiles: number;
  createdAt: string;
  updatedAt: string;
  mergedAt?: string;
}

export interface NotificationItem {
  id: string;
  type: string;
  title: string;
  body: string;
  linkUrl: string;
  read: boolean;
  createdAt: string;
}
