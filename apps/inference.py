import requests
from apps import app

API_URL = "https://api-inference.huggingface.co/models/superb/hubert-large-superb-er"
headers = {"Authorization": "Bearer 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"}

@app.route('/tone_inference')
def query(file_url):
    cont = requests.get(file_url, verify= False)
    response = requests.post(API_URL, headers=headers, data=cont, verify= False)
    
    return response.json()

#@app.route('/tone_inference')
#def query(file_url):
#    cont = requests.get(file_url, verify= False)
#    response = requests.post(API_URL, headers=headers, data=cont, verify= False).json()
    
#    return response[0]['label']