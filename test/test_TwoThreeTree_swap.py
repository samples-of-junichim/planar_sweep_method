from dataclasses import dataclass
import datetime
import unittest
from TwoThreeTree import Leaf, Node, TwoThreeTree
from test.TestClasses import MyLeaf, NodeForTest, myleaf_ctor

class TestTwoThreeTree(unittest.TestCase):
    """2-3 木に関する swap 操作のテスト
    """

    def setUp(self):
        print("2-3 tree test setup")

        # 2-3木を作成してテスト
        self.tht: TwoThreeTree = TwoThreeTree[MyLeaf, NodeForTest](myleaf_ctor)

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

    def test_swap_tree_01(self):
        """要素の入れ替え

        同じ親の隣接要素を入れ替え
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        nd1 = self.tht.search(NodeForTest("03", 7.0))
        nd2 = self.tht.search(NodeForTest("09", 8.0))

        if nd1 is None:
            raise RuntimeError("invalid search")
        if nd2 is None:
            raise RuntimeError("invalid search")

        self.tht.swap(nd1, nd2)

        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        self.tht.visualizeGraph(True, "test_swap_tree_" + datetime.datetime.now().isoformat())

    def test_swap_tree_02(self):
        """要素の入れ替え

        異なる親につながる葉要素を入れ替え
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        nd1 = self.tht.search(NodeForTest("05", 4.0))
        nd2 = self.tht.search(NodeForTest("01", 2.0))

        if nd1 is None:
            raise RuntimeError("invalid search")
        if nd2 is None:
            raise RuntimeError("invalid search")

        self.tht.swap(nd1, nd2)

        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        self.tht.visualizeGraph(True, "test_swap_tree_" + datetime.datetime.now().isoformat())
