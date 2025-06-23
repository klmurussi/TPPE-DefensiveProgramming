import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pytest
import icontract
from tests.mocks.tree_mocks import create_borrow_test_tree_t4, create_delete_propagate_underflow_test_tree, create_tree_for_predecessor_test, create_tree_for_successor_test, create_tree_for_merge_case_test

def test_delete_non_existing_key(capsys):
    b_tree = create_borrow_test_tree_t4()
    key_to_delete = 2

    with pytest.raises(icontract.errors.ViolationError) as excinfo:
        b_tree.delete(key_to_delete)

    expected_message_part = "Key to be deleted must exist in the tree."
    assert expected_message_part in str(excinfo.value)

def test_delete_from_leaf_causes_redistribution_left_borrow(capsys):
    b_tree = create_borrow_test_tree_t4()
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
    b_tree = create_borrow_test_tree_t4()
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
    b_tree = create_borrow_test_tree_t4() 
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