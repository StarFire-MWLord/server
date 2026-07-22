from flask import Flask, request, jsonify, Response
import requests
import json
import os

app = Flask(__name__)

auth_config = {"token": "", "refresh": ""}
try:
    with open("sem.json", "r", encoding="utf-8") as f:
        auth_config = json.load(f)
    print("✅ Loaded real bearer token")
except Exception as e:
    print("⚠️ Token error:", e)

REAL_BACKEND = "https://animalcompany.us-east1.nakamacloud.io"
HEADERS = {"Authorization": f"Bearer {auth_config.get('token')}" if auth_config.get('token') else None}

def real_get(endpoint):
    try:
        r = requests.get(f"{REAL_BACKEND}{endpoint}", headers=HEADERS, timeout=10)
        return r.json() if r.ok else {"success": False}
    except:
        return {"success": False}

@app.route('/health')
def health():
    return "OK"

@app.route('/v2/ANFCOASNOIODSNVOISDAHVOD', methods=['GET', 'POST'])
def custom_auth():
    print("[AUTH] Processing full login sequence")
    # Trigger key endpoints
    real_get("/v2/account")
    real_get("/v2/rpc/mining.balance")
    real_get("/v2/rpc/fishing.getWallet")
    real_get("/v2/rpc/nuts.getWallet")
    real_get("/v2/rpc/purchase.list")
    real_get("/v2/rpc/user.getFeatureFlags")
    real_get("/v2/rpc/clientBootstrap")

    return jsonify({
        "success": True,
        "user": {
            "id": "e6e488cf-79e1-48ed-8008-2829065eaf73",
            "username": "StandalonePlayer",
            "display_name": "StandalonePlayer",
            "steam_id": "76561199677913646"
        },
        "token": auth_config.get("token"),
        "refreshToken": auth_config.get("refresh")
    })

@app.route('/v2/<path:path>', methods=['GET', 'POST', 'PUT'])
def proxy_v2(path):
    url = f"{REAL_BACKEND}/v2/{path}"
    print(f"[PROXY] {request.method} /v2/{path}")
    
    headers = dict(request.headers)
    headers.pop("Host", None)
    if auth_config.get("token"):
        headers["Authorization"] = f"Bearer {auth_config.get('token')}"

    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            timeout=12
        )
        return Response(resp.content, resp.status_code, list(resp.headers.items()))
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 502

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Full Data Fetch Proxy running on port {port}")
    app.run(host='0.0.0.0', port=port)
