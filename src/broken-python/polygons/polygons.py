import turtle
from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract base class for drawable 2-D shapes."""

    @abstractmethod
    def draw(self):
        """Render the shape."""

    @abstractmethod
    def calculate_perimeter(self):
        """Return the perimeter of the shape."""


class Polygon(Shape):
    """A regular polygon with ``sides`` edges, each ``length`` units long."""

    def __init__(self, sides, length=50):
        self.sides = sides
        self.length = length

    def calculate_internal_angles_sum(self):
        """Sum of the interior angles: (n - 2) * 180."""
        return (self.sides - 2) * 180

    def calculate_internal_angle(self):
        """Single interior angle of a regular polygon: (n - 2) * 180 / n."""
        return (self.sides - 2) * 180 / self.sides

    def calculate_perimeter(self):
        """Perimeter: number of sides times the edge length."""
        return self.sides * self.length

    def draw(self):
        """Draw the polygon with the turtle, turning 360/n degrees per edge."""
        turtle.Screen()
        t = turtle.Turtle()
        t.pen(pencolor="red", pensize=2, fillcolor="green")
        for _ in range(self.sides):
            t.forward(self.length)
            t.right(360 / self.sides)


if __name__ == "__main__":
    sides = int(input("How many sides does your polygon have?: "))
    polygon = Polygon(sides)

    print("    Sides:", polygon.sides)
    print("    Internal angles sum:", polygon.calculate_internal_angles_sum())
    print("    Internal angle:", polygon.calculate_internal_angle())
    print("    Perimeter:", polygon.calculate_perimeter())

    answer = input("Would you like me to draw it? (Y/n): ")
    if answer == "" or answer.lower() == "y":
        polygon.draw()
