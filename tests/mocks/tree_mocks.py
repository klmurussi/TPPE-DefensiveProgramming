import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from btree.tree import BTree
from btree.node import BTreeNode

def create_bfs_display_test_tree_t3():
    t = 3
    tree = BTree(t)

    root_node = BTreeNode(t, leaf=False)
    root_node.keys = [40]
    tree.root = root_node

    left_child = BTreeNode(t, leaf=False)
    left_child.keys = [20]

    right_child = BTreeNode(t, leaf=False)
    right_child.keys = [60, 80]

    tree.root.children = [left_child, right_child]

    leftleft_grandchild = BTreeNode(t, leaf=True)
    leftleft_grandchild.keys = [10, 15]

    leftright_grandchild = BTreeNode(t, leaf=True)
    leftright_grandchild.keys = [25, 30]

    left_child.children = [leftleft_grandchild, leftright_grandchild]

    rightleft_grandchild = BTreeNode(t, leaf=True)
    rightleft_grandchild.keys = [45, 50]

    rightright_grandchild = BTreeNode(t, leaf=True)
    rightright_grandchild.keys = [90]

    right_child.children = [rightleft_grandchild, rightright_grandchild]

    return tree

def create_borrow_test_tree_t4():
    t = 4 

    tree = BTree(t) 

    root_node = BTreeNode(t, leaf=False) 
    root_node.keys = [20, 40, 60, 85, 105, 125]
    tree.root = root_node 

    child1 = BTreeNode(t, leaf=True) 
    child1.keys = [1, 5, 10, 15]

    child2 = BTreeNode(t, leaf=True) 
    child2.keys = [25, 30, 35]

    child3 = BTreeNode(t, leaf=True) 
    child3.keys = [45, 50, 55]

    child4 = BTreeNode(t, leaf=True) 
    child4.keys = [65, 70, 75, 80]

    child5 = BTreeNode(t, leaf=True) 
    child5.keys = [90, 95, 100]

    child6 = BTreeNode(t, leaf=True) 
    child6.keys = [110, 115, 120]

    child7 = BTreeNode(t, leaf=True) 
    child7.keys = [130, 135, 140]

    tree.root.children = [child1, child2, child3, child4, child5, child6, child7]

    return tree

def create_delete_propagate_underflow_test_tree():
    t = 2 

    tree = BTree(t) 

    root_node = BTreeNode(t, leaf=False) 
    root_node.keys = [30]
    tree.root = root_node 

    parent_left = BTreeNode(t, leaf=False) 
    parent_left.keys = [10]

    parent_right = BTreeNode(t, leaf=False) 
    parent_right.keys = [50]

    root_node.children = [parent_left, parent_right]

    child_L = BTreeNode(t, leaf=True) 
    child_L.keys = [5] 

    child_S = BTreeNode(t, leaf=True) 
    child_S.keys = [15] 

    parent_left.children = [child_L, child_S]

    child_X = BTreeNode(t, leaf=True) 
    child_X.keys = [45]

    child_Y = BTreeNode(t, leaf=True) 
    child_Y.keys = [55]

    parent_right.children = [child_X, child_Y]

    return tree

def create_tree_for_predecessor_test():
    t = 3
    tree = BTree(t)
    root = BTreeNode(t, leaf=False)
    root.keys = [50]
    tree.root = root

    left_child = BTreeNode(t, leaf=False)
    left_child.keys = [30, 40, 45]
    child1 = BTreeNode(t, leaf=True) 
    child1.keys = [26, 27]
    child2 = BTreeNode(t, leaf=True) 
    child2.keys = [31, 32]
    child3 = BTreeNode(t, leaf=True) 
    child3.keys = [41, 42]
    child4 = BTreeNode(t, leaf=True) 
    child4.keys = [47, 48, 49]
    left_child.children = [
        child1, child2, child3, child4
    ]

    right_child = BTreeNode(t, leaf=False)
    right_child.keys = [55, 60]
    child5 = BTreeNode(t, leaf=True) 
    child5.keys = [51, 52]
    child6 = BTreeNode(t, leaf=True) 
    child6.keys = [56, 57]
    child7 = BTreeNode(t, leaf=True) 
    child7.keys = [61, 62]
 
    right_child.children = [
        child5, child6, child7
    ]
    
    root.children = [left_child, right_child]
    return tree

def create_tree_for_successor_test():
    t = 3
    tree = BTree(t)
    root = BTreeNode(t, leaf=False)
    root.keys = [50]
    tree.root = root

    left_child = BTreeNode(t, leaf=False)
    left_child.keys = [40, 45]
    child1 = BTreeNode(t, leaf=True) 
    child1.keys = [36, 37]
    child2 = BTreeNode(t, leaf=True) 
    child2.keys = [41, 42]
    child3 = BTreeNode(t, leaf=True) 
    child3.keys = [46, 47]
    left_child.children = [
        child1, child2, child3
    ]

    right_child = BTreeNode(t, leaf=False)
    right_child.keys = [55, 60, 65]
    child4 = BTreeNode(t, leaf=True) 
    child4.keys = [51, 52, 53]
    child5 = BTreeNode(t, leaf=True) 
    child5.keys = [56, 57]
    child6 = BTreeNode(t, leaf=True) 
    child6.keys = [61, 62]
    child7 = BTreeNode(t, leaf=True) 
    child7.keys = [66, 67]
 
    right_child.children = [
        child4, child5, child6, child7
    ]
    
    root.children = [left_child, right_child]
    return tree

def create_tree_for_merge_case_test():
    t = 3
    tree = BTree(t)
    root = BTreeNode(t, leaf=False)
    root.keys = [50]
    tree.root = root

    left_child = BTreeNode(t, leaf=False)
    left_child.keys = [40, 45]
    child1 = BTreeNode(t, leaf=True) 
    child1.keys = [36, 37]
    child2 = BTreeNode(t, leaf=True) 
    child2.keys = [41, 42]
    child3 = BTreeNode(t, leaf=True) 
    child3.keys = [46, 47]
    left_child.children = [
        child1, child2, child3
    ]

    right_child = BTreeNode(t, leaf=False)
    right_child.keys = [60, 65]
    child4 = BTreeNode(t, leaf=True) 
    child4.keys = [56, 57]
    child5 = BTreeNode(t, leaf=True) 
    child5.keys = [61, 62]
    child6 = BTreeNode(t, leaf=True) 
    child6.keys = [66, 67]
 
    right_child.children = [
        child4, child5, child6
    ]
    
    root.children = [left_child, right_child]
    return tree