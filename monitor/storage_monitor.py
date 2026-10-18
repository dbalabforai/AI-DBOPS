import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from retention_mcp import RetentionMCP
from github_mcp import GitHubMCP
from config import MAX_BACKUP_FILES


retention = RetentionMCP()
github = GitHubMCP()

count = retention.get_backup_count()

print(
    f"Current Backup Count: {count}"
)

if count > MAX_BACKUP_FILES:

    print(
        "ALERT: Backup retention exceeded"
    )

    result = github.create_issue(
        "Backup Storage Full",
        f"""
Backup retention threshold exceeded.

Current Backups: {count}

Allowed Backups: {MAX_BACKUP_FILES}

Action Required:
Cleanup old backup files.
"""
    )

    print(result)

else:

    print(
        "Retention Healthy"
    )