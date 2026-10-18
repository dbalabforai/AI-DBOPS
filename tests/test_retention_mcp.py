from retention_mcp import RetentionMCP

mcp = RetentionMCP()

print(
    "Backup Count:",
    mcp.get_backup_count()
)

print(
    "Backup Size MB:",
    mcp.get_backup_size_mb()
)