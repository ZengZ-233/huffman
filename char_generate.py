import random

# 字符及其频率
symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
frequencies = [45, 13, 12, 16, 9, 5, 4, 3, 2, 1]

# 根据字符频率生成对应数量的字符
def generate_random_data(symbols, frequencies):
    data = []
    for symbol, freq in zip(symbols, frequencies):
        data.extend([symbol] * freq)  # 重复字符 freq 次
    random.shuffle(data)  # 打乱字符顺序
    return ''.join(data)

# 将生成的数据写入文件
def write_to_file(file_path, data):
    with open(file_path, 'w') as file:
        file.write(data)

# 主程序
if __name__ == "__main__":
    # 生成随机数据
    random_data = generate_random_data(symbols, frequencies)
    
    # 将数据写入文件
    input_file = 'huffman.txt'
    write_to_file(input_file, random_data)
    
    print(f"数据已写入 {input_file}")
