# DIP - Dependency Inversion Principle
# กล่าวว่าส่วนประกอบที่สูงกว่าควรจะไม่ขึ้นอยู่กับส่วนประกอบที่ต่ำกว่า แต่ทั้งสองควรจะขึ้นอยู่กับนามธรรม

#Bad Idea of DIP Violation
class App:
    def __init__(self):
        self.database = MySQLDatabase()  # ขึ้นอยู่กับการใช้งาน MySQL โดยตรง

    def save_data(self, data):
        self.database.save(data)

class MySQLDatabase:
    def save(self, data):
        print("Saving data to MySQL database....")

app = App()
app.save_data("Some important data")