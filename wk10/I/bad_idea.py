# ISP -Interface Segregation Principle
# กล่าววว่า  คลาสลูกไม่ควรจะถูกบังคับให้ต้องพึ่งพาอินเทอร์เฟซที่พวกเขาไม่ได้ใช้

#Bad Idea of ISP Violation
class Machine:
    def print(self):
        pass

    def scan(self):
        pass

    def fax(self, document):
        pass

class OLdPrinter(Machine): #เครื่องพิมพ์ที่ไม่มีฟังก์ชันสแกนและแฟกซ์
    def print(self):
        print("Printing...")

    def scan(self):
        raise NotImplementedError("This printer does not support scanning.")

    def fax(self, document):
        raise NotImplementedError("This printer does not support faxing.")