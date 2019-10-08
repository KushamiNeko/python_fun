import unittest

from fun.utils import pretty


class TestHelper(unittest.TestCase):
    def test_hex_to_rgb_white(self):
        rgb = pretty.hex_to_rgb8("ffffff")

        self.assertTupleEqual(rgb, (255, 255, 255))

    def test_hex_to_rgb_red(self):
        rgb = pretty.hex_to_rgb8("ff0000")

        self.assertTupleEqual(rgb, (255, 0, 0))

    def test_hex_to_rgb_green(self):
        rgb = pretty.hex_to_rgb8("00ff00")

        self.assertTupleEqual(rgb, (0, 255, 0))

    def test_hex_to_rgb_blue(self):
        rgb = pretty.hex_to_rgb8("0000ff")

        self.assertTupleEqual(rgb, (0, 0, 255))

    def test_hex_to_rgb_black(self):
        rgb = pretty.hex_to_rgb8("000000")

        self.assertTupleEqual(rgb, (0, 0, 0))
