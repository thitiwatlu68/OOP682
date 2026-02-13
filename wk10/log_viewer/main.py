from PySide6.QtWidgets import QApplication # type: ignore
from services.file_source import FileLogSource
from services.mock_source import MockLogSource
from services.csv_source import CsvLogSource
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication([])

    path = "logs/voters.csv"
    if path.endswith(".csv"):
        log = CsvLogSource(path)
    else:
        log = FileLogSource(path) 


    viewer = MainWindow(log)
    viewer.show()
    app.exec()
