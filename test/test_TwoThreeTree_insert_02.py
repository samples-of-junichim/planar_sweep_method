from dataclasses import dataclass
import datetime
import unittest
from TwoThreeTree import Leaf, Node, TwoThreeTree
from test.TestClasses import MyLeaf, NodeForTest, myleaf_ctor

class TestTwoThreeTree(unittest.TestCase):
    """2-3 木に関する挿入操作のテスト

    内部要素（子要素２つ）への挿入
    """

    def setUp(self):
        print("2-3 tree test setup")

        # 2-3木を作成してテスト
        self.tht: TwoThreeTree = TwoThreeTree[MyLeaf, NodeForTest](myleaf_ctor)

    def tearDown(self):
        pass

    def test_create_tree_1(self):
        """内部要素（子要素２つ）への３つ目の子要素の挿入

        左の部分木への挿入
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

    def test_create_tree_2(self):
        """内部要素（子要素２つ）への３つ目の子要素の挿入

        左の部分木への挿入
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

    def test_create_tree_3(self):
        """内部要素（子要素２つ）への３つ目の子要素の挿入

        左の部分木への挿入
        mid < new_key の場合

        中央の部分木への挿入
        new_key < left の場合も同じ
        """
        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 5.0))
        self.tht.insert(NodeForTest("03", 7.0))
        self.tht.insert(NodeForTest("04", 9.0))

        self.tht.insert(NodeForTest("05", 6.0))

        self.assertEqual(8, self.tht.size)
        self.assertEqual(5, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

    def test_create_tree_4(self):
        """内部要素（子要素２つ）への３つ目の子要素の挿入

        中央の部分木への挿入
        left < new_key < mid の場合

        最終的な形
             p
           /  |
          p   p
         /|  /| \
        2 5 7 8 9
        """
        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 5.0))
        self.tht.insert(NodeForTest("03", 7.0))
        self.tht.insert(NodeForTest("04", 9.0))

        self.tht.insert(NodeForTest("05", 8.0))

        self.assertEqual(8, self.tht.size)
        self.assertEqual(5, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

        # 木の形をチェック
        self.tht.visualizeGraph(True, "sample_insert_" + datetime.datetime.now().isoformat())

    def test_create_tree_5(self):
        """内部要素（子要素２つ）への３つ目の子要素の挿入

        中央の部分木への挿入
        mid < new_key の場合

        最終的な形
             p
           /  |
          p   p
         /|  /| \
        2 5 7 9 10
        """
        self.tht.insert(NodeForTest("01", 2.0))
        self.tht.insert(NodeForTest("02", 5.0))
        self.tht.insert(NodeForTest("03", 7.0))
        self.tht.insert(NodeForTest("04", 9.0))

        self.tht.insert(NodeForTest("05", 10.0))

        self.assertEqual(8, self.tht.size)
        self.assertEqual(5, self.tht.leafSize)
        self.assertEqual(3, self.tht.height)

        # 木の形をチェック
        self.tht.visualizeGraph(True, "sample_insert_" + datetime.datetime.now().isoformat())

