import os
import pymysql
from flask import Flask

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Week 2: Python web application</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 700px; margin: 3rem auto; padding: 0 1rem; line-height: 1.6; }
    h1 { color: hotpink; }
  </style>
</head>
<body>
  <h1>Week 2: Python web application</h1>
  <p>This page runs with Flask behind Nginx.</p>
  <p>Page loads: <strong>{hits}</strong></p>
  <p>The counter is stored in a MariaDB database. Every page load increases the value by one.</p>
  <h2>Restart test</h2>
  <p>Test done and was succesfull</p>
  <p><a href="https://github.com/saarailtanen/linux_course_week2">Project source code on GitHub</a></p>
</body>
</html>"""

def get_db():
    return pymysql.connect(
        host="localhost",
        user="flaskuser",
        password=os.environ["DB_PASSWORD"],
        database="counterdb",
        autocommit=True,
    )

@app.route("/")
def index():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("UPDATE counter SET hits = hits + 1 WHERE id = 1")
        cur.execute("SELECT hits FROM counter WHERE id = 1")
        hits = cur.fetchone()[0]
    db.close()
    return PAGE.replace("{hits}", str(hits))

