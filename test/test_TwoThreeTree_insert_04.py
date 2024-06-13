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
