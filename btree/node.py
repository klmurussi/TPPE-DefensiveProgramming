from icontract import require, ensure

class BTreeNode:
    @require(lambda t: t >= 2)
    def __init__(self, t: int, leaf: bool):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.children = []

    @ensure(lambda self: all(self.keys[i] <= self.keys[i+1] for i in range(len(self.keys) - 1)))
    def validate_ordered_keys(self):
        pass

    def __str__(self):
        return f"{'Folha' if self.leaf else 'Interno'} - Chaves: {self.keys}"

    def num_keys(self) -> int:
        return len(self.keys)

    def is_full(self) -> bool:
        return self.num_keys() == (2 * self.t - 1)

    def is_empty(self) -> bool:
        return self.num_keys() == 0

    def display_string(self) -> str:
        return f"[{', '.join(map(str, self.keys))}]"
