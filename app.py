from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Load sem.json or fallback
auth_config = {"token": "", "refresh": ""}
try:
    with open("sem.json", "r", encoding="utf-8") as f:
        auth_config = json.load(f)
    print("✅ Loaded sem.json")
except:
    print("⚠️ sem.json not found - using dummy")
    auth_config = {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy-standalone-token", "refresh": "dummy-refresh"}

@app.route('/health')
def health():
    return "OK"

# Primary Auth Endpoint
@app.route('/v2/ANFCOASNOIODSNVOISDAHVOD', methods=['GET', 'POST'])
def authenticate():
    print(f"[AUTH] MetaQuest/Steam Auth Request")
    return jsonify({
        "success": True,
        "user": {
            "id": "e6e488cf-79e1-48ed-8008-2829065eaf73",
            "username": "StandalonePlayer",
            "displayName": "StandalonePlayer",
            "platform": "MetaQuest",
            "metaId": "meta-dummy-12345",
            "steamId": "76561199677913646"
        },
        "token": auth_config.get("token"),
        "refreshToken": auth_config.get("refresh"),
        "expiresIn": 7200,
        "metaQuestToken": "FRLAegi7gTVyLg9rv04b35edKMZC2J4zbuDuiCOAZAyyTqFZA2zAHgjgAQ0JrfgZBXLe9evvQgS0qr3Oh9ZBWMKD2DjcZAS4CsFiriLgumYLP1ldUZAqYMZBK9HWnokbA8NO1CZB2wpF5QZDZD",
        "account": {
            "id": "e6e488cf-79e1-48ed-8008-2829065eaf73",
            "status": "active",
            "verified": True
        }
    })

# General Account Requests
@app.route('/v2/account', methods=['GET', 'POST'])
@app.route('/v2/account/<path:path>', methods=['GET', 'POST'])
def account(path=""):
    print(f"[ACCOUNT] {request.method} /v2/account/{path}")
    return jsonify({
        "success": True,
        "user": {
            "id": "e6e488cf-79e1-48ed-8008-2829065eaf73",
            "username": "StandalonePlayer",
            "displayName": "StandalonePlayer",
            "steamId": "76561199677913646"
        },
        "wallet": "{\"hardCurrency\": 9999, \"researchPoints\": 999}"
    })

# Catch everything else
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print(f"[FALLBACK] {request.method} {request.url}")
    return jsonify({"success": True, "message": "handled"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Backend running on port {port}")
    app.run(host='0.0.0.0', port=port)
