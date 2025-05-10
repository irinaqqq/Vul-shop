from flask import Flask, request, render_template_string, redirect, make_response
import sqlite3
import os
import pickle

app = Flask(__name__)
SECRET_KEY = "hardcodedsecretkey123"  # Hardcoded secret

# DB init
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    name = request.args.get('name', 'Guest')
    # XSS vulnerability
    return render_template_string("<h1>Hello, {{ name }}</h1>", name=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # SQL Injection vulnerability
        username = request.form['username']
        password = request.form['password']
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        if result:
            resp = make_response("Logged in")
            return resp
        return "Invalid credentials"
    return '''
    <form method="post">
      <input name="username" />
      <input name="password" />
      <button type="submit">Login</button>
    </form>
    '''

@app.route('/ping')
def ping():
    host = request.args.get('host', '127.0.0.1')
    # Command injection
    os.system(f"ping -c 1 {host}")
    return f"Pinging {host}"

@app.route('/redirect')
def unsafe_redirect():
    # Unvalidated redirect
    url = request.args.get('url', '/')
    return redirect(url)

@app.route('/deserialize', methods=['POST'])
def deserialize():
    # Insecure deserialization
    data = request.data
    obj = pickle.loads(data)
    return f"Deserialized: {obj}"

@app.route('/eval')
def eval_input():
    code = request.args.get("code", "")
    try:
        result = eval(code)  # Dangerous
        return str(result)
    except Exception as e:
        return str(e)

@app.after_request
def add_headers(response):
    # Missing security headers
    return response

if __name__ == '__main__':
    app.run(debug=True)
