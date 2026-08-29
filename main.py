#!/usr/bin/env python3
import sys
import subprocess
import os

def main():
    print("==========================================================")
    print("   ForgeHub - Enterprise Developer Collaboration Platform  ")
    print("==========================================================")
    print("Commands:")
    print("  python main.py start       - Start platform using Docker Compose")
    print("  python main.py stop        - Stop running platform containers")
    print("  python main.py build       - Build full stack (Backend & Frontend)")
    print("  python main.py test        - Run test verification suite")
    print("  python main.py status      - Inspect platform health status")
    print("==========================================================")

    if len(sys.argv) < 2 or sys.argv[1] == "start":
        print("[*] Starting ForgeHub via docker-compose...")
        subprocess.run("docker-compose up -d", shell=True)
    elif sys.argv[1] == "stop":
        subprocess.run("docker-compose down", shell=True)
    elif sys.argv[1] == "build":
        subprocess.run("npm --prefix frontend run build", shell=True)
    elif sys.argv[1] == "status":
        subprocess.run("docker-compose ps", shell=True)

if __name__ == "__main__":
    main()
