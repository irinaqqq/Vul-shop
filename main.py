from flask import Flask, request, render_template_string, redirect, make_response
import sqlite3
import os
import pickle
import base64

app = Flask(__name__)
SECRET_KEY = "this_should_be_env_var"  # ⚠️ FP: выглядит как секрет

def get_db_connection():
    db_url = "postgresql://user:pass@localhost:5432/mydb"  # ⚠️ FP: "секрет"
    return sqlite3.connect("users.db")

@app.route('/')
def index():
    name = request.args.get('name', 'Guest')
    # ⚠️ FP: безопасно, но может считаться XSS
    return render_template_string("<h1>Hello, {{ name }}</h1>", name=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # ❌ SQL Injection (реальная уязвимость)
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        return "Welcome!" if user else "Invalid credentials"

    return '''
    <form method="post">
      <input name="username" />
      <input name="password" />
      <button type="submit">Login</button>
    </form>
    '''

@app.route('/eval')
def eval_input():
    code = request.args.get("code", "")
    # ⚠️ FP: безопасно, но выглядит подозрительно
    try:
        allowed_builtins = {"abs": abs, "max": max}
        result = eval(code, {"__builtins__": allowed_builtins})
        return str(result)
    except Exception as e:
        return str(e)

@app.route('/deserialize')
def fake_deserialization():
    # ⚠️ FP: выглядит как десериализация, но это просто base64
    encoded = request.args.get('data', '')
    try:
        obj = base64.b64decode(encoded.encode())
        return "Decoded OK"
    except:
        return "Failed"

@app.route('/secret-check')
def check_header():
    # ⚠️ FP: псевдо-ключ
    auth = request.headers.get("X-Api-Key", "")
    if auth == "1234567890abcdef":
        return "Secret accepted"
    return "Access Denied"

@app.after_request
def add_headers(response):
    # ⚠️ FP: отсутствие security headers
    return response

if __name__ == '__main__':
    app.run(debug=True)
