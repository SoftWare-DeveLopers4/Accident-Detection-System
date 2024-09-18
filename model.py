#Run this in Google Collab
from roboflow import Roboflow
rf = Roboflow(api_key="I8XyIcOd4TBpyCIS0bCP")
project = rf.workspace("self-ixih1").project("accident-detection-qgglm")
version = project.version(3)
dataset = version.download("yolov9")

from ultralytics import YOLO
model = YOLO('yolov9c.pt')

results = model.train(data='/content/Accident-detection-3/data.yaml', epochs=300,imgsz=640,batch=16)