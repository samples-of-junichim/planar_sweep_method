
import unittest
from Point import Point
from LineSegment import LineSegment
from SweepLineMethod import SweepLineMethod


class TestSweepLineMethod(unittest.TestCase):
    """平面走査法に関するテスト

    一般的なテストケース
    """

    def test_sweepline_general_1(self):
        # 複数線分、複数交点
        lst: list[LineSegment] = []
        lst.append(LineSegment(Point(1.0,  2.0), Point(5.0, 2.0)))
        lst.append(LineSegment(Point(1.0,  1.0), Point(4.0, 4.0)))
        lst.append(LineSegment(Point(2.0,  3.0), Point(4.0, 0.0)))
        lst.append(LineSegment(Point(3.0,  2.5), Point(5.0, 3.0)))
        lst.append(LineSegment(Point(4.0,  3.0), Point(6.0, 2.0)))
        lst.append(LineSegment(Point(4.5, -1.5), Point(6.0, 3.0)))

        slm : SweepLineMethod = SweepLineMethod(lst)
        slm.exec()

        pts: list[Point] = slm.getCrossPoints()
        
        # 交点が想定のものかチェック
        self.assertEqual(5, len(pts))

        self.assertAlmostEqual(2.0, pts[0].x)
        self.assertAlmostEqual(2.0, pts[0].y)

        self.assertAlmostEqual(2.4, pts[1].x)
        self.assertAlmostEqual(2.4, pts[1].y)

        self.assertAlmostEqual(8/3, pts[2].x)
        self.assertAlmostEqual(2.0, pts[2].y)

        self.assertAlmostEqual(13/3, pts[3].x)
        self.assertAlmostEqual(17/6, pts[3].y)

        self.assertAlmostEqual(40/7, pts[4].x)
        self.assertAlmostEqual(15/7, pts[4].y)
