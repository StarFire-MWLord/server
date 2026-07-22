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
except:
    print("⚠️ Using dummy token")
    auth_config = {"token": "dummy-steam-token-for-quest", "refresh": "dummy-refresh"}

@app.route('/health')
def health():
    return "OK"

# Main Auth
@app.route('/v2/ANFCOASNOIODSNVOISDAHVOD', methods=['GET', 'POST'])
def authenticate():
    print("[AUTH] Main login")
    return jsonify({
        "success": True,
        "user": {
            "id": "e6e488cf-79e1-48ed-8008-2829065eaf73",
            "username": "StandalonePlayer",
            "display_name": "StandalonePlayer",
            "steam_id": "76561199677913646"
        },
        "token": auth_config.get("token"),
        "refreshToken": auth_config.get("refresh"),
        "expiresIn": 7200
    })

# All other /v2/ endpoints
@app.route('/v2/<path:path>', methods=['GET', 'POST'])
def v2_routes(path):
    print(f"[V2] {request.method} /v2/{path}")
    if "account" in path:
        return jsonify({
            "success": True,
            "user": {
                "id": "e6e488cf-79e1-48ed-8008-2829065eaf73",
                "username": "StandalonePlayer",
                "display_name": "StandalonePlayer",
                "steam_id": "76561199677913646"
            }
        })
    elif "mining.balance" in path or "wallet" in path:
        return jsonify({"success": True, "balance": 9999})
    elif "purchase" in path or "rpc" in path:
        return jsonify({"success": True})
    elif "storage" in path:
        return jsonify({"success": True, "data": []})
    else:
        return jsonify({"success": True})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print(f"[FALLBACK] {request.method} {request.url}")
    return jsonify({"success": True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Comprehensive Backend running on port {port}")
    app.run(host='0.0.0.0', port=port)
