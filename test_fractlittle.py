#!/usr/bin/env python3

import unittest
from fractlittle import FractLittle
import os
from PIL import Image


class FractLittleTest(unittest.TestCase):
    def setUp(self):
        self.fl = FractLittle()

    def test_create_fractlittle(self):
        self.assertIsInstance(self.fl, FractLittle)

    def test_initial_output(self):
        self.assertEqual([], self.fl.output)

    def test_fill_with_zeroes(self):
        self.fl.fill(0, 10, 10)
        self.assertIsInstance(self.fl.output[9], list)
        self.assertEqual(0, self.fl.output[0][0])

    def test_calc_center(self):
        result = self.fl.center(5, 5)
        self.assertEqual((2, 2), result)

    def test_point_value(self):
        result = self.fl.point_value(5, 5, (0, 0))
        self.assertEqual((-2, 2), result)
        result = self.fl.point_value(5, 5, (4, 0))
        self.assertEqual((2, 2), result)
        result = self.fl.point_value(5, 5, (0, 4))
        self.assertEqual((-2, -2), result)
        result = self.fl.point_value(5, 5, (4, 4))
        self.assertEqual((2, -2), result)
        result = self.fl.point_value(5, 5, (2, 2))
        self.assertEqual((0, 0), result)

    def test_fill_with_values(self):
        self.fl.fill_with_values(3, 3)
        expected = [
            [(-2, 2), (0, 2), (2, 2)],
            [(-2, 0), (0, 0), (2, 0)],
            [(-2, -2), (0, -2), (2, -2)],
        ]
        self.assertEqual(expected, self.fl.output)

    def test_value_bailout(self):
        result = self.fl.bailout((1, 1))
        self.assertEqual(False, result)
        result = self.fl.bailout((3, 3))
        self.assertEqual(True, result)

    def test_color_from_value(self):
        result = self.fl.color_from_value((-2, 2))
        self.assertEqual(' ', result)

    def test_print_fractal(self):
        result = self.fl.print(256, 256)
        test_mandelbrot = open(r"test_data/mandelbrot.txt", "r+")
        expected = test_mandelbrot.read()
        self.assertEqual(expected, result)

    def test_draw_image(self):
        filename = "tmp/image.png"
        if os.path.exists(filename):
            os.remove(filename)
        self.fl.draw(filename, 1024, 1024)
        self.assertTrue(os.path.exists(filename))
        im = Image.open(filename)
        self.assertEqual((1024, 1024), im.size)