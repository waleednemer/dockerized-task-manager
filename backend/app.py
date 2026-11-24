import os
from contextlib import closing
from datetime import date

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)

STATUSES = {"todo", "doing", "done"}
PRIORITIES = {"low", "medium", "high"}
COLS = "id, title, status, priority, due_date::text AS due_date"


def connect():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "taskdb"),
        user=os.getenv("DB_USER", "taskuser"),
        password=os.getenv("DB_PASSWORD", "taskpass"),
    )


def query(sql, params=(), fetch="all"):
    with closing(connect()) as conn, conn:  # noqa: SIM117
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall() if fetch == "all" else cur.fetchone()


def clean(data, partial=False):
    out = {}
    if "title" in data or not partial:
        title = (data.get("title") or "").strip()
        if not title:
            return None, "العنوان مطلوب"
        out["title"] = title[:200]
    if "status" in data:
        if data["status"] not in STATUSES:
            return None, "حالة غير صالحة"
        out["status"] = data["status"]
    if "priority" in data:
        if data["priority"] not in PRIORITIES:
            return None, "أولوية غير صالحة"
        out["priority"] = data["priority"]
    if "due_date" in data:
        try:
            out["due_date"] = date.fromisoformat(data["due_date"]) if data["due_date"] else None
        except ValueError:
            return None, "تاريخ غير صالح"
    return out, None


@app.get("/api/tasks")
def list_tasks():
    return jsonify(query(f"SELECT {COLS} FROM tasks ORDER BY status = 'done', id DESC"))


@app.post("/api/tasks")
def create_task():
    data, err = clean(request.get_json(silent=True) or {})
    if err:
        return jsonify(error=err), 400
    cols = ", ".join(data)
    marks = ", ".join(["%s"] * len(data))
    row = query(f"INSERT INTO tasks ({cols}) VALUES ({marks}) RETURNING {COLS}", tuple(data.values()), "one")
    return jsonify(row), 201


@app.put("/api/tasks/<int:task_id>")
def update_task(task_id):
    data, err = clean(request.get_json(silent=True) or {}, partial=True)
    if err or not data:
        return jsonify(error=err or "لا توجد بيانات للتحديث"), 400
    sets = ", ".join(f"{k} = %s" for k in data)
    row = query(f"UPDATE tasks SET {sets} WHERE id = %s RETURNING {COLS}", (*data.values(), task_id), "one")
    return (jsonify(row), 200) if row else (jsonify(error="المهمة غير موجودة"), 404)


@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    row = query("DELETE FROM tasks WHERE id = %s RETURNING id", (task_id,), "one")
    return ("", 204) if row else (jsonify(error="المهمة غير موجودة"), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051, debug=True)
