import csv
from interfaces.data_source import ILogSource

class CsvLogSource(ILogSource):

    def __init__(self, filepath):
        self.filepath = filepath

    def get_logs(self) -> list[str]:
        logs = []
        with open(self.filepath, newline='', encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                logs.append(",".join(row))  
                # ทำให้ format คล้าย log file

        return logs
