
import math
from enum import Enum, auto, unique
import sys
from dataclasses import dataclass
from Point import Point
from LineSegment import CrossPointStatus, LineSegment
from TwoThreeTree import Leaf, Node, TwoThreeTree

# for debug
#import datetime

# 走査線を移動させる際の微小値
_DELTA = 1e-5

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
    lnId: int | None         # 線分 ID, 端点追加時のみ割り当てる

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

        また、線分の端点が重なっている場合へ対応するため、以下のようにする
        ・イベント種類が異なる場合は、左端点を優先する（走査線上に線分を追加するのを優先する）
        ・線分 ID により、同一 Node であるかを判定する（一方の線分 ID がないような場合は同じとみなす）

        上記を踏まえると下記の優先順位で比較を行うこととする
            x 座標の大小
            イベントタイプ（交点、その他の順）、交点のほうが小さい（先に処理される）
            y 座標の大小
            端点が異なる場合は、イベントタイプ（左端点、右端点の順）、左端点を持つ方が小さい（先に処理される）
            線分 ID（交点同士以外の場合）、線分 ID が小さい（先に処理される）
        
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
                    # y 座標が同じ場合は、交点同士かそれ以外かで判定方法を切り替える

                    # 交点同士の場合
                    if v1.eventType == EventType.CROSS and v2.eventType == EventType.CROSS:
                        return 0
                    
                    # 交点同士の比較以外は 線分ID で同一か否かを判定
                    #   線分の端点に該当するため ID が異なっていれば、異なる点として扱う
                    if v1.lnId is None or v2.lnId is None:
                        return 0
                    else:
                        # 線分 ID がある場合は、先に、イベントタイプで判定
                        #   イベントタイプ異なる場合は、左端点を優先する(走査線上に追加する処理を優先する）
                        if v1.eventType == EventType.LEFT and v2.eventType == EventType.RIGHT:
                            return -1
                        elif v1.eventType == EventType.RIGHT and v2.eventType == EventType.LEFT:
                            return 1
                    
                        if v1.lnId > v2.lnId:
                            return 1
                        elif v1.lnId < v2.lnId:
                            return -1
                        else:
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
    _delta_x : float = -1 * _DELTA

    def __init__(self, val: ANode, parent: Node[ANode] | None, sweepline: Sweepline):
        super().__init__(val, parent,
                         # func_get_val -> str
                         #   走査線の x 座標における 線分の y 座標 を求める
                         lambda v: str(v.ls.calcYIfExist(sweepline.x)),
                         # func_comp -> int
                         #   走査線の x 座標における 2線分の y 座標 を比較する
                        self._comp)
        self._sweepline: Sweepline = sweepline

    def _comp(self, v1: ANode, v2: ANode) -> int:
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
            #   ずらすのは走査線の進行方向の逆向きとする（交点通過により並びが変わらないようにするため）
            y1: float | None
            y2: float | None
            try:
                y1 = v1.ls.calcYIfExist(self._sweepline.x + LeafA._delta_x)
            except:
                y1 = None
            try:
                y2 = v2.ls.calcYIfExist(self._sweepline.x + LeafA._delta_x)
            except:
                y2 = None

            if y1 is not None and y2 is not None:
                if math.isclose(y1, y2):
                    return 0
                elif y1 < y2:
                    return -1
                elif y1 > y2:
                    return 1
                
            # すらした結果、一方が範囲外で計算できない場合、走査線上に左端点がある線分と
            # そうではない線分からなると思われるので、一致ではなく、走査線上に左端点がある線分を優先させる
            #   もれなく交点を求められるように、走査線上に線分を追加するのを優先させるという意図
            if v1.ls.status == CrossPointStatus.OUT_OF_LINESEGMENT and v2.ls.status == CrossPointStatus.EXIST:
                # v1 が左端点 -> v1 を優先
                return -1
            elif v1.ls.status == CrossPointStatus.EXIST and v2.ls.status == CrossPointStatus.OUT_OF_LINESEGMENT:
                # v2 が左端点 -> v2 を優先
                return 1
            # すらした結果、共に範囲外で計算できない場合などは、例外を投げる
            raise RuntimeError(f"line calculation error, comparing 2 lines: {v1.ls.status = }, {v2.ls.status = }, sweep line x is {self._sweepline.x}")
            
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
    _delta_x : float = _DELTA       # 交点を持つ線分の上下判定の際に用いる微小値
    _PARALLEL_DELTA_X: float = 1.0  # 走査線に平行な線分の判定で用いる値

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
            #self._A.visualizeGraph(True, "tree_a_" + datetime.datetime.now().isoformat())

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

        # 走査線に平行な場合
        if lfb.cargo.ls.b == 0:
            # 端点を通る X 軸に平行な線を規定
            #   線分の式は b * y = c となる。その際、2点の x 座標の差分により b = 2 * _PARALLEL_DELTA_X と求められる。
            #   このため、 _PARALLEL_DELTA_X が小さすぎる値の場合、計算誤差により問題が生じる
            ln1: LineSegment = LineSegment(
                Point(self._sweepline.x - SweepLineMethod._PARALLEL_DELTA_X, lfb.cargo.ls.miny),
                Point(self._sweepline.x + SweepLineMethod._PARALLEL_DELTA_X, lfb.cargo.ls.miny))
            ln2: LineSegment = LineSegment(
                Point(self._sweepline.x - SweepLineMethod._PARALLEL_DELTA_X, lfb.cargo.ls.maxy),
                Point(self._sweepline.x + SweepLineMethod._PARALLEL_DELTA_X, lfb.cargo.ls.maxy))
            an1: ANode = ANode(ln1)
            an2: ANode = ANode(ln2)
            # 走査線に平行な線分と交点を持つ線分のリスト
            #  an1 と an2 の線分範囲にある _A の要素が、現在の走査線と交点を持つ線分となる
            lst: list[Leaf[ANode]] = self._A.range(an1, an2)
            for lf in lst:
                self._crosses.append(Point(self._sweepline.x, float(lf.val))) # Leaf.val が Y 座標以外を戻す場合は要修正
            # 交点イベントの追加は行わない
            return

        # その他の場合

        # 走査線上の線分として追加                
        sweep_line_x_old = self._sweepline.x
        an: ANode = ANode(lfb.cargo.ls)
        try:
            lfa: Leaf[ANode] = self._A.insert(an)
        except RuntimeError as e:
            # 左端点が交点でもある場合、追加時の走査線上の上下判定で範囲外のエラーとなる
            # このため、走査線を少しだけ進めて再度追加を行う
            
            #print(e)
            try:
                self._sweepline.x = self._sweepline.x + SweepLineMethod._delta_x
                lfa: Leaf[ANode] = self._A.insert(an)

            except RuntimeError as e2:
                raise RuntimeError(f"exception occured: cannot add LEFT endpoint: ({lfb.cargo.pt.x}, {lfb.cargo.pt.y})") from e2

        # 走査線を元に戻す
        self._sweepline.x = sweep_line_x_old

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

        # 走査線に平行な場合
        if lfb.cargo.ls.b == 0:
            # _A に追加されていないので、なにもしない
            return
        
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

        # 2-3 木の葉の swap メソッドを利用して走査線上の講演を入れ替える
        #   走査線上の線分は交点通過前の並びに従うので、必ず指定した線分に対する葉を取得できる
        #   その後、走査線を交点以降に動かし、上下を判定し、入れ替えを行う

        # 交点に対応する走査線上の線分の存在
        lfa_ls1: Leaf[ANode] | None = self._A.search(
            ANode(lfb.cargo.ls)
        )
        if lfa_ls1 is None:
            raise RuntimeError(f"line segment for cross point ({lfb.cargo.pt.x}, {lfb.cargo.pt.y}) was not found on sweep line, x = {self._sweepline.x}")

        # 交点に対応する走査線上の線分の存在
        lfa_ls2: Leaf[ANode] | None = self._A.search(
                ANode(lfb.cargo.ls2)
            )
        if lfa_ls2 is None:
            raise RuntimeError(f"line segment for cross point ({lfb.cargo.pt.x}, {lfb.cargo.pt.y}) was not found on sweep line, x = {self._sweepline.x}")
        
        # 上下を判定
        sweep_line_x_old: float = self._sweepline.x
        self._sweepline.x = self._sweepline.x + SweepLineMethod._delta_x

        ret: int = lfa_ls1.compareCargo(lfa_ls2.cargo)
        if  ret == 0:
            raise RuntimeError(f"two lines are same at cross point ({lfb.cargo.pt.x}, {lfb.cargo.pt.y}), sweep line, x = {self._sweepline.x}")
        elif ret > 0:
            lfa_upper_switched: Leaf[ANode] | None = lfa_ls1
            lfa_lower_switched: Leaf[ANode] | None = lfa_ls2
        else:
            lfa_upper_switched: Leaf[ANode] | None = lfa_ls2
            lfa_lower_switched: Leaf[ANode] | None = lfa_ls1

        # 走査線位置を元に戻しておく
        self._sweepline.x = sweep_line_x_old

        # 入れ替え
        self._A.swap(lfa_upper_switched, lfa_lower_switched)

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
                other.ls,
                None)
            
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
                    None,
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
        lineId: int = 0
        ls: LineSegment
        for ls in self._L:
            # 線分の左端点
            bn: BNode = BNode(
                EventType.LEFT,
                ls.minxPt,
                ls,
                None,
                lineId)
            self._B.insert(bn)

            # 線分の右端点
            bn: BNode = BNode(
                EventType.RIGHT,
                ls.maxxPt,
                ls,
                None,
                lineId)
            self._B.insert(bn)
            lineId += 1

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
    
