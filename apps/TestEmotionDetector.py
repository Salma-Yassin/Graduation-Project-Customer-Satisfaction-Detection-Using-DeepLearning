import cv2
import numpy as np
from keras.models import model_from_json
import re

def extractIDfromURL(url):
    
    id_regex = r"/d/(\w+)/"
    match = re.search(id_regex, url)
    
    if match:
        id = match.group(1)
        return id
    else:
        print("No id found in URL")
        return 0

def predictEmotionFace(url_base):
     

    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    emotion_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    # load json and create model
    json_file = open('apps/model/emotion_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    emotion_model = model_from_json(loaded_model_json)

    # load weights into new model
    emotion_model.load_weights("apps/model/emotion_model.h5")
    print("Loaded model from disk")

    id = extractIDfromURL(url_base)
    # start the webcam feed
    url = "https://drive.google.com/uc?id=" + id
    print(url)

    # Open the video file using OpenCV
    cap = cv2.VideoCapture(url)
    print(cap.isOpened()) # add this line after line 20  

    while True:
        # Find haar cascade to draw bounding box around face
        ret, frame = cap.read()
        
        # check if video file is being read correctly
        if not ret:
            break

        # check if video frame dimensions are not zero
        if frame.shape[0] == 0 or frame.shape[1] == 0:
            continue

        # resize the video frame
        frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_LINEAR)

        face_detector = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces available on camera
        num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        # take each face available on the camera and Preprocess it
        for (x, y, w, h) in num_faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

            # predict the emotions
            emotion_prediction = emotion_model.predict(cropped_img)
            maxindex = int(np.argmax(emotion_prediction))
            emotion_counts[maxindex] += 1
            # cv2.putText(frame, emotion_dict[maxindex], (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            # output_file.write(frame)
            # cv2.imshow('Emotion Detection', frame)
            #print('showed')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    dominant_emotion = max(emotion_counts, key=emotion_counts.get)
    print("Dominant emotion: ", emotion_dict[dominant_emotion])
    print(emotion_counts)


    # get the frame width and height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # create a VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter('output_video_6.mp4', fourcc, 30, (frame_width, frame_height))

    cap = cv2.VideoCapture(url)
    print(cap.isOpened()) # add this line after line 20 

    # loop through the frames of the video
    while True:
        ret, frame = cap.read()
        if not ret:
            print('finished')
            break

        # write the variable on top of the frame

        cv2.putText(frame, f"Detected: {emotion_dict[dominant_emotion]}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # write the modified frame to the output video
        output_video.write(frame)
        print('1')

    # release the resources
    cap.release()
    output_video.release()
    cv2.destroyAllWindows()

    return emotion_dict[dominant_emotion]
