"""
Deliberately vulnerable Flask app for GH-500 (GitHub Advanced Security) practice.

DO NOT DEPLOY. Every route below contains a classic flaw that CodeQL should flag.
Each one is tagged with the CWE so you can match it to the alert in the Security tab.
"""
import os
import pickle
import sqlite3
import subprocess
import hashlib

import yaml
from flask import Flask, request, send_file, make_response

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def get_db():
    return sqlite3.connect(DB_PATH)


# CWE-89: SQL injection -> py/sql-injection
@app.route("/user")
def get_user():
    username = request.args.get("name", "")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users WHERE name = '" + username + "'")
    return str(cur.fetchall())


# CWE-78: OS command injection -> py/command-line-injection
@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    output = subprocess.check_output("ping -c 1 " + host, shell=True)
    return output


# CWE-22: Path traversal -> py/path-injection
@app.route("/download")
def download():
    filename = request.args.get("file", "readme.txt")
    return send_file(os.path.join("/srv/files", filename))


# CWE-79: Reflected XSS -> py/reflective-xss
@app.route("/hello")
def hello():
    name = request.args.get("name", "world")
    return make_response("<h1>Hello " + name + "</h1>")


# CWE-502: Unsafe deserialization -> py/unsafe-deserialization
@app.route("/load", methods=["POST"])
def load():
    obj = pickle.loads(request.get_data())
    return str(obj)


# CWE-502 again, via YAML -> py/unsafe-deserialization
@app.route("/config", methods=["POST"])
def config():
    data = yaml.load(request.get_data(), Loader=yaml.Loader)
    return str(data)


# CWE-327/328: Weak hashing of a password -> py/weak-sensitive-data-hashing
@app.route("/register", methods=["POST"])
def register():
    password = request.form.get("password", "")
    digest = hashlib.md5(password.encode()).hexdigest()
    return digest


# CWE-601: Open redirect -> py/url-redirection
@app.route("/go")
def go():
    from flask import redirect
    return redirect(request.args.get("next", "/"))


if __name__ == "__main__":
    # CWE-489/215: Debug mode enabled -> py/flask-debug
    app.run(debug=True, host="0.0.0.0")
