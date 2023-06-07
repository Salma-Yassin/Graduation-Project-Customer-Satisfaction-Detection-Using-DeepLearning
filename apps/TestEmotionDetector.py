import cv2
import numpy as np
from keras.models import model_from_json
import re

def extractIDfromURL(url):
    
    id_regex = r'/d/([-\w]+)'
    match = re.search(id_regex, url)
    
    if match:
        id = match.group(1)
        return id
    else:
        print("No id found in URL")
        return 0

def predictEmotionFace(url_base, flag):
     

    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    emotion_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    frame_dict = {}
    c = 0

    # load json and create model
    json_file = open('apps/model/emotion_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    emotion_model = model_from_json(loaded_model_json)

    # load weights into new model
    emotion_model.load_weights("apps/model/emotion_model.h5")
    print("Loaded model from disk")

    if (flag == 'url'):
        id = extractIDfromURL(url_base)
        # start the webcam feed
        url = "https://drive.google.com/uc?id=" + id
        print(url)
        file =url
    elif(flag == 'local'):
        file = url_base

    # Open the video file using OpenCV
    # url ="videoplayback_Trim.mp4"
    cap = cv2.VideoCapture(file)
    print(cap.isOpened()) # add this line after line 20  

    #fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #output_file = cv2.VideoWriter("Results/intermediate_results.mp4", fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

    while True:
        # Find haar cascade to draw bounding box around face
        ret, frame = cap.read()
        
        # check if video file is being read correctly
        if not ret:
            break

        # check if video frame dimensions are not zero
        if frame.shape[0] == 0 or frame.shape[1] == 0:
            continue
        else:
            c = c + 1

        # resize the video frame
        frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_LINEAR)

        face_detector = cv2.CascadeClassifier('apps/haarcascades/haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces available on camera
        num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        # take each face available on the camera and Preprocess it
        for (x, y, w, h) in num_faces:
            # cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
           
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

            # predict the emotions
            emotion_prediction = emotion_model.predict(cropped_img)
            maxindex = int(np.argmax(emotion_prediction))
            emotion_counts[maxindex] += 1

            #cv2.putText(frame, emotion_dict[maxindex], (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            #output_file.write(frame)
            frame_dict[c] = []
            frame_dict[c].append(((x, y-50) , (x+w, y+h+10) , emotion_dict[maxindex],(x+5, y-20)))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    

    dominant_emotion = max(emotion_counts, key=emotion_counts.get)
    print("Dominant emotion: ", emotion_dict[dominant_emotion])
    print(emotion_counts)
    cap.release()
    #print(frame_dict)
    #output_file.release()
    #cv2.destroyAllWindows()

    cap = cv2.VideoCapture(file)
    print(cap.isOpened()) # add this line after line 20 
    c = 0

    # get the frame width and height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # create a VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter("Results/output_video_6.mp4", fourcc, 30, (frame_width, frame_height))

    # loop through the frames of the video
    while True:
        ret, frame = cap.read()
        if not ret:
            print('finished')
            break

        # check if video frame dimensions are not zero
        if frame.shape[0] == 0 or frame.shape[1] == 0:
            continue
        else:
            c = c + 1

        # write the variable on top of the frame

        cv2.putText(frame, f"Detected: {emotion_dict[dominant_emotion]}", (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

         # resize the video frame
        frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_LINEAR)

        try:
            for i in range(len(frame_dict[c])):
                cv2.rectangle(frame, frame_dict[c][i][0], frame_dict[c][i][1], (0, 255, 0), 4)
                cv2.putText(frame, frame_dict[c][i][2],  frame_dict[c][i][3], cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        except:
            print(c)


        # write the modified frame to the output video
        frame = cv2.resize(frame, (frame_width , frame_height), interpolation=cv2.INTER_LINEAR)
        output_video.write(frame)
        print('1')

    # release the resources
    cap.release()
    output_video.release()
    cv2.destroyAllWindows()
    
    emotionOutputDict = {} 
    for key in emotion_dict.keys():
        emotionOutputDict[emotion_dict[key]] = emotion_counts[key]

    # print(emotionOutputDict)
    sorted_dict = dict(sorted(emotionOutputDict.items(), key=lambda x: x[1], reverse=True))
    return sorted_dict

    # return emotion_dict[dominant_emotion]


#url_base = "https://drive.google.com/file/d/1WYaqDPMIM426y3ZU5y_HH6f4aUVV_XA1/view"
#predictEmotionFace(url_base)