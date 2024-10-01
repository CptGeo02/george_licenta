import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os

class App:
    def __init__(self, root, detector, table_tracker, client_tracker, data_manager, logger):
        self.root = root
        self.detector = detector
        self.table_tracker = table_tracker
        self.client_tracker = client_tracker
        self.data_manager = data_manager
        self.logger = logger
        self.image_list = []
        self.image_index = 0

        # Inițializare GUI
        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.pack()

        # Butoane pentru alegerea sursei
        self.live_button = tk.Button(self.root, text="Camera Live", command=self.select_camera)
        self.live_button.pack(side=tk.LEFT)

        self.video_button = tk.Button(self.root, text="Video", command=self.select_video)
        self.video_button.pack(side=tk.LEFT)

        self.image_button = tk.Button(self.root, text="Imagini", command=self.select_images)
        self.image_button.pack(side=tk.LEFT)

        # Săgeți pentru navigarea printre imagini
        self.prev_button = tk.Button(self.root, text="Prev", command=self.prev_image)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_image)
        self.next_button.pack(side=tk.LEFT)

        # Etichete pentru numărul de mese și statusul acestora
        self.table_count_label = tk.Label(self.root, text="Număr mese: 0")
        self.table_count_label.pack()

        self.client_count_label = tk.Label(self.root, text="Număr clienți: 0")
        self.client_count_label.pack()

        self.table_status_label = tk.Label(self.root, text="Status mese: ")
        self.table_status_label.pack()

        # Inițializare variabile
        self.video_source = None
        self.cap = None

    def select_camera(self):
        self.video_source = 0  # Camera live
        self.cap = cv2.VideoCapture(self.video_source)
        self.update_frame()

    def select_video(self):
        self.video_source = "path_to_video.mp4"  # Schimbă cu calea fișierului video dorit
        self.cap = cv2.VideoCapture(self.video_source)
        self.update_frame()

    def select_images(self):
        self.image_list = [os.path.join("data/images", f) for f in os.listdir("data/images") if f.endswith(('.png', '.jpg', '.jpeg'))]
        if self.image_list:
            self.image_index = 0
            self.show_image(self.image_list[self.image_index])

   
    def next_image(self):
        if self.image_list and self.image_index < len(self.image_list) - 1:
            self.image_index += 1
            self.show_image(self.image_list[self.image_index])

    def prev_image(self):
        if self.image_list and self.image_index > 0:
            self.image_index -= 1
            self.show_image(self.image_list[self.image_index])


    def resize_frame(self, frame, target_width, target_height):
        height, width = frame.shape[:2]
        aspect_ratio = width / height

        # Ajustează dimensiunile pentru a păstra aspectul
        if width > height:
            new_width = target_width
            new_height = int(target_width / aspect_ratio)
        else:
            new_height = target_height
            new_width = int(target_height * aspect_ratio)

        # Redimensionează imaginea
        return cv2.resize(frame, (new_width, new_height))

    def show_image(self, image_path):
        frame = cv2.imread(image_path)
        if frame is not None:
            # Detectează obiectele în cadrul imaginii
            detections = self.detector.detect_frame(frame)
            self.table_tracker.update(detections)
            self.client_tracker.update(detections)

            # Desenarea detecțiilor pe frame
            self.draw_detections(frame)

            # Redimensionează imaginea pentru a se potrivi cu canvas-ul
            frame_resized = self.resize_frame(frame, 640, 480)

            # Convertirea imaginii BGR în RGB pentru a fi afișată corect în Tkinter
            img = Image.fromarray(cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB))
            imgTk = ImageTk.PhotoImage(image=img)

            # Afișarea imaginii în canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgTk)
            self.canvas.image = imgTk

    def draw_detections(self, frame):
        # Desenează dreptunghiuri pentru mese
        for table in self.table_tracker.tables:
            if hasattr(table, 'bbox'):
                x1, y1, x2, y2 = table.bbox
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)  # Roșu pentru mese

        # Desenează dreptunghiuri pentru clienți
        for client in self.client_tracker.clients:
            if hasattr(client, 'bbox'):
                x1, y1, x2, y2 = client.bbox
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)  # Verde pentru clienți


    def update_frame(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                detections = self.detector.detect_frame(frame)
                self.table_tracker.update(detections)
                self.client_tracker.update(detections)

                self.draw_detections(frame)
                self.update_labels()

                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                imgTk = ImageTk.PhotoImage(image=img)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=imgTk)
                self.canvas.image = imgTk
            self.root.after(10, self.update_frame)

  
    def update_labels(self):
        num_tables = len(self.table_tracker.tables)
        num_clients = len(self.client_tracker.clients)

        self.table_count_label.config(text=f"Număr mese: {num_tables}")
        self.client_count_label.config(text=f"Număr clienți: {num_clients}")

        table_statuses = [f"Masa {i}: {table['status']}" for i, table in enumerate(self.table_tracker.get_table_data().values())]
        self.table_status_label.config(text="Status mese: " + ", ".join(table_statuses))

    def run(self):
        self.root.mainloop()
