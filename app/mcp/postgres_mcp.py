import psycopg2


class PostgresMCP:

    def __init__(self):
        self.conn_info = {
            "host": "localhost",
            "database": "companydb",
            "user": "postgres",
            "password": "singh"
        }

    def db_status(self):
        try:
            conn = psycopg2.connect(**self.conn_info)
            conn.close()
            return "Database is ONLINE"
        except Exception as e:
            return f"Database is OFFLINE: {e}"

    def get_employee_count(self):
        try:
            conn = psycopg2.connect(**self.conn_info)

            cur = conn.cursor()

            cur.execute(
                "SELECT COUNT(*) FROM employees"
            )

            count = cur.fetchone()[0]

            cur.close()
            conn.close()

            return count

        except Exception as e:
            return str(e)

    def run_query(self, query):
        try:
            conn = psycopg2.connect(**self.conn_info)

            cur = conn.cursor()

            cur.execute(query)

            rows = cur.fetchall()

            cur.close()
            conn.close()

            return rows

        except Exception as e:
            return str(e)