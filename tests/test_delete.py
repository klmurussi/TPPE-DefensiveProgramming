import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from btree.tree import BTree
from btree.node import BTreeNode 

def create_specific_delete_test_tree_structure():
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

def test_delete_non_existing_key(capsys):
    b_tree = create_specific_delete_test_tree_structure()

    expected_message = "A chave 2 não existe na árvore. Nenhuma ação foi tomada."

    key_to_delete = 2 

    capsys.readouterr() 
    b_tree.delete(key_to_delete)
    captured = capsys.readouterr() 

    assert expected_message in captured.out
    
    capsys.readouterr()
    b_tree.print_tree_bfs()
    tree_after_delete_output = capsys.readouterr().out

    expected_tree_structure = (
        "[20, 40, 60, 85, 105, 125]\n"
        "[1, 5, 10, 15] [25, 30, 35] [45, 50, 55] [65, 70, 75, 80] [90, 95, 100] [110, 115, 120] [130, 135, 140]\n"
    )
    assert tree_after_delete_output == expected_tree_structure, \
        f"A árvore foi modificada indevidamente!\nEsperado:\n{expected_tree_structure}\nObtido:\n{tree_after_delete_output}"

def test_delete_from_leaf_causes_redistribution_left_borrow(capsys):
    b_tree = create_specific_delete_test_tree_structure()
    key_to_delete = 25 

    capsys.readouterr()
    b_tree.delete(key_to_delete)
    captured_messages = capsys.readouterr().out

    assert f"Chave {key_to_delete} removida com sucesso." in captured_messages

    capsys.readouterr()
    b_tree.print_tree_bfs()
    tree_final_output = capsys.readouterr().out

    expected_tree_structure = (
        "[15, 40, 60, 85, 105, 125]\n" 
        "[1, 5, 10] [20, 30, 35] [45, 50, 55] [65, 70, 75, 80] [90, 95, 100] [110, 115, 120] [130, 135, 140]\n"  
    )

    assert tree_final_output == expected_tree_structure

def test_delete_from_leaf_causes_redistribution_right_borrow(capsys):
    b_tree = create_specific_delete_test_tree_structure()
    key_to_delete = 45 

    capsys.readouterr()
    b_tree.delete(key_to_delete)
    captured_messages = capsys.readouterr().out

    assert f"Chave {key_to_delete} removida com sucesso." in captured_messages

    capsys.readouterr()
    b_tree.print_tree_bfs()
    tree_final_output = capsys.readouterr().out

    expected_tree_structure = (
        "[20, 40, 65, 85, 105, 125]\n" 
        "[1, 5, 10, 15] [25, 30, 35] [50, 55, 60] [70, 75, 80] [90, 95, 100] [110, 115, 120] [130, 135, 140]\n"  
    )
    assert tree_final_output == expected_tree_structure

def test_delete_causes_merge_with_left_sibling_t4(capsys):
    b_tree = create_specific_delete_test_tree_structure() 
    key_to_delete = 115

    capsys.readouterr() 
    b_tree.delete(key_to_delete)
    captured_messages = capsys.readouterr().out 

    assert f"Chave {key_to_delete} removida com sucesso." in captured_messages

    capsys.readouterr()
    b_tree.print_tree_bfs()
    tree_final_output = capsys.readouterr().out

    expected_tree_structure = (
        "[20, 40, 60, 85, 125]\n"
        "[1, 5, 10, 15] [25, 30, 35] [45, 50, 55] [65, 70, 75, 80] [90, 95, 100, 105, 110, 120] [130, 135, 140]\n" 
    )
    assert tree_final_output == expected_tree_structure

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

def test_delete_propagates_underflow_and_decreases_height(capsys):
    b_tree = create_delete_propagate_underflow_test_tree() 
    key_to_delete = 5 

    capsys.readouterr() 
    b_tree.delete(key_to_delete)
    captured_messages = capsys.readouterr().out 

    assert f"Chave {key_to_delete} removida com sucesso." in captured_messages

    capsys.readouterr() 
    b_tree.print_tree_bfs()
    tree_final_output = capsys.readouterr().out

    expected_tree_structure = (
        "[30, 50]\n" 
        "[10, 15] [45] [55]\n"
    )
    assert tree_final_output == expected_tree_structure

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

def test_delete_internal_node_case_predecessor(capsys):
    b_tree = create_tree_for_predecessor_test()
    key_to_delete = 50 

    capsys.readouterr()
    b_tree.delete(key_to_delete)
    captured_messages = capsys.readouterr().out

    assert f"Chave {key_to_delete} removida com sucesso." in captured_messages

    capsys.readouterr()
    b_tree.print_tree_bfs()
    tree_final_output = capsys.readouterr().out

    expected_tree_structure = (
        "[49]\n" 
        "[30, 40, 45] [55, 60]\n"
        "[26, 27] [31, 32] [41, 42] [47, 48] [51, 52] [56, 57] [61, 62]\n" 
    )
    assert tree_final_output == expected_tree_structure

def test_delete_internal_node_case_sucessor(capsys):
    b_tree = create_tree_for_successor_test()
    key_to_delete = 50 

    capsys.readouterr()
    b_tree.delete(key_to_delete)
    captured_messages = capsys.readouterr().out

    assert f"Chave {key_to_delete} removida com sucesso." in captured_messages

    capsys.readouterr()
    b_tree.print_tree_bfs()
    tree_final_output = capsys.readouterr().out

    expected_tree_structure = (
        "[51]\n"
        "[40, 45] [55, 60, 65]\n"
        "[36, 37] [41, 42] [46, 47] [52, 53] [56, 57] [61, 62] [66, 67]\n" 
    )

    assert tree_final_output == expected_tree_structure

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

def test_delete_internal_node_case_merge(capsys):
    b_tree = create_tree_for_merge_case_test()
    key_to_delete = 50 

    capsys.readouterr()
    b_tree.delete(key_to_delete)
    captured_messages = capsys.readouterr().out

    assert f"Chave {key_to_delete} removida com sucesso." in captured_messages

    capsys.readouterr()
    b_tree.print_tree_bfs()
    tree_final_output = capsys.readouterr().out

    expected_tree_structure = (
        "[40, 45, 60, 65]\n"
        "[36, 37] [41, 42] [46, 47, 56, 57] [61, 62] [66, 67]\n"
    )

    assert tree_final_output == expected_tree_structure