from postgres_mcp import PostgresMCP

db = PostgresMCP()

print("\n=== DB STATUS ===")
print(db.db_status())

print("\n=== EMPLOYEE COUNT ===")
print(db.get_employee_count())

print("\n=== EMPLOYEES ===")
print(
    db.run_query(
        "SELECT * FROM employees"
    )
)