import zipfile

with zipfile.ZipFile("ForgeHub-Developer-Collaboration-Platform.zip", "r") as z:
    names = z.namelist()
    has_git = any(n.startswith(".git/") or n.startswith(".git\\") for n in names)
    has_backend = any(n.startswith("backend/") for n in names)
    has_frontend = any(n.startswith("frontend/") for n in names)
    print("="*50)
    print("       EVALUATOR ZIP INTEGRITY REPORT")
    print("="*50)
    print(f"  Total Archived Files : {len(names)}")
    print(f"  Contains .git folder : {has_git}")
    print(f"  Contains backend     : {has_backend}")
    print(f"  Contains frontend    : {has_frontend}")
    print("="*50)