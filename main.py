import yaml
from src.detection.yolov8_detector import YOLOv8Detector
from src.tracking.table_tracker import TableTracker
from src.tracking.client_tracker import ClientTracker
from src.analysis.data_manager import DataManager
from src.analysis.statistics import Statistics
from src.utils.logger import Logger
import cv2
import tkinter as tk
from src.gui import App  # Importă aplicația GUI

def main():
    logger = Logger()
    
    # Încarcă configurațiile
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # Inițializează detectorul YOLOv8
    detector = YOLOv8Detector(model_path=config['model_path'], logger=logger)

    # Inițializează tracker-ul pentru mese și clienți
    table_tracker = TableTracker(logger=logger)
    client_tracker = ClientTracker(logger=logger)

    # Inițializează managerul de date
    data_manager = DataManager(output_path=config['output_path'], logger=logger)

    # Inițializează fereastra principală Tkinter
    root = tk.Tk()
    app = App(root, detector, table_tracker, client_tracker, data_manager, logger)  # Adaugă logger aici

    # Rulare GUI
    root.mainloop()

    # Eliberare resurse video
    app.cap.release()
    cv2.destroyAllWindows()

    # Generare statistici
    statistics = Statistics(data_manager.get_data(), logger=logger)
    statistics.generate_report()


if __name__ == "__main__":
    main()
