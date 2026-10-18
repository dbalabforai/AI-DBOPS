from github_mcp import GitHubMCP
from remediation_mcp import RemediationMCP

github = GitHubMCP()
remediation = RemediationMCP()

issues = github.repo.get_issues(
    state="open"
)

for issue in issues:

    print(
        f"#{issue.number} | {issue.state} | {issue.title}"
    )

    if issue.state != "open":
        continue

    if "Database Backup Failure" not in issue.title:

        print("Skipping")

        continue

    print("Processing Backup Failure")

    output = remediation.run_backup()

    success = remediation.verify_backup()

    if success:

        github.comment_issue(
            issue.number,
            f"""
Automated remediation completed.

Action Taken:
- Executed backup_database.py

Result:
{output}

Verification:
Backup file verified successfully.

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
            "Remediation attempted but verification failed."
        )

        print(
            f"Issue #{issue.number} requires manual review"
        )