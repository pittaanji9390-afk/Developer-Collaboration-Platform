#!/usr/bin/env python3
"""
ForgeHub Enterprise Command Line Interface (CLI)
"""
import sys
import os

from commands.auth_cmd import AuthCommand
from commands.repo_cmd import RepoCommand
from commands.pr_cmd import PrCommand
from commands.issue_cmd import IssueCommand
from commands.workflow_cmd import WorkflowCommand
from commands.runner_cmd import RunnerCommand
from commands.secret_cmd import SecretCommand
from commands.org_cmd import OrgCommand
from commands.audit_cmd import AuditCommand
from commands.security_cmd import SecurityCommand
from commands.discussion_cmd import DiscussionCommand
from commands.project_cmd import ProjectCommand
from commands.config_cmd import ConfigCommand

COMMANDS = {
    "auth": AuthCommand,
    "repo": RepoCommand,
    "pr": PrCommand,
    "issue": IssueCommand,
    "workflow": WorkflowCommand,
    "runner": RunnerCommand,
    "secret": SecretCommand,
    "org": OrgCommand,
    "audit": AuditCommand,
    "security": SecurityCommand,
    "discussion": DiscussionCommand,
    "project": ProjectCommand,
    "config": ConfigCommand
}

def print_banner():
    print("================================================================")
    print("    ForgeHub Developer Collaboration Platform - Enterprise CLI   ")
    print("================================================================")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print_banner()
        print("Usage: forgehub <command> <action> [options]")
        print("\nAvailable commands:")
        for cmd_name in sorted(COMMANDS.keys()):
            print(f"  {cmd_name:<14} - Manage {cmd_name} resources")
        print("\nExample: forgehub repo list")
        print("         forgehub pr create --title 'Fix bug' --branch feature/patch")
        return 0

    cmd_name = sys.argv[1].lower()
    if cmd_name not in COMMANDS:
        print(f"Error: Unknown command '{cmd_name}'. Run 'forgehub --help' for usage.")
        return 1

    handler_cls = COMMANDS[cmd_name]
    handler = handler_cls()
    action = sys.argv[2] if len(sys.argv) > 2 else "list"
    return handler.execute(action, *sys.argv[3:])

if __name__ == "__main__":
    sys.exit(main())
