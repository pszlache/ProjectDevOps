import psycopg2
import csv
from datetime import datetime
import os
import time

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "devops_db")
DB_USER = os.getenv("DB_USER", "devops")
DB_PASSWORD = os.getenv("DB_PASSWORD", "devops")

OUTPUT_DIR = "/seed_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

users = [
    ("Piotr", "piotr@example.com"),
    ("Andrzej", "andrzej@example.com"),
    ("Robert", "robert@example.com"),
    ("Kasia", "kasia@example.com"),
    ("Anna", "anna@example.com"),
]

def wait_for_db():
    for i in range(10):
        try:
            psycopg2.connect(
                host=DB_HOST,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
            ).close()
            print("Database is ready")
            return
        except Exception:
            print(f"DB not ready yet... retry {i+1}/10")
            time.sleep(2)
    raise Exception("Database not available")

def main():
    wait_for_db()

    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    cur = conn.cursor()

    cur.executemany(
        """
        INSERT INTO users (username)
        VALUES (%s)
        ON CONFLICT DO NOTHING
        """,
        [(u[0],) for u in users]
    )

    conn.commit()

    csv_path = os.path.join(OUTPUT_DIR, "users.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username"])
        for u in users:
            writer.writerow([u[0]])

    log_path = os.path.join(OUTPUT_DIR, "seed.log")
    with open(log_path, "w") as f:
        f.write(f"Seed completed at {datetime.utcnow()} UTC\n")
        f.write(f"Inserted {len(users)} users\n")

    cur.close()
    conn.close()
    print("🌱 Seed completed successfully")

if __name__ == "__main__":
    main()
