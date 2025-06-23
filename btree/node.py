from icontract import require, ensure

class BTreeNode:
    @require(lambda t: t >= 2)
    def __init__(self, t: int, leaf: bool):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.children = []

    def __str__(self):
        return f"{'Folha' if self.leaf else 'Interno'} - Chaves: {self.keys}"

    def num_keys(self) -> int:
        return len(self.keys)

    def is_full(self) -> bool:
        # na vdd, ele está cheio com 2 * t -1
        return self.num_keys() == (2 * self.t)

    def is_empty(self) -> bool:
        return self.num_keys() == 0

    def display_string(self) -> str:
        return f"[{', '.join(map(str, self.keys))}]"

    def orderkeys(self):
        self.keys.sort()

    def is_underflow(self) -> bool:
        return self.num_keys() == (self.t - 2)

    def num_children(self) -> int:
        return len(self.children)