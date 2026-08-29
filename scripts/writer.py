import base64, os, sys

def write_b64(path, b64_str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    content = base64.b64decode(b64_str).decode('utf-8')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    lines = len(content.splitlines())
    print(f'Wrote: {path} ({lines} lines)')

if __name__ == '__main__':
    if len(sys.argv) == 3:
        write_b64(sys.argv[1], sys.argv[2])
