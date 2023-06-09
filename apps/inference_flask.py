import requests
from apps import app
from .TestEmotionDetector import predictEmotionFace
from .yolo_inference import functionpaths_image, functionpaths_video
import json
import emotic

API_URL = "https://api-inference.huggingface.co/models/superb/hubert-large-superb-er"
headers = {"Authorization": "Bearer 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"}


@app.route('/tone_inference')
def query(file_url):
    cont = requests.get(file_url, verify=False)
    response = requests.post(API_URL, headers=headers,
                             data=cont, verify=False).json()

    return response




@app.route('/face_inference')
def query_face(file_url,flag):
    # cont = requests.get(file_url, verify= False)
    response = predictEmotionFace(file_url,flag)
    return response


@app.route('/body_video_inference')
def query_body_video(video_path,name):
    # cont = requests.get(file_url, verify= False)
    emotion = functionpaths_video(video_path,name)
    emotion = sorted(emotion.items(), key=lambda x: x[1], reverse=True)
    output = json.dumps(emotion, indent=4)
    return output


@app.route('/body_image_inference')
def query_body_image(image_txt_path):
    # cont = requests.get(file_url, verify= False)
    emotion = functionpaths_image(image_txt_path)
    emotion = sorted(emotion.items(), key=lambda x: x[1], reverse=True)
    output = json.dumps(emotion, indent=4)
    return output


@app.route('/tone_inferenceLocal')
def queryLocal(file):
    with open(file, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data).json()
    return response

# @app.route('/tone_inference')
# def query(file_url):
#    cont = requests.get(file_url, verify= False)
#    response = requests.post(API_URL, headers=headers, data=cont, verify= False).json()

#    return response[0]['label']
