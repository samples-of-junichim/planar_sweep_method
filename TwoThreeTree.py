"""2-3木モジュール
"""

from abc import ABC, abstractmethod
from enum import Enum, auto, unique
from typing import Callable, Generic, Self, TypeVar, Union

from graphviz import Digraph

@unique
class NodeChildPos(Enum):
    LEFT  = auto()
    MID   = auto()
    RIGHT = auto()

T=TypeVar("T")
class Node(ABC, Generic[T]):
    """2-3木の節点を表す抽象クラス
    """

    def __init__(self, parent: Union["Node", None]): # Self を指定しても、 Node の派生クラスにはならない
        self.parent: Self | None = parent

    @property
    def isRoot(self) -> bool:
        return self.parent is None

    @property
    @abstractmethod
    def isInternal(self) -> bool:
        raise NotImplementedError()

    @property
    @abstractmethod
    def isLeaf(self) -> bool:
        raise NotImplementedError()

    @property
    def left(self) -> Self | None:
        return None

    @left.setter
    def left(self, node: Self | None):
        pass
        
    @property
    def mid(self) -> Self | None:
        return None
    
    @mid.setter
    def mid(self, node: Self | None):
        pass
        
    @property
    def right(self) -> Self | None:
        return None

    @right.setter
    def right(self, node: Self | None):
        pass

    @property
    def numberOfChild(self) -> int:
        count: int = 0
        if self.left is not None:
            count += 1
        if self.mid is not None:
            count += 1
        if self.right is not None:
            count += 1
        return count
    
    @property
    def cargo(self) -> T:
        raise NotImplementedError()
    
    @property
    def val(self) -> str:
        raise NotImplementedError()
    

class InternalNode(Node[T]):
    """ 2-3木の葉以外の内部節点（根を含む、内部の Node）を表すクラス

    この内部節点クラスは以下の特徴を持つ

    2または3の子要素を持つ
    子要素は InternalNode または Leaf である
    left -> mid -> right の順番で埋まっていく
    以下の２つの値を取り出すことが可能
        left の部分木の最大要素
        mid の部分木の最大要素
    """

    def __init__(self, parent: Node[T] | None):
        """初期化

        Args:
            parent: 親 Node
        """
        super().__init__(parent)

        self._left: Node[T] | None = None
        self._mid: Node[T] | None = None
        self._right: Node[T] | None = None

        self.left_max_node: Node[T] | None = None
        self.mid_max_node: Node[T] | None = None

    @property
    def isInternal(self) -> bool:
        return True
    
    @property
    def isLeaf(self) -> bool:
        return not self.isInternal
    
    @property
    def left(self) -> Node[T] | None:
        return self._left

    @left.setter
    def left(self, node: Node[T] | None):
        #super().left = node
        if (self._mid is not None or self._right is not None) and node is None:
            raise RuntimeError("left cannot set None before mid or right is not None.")
        self._left = node

    @property
    def mid(self) -> Node[T] | None:
        return self._mid

    @mid.setter
    def mid(self, node: Node[T] | None):
        #super().mid = node
        if self._left is None and node is not None:
            raise RuntimeError("mid cannot set because left is None.")
        if self._right is not None and node is None:
            raise RuntimeError("mid cannot set None before right is not None.")
        self._mid = node

    @property
    def right(self) -> Node[T] | None:
        return self._right

    @right.setter
    def right(self, node: Node[T] | None):
        #super().right = node
        if self._mid is None and node is not None:
            raise RuntimeError("right cannot set because mid is None.")
        self._right = node

    @property
    def left_max_val(self) -> str:
        if self.left_max_node is None:
            # root 要素のみの場合が該当する。それ以外は起こらないはず
            raise RuntimeError("invalid method call. left max node is None.")
        return self.left_max_node.val

    @property
    def mid_max_val(self) -> str:
        if self.mid_max_node is None:
            # 葉が１つの場合には、起こりえる状況だが、呼び出し元側でチェックすることを期待
            raise RuntimeError("invalid method call. mid max node is None.")
        return self.mid_max_node.val

class Leaf(Node[T]):
    """2-3木の葉クラス

    Node クラスの派生とする
    """

    def __init__(self, cargo: T, parent: Node[T] | None, func_get_val: Callable[[T], str], func_comp: Callable[[T, T], int]):
        """初期化

        Args:
            cargo: 葉が保持するオブジェクト
            parent: 親 Node
            func_get_val: 葉から値を取得する関数
            func_comp: 葉の値の比較関数, func_comp(a, b) で呼ぶと, a > b => 正の値, a == b => 0, a < b => 負の値
        """
        super().__init__(parent)

        self._cargo = cargo
        self._func_get_val = func_get_val
        self._func_comp = func_comp

    @property
    def isInternal(self) -> bool:
        return False
    
    @property
    def isLeaf(self) -> bool:
        return not self.isInternal
    
    @property
    def cargo(self) -> T:
        return self._cargo
    
    @property
    def val(self) -> str:
        return self._func_get_val(self._cargo)

    def compareCargo(self, other: T) -> int:
        """格納している要素の比較
        
        本 Leaf オブジェクトが保持するオブジェクトの値を比較する

        Args:
            other  格納要素と同じ型のオブジェクト

        Returns:
            0: 一致,  負の値: 本 Leaf オブジジェクト < other,  正の値: 本 Leaf オブジェクト > other
        """
        return self._func_comp(self._cargo, other)
    
    def isEqualCargo(self, other: T) -> bool:
        """格納している要素が等しいか否か判定
        
        本 Leaf オブジェクトが保持するオブジェクトの値を比較する

        Args:
            other  格納要素と同じ型のオブジェクト

        Returns:
            True: 一致,  False: 不一致
        """
        return self.compareCargo(other) == 0
    
    def __eq__(self, other: Self) -> bool:
        """比較演算子
        
        本 Leaf オブジェクトが保持するオブジェクトの値を比較する
            
        Args:
            other  格納要素と同じ型のオブジェクト

        Returns:
            True: 一致,  False: 不一致
        """
        return self.isEqualCargo(other.cargo)


NL = TypeVar("NL", bound=Leaf)
class TwoThreeTree(Generic[NL, T]): # T は Node の型パラメータと一致することを想定
    """2-3木クラス

    2-3木を表すクラス
    """
    def __init__(self, func_leaf_ctor: Callable[[T, Node[T]], NL]):
        """初期化

        根の Node を作成する
        作成時点では root は子要素を一つも持たない点に注意

        Args:
            func_leaf_ctor: 値オブジェクト T より 葉の要素を作成する関数, 第1引数: 値オブジェクト T, 第2引数: 親ノード
        """
        self.root: InternalNode[T] = InternalNode[T](None)
        self._func_leaf_ctor = func_leaf_ctor

    @property
    def size(self) -> int:
        """2-3木全体のノード数

        Returns:
            内部節点＋葉のノード数
        """
        return self.__size(self.root)

    def __size(self, nd: Node[T] | None) -> int:
        if nd is None:
            return 0
        return self.__size(nd.left) + self.__size(nd.mid) + self.__size(nd.right) + 1

    @property
    def leafSize(self) -> int:
        """2-3木の葉の数

        Returns:
            葉の数
        """
        return self.__leaf_size(self.root)

    def __leaf_size(self, nd: Node[T] | None) -> int:
        if nd is None:
            return 0
        return self.__leaf_size(nd.left) + self.__leaf_size(nd.mid) + self.__leaf_size(nd.right) + (1 if isinstance(nd, Leaf) else 0)

    @property
    def height(self) -> int:
        """2-3木の高さ

        Returns:
            2-3木の高さ
        """
        nd: Node[T] | None = self.root
        count: int = 0
        while(True):
            if nd is None:
                return count
            
            count = count + 1
            if isinstance(nd, Leaf):
                return count
            if nd.left is None:
                return count
            nd = nd.left

    def search(self, target: T) -> Leaf[T] | None:
        """検索

        引数で与えられたオブジェクトの値と同じ値を持つ Node を返す

        Args:
            target: 検索対象の要素
        """
        result: Node[T] = self._search_raw(target)
        if isinstance(result, Leaf):
            return result
        else:
            return None

    def _search_raw(self, target: T) -> Node[T]:
        """低レベルの検索

        引数で与えられたオブジェクトの値と同じ値を持つ Leaf を返す
        もし、 同じ値の Leaf が見つからない場合は Leaf があるであろう
        節点の Node を返す

        見つかったかどうかは戻り値のインスタンスを調べることで判定可能
        """
        nd: Node[T] | None = self.root

        # root のみの場合へ対応
        if nd.left_max_node is None:
            return nd

        parent: InternalNode[T] = nd
        while(nd is not None):

            # 葉に到達した時
            if nd.isLeaf:
                if not isinstance(nd, Leaf):
                    raise RuntimeError("invalid structure. maybe logical error")
                if nd.isEqualCargo(target):
                     return nd
                else:
                    return parent

            # 中間の節点
            if not isinstance(nd, InternalNode):
                raise RuntimeError("invalid node type.")

            parent = nd
            if nd.left_max_node is None:
                # 中間の節点があるのに、左側に葉がないのは、ありえない
                raise RuntimeError("invalid structure. maybe logical error")
            
            if not isinstance(nd.left_max_node, Leaf):
                # 左側の最大要素は常に葉
                raise RuntimeError("invalid structure. maybe logical error")

            if nd.left_max_node.compareCargo(target) >= 0:
                nd = nd.left
            else:
                if nd.mid_max_node is None:
                    # 中央がない場合
                    return parent
                else:
                    if not isinstance(nd.mid_max_node, Leaf):
                        # 中央の最大要素は常に葉
                        raise RuntimeError("invalid structure. maybe logical error")
                    if nd.left_max_node.compareCargo(target) < 0 and nd.mid_max_node.compareCargo(target) >= 0:
                        nd = nd.mid
                    else:
                        # 中央の最大要素より大きいけど、 右の子がない場合へ対応
                        if nd.right is None:
                            nd = nd.mid
                        else:
                            nd = nd.right
        
        # 見つからなかった場合
        return parent

    def maximum(self) -> Leaf[T] | None:
        """2-3木に格納されている最大の値を持つ要素を取得

        Returns:
            最大の要素, 要素が一つもない場合は None
        """
        return self._maximum_raw(self.root)

    def _maximum_raw(self, nd: Node[T] | None) -> Leaf[T] | None:
        """ある Node 以下で、最大の値を持つ要素を取得

        Returns:
            最大の要素, 要素が一つもない場合は None
        """
        if nd is None:
            return None
        while (True):
            if isinstance(nd, Leaf):
                return nd
            
            if nd.right is not None:
                nd = nd.right
            elif nd.mid is not None:
                nd = nd.mid
            elif nd.left is not None:
                nd = nd.left
            else:
                return None

    def minimum(self) -> Leaf[T] | None:
        """2-3木に格納されている最小の値を持つ要素を取得

        Returns:
            最小の要素, 要素が一つもない場合は None
        """
        return self._minimum_raw(self.root)
    
    def _minimum_raw(self, nd: Node[T] | None) -> Leaf[T] | None:
        """ある Node 以下で、最小の値を持つ要素を取得

        Returns:
            最小の要素, 要素が一つもない場合は None
        """
        if nd is None:
            return None
        while (True):
            if isinstance(nd, Leaf):
                return nd
            
            if nd.left is not None:
                nd = nd.left
            else:
                return None

    def successor(self, obj: Leaf[T]) -> Leaf[T] | None:
        """引数の要素の次の要素を取得

        Args:
            obj: 基準となる要素
        
        Returns:
            次の要素, None 見つからない（obj に対する葉がない場合も含む）
        """
        nd: Node[T] = self._search_raw(obj.cargo)
        if not isinstance(nd, Leaf):
            return None

        # 次の要素を含む部分木を見つける
        nxt: Node[T] | None = self._find_next_subtree_recursive(nd)

        # 部分木の最小要素を取得
        return self._minimum_raw(nxt)

    def _find_next_subtree_recursive(self, nd: Node[T]) -> Node[T] | None:
        while(True):
            tmp: Node[T] | None = self._find_next_subtree_as_siblings(nd)
            if tmp is not None:
                return tmp
            
            # 一つ上の階層へ移動
            if nd.parent is None:
                return None
            nd = nd.parent

    def _find_next_subtree_as_siblings(self, nd: Node[T]) -> Node[T] | None:
        p: Node[T] | None = nd.parent

        if p is None:
            return None
        if nd is p.left:
            return p.mid
        elif nd is p.mid:
            return p.right
        return None
    
    def predecessor(self, obj: Leaf[T]) -> Leaf[T] | None:
        """引数の要素の前の要素を取得

        Args:
            obj: 基準となる要素
        
        Returns:
            前の要素, None 見つからない（obj に対する葉がない場合も含む）
        """
        nd: Node[T] = self._search_raw(obj.cargo)
        if not isinstance(nd, Leaf):
            return None

        # 前の要素を含む部分木を見つける
        prv: Node[T] | None = self._find_prev_subtree_recursive(nd)

        # 部分木の最大要素を取得
        return self._maximum_raw(prv)

    def _find_prev_subtree_recursive(self, nd: Node[T]) -> Node[T] | None:
        while(True):
            tmp: Node[T] | None = self._find_prev_subtree_as_siblings(nd)
            if tmp is not None:
                return tmp
            
            # 一つ上の階層へ移動
            if nd.parent is None:
                return None
            nd = nd.parent

    def _find_prev_subtree_as_siblings(self, nd: Node[T]) -> Node[T] | None:
        p: Node[T] | None = nd.parent

        if p is None:
            return None
        if nd is p.right:
            return p.mid
        elif nd is p.mid:
            return p.left
        return None

    def insert(self, obj: T) -> Leaf[T]:
        """要素の追加

        引数で与えられた obj を内部に持つ葉を作成して、木に追加する
        もし、引数の obj が既に存在していた場合は、なにもしない

        当該要素を追加したのち、2-3木が保たれるように再構築を行う

        Args:
            obj: 追加対象の要素

        Returns:
            2-3 木における追加した要素に該当する Leaf
        """

        # 挿入場所を見つける
        result: Node[T] = self._search_raw(obj)

        if not isinstance(result, InternalNode):
            # 既に挿入済み
            # TODO 同じ値の場合はどう扱う？
            if isinstance(result, Leaf):
                return result
            else:
                raise RuntimeError("Node is not Leaf.")
        
        # 2-3木を再構成
        parent: InternalNode[T] = result

        # 挿入するオブジェクトに対する葉を生成
        leaf: Leaf[T] = self._func_leaf_ctor(obj, parent)

        # 葉を木に追加
        inter: InternalNode[T] | None = self._insert_leaf(parent, leaf)

        # 中間要素の追加がない場合
        if inter is None:
            # 最大要素のアップデート
            self._update_max_node(leaf.parent)
            return leaf

        # 中間要素が増えた場合
        base: InternalNode[T] = parent                # 葉の追加先となる基準の内部節点
        target: InternalNode[T] | None = base.parent
        while(True):

            # base が root の時
            if target is None:
                new_root: InternalNode[T] = InternalNode[T](None)

                base.parent = new_root
                new_root.left = base
                inter.parent = new_root
                new_root.mid = inter

                # root を更新
                self.root = new_root

                # 最大要素のアップデート
                self._update_max_node(self.root)
                break
            
            if target.left is None or target.mid is None:
                raise RuntimeError("internal error: each internal node must be at least 2 children.")
            
            if target.right is None:
                # 子要素が２個
                if base is target.left:
                    # 左子要素が増加
                    target.right = target.mid
                    target.mid = inter
                else:
                    # 中央子要素が増加
                    target.right = inter

                # 最大要素のアップデート
                self._update_max_node(target)
                break
            else:
                # 子要素が３個
                if base is target.left:
                    # 左子要素が増加
                    inter = self._insert_leaf_with_inter(target, target.left, inter, target.mid, target.right)
                elif base is target.mid:
                    # 中央子要素が増加
                    inter = self._insert_leaf_with_inter(target, target.left, target.mid, inter, target.right)
                else:
                    # 右子要素が増加
                    inter = self._insert_leaf_with_inter(target, target.left, target.mid, target.right, inter)
                # 木の上へ
                base = target
                target = target.parent
            
        # 追加要素を返す
        return leaf

    def _insert_leaf(self, target: InternalNode[T], leaf: Leaf[T]) -> InternalNode[T] | None:
        """ 葉を2-3木に追加する

        追加する葉を2-3木の節点に追加する
        本関数呼び出し終了時点では、2-3木が再構成されていないので注意

        Args:
            target: 葉を追加する節点
            leaf: 追加したい葉

        Returns:
            葉を追加した際に内部節点が増加した場合はその Node, 増加しなかった場合は None
        """
        inter: InternalNode[T] | None = None

        # 特殊なケース
        if target.isRoot:
            # (1) target が root で 1個目の葉を追加する場合
            if target.left is None:
                target.left = leaf
                return inter

            # (2) target が root で 2個目の葉を追加する場合
            elif target.mid is None and target.left_max_node is not None:
                if leaf.compareCargo(target.left_max_node.cargo) <= 0:
                    target.mid = target.left
                    target.left = leaf
                else:
                    target.mid = leaf
                return inter

        # 通常のケース
        #   上記の特殊ケース以外は target は常に 2 個または 3 個の子要素を持つ
        if target.left is None or target.mid is None:
            raise RuntimeError("internal error: each internal node must be at least 2 children.")
        #   left や mid が None ではないので、 max_node が必ず存在することも確認しておく
        if target.left_max_node is None or target.mid_max_node is None:
            raise RuntimeError("internal error: each internal node must have left or mid max node.")
        
        if leaf.compareCargo(target.left_max_node.cargo) <= 0:
            # 挿入位置: left の左
            if target.right is None:
                # 子要素２個
                self._insert_leaf_without_inter(target, leaf, target.left, target.mid)
            else:
                # 子要素３個
                inter = self._insert_leaf_with_inter(target, leaf, target.left, target.mid, target.right)

        elif leaf.compareCargo(target.left_max_node.cargo) > 0 and leaf.compareCargo(target.mid_max_node.cargo) <= 0:

            # 挿入位置: left と mid の間
            if target.right is None:
                # 子要素２個
                self._insert_leaf_without_inter(target, target.left, leaf, target.mid)
            else:
                # 子要素３個
                inter = self._insert_leaf_with_inter(target, target.left, leaf, target.mid, target.right)

        elif target.right is None:
            # 挿入位置: mid の右
            #   子要素は常に２個
            self._insert_leaf_without_inter(target, target.left, target.mid, leaf)

        elif leaf.compareCargo(target.right.cargo) <= 0:
            # 挿入位置: mid と right の間
            #   子要素は常に３個
            inter = self._insert_leaf_with_inter(target, target.left, target.mid, leaf, target.right)

        else:
            # 挿入位置: right の右
            #   子要素は常に３個
            inter = self._insert_leaf_with_inter(target, target.left, target.mid, target.right, leaf)

        return inter
    
    def _insert_leaf_without_inter(self, target: InternalNode[T], left: Node[T], mid: Node[T], right: Node[T]):
        """ 内部節点の増加のない子要素の追加

        target の子要素が２この場合に呼ばれる

        Args:
            target: 子要素（葉）を追加する内部節点
            left: 左の子要素
            mid: 中央の子要素
            right: 右の子要素
        """
        target.right = right
        target.mid = mid
        target.left = left
        # 最大要素の更新
        self._update_max_node_raw(target)

    def _insert_leaf_with_inter(self, target: InternalNode[T], prev_left: Node[T], prev_mid: Node[T], new_left: Node[T], new_mid: Node[T]) -> InternalNode[T]:
        """ 内部節点の追加を伴う子要素の追加
    
        target の子要素が３個の時に呼ばれる
        target の右隣に新しい内部節点を追加し、それぞれ子要素を２個持つようにする

        Args:
            target: 子要素（葉または内部節点）を追加する内部節点
            prev_left: 左側の内部節点(target)の左の子要素
            prev_mid: 左側の内部節点(target)の中央の子要素
            new_left: 右側の内部節点(追加される節点)の左の子要素
            new_mid: 右側の内部節点(追加される節点)の中央の子要素

        Returns:
            target の右側に追加した内部節点
        """
        inter: InternalNode[T] = InternalNode[T](target.parent)

        # 追加したノード
        new_left.parent = inter
        new_mid.parent = inter
        inter.left = new_left
        inter.mid = new_mid

        # 最大要素の更新
        self._update_max_node_raw(inter)

        # 既存ノード
        target.right = None

        prev_left.parent = target
        prev_mid.parent = target
        target.left = prev_left
        target.mid = prev_mid

        # 最大要素の更新
        self._update_max_node_raw(target)

        return inter

    def _update_max_node(self, nd: Node[T] | None):
        """ 再帰的に木全体の最大 node を更新

        内部節点 nd を対象とし、木全体の最大 node を
        更新する

        Args:
            nd: 最大 Node を更新する内部節点
        """
        if nd is None:
            return
        
        self._update_max_node_raw(nd)
        # root まで再帰
        self._update_max_node(nd.parent)

    def _update_max_node_raw(self, nd: Node[T] | None):
        """ 最大 node を更新

        内部節点 nd を対象とし、 nd の最大 node のみを更新する

        Args:
            nd: 最大 Node を更新する内部節点
        """
        if nd is None:
            return
        
        if not isinstance(nd, InternalNode):
            raise RuntimeError()
        
        # 更新
        nd.left_max_node = self._maximum_raw(nd.left)
        nd.mid_max_node = self._maximum_raw(nd.mid)

    def delete(self, obj: T):
        """要素の削除

        引数で与えられた obj と同じ値を持つ葉を検索して削除する
        もし、対象となる葉がなければ、なにもしない

        当該要素を削除したのち、2-3木が保たれるように再構築を行う

        Args:
            obj: 削除対象の要素
        """

        # 削除対象を見つける
        result: Node[T] = self._search_raw(obj)

        if not isinstance(result, Leaf):
            # 削除対象がない
            return

        # ノードを削除
        if result.parent is None or not isinstance(result.parent, InternalNode):
            raise RuntimeError()
        
        base : InternalNode[T] = result.parent
        self._delete_raw(result, base)
        # base の子要素は左詰めになっている点に注意

        # 2-3木を再構成
        while (True):
            # 子要素が２以上ある場合は、2-3木が成立している
            if base.numberOfChild >= 2:
                # 最大要素を更新
                self._update_max_node(base)
                break

            # 以下の処理は base の子要素が１の場合に行う

            # base が root の場合
            if base.parent is None: # base.isRoot が True も同じ
                if isinstance(base.left, InternalNode):
                    base.left.parent = None
                    self.root = base.left
                    # 最大要素を更新
                    self._update_max_node(self.root)
                    break
                elif isinstance(base.left, Leaf):
                    # root 配下に葉のみがある場合で、葉が１つの場合
                    # 最大要素を更新
                    self._update_max_node(self.root)
                    break
                elif base.left is None and self.root.numberOfChild == 0:
                    # root のみの場合
                    # 最大要素を更新
                    self._update_max_node(self.root)
                    break
                else:
                    raise RuntimeError()

            # base の親から見た位置により処理を分岐
            parent: Node[T] = base.parent

            sibling: Node[T] | None
            if base is parent.left:
                sibling = parent.mid
                if sibling is None:
                    raise RuntimeError()
                self._concat_left_to_right(base, sibling)

            elif base is parent.mid:
                sibling = parent.left
                if sibling is None:
                    raise RuntimeError()
                self._concat_right_to_left(base, sibling)
                
            elif base is parent.right:
                sibling = parent.mid
                if sibling is None:
                    raise RuntimeError()
                self._concat_right_to_left(base, sibling)
            else:
                raise RuntimeError()            

            # 一つ上へ
            base = base.parent


    def _delete_raw(self, target_leaf: Node[T], parent: Node[T]):
        """葉の削除

        指定された葉を削除する。
        この関数終了時点では、2-3木を満たす parent には
        なっていない点に注意。

        また、 parent の子要素は、削除後左詰めになるように移動しておく

        Args:
            target_leaf: 削除対象の葉
            parent: target_leaf の親
        """
        if target_leaf is parent.left:
            parent.left = parent.mid
            parent.mid = parent.right
            parent.right = None
        elif target_leaf is parent.mid:
            parent.mid = parent.right
            parent.right = None
        elif target_leaf is parent.right :
            parent.right = None
        else:
            # ここにはこないはず
            raise RuntimeError()

    def _concat_left_to_right(self, base: Node[T], sibling: Node[T]):
        """左の子要素を右の子要素と結合

        下記のパターンがあり得る
            left -> mid

        Args:
            base: 削除した Node の親, 常に left
            sibling: base の兄弟要素, 常に mid
        """
        if sibling.numberOfChild == 2:
            # base の子を sibling にまとめる
            sibling.right = sibling.mid
            sibling.mid   = sibling.left

            if base.left is None:
                raise RuntimeError()
            base.left.parent = sibling
            sibling.left  = base.left
            base.left     = None

            # base を削除
            if base.parent is None:
                raise RuntimeError()
            
            base.parent.left  = sibling
            base.parent.mid   = base.parent.right
            base.parent.right = None

            # max_node の更新
            self._update_max_node_raw(sibling)
            self._update_max_node_raw(base.parent)

        elif sibling.numberOfChild == 3:
            # base と sibling で子要素を分け合う
            if sibling.left is None:
                raise RuntimeError()
            sibling.left.parent = base
            base.mid = sibling.left

            sibling.left = sibling.mid
            sibling.mid = sibling.right
            sibling.right = None

            # max_node の更新
            self._update_max_node_raw(base)
            self._update_max_node_raw(sibling)
        else:
            raise RuntimeError()

    def _concat_right_to_left(self, base: Node[T], sibling: Node[T]):
        """右の子要素を左の子要素と結合

        下記の２パターンがあり得る
            left <- mid
            mid  <- right

        Args:
            base: 削除した Node の親, mid または right
            sibling: base の兄弟要素, left または mid
        """
        if sibling.numberOfChild == 2:
            # base の子を sibling にまとめる
            if base.left is None:
                raise RuntimeError()
            base.left.parent = sibling
            sibling.right = base.left
            base.left = None

            # base を削除
            if base.parent is None:
                raise RuntimeError()
            
            if base is base.parent.mid:
                base.parent.mid = base.parent.right
            base.parent.right = None

            # max_node の更新
            self._update_max_node_raw(sibling)
            self._update_max_node_raw(base.parent)

        elif sibling.numberOfChild == 3:
            # base と sibling で子要素を分け合う
            base.mid = base.left

            if sibling.right is None:
                raise RuntimeError()
            sibling.right.parent = base
            base.left = sibling.right
            sibling.right = None

            # max_node の更新
            self._update_max_node_raw(base)
            self._update_max_node_raw(sibling)
        else:
            raise RuntimeError()

    def removeAll(self):
        """root 以外のすべての要素を削除
        """
        if self.root.right is not None:
            self.root.right = None
        if self.root.mid is not None:
            self.root.mid = None
        if self.root.left is not None:
            self.root.left = None

    def visualizeGraph(self, verbose: bool, graph_name:str = "two_three_graph.gv", format_name: str = "pdf"):
        """2-3木を図示する

        graphviz ファイルおよびフォーマットに従った図ファイルを出力する

        詳細モードが指定された場合、以下も行う
            ・内部節点の left max, mid max を表示
            ・子要素から親要素への参照を表示
            ・graphviz の記述内容を標準出力へ出力

        Args:
            verbose: 詳細モード
            graph_name: 出力ファイル名, デフォルトは two_three_graph.gv
            format_name: 出力フォーマット, pdf, png など, デフォルトは pdf
        """
        g = Digraph(format=format_name)
        g.attr("node", shape="circle")

        # root
        self._visualizeGraph_raw(g, self.root, verbose)
        
        # for debug
        if verbose:
            print(g.source)

        g.render(graph_name)

    def _visualizeGraph_raw(self, g: Digraph, nd: Node[T] | None, verbose: bool):
        """再帰によりグラフを描画

        詳細モードの場合、子要素から親要素への参照も表示する

        Args:
            g: Digraph
            nd: 描画対象ノード
            verbose: 詳細モード
        """
        if nd is None:
            return
        
        # 対象 Node の描画
        self._drawNode(g, nd, verbose)

        # 子要素
        if nd.left is not None:
            self._drawNode(g, nd.left, verbose)
            g.edge(str(id(nd)), str(id(nd.left)))
            if verbose:
                g.edge(str(id(nd.left)), str(id(nd.left.parent)))

            self._visualizeGraph_raw(g, nd.left, verbose)

        if nd.mid is not None:
            self._drawNode(g, nd.mid, verbose)
            g.edge(str(id(nd)), str(id(nd.mid)))
            if verbose:
                g.edge(str(id(nd.mid)), str(id(nd.mid.parent)))

            self._visualizeGraph_raw(g, nd.mid, verbose)

        if nd.right is not None:
            self._drawNode(g, nd.right, verbose)
            g.edge(str(id(nd)), str(id(nd.right)))
            if verbose:
                g.edge(str(id(nd.right)), str(id(nd.right.parent)))

            self._visualizeGraph_raw(g, nd.right, verbose)

    def _drawNode(self, g: Digraph, nd: Node[T], verbose: bool):
        """Node の描画

        詳細モードの場合、内部節点についての left max, mid max も出力する

        Args:
            g: Digraph
            nd: 描画対象ノード
            verbose: 詳細モード
        """
        if isinstance(nd, InternalNode):
            g.node(str(id(nd)), "", xlabel=self._createlabel(nd) if verbose else "")
        else:
            g.node(str(id(nd)), self._createlabel(nd), shape="circle")

    def _createlabel(self, nd: Node[T] | None) -> str:
        if nd is None:
            return ""
        
        if isinstance(nd, InternalNode):
            left_str: str = ""
            mid_str: str  = ""
            if nd.left_max_node is not None:
                left_str = f"left: {nd.left_max_val}"
            if nd.mid_max_node is not None:
                mid_str = f"mid: {nd.mid_max_val}"
            return left_str + "\\n" + mid_str
        else:
            return f"{nd.val}"
