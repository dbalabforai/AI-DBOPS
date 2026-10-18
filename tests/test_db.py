import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="companydb",
        user="postgres",
        password="singh"
    )

    print("Connected to PostgreSQL")

    cur = conn.cursor()

    cur.execute("SELECT * FROM employees")

    rows = cur.fetchall()

    print("\nEmployees:")

    for row in rows:
        print(row)

    cur.close()
    conn.close()

    print("\nConnection closed")

except Exception as e:
    print(f"Error: {e}")