import os

def convert_utf8_to_gbk(folder_path):
    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                try:
                    # 读取utf-8编码的文件
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 将内容写入gbk编码的文件
                    with open(file_path, 'w', encoding='gbk') as f:
                        f.write(content)

                    print(f"成功转换: {file_path}")
                except Exception as e:
                    print(f"转换失败: {file_path}，错误: {e}")

# 使用示例
folder_path = 'D:\MirServer\Mir200\Envir\MonItems'  # 替换为你的文件夹路径
convert_utf8_to_gbk(folder_path)
