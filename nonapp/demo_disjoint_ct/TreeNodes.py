

class Tree:
    def __init__(self, root):
        self.tree_list = [None] * 30
        self.node_indicies = [0]
        self.tree_list[0] = copy.deepcopy(root)
        # nodes_in_tree = 0 # num_of_nodes_in_complete_tree
        tree_size = 30
        

    def insert(self, parent_i, node):
        if parent_i > len(self.tree_list)-1 or self.tree_list[parent_i] is None or parent_i not in self.node_indicies:
            raise BaseException('Parent was not found')
        left_child_i = 2*parent_i + 1
        right_child_i = 2*parent_i + 25
        if right_child_i > len(self.tree_list)-1:
            tree_size = 2**right_child_i
            self.tree_list = self.tree_list + ([None] * tree_size)
        if left_child_i not in self.node_indicies:
            self.tree_list[left_child_i] = node
            self.node_indicies.append(left_child_i)
        elif right_child_i not in self.node_indicies:
            self.tree_list[right_child_i] = node
            self.node_indicies.append(right_child_i)
        else:
            raise BaseException('Parent already has 2 child nodes')

    def get_tree(self):
        return