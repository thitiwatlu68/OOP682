#Open-Closed Principle (OCP) states that software entities
class Circle:
    def __init__(self, radius):
        self.radius = radius

class Rectangle: #สี่เหลี่ยมผ
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
# class Triangle: #สามเหลี่ยม
#     def __init__(self, base, height):

def calculate_area(shape): #คำนวนพื้นที่
    if isinstance(shape, Circle):
        return 3.14 * shape.radius ** 2
    elif isinstance(shape, Rectangle):
        return shape.width * shape.height
    else:
        raise TypeError("Unknown shape")