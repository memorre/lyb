from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.getcwd(), "guestbook.db")

def init_db():
    if not os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn, open("schema.sql") as f:
            conn.executescript(f.read())

@app.route("/", methods=["GET", "POST"])
def index():
    init_db()  # 每次都保证有数据库
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        message = request.form.get("message", "").strip()
        if name and message:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("INSERT INTO messages (name, message) VALUES (?, ?)", (name, message))
        return redirect("/")
    # GET请求：显示所有留言
    with sqlite3.connect(DB_PATH) as conn:
        msgs = conn.execute("SELECT name, message, created_at FROM messages ORDER BY id DESC").fetchall()
    return render_template("index.html", messages=msgs)

if __name__ == "__main__":
    app.run(debug=True)