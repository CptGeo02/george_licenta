import time
from models.detection_model import YoloNASDetector
from utils.table_status import TableStatus
from utils.time_tracking import TimeTracker
import pandas as pd

# Inițializare modele și algoritmi
detector = YoloNASDetector()
status_checker = TableStatus()
time_tracker = TimeTracker()

# Exemplu de date simulate (în viața reală, ai lua aceste date din camera RealSense D435i)
tables = [{'id': 1, 'status': 'available', 'people': 0},
          {'id': 2, 'status': 'eating', 'people': 4}]

# Funcția principală de monitorizare
def monitor_restaurant():
    for table in tables:
        # Actualizează statusul mesei
        table['status'] = status_checker.check_status(table['id'])
        
        # Monitorizează timpul petrecut de clienți la masă
        time_tracker.track_time(table['id'])
        
        # Adaugă datele la un fișier Excel
        data = {
            'Table ID': table['id'],
            'Status': table['status'],
            'People Count': table['people'],
            'Total Time': time_tracker.get_total_time(table['id']),
            'Order Time': time_tracker.get_order_time(table['id']),
            'Wait Time': time_tracker.get_wait_time(table['id'])
        }
        
        save_to_excel(data)

def save_to_excel(data):
    df = pd.DataFrame([data])
    with pd.ExcelWriter('data/customer_data.xlsx', mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False, header=False)

if __name__ == "__main__":
    while True:
        monitor_restaurant()
        time.sleep(10)  # Rulăm la fiecare 10 secunde pentru actualizare