import os

code_extensions = {'.java', '.ts', '.tsx', '.py', '.sql'}
excludes = {'node_modules', '.git', 'target', 'dist', '.idea', '.vscode', 'test', 'src/test'}

total_lines = 0
file_counts = {}
loc_by_ext = {}

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in excludes and not d.startswith('.')]
    if 'test' in root.replace('\\', '/').split('/'):
        continue
    for file in files:
        ext = os.path.splitext(file)[1]
        if ext in code_extensions:
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = sum(1 for line in f if line.strip())
                    total_lines += lines
                    loc_by_ext[ext] = loc_by_ext.get(ext, 0) + lines
                    file_counts[ext] = file_counts.get(ext, 0) + 1
            except Exception:
                pass

print("="*50)
print("      FORGEHUB PURE SOURCE CODE METRICS")
print("="*50)
for ext, count in sorted(file_counts.items()):
    print(f"  {ext:<8} : {count:>4} files | {loc_by_ext[ext]:>7} LOC")
print("-" * 50)
print(f"  TOTAL PURE CODE LOC : {total_lines:>7} LOC (Target: 52,000+)")
print("="*50)