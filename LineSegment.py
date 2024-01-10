
from enum import Enum, auto, unique
import math
from typing import Self
from Point import Point
    
@unique
class CrossPointStatus(Enum):
    NOT_CALCULATED     = auto() # 未計算
    EXIST              = auto() # 交点が存在
    PARALLEL           = auto() # 2線分が平行
    ON_LINE            = auto() # 2線分が直線上にある
    ON_LINE_OVERLAP    = auto() # 2線分が直線上にあり重なっている
    ON_LINE_INCLUDED   = auto() # 2線分が直線上にあり、一方が他方に含まれている
    OUT_OF_LINESEGMENT = auto() # 交点があるが線分外

# 浮動小数点を０と比較する際の許容誤差
_ABS_TOL: float = 1e-10

class LineSegment:
    """線分クラス

    ２点を両端とする線分を表すクラス

    Attributes:
        pt1: 端点１
        pt2: 端点２
    
    Note:
        端点１と端点２に何らかの位置関係は規定されない
    """

    def __init__(self, pt1: Point | None = None, pt2: Point | None = None):
        self.pt1: Point = Point() if pt1 is None else pt1
        self.pt2: Point = Point() if pt2 is None else pt2
        self._cp_status = CrossPointStatus.NOT_CALCULATED

    def setPoints(self, pt1: Point, pt2: Point):
        """線分の両端を設定する

        Args:
            pt1: 一方の端点
            pt2: もう一方の端点
        """
        self.pt1 = Point().copyPoint(pt1)
        self.pt2 = Point().copyPoint(pt2)
        return self
    
    def copyLineSegment(self, ls: Self):
        """線分をコピーして、両端点を設定する

        Args:
            ls: 線分
        """
        self.pt1 = Point().copyPoint(ls.pt1)
        self.pt2 = Point().copyPoint(ls.pt2)
        return self

    @property
    def minx(self) -> float:
        return self.minxPt.x

    @property
    def minxPt(self) -> Point:
        if self.pt1.x < self.pt2.x:
            return self.pt1
        return self.pt2
    
    @property
    def maxx(self) -> float:
        return self.maxxPt.x

    @property
    def maxxPt(self) -> Point:
        if self.pt1.x < self.pt2.x:
            return self.pt2
        return self.pt1
    
    @property
    def miny(self) -> float:
        return self.minyPt.y

    @property
    def minyPt(self) -> Point:
        if self.pt1.y < self.pt2.y:
            return self.pt1
        return self.pt2
    
    @property
    def maxy(self) -> float:
        return self.maxyPt.y

    @property
    def maxyPt(self) -> Point:
        if self.pt1.y < self.pt2.y:
            return self.pt2
        return self.pt1
    
    @property
    def a(self) -> float:
        """線分を直線とした際の x の係数 a
        ax + by = c
        """
        return self.pt2.y - self.pt1.y

    @property
    def b(self) -> float:
        """線分を直線とした際の y の係数 b
        ax + by = c
        """
        return self.pt1.x - self.pt2.x

    @property
    def c(self) -> float:
        """線分を直線とした際の定数項 c
        ax + by = c
        """
        return self.pt1.x * self.pt2.y - self.pt1.y * self.pt2.x
    
    @property
    def status(self) -> CrossPointStatus:
        """線分の交点の状態を調べる

        getCrossPoint, hasCrossPoint, calcX, calcY 呼び出し後に、交点の
        状態が設定される

        Returns:
            交点の状態を表す enum
        """
        return self._cp_status

    def resetStatus(self):
        """線分の交点の状態を初期値に戻す
        """
        self._cp_status = CrossPointStatus.NOT_CALCULATED

    def isInLineSegment(self, pt: Point) -> bool:
        """線分上に Point があるか

        Args:
            pt: 判定対象の Point
        
        Returns:
            線分上にあれば true
        """
        return self.isOnLineByLineSegment(pt) and self.isInsideRectangle(pt)

    def isOnLineByLineSegment(self, pt: Point) -> bool:
        """線分を含む直線上に Point があるか

        Args:
            pt: 判定対象の Point
        
        Returns:
            直線上にあれば true
        """
        return math.isclose(self.c, self.a * pt.x + self.b * pt.y)
    
    def isInsideRectangle(self, pt: Point) -> bool:
        """線分の両端点が作る四角形内に Point があるか

        Args:
            pt: 判定対象の Point
        
        Returns:
            矩形内にあれば true
        """
        return self.minx <= pt.x and pt.x <= self.maxx and self.miny <= pt.y and pt.y <= self.maxy
        
    def hasCrossPoint(self, other: Self) -> bool:
        """線分の交点が存在するか否か

        Args:
            other: 線分

        Returns:
            交点が存在する場合は true, なければ false
        """
        pt = self._calcCrossPoint(other)
        return pt is not None

    def getCrossPoint(self, other: Self) -> Point | None:
        """線分の交点を求める

        Args:
            other: もう一方の線分
        Returns:
            交点の Point オブジェクト, 交点がない場合は None
        """
        return self._calcCrossPoint(other)

    def _calcCrossPoint(self, other: Self) -> Point | None:
        """線分の交点を求める

        Args:
            other: もう一方の線分
        Returns:
            交点の Point オブジェクト, 交点がない場合は None
        """
        d: float = other.a * self.b - self.a * other.b
        if math.isclose(d, 0, abs_tol=_ABS_TOL):
            # 2線分が平行
            self._cp_status = CrossPointStatus.PARALLEL

            if (self.isOnLineByLineSegment(other.pt1) or self.isOnLineByLineSegment(other.pt2)):
                # 同じ直線上に 2 線分がある
                self._cp_status = CrossPointStatus.ON_LINE

                if (self.isInLineSegment(other.pt1) or self.isInLineSegment(other.pt2)
                    or other.isInLineSegment(self.pt1) or other.isInLineSegment(self.pt2)):
                    # 線分が重なっている
                    self._cp_status = CrossPointStatus.ON_LINE_OVERLAP
                    if ((self.isInLineSegment(other.pt1) and self.isInLineSegment(other.pt2))
                        or (other.isInLineSegment(self.pt1) and other.isInLineSegment(self.pt2))):
                        # 一方が他方に含まれている
                        self._cp_status = CrossPointStatus.ON_LINE_INCLUDED
            return None

        x: float = (other.c * self.b - self.c * other.b) / d
        y: float = (self.c * other.a - other.c * self.a) / d

        # 有効範囲内か？
        pt: Point = Point().setAddress(x, y)
        if self.isInsideRectangle(pt) and other.isInsideRectangle(pt):
            self._cp_status = CrossPointStatus.EXIST
            return pt
        self._cp_status = CrossPointStatus.OUT_OF_LINESEGMENT
        return None

    def calcXIfExist(self, y: float) -> float:
        """線分上の x 座標値を求める

        Args:
            y: y 座標値
        Returns:
            線分上の x 座標値, 直線が x 軸に平行な場合および線分外の場合はエラーとする
        """
        result: float | None = self.calcX(y)
        if (result is not None and self.status == CrossPointStatus.EXIST):
            return result
        if (self.status == CrossPointStatus.PARALLEL):
            raise RuntimeError("linesegment is parallel to x axis")
        elif (self.status == CrossPointStatus.OUT_OF_LINESEGMENT):
            raise RuntimeError("linesegment is not cross to y")
        else:
            raise RuntimeError("unexpected error")
    
    def calcX(self, y: float) -> float | None:
        """線分上の x 座標値を求める

        Args:
            y: y 座標値
        Returns:
            線分上の x 座標値, 直線が x 軸に平行な場合および線分外の場合は None
        """
        if (math.isclose(self.a, 0, abs_tol=_ABS_TOL)):
            self._cp_status = CrossPointStatus.PARALLEL
            return None
        
        x: float = (self.c - self.b * y) / self.a

        pt: Point = Point().setAddress(x, y)
        if self.isInsideRectangle(pt):
            self._cp_status = CrossPointStatus.EXIST
            return x
        
        self._cp_status = CrossPointStatus.OUT_OF_LINESEGMENT
        return None
    
    def calcYIfExist(self, x: float) -> float:
        """線分上の y 座標値を求める

        Args:
            x: x 座標値
        Returns:
            線分上の y 座標値, 直線が y 軸に平行な場合および線分外の場合はエラーとする
        """
        result: float | None = self.calcY(x)
        if (result is not None and self.status == CrossPointStatus.EXIST):
            return result
        if (self.status == CrossPointStatus.PARALLEL):
            raise RuntimeError("linesegment is parallel to y axis")
        elif (self.status == CrossPointStatus.OUT_OF_LINESEGMENT):
            raise RuntimeError("linesegment is not cross to x")
        else:
            raise RuntimeError("unexpected error")
    
    def calcY(self, x: float) -> float | None:
        """線分上の y 座標値を求める

        Args:
            x: x 座標値
        Returns:
            線分上の y 座標値, 直線が y 軸に平行な場合および線分外の場合は None
        """
        if (math.isclose(self.b, 0, abs_tol=_ABS_TOL)):
            self._cp_status = CrossPointStatus.PARALLEL
            return None
        
        y: float = (self.c - self.a * x) / self.b

        pt: Point = Point().setAddress(x, y)
        if self.isInsideRectangle(pt):
            self._cp_status = CrossPointStatus.EXIST
            return y
        
        self._cp_status = CrossPointStatus.OUT_OF_LINESEGMENT
        return None


