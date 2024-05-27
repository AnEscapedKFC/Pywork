import time
start = time.perf_counter()
def read_merkle_tree_from_file(filename):
    merkle_tree = []
    level = 0
    with open(filename, 'r') as file:
        lines = file.readlines()[1:]
        for line in lines:
            if ":" in line.strip():  # Ignore empty lines
                if "value" in line.strip():
                    hash_value = line.strip().split(': ')[-1]
                    merkle_tree[level].append(hash_value)
                else:
                    level = int(line.strip().split(':')[-1])
                    if len(merkle_tree) < level + 1:
                        merkle_tree.append([])
    return merkle_tree

def compare_merkle_trees(tree1, tree2):
    different_nodes = []
    level = 0
    for nodes1, nodes2 in zip(tree1, tree2):
        if len(different_nodes) < level + 1:
            different_nodes.append([])
        for node1, node2 in zip(nodes1, nodes2):
            if node1 != node2:
                different_nodes[level].append((node1, node2))
        level += 1
    return different_nodes

# if __name__ == "__main__":
#     flag = True
#     file1 = "D:/king/Merkle1_Tree.txt"
#     file2 = "D:/king/Merkle1_Tree.txt"
#     with open("D:/king/fxnb.txt","w") as fp3:
#         merkle_tree1 = read_merkle_tree_from_file(file1)
#         merkle_tree2 = read_merkle_tree_from_file(file2)
#         different_nodes = compare_merkle_trees(merkle_tree1, merkle_tree2)
#         # print(different_nodes[0][0])
#         # if (different_nodes[0][0] == None ):
#         flag = False
#
#         for level in range(len(different_nodes)):
#             if different_nodes[level]:
#                 fp3.write(f"第{level}层：\n")
#                 flag = True
#                 for different_nodes_tuple in different_nodes[level]:
#                     fp3.write(f"{different_nodes_tuple[0]} <--> {different_nodes_tuple[0]}\n")
#         if flag == False:
#             print("No differences found.\n")


end = time.perf_counter()
print("运行耗时", end-start)
