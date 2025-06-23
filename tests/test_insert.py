import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from btree.tree import BTree
from btree.node import BTreeNode 

def create_initial_tree(t_val, initial_values):
    tree = BTree(t_val)
    for val in initial_values:
        tree.insert(val)
    return tree

def test_insert_first_key_t2(capsys):
    t = 2
    b_tree = BTree(t) 

    b_tree.insert(10)

    captured_initial = capsys.readouterr()
    assert captured_initial.out == "" 

    capsys.readouterr() 
    b_tree.print_tree_bfs()
    tree_output = capsys.readouterr().out

    expected_output = "[10]\n"
    assert tree_output == expected_output, f"Saída incorreta!\nEsperado:\n{expected_output}\nObtido:\n{tree_output}"
    assert b_tree.root.keys == [10]
    assert b_tree.root.num_keys() == 1
    assert b_tree.root.leaf == True

def test_insert_into_leaf_no_split_t3(capsys):
    t = 3 
    b_tree = create_initial_tree(t, [10, 5, 20])
    b_tree.insert(15)

    captured_initial = capsys.readouterr()
    assert captured_initial.out == "" 

    capsys.readouterr()
    b_tree.print_tree_bfs()
    tree_output = capsys.readouterr().out

    expected_output = "[5, 10, 15, 20]\n"
    assert tree_output == expected_output, f"Saída incorreta!\nEsperado:\n{expected_output}\nObtido:\n{tree_output}"
    assert b_tree.root.keys == [5, 10, 15, 20]
    assert b_tree.root.num_keys() == 4
    assert b_tree.root.leaf == True

def test_insert_duplicate_key(capsys):
    t = 2
    b_tree = create_initial_tree(t, [10, 20])
    b_tree.insert(10) 

    captured = capsys.readouterr()

    expected_message = "A chave 10 já existe na árvore. Nenhuma ação foi tomada."
    assert expected_message in captured.out