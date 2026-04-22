from flask import Flask, render_template, request, jsonify, Response
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("QR_API_KEY", "secret:qr.repairsolutions.com:1b1da:ac68125cf702df4afbb860031be954b5")
API_BASE = "https://api.qrpci.com"


def api_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/folders")
def get_folders():
    """Fetch the list of folders from the QR API to populate the dropdown."""
    try:
        resp = requests.get(f"{API_BASE}/api/v2/folders", headers=api_headers(), timeout=10)
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/create-qr", methods=["POST"])
def create_qr():
    """Create a new QR code via the API."""
    try:
        data = request.json

        payload = {"target_url": data["target_url"]}

        if data.get("title"):
            payload["title"] = data["title"]
        if data.get("medium"):
            payload["medium"] = data["medium"]
        if data.get("folder_id"):
            payload["folder_id"] = data["folder_id"]

        resp = requests.post(
            f"{API_BASE}/api/v2/qrcodes",
            json=payload,
            headers=api_headers(),
            timeout=15
        )
        return jsonify(resp.json()), resp.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/download-qr/<code>")
def download_qr(code):
    """Proxy the QR code image from the API so the browser can display/download it."""
    try:
        resp = requests.get(
            f"{API_BASE}/api/v2/qrcodes/{code}/download-image/basic",
            headers=api_headers(),
            timeout=15
        )
        return Response(
            resp.content,
            mimetype=resp.headers.get("Content-Type", "image/png")
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
