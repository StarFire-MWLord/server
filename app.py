from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Load tokens
auth_config = {"token": "", "refresh": ""}
sem_path = os.path.join(os.path.dirname(__file__), "sem.json")

try:
    with open(sem_path, "r", encoding="utf-8") as f:
        auth_config = json.load(f)
    print("✅ Loaded sem.json")
except Exception as e:
    print(f"❌ Could not load sem.json: {e}")

@app.route('/health')
def health():
    return "OK"

# Match the original weird authenticate endpoint
@app.route('/v2/ANFCOASNOIODSNVOISDAHVOD', methods=['GET', 'POST'])
def authenticate():
    print(f"[AUTH] {request.method} {request.url}")
    return jsonify({
        "success": True,
        "user": {
            "id": "standalone-user",
            "username": "Player",
            "displayName": "Standalone"
        },
        "token": auth_config.get("token"),
        "refreshToken": auth_config.get("refresh"),
        "expiresIn": 7200
    })

# General account routes
@app.route('/v2/account', methods=['GET', 'POST'])
@app.route('/v2/account/<path:path>', methods=['GET', 'POST'])
def account_routes(path=None):
    print(f"[ACCOUNT] {request.method} {request.url}")
    return jsonify({
        "success": True,
        "data": {"status": "ok"}
    })

# Catch all other requests
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print(f"[FALLBACK] {request.method} {request.url}")
    return jsonify({"success": True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Backend running on port {port}")
    app.run(host='0.0.0.0', port=port)
