import tkinter as tk
import cv2
from PIL import Image, ImageTk

class App:
    def __init__(self, root, detector, table_tracker, client_tracker, data_manager, logger):
        self.root = root
        self.detector = detector
        self.table_tracker = table_tracker
        self.client_tracker = client_tracker
        self.data_manager = data_manager
        self.logger = logger

        # Inițializare GUI
        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.pack()

        # Etichete pentru numărul de mese și statusul acestora
        self.table_count_label = tk.Label(self.root, text="Număr mese: 0")
        self.table_count_label.pack()

        self.client_count_label = tk.Label(self.root, text="Număr clienți: 0")
        self.client_count_label.pack()

        self.table_status_label = tk.Label(self.root, text="Status mese: ")
        self.table_status_label.pack()

        # Inițializare captura video
        self.video_source = 0  # Poți schimba cu un fișier video
        self.cap = cv2.VideoCapture(self.video_source)
        if not self.cap.isOpened():
            print("Cannot open video source")
            self.root.quit()

        # Start update frame
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Detectare cadre
            detections = self.detector.detect_frame(frame)
            print(f"Detecții: {detections}")  # Printare detecții

            # Actualizare stări mese și clienți
            self.table_tracker.update(detections)
            self.client_tracker.update(detections)

            # Verifică numărul de mese și clienți
            print(f"Mese detectate: {self.table_tracker.tables}")  # Printare mese
            print(f"Clienți detectați: {self.client_tracker.clients}")  # Printare clienți

            # Desenare detectări pe cadru
            self.draw_detections(frame)

            # Obține datele pentru afișare
            self.update_labels()

            # Afișează imaginea pe canvas
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgTk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgTk)
            self.canvas.image = imgTk  # Asta previne garbage collection
        else:
            print("Failed to read frame")

        self.root.after(10, self.update_frame)  # Apel recursiv

    def draw_detections(self, frame):
        # Desenează dreptunghiuri pentru mese
        for table in self.table_tracker.tables:
            if hasattr(table, 'bbox'):  # Verifică dacă are bbox
                x1, y1, x2, y2 = table.bbox
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Dreptunghi albastru
                print(f"Dreptunghi masă: {table.bbox}")  # Printare bbox masă

        # Desenează dreptunghiuri pentru clienți
        for client in self.client_tracker.clients:
            if hasattr(client, 'bbox'):  # Verifică dacă are bbox
                x1, y1, x2, y2 = client.bbox
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Dreptunghi verde
                print(f"Dreptunghi client: {client.bbox}")  # Printare bbox client

    def update_labels(self):
        # Obține numărul de mese și clienți
        num_tables = len(self.table_tracker.tables)  # Modifică în funcție de implementarea ta
        num_clients = len(self.client_tracker.clients)  # Modifică în funcție de implementarea ta

        self.table_count_label.config(text=f"Număr mese: {num_tables}")
        self.client_count_label.config(text=f"Număr clienți: {num_clients}")

        # Afișează statusul meselor
        table_statuses = [f"Masa {i}: {table['status']}" for i, table in enumerate(self.table_tracker.get_table_data().values())]
        self.table_status_label.config(text="Status mese: " + ", ".join(table_statuses))

    def run(self):
        self.root.mainloop()
