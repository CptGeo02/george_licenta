import cv2
import torch
import numpy as np
from ultralytics import YOLO
from src.utils.logger import Logger

class YOLOv8Detector:
    def __init__(self, model_path, logger: Logger, video_source=0, task='detect'):
        # Verifică dacă CUDA este disponibil
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Utilizarea device-ului: {self.device}")  # Afișează dacă folosești GPU sau CPU
        
        self.model = YOLO(model_path, task=task)
        self.logger = logger
        self.video_source = video_source  # Sursa video, cu camera live ca implicit

    def detect_frame(self, frame):
        # Redimensionează frame-ul la dimensiunea 640x640
        frame_resized = cv2.resize(frame, (640, 640))
        
        # Normalizează frame-ul (transformă din intervalul 0-255 în 0.0-1.0)
        frame_normalized = frame_resized / 255.0
        
        # Asigură-te că frame-ul este un tensor
        frame_tensor = torch.from_numpy(frame_normalized).permute(2, 0, 1).float()  # Schimbă dimensiunile
        frame_tensor = frame_tensor.unsqueeze(0).to(self.device)  # Adaugă dimensiunea batch-ului și mută tensorul

        # Execută detectarea
        results = self.model(frame_tensor)

        if len(results) == 0 or len(results[0].boxes) == 0:
            return []  # Nu au fost detectate obiecte

        detections = []
        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # Coordonatele
            cls = int(box.cls[0])  # Clasa
            conf = box.conf[0]  # Scorul de încredere

            detections.append({
                'box': (x1.item(), y1.item(), x2.item(), y2.item()),  # Convertim la float
                'class': cls,
                'confidence': conf.item()  # Convertim la float
            })

        return detections

    
    def exit_requested(self):
        return cv2.waitKey(1) & 0xFF == ord('q')
