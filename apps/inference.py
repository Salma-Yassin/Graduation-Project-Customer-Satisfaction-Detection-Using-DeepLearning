import requests
from apps import app
from .TestEmotionDetector import predictEmotionFace

API_URL = "https://api-inference.huggingface.co/models/superb/hubert-large-superb-er"
headers = {"Authorization": "Bearer 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"}

@app.route('/tone_inference')
def query(file_url):
    cont = requests.get(file_url, verify= False)
    response = requests.post(API_URL, headers=headers, data=cont, verify= False).json()
    
    return response


@app.route('/face_inference')
def query_face(file_url):
    # cont = requests.get(file_url, verify= False)
    response = predictEmotionFace(file_url)
    return response

@app.route('/tone_inferenceLocal')
def queryLocal(file):
    with open(file, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers = headers, data = data).json()
    return response


#@app.route('/tone_inference')
#def query(file_url):
#    cont = requests.get(file_url, verify= False)
#    response = requests.post(API_URL, headers=headers, data=cont, verify= False).json()
    
#    return response[0]['label']
