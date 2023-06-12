from yolo_inference import functionpaths_image
from yolo_inference import functionpaths_video
import yolo_inference
from emotic import Emotic
import re
import json


videopath="https://drive.google.com/file/d/13foVA6zIzSDdo1oQG-VnlvAeyWFhLhMH/view"

imagepath=r"C:\Users\Dell\Desktop\emotic\inferlist.txt"
emotion=functionpaths_video(videopath)
emotion=sorted(emotion.items(), key=lambda x:x[1],reverse=True)
output=json.dumps(emotion,indent=4)
#url
#json object sorted with probabilties
#branch
print(output)
#emotion=functionpaths_image(imagepath)

