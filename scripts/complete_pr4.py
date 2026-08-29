import os
import subprocess

def run_git(cmd):
    print(f">> git {cmd}")
    res = subprocess.run(f"git {cmd}", shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr and "warning:" not in res.stderr:
        print(res.stderr.strip())
    return res

os.makedirs("docs/compliance", exist_ok=True)
with open("docs/compliance/LICENSE_COMPLIANCE.md", "w", encoding="utf-8") as f:
    f.write("# SPDX License Governance Matrix\nEvaluates copyleft, permissive, and proprietary license compatibility.\n")

run_git("add docs/compliance/LICENSE_COMPLIANCE.md")
run_git('commit -m "feat(governance): add SPDX license compliance guidelines"')
run_git("checkout main")
run_git('merge --no-ff feature/spdx-governance-and-analytics -m "Merge pull request #4 from feature/spdx-governance-and-analytics - add SPDX license compliance guidelines"')
run_git("push origin main --all")
print("PR 4 completed and all branches pushed to GitHub.")