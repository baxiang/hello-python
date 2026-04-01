# 数据结构示例

"""
Python 数据结构示例
包含：列表、元组、字典、集合
"""

# 1. 列表
def list_examples():
    """列表操作"""
    fruits = ["苹果", "香蕉", "橙子"]
    
    print(f"原始列表: {fruits}")
    
    # 添加元素
    fruits.append("葡萄")
    print(f"append 后: {fruits}")
    
    fruits.insert(1, "西瓜")
    print(f"insert 后: {fruits}")
    
    # 删除元素
    fruits.remove("香蕉")
    print(f"remove 后: {fruits}")
    
    popped = fruits.pop()
    print(f"pop 后: {fruits}, 弹出: {popped}")
    
    # 切片
    numbers = list(range(10))
    print(f"\n数字列表: {numbers}")
    print(f"前5个: {numbers[:5]}")
    print(f"后5个: {numbers[-5:]}")
    print(f"偶数索引: {numbers[::2]}")


# 2. 元组
def tuple_examples():
    """元组操作"""
    point = (3, 4)
    print(f"点坐标: {point}")
    print(f"x = {point[0]}, y = {point[1]}")
    
    # 解包
    x, y = point
    print(f"解包: x={x}, y={y}")
    
    # 命名元组
    from collections import namedtuple
    Point = namedtuple("Point", ["x", "y"])
    p = Point(3, 4)
    print(f"命名元组: {p}, x={p.x}, y={p.y}")


# 3. 字典
def dict_examples():
    """字典操作"""
    person = {
        "name": "张三",
        "age": 25,
        "city": "北京"
    }
    
    print(f"字典: {person}")
    
    # 访问
    print(f"姓名: {person['name']}")
    print(f"年龄: {person.get('age')}")
    
    # 添加/修改
    person["email"] = "zhangsan@example.com"
    person["age"] = 26
    print(f"修改后: {person}")
    
    # 遍历
    print("\n遍历:")
    for key, value in person.items():
        print(f"  {key}: {value}")
    
    # 字典推导式
    squares = {x: x ** 2 for x in range(5)}
    print(f"\n平方字典: {squares}")


# 4. 集合
def set_examples():
    """集合操作"""
    a = {1, 2, 3, 4, 5}
    b = {4, 5, 6, 7, 8}
    
    print(f"集合 A: {a}")
    print(f"集合 B: {b}")
    
    print(f"\n集合运算:")
    print(f"并集: {a | b}")
    print(f"交集: {a & b}")
    print(f"差集 (A-B): {a - b}")
    print(f"对称差: {a ^ b}")
    
    # 去重
    numbers = [1, 2, 2, 3, 3, 3, 4]
    unique = list(set(numbers))
    print(f"\n去重: {numbers} -> {unique}")


if __name__ == "__main__":
    print("=" * 40)
    print("数据结构示例")
    print("=" * 40)
    
    print("\n【列表】")
    list_examples()
    
    print("\n【元组】")
    tuple_examples()
    
    print("\n【字典】")
    dict_examples()
    
    print("\n【集合】")
    set_examples()