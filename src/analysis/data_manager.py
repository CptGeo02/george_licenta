import pandas as pd

class DataManager:
    def __init__(self, output_path, logger):
        self.output_path = output_path
        self.data = []
        self.logger = logger

    def save_data(self, table_data, client_data):
        self.logger.log("Saving data to Excel...")
        data_entry = {'table_data': table_data, 'client_data': client_data}
        self.data.append(data_entry)
        df = pd.DataFrame(self.data)
        df.to_excel(self.output_path, index=False)

    def get_data(self):
        return self.data
