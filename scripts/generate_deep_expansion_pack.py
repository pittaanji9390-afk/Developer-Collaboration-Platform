from common_writer import write_file

# ==============================================================================
# 1. GRAPHQL SCHEMA & RESOLVERS
# ==============================================================================
gql_schema = """type Query {
  repository(owner: String!, slug: String!): Repository
  repositories(visibility: String, page: Int, size: Int): RepositoryConnection!
  viewer: User
  user(username: String!): User
  organization(slug: String!): Organization
  search(query: String!, type: SearchType, page: Int, size: Int): SearchResultConnection!
}

type Mutation {
  createRepository(input: CreateRepositoryInput!): Repository!
  createIssue(repositoryId: ID!, input: CreateIssueInput!): Issue!
  createPullRequest(repositoryId: ID!, input: CreatePullRequestInput!): PullRequest!
  mergePullRequest(repositoryId: ID!, number: Int!, strategy: MergeStrategy!): PullRequest!
  addIssueComment(issueId: ID!, body: String!): IssueComment!
  createDiscussion(repositoryId: ID!, input: CreateDiscussionInput!): Discussion!
}

enum SearchType {
  REPOSITORY
  ISSUE
  PULL_REQUEST
  USER
  ORGANIZATION
}

enum MergeStrategy {
  MERGE_COMMIT
  SQUASH
  REBASE
}

input CreateRepositoryInput {
  name: String!
  slug: String!
  description: String
  visibility: String
  organizationSlug: String
}

input CreateIssueInput {
  title: String!
  body: String
  priority: String
}

input CreatePullRequestInput {
  title: String!
  body: String
  sourceBranch: String!
  targetBranch: String!
  draft: Boolean
}

input CreateDiscussionInput {
  categoryId: ID!
  title: String!
  body: String!
}

type Repository {
  id: ID!
  name: String!
  slug: String!
  description: String
  visibility: String!
  defaultBranch: String!
  forkCount: Int!
  starCount: Int!
  openIssuesCount: Int!
  openPrsCount: Int!
  createdAt: String!
  updatedAt: String!
}

type RepositoryConnection {
  items: [Repository!]!
  totalElements: Int!
  totalPages: Int!
  pageNumber: Int!
}

type User {
  id: ID!
  username: String!
  email: String!
  displayName: String
  avatarUrl: String
  bio: String
  company: String
  location: String
  website: String
  role: String!
  createdAt: String!
}

type Organization {
  id: ID!
  name: String!
  slug: String!
  displayName: String
  description: String
  avatarUrl: String
  visibility: String!
  createdAt: String!
}

type Issue {
  id: ID!
  number: Int!
  title: String!
  body: String
  status: String!
  priority: String!
  authorUsername: String!
  authorAvatarUrl: String
  commentsCount: Int!
  createdAt: String!
  updatedAt: String!
}

type IssueComment {
  id: ID!
  authorUsername: String!
  authorAvatarUrl: String
  body: String!
  createdAt: String!
}

type PullRequest {
  id: ID!
  number: Int!
  title: String!
  body: String
  sourceBranch: String!
  targetBranch: String!
  status: String!
  draft: Boolean!
  mergeable: Boolean!
  authorUsername: String!
  additions: Int!
  deletions: Int!
  createdAt: String!
}

type Discussion {
  id: ID!
  number: Int!
  title: String!
  body: String!
  categoryName: String!
  categoryEmoji: String
  authorUsername: String!
  commentsCount: Int!
  upvotesCount: Int!
  createdAt: String!
}

type SearchResultConnection {
  totalResults: Int!
  items: [SearchResultItem!]!
}

type SearchResultItem {
  entityType: String!
  entityId: String!
  title: String!
  snippet: String
}
"""
write_file("backend/src/main/resources/graphql/schema.graphqls", gql_schema)

print("gen_graphql complete.")