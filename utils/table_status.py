class TableStatus:
    def check_status(self, table_id):
        # Statusul mesei bazat pe procesarea imaginii
        # Returnăm statusuri simulate pentru exemplu
        return "eating" if table_id == 2 else "available"
