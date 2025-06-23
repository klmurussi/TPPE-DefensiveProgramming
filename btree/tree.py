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