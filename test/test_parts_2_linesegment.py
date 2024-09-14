
import unittest

from Point import Point
from LineSegment import CrossPointStatus, LineSegment


class TestLineSegment(unittest.TestCase):
    """線分クラスに関するテスト
    """

    def setUp(self):
        self.ls: LineSegment = LineSegment(Point(1, -1), Point(3, 1))

    def test_linesegment_1(self):
        ls: LineSegment = LineSegment()

        self.assertEqual(0, ls.pt1.x)
        self.assertEqual(0, ls.pt1.y)
        self.assertEqual(0, ls.pt2.x)
        self.assertEqual(0, ls.pt2.y)

    def test_linesegment_2(self):
        self.assertEqual(1,  self.ls.pt1.x)
        self.assertEqual(-1, self.ls.pt1.y)
        self.assertEqual(3,  self.ls.pt2.x)
        self.assertEqual(1,  self.ls.pt2.y)

        self.assertEqual(2,  self.ls.a)
        self.assertEqual(-2, self.ls.b)
        self.assertEqual(4,  self.ls.c)

    def test_linesegment_2_1(self):
        # 傾き正の線分
        self.assertEqual(1,  self.ls.minx)
        self.assertEqual(3,  self.ls.maxx)
        self.assertEqual(-1, self.ls.miny)
        self.assertEqual(1,  self.ls.maxy)

        self.assertEqual(1,  self.ls.minxPt.x)
        self.assertEqual(-1, self.ls.minxPt.y)
        self.assertEqual(3,  self.ls.maxxPt.x)
        self.assertEqual(1,  self.ls.maxxPt.y)
        self.assertEqual(1,  self.ls.minyPt.x)
        self.assertEqual(-1, self.ls.minyPt.y)
        self.assertEqual(3,  self.ls.maxyPt.x)
        self.assertEqual(1,  self.ls.maxyPt.y)

    def test_linesegment_2_2(self):
        # 傾き負の線分
        ls: LineSegment = LineSegment()
        ls.setPoints(Point().setAddress(1, 1), Point().setAddress(3, -1))

        self.assertEqual(1,  ls.minx)
        self.assertEqual(3,  ls.maxx)
        self.assertEqual(-1, ls.miny)
        self.assertEqual(1,  ls.maxy)

        self.assertEqual(1,  ls.minxPt.x)
        self.assertEqual(1,  ls.minxPt.y)
        self.assertEqual(3,  ls.maxxPt.x)
        self.assertEqual(-1, ls.maxxPt.y)
        self.assertEqual(3,  ls.minyPt.x)
        self.assertEqual(-1, ls.minyPt.y)
        self.assertEqual(1,  ls.maxyPt.x)
        self.assertEqual(1,  ls.maxyPt.y)

    def test_linesegment_3(self):
        ls: LineSegment = LineSegment()
        ls.copyLineSegment(self.ls)

        self.assertEqual(1,  ls.pt1.x)
        self.assertEqual(-1, ls.pt1.y)
        self.assertEqual(3,  ls.pt2.x)
        self.assertEqual(1,  ls.pt2.y)

        self.assertEqual(2,  ls.a)
        self.assertEqual(-2, ls.b)
        self.assertEqual(4,  ls.c)

        self.assertNotEqual(id(ls.pt1), id(self.ls.pt1))
        self.assertNotEqual(id(ls.pt2), id(self.ls.pt2))
        self.assertNotEqual(id(ls.pt1), id(self.ls.pt2))

    def test_linesegment_4(self):
        ret: bool = self.ls.isInsideRectangle(Point().setAddress(2, 0))
        self.assertTrue(ret)

    def test_linesegment_5(self):
        ret: bool = self.ls.isInsideRectangle(Point().setAddress(4, 2))
        self.assertFalse(ret)

    def test_linesegment_6(self):
        ret: bool = self.ls.isInsideRectangle(Point().setAddress(3, 1))
        self.assertTrue(ret)

    def test_linesegment_7(self):
        ret: bool = self.ls.isInsideRectangle(Point().setAddress(1, -1))
        self.assertTrue(ret)

    def test_linesegment_8(self):
        """線分が交点を持つ
        """
        ls: LineSegment = LineSegment()
        ls.setPoints(Point().setAddress(2, 1), Point().setAddress(3, 0))

        pt = self.ls.getCrossPoint(ls)
        self.assertEqual(CrossPointStatus.EXIST, self.ls.status)
        self.assertIsNotNone(pt)
        assert(pt is not None)
        self.assertEqual(2.5, pt.x)
        self.assertEqual(0.5, pt.y)
        
    def test_linesegment_9(self):
        """線分が交点を持ち、交点が線分上
        """
        ls: LineSegment = LineSegment()
        ls.setPoints(Point().setAddress(2, 1), Point().setAddress(2.5, 0.5))

        pt = self.ls.getCrossPoint(ls)
        self.assertEqual(CrossPointStatus.EXIST, self.ls.status)
        self.assertIsNotNone(pt)
        assert(pt is not None)
        self.assertEqual(2.5, pt.x)
        self.assertEqual(0.5, pt.y)

    def test_linesegment_10(self):
        """線分を延長した直線は交わるが、線分外
        """
        ls: LineSegment = LineSegment()
        ls.setPoints(Point().setAddress(2, 1), Point().setAddress(1, 2))

        pt = self.ls.getCrossPoint(ls)
        self.assertEqual(CrossPointStatus.OUT_OF_LINESEGMENT, self.ls.status)
        self.assertIsNone(pt)

    def test_linesegment_11(self):
        """2線分が平行
        """
        ls: LineSegment = LineSegment()
        ls.setPoints(Point().setAddress(1, 0), Point().setAddress(3, 2))

        pt = self.ls.getCrossPoint(ls)
        self.assertEqual(CrossPointStatus.PARALLEL, self.ls.status)
        self.assertIsNone(pt)

    def test_linesegment_12(self):
        """2線分が同一直線上（重なりなし）
        """
        ls: LineSegment = LineSegment()
        ls.setPoints(Point().setAddress(4, 2), Point().setAddress(5, 3))

        pt = self.ls.getCrossPoint(ls)
        self.assertEqual(CrossPointStatus.ON_LINE, self.ls.status)
        self.assertIsNone(pt)

    def test_linesegment_13(self):
        """2線分が同一直線上（重なりあり）
        """
        ls: LineSegment = LineSegment()
        ls.setPoints(Point().setAddress(2, 0), Point().setAddress(4, 2))

        pt = self.ls.getCrossPoint(ls)
        self.assertEqual(CrossPointStatus.ON_LINE_OVERLAP, self.ls.status)
        self.assertIsNone(pt)

    def test_linesegment_14(self):
        """2線分が同一直線上（重なりあり、一方が他方を含む）
        """
        ls: LineSegment = LineSegment()
        ls.setPoints(Point().setAddress(1.5, -0.5), Point().setAddress(2.5, 0.5))

        pt = self.ls.getCrossPoint(ls)
        self.assertEqual(CrossPointStatus.ON_LINE_INCLUDED, self.ls.status)
        self.assertIsNone(pt)
