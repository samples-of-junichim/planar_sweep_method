from dataclasses import dataclass
import unittest
from TwoThreeTree import Leaf, Node, TwoThreeTree

# テスト用の Node 要素
@dataclass
class NodeForTest:
    id: str     # id
    key: float  # キー

class MyLeaf(Leaf[NodeForTest]):

    def __init__(self, val: NodeForTest, parent: Node[NodeForTest] | None):
        super().__init__(val, parent, get_key, comp_key)

def get_key(v: NodeForTest) -> float:
    return v.key
def comp_key(v1: NodeForTest, v2: NodeForTest) -> bool:
    return v1.key == v2.key
def myleaf_ctor(v: NodeForTest, parent: Node[NodeForTest]):
    return MyLeaf(v, parent)


class TestTwoThreeTree(unittest.TestCase):
    """2-3 木に関する削除操作のテスト
    """

    def setUp(self):
        print("2-3 tree test setup")

        # 2-3木を作成してテスト
        self.tht: TwoThreeTree = TwoThreeTree[MyLeaf, NodeForTest](get_key, comp_key, myleaf_ctor)

        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 5.0))
        self.tht.insert(NodeForTest("03", 7.0))
        self.tht.insert(NodeForTest("04", 9.0))

        self.tht.insert(NodeForTest("05", 4.0))
        self.tht.insert(NodeForTest("06", 1.0))
        self.tht.insert(NodeForTest("07", 3.0))
        self.tht.insert(NodeForTest("08", 10.0))
        self.tht.insert(NodeForTest("09", 8.0))

    def tearDown(self):
        pass

    def test_remove_tree_01(self):
        """内部要素（子要素２）からの子要素(mid)の削除

        右の兄弟から移動
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        self.tht.delete(NodeForTest("01", 2.0))

        self.assertEqual(15, self.tht.size)
        self.assertEqual(8, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

    def test_remove_tree_02(self):
        """内部要素（子要素２）からの子要素(left)の削除

        右の兄弟から移動
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        self.tht.delete(NodeForTest("01", 1.0))

        self.assertEqual(15, self.tht.size)
        self.assertEqual(8, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

    def test_remove_tree_03(self):
        """内部要素（子要素２）からの子要素(mid)の削除

        左の兄弟から移動
        """
        self.tht.insert(NodeForTest("10", 6.0))

        self.assertEqual(17, self.tht.size)
        self.assertEqual(10, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        self.tht.delete(NodeForTest("01", 10.0))

        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

    def test_remove_tree_04(self):
        """内部要素（子要素２）からの子要素(left)の削除

        左の兄弟から移動
        """
        self.tht.insert(NodeForTest("10", 6.0))

        self.assertEqual(17, self.tht.size)
        self.assertEqual(10, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        self.tht.delete(NodeForTest("01", 9.0))

        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

    def test_remove_tree_05(self):
        """内部要素（子要素３）からの子要素(right)の削除
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        self.tht.delete(NodeForTest("01", 5.0))

        self.assertEqual(15, self.tht.size)
        self.assertEqual(8, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        # root 要素の left_max, mid_max をチェック

    def test_remove_tree_06(self):
        """内部要素からの子要素の削除

        left -> mid で結合
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        self.tht.delete(NodeForTest("01", 2.0))
        self.tht.delete(NodeForTest("02", 3.0))

        self.assertEqual(11, self.tht.size)
        self.assertEqual(7, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

    def test_remove_tree_07(self):
        """内部要素からの子要素の削除

        mid -> left, (right なし)  で結合
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        self.tht.delete(NodeForTest("01", 3.0))
        self.tht.delete(NodeForTest("02", 4.0))

        self.assertEqual(11, self.tht.size)
        self.assertEqual(7, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

    def test_remove_tree_08(self):
        """内部要素からの子要素の削除

        mid -> left, (right あり) で結合
        """
        self.tht.insert(NodeForTest("10", 6.0))
        self.tht.insert(NodeForTest("11", 5.5))

        self.assertEqual(19, self.tht.size)
        self.assertEqual(11, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        self.tht.delete(NodeForTest("01", 8.0))

        self.assertEqual(17, self.tht.size)
        self.assertEqual(10, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

    def test_remove_tree_09(self):
        """内部要素からの子要素の削除

        right -> mid で結合
        """
        self.tht.insert(NodeForTest("10", 6.0))
        self.tht.insert(NodeForTest("11", 5.5))

        self.assertEqual(19, self.tht.size)
        self.assertEqual(11, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        self.tht.delete(NodeForTest("01", 9.0))

        self.assertEqual(17, self.tht.size)
        self.assertEqual(10, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)
