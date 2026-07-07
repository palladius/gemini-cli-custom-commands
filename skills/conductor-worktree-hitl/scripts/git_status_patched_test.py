#!/usr/bin/env python3
"""
# Unit tests for git_status_patched.py
#
# USER MANUAL:
# This is a self-runnable test suite to verify the matching and utility
# functions inside git_status_patched.py.
#
# How to run:
#   python3 git_status_patched_test.py
"""

import unittest
from unittest.mock import patch
import os
import json
import sys

# Append script directory to sys.path to import git_status_patched
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import git_status_patched

class TestGitStatusPatched(unittest.TestCase):
    @patch('git_status_patched.find_repo_root')
    def test_find_matching_track_explicit_path(self, mock_find_root):
        mock_find_root.return_value = "/repo"
        tracks_meta = [
            {
                "_track_id": "track_1",
                "_metadata_path": "/repo/conductor/tracks/track_1/metadata.json",
                "worktree": {
                    "path": ".worktrees/issue-1-agostina"
                }
            }
        ]
        
        # Test match
        meta = git_status_patched.find_matching_track(
            "/repo/.worktrees/issue-1-agostina", 
            "branch-1", 
            tracks_meta
        )
        self.assertIsNotNone(meta)
        self.assertEqual(meta["_track_id"], "track_1")

    def test_find_matching_track_branch(self):
        tracks_meta = [
            {
                "_track_id": "track_2",
                "_metadata_path": "/repo/conductor/tracks/track_2/metadata.json",
                "worktree": {
                    "branch": "feature/cool-stuff"
                }
            }
        ]
        
        meta = git_status_patched.find_matching_track(
            "/repo/.worktrees/some-folder", 
            "feature/cool-stuff", 
            tracks_meta
        )
        self.assertIsNotNone(meta)
        self.assertEqual(meta["_track_id"], "track_2")

    def test_find_matching_track_substring(self):
        tracks_meta = [
            {
                "_track_id": "issue-123-bugfix",
                "_metadata_path": "/repo/conductor/tracks/issue-123-bugfix/metadata.json"
            }
        ]
        
        meta = git_status_patched.find_matching_track(
            "/repo/.worktrees/issue-123-bugfix-agostina", 
            "some-branch", 
            tracks_meta
        )
        self.assertIsNotNone(meta)
        self.assertEqual(meta["_track_id"], "issue-123-bugfix")

    def test_find_matching_track_issue_number(self):
        tracks_meta = [
            {
                "_track_id": "bugfix_track",
                "_metadata_path": "/repo/conductor/tracks/bugfix_track/metadata.json",
                "github_issue": {
                    "number": 456
                }
            }
        ]
        
        meta = git_status_patched.find_matching_track(
            "/repo/.worktrees/issue-456-mario", 
            "some-branch", 
            tracks_meta
        )
        self.assertIsNotNone(meta)
        self.assertEqual(meta["_track_id"], "bugfix_track")

if __name__ == "__main__":
    unittest.main()
