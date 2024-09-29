# src/tracking/table_tracker.py

class TableTracker:
    def __init__(self, logger):
        self.logger = logger
        self.tables = {}  # Dictionar pentru starea meselor

    def update(self, detections):
        print(f"Updating table tracker with detections: {detections}")  # Debug print

        for detection in detections:
            if detection['class'] == 0:  # Asigură-te că clasa este corectă pentru mese
                table_id = detection.get('id')  # Presupunem că ai un ID unic

                # Verifică dacă masa a fost deja detectată
                if table_id in self.tables:
                    print(f"Table {table_id} already detected, updating status.")  # Debug print
                    status = self.determine_table_status(detection)
                    self.tables[table_id]['status'] = status  # Actualizează doar starea
                else:
                    status = self.determine_table_status(detection)
                    self.tables[table_id] = {
                        'status': status,
                        'client_count': detection.get('client_count', 0),
                        'time_spent': detection.get('time_spent', 0)
                    }
                    print(f"Added new table {table_id} with status: {status}")  # Debug print

        self.reset_tables()  # Reset the tables that are not detected anymore

    def determine_table_status(self, detection):
        # Logica pentru a determina starea mesei
        # Exemplu simplu:
        if detection.get('clean', True):  # Presupunem că există un câmp 'clean' în detections
            return "Available"
        else:
            return "Need to clean"

    def is_table_present(self, table_id):
        # Implementare a unei logici pentru a verifica dacă masa este încă prezentă
        # Aici ar trebui să ai logica ta pentru a determina dacă masa este prezentă sau nu
        return True  # Temporar întoarce True

    def reset_tables(self):
        # Poate fi folosit pentru a reseta mesele care nu mai sunt detectate
        for table_id in list(self.tables.keys()):
            if not self.is_table_present(table_id):
                print(f"Removing table {table_id} as it is no longer detected.")  # Debug print
                del self.tables[table_id]

    def get_table_data(self):
        # Returnează informațiile despre mese
        return self.tables

    def reset(self):
        self.tables.clear()
