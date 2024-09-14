import time

class TimeTracker:
    def __init__(self):
        self.time_data = {}

    def track_time(self, table_id):
        if table_id not in self.time_data:
            self.time_data[table_id] = {
                'start_time': time.time(),
                'order_time': None,
                'wait_time': None
            }

    def get_total_time(self, table_id):
        if table_id in self.time_data:
            return time.time() - self.time_data[table_id]['start_time']
        return 0

    def get_order_time(self, table_id):
        # Aici ai adăuga logica pentru timpul până la preluarea comenzii
        return 0

    def get_wait_time(self, table_id):
        # Aici ai adăuga logica pentru timpul până la primirea comenzii
        return 0
