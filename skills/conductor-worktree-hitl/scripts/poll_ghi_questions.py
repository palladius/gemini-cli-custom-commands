#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import re
from datetime import datetime

def find_conductor_dir():
    # Look for the nearest 'conductor' folder going up the directory tree
    curr = os.getcwd()
    while True:
        candidate = os.path.join(curr, "conductor")
        if os.path.isdir(candidate):
            return candidate
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    # Default fallback to ./conductor
    return os.path.join(os.getcwd(), "conductor")

CONDUCTOR_DIR = find_conductor_dir()
QUESTIONS_JSON = os.path.join(CONDUCTOR_DIR, "questions.json")

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}: {e.stderr}", file=sys.stderr)
        return None

def fetch_issues():
    cmd = ["gh", "issue", "list", "--state", "open", "--json", "number,title,author"]
    output = run_command(cmd)
    if not output:
        return []
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return []

def fetch_comments(issue_number):
    cmd = ["gh", "issue", "view", str(issue_number), "--json", "comments"]
    output = run_command(cmd)
    if not output:
        return []
    try:
        data = json.loads(output)
        return data.get("comments", [])
    except json.JSONDecodeError:
        return []

def update_conductor_tracks(issue_number, agent_name, answer_text):
    # Scan conductor/tracks/ to find any metadata.json matching the issue number
    tracks_dir = os.path.join(CONDUCTOR_DIR, "tracks")
    if not os.path.isdir(tracks_dir):
        return

    for track_id in os.listdir(tracks_dir):
        track_path = os.path.join(tracks_dir, track_id)
        metadata_path = os.path.join(track_path, "metadata.json")
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    meta = json.load(f)
                
                # Check if this track is associated with the target GitHub issue
                gh_issue = meta.get("github_issue", {})
                if gh_issue.get("number") == issue_number:
                    updated = False
                    for q in meta.get("active_questions", []):
                        if q.get("agent") == agent_name and q.get("status") == "awaiting_human":
                            q["status"] = "answered"
                            q["answer"] = answer_text
                            updated = True
                    
                    if updated:
                        meta["updated_at"] = datetime.utcnow().isoformat() + "Z"
                        with open(metadata_path, "w") as f:
                            json.dump(meta, f, indent=2)
                        print(f"   💾 Updated local track metadata: {track_id}/metadata.json")
            except Exception as e:
                print(f"   ⚠️ Error updating track metadata for {track_id}: {e}", file=sys.stderr)
def get_issues_awaiting_human():
    # Scan conductor/tracks/*/metadata.json for any active questions awaiting human response
    tracks_dir = os.path.join(CONDUCTOR_DIR, "tracks")
    if not os.path.isdir(tracks_dir):
        return {}

    issues_to_poll = {}
    for track_id in os.listdir(tracks_dir):
        track_path = os.path.join(tracks_dir, track_id)
        metadata_path = os.path.join(track_path, "metadata.json")
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    meta = json.load(f)
                
                status = meta.get("status", "unknown").upper()
                if status in ("COMPLETED", "RESOLVED", "CLOSED"):
                    continue
                
                active_qs = meta.get("active_questions", [])
                has_awaiting = any(q.get("status") == "awaiting_human" for q in active_qs)
                
                gh_issue = meta.get("github_issue", {})
                issue_num = gh_issue.get("number")
                
                if has_awaiting and issue_num:
                    issues_to_poll[issue_num] = {
                        "track_id": track_id,
                        "title": meta.get("description", "Awaiting input")
                    }
            except Exception as e:
                print(f"   ⚠️ Error reading track metadata for {track_id}: {e}", file=sys.stderr)
                
    return issues_to_poll

def process_questions():
    print(f"🤖 Scanning local tracks (Conductor: {CONDUCTOR_DIR})...")
    issues_to_poll = get_issues_awaiting_human()
    
    if not issues_to_poll:
        print("✅ No local tracks are currently awaiting human input. Skipping GitHub poll.")
        # Ensure questions.json is empty/cleared
        if os.path.exists(QUESTIONS_JSON):
            try:
                with open(QUESTIONS_JSON, "w") as f:
                    json.dump([], f, indent=2)
            except Exception:
                pass
        return

    print(f"🔍 Found {len(issues_to_poll)} issue(s) awaiting human input. Polling GitHub comments...")
    active_questions = []

    question_pattern = re.compile(r"\[QUESTION\](?:\[([^\]]+)\])?\s*(.*)", re.IGNORECASE)
    answer_pattern = re.compile(r"\[ANSWER\](?:\[([^\]]+)\])?\s*(.*)", re.IGNORECASE)

    for num, track_info in issues_to_poll.items():
        title = track_info["title"]
        comments = fetch_comments(num)
        if not comments:
            continue

        questions_by_agent = {}

        for comment in comments:
            author = comment["author"]["login"]
            body = comment["body"]
            created_at = comment["createdAt"]

            q_match = question_pattern.search(body)
            if q_match:
                agent_name = q_match.group(1) or author
                q_text = q_match.group(2).strip()
                questions_by_agent[agent_name] = {
                    "issue_number": num,
                    "issue_title": title,
                    "agent": agent_name,
                    "question": q_text,
                    "created_at": created_at,
                    "author": author
                }
                continue

            a_match = answer_pattern.search(body)
            if a_match:
                agent_name = a_match.group(1) or author
                a_text = a_match.group(2).strip()
                if agent_name in questions_by_agent:
                    questions_by_agent[agent_name]["answer"] = a_text
                    # Sync to Conductor++ track database
                    update_conductor_tracks(num, agent_name, a_text)

        for q in questions_by_agent.values():
            active_questions.append(q)

    # Ensure output dir exists
    os.makedirs(CONDUCTOR_DIR, exist_ok=True)

    # Save to global questions.json
    with open(QUESTIONS_JSON, "w") as f:
        json.dump(active_questions, f, indent=2)

    # Output report
    if active_questions:
        print(f"\n📢 Found {len(active_questions)} Active Question(s) from Subagents:\n")
        for q in active_questions:
            print(f"🔹 Issue #{q['issue_number']}: {q['issue_title']}")
            print(f"   👤 Agent: {q['agent']}")
            print(f"   ❓ Question: {q['question']}")
            if "answer" in q:
                print(f"   ✅ Answered: {q['answer']}")
            else:
                print(f"   ⚠️ Awaiting Human Answer!")
            print(f"   ⏰ Date: {q['created_at']}")
            print("-" * 50)
    else:
        print("\n✅ No active questions from subagents. All clear!")

if __name__ == "__main__":
    process_questions()
