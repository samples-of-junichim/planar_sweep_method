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
    """2-3 木に関する挿入操作のテスト
    """

    def setUp(self):
        print("2-3 tree test setup")

        # 2-3木を作成してテスト
        self.tht: TwoThreeTree = TwoThreeTree[MyLeaf, NodeForTest](get_key, comp_key, myleaf_ctor)

    def tearDown(self):
        pass

    def test_create_tree_1(self):
        """root への１つ目の子要素の挿入
        """
        self.tht.insert(NodeForTest("01", 2.0))

        self.assertEqual(2, self.tht.size)
        self.assertEqual(1, self.tht.leafSize)
        self.assertEqual(2, self.tht.height)

    def test_create_tree_2(self):
        """root への２つ目の子要素の挿入

        new_key < key1 の場合
        """
        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 1.0))

        self.assertEqual(3, self.tht.size)
        self.assertEqual(2, self.tht.leafSize)
        self.assertEqual(2, self.tht.height)

    def test_create_tree_3(self):
        """root への２つ目の子要素の挿入

        key1 < new_key の場合
        """
        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 5.0))

        self.assertEqual(3, self.tht.size)
        self.assertEqual(2, self.tht.leafSize)
        self.assertEqual(2, self.tht.height)

    def test_create_tree_4(self):
        """root への３つ目の子要素の挿入

        new_key < key1 < key2  の場合
        """
        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 5.0))
        self.tht.insert(NodeForTest("03", 1.0))

        self.assertEqual(4, self.tht.size)
        self.assertEqual(3, self.tht.leafSize)
        self.assertEqual(2, self.tht.height)

    def test_create_tree_5(self):
        """root への３つ目の子要素の挿入

        key1 < new_key < key2 の場合
        """
        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 7.0))
        self.tht.insert(NodeForTest("03", 5.0))

        self.assertEqual(4, self.tht.size)
        self.assertEqual(3, self.tht.leafSize)
        self.assertEqual(2, self.tht.height)

    def test_create_tree_6(self):
        """root への３つ目の子要素の挿入

        key1 < key2 < new_key の場合
        """
        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 5.0))
        self.tht.insert(NodeForTest("03", 7.0))

        self.assertEqual(4, self.tht.size)
        self.assertEqual(3, self.tht.leafSize)
        self.assertEqual(2, self.tht.height)

    def test_create_tree_7(self):
        """root への４つ目の子要素の挿入

        new_key < left の場合
        """
        self.tht.insert(NodeForTest("01", 5.0))
        self.tht.insert(NodeForTest("02", 7.0))
        self.tht.insert(NodeForTest("03", 9.0))
        self.tht.insert(NodeForTest("04", 2.0))

        self.assertEqual(7, self.tht.size)
        self.assertEqual(4, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

    def test_create_tree_8(self):
        """root への４つ目の子要素の挿入

        left < new_key < mid の場合
        """
        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 7.0))
        self.tht.insert(NodeForTest("03", 9.0))
        self.tht.insert(NodeForTest("04", 5.0))

        self.assertEqual(7, self.tht.size)
        self.assertEqual(4, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

    def test_create_tree_9(self):
        """root への４つ目の子要素の挿入

        mid < new_key < right の場合
        """
        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 5.0))
        self.tht.insert(NodeForTest("03", 9.0))
        self.tht.insert(NodeForTest("04", 7.0))

        self.assertEqual(7, self.tht.size)
        self.assertEqual(4, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

    def test_create_tree_10(self):
        """root への４つ目の子要素の挿入

        right < new_key の場合
        """
        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 5.0))
        self.tht.insert(NodeForTest("03", 7.0))
        self.tht.insert(NodeForTest("04", 9.0))

        self.assertEqual(7, self.tht.size)
        self.assertEqual(4, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

    def test_create_tree_11(self):
        """内部要素（子要素２つ）への３つ目の子要素の挿入

        new_key < left の場合
        """
        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 5.0))
        self.tht.insert(NodeForTest("03", 7.0))
        self.tht.insert(NodeForTest("04", 9.0))

        self.tht.insert(NodeForTest("05", 1.0))

        self.assertEqual(8, self.tht.size)
        self.assertEqual(5, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

    def test_create_tree_12(self):
        """内部要素（子要素２つ）への３つ目の子要素の挿入

        left < new_key < mid の場合
        """
        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 5.0))
        self.tht.insert(NodeForTest("03", 7.0))
        self.tht.insert(NodeForTest("04", 9.0))

        self.tht.insert(NodeForTest("05", 4.0))

        self.assertEqual(8, self.tht.size)
        self.assertEqual(5, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

    def test_create_tree_13(self):
        """内部要素（子要素２つ）への３つ目の子要素の挿入

        mid < new_key の場合
        """
        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 5.0))
        self.tht.insert(NodeForTest("03", 7.0))
        self.tht.insert(NodeForTest("04", 9.0))

        self.tht.insert(NodeForTest("05", 6.0))

        self.assertEqual(8, self.tht.size)
        self.assertEqual(5, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

    def test_create_tree_14(self):
        """内部要素（子要素３つ）への４つ目の子要素の挿入

        new_key < left の場合

        最終的な形
              p
           /  |   \
          p   p   p
         /|  /|  /|
        1 2 4 5 7 9
        """
        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 5.0))
        self.tht.insert(NodeForTest("03", 7.0))
        self.tht.insert(NodeForTest("04", 9.0))

        self.tht.insert(NodeForTest("05", 4.0))
        self.tht.insert(NodeForTest("06", 1.0))

        self.assertEqual(10, self.tht.size)
        self.assertEqual(6, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

    def test_create_tree_15(self):
        """内部要素（子要素３つ）への４つ目の子要素の挿入

        left < new_key < mid の場合

        最終的な形
              p
           /  |   \
          p   p   p
         /|  /|  /|
        1 2 4 5 7 9
        """
        self.tht.insert(NodeForTest("01", 1.0))
        self.tht.insert(NodeForTest("02", 5.0))
        self.tht.insert(NodeForTest("03", 7.0))
        self.tht.insert(NodeForTest("04", 9.0))

        self.tht.insert(NodeForTest("05", 4.0))
        self.tht.insert(NodeForTest("06", 2.0))

        self.assertEqual(10, self.tht.size)
        self.assertEqual(6, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

    def test_create_tree_16(self):
        """内部要素（子要素３つ）への４つ目の子要素の挿入

        mid < new_key < right の場合

        最終的な形

              p
           /  |   \
          p   p   p
         /|  /|  /|
        1 2 4 5 7 9
        """
        self.tht.insert(NodeForTest("01", 1.0))
        self.tht.insert(NodeForTest("02", 5.0))
        self.tht.insert(NodeForTest("03", 7.0))
        self.tht.insert(NodeForTest("04", 9.0))

        self.tht.insert(NodeForTest("05", 2.0))
        self.tht.insert(NodeForTest("06", 4.0))

        self.assertEqual(10, self.tht.size)
        self.assertEqual(6, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

    def test_create_tree_17(self):
        """内部要素（子要素３つ）への４つ目の子要素の挿入

        right < new_key の場合

        最終的な形
             p
           /   \
          p     p
         /|\   /|\
        1 2 4 5 7 9
        """
        self.tht.insert(NodeForTest("01", 1.0))
        self.tht.insert(NodeForTest("02", 4.0))
        self.tht.insert(NodeForTest("03", 7.0))
        self.tht.insert(NodeForTest("04", 9.0))

        self.tht.insert(NodeForTest("05", 2.0))
        self.tht.insert(NodeForTest("06", 5.0))

        self.assertEqual(9, self.tht.size)
        self.assertEqual(6, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)
