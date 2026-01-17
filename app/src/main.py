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


@app.route("/users")
def get_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, username, created_at FROM users;")
    rows = cur.fetchall()

    users = [
        {
            "id": r[0],
            "username": r[1],
            "created_at": r[2].isoformat()
        }
        for r in rows
    ]

    cur.close()
    conn.close()

    return jsonify(users), 200


@app.route("/items")
def get_items():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, created_at FROM items;")
    rows = cur.fetchall()

    items = [
        {
            "id": r[0],
            "name": r[1],
            "created_at": r[2].isoformat()
        }
        for r in rows
    ]

    cur.close()
    conn.close()

    return jsonify(items), 200


@app.route("/users/<int:user_id>")
def get_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username, created_at FROM users WHERE id = %s;",
        (user_id,)
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(
        {
            "id": row[0],
            "username": row[1],
            "created_at": row[2].isoformat()
        }
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
