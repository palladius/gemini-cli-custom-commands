#!/usr/bin/env python3
"""
# Conductor++ Worktree Git Status Helper (v2.0)
#
# USER MANUAL:
# This script aggregates the git status and Conductor++ metadata across all
# active git worktrees located under `.worktrees/`.
#
# How to run:
#   python3 git_status_patched.py
#
# Requirements:
#   - Python 3.x
#   - Must be executed inside a Git repository.
#
# What it does:
#   1. Resolves all active git worktrees via `git worktree list --porcelain`.
#   2. Scans the central `conductor/tracks/` folder for track metadata.
#   3. Correlates each worktree to its track metadata.
#   4. Checks for uncommitted changes in each worktree using `git status --porcelain`.
#   5. Outputs an aggregated, color-coded summary indicating status, agent, branch,
#      uncommitted files, and active questions.
"""

import os
import sys
import json
import subprocess
import re

# Terminal colors for premium UI
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

def print_bold(text, color=RESET):
    print(f"{BOLD}{color}{text}{RESET}")

def find_repo_root():
    try:
        res = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError:
        curr = os.getcwd()
        while curr != os.path.dirname(curr):
            if os.path.isdir(os.path.join(curr, ".git")):
                return curr
            curr = os.path.dirname(curr)
        return None

def get_git_worktrees(repo_root):
    worktrees = []
    try:
        res = subprocess.run(["git", "worktree", "list", "--porcelain"], cwd=repo_root, capture_output=True, text=True, check=True)
        current_wt = {}
        for line in res.stdout.splitlines():
            line = line.strip()
            if not line:
                if current_wt:
                    worktrees.append(current_wt)
                    current_wt = {}
                continue
            parts = line.split(" ", 1)
            key = parts[0]
            val = parts[1] if len(parts) > 1 else ""
            if key == "worktree":
                current_wt["path"] = val
            elif key == "branch":
                current_wt["branch"] = val.replace("refs/heads/", "")
            elif key == "HEAD":
                current_wt["head"] = val
        if current_wt:
            worktrees.append(current_wt)
    except Exception as e:
        print(f"{RED}Error listing git worktrees: {e}{RESET}")
    return worktrees

def get_git_status(wt_path):
    try:
        res = subprocess.run(["git", "status", "--porcelain"], cwd=wt_path, capture_output=True, text=True, check=True)
        lines = [l.strip() for l in res.stdout.splitlines() if l.strip()]
        if not lines:
            return False, "Clean", []
        
        modified = 0
        added = 0
        deleted = 0
        untracked = 0
        other = 0
        
        for line in lines:
            status = line[:2]
            if "M" in status:
                modified += 1
            elif "A" in status:
                added += 1
            elif "D" in status:
                deleted += 1
            elif "??" in status:
                untracked += 1
            else:
                other += 1
                
        parts = []
        if added: parts.append(f"+{added}")
        if modified: parts.append(f"~{modified}")
        if deleted: parts.append(f"-{deleted}")
        if untracked: parts.append(f"?{untracked}")
        if other: parts.append(f"o{other}")
        
        summary = ", ".join(parts)
        return True, summary, lines
    except Exception as e:
        return False, f"Error: {e}", []

def load_track_metadata(repo_root):
    tracks_metadata = []
    conductor_dir = os.path.join(repo_root, "conductor")
    tracks_dir = os.path.join(conductor_dir, "tracks")
    if not os.path.isdir(tracks_dir):
        return []
        
    try:
        for track_id in os.listdir(tracks_dir):
            track_path = os.path.join(tracks_dir, track_id)
            if not os.path.isdir(track_path):
                continue
            metadata_path = os.path.join(track_path, "metadata.json")
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, "r") as f:
                        meta = json.load(f)
                        meta["_track_id"] = track_id
                        meta["_metadata_path"] = metadata_path
                        tracks_metadata.append(meta)
                except Exception:
                    pass
    except Exception:
        pass
    return tracks_metadata

def find_matching_track(wt_path, wt_branch, tracks_meta):
    abs_wt_path = os.path.abspath(wt_path)
    wt_dir_name = os.path.basename(abs_wt_path)
    
    # 1. Match by explicit path/directory
    for meta in tracks_meta:
        wt_cfg = meta.get("worktree", {})
        cfg_dir = wt_cfg.get("directory") or wt_cfg.get("path")
        if cfg_dir:
            if not os.path.isabs(cfg_dir):
                repo_root = find_repo_root()
                if not repo_root and "_metadata_path" in meta:
                    p = os.path.abspath(meta["_metadata_path"])
                    for _ in range(4):
                        p = os.path.dirname(p)
                    repo_root = p
                if repo_root:
                    cfg_dir = os.path.join(repo_root, cfg_dir)
            if os.path.abspath(cfg_dir) == abs_wt_path:
                return meta
                
    # 2. Match by branch name
    for meta in tracks_meta:
        wt_cfg = meta.get("worktree", {})
        if wt_cfg.get("branch") == wt_branch:
            return meta
            
    # 3. Match by track_id substring in worktree directory name
    for meta in tracks_meta:
        track_id = meta.get("_track_id")
        if track_id and track_id in wt_dir_name:
            return meta
            
    # 4. Match by github issue number in worktree directory name
    for meta in tracks_meta:
        issue_cfg = meta.get("github_issue", {})
        issue_num = issue_cfg.get("number")
        if issue_num and f"issue-{issue_num}" in wt_dir_name:
            return meta
            
    return None

def main():
    repo_root = find_repo_root()
    if not repo_root:
        print(f"{RED}Error: Not in a git repository.{RESET}")
        sys.exit(1)
        
    print_bold("🌳 Conductor++ Worktree Git Status Patched Helper (v2.0)", CYAN)
    print(f"Repository Root: {repo_root}\n")
    
    worktrees = get_git_worktrees(repo_root)
    sub_worktrees = [w for w in worktrees if ".worktrees" in w.get("path", "")]
    
    if not sub_worktrees:
        print(f"{YELLOW}No active sub-worktrees detected in .worktrees/.{RESET}")
        sys.exit(0)
        
    tracks_meta = load_track_metadata(repo_root)
    
    # Header
    print_bold(f"{'WORKTREE FOLDER':<30} | {'BRANCH':<20} | {'AGENT':<12} | {'GIT STATUS':<15} | {'TRACK STATUS':<12} | {'BLOCKED':^7}", BOLD)
    print("=" * 110)
    
    for wt in sub_worktrees:
        wt_path = wt["path"]
        wt_branch = wt.get("branch", "unknown")
        wt_folder = os.path.basename(wt_path)
        
        is_dirty, git_status_summary, git_details = get_git_status(wt_path)
        meta = find_matching_track(wt_path, wt_branch, tracks_meta)
        
        agent = "unknown"
        track_status = "UNKNOWN"
        is_blocked = "No"
        current_task = ""
        awaiting_questions = []
        
        if meta:
            agent = meta.get("agent") or meta.get("assignee") or "unknown"
            track_status = meta.get("status", "unknown").upper()
            
            active_qs = meta.get("active_questions", [])
            awaiting_questions = [q for q in active_qs if q.get("status") == "awaiting_human"]
            
            if meta.get("blocked") or track_status == "BLOCKED" or awaiting_questions:
                is_blocked = f"{RED}{BOLD}YES{RESET}"
            else:
                is_blocked = "No"
                
            tasks = meta.get("tasks", [])
            in_progress_tasks = [t for t in tasks if t.get("status") in ("in_progress", "active", "IN_PROGRESS", "ACTIVE")]
            if in_progress_tasks:
                current_task = in_progress_tasks[0].get("name") or in_progress_tasks[0].get("description") or ""
            elif tasks:
                open_tasks = [t for t in tasks if t.get("status") not in ("completed", "done", "COMPLETED", "DONE", "RESOLVED")]
                if open_tasks:
                    current_task = open_tasks[0].get("name") or open_tasks[0].get("description") or ""
        else:
            parts = wt_folder.split("-")
            if len(parts) >= 3:
                agent = parts[-1]
                
        status_color = GREEN
        if "Error" in git_status_summary:
            status_color = RED
        elif is_dirty:
            status_color = CYAN
            
        track_status_color = RESET
        if track_status == "ACTIVE" or track_status == "IN_PROGRESS":
            track_status_color = GREEN
        elif track_status == "BLOCKED":
            track_status_color = RED
        elif track_status in ("COMPLETED", "DONE", "RESOLVED"):
            track_status_color = MAGENTA
            
        wt_folder_truncated = wt_folder[:28] + ".." if len(wt_folder) > 30 else wt_folder
        wt_branch_truncated = wt_branch[:18] + ".." if len(wt_branch) > 20 else wt_branch
        agent_truncated = agent[:12]
        
        print(f"{wt_folder_truncated:<30} | "
              f"{wt_branch_truncated:<20} | "
              f"{agent_truncated:<12} | "
              f"{status_color}{git_status_summary:<15}{RESET} | "
              f"{track_status_color}{track_status:<12}{RESET} | "
              f"{is_blocked:^7}")
        
        indent = "   "
        if awaiting_questions:
            print(f"{indent}{YELLOW}⚠️  Awaiting Human Input ({len(awaiting_questions)} questions):{RESET}")
            for i, q in enumerate(awaiting_questions, 1):
                q_text = q.get("question", "No question text")
                q_agent = q.get("agent", agent)
                print(f"{indent}   {i}. [{q_agent}]: {q_text}")
                
        if current_task:
            print(f"{indent}📌 Current Task: {current_task}")
            
        if is_dirty and git_details:
            print(f"{indent}📂 Uncommitted Changes:")
            for detail in git_details[:5]:
                print(f"{indent}   {detail}")
            if len(git_details) > 5:
                print(f"{indent}   ... and {len(git_details) - 5} more files.")
        print()

if __name__ == "__main__":
    main()
