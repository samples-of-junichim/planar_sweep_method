from dataclasses import dataclass
import datetime
import unittest
from TwoThreeTree import Leaf, Node, TwoThreeTree
from test.TestClasses import MyLeaf, NodeForTest, myleaf_ctor

class TestTwoThreeTree(unittest.TestCase):
    """2-3 木に関する range 操作のテスト
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

        #self.tht.visualizeGraph(True, "test_range_tree_" + datetime.datetime.now().isoformat())

    def tearDown(self):
        pass

    def test_range_tree_01(self):
        """範囲の抽出

        [min, max] 内の要素と抽出
        最初の要素は、 left ノードになる
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        nd1 = NodeForTest("a", 6.0)
        nd2 = NodeForTest("b", 9.5)
        lst = self.tht.range(nd1, nd2)

        self.assertEqual(3, len(lst))

        self.assertAlmostEqual(7.0, float(lst[0].val))
        self.assertAlmostEqual(8.0, float(lst[1].val))
        self.assertAlmostEqual(9.0, float(lst[2].val))

    def test_range_tree_02(self):
        """範囲の抽出

        [min, max] 内の要素と抽出
        最初の要素は、 mid ノードになる
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        nd1 = NodeForTest("a", 3.5)
        nd2 = NodeForTest("b", 6.0)
        lst = self.tht.range(nd1, nd2)

        self.assertEqual(2, len(lst))

        self.assertAlmostEqual(4.0, float(lst[0].val))
        self.assertAlmostEqual(5.0, float(lst[1].val))

    def test_range_tree_03(self):
        """範囲の抽出

        [min, max] 内の要素と抽出
        最初の要素は、 right ノードになる
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        nd1 = NodeForTest("a", 4.5)
        nd2 = NodeForTest("b", 9.5)
        lst = self.tht.range(nd1, nd2)

        self.assertEqual(4, len(lst))

        self.assertAlmostEqual(5.0, float(lst[0].val))
        self.assertAlmostEqual(7.0, float(lst[1].val))
        self.assertAlmostEqual(8.0, float(lst[2].val))
        self.assertAlmostEqual(9.0, float(lst[3].val))

    def test_range_tree_04(self):
        """範囲の抽出

        [min, max] 内の要素と抽出
        min および max が要素と一致
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        nd1 = NodeForTest("a", 4.0)
        nd2 = NodeForTest("b", 8.0)
        lst = self.tht.range(nd1, nd2)

        self.assertEqual(4, len(lst))

        self.assertAlmostEqual(4.0, float(lst[0].val))
        self.assertAlmostEqual(5.0, float(lst[1].val))
        self.assertAlmostEqual(7.0, float(lst[2].val))
        self.assertAlmostEqual(8.0, float(lst[3].val))

    def test_range_tree_05(self):
        """範囲の抽出

        [min, max] 内の要素と抽出
        max が最大要素より大きい
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        nd1 = NodeForTest("a", 3.0)
        nd2 = NodeForTest("b", 11.0)
        lst = self.tht.range(nd1, nd2)

        self.assertEqual(7, len(lst))

        self.assertAlmostEqual(3.0, float(lst[0].val))
        self.assertAlmostEqual(4.0, float(lst[1].val))
        self.assertAlmostEqual(5.0, float(lst[2].val))
        self.assertAlmostEqual(7.0, float(lst[3].val))
        self.assertAlmostEqual(8.0, float(lst[4].val))
        self.assertAlmostEqual(9.0, float(lst[5].val))
        self.assertAlmostEqual(10.0, float(lst[6].val))

    def test_range_tree_06(self):
        """範囲の抽出

        [min, max] 内の要素と抽出
        min が最小要素より小さい
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        nd1 = NodeForTest("a", 0.5)
        nd2 = NodeForTest("b", 1.5)
        lst = self.tht.range(nd1, nd2)

        self.assertEqual(1, len(lst))

        self.assertAlmostEqual(1.0, float(lst[0].val))

    def test_range_tree_07(self):
        """範囲の抽出

        [min, max] 内の要素と抽出
        min が最小要素より小さい
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        nd1 = NodeForTest("a", 0.5)
        nd2 = NodeForTest("b", 1.5)
        lst = self.tht.range(nd1, nd2)

        self.assertEqual(1, len(lst))

        self.assertAlmostEqual(1.0, float(lst[0].val))
