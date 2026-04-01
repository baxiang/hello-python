# Python 入门示例

"""
Python 入门示例代码
包含：变量、数据类型、运算符、输入输出
"""

# 1. 变量与数据类型
name = "Python"          # 字符串
version = 3.11           # 浮点数
year = 2024              # 整数
is_popular = True        # 布尔值

print(f"语言: {name}")
print(f"版本: {version}")
print(f"年份: {year}")
print(f"流行: {is_popular}")


# 2. 运算符
a, b = 10, 3

print(f"\n运算符示例:")
print(f"{a} + {b} = {a + b}")   # 加法
print(f"{a} - {b} = {a - b}")   # 减法
print(f"{a} * {b} = {a * b}")   # 乘法
print(f"{a} / {b} = {a / b}")   # 除法
print(f"{a} // {b} = {a // b}") # 整除
print(f"{a} % {b} = {a % b}")   # 取余
print(f"{a} ** {b} = {a ** b}") # 幂运算


# 3. 输入输出
def greet():
    """简单的问候程序"""
    user_name = input("请输入你的名字: ")
    print(f"你好, {user_name}! 欢迎学习 Python!")


# 4. 类型转换
def type_conversion():
    """类型转换示例"""
    # 字符串转数字
    num_str = "123"
    num_int = int(num_str)
    num_float = float(num_str)
    
    print(f"字符串: {num_str} (类型: {type(num_str).__name__})")
    print(f"整数: {num_int} (类型: {type(num_int).__name__})")
    print(f"浮点数: {num_float} (类型: {type(num_float).__name__})")


if __name__ == "__main__":
    print("=" * 40)
    print("Python 入门示例")
    print("=" * 40)
    
    type_conversion()
    print()
    # greet()  # 取消注释以运行交互式示例