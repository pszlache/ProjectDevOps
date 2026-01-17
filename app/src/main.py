from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("DB_NAME", "devops_db"),
        user=os.getenv("DB_USER", "devops"),
        password=os.getenv("DB_PASSWORD", "devops"),
        port=5432
    )

@app.route("/")
def index():
    return "ProjectDevOps"

@app.route("/health")
def health():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM users;")
        users_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM items;")
        items_count = cur.fetchone()[0]

        cur.close()
        conn.close()

        return jsonify(
            status="ok",
            users=users_count,
            items=items_count
        ), 200
    except Exception as e:
        return jsonify(
            status="error",
            error=str(e)
        ), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)