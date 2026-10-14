import os
import subprocess
from datetime import datetime

BACKUP_DIR = "backups"

os.makedirs(BACKUP_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

backup_file = os.path.join(
    BACKUP_DIR,
    f"companydb_{timestamp}.sql"
)

pg_dump = r"C:\Users\LABWORK\AI-DB\postgresql\bin\pg_dump.exe"

cmd = [
    pg_dump,
    "-U",
    "postgres",
    "-d",
    "companydb",
    "-f",
    backup_file
]

env = os.environ.copy()

env["PGPASSWORD"] = "singh"

try:
    result = subprocess.run(
        cmd,
        env=env,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Backup successful")
        print(backup_file)
    else:
        print("Backup failed")
        print(result.stderr)

except Exception as e:
    print(e)