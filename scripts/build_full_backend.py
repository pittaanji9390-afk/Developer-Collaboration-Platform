# ForgeHub Backend Generator Script
import os, sys

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    lines = len(content.strip().splitlines())
    print(f'Wrote: {path} ({lines} lines)')

print('build_full_backend.py initialized')
