from flask import Flask, request, jsonify, Response
import requests
import json
import os

app = Flask(__name__)

# Load your real tokens
auth_config = {"token": "", "refresh": ""}
try:
    with open("sem.json", "r", encoding="utf-8") as f:
        auth_config = json.load(f)
    print("✅ Loaded real Steam tokens from sem.json")
except:
    print("⚠️ sem.json not found - add it to Render")
    auth_config = {"token": "", "refresh": ""}

REAL_BACKEND = "https://animalcompany.us-east1.nakamacloud.io"

@app.route('/health')
def health():
    return "Proxy OK"

# Special Auth Endpoint
@app.route('/v2/ANFCOASNOIODSNVOISDAHVOD', methods=['GET', 'POST'])
def custom_auth():
    print("[PROXY] Handling custom auth")
    # Forward to real Steam auth
    url = f"{REAL_BACKEND}/v2/account/authenticate/steam?create=true&sync=false"
    headers = {
        "Authorization": f"Bearer {auth_config.get('token')}",
        "Content-Type": "application/json"
    }
    try:
        resp = requests.post(url, headers=headers, json=request.json if request.is_json else None, timeout=10)
        return Response(resp.content, resp.status_code, resp.headers.items())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Proxy all other /v2/ requests
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
            cookies=request.cookies,
            timeout=15
        )
        return Response(resp.content, resp.status_code, resp.headers.items())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 502

# Catch-all
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print(f"[FALLBACK] {request.method} {request.url}")
    return jsonify({"success": True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Real Proxy Backend running on port {port}")
    app.run(host='0.0.0.0', port=port)
