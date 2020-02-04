#!/usr/bin/env python3
import cmath
from PIL import Image

class FractLittle:
    def __init__(self):
        self.output = []

    def fill(self, initial_value, width, height):
        for _ in range(0, width):
            row = []
            for _ in range(0, height):
                row.append(initial_value)
            self.output.append(row)

    def center(self, width, height):
        return ((width - 1)/2, (height - 1)/2)

    def point_value(self, width, height, point):
        point_x, point_y = point
        center_x, center_y = self.center(width, height)
        value_x = (point_x - center_x) * 2 / center_x # left to right
        value_y = (point_y - center_y) * -2 / center_y # bottom to top
        return (value_x, value_y)

    def fill_with_values(self, width, height):
        for point_y in range(0, height):
            row = []
            for point_x in range(0, width):
                value = self.point_value(width, height, (point_x, point_y))
                row.append(value)
            self.output.append(row)

    def bailout(self, value):
        x, y = value
        return abs(x) > 2 or abs(y) > 2

    def color_from_value(self, value):
        x, y = value
        complex_value = complex(x, y)
        z = complex(0, 0)
        for _ in range(0, 200):
            z = z**2 + complex_value
            if self.bailout((z.real, z.imag)):
                break
        else:
            return '@'
        return ' '

    def print(self, width, height):
        result = ""
        self.fill_with_values(width, height)
        for row in self.output:
            for column in row:
                result += self.color_from_value(column)
            result += "\n"
        return result

    def draw(self, filename, width, height):
        img = Image.new("RGB", (width, height), color = "white")

        self.fill_with_values(width, height)
        for y, row in enumerate(self.output):
            for x, column in enumerate(row):
                is_constant = self.color_from_value(column).strip()
                # draw a pixel color
                if is_constant:
                    img.putpixel((x,y), (0, 0, 0))
        img.save(filename)
