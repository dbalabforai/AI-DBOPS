import os
import subprocess
from datetime import datetime

from config import DATABASES

BACKUP_DIR = "backups"

os.makedirs(
    BACKUP_DIR,
    exist_ok=True
)

PG_DUMP = (
    r"C:\Users\LABWORK\AI-DB\postgresql\bin\pg_dump.exe"
)

POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "singh"


def backup_database(db_name):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_file = os.path.join(
        BACKUP_DIR,
        f"{db_name}_{timestamp}.sql"
    )

    cmd = [
        PG_DUMP,
        "-U",
        POSTGRES_USER,
        "-d",
        db_name,
        "-f",
        backup_file
    ]

    env = os.environ.copy()

    env["PGPASSWORD"] = (
        POSTGRES_PASSWORD
    )

    result = subprocess.run(
        cmd,
        env=env,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:

        print(
            f"✅ {db_name} backed up"
        )

        return True

    else:

        print(
            f"❌ {db_name} failed"
        )

        print(result.stderr)

        return False


for db in DATABASES:

    backup_database(
        db["name"]
    )