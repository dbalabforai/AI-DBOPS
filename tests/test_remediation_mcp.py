from remediation_mcp import RemediationMCP

mcp = RemediationMCP()

print(
    mcp.run_backup()
)

print(
    mcp.verify_backup()
)