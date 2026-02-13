# DIP - Dependency Inversion Principle
# กล่าวว่าส่วนประกอบที่สูงกว่าควรจะไม่ขึ้นอยู่กับส่วนประกอบที่ต่ำกว่า แต่ทั้งสองควรจะขึ้นอยู่กับนามธรรม

#Good Idea of DIP Violation
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass

class MySQLDatabase(Database):
    def save(self, data):
        print("Saving data to MySQL database....")

class PostgreSQLDatabase(Database):
    def save(self, data):
        print("Saving data to PostgreSQL database....")

class App:
    def __init__(self, database: Database):
        self.database = database  # ขึ้นอยู่กับนามธรรม Database

    def save_data(self, data):
        self.database.save(data)

# การใช้งาน
mysql_db = MySQLDatabase()
app = App(mysql_db)
app.save_data("Sample Data")