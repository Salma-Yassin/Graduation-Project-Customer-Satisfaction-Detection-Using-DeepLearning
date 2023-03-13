import requests
from apps import app

API_URL = "https://api-inference.huggingface.co/models/superb/hubert-large-superb-er"
headers = {"Authorization": "Bearer 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"}

@app.route('/tone_inference')
def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()
