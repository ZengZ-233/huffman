import heapq
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

# 哈夫曼树节点类
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# 1. 哈夫曼树构建
def build_huffman_tree(freq_map):
    # 检查频率映射是否为空，如果为空则输出错误信息并返回None
    if not freq_map:  
        print("字符频率映射为空，请检查输入数据")
        return None
    # 创建一个最小堆，堆中的元素是Node对象，每个Node对象包含字符和对应的频率
    heap = [Node(char, freq) for char, freq in freq_map.items()]
    # 将列表转换为堆（heapify操作）
    heapq.heapify(heap)
    # 当堆中有多个元素时，继续合并节点
    while len(heap) > 1:
        # 弹出堆中的最小频率节点，构成左子树
        left = heapq.heappop(heap)
        # 弹出堆中的下一个最小频率节点，构成右子树
        right = heapq.heappop(heap)
        # 创建一个新的父节点，频率为两个子节点频率的和
        new_node = Node(None, left.freq + right.freq)
        # 将左子节点和右子节点分别连接到父节点
        new_node.left = left
        new_node.right = right
        # 将新的父节点重新放回堆中
        heapq.heappush(heap, new_node)
    # 如果堆为空，说明构建哈夫曼树失败
    if not heap:
        print("哈夫曼树构建失败：堆为空")
        return None
    # 返回堆中剩下的唯一节点，即哈夫曼树的根节点
    return heap[0]


# 2. 生成哈夫曼编码
def generate_huffman_codes(root, current_code="", codes=None):
    if codes is None:
        codes = {}

    if root is not None:
        if root.char is not None:
            codes[root.char] = current_code
        generate_huffman_codes(root.left, current_code + "0", codes)
        generate_huffman_codes(root.right, current_code + "1", codes)

    return codes

# 可视化哈夫曼树
def draw_huffman_tree(node, data):
    # 使用一个字典来追踪节点位置
    saw = defaultdict(int)

    def create_graph(G, node, p_name="initvalue", pos={}, x=0, y=0, layer=1):
        if not node:
            return
        name = str(node.char if node.char else node.freq)
        print(f"node.name: {name}, x,y: ({x},{y}) layer: {layer}")
        saw[name] += 1
        if name in saw.keys():
            name += ' ' * saw[name]
        if p_name != "initvalue":
            G.add_edge(p_name, name)
        pos[name] = (x, y)

        # 递归绘制左子树和右子树
        l_x, l_y = x - 1 / (3 * layer), y - 1
        l_layer = layer + 1
        create_graph(G, node.left, name, x=l_x, y=l_y, pos=pos, layer=l_layer)

        r_x, r_y = x + 1 / (3 * layer), y - 1
        r_layer = layer + 1
        create_graph(G, node.right, name, x=r_x, y=r_y, pos=pos, layer=r_layer)
        return G, pos

    # 创建图和绘制位置
    graph = nx.DiGraph()
    graph, pos = create_graph(graph, node)
    
    # 设置绘图
    fig, ax = plt.subplots(figsize=(8, 10))
    color_map = []

    for degree in graph.out_degree:
        if degree[1] == 0:  # 叶子节点
            color_map.append('blue')
        else:
            color_map.append('green')
    
    # 绘制网络图
    nx.draw_networkx(graph, pos, ax=ax, node_size=1000, node_color=color_map, with_labels=True, font_size=10)
    plt.show()

# 3. 数据压缩
def compress(data, huffman_codes):
    return ''.join(huffman_codes[char] for char in data)

# 4. 数据解压缩
def decompress(encoded_data, root):
    # 用来存储解压后的字符列表
    decoded_data = []
    # 当前节点初始化为哈夫曼树的根节点
    current_node = root
    # 遍历编码后的数据（每个bit）
    for bit in encoded_data:
        # 如果bit是"0"，则沿着左子树继续向下
        if bit == "0":
            current_node = current_node.left
        # 如果bit是"1"，则沿着右子树继续向下
        else:
            current_node = current_node.right
        # 如果当前节点是叶子节点（字符节点），则将字符添加到解压数据中
        if current_node.char is not None:
            decoded_data.append(current_node.char)
            # 解码完成后，回到根节点，继续解码下一个字符
            current_node = root  
    # 将解压后的字符列表合并为一个字符串并返回
    return ''.join(decoded_data)


# 5. 从文本文件中读取内容
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# 6. 计算固定长度编码下的比特数
def calculate_fixed_length_bits(data, num_chars=10, bits_per_char=4):
    # 每个字符使用固定比特数
    return len(data) * bits_per_char

# 7. 计算哈夫曼编码下的比特数
def calculate_huffman_bits(data, huffman_codes):
    return sum(len(huffman_codes[char]) for char in data)

# 8. 主函数：读取文件并进行哈夫曼编码和解压缩，并比较压缩效果
def huffman_compress_decompress(input_file, output_file_compressed, output_file_decompressed):
    # 读取文本文件
    data = read_file(input_file)
    
    # 计算字符频率
    freq_map = {}
    for char in data:
        if char in freq_map:
            freq_map[char] += 1
        else:
            freq_map[char] = 1
    
    # 生成哈夫曼树
    root = build_huffman_tree(freq_map)
    
    # 生成哈夫曼编码
    huffman_codes = generate_huffman_codes(root)

    # 打印每个字符及其对应的哈夫曼编码
    print("Huffman编码:")
    for char, code in huffman_codes.items():
        print(f"字符: '{char}' => Huffman编码为: {code}")

    # 计算固定长度编码比特数
    fixed_length_bits = calculate_fixed_length_bits(data)
    
    # 压缩数据
    compressed_data = compress(data, huffman_codes)
    
    # 计算哈夫曼编码下的比特数
    huffman_bits = calculate_huffman_bits(data, huffman_codes)
    
    # 解压缩数据
    decompressed_data = decompress(compressed_data, root)

    # 将压缩后的数据写入输出文件
    with open(output_file_compressed, 'w') as file:
        file.write(compressed_data)
    
    # 将解压后的数据写入输出文件
    with open(output_file_decompressed, 'w') as file:
        file.write(decompressed_data)
    
    # 打印压缩和解压的结果
    print(f"\n原始数据: {data}")  
    print(f"压缩后的数据: {compressed_data}")  
    print(f"解压后的数据: {decompressed_data}") 
    
    # 输出比特数对比
    print(f"\n固定长度编码下的比特数: {fixed_length_bits}")
    print(f"哈夫曼编码下的比特数: {huffman_bits}")
    print(f"压缩比: {fixed_length_bits / huffman_bits:.2f}")
    
    # 绘制哈夫曼树
    draw_huffman_tree(root, huffman_codes)

    return compressed_data, decompressed_data


if __name__ == "__main__":
    input_file = 'huffman.txt'  # 输入文本文件路径
    output_file_compressed = 'huffman_compressed.txt'  # 输出压缩后的文件
    output_file_decompressed = 'huffman_decompressed.txt'  # 输出解压后的文件

    # 执行哈夫曼压缩与解压缩
    huffman_compress_decompress(input_file, output_file_compressed, output_file_decompressed)
