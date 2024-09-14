
import unittest

from Point import Point


class TestPoint(unittest.TestCase):
    """点クラスに関するテスト
    """

    def test_point_1(self):
        pt1: Point = Point()

        self.assertEqual(0, pt1.x)
        self.assertEqual(0, pt1.y)

    def test_point_2(self):
        pt2: Point = Point(1.0, 2.0)

        self.assertEqual(1, pt2.x)
        self.assertEqual(2, pt2.y)

    def test_point_3(self):
        pt2: Point = Point()
        pt2.setAddress(1.0, 2.0)

        pt3: Point = Point()
        pt3.copyPoint(pt2)

        self.assertEqual(1, pt2.x)
        self.assertEqual(2, pt2.y)
        self.assertEqual(1, pt3.x)
        self.assertEqual(2, pt3.y)

        self.assertNotEqual(id(pt3), id(pt2))

