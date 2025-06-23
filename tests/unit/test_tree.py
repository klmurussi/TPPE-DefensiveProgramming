import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from tests.mocks.tree_mocks import create_bfs_display_test_tree_t3

def test_print_tree_bfs_output(capsys):
    b_tree = create_bfs_display_test_tree_t3()

    b_tree.print_tree_bfs()

    captured = capsys.readouterr()

    expected_output = (
        "[40]\n"
        "[20] [60, 80]\n"
        "[10, 15] [25, 30] [45, 50] [90]\n"
    )

    assert captured.out == expected_output