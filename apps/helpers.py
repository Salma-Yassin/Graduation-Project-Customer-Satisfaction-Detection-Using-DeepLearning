import cv2
from io import BytesIO
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload,MediaFileUpload

def write_video_drive(url, output_folder_id, output_video_name , emotion):
    # set up Google Drive API credentials
    creds = service_account.Credentials.from_service_account_file('path/to/credentials.json')
    drive_service = build('drive', 'v3', credentials=creds)
    
    # create a VideoCapture object from the URL
    cap = cv2.VideoCapture(url)
    print(cap.isOpened()) # add this line after line 20 

    # create the output video file on Google Drive
    file_metadata = {'name': output_video_name, 'parents': [output_folder_id]}
    media = MediaFileUpload(output_video_name, mimetype='video/mp4')
    output_video = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # loop through the frames of the video
    while True:
        ret, frame = cap.read()
        if not ret:
            print('finished')
            break

        # write the variable on top of the frame
        cv2.putText(frame, f"Detected: {emotion}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # write the modified frame to the output video
        success, encoded_image = cv2.imencode('.jpg', frame)
        media = MediaIoBaseUpload(BytesIO(encoded_image.tobytes()), mimetype='video/mp4')
        update = drive_service.files().update(fileId=output_video['id'], media_body=media, fields='id').execute()
        print('1')

    # release the resources
    cap.release()
    cv2.destroyAllWindows()
