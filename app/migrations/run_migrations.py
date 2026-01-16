import os
import time
import psycopg2

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "devops_db")
DB_USER = os.getenv("DB_USER", "devops")
DB_PASSWORD = os.getenv("DB_PASSWORD", "devops")
DB_PORT = int(os.getenv("DB_PORT", 5432))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_FILE = os.path.join(BASE_DIR, "init.sql")

MAX_RETRIES = 10
RETRY_DELAY = 3  # seconds


def wait_for_db():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
            )
            conn.close()
            print("✅ Database is ready")
            return
        except psycopg2.OperationalError:
            print(f"⏳ DB not ready yet... retry {attempt}/{MAX_RETRIES}")
            time.sleep(RETRY_DELAY)

    raise RuntimeError("❌ Database not available after retries")


def run_migrations():
    with open(SQL_FILE, "r") as f:
        sql = f.read()

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute(sql)

    conn.close()
    print("✅ Migrations applied successfully")


def main():
    print("🚀 Starting migration runner")
    wait_for_db()
    run_migrations()


if __name__ == "__main__":
    main()