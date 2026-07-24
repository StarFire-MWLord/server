from flask import Flask, request, jsonify, send_file
import json
import os
import random
import string
import time
import sqlite3
import requests

app = Flask(__name__)

# === CONFIG ===
DISCORD_WEBHOOK = "https://ptb.discord.com/api/webhooks/1530322620543795371/0p2FF-bYrZztmkoIRMbJDSpTgm__r72Yg8s819LcNk8L48EGuq4eWdWSmh0RQXq8hrwR"  # Change or leave as is
DB_PATH = "userdata.db"

# Load sem.json if exists
auth_config = {"token": "", "refresh": ""}
try:
    with open("sem.json", "r", encoding="utf-8") as f:
        auth_config = json.load(f)
    print("✅ Loaded sem.json")
except:
    print("⚠️ sem.json not found")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        ip TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        custom_id TEXT NOT NULL,
        create_time REAL NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS banned_ips (
        ip TEXT PRIMARY KEY
    )''')
    conn.commit()
    conn.close()

init_db()

def get_or_create_user(ip):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM banned_ips WHERE ip = ?", (ip,))
    if cur.fetchone():
        conn.close()
        return None, True

    cur.execute("SELECT username, custom_id FROM users WHERE ip = ?", (ip,))
    result = cur.fetchone()
    if result:
        conn.close()
        return {"username": result[0], "custom_id": result[1]}, False
    else:
        username = "Xera+" + ''.join(random.choices(string.ascii_uppercase, k=6))
        custom_id = ''.join(random.choices(string.digits, k=17))
        cur.execute("INSERT INTO users (ip, username, custom_id, create_time) VALUES (?, ?, ?, ?)",
                    (ip, username, custom_id, time.time()))
        conn.commit()
        conn.close()
        return {"username": username, "custom_id": custom_id}, False

@app.route('/health')
def health():
    return "OK"

@app.route('/v2/account/authenticate/custom', methods=['GET','POST','PUT','DELETE','PATCH','OPTIONS'])
def custom_auth():
    return jsonify({
        "success": True,
        "token": auth_config.get("token"),
        "refresh_token": auth_config.get("refresh")
    })

@app.route('/v2/account', methods=['GET','PUT'])
def account():
    ip = request.remote_addr or "127.0.0.1"
    user, banned = get_or_create_user(ip)
    if banned or not user:
        return jsonify({"error": "banned"}), 403

    username = "XERA COMPANY"
    return jsonify({
        "user": {
            "id": "2e8aace0-282d-4c3d-b9d4-6a3b3ba2c2a6",
            "username": username,
            "lang_tag": "en",
            "edge_count": 4,
            "create_time": "2024-08-24T07:30:12Z",
            "update_time": "2025-04-05T21:00:27Z"
        },
        "wallet": '{"stashCols": 16, "stashRows": 8, "hardCurrency": 30000000, "softCurrency": 20000000, "researchPoints": 69420}',
        "custom_id": user["custom_id"]
    })

@app.route('/v2/rpc/<path:path>', methods=['GET','POST','PUT','DELETE','PATCH','OPTIONS'])
def rpc(path):
    print(f"[RPC] {path}")
    return jsonify({"success": True, "payload": {}})

@app.route('/v2/storage', methods=['GET','POST','PUT','DELETE','PATCH','OPTIONS'])
def storage():
    return jsonify({"objects": []})

@app.route('/v2/storage/econ_gameplay_items', methods=['GET','POST','PUT','DELETE','PATCH','OPTIONS'])
def econ_items():
    return jsonify({"payload": []})

@app.route('/game-data-prod.zip')
def game_data():
    try:
        return send_file("game-data-prod.zip", as_attachment=False)
    except:
        return "File not found", 404

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print(f"[FALLBACK] {request.method} {path}")
    return jsonify({"success": True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Backend running on port {port}")
    app.run(host='0.0.0.0', port=port)
