import subprocess
import os

def run_git(args):
    print(f"Running: git {' '.join(args)}")
    res = subprocess.run(["git"] + args, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[Error] git {' '.join(args)} failed:\n{res.stderr}")
        return False
    print(res.stdout.strip())
    return True

def main():
    repo_dir = "/Users/aadityamohansamadhiya/Composio/composio-agent-research"
    os.chdir(repo_dir)
    
    # 1. Initialize repository
    if not os.path.exists(".git"):
        if not run_git(["init"]):
            return
            
    # 2. Configure local user details
    run_git(["config", "user.name", "Aaditya mohan samadhiya"])
    run_git(["config", "user.email", "Aaditya29112005@users.noreply.github.com"])
    
    # Define the 15 commits (file_paths, commit_message)
    commits = [
        (["apps.csv"], "Initial commit: Added SaaS research target configurations"),
        (["research/initialize_data.py"], "feat: Added dataset initialize script for database cache"),
        (["dataset.json"], "data: Generated SaaS profile database (100 apps)"),
        (["research/agent.py"], "feat: Implemented multi-agent research pipeline runner CLI"),
        (["research/verification.py"], "feat: Implemented double-pass verification audit engine"),
        (["research/verification_report.json"], "test: Generated verification hits and misses audit logs"),
        (["research/pattern_analysis.py"], "feat: Implemented statistical pattern clustering analysis"),
        (["research/patterns_report.json"], "data: Generated aggregated stats and blockers report"),
        (["assets/workflow.svg"], "docs: Created horizontal data workflow pipeline SVG"),
        (["assets/architecture.svg"], "docs: Created multi-agent architecture relationship SVG"),
        (["research/generate_html.py"], "feat: Implemented dynamic dashboard compilation engine"),
        (["reports/index.html"], "feat: Compiled zero-dependency interactive dashboard page"),
        (["research/verify_html.py"], "test: Implemented programmatic HTML markup validation script"),
        (["README.md"], "docs: Wrote installation and setup instructions README.md"),
        (["research/git_push_helper.py"], "release: Finalized AI Research Platform production assets")
    ]
    
    # Execute commits step-by-step
    for idx, (files, message) in enumerate(commits):
        print(f"\n--- Making Commit {idx+1}/15 ---")
        for f in files:
            if not run_git(["add", f]):
                print(f"[Warning] Failed to add {f}")
        run_git(["commit", "-m", message])

    # Rename branch to main
    run_git(["branch", "-M", "main"])
    
    # Add remote
    remote_url = "https://github.com/Aaditya29112005/composio.git"
    print(f"\nSetting remote origin to {remote_url}")
    # Remove existing remote if present
    subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
    if run_git(["remote", "add", "origin", remote_url]):
        print("\nPushing to GitHub (origin main)...")
        # Run push
        res = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)
        print(res.stdout)
        if res.returncode != 0:
            print(f"[Error] Push failed:\n{res.stderr}")
            print("\n[NOTE] If push failed due to authentication/permissions, please run:")
            print("  git push -u origin main")
            print("directly in your terminal where your GitHub credentials/SSH keys are loaded.")
        else:
            print("[✓] PUSH COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
