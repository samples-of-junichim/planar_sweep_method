
import math
from enum import Enum, auto, unique
import sys
from dataclasses import dataclass
from Point import Point
from LineSegment import CrossPointStatus, LineSegment
from TwoThreeTree import Leaf, Node, TwoThreeTree

# for debug
#import datetime

@unique
class EventType(Enum):
    """イベント種類の enum

    平面走査法のイベント種類を表す
    """
    LEFT  = auto()  # 左端点
    CROSS = auto()  # 交点
    RIGHT = auto()  # 右端点


@dataclass
class BNode:
    """平面走査法で用いるイベント管理するための Node 要素
    """
    eventType: EventType     # イベント種類
    pt: Point                # イベントに対する Point, この X 座標がメインのキー
    ls: LineSegment          # Point が存在する線分
    ls2: LineSegment | None  # イベントが交点の場合の２つ目の線分

class LeafB(Leaf[BNode]):

    def __init__(self, val: BNode, parent: Node[BNode] | None):
        super().__init__(val, parent, self._get_leafb_key, self._comp_leafb_key)

    def _get_leafb_key(self, v: BNode) -> str:
        return f"({v.pt.x}, {v.pt.y}), {v.eventType}"
    
    def _comp_leafb_key(self, v1: BNode, v2: BNode) -> int:
        '''イベント要素の比較関数

        走査線上に端点および交点が複数存在する場合に対応できるように、
        x および y 座標を用いて同一 Node であるか判定する（x 座標が優先）
        
        そのうえで、イベントとしては交点を優先的に処理する
        （走査線上に交点と端点がある場合、先に交点を処理して線分を入れ替えて
        おかないと、端点追加に伴う上下の線分が正しく判定できなくなる）

        上記を踏まえると下記の優先順位で比較を行うこととする
            x 座標の大小
            イベントタイプ（交点、その他の順）、交点のほうが小さい（先に処理される）
            y 座標の大小
        
        Args:
            v1: 比較要素1
            v2: 比較要素2

        Returns:
            0: 一致,  負の値: v1 < v2,  正の値: v1 > v2
        '''
        if math.isclose(v1.pt.x, v2.pt.x):
            if v1.eventType == EventType.CROSS and v2.eventType != EventType.CROSS:
                return -1
            elif v1.eventType != EventType.CROSS and v2.eventType == EventType.CROSS:
                return 1
            else:
                #イベントタイプが同種類（交点同士または交点以外同士）の場合は y 座標を用いて判定する
                if math.isclose(v1.pt.y, v2.pt.y):
                    return 0
                if v1.pt.y < v2.pt.y:
                    return -1
                else:
                    return 1
        if v1.pt.x < v2.pt.x:
            return -1
        else:
            return 1    

def leafb_ctor(v: BNode, parent: Node[BNode]):
    return LeafB(v, parent)


@dataclass
class Sweepline:
    x: float   # 走査線の x 座標

@dataclass
class ANode:
    """平面走査法で用いる走査線上の線分を管理するための Node 要素
    """
    ls: LineSegment      # Point が存在する線分, 走査線上における線分の y 座標をキーとする

class LeafA(Leaf[ANode]):
    _delta_x : float = 1e-5
    _sweepline: Sweepline

    def __init__(self, val: ANode, parent: Node[ANode] | None, sweepline: Sweepline):
        super().__init__(val, parent,
                         # func_get_val -> str
                         #   走査線の x 座標における 線分の y 座標 を求める
                         lambda v: str(v.ls.calcYIfExist(sweepline.x)),
                         # func_comp -> int
                         #   走査線の x 座標における 2線分の y 座標 を比較する
                        self._comp)
        self._sweepline = sweepline

    def _comp(self, v1, v2) -> int:
        """走査線の x 座標における ２線分（ANodeとして与える）の y 座標 を比較する
            
            v1 の y 座標のほうが大きい場合に正の値を返す

        Args:
            v1: 線分を含む ANode
            v2: 線分を含む ANode

        Returns:
            v1 の y 座標 > v2 の y 座標 => 正の値
            v1 の y 座標 == v2 の y 座標 => 0
            v1 の y 座標 < v2 の y 座標 => 負の値
        """
        # 走査線上の y 座標を比較
        if (math.isclose(v1.ls.calcYIfExist(self._sweepline.x), v2.ls.calcYIfExist(self._sweepline.x))):
            # 走査線上の y 座標が同じ場合への対応

            # 線分が同じであれば、走査線上の同一点（同一線分）と考え、一致とする
            if ((v1.ls.pt1 == v2.ls.pt1 and v1.ls.pt2 == v2.ls.pt2) or
                (v1.ls.pt1 == v2.ls.pt2 and v1.ls.pt2 == v2.ls.pt1)):
                return 0
            
            # 異なる線分同士の場合は、交点である可能性が高い。なので、少しずらして線分の上下を判定する
            try:
                if (math.isclose(v1.ls.calcYIfExist(self._sweepline.x + self._delta_x), v2.ls.calcYIfExist(self._sweepline.x + self._delta_x))):
                    return 0
                elif (v1.ls.calcYIfExist(self._sweepline.x + self._delta_x) < v2.ls.calcYIfExist(self._sweepline.x + self._delta_x)):
                    return -1
                elif (v1.ls.calcYIfExist(self._sweepline.x + self._delta_x) > v2.ls.calcYIfExist(self._sweepline.x + self._delta_x)):
                    return 1
                else:
                    # ここにはこないはず
                    return 0
            except RuntimeError as e:
                raise RuntimeError(f"exception occured, comparing 2 lines: {v1.ls.status = }, {v2.ls.status = }, sweep line x is {self._sweepline.x}") from e
            
        elif (v1.ls.calcYIfExist(self._sweepline.x) < v2.ls.calcYIfExist(self._sweepline.x)):
            return -1
        elif (v1.ls.calcYIfExist(self._sweepline.x) > v2.ls.calcYIfExist(self._sweepline.x)):
            return 1
        # ここにはこないはず
        raise RuntimeError(f"invalid compare y values, sweepline x is {self._sweepline.x}")

class SweepLineMethod:
    """平面走査法

    与えられた全線分の全交点を求める

    Y軸に平行な走査線を、X軸に沿ってマイナス方向からプラス方向に走査させて、
    交点を求める

    _L         : 線分のリスト
    _sweepline : 走査線
    _A         : 走査線上に存在する線分の配列, 2-3木で管理
    _B         : イベントの配列, 2-3木で管理
    _crosses   : 交点のリスト
    """

    def __init__(self, lses: list[LineSegment]):
        """コンストラクタ

        Args:
            lses  線分のリスト
        """
        self._L: list[LineSegment] = lses

        # 平面走査法で用いる配列を準備
        self._sweepline: Sweepline = Sweepline(-sys.float_info.max)
        self._A: TwoThreeTree[LeafA, ANode] = TwoThreeTree[LeafA, ANode](lambda v, p : LeafA(v, p, self._sweepline)) # sweepline が必要で、かつ実行時にバインドしたいので、lambdaで定義する
        self._B: TwoThreeTree[LeafB, BNode] = TwoThreeTree[LeafB, BNode](leafb_ctor)

        # 交点のリスト
        self._crosses: list[Point] = []

    def getCrossPoints(self) -> list[Point]:
        return self._crosses

    def exec(self):
        """平面走査法の実行
        """

        # 初期化
        self._init()

        # line sweep
        while(True):
            lfb: Leaf[BNode] | None = self._B.minimum()

            # for debug
            #self._B.visualizeGraph(True, "tree_b_" + datetime.datetime.now().isoformat())

            if lfb is None:
                break
            if not isinstance(lfb, LeafB):
                raise RuntimeError("unknown minimum leaf")
            
            # 走査線を移動
            self._sweepline.x = lfb.cargo.pt.x

            # イベントに応じて処理を分岐
            if lfb.cargo.eventType == EventType.LEFT:
                self._procLeft(lfb)

            elif lfb.cargo.eventType == EventType.RIGHT:
                self._procRight(lfb)

            elif lfb.cargo.eventType == EventType.CROSS:
                self._procCross(lfb)
            
            # 次のイベントへ
            self._B.delete(lfb.cargo)
        return
    
    def _procLeft(self, lfb: LeafB):
        """左端点のイベントを処理

        走査線上の線分を管理する木にノードを追加

        Args:
            lfb  線分の端点
        """

        # 走査線上の線分として追加                
        an: ANode = ANode(lfb.cargo.ls)
        lfa: Leaf[ANode] = self._A.insert(an)

        # 追加線分の前後の交点を確認し、あれば追加
        prev: Leaf[ANode] | None = self._A.predecessor(lfa)
        succ: Leaf[ANode] | None = self._A.successor(lfa)

        if prev is not None:
            self._checkCrossPoint(lfa.cargo, prev.cargo)
        if succ is not None:
            self._checkCrossPoint(lfa.cargo, succ.cargo)

        return

    def _procRight(self, lfb: LeafB):
        """右端点のイベントを処理

        走査線上の線分を管理する木からノードを削除
        
        Args:
            lfb  線分の端点
        """

        # 端点に対応する走査線上の線分
        an: ANode = ANode(lfb.cargo.ls)
        lfa: Leaf[ANode] | None = self._A.search(an)

        if lfa is None:
            raise RuntimeError(f"right point ({lfb.cargo.pt.x}, {lfb.cargo.pt.y}) was not found in line segments on sweep line: {lfb.cargo.pt.x}")

        # 削除線分の前後の Node を取得
        prev: Leaf[ANode] | None = self._A.predecessor(lfa)
        succ: Leaf[ANode] | None = self._A.successor(lfa)

        # 削除
        self._A.delete(lfa.cargo)

        # 削除線分の前後の線分に対する交点を確認し、あれば追加
        if prev is not None and succ is not None:
            self._checkCrossPoint(prev.cargo, succ.cargo)
        return
    
    def _procCross(self, lfb: LeafB):
        """交点のイベントを処理

        走査線上の線分を管理する木の順序を入れ替え
        
        Args:
            lfb  線分の交点
        """
        # 交点なので、必ずあるはず
        if lfb.cargo.ls2 is None:
            raise RuntimeError("no 2nd line segment")

        # 交点に対応する走査線上の点
        #   走査線が交点に達する前の時点で、下側の線分上のもの（Y座標が小さいもの）
        lfa_lower: Leaf[ANode] | None = self._A.search(
            ANode(lfb.cargo.ls)
        )
        if lfa_lower is None:
            lfa_lower: Leaf[ANode] | None = self._A.search(
                ANode(lfb.cargo.ls2)
            )
        if lfa_lower is None:
            raise RuntimeError("cross point was not found on lower line segment")

        #   走査線が交点に達する前の時点で、上側の線分上のもの（Y座標が大きいもの）
        lfa_upper: Leaf[ANode] | None = self._A.successor(lfa_lower)
        if lfa_upper is None:
            raise RuntimeError("cross point was not found on upper line segment")
        
        # 線分の入れ替え
        #   2-3 木内部の並びを変更するため、葉を削除後改めて追加すれば、
        #   その時の走査線に対応した位置に挿入される
        self._A.delete(lfa_lower.cargo)
        lfa_upper_switched: Leaf[ANode] | None = self._A.insert(lfa_lower.cargo)
        lfa_lower_switched: Leaf[ANode] | None = lfa_upper

        # 新しい交点の探索

        # 交点通過後、上側になる線分と、さらにその上の線分との交点
        lfa_next: Leaf[ANode] | None = self._A.successor(lfa_upper_switched)
        if lfa_next is not None:
            self._checkCrossPoint(lfa_upper_switched.cargo, lfa_next.cargo)
        # 交点通過後、下側になる線分と、さらにその下の線分との交点
        lfa_prev: Leaf[ANode] | None = self._A.predecessor(lfa_lower_switched)
        if lfa_prev is not None:
            self._checkCrossPoint(lfa_lower_switched.cargo, lfa_prev.cargo)

        return

    def _checkCrossPoint(self, target: ANode, other: ANode):
        """２線分の交点をチェック

        もし、交点が見つかれば、イベント木へ追加

        Args:
            target  線分１
            other   線分２
        """
        cp : Point | None = target.ls.getCrossPoint(other.ls)

        if cp is not None:
            addpt: BNode = BNode(
                EventType.CROSS,
                cp,
                target.ls,
                other.ls)
            
            # すでに発見した交点であれば何もしない
            if self._isExistCrossPoint(cp):
                return
            
            # 交点リストへ追加
            self._crosses.append(cp)

            # 交点と同じ座標の端点があるかチェック
            lfb_end: Leaf[BNode] | None = self._B.search(
                BNode(
                    EventType.RIGHT, # CROSS 以外を指定
                    cp,
                    target.ls,       # other.ls でもよい
                    None))
            if lfb_end is not None:
                # 端点がある場合は、交点としてイベント木には追加しない
                return

            # イベントへ交点を追加
            self._B.insert(addpt)
        return
    
    def _init(self):
        """平面走査法実行前の初期化

        対象線分の両端点をイベント木に追加        
        """
        # 線分の端点を B に追加
        ls: LineSegment
        for ls in self._L:
            # 線分の左端点
            bn: BNode = BNode(
                EventType.LEFT,
                ls.minxPt,
                ls,
                None)
            self._B.insert(bn)

            # 線分の右端点
            bn: BNode = BNode(
                EventType.RIGHT,
                ls.maxxPt,
                ls,
                None)
            self._B.insert(bn)

        # Aは 初期化時点では空のため、何もしない
        return

    def _isExistCrossPoint(self, cp: Point):
        """交点が発見済みか否か

        Args:
            cp  検査対象の交点

        Returns:
            true: 交点が発見済み    false: 交点未発見
        """
        ret: Point | None = next((pt for pt in self._crosses if pt.x == cp.x and pt.y == cp.y), None)
        return isinstance(ret, Point)
    
