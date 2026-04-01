# 基础语法示例

"""
Python 基础语法示例
包含：条件语句、循环、列表推导式
"""

# 1. 条件语句
def check_score(score):
    """根据分数判断等级"""
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"


# 2. 循环语句
def loop_examples():
    """循环示例"""
    print("for 循环:")
    for i in range(5):
        print(f"  第 {i + 1} 次循环")
    
    print("\nwhile 循环:")
    count = 0
    while count < 3:
        print(f"  count = {count}")
        count += 1
    
    print("\n遍历列表:")
    fruits = ["苹果", "香蕉", "橙子"]
    for fruit in fruits:
        print(f"  水果: {fruit}")


# 3. 列表推导式
def comprehension_examples():
    """推导式示例"""
    # 列表推导式
    squares = [x ** 2 for x in range(10)]
    print(f"平方数: {squares}")
    
    # 带条件的列表推导式
    even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
    print(f"偶数的平方: {even_squares}")
    
    # 字典推导式
    word_lengths = {word: len(word) for word in ["hello", "world", "python"]}
    print(f"单词长度: {word_lengths}")


# 4. match 语句 (Python 3.10+)
def match_example(status):
    """match 语句示例"""
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:
            return "Unknown"


if __name__ == "__main__":
    print("=" * 40)
    print("基础语法示例")
    print("=" * 40)
    
    # 条件语句
    print("\n条件语句:")
    for score in [95, 85, 65, 45]:
        print(f"  分数 {score}: {check_score(score)}")
    
    # 循环
    print()
    loop_examples()
    
    # 推导式
    print()
    comprehension_examples()
    
    # match
    print(f"\nmatch 示例: 状态码 200 -> {match_example(200)}")