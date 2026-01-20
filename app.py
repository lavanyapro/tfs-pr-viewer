from flask import Flask, jsonify, render_template
import requests
import base64
import os

app = Flask(__name__)

ORGANIZATION = "your_org"
PROJECT = "your_project"
REPOSITORY_ID = "your_repo_id"

PAT = os.getenv("AZURE_DEVOPS_PAT")
if not PAT:
    raise Exception("AZURE_DEVOPS_PAT environment variable not set")

API_URL = f"https://dev.azure.com/{ORGANIZATION}/{PROJECT}/_apis/git/repositories/{REPOSITORY_ID}/pullrequests?api-version=7.0"

auth_token = base64.b64encode(f":{PAT}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {auth_token}",
    "Content-Type": "application/json"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/pullrequests")
def pull_requests():
    response = requests.get(API_URL, headers=HEADERS)
    data = response.json()

    prs = []
    for pr in data.get("value", []):
        prs.append({
            "id": pr["pullRequestId"],
            "title": pr["title"],
            "status": pr["status"],
            "createdBy": pr["createdBy"]["displayName"]
        })

    return jsonify(prs)

if __name__ == "__main__":
    app.run(debug=True)
