
import unittest
from Point import Point
from LineSegment import LineSegment
from SweepLineMethod import SweepLineMethod


class TestSweepLineMethod(unittest.TestCase):
    """典型的な 平面走査法に関するテスト
    """

    def test_sweepline_1(self):
        # 線分数: 2, 交点数: 1
        lst: list[LineSegment] = []
        lst.append(LineSegment(Point( 0,  1), Point(1, 0)))
        lst.append(LineSegment(Point(-1, -1), Point(2, 2)))

        slm : SweepLineMethod = SweepLineMethod(lst)
        slm.exec()

        pts: list[Point] = slm.getCrossPoints()
        
        # 交点が想定のものかチェック
        self.assertEqual(1, len(pts))

        self.assertAlmostEqual(0.5, pts[0].x)
        self.assertAlmostEqual(0.5, pts[0].y)

    def test_sweepline_2(self):
        # 線分数: 3, 交点数: 3
        lst: list[LineSegment] = []
        lst.append(LineSegment(Point( 0,  1), Point(1.5, -0.5)))
        lst.append(LineSegment(Point(-1, -1), Point(2, 2)))
        lst.append(LineSegment(Point(-2, -0.75), Point(3, 0.5)))

        slm : SweepLineMethod = SweepLineMethod(lst)
        slm.exec()

        pts: list[Point] = slm.getCrossPoints()
        
        # 交点が想定のものかチェック
        self.assertEqual(3, len(pts))

        self.assertAlmostEqual(-1/3, pts[0].x)
        self.assertAlmostEqual(-1/3, pts[0].y)

        self.assertAlmostEqual(0.5, pts[1].x)
        self.assertAlmostEqual(0.5, pts[1].y)

        self.assertAlmostEqual(1, pts[2].x)
        self.assertAlmostEqual(0, pts[2].y)
