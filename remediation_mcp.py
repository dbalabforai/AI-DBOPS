import subprocess
import os


class RemediationMCP:

    def run_backup(self):

        result = subprocess.run(
            ["py", "backup_database.py"],
            capture_output=True,
            text=True
        )

        return result.stdout

    def verify_backup(self):

        if not os.path.exists("backups"):
            return False

        files = [
            f for f in os.listdir("backups")
            if f.endswith(".sql")
        ]

        return len(files) > 0