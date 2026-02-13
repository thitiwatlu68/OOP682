class PDFReportGenerator:
    def __init__(self, data):
        self.data = data

class ExcelReportGenerator:
    def __init__(self, data):
        self.data = data
        
    def generate(self):
        pass

class EmailSender:
    def __init__(self, report):
        self.report = report

    def send(self, recipient):
        pass