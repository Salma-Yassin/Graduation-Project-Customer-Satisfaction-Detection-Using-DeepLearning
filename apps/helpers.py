import cv2
from apps import app
from io import BytesIO
from google.oauth2 import service_account
#from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError
#from googleapiclient.http import MediaIoBaseUpload,MediaFileUpload

# def write_video_drive(url, output_folder_id, output_video_name , emotion):
#     # set up Google Drive API credentials
#     creds = service_account.Credentials.from_service_account_file('path/to/credentials.json')
#     drive_service = build('drive', 'v3', credentials=creds)
    
#     # create a VideoCapture object from the URL
#     cap = cv2.VideoCapture(url)
#     print(cap.isOpened()) # add this line after line 20 

#     # create the output video file on Google Drive
#     file_metadata = {'name': output_video_name, 'parents': [output_folder_id]}
#     media = MediaFileUpload(output_video_name, mimetype='video/mp4')
#     output_video = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

#     # loop through the frames of the video
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print('finished')
#             break

#         # write the variable on top of the frame
#         cv2.putText(frame, f"Detected: {emotion}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

#         # write the modified frame to the output video
#         success, encoded_image = cv2.imencode('.jpg', frame)
#         media = MediaIoBaseUpload(BytesIO(encoded_image.tobytes()), mimetype='video/mp4')
#         update = drive_service.files().update(fileId=output_video['id'], media_body=media, fields='id').execute()
#         print('1')

#     # release the resources
#     cap.release()
#     cv2.destroyAllWindows()

def sorting_audio(category):
    # sorted_audio = {'hap' , 'sad', 'neu', 'ang'}
    sorted_result = {}
    for item in category:
        sorted_result[item['label']] = item['score']

    sorted_result = {'hap': sorted_result['hap'], 'sad': sorted_result['sad'], 'neu': sorted_result['neu'], 'ang': sorted_result['ang']}
    return sorted_result

def overall_result(body_results, face_results, audio_results):
    categories = {'Happy': 0, 'Sad': 0, 'Fearful': 0, 'Neutral': 0, 'Angry': 0}

    for emotion in categories:
        e1 = face_results[emotion]
        e2 = body_results[emotion]

        if emotion == 'Happy':
            e3 = audio_results['hap']
        elif emotion == 'Sad':
            e3 = audio_results['sad']
        elif emotion == 'Neutral':
            e3 = audio_results['neu']
        elif emotion == 'Angry':
            e3 = audio_results['ang']
        else:
            e3 = 0
        avg =(e1+e2+e3)/3
        categories[emotion] = avg
    return categories



def summerize_video_body(in_category):
  
    summerized_categories = {'Happy': ['Engagement', 'Pleasure', 'Affection', 'Happiness', 'Esteem','Excitement', 'Surprise'],
                'Sad': ['Annoyance', 'Aversion', 'Sadness', 'Sensitivity', 'Suffering', 'Pain', 'Sympathy', 'Fatigue'],
                'Fearful': ['Disquietment', 'Doubt_Confusion', 'Fear'],
                'Neutral': ['Embarrassment', 'Peace', 'Yearning', 'Anticipation'],
                'Angry': ['Disapproval', 'Disconnection']}

    mapped_results = {}

    for category, emotions in summerized_categories.items():
        total_score = 0
        for emotion in emotions:
            total_score += in_category.get(emotion, 0)
        mapped_results[category] = total_score
    return mapped_results


def sorting_video_face(in_category):
    # sorted_audio = {'hap' , 'sad', 'neu', 'ang'}
    sorted_result = {}
    
    new_categories = {'Happy': ['Happy', 'Surprised'],
                'Sad': ['Sad'],
                'Fearful': ['Fearful'],
                'Neutral': ['Neutral'],
                'Angry': ['Angry', 'Disgusted']}
    mapped_results = {}

    for category, emotions in new_categories.items():
        total_score = 0
        for emotion in emotions:
            total_score += in_category.get(emotion, 0)
        mapped_results[category] = total_score
    return mapped_results
    # for k,v in category.item:
    #     sorted_result[k] = v

    # sorted_result = {'Happy': category['Happy'], 'Sad': category['Sad'], 'Fearful': category['Fearful'], 'Neutral': category['Neutral'], 'Angry': category['Angry'], 'Disgusted': category['Disgusted'],'Surprised': category['Surprised'] }
    # return sorted_result

def unify_audio(result):
    if (result == 'hap'):
        unified_result = 'Satisfied'
    elif(result == 'neu'):
        unified_result = 'Neutral'
    else:
        unified_result = 'Unsatisfied'
    return unified_result

##{"Happy": 186, "Neutral": 104, "Fearful": 33, "Angry": 15, "Sad": 6, "Disgusted": 0, "Surprised": 0}
def unify_video(result):
    if (result == 'Happy'):
        unified_result = 'Satisfied'
    elif(result == 'Neutral'):
        unified_result = 'Neutral'
    else:
        unified_result = 'Unsatisfied'
    return unified_result

def normalize_dict(d):
    total_sum = sum(d.values())
    normalized_dict = {}
    for k, v in d.items():
        normalized_dict[k] = v / total_sum
    return normalized_dict
