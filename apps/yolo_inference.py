import argparse 
import cv2
import numpy as np 
import os 
import math
import torch 
from torchvision import transforms
import re
from emotic import Emotic 
from inference import infer
from yolo_utils import prepare_yolo, rescale_boxes, non_max_suppression
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu', type=int, default=0, help='gpu id')
    parser.add_argument('--experiment_path', type=str, default=r"C:\Users\Dell\Desktop\emotic\debug_exp", help='Path of experiment files (results, models, logs)')
    parser.add_argument('--model_dir', type=str, default='models', help='Folder to access the models')
    parser.add_argument('--result_dir', type=str, default='results', help='Path to save the results')
    parser.add_argument('--inference_file', type=str, help='Text file containing image context paths and bounding box')
    parser.add_argument('--video_file', type=str, help='Test video file')
    # Generate args
    args = parser.parse_args()
    return args


def get_bbox(yolo_model, device, image_context, yolo_image_size=416, conf_thresh=0.8, nms_thresh=0.4):
  ''' Use yolo to obtain bounding box of every person in context image. 
  :param yolo_model: Yolo model to obtain bounding box of every person in context image. 
  :param device: Torch device. Used to send tensors to GPU (if available) for faster processing. 
  :yolo_image_size: Input image size for yolo model. 
  :conf_thresh: Confidence threshold for yolo model. Predictions with object confidence > conf_thresh are returned. 
  :nms_thresh: Non-maximal suppression threshold for yolo model. Predictions with IoU > nms_thresh are returned. 
  :return: Numpy array of bounding boxes. Array shape = (no_of_persons, 4). 
  '''
  test_transform = transforms.Compose([transforms.ToPILImage(),transforms.ToTensor()])
  image_yolo = test_transform(cv2.resize(image_context, (416, 416))).unsqueeze(0).to(device)

  with torch.no_grad():
    detections = yolo_model(image_yolo)
    nms_det  = non_max_suppression(detections, conf_thresh, nms_thresh)[0]
    det = rescale_boxes(nms_det, yolo_image_size, (image_context.shape[:2]))
  
  bboxes = []
  for x1, y1, x2, y2, _, _, cls_pred in det:
    if cls_pred == 0:  # checking if predicted_class = persons. 
      x1 = int(min(image_context.shape[1], max(0, x1)))
      x2 = int(min(image_context.shape[1], max(x1, x2)))
      y1 = int(min(image_context.shape[0], max(15, y1)))
      y2 = int(min(image_context.shape[0], max(y1, y2)))
      bboxes.append([x1, y1, x2, y2])
  return np.array(bboxes)


def yolo_infer(images_list, result_path, model_path, context_norm, body_norm, ind2cat, ind2vad):
  ''' Infer on a list of images defined in images_list text file to obtain bounding boxes of persons in the images using yolo model.
  :param images_list: Text file specifying the images to conduct inference. A row in the file is Path_of_image. 
  :param result_path: Directory path to save the results (images with the predicted emotion categories and continuous emotion dimesnions).
  :param model_path: Directory path to load models and val_thresholds to perform inference.
  :param context_norm: List containing mean and std values for context images. 
  :param body_norm: List containing mean and std values for body images. 
  :param ind2cat: Dictionary converting integer index to categorical emotion. 
  :param ind2vad: Dictionary converting integer index to continuous emotion dimension (Valence, Arousal and Dominance).
  :param args: Runtime arguments.
  '''
  device = torch.device("cpu")
  yolo = prepare_yolo(model_path)
  yolo = yolo.to(device)
  yolo.eval()

  thresholds = torch.FloatTensor(np.load(os.path.join(result_path, 'val_thresholds.npy'))).to(device) 
  model_context = torch.load(os.path.join(model_path,'model_context1.pth')).to(device)
  model_body = torch.load(os.path.join(model_path,'model_body1.pth')).to(device)
  emotic_model = torch.load(os.path.join(model_path,'model_emotic1.pth')).to(device)
  models = [model_context, model_body, emotic_model]

  with open(images_list, 'r') as f:
    lines = f.readlines()
  result_file = os.path.join(result_path, 'inference_list.txt')
  with open(result_file, 'w') as f:
    pass

  dominant_emotion = dict()
  dominant_emotion_counter_neutral = 0
  dominant_emotion_counter_positive = 0
  dominant_emotion_counter_negative = 0


  for idx, line in enumerate(lines):
    image_context_path = line.split('\n')[0].split(' ')[0]
    image_context = cv2.cvtColor(cv2.imread(image_context_path), cv2.COLOR_BGR2RGB)
    try:
      bbox_yolo = get_bbox(yolo, device, image_context)
      for pred_bbox in bbox_yolo:
        pred_cat, pred_cont = infer(context_norm, body_norm, ind2cat, ind2vad, device, thresholds, models, image_context=image_context, bbox=pred_bbox, to_print=False)
        write_text_vad = list()
        for continuous in pred_cont:
          write_text_vad.append(str('%.1f' %(continuous)))
        write_text_vad = 'vad ' + ' '.join(write_text_vad) 
        image_context = cv2.rectangle(image_context, (pred_bbox[0], pred_bbox[1]),(pred_bbox[2] , pred_bbox[3]), (255, 0, 0), 3)
        height, width, _ = image_context.shape
        FONT_SCALE = 2e-3  # Adjust for larger font size in all images
        THICKNESS_SCALE = 1e-3
        cv2.putText(image_context, write_text_vad, (pred_bbox[0], pred_bbox[1] - 5), cv2.FONT_HERSHEY_PLAIN, fontScale=min(width, height) * FONT_SCALE,thickness=math.ceil(min(width, height) * THICKNESS_SCALE),color=(0, 0, 255))
        for i, emotion in enumerate(pred_cat):
          cv2.putText(image_context, emotion, (pred_bbox[0], pred_bbox[1] + (i+1)*12), cv2.FONT_HERSHEY_PLAIN,fontScale=min(width, height) * FONT_SCALE,thickness=math.ceil(min(width, height) * THICKNESS_SCALE),color=(0, 0, 255))


        write_line = list()
        write_line.append(image_context_path)
        for emotion in pred_cat:
          write_line.append(emotion)
          if emotion=="Neutral":
            dominant_emotion_counter_neutral = dominant_emotion_counter_neutral + 1
            dominant_emotion["Neutral"]=dominant_emotion_counter_neutral
          if emotion=="Positive":
            dominant_emotion_counter_positive = dominant_emotion_counter_positive + 1
            dominant_emotion["Positive"]=dominant_emotion_counter_positive
          if emotion=="Negative":
            dominant_emotion_counter_negative = dominant_emotion_counter_negative + 1
            dominant_emotion["Negative"]=dominant_emotion_counter_negative
        for continuous in pred_cont:
          write_line.append(str('%.4f' %(continuous)))
        write_line = ' '.join(write_line) 
        with open(result_file, 'a') as f:
          f.writelines(write_line)
          f.writelines('\n')


    except Exception as e:
      print ('Exception for image ',image_context_path)
      print (e)
    cv2.imwrite(os.path.join(result_path, 'img_%r.jpg' %(idx)), cv2.cvtColor(image_context, cv2.COLOR_RGB2BGR))
    print ('completed inference for image %d'  %(idx))

def extractIDfromURL(url):
  id_regex = r'/d/([-\w]+)'
  match = re.search(id_regex, url)

  if match:
    id = match.group(1)
    return id
  else:
    print("No id found in URL")
    return 0


def yolo_video(video_file, result_path, model_path, context_norm, body_norm, ind2cat, ind2vad):
  ''' Perform inference on a video. First yolo model is used to obtain bounding boxes of persons in every frame.
  After that the emotic model is used to obtain categoraical and continuous emotion predictions. 
  :param video_file: Path of video file. 
  :param result_path: Directory path to save the results (output video).
  :param model_path: Directory path to load models and val_thresholds to perform inference.
  :param context_norm: List containing mean and std values for context images. 
  :param body_norm: List containing mean and std values for body images. 
  :param ind2cat: Dictionary converting integer index to categorical emotion. 
  :param ind2vad: Dictionary converting integer index to continuous emotion dimension (Valence, Arousal and Dominance).
  :param args: Runtime arguments.
  '''  
  #device = torch.device("cuda:%s" %(str(args.gpu)) if torch.cuda.is_available() else "cpu")
  device = torch.device("cpu")
  yolo = prepare_yolo(model_path)
  yolo = yolo.to(device)
  yolo.eval()

  thresholds = torch.FloatTensor(np.load(os.path.join(result_path, 'val_thresholds.npy'))).to(device) 
  model_context = torch.load(os.path.join(model_path,'model_context1.pth')).to(device)
  model_body = torch.load(os.path.join(model_path,'model_body1.pth')).to(device)
  emotic_model = torch.load(os.path.join(model_path,'model_emotic1.pth')).to(device)
  model_context.eval()
  model_body.eval()
  emotic_model.eval()
  models = [model_context, model_body, emotic_model]


  id = extractIDfromURL(video_file)
  # start the webcam feed
  url = "https://drive.google.com/uc?id=" + id
  # print(url)

  # # Open the video file using OpenCV
  # cap = cv2.VideoCapture(url)
  #  # add this line after line 20


  video_stream = cv2.VideoCapture(url)
  print(video_stream.isOpened())
  writer = None
  result_file = os.path.join(result_path, 'inference_list.txt')
  with open(result_file, 'w') as f:
    pass
  print ('Starting testing on video')
  c=0
  dominant_emotion=dict()
  dominant_emotion_counter_neutral=0
  dominant_emotion_counter_positive=0
  dominant_emotion_counter_negative=0
  while True:
    (grabbed, frame) = video_stream.read()
    if not grabbed:
      break
    image_context = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    height, width, _ = image_context.shape
    FONT_SCALE = 2e-3  # Adjust for larger font size in all images
    THICKNESS_SCALE = 1e-3
    try: 
      bbox_yolo = get_bbox(yolo, device, image_context)
      for pred_idx, pred_bbox in enumerate(bbox_yolo):
        pred_cat, pred_cont = infer(context_norm, body_norm, ind2cat, ind2vad, device, thresholds, models, image_context=image_context, bbox=pred_bbox, to_print=False)
        write_text_vad = list()
        for continuous in pred_cont:
          write_text_vad.append(str('%.1f' %(continuous)))
        write_text_vad = 'vad ' + ' '.join(write_text_vad) 
        image_context = cv2.rectangle(image_context, (pred_bbox[0], pred_bbox[1]),(pred_bbox[2] , pred_bbox[3]), (255, 0, 0), 3)
        cv2.putText(image_context, write_text_vad, (pred_bbox[0], pred_bbox[1] - 5), cv2.FONT_HERSHEY_PLAIN, fontScale=min(width, height) * FONT_SCALE,thickness=math.ceil(min(width, height) * THICKNESS_SCALE),color=(0, 0, 255))
        for i, emotion in enumerate(pred_cat):
          cv2.putText(image_context, emotion, (pred_bbox[0], pred_bbox[1] + (i+1)*12), cv2.FONT_HERSHEY_PLAIN, fontScale=min(width, height) * FONT_SCALE,thickness=math.ceil(min(width, height) * THICKNESS_SCALE),color=(0, 0, 255))
        write_line = list()
        write_line.append('Frame'+str(c))
        for emotion in pred_cat:
          write_line.append(emotion)
          if emotion=="Neutral":
            dominant_emotion_counter_neutral = dominant_emotion_counter_neutral + 1
            dominant_emotion["Neutral"]=dominant_emotion_counter_neutral
          if emotion=="Positive":
            dominant_emotion_counter_positive = dominant_emotion_counter_positive + 1
            dominant_emotion["Positive"]=dominant_emotion_counter_positive
          if emotion=="Negative":
            dominant_emotion_counter_negative = dominant_emotion_counter_negative + 1
            dominant_emotion["Negative"]=dominant_emotion_counter_negative

        for continuous in pred_cont:
          write_line.append(str('%.4f' %(continuous)))
        write_line = ' '.join(write_line) 
        with open(result_file, 'a') as f:
          f.writelines(write_line)
          f.writelines('\n')
        c=c+1
    except Exception:
      c=c+1
      pass
    if writer is None:
      fourcc = cv2.VideoWriter_fourcc(*"MJPG")
      writer = cv2.VideoWriter(os.path.join(result_path, 'result_vid.avi'), fourcc, 30, (image_context.shape[1], image_context.shape[0]), True)  
    writer.write(cv2.cvtColor(image_context, cv2.COLOR_RGB2BGR))

  writer.release()
  video_stream.release() 
  print ('Completed video')
  return dominant_emotion


def check_paths(args):
  ''' Check (create if they don't exist) experiment directories.
  :param args: Runtime arguments as passed by the user.
  :return: result_dir_path, model_dir_path.
  '''
  if args.inference_file is not None: 
    if not os.path.exists(args.inference_file):
      raise ValueError('inference file does not exist. Please pass a valid inference file')
  if args.video_file is not None: 
    if not os.path.exists(args.video_file):
      raise ValueError('video file does not exist. Please pass a valid video file')
  if args.inference_file is None and args.video_file is None: 
    raise ValueError(' both inference file and video file can\'t be none. Please specify one and run again')
  model_path = os.path.join(args.experiment_path, args.model_dir)
  if not os.path.exists(model_path):
    raise ValueError('model path %s does not exist. Please pass a valid model_path' %(model_path))
  result_path = os.path.join(args.experiment_path, args.result_dir)
  if not os.path.exists(result_path):
    os.makedirs(result_path)
  return result_path, model_path

# if __name__=='__main__':
#   args = parse_args()
#
#   result_path, model_path = check_paths(args)

cat = ['Affection', 'Anger', 'Annoyance', 'Anticipation', 'Aversion', 'Confidence', 'Disapproval', 'Disconnection', \
          'Disquietment', 'Doubt/Confusion', 'Embarrassment', 'Engagement', 'Esteem', 'Excitement', 'Fatigue', 'Fear','Happiness', \
          'Pain', 'Peace', 'Pleasure', 'Sadness', 'Sensitivity', 'Suffering', 'Surprise', 'Sympathy', 'Yearning']
cat2ind = {}
ind2cat = {}
for idx, emotion in enumerate(cat):
  cat2ind[emotion] = idx
  ind2cat[idx] = emotion

vad = ['Valence', 'Arousal', 'Dominance']
ind2vad = {}
for idx, continuous in enumerate(vad):
  ind2vad[idx] = continuous

context_mean = [0.4690646, 0.4407227, 0.40508908]
context_std = [0.2514227, 0.24312855, 0.24266963]
body_mean = [0.43832874, 0.3964344, 0.3706214]
body_std = [0.24784276, 0.23621225, 0.2323653]
context_norm = [context_mean, context_std]
body_norm = [body_mean, body_std]

def functionpaths_video(url_path):
  modelpath = r"C:\Users\Dell\Desktop\emotic\debug_exp\models"
  resultspath = r"C:\Users\Dell\Desktop\emotic\debug_exp\results"
  emotion=yolo_video(url_path, resultspath, modelpath, context_norm, body_norm, ind2cat, ind2vad)
  return emotion

def functionpaths_image(images_path):
  modelpath=r"C:\Users\Dell\Desktop\emotic\debug_exp\models"
  resultspath = r"C:\Users\Dell\Desktop\emotic\debug_exp\results"
  emotion=yolo_infer(images_path, resultspath, modelpath, context_norm, body_norm, ind2cat, ind2vad)
  return emotion

  # if args.inference_file is not None:
  #   print ('inference over inference file images')
  #   yolo_infer(args.inference_file, result_path, model_path, context_norm, body_norm, ind2cat, ind2vad, args)
  # if args.video_file is not None:
  #   print ('inference over test video')
  #   yolo_video(args.video_file, result_path, model_path, context_norm, body_norm, ind2cat, ind2vad, args)
