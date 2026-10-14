import os
from datetime import datetime, timedelta

BACKUP_FOLDER = "backups"

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
        return False, f"Backup too old: {age}"

    return True, newest


status, message = check_backup()

if status:
    print("HEALTHY")
    print(message)
else:
    print("ALERT")
    print(message)