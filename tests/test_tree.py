import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from btree.tree import BTree
from btree.node import BTreeNode

def mock_tree_for_bfs_test():
    t = 3
    tree = BTree(t)

    # Nível 0: Raiz [40]
    root_node = BTreeNode(t, leaf=False)
    root_node.keys = [40]
    tree.root = root_node

    # Nível 1: Filhos da Raiz
    left_child = BTreeNode(t, leaf=False)
    left_child.keys = [20]

    right_child = BTreeNode(t, leaf=False)
    right_child.keys = [60, 80]

    tree.root.children = [left_child, right_child]

    # Nível 2: Filhos de [20]
    leftleft_grandchild = BTreeNode(t, leaf=True)
    leftleft_grandchild.keys = [10, 15]

    leftright_grandchild = BTreeNode(t, leaf=True)
    leftright_grandchild.keys = [25, 30]

    left_child.children = [leftleft_grandchild, leftright_grandchild]

    # Nível 2: Filhos de [60, 80]
    rightleft_grandchild = BTreeNode(t, leaf=True)
    rightleft_grandchild.keys = [45, 50]

    rightright_grandchild = BTreeNode(t, leaf=True)
    rightright_grandchild.keys = [90]

    right_child.children = [rightleft_grandchild, rightright_grandchild]

    return tree

def test_print_tree_bfs_output(capsys):
    b_tree = mock_tree_for_bfs_test()

    b_tree.print_tree_bfs()

    captured = capsys.readouterr()

    expected_output = (
        "[40]\n"
        "[20] [60, 80]\n"
        "[10, 15] [25, 30] [45, 50] [90]\n"
    )

    assert captured.out == expected_output