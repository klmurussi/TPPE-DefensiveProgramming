from icontract import ensure
from collections import deque
from .node import BTreeNode

class BTree:
    def __init__(self, t: int):
        self.t = t
        self.root = BTreeNode(t, leaf=True)

    def _check_all_leaves_at_same_level(self) -> bool:
        if not self.root or not self.root.keys:
            return True

        leaf_level = -1
        q = deque([(self.root, 0)]) # Use deque para popleft

        while q:
            current_node, level = q.popleft()

            if current_node.leaf:
                if leaf_level == -1:
                    leaf_level = level
                elif leaf_level != level:
                    return False
            else:
                for child in current_node.children:
                    q.append((child, level + 1))
        return True

    @ensure(lambda result: result is None or \
                           (isinstance(result, tuple) and len(result) == 2 and \
                            isinstance(result[0], BTreeNode) and isinstance(result[1], int)))
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

    def insert(self, k: int):
        root = self.root

        if self.search(k, self.root): 
            print(f"A chave {k} já existe na árvore. Nenhuma ação foi tomada.")
            return

        if root.num_keys() == 0:
            self.insert_non_full(root, k)
            return

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