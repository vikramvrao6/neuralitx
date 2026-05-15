from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "neuralitx-dev-key")

os.makedirs('uploads', exist_ok=True)
os.makedirs('database', exist_ok=True)

import sqlite3
def init_db():
    conn = sqlite3.connect('database/neuralytic.db')
    conn.executescript(open('database/schema.sql').read())
    conn.commit()
    conn.close()

init_db()

@app.after_request
def add_headers(response):
    response.headers['Content-Security-Policy'] = "frame-src *; default-src * 'unsafe-inline' 'unsafe-eval'"
    return response

# Register blueprints
from routes.main import main_bp
from routes.analysis import analysis_bp
from routes.auth import auth_bp

app.register_blueprint(main_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)