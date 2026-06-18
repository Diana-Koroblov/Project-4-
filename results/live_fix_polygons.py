import turtle

class Polygon:
    def __init__(self, sides):
        self.sides = sides
        self.internal_angles_sum = (sides - 2) * 180
        self.internal_angle = self.internal_angles_sum / sides
    
    def draw(self):
        t = turtle.Turtle()
        t.pen(pencolor="red", pensize=2, fillcolor="green")
        length_of_edge = 50
        for i in range(0, self.sides):
            t.forward(length_of_edge)
            t.right(360 / self.sides)

sides = int(input("How many sides does your polygon have?: " ))
polygon = Polygon(sides)
print("    Sides:", polygon.sides)
print("    Internal angles sum:", polygon.internal_angles_sum)
print("    Internal angles:", polygon.internal_angle)
draw = input("Would you like me to draw it? (Y/n): ")
if draw == "" or draw.lower() == "y":
    polygon.draw()
    turtle.done()