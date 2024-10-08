
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

    def test_sweepline_3(self):
        # 線分数: 2, 交点数: 1
        #   線分の右端点 = 交点 の場合
        lst: list[LineSegment] = []
        lst.append(LineSegment(Point(-0.5, -0.5), Point(0.5, 0.5)))
        lst.append(LineSegment(Point(0, 1), Point(1, 0)))

        slm : SweepLineMethod = SweepLineMethod(lst)
        slm.exec()

        pts: list[Point] = slm.getCrossPoints()
        
        # 交点が想定のものかチェック
        self.assertEqual(1, len(pts))

        self.assertAlmostEqual(0.5, pts[0].x)
        self.assertAlmostEqual(0.5, pts[0].y)

    def test_sweepline_4(self):
        # 線分数: 2, 交点数: 1
        #   線分の左端点 = 交点 の場合
        lst: list[LineSegment] = []
        lst.append(LineSegment(Point(-0.5, -0.5), Point(1, 1)))
        lst.append(LineSegment(Point(0.5, 0.5), Point(1, 0)))

        slm : SweepLineMethod = SweepLineMethod(lst)
        slm.exec()

        pts: list[Point] = slm.getCrossPoints()
        
        # 交点が想定のものかチェック
        self.assertEqual(1, len(pts))

        self.assertAlmostEqual(0.5, pts[0].x)
        self.assertAlmostEqual(0.5, pts[0].y)

    def test_sweepline_5(self):
        # 線分数: 3, 交点数: 2
        #   交点 と端点（左端点）が同一の走査線上にある場合
        lst: list[LineSegment] = []
        lst.append(LineSegment(Point(-0.5, -0.5), Point(1.25, 1.25)))
        lst.append(LineSegment(Point(   0,    1), Point(   1, 0)))
        lst.append(LineSegment(Point( 0.5,    1), Point( 1.5, 0)))

        slm : SweepLineMethod = SweepLineMethod(lst)
        slm.exec()

        pts: list[Point] = slm.getCrossPoints()
        
        # 交点が想定のものかチェック
        self.assertEqual(2, len(pts))

        self.assertAlmostEqual(0.5, pts[0].x)
        self.assertAlmostEqual(0.5, pts[0].y)

        self.assertAlmostEqual(0.75, pts[1].x)
        self.assertAlmostEqual(0.75, pts[1].y)

    def test_sweepline_6(self):
        # 線分数: 3, 交点数: 3
        #   交点 と端点（右端点）が同一の走査線上にある場合
        lst: list[LineSegment] = []
        lst.append(LineSegment(Point( 0.0,  0.0 ), Point(2.0,  2.0)))
        lst.append(LineSegment(Point( 0.75, 1.5 ), Point(1.25, 0.5)))
        lst.append(LineSegment(Point(-0.5,  1.25), Point(1.75, 1.25)))

        slm : SweepLineMethod = SweepLineMethod(lst)
        slm.exec()

        pts: list[Point] = slm.getCrossPoints()
        
        # 交点が想定のものかチェック
        self.assertEqual(3, len(pts))

        self.assertAlmostEqual(1.25, pts[0].x)
        self.assertAlmostEqual(1.25, pts[0].y)

        self.assertAlmostEqual(7/8,  pts[1].x)
        self.assertAlmostEqual(1.25, pts[1].y)

        self.assertAlmostEqual(1.0, pts[2].x)
        self.assertAlmostEqual(1.0, pts[2].y)

    def test_sweepline_7(self):
        # 線分数: 3, 交点数: 2
        #   複数の端点が同一の走査線上にある場合
        lst: list[LineSegment] = []
        lst.append(LineSegment(Point(1.0,  1.0), Point(3.0, -1.0)))
        lst.append(LineSegment(Point(1.0,  2.0), Point(2.0, -1.0)))
        lst.append(LineSegment(Point(2.0, -0.5), Point(3.0,    0)))

        slm : SweepLineMethod = SweepLineMethod(lst)
        slm.exec()

        pts: list[Point] = slm.getCrossPoints()
        
        # 交点が想定のものかチェック
        self.assertEqual(2, len(pts))

        self.assertAlmostEqual(1.5, pts[0].x)
        self.assertAlmostEqual(0.5, pts[0].y)

        self.assertAlmostEqual( 7/3, pts[1].x)
        self.assertAlmostEqual(-1/3, pts[1].y)

    def test_sweepline_8(self):
        # 線分数: 4, 交点数: 4
        #   複数の交点が同一の走査線上にある場合
        lst: list[LineSegment] = []
        lst.append(LineSegment(Point(1.0,  2.0), Point(3.0,    0)))
        lst.append(LineSegment(Point(1.0,  1.0), Point(3.0, -1.0)))
        lst.append(LineSegment(Point(1.0,    0), Point(3.0,  2.0)))
        lst.append(LineSegment(Point(1.0, -1.0), Point(3.0,  1.0)))

        slm : SweepLineMethod = SweepLineMethod(lst)
        slm.exec()

        pts: list[Point] = slm.getCrossPoints()
        
        # 交点が想定のものかチェック
        self.assertEqual(4, len(pts))

        self.assertAlmostEqual(1.5, pts[0].x)
        self.assertAlmostEqual(0.5, pts[0].y)

        self.assertAlmostEqual(2.0, pts[1].x)
        self.assertAlmostEqual(1.0, pts[1].y)

        self.assertAlmostEqual(2.0, pts[2].x)
        self.assertAlmostEqual(0.0, pts[2].y)

        self.assertAlmostEqual(2.5, pts[3].x)
        self.assertAlmostEqual(0.5, pts[3].y)

    def test_sweepline_9(self):
        # 線分数: 2, 交点数: 1
        #   左端点で２線分が重なっている場合
        lst: list[LineSegment] = []
        lst.append(LineSegment(Point(1.0,  1.0), Point(1.5,   0)))
        lst.append(LineSegment(Point(1.0,  1.0), Point(2.0, 2.0)))

        slm : SweepLineMethod = SweepLineMethod(lst)
        slm.exec()

        pts: list[Point] = slm.getCrossPoints()
        
        # 交点が想定のものかチェック
        self.assertEqual(1, len(pts))

        self.assertAlmostEqual(1.0, pts[0].x)
        self.assertAlmostEqual(1.0, pts[0].y)
    
    def test_sweepline_10(self):
        # 線分数: 2, 交点数: 1
        #   右端点で２線分が重なっている場合
        lst: list[LineSegment] = []
        lst.append(LineSegment(Point(3.0,  2.0), Point(4.0, 1.0)))
        lst.append(LineSegment(Point(2.5,  0.0), Point(4.0, 1.0)))

        slm : SweepLineMethod = SweepLineMethod(lst)
        slm.exec()

        pts: list[Point] = slm.getCrossPoints()
        
        # 交点が想定のものかチェック
        self.assertEqual(1, len(pts))

        self.assertAlmostEqual(4.0, pts[0].x)
        self.assertAlmostEqual(1.0, pts[0].y)

    def test_sweepline_11(self):
        # 線分数: 2, 交点数: 1
        #   左端点と右端点で２線分が重なっている場合
        lst: list[LineSegment] = []
        lst.append(LineSegment(Point(0.0,  0.0), Point(1.0, 1.0)))
        lst.append(LineSegment(Point(1.0,  1.0), Point(2.0, 0.0)))

        slm : SweepLineMethod = SweepLineMethod(lst)
        slm.exec()

        pts: list[Point] = slm.getCrossPoints()
        
        # 交点が想定のものかチェック
        self.assertEqual(1, len(pts))

        self.assertAlmostEqual(1.0, pts[0].x)
        self.assertAlmostEqual(1.0, pts[0].y)
