from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Load your tokens
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

# Main Auth Endpoint (matches the weird path in your script)
@app.route('/v2/ANFCOASNOIODSNVOISDAHVOD', methods=['GET', 'POST'])
def authenticate():
    print(f"[AUTH] Request received")
    
    return jsonify({
        "success": True,
        "user": {
            "id": "e6e488cf-79e1-48ed-8008-2829065eaf73",
            "username": "2c0C8oZtCtj5WWeE",
            "display_name": "John",
            "lang_tag": "en",
            "metadata": "{}",
            "steam_id": "76561199677913646",
            "edge_count": 115,
            "create_time": "2026-07-01T00:44:47Z",
            "update_time": "2026-07-22T00:00:00Z"
        },
        "token": auth_config.get("token"),
        "refreshToken": auth_config.get("refresh"),
        "expiresIn": 7200,
        "wallet": "{\"hardCurrency\": 999, \"researchPoints\": 999}"
    })

# General Account Endpoints
@app.route('/v2/account', methods=['GET', 'POST'])
@app.route('/v2/account/<path:path>', methods=['GET', 'POST'])
def account(path=""):
    print(f"[ACCOUNT] {request.method} /v2/account/{path}")
    return jsonify({
        "user": {
            "id": "e6e488cf-79e1-48ed-8008-2829065eaf73",
            "username": "2c0C8oZtCtj5WWeE",
            "display_name": "John",
            "steam_id": "76561199677913646"
        },
        "wallet": "{\"hardCurrency\": 999, \"researchPoints\": 999}"
    })

# Catch-all for other calls
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print(f"[FALLBACK] {request.method} {request.url}")
    return jsonify({"success": True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Backend running on port {port}")
    app.run(host='0.0.0.0', port=port)
