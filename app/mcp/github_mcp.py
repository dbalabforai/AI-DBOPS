import os

from github import Github
from dotenv import load_dotenv


class GitHubMCP:

    def __init__(self):

        load_dotenv()

        token = os.getenv("GITHUB_TOKEN")

        self.github = Github(token)

        self.repo = self.github.get_repo(
            "dbalabforai/AI-DBOPS"
        )

    def create_issue(self, title, body):

        issue = self.repo.create_issue(
            title=title,
            body=body
        )

        return f"Issue #{issue.number} created"

    def list_open_issues(self):

        issues = self.repo.get_issues(
            state="open"
        )

        return [
            f"#{issue.number} - {issue.title}"
            for issue in issues
        ]

    def comment_issue(self, issue_number, comment):

        issue = self.repo.get_issue(
            issue_number
        )

        issue.create_comment(
            comment
        )

        return f"Comment added to issue #{issue_number}"

    def close_issue(self, issue_number):

        issue = self.repo.get_issue(
            issue_number
        )

        issue.edit(
            state="closed"
        )

        return f"Issue #{issue_number} closed"