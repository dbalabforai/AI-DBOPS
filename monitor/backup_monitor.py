import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from datetime import datetime, timedelta

from github_mcp import GitHubMCP

BACKUP_FOLDER = "backups"


def create_alert(message):

    github = GitHubMCP()

    title = "Database Backup Failure"

    body = f"""
Severity: High

Time: {datetime.now()}

Issue:
{message}

Source:
backup_monitor.py
"""

    result = github.create_issue(
        title,
        body
    )

    print(result)


def check_backup():

    if not os.path.exists(BACKUP_FOLDER):
        return False, "Backup folder missing"

    files = [
        f for f in os.listdir(BACKUP_FOLDER)
        if f.endswith(".sql")
    ]

    if not files:
        return False, "No backup files found"

    newest = max(
        [os.path.join(BACKUP_FOLDER, f) for f in files],
        key=os.path.getmtime
    )

    modified = datetime.fromtimestamp(
        os.path.getmtime(newest)
    )

    age = datetime.now() - modified

    if age > timedelta(hours=24):
        return False, f"Backup older than 24 hours: {age}"

    return True, newest


status, message = check_backup()

if status:
    print("HEALTHY")
    print(message)

else:
    print("ALERT")
    print(message)

    create_alert(message)