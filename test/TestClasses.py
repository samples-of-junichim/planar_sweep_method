
from dataclasses import dataclass
import math
from TwoThreeTree import Leaf, Node

# テスト用の Node 要素
@dataclass
class NodeForTest:
    id: str     # id
    key: float  # キー

class MyLeaf(Leaf[NodeForTest]):

    def __init__(self, val: NodeForTest, parent: Node[NodeForTest] | None):
        super().__init__(val, parent, self._get_key, self._comp_key)

    def _get_key(self, v: NodeForTest) -> str:
        return str(v.key)
    
    def _comp_key(self, v1: NodeForTest, v2: NodeForTest) -> int:
        if math.isclose(v1.key, v2.key):
            return 0
        if v1.key < v2.key:
            return -1
        else:
            return 1    

def myleaf_ctor(v: NodeForTest, parent: Node[NodeForTest]):
    return MyLeaf(v, parent)
