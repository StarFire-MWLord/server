from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Load tokens from sem.json
auth_config = {"token": "", "refresh": ""}

sem_path = os.path.join(os.path.dirname(__file__), "sem.json")

try:
    with open(sem_path, "r", encoding="utf-8") as f:
        auth_config = json.load(f)
    print("✅ Loaded sem.json")
except Exception as e:
    print(f"❌ Could not load sem.json: {e}")

# Base success response
def success_response():
    return {
        "success": True,
        "user": {
            "id": "python-standalone-user",
            "username": "StandalonePlayer",
            "displayName": "Python Backend User"
        },
        "token": auth_config.get("token"),
        "refreshToken": auth_config.get("refresh"),
        "expiresIn": 7200
    }

@app.route('/health')
def health():
    return "OK", 200

@app.route('/v2/account/authenticate', methods=['GET', 'POST'])
def authenticate():
    print(f"[AUTH] {request.method} {request.url}")
    return jsonify(success_response())

@app.route('/v2/account/<path:path>', methods=['GET', 'POST', 'PUT'])
def account_routes(path):
    print(f"[ACCOUNT] {request.method} /v2/account/{path}")
    return jsonify({
        "success": True,
        **success_response()["user"],
        "data": {"status": "ok"}
    })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print(f"[FALLBACK] {request.method} {request.url}")
    return jsonify({"success": True, "message": "handled by python backend"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Python Animal Company Backend running on port {port}")
    app.run(host='0.0.0.0', port=port)
