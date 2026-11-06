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
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Quicksand:wght@500;700&display=swap');
    html { background: linear-gradient(160deg, #ffe4f1 0%, #ffc2e0 50%, #ffb0d4 100%); min-height: 100%; }
    body { font-family: 'Quicksand', Arial, sans-serif; color: #5a2a45; max-width: 700px; margin: 2.5rem auto; padding: 2rem 2.2rem; line-height: 1.7; background: rgba(255, 255, 255, 0.85); border-radius: 28px; box-shadow: 0 10px 35px rgba(255, 105, 180, 0.35); border: 3px solid #ffb6d9; }
    h1 { font-family: 'Pacifico', cursive; font-weight: normal; color: #ff3d9a; font-size: 2.4rem; text-shadow: 2px 2px 0 #ffd1e8; }
    h2 { color: #e0559c; border-bottom: 2px dotted #ffb6d9; padding-bottom: 4px; }
    strong { background: #ff69b4; color: white; padding: 2px 14px; border-radius: 999px; font-size: 1.1rem; }
    a { color: #d6247f; font-weight: 700; text-decoration: none; border-bottom: 2px solid #ffb6d9; }
    a:hover { background: #ffd1e8; border-radius: 6px; }

    .counter { background: #fff0f7; border: 3px dashed #ff69b4; border-radius: 20px; padding: 1rem 1.5rem; text-align: center; font-size: 1.1rem; box-shadow: 0 4px 14px rgba(255, 105, 180, 0.3); margin: 1.5rem 0; }
    .counter strong { display: block; background: none; color: #ff3d9a; font-family: 'Pacifico', cursive; font-weight: normal; font-size: 2.8rem; padding: 0; }
  
    .flow { text-align: center; font-weight: 700; color: #d6247f; background: #ffe4f1; border-radius: 999px; padding: 0.5rem 1rem; }
    .tech { background: #fff0f7; border-left: 8px solid #ff69b4; border-radius: 14px; padding: 0.4rem 1.2rem; margin: 1rem 0; }
    .tech h3 { color: #e0559c; margin-bottom: 0; }
  
    .test { background: #fff8fb; border: 1px solid #ffd1e8; border-radius: 12px; padding: 0.2rem 1.2rem 0.6rem; margin: 1.8rem 0; font-size: 0.95rem; }
    .test h2 { color: #e0559c; font-size: 1.1rem; border-bottom: none; margin-bottom: 0; }
    .test p { margin-top: 0.3rem; }
  </style>
</head>
<body>
  <h1>Week 2: Python web application</h1>
  <p>This page runs with Flask behind Nginx.</p>
  <div class="counter">Page loads<strong>{hits}</strong></div>
  <p>The counter is stored in a MariaDB database. Every page load increases the value by one.</p>
  <h2>How it works</h2>
  <p class="flow">Browser &rarr; Nginx &rarr; Gunicorn + Flask &rarr; MariaDB</p>
  <div class="tech">
    <h3>Nginx</h3>
    <p>Nginx is a web server and reverse proxy. It listens on port 80 and receives the requests from browsers. Instead of creating the page itself, it forwards the request to the Flask application and sends the answer back to the visitor. It also handles many connections at the same time very efficiently.</p>
  </div>
  <div class="tech">
    <h3>Flask</h3>
    <p>Flask is a lightweight Python web framework. My application is one Python file that runs as a systemd service with Gunicorn. On every page load it increases the counter in the database, reads the new value and builds this HTML page.</p>
  </div>
  <div class="tech">
    <h3>MariaDB</h3>
    <p>MariaDB is an open-source relational database, originally a fork of MySQL. It stores the page load counter in a table on the disk, so the value is not lost when the application or the whole server restarts. Flask connects to it with its own database user that only has access to this one database.</p>
  </div>

  <div class="test"><h2>Restart test</h2><p>Test done and was succesfull</p></div>
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

