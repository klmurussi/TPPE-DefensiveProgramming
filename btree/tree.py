import icontract
from collections import deque
from .node import BTreeNode
from copy import deepcopy

@icontract.invariant(lambda self: self._check_all_leaves_at_same_level(), "All leaves must be at the same level in the B-tree.")
@icontract.invariant(lambda self: self._check_all_keys_ordered(), "All keys must be in increasing order within all nodes.")
class BTree:
    def __init__(self, t: int):
        self.t = t
        self.root = BTreeNode(t, leaf=True)

    def _check_all_leaves_at_same_level(self) -> bool:
        if not self.root or self.root.num_keys() == 0:
            return True

        leaf_level = -1
        q = deque([(self.root, 0)])

        while q:
            current_node, level = q.popleft()

            if current_node.leaf:
                if leaf_level == -1:
                    leaf_level = level
                elif leaf_level != level:
                    return False
            else:
                for child in current_node.children:
                    if child:
                        q.append((child, level + 1))
        return True

    def _check_all_keys_ordered(self) -> bool:
        if not self.root:
            return True
        q = deque([self.root])
        while q:
            node = q.popleft()
            if not all(node.keys[i] <= node.keys[i+1] for i in range(node.num_keys() - 1)):
                return False
            if not node.leaf:
                for child in node.children:
                    if child:
                        q.append(child)
        return True

    @icontract.ensure(lambda self, result: isinstance(result, bool))
    def _check_node_key_counts(self) -> bool:
        if not self.root:
            return True
        q = deque([self.root])
        while q:
            node = q.popleft()
            if node == self.root:
                if not (1 <= node.num_keys() <= (2 * self.t - 1)):
                    return False
            else:
                if not (self.t - 1 <= node.num_keys() <= (2 * self.t - 1)):
                    return False
            if not node.leaf:
                for child in node.children:
                    if child:
                        q.append(child)
        return True

    @icontract.ensure(lambda self, result: isinstance(result, bool))
    def _check_node_child_counts(self) -> bool:
        if not self.root:
            return True

        if self.root.leaf:
            if self.root.num_children() != 0:
                return False
            return True

        q = deque([self.root])
        while q:
            node = q.popleft()
            if node.leaf:
                if node.num_children() != 0:
                    return False
                continue

            if node == self.root:
                if not (2 <= node.num_children() <= (2 * self.t)):
                    return False
            else:
                if not (self.t <= node.num_children() <= (2 * self.t)):
                    return False

            if node.num_children() != node.num_keys() + 1:
                return False

            for child in node.children:
                if child:
                    q.append(child)
                else:
                    return False
        return True

    @icontract.ensure(lambda result: result >= 0)
    def _get_height(self) -> int:
        if not self.root or self.root.num_keys() == 0:
            return 0

        q = deque([(self.root, 0)])
        height = 0
        while q:
            current_node, level = q.popleft()
            height = max(height, level)
            if not current_node.leaf:
                for child in current_node.children:
                    if child:
                        q.append((child, level + 1))
        return height

    def search(self, k: int, node: BTreeNode = None):
        if node is None:
            node = self.root

        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        if i < len(node.keys) and node.keys[i] == k:
            return (node, i)

        if node.leaf:
            return None

        if not node.children:
            return None

        return self.search(k, node.children[i])

    def print_tree_bfs(self):
        if self.root is None or not self.root.keys:
            return

        queue = deque([(self.root, 0)])

        current_level = 0
        current_line_parts = []

        while queue:
            node, level = queue.popleft()

            if level > current_level:
                print(" ".join(current_line_parts))
                current_line_parts = []
                current_level = level

            current_line_parts.append(node.display_string())

            if not node.leaf:
                for child in node.children:
                    if child:
                        queue.append((child, level + 1))

        if current_line_parts:
            print(" ".join(current_line_parts))

    def _split_child(self, parent: BTreeNode, child_index: int):
        t = self.t
        full_child = parent.children[child_index]
        new_node = BTreeNode(t, leaf=full_child.leaf)

        mid_key = full_child.keys[t - 1]

        new_node.keys = full_child.keys[t:]

        full_child.keys = full_child.keys[:t - 1]

        if not full_child.leaf:
            new_node.children = full_child.children[t:]
            full_child.children = full_child.children[:t]

        parent.children.insert(child_index + 1, new_node)
        parent.keys.insert(child_index, mid_key)
        parent.orderkeys()

    def insert_non_full(self, node: BTreeNode, k: int):
        node.keys.append(k)
        node.orderkeys()

    def bottom_up_correction(self, node_to_check: BTreeNode, path_to_root: list):
        current_node = node_to_check

        while current_node.is_full():
            if not path_to_root:
                t = self.t
                new_root = BTreeNode(t, leaf=False)
                new_root.children.append(current_node)

                self._split_child(new_root, 0)
                self.root = new_root
                break
            else:
                parent, child_index_in_parent = path_to_root.pop()
                self._split_child(parent, child_index_in_parent)
                current_node = parent

    @icontract.snapshot(lambda self: self._get_height(), name="old_height_value")
    @icontract.require(lambda self, k: self.search(k, self.root) is None, "Key to be inserted must not exist in the tree.")
    @icontract.ensure(lambda self, k: self.search(k, self.root) is not None, "Inserted key must exist in the tree after operation.")
    @icontract.ensure(lambda self: self._check_node_key_counts(), "Node key counts must be valid after insert.")
    @icontract.ensure(lambda self: self._check_node_child_counts(), "Node child counts must be valid after insert.")
    @icontract.ensure(
            lambda self, result:
                (self._get_height() == result) or (self._get_height() == result + 1),
                "Altura após inserção deve ser a mesma ou aumentar em 1"
        )
    def insert(self, k: int):
        root = self.root
        old_height = self._get_height()

        if self.search(k, self.root):
            print(f"A chave {k} já existe na árvore. Nenhuma ação foi tomada.")
            return old_height

        if root.num_keys() == 0:
            self.insert_non_full(root, k)
            return old_height

        current_node = self.root
        parent_path = []

        while not current_node.leaf:
            i = 0
            while i < len(current_node.keys) and k > current_node.keys[i]:
                i += 1

            parent_path.append((current_node, i))
            current_node = current_node.children[i]

        self.insert_non_full(current_node, k)
        self.bottom_up_correction(current_node, parent_path)

        return old_height

    @icontract.require(lambda self, k: self.search(k, self.root) is not None, "Key to be deleted must exist in the tree.")
    @icontract.ensure(lambda self, k: self.search(k, self.root) is None, "Deleted key must not exist in the tree after operation.")
    @icontract.ensure(lambda self: self._check_node_key_counts(), "Node key counts must be valid after delete.")
    @icontract.ensure(lambda self: self._check_node_child_counts(), "Node child counts must be valid after delete.")
    @icontract.ensure(
        lambda self, result:
            self._get_height() == result or self._get_height() == result - 1,
        description="Altura após fusão deve ser a mesma ou diminuir em 1"
    )
    def delete(self, k: int):
        root = self.root

        if not self.search(k, self.root):
            print(f"A chave {k} não existe na árvore. Nenhuma ação foi tomada.")
            return

        old_height = self._get_height()

        self._delete_recursive(self.root, k)

        if self.root.num_keys() == 0 and not self.root.leaf:
             self.root = self.root.children[0]

        print(f"Chave {k} removida com sucesso.")
        return old_height

    def _delete_recursive(self, node: BTreeNode, k: int):
        i = 0
        while i < node.num_keys() and k > node.keys[i]:
            i += 1

        if i < node.num_keys() and node.keys[i] == k:
            if node.leaf:
                node.keys.pop(i)
                node.orderkeys()
            else:
                self._delete_internal_node_key(node, i)
                pass

        else:
            if node.leaf:
                return

            self._delete_recursive(node.children[i], k)
            self._ensure_child_has_enough_keys(node, i)

    def _ensure_child_has_enough_keys(self, parent_node: BTreeNode, child_index: int):
        t = self.t
        child_node = parent_node.children[child_index]

        if not child_node.is_underflow():
            return

        if child_index > 0 and parent_node.children[child_index - 1].num_keys() >= t:
            self._borrow_from_left(parent_node, child_index)
        elif child_index < parent_node.num_children() - 1 and parent_node.children[child_index + 1].num_keys() >= t:
            self._borrow_from_right(parent_node, child_index)
        else:
            if child_index > 0:
                self._merge_nodes(parent_node, child_index - 1)
            else:
                self._merge_nodes(parent_node, child_index)

    def _borrow_from_left(self, parent_node, child_index):
        child_node = parent_node.children[child_index]
        left_sibling = parent_node.children[child_index - 1]

        child_node.keys.insert(0, parent_node.keys[child_index - 1])
        child_node.orderkeys()

        parent_node.keys[child_index - 1] = left_sibling.keys.pop()
        left_sibling.orderkeys()

        if not left_sibling.leaf:
            child_node.children.insert(0, left_sibling.children.pop())

        print("emprestar")

    def _borrow_from_right(self, parent_node, child_index):
        child_node = parent_node.children[child_index]
        right_sibling = parent_node.children[child_index + 1]

        child_node.keys.append(parent_node.keys[child_index])
        child_node.orderkeys()

        parent_node.keys[child_index] = right_sibling.keys.pop(0)
        right_sibling.orderkeys()

        if not right_sibling.leaf:
             child_node.children.append(right_sibling.children.pop(0))

        print("emprestar")

    def _merge_nodes(self, parent: BTreeNode, child_index_left: int):
        left_child = parent.children[child_index_left]
        right_child = parent.children[child_index_left + 1]
        key_from_parent = parent.keys[child_index_left]

        left_child.keys.append(key_from_parent)
        left_child.keys.extend(right_child.keys)
        left_child.orderkeys()

        if not left_child.leaf:
            left_child.children.extend(right_child.children)

        parent.children.pop(child_index_left + 1)
        parent.keys.pop(child_index_left)
        parent.orderkeys()

        if parent == self.root and parent.num_keys() == 0 and not parent.leaf:
            self.root = left_child

    def _find_predecessor(self, node: BTreeNode):
        while not node.leaf:
            node = node.children[node.num_keys()]
        return (node, node.num_keys() - 1)

    def _find_successor(self, node: BTreeNode):
        while not node.leaf:
            node = node.children[0]
        return (node, 0)

    def _delete_internal_node_key(self, node: BTreeNode, key_index: int):
        t = self.t
        k_to_delete = node.keys[key_index]

        left_child = node.children[key_index]
        right_child = node.children[key_index + 1]

        if left_child.num_keys() >= t:
            predecessor_node, predecessor_idx_in_node = self._find_predecessor(left_child)
            predecessor_key = predecessor_node.keys[predecessor_idx_in_node]

            node.keys[key_index] = predecessor_key
            node.orderkeys()

            self._delete_recursive(left_child, predecessor_key)

        elif right_child.num_keys() >= t:
            successor_node, successor_idx_in_node = self._find_successor(right_child)
            successor_key = successor_node.keys[successor_idx_in_node]

            node.keys[key_index] = successor_key
            node.orderkeys()

            self._delete_recursive(right_child, successor_key)

        else:
            left_child.keys.append(k_to_delete)
            left_child.keys.extend(right_child.keys)
            left_child.orderkeys()

            if not left_child.leaf:
                left_child.children.extend(right_child.children)

            node.keys.pop(key_index)
            node.children.pop(key_index + 1)
            node.orderkeys()

            self._delete_recursive(left_child, k_to_delete)