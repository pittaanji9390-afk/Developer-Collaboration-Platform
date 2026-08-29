import os

def write_file(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    lines = len(content.strip().splitlines())
    print(f"Created: {path} ({lines} lines)")

if __name__ == "__main__":
    write_file(".gitignore", "target/\nnode_modules/\ndist/\ndata/\n*.class\n*.log\n.DS_Store\nThumbs.db\n.idea/\n*.iml\n.vscode/\n.env\n.env.local\n")
    write_file(".env.example", "SERVER_PORT=8080\nSPRING_PROFILES_ACTIVE=dev\nDB_HOST=localhost\nDB_PORT=5432\nDB_NAME=forgehub\nDB_USER=forgehub\nDB_PASSWORD=forgehub_secure_pass\nREDIS_HOST=localhost\nREDIS_PORT=6379\nREDIS_PASSWORD=\nVAULT_KEY=635266556A586E3272357538782F413F4428472B4B6250645367566B5970404E\nGIT_STORAGE_ROOT=./data/git-repositories\nUPLOADS_STORAGE_ROOT=./data/uploads\nCI_WORKSPACE_ROOT=./data/ci-workspaces\n")
    print("common_writer verified!")