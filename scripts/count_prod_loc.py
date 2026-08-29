import os

extensions = {'.java', '.ts', '.tsx', '.sql', '.css', '.html', '.yml', '.yaml', '.json', '.md'}
excludes = {'node_modules', '.git', 'target', 'dist', '.idea', '.vscode', 'scripts', 'test', 'src/test', 'package-lock.json'}

total_lines = 0
file_counts = {}
loc_by_ext = {}

for root, dirs, files in os.walk('.'):
    # Skip test dirs and excluded dirs
    dirs[:] = [d for d in dirs if d not in excludes and not d.startswith('.')]
    if 'test' in root.replace('\\', '/').split('/'):
        continue
    for file in files:
        if file in excludes or file == 'package-lock.json':
            continue
        ext = os.path.splitext(file)[1]
        if ext in extensions:
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
print("      FORGEHUB PROD LOC METRICS (TESTS EXCLUDED)")
print("="*50)
for ext, count in sorted(file_counts.items()):
    print(f"  {ext:<8} : {count:>4} files | {loc_by_ext[ext]:>7} LOC")
print("-" * 50)
print(f"  TOTAL PROD LOC : {total_lines:>7} LOC (Target: 50,000+)")
print("="*50)