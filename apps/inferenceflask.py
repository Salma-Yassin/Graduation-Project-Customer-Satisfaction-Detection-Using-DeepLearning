import requests
from apps import app
from .TestEmotionDetector import predictEmotionFace
from .yolo_inference import functionpaths_image
from .yolo_inference import functionpaths_video
import json
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
@app.route('/face_inference')
def query_body(file_url):
    # cont = requests.get(file_url, verify= False)
    emotion=functionpaths_video(file_url)
    emotion=sorted(emotion.items(), key=lambda x:x[1],reverse=True)
    output=json.dumps(emotion,indent=4)
    return output