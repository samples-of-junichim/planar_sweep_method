from dataclasses import dataclass
import datetime
import unittest
from TwoThreeTree import Leaf, Node, TwoThreeTree
from test.TestClasses import MyLeaf, NodeForTest, myleaf_ctor

class TestTwoThreeTree(unittest.TestCase):
    """典型的な 2-3 木に関するテスト
    """

    @classmethod
    def setUpClass(cls):
        print("2-3 tree test setup")

        # 2-3木を作成してテスト
        cls.tht: TwoThreeTree = TwoThreeTree[MyLeaf, NodeForTest](myleaf_ctor)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_create_tree_1(self):
        TestTwoThreeTree.tht.visualizeGraph(True, "sample_" + datetime.datetime.now().isoformat(), format_name="png")

        TestTwoThreeTree.tht.insert(NodeForTest("01", 2.0))

        self.assertEqual(2, TestTwoThreeTree.tht.size)
        self.assertEqual(1, TestTwoThreeTree.tht.leafSize)
        self.assertEqual(2, TestTwoThreeTree.tht.height)

        TestTwoThreeTree.tht.visualizeGraph(True, "sample_" + datetime.datetime.now().isoformat(), format_name="png")

    def test_create_tree_2(self):
        TestTwoThreeTree.tht.insert(NodeForTest("02", 5.0))

        self.assertEqual(3, TestTwoThreeTree.tht.size)
        self.assertEqual(2, TestTwoThreeTree.tht.leafSize)
        self.assertEqual(2, TestTwoThreeTree.tht.height)

        TestTwoThreeTree.tht.visualizeGraph(True, "sample_" + datetime.datetime.now().isoformat(), format_name="png")

    def test_create_tree_3(self):
        TestTwoThreeTree.tht.insert(NodeForTest("03", 9.0))

        self.assertEqual(4, TestTwoThreeTree.tht.size)
        self.assertEqual(3, TestTwoThreeTree.tht.leafSize)
        self.assertEqual(2, TestTwoThreeTree.tht.height)

        TestTwoThreeTree.tht.visualizeGraph(True, "sample_" + datetime.datetime.now().isoformat(), format_name="png")

    def test_create_tree_4(self):
        TestTwoThreeTree.tht.insert(NodeForTest("04", 7.0))

        self.assertEqual(7, TestTwoThreeTree.tht.size)
        self.assertEqual(4, TestTwoThreeTree.tht.leafSize)
        self.assertEqual(3, TestTwoThreeTree.tht.height)

        TestTwoThreeTree.tht.visualizeGraph(True, "sample_" + datetime.datetime.now().isoformat(), format_name="png")

    def test_create_tree_5(self):
        TestTwoThreeTree.tht.insert(NodeForTest("05", 4.0))

        self.assertEqual(8, TestTwoThreeTree.tht.size)
        self.assertEqual(5, TestTwoThreeTree.tht.leafSize)
        self.assertEqual(3, TestTwoThreeTree.tht.height)

        TestTwoThreeTree.tht.visualizeGraph(True, "sample_" + datetime.datetime.now().isoformat(), format_name="png")

    def test_create_tree_6(self):
        TestTwoThreeTree.tht.insert(NodeForTest("06", 1.0))

        self.assertEqual(10, TestTwoThreeTree.tht.size)
        self.assertEqual(6, TestTwoThreeTree.tht.leafSize)
        self.assertEqual(3, TestTwoThreeTree.tht.height)

        TestTwoThreeTree.tht.visualizeGraph(True, "sample_" + datetime.datetime.now().isoformat(), format_name="png")

    def test_create_tree_7(self):
        TestTwoThreeTree.tht.insert(NodeForTest("07", 3.0))

        self.assertEqual(11, TestTwoThreeTree.tht.size)
        self.assertEqual(7, TestTwoThreeTree.tht.leafSize)
        self.assertEqual(3, TestTwoThreeTree.tht.height)

        TestTwoThreeTree.tht.visualizeGraph(True, "sample_" + datetime.datetime.now().isoformat(), format_name="png")

    def test_create_tree_8(self):
        TestTwoThreeTree.tht.insert(NodeForTest("08", 10.0))

        self.assertEqual(12, TestTwoThreeTree.tht.size)
        self.assertEqual(8, TestTwoThreeTree.tht.leafSize)
        self.assertEqual(3, TestTwoThreeTree.tht.height)

        TestTwoThreeTree.tht.visualizeGraph(True, "sample_" + datetime.datetime.now().isoformat(), format_name="png")

    def test_create_tree_9(self):
        TestTwoThreeTree.tht.insert(NodeForTest("09", 8.0))

        self.assertEqual(16, TestTwoThreeTree.tht.size)
        self.assertEqual(9, TestTwoThreeTree.tht.leafSize)
        self.assertEqual(4, TestTwoThreeTree.tht.height)

        TestTwoThreeTree.tht.visualizeGraph(True, "sample_" + datetime.datetime.now().isoformat(), format_name="png")

    def test_max_min(self):
        # 最大と最小
        m = TestTwoThreeTree.tht.minimum()
        self.assertIsNotNone(m)
        if m is not None:
            self.assertAlmostEqual(1.0, float(m.val))

        m = TestTwoThreeTree.tht.maximum()
        self.assertIsNotNone(m)
        if m is not None:
            self.assertAlmostEqual(10.0, float(m.val))

    def test_node_search(self):
        # 探索
        nd = TestTwoThreeTree.tht.search(NodeForTest("07", 3.0))
        self.assertIsNotNone(nd)
        if nd is not None:
            self.assertAlmostEqual(3.0, float(nd.val))

            # 次要素
            s = TestTwoThreeTree.tht.successor(nd)
            self.assertIsNotNone(s)
            if s is not None:
                self.assertAlmostEqual(4.0, float(s.val))

            # 前要素
            p = TestTwoThreeTree.tht.predecessor(nd)
            self.assertIsNotNone(p)
            if p is not None:
                self.assertAlmostEqual(2.0, float(p.val))

    def test_node_search_minimum(self):
        # 最小値の探索
        nd = TestTwoThreeTree.tht.search(NodeForTest("03", 1.0))
        self.assertIsNotNone(nd)
        if nd is not None:
            self.assertAlmostEqual(1.0, float(nd.val))

            # 次要素
            s = TestTwoThreeTree.tht.successor(nd)
            self.assertIsNotNone(s)
            if s is not None:
                self.assertAlmostEqual(2.0, float(s.val))

            # 前要素
            p = TestTwoThreeTree.tht.predecessor(nd)
            self.assertIsNone(p)

    def test_node_search_maximum(self):
        # 最大値の探索
        nd = TestTwoThreeTree.tht.search(NodeForTest("08", 10.0))
        self.assertIsNotNone(nd)
        if nd is not None:
            self.assertAlmostEqual(10.0, float(nd.val))

            # 次要素
            s = TestTwoThreeTree.tht.successor(nd)
            self.assertIsNone(s)

            # 前要素
            p = TestTwoThreeTree.tht.predecessor(nd)
            self.assertIsNotNone(p)
            if p is not None:
                self.assertAlmostEqual(9.0, float(p.val))

    def test_remove_1(self):
        # 削除
        self.assertEqual(16, TestTwoThreeTree.tht.size)
        self.assertEqual(9, TestTwoThreeTree.tht.leafSize)
        self.assertEqual(4, TestTwoThreeTree.tht.height)

        nd = TestTwoThreeTree.tht.search(NodeForTest("02", 2.0))
        self.assertIsNotNone(nd)
        if nd is not None:
            self.assertAlmostEqual(2.0, float(nd.val))

        TestTwoThreeTree.tht.delete(NodeForTest("02", 2.0))

        self.assertEqual(15, TestTwoThreeTree.tht.size)
        self.assertEqual(8, TestTwoThreeTree.tht.leafSize)
        self.assertEqual(4, TestTwoThreeTree.tht.height)

        nd = TestTwoThreeTree.tht.search(NodeForTest("02", 2.0))
        self.assertIsNone(nd)

    def test_remove_2(self):
        # 削除
        self.assertEqual(15, TestTwoThreeTree.tht.size)
        self.assertEqual(8, TestTwoThreeTree.tht.leafSize)
        self.assertEqual(4, TestTwoThreeTree.tht.height)

        nd = TestTwoThreeTree.tht.search(NodeForTest("03", 3.0))
        self.assertIsNotNone(nd)
        if nd is not None:
            self.assertAlmostEqual(3.0, float(nd.val))

        TestTwoThreeTree.tht.delete(NodeForTest("03", 3.0))

        self.assertEqual(11, TestTwoThreeTree.tht.size)
        self.assertEqual(7, TestTwoThreeTree.tht.leafSize)
        self.assertEqual(3, TestTwoThreeTree.tht.height)

        nd = TestTwoThreeTree.tht.search(NodeForTest("03", 3.0))
        self.assertIsNone(nd)

    def test_remove_3(self):
        # すべて削除
        self.assertEqual(11, TestTwoThreeTree.tht.size)
        self.assertEqual(7, TestTwoThreeTree.tht.leafSize)
        self.assertEqual(3, TestTwoThreeTree.tht.height)

        TestTwoThreeTree.tht.removeAll()

        self.assertEqual(1, TestTwoThreeTree.tht.size)
        self.assertEqual(0, TestTwoThreeTree.tht.leafSize)
        self.assertEqual(1, TestTwoThreeTree.tht.height)
