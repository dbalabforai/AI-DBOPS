import os


class RetentionMCP:

    BACKUP_FOLDER = "backups"

    def get_backup_count(self):

        if not os.path.exists(self.BACKUP_FOLDER):
            return 0

        return len([
            f for f in os.listdir(
                self.BACKUP_FOLDER
            )
            if f.endswith(".sql")
        ])

    def get_backup_size_mb(self):

        total_size = 0

        if not os.path.exists(
            self.BACKUP_FOLDER
        ):
            return 0

        for file in os.listdir(
            self.BACKUP_FOLDER
        ):

            if file.endswith(".sql"):

                path = os.path.join(
                    self.BACKUP_FOLDER,
                    file
                )

                total_size += os.path.getsize(
                    path
                )

        return round(
            total_size / 1024 / 1024,
            2
        )

    def cleanup_old_backups(
        self,
        keep_count=5
    ):

        files = []

        for file in os.listdir(
            self.BACKUP_FOLDER
        ):

            if file.endswith(".sql"):

                path = os.path.join(
                    self.BACKUP_FOLDER,
                    file
                )

                files.append(
                    (
                        path,
                        os.path.getmtime(path)
                    )
                )

        files.sort(
            key=lambda x: x[1]
        )

        removed = []

        while len(files) > keep_count:

            file_to_delete = files.pop(0)

            os.remove(
                file_to_delete[0]
            )

            removed.append(
                os.path.basename(
                    file_to_delete[0]
                )
            )

        return removed