
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
        super().__init__(val, parent, get_key, comp_key)

def get_key(v: NodeForTest) -> float:
    return v.key
def comp_key(v1: NodeForTest, v2: NodeForTest) -> int:
    if math.isclose(v1.key, v2.key):
        return 0
    if v1.key < v2.key:
        return -1
    else:
        return 1    
def myleaf_ctor(v: NodeForTest, parent: Node[NodeForTest]):
    return MyLeaf(v, parent)
