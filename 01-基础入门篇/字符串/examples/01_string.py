# 字符串示例

"""
Python 字符串示例
包含：字符串操作、格式化、常用方法
"""

# 1. 字符串创建
def string_creation():
    """字符串创建方式"""
    s1 = "Hello"
    s2 = 'World'
    s3 = """多行
字符串"""
    s4 = f"{s1} {s2}"  # f-string
    
    print(f"s1: {s1}")
    print(f"s2: {s2}")
    print(f"s3: {s3}")
    print(f"s4: {s4}")


# 2. 字符串操作
def string_operations():
    """字符串操作"""
    s = "Hello, Python!"
    
    print(f"原始字符串: {s}")
    print(f"长度: {len(s)}")
    print(f"大写: {s.upper()}")
    print(f"小写: {s.lower()}")
    print(f"首字母大写: {s.capitalize()}")
    print(f"反转: {s[::-1]}")
    
    # 切片
    print(f"\n切片操作:")
    print(f"s[0:5]: {s[0:5]}")
    print(f"s[7:]: {s[7:]}")
    print(f"s[-6:-1]: {s[-6:-1]}")


# 3. 字符串格式化
def string_formatting():
    """字符串格式化"""
    name = "Python"
    version = 3.11
    
    # f-string (推荐)
    s1 = f"{name} {version}"
    
    # format 方法
    s2 = "{} {}".format(name, version)
    
    # % 格式化 (旧式)
    s3 = "%s %.2f" % (name, version)
    
    print(f"f-string: {s1}")
    print(f"format: {s2}")
    print(f"% 格式化: {s3}")
    
    # 格式化选项
    num = 3.14159
    print(f"\n格式化数字:")
    print(f"保留2位小数: {num:.2f}")
    print(f"百分比: {num:.2%}")
    print(f"科学计数法: {num:.2e}")


# 4. 字符串方法
def string_methods():
    """常用字符串方法"""
    s = "  hello, python world  "
    
    print(f"原始: '{s}'")
    print(f"strip: '{s.strip()}'")
    print(f"lstrip: '{s.lstrip()}'")
    print(f"rstrip: '{s.rstrip()}'")
    
    # 分割和连接
    words = "apple,banana,orange".split(",")
    print(f"\n分割: {words}")
    print(f"连接: {' - '.join(words)}")
    
    # 查找和替换
    text = "I like Python"
    print(f"\n查找 'Python': {text.find('Python')}")
    print(f"替换: {text.replace('Python', 'Java')}")
    
    # 判断方法
    print(f"\n判断方法:")
    print(f"'123'.isdigit(): {'123'.isdigit()}")
    print(f"'abc'.isalpha(): {'abc'.isalpha()}")
    print(f"'abc123'.isalnum(): {'abc123'.isalnum()}")


if __name__ == "__main__":
    print("=" * 40)
    print("字符串示例")
    print("=" * 40)
    
    string_creation()
    print()
    string_operations()
    print()
    string_formatting()
    print()
    string_methods()