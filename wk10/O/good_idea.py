from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass 

class Circle(Shape): #วงกลม
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2
    
class Rectangle(Shape): #สี่เหลี่ยม
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self): 
        return self.width * self.height
    
def calculate_area(shape: Shape): #คำนวนพื้นที่
    return shape.area()