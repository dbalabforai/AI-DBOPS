from retention_mcp import RetentionMCP

mcp = RetentionMCP()

print(
    "Before:",
    mcp.get_backup_count()
)

removed = mcp.cleanup_old_backups(
    keep_count=5
)

print(
    "Removed:",
    removed
)

print(
    "After:",
    mcp.get_backup_count()
)