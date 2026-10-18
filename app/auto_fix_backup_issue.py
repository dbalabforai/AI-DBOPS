from github_mcp import GitHubMCP
from remediation_mcp import RemediationMCP
from retention_mcp import RetentionMCP
from config import MAX_BACKUP_FILES

github = GitHubMCP()
remediation = RemediationMCP()
retention = RetentionMCP()

issues = github.repo.get_issues(
    state="open"
)

for issue in issues:

    print(
        f"#{issue.number} | {issue.title}"
    )

    #
    # DATABASE BACKUP FAILURE
    #
    if issue.title == "Database Backup Failure":

        print(
            "Processing Backup Failure"
        )

        output = remediation.run_backup()

        success = remediation.verify_backup()

        if success:

            github.comment_issue(
                issue.number,
                f"""
Automated remediation completed.

Action:
Executed backup_database.py

Result:
{output}

Verification:
Backup verified successfully.

Status:
Resolved
"""
            )

            github.close_issue(
                issue.number
            )

            print(
                f"Issue #{issue.number} resolved"
            )

        else:

            github.comment_issue(
                issue.number,
                "Remediation failed."
            )

    #
    # BACKUP STORAGE FULL
    #
    elif issue.title == "Backup Storage Full":

        print(
            "Processing Storage Alert"
        )

        removed = retention.cleanup_old_backups(
            keep_count=MAX_BACKUP_FILES
        )

        current_count = (
            retention.get_backup_count()
        )

        if current_count <= MAX_BACKUP_FILES:

            github.comment_issue(
                issue.number,
                f"""
Automated retention cleanup completed.

Files Removed:
{removed}

Current Backup Count:
{current_count}

Status:
Resolved
"""
            )

            github.close_issue(
                issue.number
            )

            print(
                f"Issue #{issue.number} resolved"
            )

        else:

            github.comment_issue(
                issue.number,
                "Cleanup failed. Manual review required."
            )