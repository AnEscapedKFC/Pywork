import hashlib  # 用于哈希值计算
import randomB
import os
import time

global root1
global node1
file_path = "D:/1.txt"  # 请替换为实际文件路径
# 默克尔树节点类的定义
class MerkleNode(object):
    def __init__(self, left=None, right=None, data=None):
        self.left = left
        self.right = right
        # data中保存着哈希值
        self.data = data

# 以递归的方式构建默克尔树
def createTree(nodes): # nodes为叶子节点列表
    list_len = len(nodes)
    if list_len == 0:
        return 0
    else:
        while list_len % 2 != 0:
            nodes.extend(nodes[-1:]) #extend方法用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）；此处当列表中的节点为奇数时，复制列表中的最后一个元素。
            list_len = len(nodes)
        secondary = [] # 树节点列表
        # 两两合并节点，并计算其哈希值
        for k in [nodes[x:x + 2] for x in range(0, list_len, 2)]: # 创建了一个包含两个叶子节点的子列表k。
            d1 = k[0].data.encode()
            d2 = k[1].data.encode()
            sha256 = hashlib.sha256()
            sha256.update(d1 + d2)
            newdata = sha256.hexdigest() # 以十六进制表示
            node = MerkleNode(left=k[0], right=k[1], data=newdata) # 创建一个新的节点，并指定左右孩子（若无，则复制兄弟的孩子）
            secondary.append(node)
        if len(secondary) == 1:
            return secondary[0]
        else:
            return createTree(secondary)

def BFS(root):
    print('开始广度优先搜索，构建默克尔树...')
    queue = [root]  # 初始队列，根节点入队
    current_level = 1  # 当当前层级

    while queue:
        print("层级:", current_level)  # 输出当前层级
        num_nodes_in_current_level = len(queue)

        for i in range(num_nodes_in_current_level):
            node = queue.pop(0)
            print("Hash value:", node.data)

            # 将左右子节点入队
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        current_level += 1  # 进入下一层

binary_files = []

b1_list = []

def mk_SubFile(des_path, sub, buf, binary_files):
    # 省略不变的部分
    binary_files.append(buf)
    return sub + 1

def mk_SubFile(des_path, sub, buf, binary_files):
    filename = os.path.join(des_path, f"subfile_{sub}")
    print(f'正在生成子文件: {filename}')
    with open(filename, 'wb') as fout:
        fout.write(buf)
        binary_files.append(buf)
        return sub + 1

def binary_string(data):
    return ''.join(format(byte, '08b') for byte in data)

def split_By_size(file_path, size, des_path):
    binary_files = []
    with open(file_path, 'rb') as fin:
        buf = fin.read(size)
        sub = 1
        while len(buf) > 0:
            sub = mk_SubFile(des_path, sub, buf, binary_files)
            buf = fin.read(size)
    print(f"拆分完成，文件存放在路径: {des_path}")
    return binary_files

def write_Merkle_Tree_to_file(root, filename, filepath):
    full_filepath = os.path.join(filepath, filename)
    with open(full_filepath, 'w') as file:
        file.write("Merkle Tree:\n")
        write_Merkle_Node_to_file(root, file, 0)

def write_Merkle_Node_to_file(node, file, level):
    if node:
        file.write(f"层级: {level}\n")
        file.write(f"Hash value: {node.data}\n")
        if node.left or node.right:
            write_Merkle_Node_to_file(node.left, file, level + 1)
            write_Merkle_Node_to_file(node.right, file, level + 1)

def CreateMerkleTree(file_path):
    start = time.perf_counter()
    with open(file_path, 'rb') as fin:
        data = fin.read()
        file_size = len(data)
        size = file_size // 31  # 计算每个子文件的大小
    des_path = "D:/6"  # 请替换为你想要存放拆分文件的目标路径
    binary_files = split_By_size(file_path, size, des_path)
    # 输出二进制数据列表
    for i, data in enumerate(binary_files):
        binary_str = binary_string(data)
        b1_list.append(binary_str)
    # blocks = ['11111111111111111000000010000000000000000', '11111111111111111000000000000000010000000', '11111111111111110000000000000000000000011', '11111111111111111000000000000000000000001','11111101111111111000000100000000000000001']
    node1 = []# 创建一个列表，用于存储默克尔树的节点
    #print(blocks)
    print("节点哈希值：")
    for element in b1_list:  # 遍历示例数据
        sha256 = hashlib.sha256()  # 使用SHA-256哈希算法
        sha256.update(element.encode())
        d = sha256.hexdigest()  # 计算节点的信息摘要
        node1.append(MerkleNode(data=d))  # 添加至默克尔树节点中
        print(f"{element}:{d}")
    root1 = createTree(node1)  # 创建默克尔根节点
    BFS(root1)  # 基于BFS算法构建默克尔树并输出所有的哈希(摘要)
    print("根节点的值为:", root1.data)  # 输出根节点的值
    write_Merkle_Tree_to_file(root1, "Merkle1_Tree.txt", "F:\hashpython\Scripts")  # 写入
    print("Merkle树已写入文件 F:\hashpython\Scripts")
    end = time.perf_counter()
    print("运行耗时", end-start)

