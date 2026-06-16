#!/usr/bin/env python3
import os
import sys
import json
import re
from datetime import datetime

def parse_datetime(dt_str):
    if not dt_str:
        return None
    dt_str = str(dt_str).strip()
    if dt_str.endswith("Z"):
        dt_str = dt_str[:-1] + "+00:00"
    try:
        from datetime import timezone
        dt = datetime.fromisoformat(dt_str)
        if dt.tzinfo is not None:
            dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt
    except Exception:
        try:
            match = re.match(r"^(\d{4})[^\d]?(\d{2})[^\d]?(\d{2})[T\s]?(\d{2})?[^\d]?(\d{2})?[^\d]?(\d{2})?", dt_str)
            if match:
                parts = [int(p) for p in match.groups() if p is not None]
                while len(parts) < 6:
                    parts.append(0)
                return datetime(*parts)
        except Exception:
            pass
    return None

def get_github_issue_timestamps(repo_path):
    import subprocess
    cmd = ["gh", "issue", "list", "--state", "all", "--json", "number,updatedAt", "--limit", "100"]
    try:
        result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return {item["number"]: item["updatedAt"] for item in data if "number" in item and "updatedAt" in item}
    except Exception:
        return {}

# Terminal Colors
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
RESET = "\033[0m"

def print_bold(text, color=""):
    print(f"{BOLD}{color}{text}{RESET}")

def make_progress_bar(pct, width=10):
    filled_chars = int(round((pct / 100.0) * width))
    empty_chars = width - filled_chars
    return "█" * filled_chars + "░" * empty_chars

def parse_plan_tasks(plan_path):
    """Parses plan.md to count total, completed, in-progress, and pending tasks."""
    if not os.path.exists(plan_path):
        return None
    
    total = 0
    completed = 0
    in_progress = 0
    pending = 0
    
    # Matches list checkboxes: - [ ] Task, - [x] Task, - [~] Task
    checkbox_pattern = re.compile(r"^\s*-\s+\[([ x~])\]")
    
    try:
        with open(plan_path, "r", encoding="utf-8") as f:
            for line in f:
                match = checkbox_pattern.match(line)
                if match:
                    total += 1
                    status_char = match.group(1)
                    if status_char == "x":
                        completed += 1
                    elif status_char == "~":
                        in_progress += 1
                    else:
                        pending += 1
    except Exception:
        return None
        
    return {
        "total": total,
        "completed": completed,
        "in_progress": in_progress,
        "pending": pending
    }

def inspect_repository(repo_path, show_all=True, short_mode=False):
    repo_path = os.path.abspath(repo_path)
    conductor_dir = os.path.join(repo_path, "conductor")
    gh_timestamps = get_github_issue_timestamps(repo_path)
    
    # Scan .worktrees/ directory to match active worktrees and agent names
    worktrees_by_ghi = {}
    worktrees_by_slug = {}
    worktrees_path = os.path.join(repo_path, ".worktrees")
    if os.path.isdir(worktrees_path):
        try:
            for item in os.listdir(worktrees_path):
                item_path = os.path.join(worktrees_path, item)
                if os.path.isdir(item_path):
                    match = re.match(r"^issue-(.+)-([^-]+)$", item)
                    if match:
                        issue_id = match.group(1)
                        agent_name = match.group(2)
                        val = {"dir": item, "agent": agent_name}
                        if issue_id.isdigit():
                            worktrees_by_ghi[issue_id] = val
                        else:
                            worktrees_by_slug[issue_id] = val
        except Exception:
            pass
            
    print_bold(f"\n🔍 Inspecting Conductor Workspace: {repo_path}", CYAN)
    
    if not os.path.isdir(conductor_dir):
        print(f"{RED}Error: 'conductor/' directory not found in {repo_path}.{RESET}")
        print("Please ensure Conductor is initialized in this repository.")
        sys.exit(1)
        
    # Read Product Metadata
    product_path = os.path.join(conductor_dir, "product.md")
    if os.path.exists(product_path):
        try:
            with open(product_path, "r") as f:
                content = f.read().strip()
                title_line = [line for line in content.split("\n") if line.startswith("# ")][:1]
                title = title_line[0].replace("# ", "") if title_line else "Unknown Product"
                print_bold(f"📦 Product: {title}", BOLD)
        except Exception:
            pass

    # Scan Tracks
    tracks_dir = os.path.join(conductor_dir, "tracks")
    if not os.path.isdir(tracks_dir):
        print(f"{YELLOW}No tracks directory found at 'conductor/tracks/'.{RESET}")
        return

    tracks = os.listdir(tracks_dir)
    # Filter only directories
    track_dirs = [t for t in tracks if os.path.isdir(os.path.join(tracks_dir, t))]
    
    if not track_dirs:
        print("No feature/bugfix tracks registered.")
        return
        
    if short_mode:
        print_bold(f"{'STATUS':<11} | {'PROGRESS':^10} | {'RATIO':^5} | {'GHI':^5} | {'AGENT':^10} | {'CHANGED':^11} | {'TRACK ID':<50} | {'🌳':^3}", BOLD)
        print("=" * 126)
    else:
        print_bold(f"\n🛣️  Tracks Registry ({'all' if show_all else 'open'} tracks):", BOLD)
        print("=" * 60)
    
    track_details = []
    for track_id in track_dirs:
        track_path = os.path.join(tracks_dir, track_id)
        metadata_path = os.path.join(track_path, "metadata.json")
        plan_path = os.path.join(track_path, "plan.md")
        
        status = "unknown"
        description = "No description"
        active_questions = []
        worktree_branch = None
        worktree_dir = None
        github_issue_num = None
        
        # Parse metadata
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    meta = json.load(f)
                    status = meta.get("status", "unknown").upper()
                    description = meta.get("description", description)
                    active_questions = meta.get("active_questions", [])
                    
                    worktree = meta.get("worktree", {})
                    worktree_branch = worktree.get("branch")
                    worktree_dir = worktree.get("directory")
                    
                    gh_issue = meta.get("github_issue", {})
                    github_issue_num = gh_issue.get("number")
            except Exception as e:
                status = f"METADATA_ERROR ({str(e)})"
                
        # Parse plan: first try JSON tasks list (Conductor++), then fall back to plan.md
        plan_stats = None
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    meta = json.load(f)
                    tasks_list = meta.get("tasks")
                    if isinstance(tasks_list, list) and len(tasks_list) > 0:
                        total = len(tasks_list)
                        completed = sum(1 for t in tasks_list if t.get("status") in ("completed", "resolved"))
                        in_progress = sum(1 for t in tasks_list if t.get("status") in ("in_progress", "active"))
                        pending = total - completed - in_progress
                        plan_stats = {
                            "total": total,
                            "completed": completed,
                            "in_progress": in_progress,
                            "pending": pending
                        }
            except Exception:
                pass

        if not plan_stats:
            plan_stats = parse_plan_tasks(plan_path)
            
        # Determine timestamps
        gh_time = None
        if github_issue_num and github_issue_num in gh_timestamps:
            gh_time = parse_datetime(gh_timestamps[github_issue_num])
            
        lc_time = None
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    meta = json.load(f)
                    updated_val = meta.get("updated_at") or meta.get("last_changed")
                    if updated_val:
                        lc_time = parse_datetime(updated_val)
            except Exception:
                pass
                
        if not lc_time and os.path.exists(metadata_path):
            try:
                mtime = os.path.getmtime(metadata_path)
                lc_time = datetime.utcfromtimestamp(mtime)
            except Exception:
                pass
                
        # Compare and decide
        effective_time = None
        source_emoji = ""
        
        if gh_time and lc_time:
            if gh_time >= lc_time:
                effective_time = gh_time
                source_emoji = "🐙"
            else:
                effective_time = lc_time
                source_emoji = "💻"
        elif gh_time:
            effective_time = gh_time
            source_emoji = "🐙"
        elif lc_time:
            effective_time = lc_time
            source_emoji = "💻"
            
        display_time = "-"
        if effective_time:
            from datetime import timezone
            now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
            diff = now_utc - effective_time
            total_seconds = int(diff.total_seconds())
            
            # If changed within the last 24 hours, show relative format
            if total_seconds < 86400:
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                
                if hours > 0:
                    if minutes > 0:
                        rel_str = f"{hours}h{minutes}m"
                    else:
                        rel_str = f"{hours}h"
                elif minutes > 0:
                    rel_str = f"{minutes}min"
                else:
                    rel_str = f"{max(0, seconds)}sec"
                
                display_time = f"{source_emoji} {rel_str}"
            else:
                days = total_seconds // 86400
                display_time = f"{source_emoji} {days}days"

        # Determine if worktree exists
        has_worktree = False
        if worktree_dir:
            full_wt_path = os.path.join(repo_path, worktree_dir) if not os.path.isabs(worktree_dir) else worktree_dir
            if os.path.isdir(full_wt_path):
                has_worktree = True
                
        # Also check "path" from metadata:
        if not has_worktree and os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    meta = json.load(f)
                    w_path = meta.get("worktree", {}).get("path")
                    if w_path:
                        full_wt_path = os.path.join(repo_path, w_path) if not os.path.isabs(w_path) else w_path
                        if os.path.isdir(full_wt_path):
                            has_worktree = True
            except Exception:
                pass
                
        if not has_worktree and github_issue_num:
            if str(github_issue_num) in worktrees_by_ghi:
                has_worktree = True
                
        if not has_worktree:
            slug1 = track_id.replace("_", "-")
            slug2 = re.sub(r"-\d{8}$", "", slug1)
            if slug1 in worktrees_by_slug or slug2 in worktrees_by_slug:
                has_worktree = True

        # Extract Agent name
        agent = None
        # 1. Metadata keys
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    meta = json.load(f)
                    for key in ["agent", "agent_name", "assigned_agent", "assignee"]:
                        if meta.get(key):
                            agent = meta.get(key)
                            break
                            
                    # 2. Active human questions
                    if not agent:
                        active_qs = meta.get("active_questions", [])
                        if isinstance(active_qs, list):
                            for q in active_qs:
                                for key in ["agent", "agent_name", "assigned_agent", "assignee"]:
                                    if q.get(key):
                                        agent = q.get(key)
                                        break
                                if agent:
                                    break
                                    
                    # 3. Tasks list
                    if not agent:
                        tasks = meta.get("tasks", [])
                        if isinstance(tasks, list):
                            for t in tasks:
                                for key in ["agent", "agent_name", "assigned_agent", "assignee"]:
                                    if t.get(key):
                                        agent = t.get(key)
                                        break
                                if agent:
                                    break
            except Exception:
                pass
                
        # 4. Worktree folder matching GHI
        if not agent and github_issue_num:
            ghi_str = str(github_issue_num)
            if ghi_str in worktrees_by_ghi:
                agent = worktrees_by_ghi[ghi_str]["agent"]
                
        # 5. Worktree folder matching slug
        if not agent:
            slug1 = track_id.replace("_", "-")
            slug2 = re.sub(r"-\d{8}$", "", slug1)
            if slug1 in worktrees_by_slug:
                agent = worktrees_by_slug[slug1]["agent"]
            elif slug2 in worktrees_by_slug:
                agent = worktrees_by_slug[slug2]["agent"]
                
        # 6. Worktree path in metadata
        if not agent and os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    meta = json.load(f)
                    w_path = meta.get("worktree", {}).get("path") or meta.get("worktree", {}).get("directory")
                    if w_path:
                        basename = os.path.basename(w_path)
                        match = re.match(r"^issue-(.+)-([^-]+)$", basename)
                        if match:
                            agent = match.group(2)
            except Exception:
                pass

        track_details.append({
            "track_id": track_id,
            "status": status,
            "description": description,
            "active_questions": active_questions,
            "worktree_branch": worktree_branch,
            "worktree_dir": worktree_dir,
            "github_issue_num": github_issue_num,
            "plan_stats": plan_stats,
            "display_time": display_time,
            "effective_time": effective_time,
            "agent": agent,
            "has_worktree": has_worktree
        })

    # Filter completed if we only want open tracks
    if not show_all:
        track_details = [t for t in track_details if t["status"] not in ("COMPLETED", "RESOLVED", "CLOSED")]

    # Sort by effective last changed datetime (recent on top, latest first)
    def get_sort_key(track):
        t = track.get("effective_time")
        if t is None:
            return datetime(1970, 1, 1)
        return t

    track_details.sort(key=get_sort_key, reverse=True)

    for track in track_details:
        track_id = track["track_id"]
        status = track["status"]
        description = track["description"]
        active_questions = track["active_questions"]
        worktree_branch = track["worktree_branch"]
        worktree_dir = track["worktree_dir"]
        github_issue_num = track["github_issue_num"]
        plan_stats = track["plan_stats"]
        
        # Format Status with color
        status_color = RESET
        if status in ("COMPLETED", "RESOLVED", "CLOSED"):
            status_color = GREEN
        elif status in ("IN_PROGRESS", "ACTIVE"):
            status_color = YELLOW
        elif status == "PENDING":
            status_color = CYAN
            
        if short_mode:
            ratio_str = "N/A"
            pct = 0
            if plan_stats:
                if plan_stats["total"] > 0:
                    pct = int((plan_stats["completed"] / plan_stats["total"]) * 100)
                ratio_str = f"{plan_stats['completed']}/{plan_stats['total']}"
            
            bar = make_progress_bar(pct)
            status_padded = f"{status:<11}"
            status_colored = f"{status_color}{status_padded}{RESET}"
            ghi_str = f"#{github_issue_num}" if github_issue_num else ""
            agent_str = track.get("agent") or ""
            display_time_str = track.get("display_time") or "-"
            tree_str = "🌳" if track.get("has_worktree") else ""
            print(f"{status_colored} | {bar} | {ratio_str:>5} | {ghi_str:^5} | {agent_str:^10} | {display_time_str:^11} | {track_id:<50} | {tree_str:^3}")
            continue
            
        wt_suffix = " [🌳]" if track.get("has_worktree") else ""
        print(f"🔸 Track: {BOLD}{track_id}{RESET}{wt_suffix}")
        print(f"   Status: {BOLD}{status_color}{status}{RESET}")
        if track.get("agent"):
            print(f"   Agent: {BOLD}{track.get('agent')}{RESET}")
        display_time = track.get("display_time")
        if display_time and display_time != "-":
            print(f"   Last Changed: {display_time}")
        print(f"   Details: {description}")
        
        if github_issue_num:
            print(f"   GitHub Issue: #{github_issue_num}")
            
        if worktree_branch:
            print(f"   Git Worktree: {worktree_branch} (dir: {worktree_dir})")
            
        if plan_stats:
            pct = 0
            if plan_stats["total"] > 0:
                pct = int((plan_stats["completed"] / plan_stats["total"]) * 100)
            print(f"   Progress: {BOLD}{pct}%{RESET} ({plan_stats['completed']}/{plan_stats['total']} tasks completed, {plan_stats['in_progress']} active)")
            
        # Display questions / blockers
        if active_questions:
            print_bold(f"   ⚠️ Active Human Questions ({len(active_questions)}):", YELLOW)
            for q in active_questions:
                q_status = q.get("status", "awaiting_human").upper()
                q_color = YELLOW if q_status == "AWAITING_HUMAN" else GREEN
                print(f"     - [{q_color}{q_status}{RESET}] {q.get('question')}")
                if q.get("answer"):
                    print(f"       ↳ {GREEN}Answer: {q['answer']}{RESET}")
                    
        print("-" * 60)

    # Calculate Totals
    sum_completed = 0
    sum_total = 0
    has_stats = False
    for t in track_details:
        stats = t.get("plan_stats")
        if stats:
            sum_completed += stats["completed"]
            sum_total += stats["total"]
            has_stats = True
            
    completed_tracks = sum(1 for t in track_details if t["status"] in ("COMPLETED", "RESOLVED", "CLOSED"))
    open_tracks = len(track_details) - completed_tracks
    worktree_count = sum(1 for t in track_details if t.get("has_worktree"))
    ratio_summary = f"{sum_completed}/{sum_total}" if has_stats else "N/A"
    
    if short_mode:
        total_label = f"{'TOTAL':<11}"
        empty_bar = " " * 10
        total_ratio = f"{ratio_summary:>5}"
        empty_ghi = " " * 5
        empty_agent = " " * 10
        empty_changed = " " * 11
        tracks_summary = f"{completed_tracks} completed, {open_tracks} open ({len(track_details)} total)"
        tree_summary = f"{worktree_count} 🌳"
        print("=" * 126)
        print(f"{total_label} | {empty_bar} | {total_ratio} | {empty_ghi} | {empty_agent} | {empty_changed} | {tracks_summary:<50} | {tree_summary:^3}")
    else:
        print("=" * 60)
        print(f"📊 Totals: {completed_tracks} completed, {open_tracks} open ({len(track_details)} total) | Tasks: {ratio_summary} | Worktrees: {worktree_count} 🌳\n")

if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Inspect a Conductor++ workspace's tracks and tasks.")
    parser.add_argument("repo_path", nargs="?", default=".", help="Path to the target git repository (default: .)")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--open", action="store_true", help="Display only open (non-completed) tracks")
    group.add_argument("--all", action="store_true", help="Display all tracks (including completed/resolved)")
    
    parser.add_argument("--short", action="store_true", help="Display only a one-line summary per track with ASCII progress bar")
    
    # If no arguments provided, print help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
        
    args = parser.parse_args()
    
    if not os.path.exists(args.repo_path):
        print(f"{RED}Error: Path {args.repo_path} does not exist.{RESET}")
        sys.exit(1)
        
    inspect_repository(args.repo_path, show_all=args.all, short_mode=args.short)
