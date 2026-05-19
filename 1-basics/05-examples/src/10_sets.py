"""
章节：10 - 集合
文档：01-基础入门篇/数据结构/04-集合.md
"""

from typing import Any


def example_01_basic() -> set[str]:
    """示例1：集合最简用法"""
    fruits: set[str] = {"apple", "banana", "orange"}
    fruits.add("grape")
    if "apple" in fruits:
        print("有苹果")
    return fruits


def example_02_level1() -> set[int]:
    """示例2：层级1 - 去重"""
    numbers: list[int] = [1, 2, 2, 3, 3, 3, 4]
    unique: set[int] = set(numbers)
    print(unique)
    return unique


def example_03_level2() -> bool:
    """示例3：层级2 - 成员检测"""
    allowed_users: set[str] = {"admin", "manager", "editor"}
    user: str = "admin"
    has_access: bool = user in allowed_users
    print(f"{user} 有权限：{has_access}")
    return has_access


def example_04_level3() -> set[int]:
    """示例4：层级4 - 集合运算"""
    group_a: set[int] = {1, 2, 3, 4}
    group_b: set[int] = {3, 4, 5, 6}
    common: set[int] = group_a & group_b
    print(f"交集：{common}")
    return common


def example_05_level4() -> dict[str, set[str]]:
    """示例5：层级5 - 差集应用"""
    old_users: set[str] = {"user1", "user2", "user3"}
    new_users: set[str] = {"user2", "user3", "user4"}

    added: set[str] = new_users - old_users
    removed: set[str] = old_users - new_users

    print(f"新增：{added}")
    print(f"删除：{removed}")

    return {"added": added, "removed": removed}


def example_06_level5() -> list[int]:
    """示例6：层级6 - 数据清洗"""
    records: list[int] = [1, 2, 2, 3, 3, 4, 4, 5]
    seen: set[int] = set()
    result: list[int] = []

    for record in records:
        if record not in seen:
            seen.add(record)
            result.append(record)

    print(f"去重后：{result}")
    return result


def example_practical() -> dict[str, Any]:
    """综合应用：用户权限管理系统"""
    role_permissions: dict[str, set[str]] = {
        "admin": {"read", "write", "delete", "manage_users"},
        "editor": {"read", "write", "edit"},
        "viewer": {"read"},
    }

    user_roles: dict[str, set[str]] = {
        "张三": {"admin"},
        "李四": {"editor"},
        "王五": {"viewer"},
    }

    def get_user_permissions(user: str) -> set[str]:
        permissions: set[str] = set()
        for role in user_roles.get(user, set()):
            permissions |= role_permissions.get(role, set())
        return permissions

    user = "张三"
    permissions = get_user_permissions(user)
    print(f"{user} 的权限：{permissions}")

    return {"user": user, "permissions": permissions}


def main() -> None:
    """主函数：运行所有示例"""
    print("=" * 60)
    print("章节 10 - 集合")
    print("=" * 60)

    example_01_basic()
    example_02_level1()
    example_03_level2()
    example_04_level3()
    example_05_level4()
    example_06_level5()
    example_practical()

    print("=" * 60)
    print("✅ 所有示例运行完成")


if __name__ == "__main__":
    main()
