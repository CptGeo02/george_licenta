import torch

class YoloNASDetector:
    def __init__(self):
        # Încarcă modelul YOLO NAS
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5n')  # YOLO-NAS simplificat
        
    def detect(self, image):
        results = self.model(image)
        return results