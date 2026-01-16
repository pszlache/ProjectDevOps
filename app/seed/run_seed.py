import psycopg2
import csv
from datetime import datetime
import os

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "devobs_db")
DB_USER = os.getenv("DB_USER", "devops")
DB_PASSWORD = os.getenv("DB_PASSWORD", "devops")

OUTPUT_DIR = "/seed_outpus"
os.makedirs(OUTPUT_DIR, exist_ok=True)

users = [
    ("Piotr", "piotr@example.com"),
    ("Andrzej", "andrzej@example.com"),
    ("Robert", "robert@example.com"),
    ("Kasia", "kasia@example.com"),
    ("Anna", "anna@example.com"),
]

def main():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    """)

    cur.executemany(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        users
    )

    conn.commit()

    csv_path = os.path.join(OUTPUT_DIR, "users.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "email"])
        writer.writerows(users)

    log_path = os.path.join(OUTPUT_DIR, "seed.log")
    with open(log_path, "w") as f:
        f.write(f"Seed completed at {datetime.utcnow()} UTC\n")
        f.write(f"Inserted {len(users)} users\n")
                
    cur.close()
    conn.close()

    if __name__ == "__main__":
        main()