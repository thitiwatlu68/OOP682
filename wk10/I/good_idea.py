# ISP -Interface Segregation Principle
# กล่าววว่า  คลาสลูกไม่ควรจะถูกบังคับให้ต้องพึ่งพาอินเทอร์เฟซที่พวกเขาไม่ได้ใช้

#good Idea of ISP Violation
from abc import ABC, abstractmethod

class Printer:
    @abstractmethod
    def print(self):
        pass
class Scanner:
    @abstractmethod
    def scan(self):
        pass
class Fax :
    @abstractmethod
    def fax(self, document):
        pass

#เครื่องพิมพ์ที่มีฟังก์ชันครบถ้วน
class MultiFunctionPrinter(Printer, Scanner, Fax):
    def print(self):
        print("Printing...")

    def scan(self):
        print("Scanning...")

    def fax(self, document):
        print("Faxing...")