from dataclasses import dataclass
import datetime
import unittest
from TwoThreeTree import Leaf, Node, TwoThreeTree
from test.TestClasses import MyLeaf, NodeForTest, myleaf_ctor

class TestTwoThreeTree(unittest.TestCase):
    """2-3 木に関する挿入操作のテスト

    木の構築テスト
    """

    def setUp(self):
        print("2-3 tree test setup")

        # 2-3木を作成してテスト
        self.tht: TwoThreeTree = TwoThreeTree[MyLeaf, NodeForTest](myleaf_ctor)

    def tearDown(self):
        pass

    def test_create_tree_1(self):
        """木の構築テスト
        """
        self.tht.visualizeGraph(True, "sample_tree_const_root_" + datetime.datetime.now().isoformat())

        self.tht.insert(NodeForTest("01", 0.0))
        self.tht.visualizeGraph(True, "sample_tree_const_1_" + datetime.datetime.now().isoformat())

        self.tht.insert(NodeForTest("02", 1.5))
        self.tht.visualizeGraph(True, "sample_tree_const_2_" + datetime.datetime.now().isoformat())

        self.tht.insert(NodeForTest("03", -1))
        self.tht.visualizeGraph(True, "sample_tree_const_3_" + datetime.datetime.now().isoformat())

        self.tht.insert(NodeForTest("04", 2))
        self.tht.visualizeGraph(True, "sample_tree_const_4_" + datetime.datetime.now().isoformat())

        self.tht.insert(NodeForTest("05", -2))
        self.tht.visualizeGraph(True, "sample_tree_const_5_" + datetime.datetime.now().isoformat())

        self.tht.insert(NodeForTest("06", 3))
        self.tht.visualizeGraph(True, "sample_tree_const_6_" + datetime.datetime.now().isoformat())

        self.tht.insert(NodeForTest("07", 4))
        self.tht.visualizeGraph(True, "sample_tree_const_7_" + datetime.datetime.now().isoformat())

        self.assertEqual(11, self.tht.size)
        self.assertEqual(7, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

    def test_create_tree_2(self):
        """木の構築テスト

        test_create_tree_3 との比較を行う
        """
        self.tht.insert(NodeForTest("01", -0.5))
        self.tht.insert(NodeForTest("01", 1.25))
        self.tht.insert(NodeForTest("01", 0))
        self.tht.insert(NodeForTest("01", 1))

        self.tht.visualizeGraph(True, "sample_tree_const_t2_1_" + datetime.datetime.now().isoformat())

        self.tht.insert(NodeForTest("01", 0.5))

        self.tht.visualizeGraph(True, "sample_tree_const_t2_2_" + datetime.datetime.now().isoformat())

        self.tht.insert(NodeForTest("01", 1.5))

        self.tht.visualizeGraph(True, "sample_tree_const_t2_3_" + datetime.datetime.now().isoformat())

        # leaf が 2 の中間ノードが 3 つ
        self.assertEqual(10, self.tht.size)
        self.assertEqual(6, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

    def test_create_tree_3(self):
        """木の構築テスト

        test_create_tree_2 と同じ葉の要素だが、
        追加する順番が異なると、結果の木が異なる
        """
        self.tht.insert(NodeForTest("01", -0.5))
        self.tht.insert(NodeForTest("01", 0.5))
        self.tht.insert(NodeForTest("01", 1))
        self.tht.insert(NodeForTest("01", 1.25))

        self.tht.visualizeGraph(True, "sample_tree_const_t3_1_" + datetime.datetime.now().isoformat())

        self.tht.insert(NodeForTest("01", 0))

        self.tht.visualizeGraph(True, "sample_tree_const_t3_2_" + datetime.datetime.now().isoformat())

        self.tht.insert(NodeForTest("01", 1.5))

        self.tht.visualizeGraph(True, "sample_tree_const_t3_3_" + datetime.datetime.now().isoformat())

        # leaf が 3 の中間ノードが 2 つ
        self.assertEqual(9, self.tht.size)
        self.assertEqual(6, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)
