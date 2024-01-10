
from doctest import UnexpectedException
from enum import Enum, auto, unique
import math
from typing import Self

class Point:
    """点クラス

    ２次元平面上の点を表すクラス

    Attributes:
        x: x 座標
        y: y 座標
    """

    def __init__(self, x: float | None = None, y: float | None = None):
        self.x : float = 0 if x is None else x
        self.y : float = 0 if y is None else y

    def setAddress(self, x: float, y: float):
        """点の座標を設定する

        Args:
            x: x座標
            y: y座標
        """
        self.x = x
        self.y = y
        return self

    def copyPoint(self, pt: Self):
        """点をコピーして、座標を設定する

        Args:
            pt: Point オブジェクト
        """
        self.x = pt.x
        self.y = pt.y
        return self
        
    def __eq__(self, other: Self) -> bool:
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
