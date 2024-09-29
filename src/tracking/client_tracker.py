# src/tracking/client_tracker.py

class ClientTracker:
    def __init__(self, logger):
        self.logger = logger
        self.clients = []  # Listă cu clienții detectați
        self.client_count = 0  # Numărul total de clienți

    def update(self, detections):
        print(f"Updating client tracker with detections: {detections}")  # Debug print

        for detection in detections:
            if detection['class'] == 1:  # Asigură-te că clasa este corectă (de exemplu, '1' pentru persoane)
                client_id = detection.get('id')  # Folosește un ID unic pentru client
                if client_id not in [client.get('id') for client in self.clients]:  # Verifică dacă clientul nu există deja
                    self.client_count += 1
                    self.clients.append(detection)
                    print(f"Added new client: {client_id}")  # Debug print
                else:
                    print(f"Client {client_id} already detected")  # Debug print

    def get_client_data(self):
        # Returnează informațiile despre clienți
        return {
            "total_clients": self.client_count,
            "clients": self.clients
        }

    def reset(self):
        self.clients.clear()
        self.client_count = 0
