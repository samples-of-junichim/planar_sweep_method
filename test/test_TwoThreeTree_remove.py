from dataclasses import dataclass
import datetime
import unittest
from TwoThreeTree import Leaf, Node, TwoThreeTree
from test.TestClasses import MyLeaf, NodeForTest, myleaf_ctor

class TestTwoThreeTree(unittest.TestCase):
    """2-3 木に関する削除操作のテスト
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

        # root 要素の left_max, mid_max をチェック
        self.tht.visualizeGraph(True, "sample_" + datetime.datetime.now().isoformat())

        self.tht.delete(NodeForTest("01", 5.0))

        self.assertEqual(15, self.tht.size)
        self.assertEqual(8, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        # root 要素の left_max, mid_max をチェック
        self.tht.visualizeGraph(True, "sample_" + datetime.datetime.now().isoformat())

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

    def test_remove_tree_10(self):
        """子要素を削除

        残りの葉 3要素
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        self.tht.delete(NodeForTest("08", 10.0))
        self.tht.delete(NodeForTest("04", 9.0))
        self.tht.delete(NodeForTest("09", 8.0))
        self.tht.delete(NodeForTest("03", 7.0))
        self.tht.delete(NodeForTest("02", 5.0))
        self.tht.delete(NodeForTest("05", 4.0))

        self.assertEqual(4, self.tht.size)
        self.assertEqual(3, self.tht.leafSize)
        self.assertEqual(2, self.tht.height)

        self.tht.visualizeGraph(True, "sample_left_3_" + datetime.datetime.now().isoformat())

    def test_remove_tree_11(self):
        """子要素を削除

        残りの葉 2要素
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        self.tht.delete(NodeForTest("08", 10.0))
        self.tht.delete(NodeForTest("04", 9.0))
        self.tht.delete(NodeForTest("09", 8.0))
        self.tht.delete(NodeForTest("03", 7.0))
        self.tht.delete(NodeForTest("02", 5.0))
        self.tht.delete(NodeForTest("05", 4.0))
        self.tht.delete(NodeForTest("07", 3.0))

        self.assertEqual(3, self.tht.size)
        self.assertEqual(2, self.tht.leafSize)
        self.assertEqual(2, self.tht.height)

        self.tht.visualizeGraph(True, "sample_left_2_" + datetime.datetime.now().isoformat())

    def test_remove_tree_12(self):
        """子要素を削除

        残りの葉 1要素
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        self.tht.delete(NodeForTest("08", 10.0))
        self.tht.delete(NodeForTest("04", 9.0))
        self.tht.delete(NodeForTest("09", 8.0))
        self.tht.delete(NodeForTest("03", 7.0))
        self.tht.delete(NodeForTest("02", 5.0))
        self.tht.delete(NodeForTest("05", 4.0))
        self.tht.delete(NodeForTest("07", 3.0))
        self.tht.delete(NodeForTest("01", 2.0))

        self.assertEqual(2, self.tht.size)
        self.assertEqual(1, self.tht.leafSize)
        self.assertEqual(2, self.tht.height)

        self.tht.visualizeGraph(True, "sample_left_1_" + datetime.datetime.now().isoformat())

    def test_remove_tree_13(self):
        """子要素を削除

        残りの葉 0要素（ルートのみ）
        """
        self.assertEqual(16, self.tht.size)
        self.assertEqual(9, self.tht.leafSize)
        self.assertEqual(4, self.tht.height)

        self.tht.delete(NodeForTest("08", 10.0))
        self.tht.delete(NodeForTest("04", 9.0))
        self.tht.delete(NodeForTest("09", 8.0))
        self.tht.delete(NodeForTest("03", 7.0))
        self.tht.delete(NodeForTest("02", 5.0))
        self.tht.delete(NodeForTest("05", 4.0))
        self.tht.delete(NodeForTest("07", 3.0))
        self.tht.delete(NodeForTest("01", 2.0))
        self.tht.delete(NodeForTest("06", 1.0))

        self.assertEqual(1, self.tht.size)
        self.assertEqual(0, self.tht.leafSize)
        self.assertEqual(1, self.tht.height)

        self.tht.visualizeGraph(True, "sample_left_only_root_" + datetime.datetime.now().isoformat())
