import os
from datetime import datetime

import pandas as pd
import streamlit as st

from config import DATABASES

from mcp.retention_mcp import RetentionMCP
from mcp.github_mcp import GitHubMCP


st.set_page_config(
    page_title="AI-DBOPS",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI-DBOPS Dashboard")

retention = RetentionMCP()
github = GitHubMCP()

open_issues = list(
    github.repo.get_issues(
        state="open"
    )
)

#
# KPI Cards
#
healthy_count = 0

for db in DATABASES:

    db_name = db["name"]

    has_backup = False

    if os.path.exists("backups"):

        for file in os.listdir("backups"):

            if file.startswith(db_name):

                has_backup = True
                break

    if has_backup:
        healthy_count += 1

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Databases",
    len(DATABASES)
)

col2.metric(
    "Healthy Databases",
    healthy_count
)

col3.metric(
    "Open Incidents",
    len(open_issues)
)

col4.metric(
    "Backup Storage MB",
    retention.get_backup_size_mb()
)

st.divider()

#
# Database Status Table
#
rows = []

backup_files = []

if os.path.exists("backups"):

    backup_files = [
        f
        for f in os.listdir("backups")
        if f.endswith(".sql")
    ]

for db_info in DATABASES:

    db_name = db_info["name"]
    db_type = db_info["type"]

    matching_files = [
        f
        for f in backup_files
        if f.startswith(db_name)
    ]

    issue_number = "None"

    for issue in open_issues:

        if db_name.lower() in issue.title.lower():

            issue_number = f"#{issue.number}"

    if matching_files:

        latest_backup = max(
            matching_files,
            key=lambda x: os.path.getmtime(
                os.path.join(
                    "backups",
                    x
                )
            )
        )

        full_path = os.path.join(
            "backups",
            latest_backup
        )

        backup_time = datetime.fromtimestamp(
            os.path.getmtime(full_path)
        )

        backup_size = round(
            os.path.getsize(full_path) / 1024,
            2
        )

        backup_age = round(
            (
                datetime.now()
                - backup_time
            ).total_seconds()
            / 3600,
            2
        )

        if backup_age > 24:

            backup_status = "🟡 Warning"

        else:

            backup_status = "🟢 Success"

        rows.append(
            {
                "DB Name": db_name,
                "DB Type": db_type,
                "DB Status": "🟢 Online",
                "Backup Status": backup_status,
                "Backup Age (hrs)": backup_age,
                "Last Backup": backup_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "Backup Size KB": backup_size,
                "Open Issue": issue_number
            }
        )

    else:

        rows.append(
            {
                "DB Name": db_name,
                "DB Type": db_type,
                "DB Status": "🟢 Online",
                "Backup Status": "🟡 No Backup",
                "Backup Age (hrs)": "N/A",
                "Last Backup": "N/A",
                "Backup Size KB": "N/A",
                "Open Issue": issue_number
            }
        )

st.subheader("Database Backup Status")

st.dataframe(
    pd.DataFrame(rows),
    use_container_width=True,
    hide_index=True
)

st.divider()

#
# Open Incidents
#
st.subheader("Open Incidents")

incident_rows = []

for issue in open_issues:

    incident_rows.append(
        {
            "Issue #": issue.number,
            "Title": issue.title,
            "Created": issue.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }
    )

if incident_rows:

    st.dataframe(
        pd.DataFrame(
            incident_rows
        ),
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "No open incidents"
    )