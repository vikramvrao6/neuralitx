from flask import Flask
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "neuralitx-dev-key")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
DB_DIR = os.path.join(BASE_DIR, 'database')
DB_PATH = os.path.join(DB_DIR, 'neuralitx.db')
SCHEMA_PATH = os.path.join(DB_DIR, 'schema.sql')

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

init_db()

@app.after_request
def add_headers(response):
    response.headers['Content-Security-Policy'] = "frame-src *; default-src * 'unsafe-inline' 'unsafe-eval'"
    return response

from routes.main import main_bp
from routes.analysis import analysis_bp
from routes.auth import auth_bp

app.register_blueprint(main_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)