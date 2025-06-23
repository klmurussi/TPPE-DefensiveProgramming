# main.py
from btree.tree import BTree

if __name__ == "__main__":
    b_tree = BTree(t=2) # Grau mínimo 2, significando 2-3 tree
    keys = []

    while True:
        print ("1 - to insert, 2 - to delete")
        a = input()
        if (int(a) == 1):
            one = input()
            b_tree.insert(int(one))
            b_tree.print_tree_bfs()
        else:
            two = input()
            b_tree.delete(int(two))
            b_tree.print_tree_bfs()

