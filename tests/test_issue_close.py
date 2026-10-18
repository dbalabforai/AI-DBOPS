# test_issue_close.py

from github_mcp import GitHubMCP

github = GitHubMCP()

print(
    github.comment_issue(
        3,
        "Automated remediation completed successfully."
    )
)

print(
    github.close_issue(3)
)