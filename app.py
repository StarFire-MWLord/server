from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Load tokens
auth_config = {"token": "", "refresh": ""}
try:
    with open("sem.json", "r", encoding="utf-8") as f:
        auth_config = json.load(f)
    print("✅ Loaded sem.json")
except Exception as e:
    print(f"❌ sem.json error: {e}")

@app.route('/health')
def health():
    return "OK"

@app.route('/v2/ANFCOASNOIODSNVOISDAHVOD', methods=['GET', 'POST'])
def authenticate():
    print(f"[AUTH] Received request")
    return jsonify({
        "success": True,
        "user": {
            "id": "quest-user",
            "username": "StandalonePlayer",
            "displayName": "Standalone",
            "platform": "MetaQuest"
        },
        "token": auth_config.get("token"),
        "refreshToken": auth_config.get("refresh"),
        "expiresIn": 7200,
        "metaQuestToken": "dummy-meta-token",
        "account": {
            "id": "quest-user",
            "status": "active"
        }
    })

@app.route('/v2/account', methods=['GET', 'POST'])
@app.route('/v2/account/<path:path>', methods=['GET', 'POST'])
def account(path=""):
    print(f"[ACCOUNT] {request.method} /v2/account/{path}")
    return jsonify({
        "success": True,
        "user": {
            "id": "quest-user",
            "username": "StandalonePlayer",
            "displayName": "Standalone"
        },
        "data": {"status": "ok"}
    })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print(f"[FALLBACK] {request.method} {request.url}")
    return jsonify({"success": True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Backend running on port {port}")
    app.run(host='0.0.0.0', port=port)
