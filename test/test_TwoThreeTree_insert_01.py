from dataclasses import dataclass
import datetime
import unittest
from TwoThreeTree import Leaf, Node, TwoThreeTree
from test.TestClasses import MyLeaf, NodeForTest, myleaf_ctor

class TestTwoThreeTree(unittest.TestCase):
    """2-3 木に関する挿入操作のテスト

    root への挿入テスト
    """

    def setUp(self):
        print("2-3 tree test setup")

        # 2-3木を作成してテスト
        self.tht: TwoThreeTree = TwoThreeTree[MyLeaf, NodeForTest](myleaf_ctor)

    def tearDown(self):
        pass

    def test_create_tree_1(self):
        """root への１つ目の子要素の挿入
        """
        self.tht.visualizeGraph(True, "sample_only_root_" + datetime.datetime.now().isoformat())

        self.tht.insert(NodeForTest("01", 2.0))

        self.assertEqual(2, self.tht.size)
        self.assertEqual(1, self.tht.leafSize)
        self.assertEqual(2, self.tht.height)

        self.tht.visualizeGraph(True, "sample_only_1_" + datetime.datetime.now().isoformat())

    def test_create_tree_2(self):
        """root への２つ目の子要素の挿入

        new_key < key1 の場合
        """
        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 1.0))

        self.assertEqual(3, self.tht.size)
        self.assertEqual(2, self.tht.leafSize)
        self.assertEqual(2, self.tht.height)

        self.tht.visualizeGraph(True, "sample_only_2_" + datetime.datetime.now().isoformat())

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

        self.tht.visualizeGraph(True, "sample_only_3_" + datetime.datetime.now().isoformat())

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
