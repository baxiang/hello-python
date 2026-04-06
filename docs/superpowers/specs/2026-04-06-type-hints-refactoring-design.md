# 类型提示子目录重构设计

**日期：** 2026-04-06
**状态：** 已批准

---

## 目标

改进 02-核心编程篇/类型提示 子目录：
1. 应用渐进式教学方法，改进现有文档结构
2. 精简与 01-基础入门篇 重复的内容
3. 扩展高级类型提示主题（ParamSpec、TypeGuard 进阶、Final/ClassVar、Python 3.12+ 特性）
4. 完善示例项目，覆盖所有文档主题

---

## 整体架构

```
02-核心编程篇/类型提示/
├── README.md                    # 章节概览和导航
├── 01-类型提示基础.md           # 精简后约 350 行
├── 02-类型进阶应用.md           # 新组织约 400 行  
├── 03-高级类型特性.md           # 新增约 300 行
└── type_hints_demo/             # 示例项目
    ├── README.md                # 使用文档
    ├── pyproject.toml           # 项目配置（Python 3.11+）
    ├── app/
    │   ├── core/
    │   │   ├── basics.py        # 基础类型示例
    │   │   ├── generics.py      # 泛型示例
    │   │   ├── protocols.py     # 协议示例
    │   │   └── advanced.py      # 高级特性示例
    │   └── utils/
    │       └── helpers.py       # 辅助函数
    └── tests/
        ├── test_basics.py
        ├── test_generics.py
        ├── test_protocols.py
        └── test_advanced.py
```

---

## 文档内容设计

### 01-类型提示基础.md（约 350 行）

**与入门篇衔接：**
- 入门篇已覆盖：基本类型、简单函数注解、类型提示作用
- 本篇重点：容器类型详解、Optional/Union 实用场景、Callable 应用

**章节结构（6 步渐进式）：**

```
第 1 章：容器类型深入理解
├── 1.1 问题引入：为什么需要指定容器元素类型？
├── 1.2 概念解释：泛型容器的类型参数
├── 1.3 最简示例：list[int] vs list
├── 1.4 详细说明：list/dict/tuple/set 的类型注解
├── 1.5 渐进复杂：嵌套容器、混合类型
└── 1.6 实际应用：统计单词频率、处理配置

第 2 章：可选值与联合类型
├── 2.1 问题引入：函数可能返回 None 怎么标注？
├── 2.2 概念解释：Optional 和 Union 的含义
├── 2.3 最简示例：str | None 语法
├── 2.4 详细说明：新旧语法对比、使用场景
├── 2.5 渐进复杂：多重联合、类型收窄
└── 2.6 实际应用：查找用户、解析输入

第 3 章：函数类型 Callable
├── 3.1 问题引入：如何标注回调函数？
├── 3.2 概念解释：Callable 的参数和返回类型
├── 3.3 最简示例：Callable[[int], str]
├── 3.4 详细说明：各种 Callable 形式
├── 3.5 渐进复杂：无参数、可变参数
└── 3.6 实际应用：策略模式、事件处理

第 4 章：类型别名
├── 4.1 问题引入：复杂类型写起来太长？
├── 4.2 概念解释：类型别名的作用
├── 4.3 最简示例：UserId = int
├── 4.4 详细说明：简单别名、复杂别名
├── 4.5 渐进复杂：NewType 的区别
└── 4.6 实际应用：业务类型定义
```

**精简策略：**
- 删除与入门篇重复的"为什么要用类型提示"部分
- 保留但精简基础类型注解（作为快速回顾）
- 重点放在容器类型的详细解释和实际应用

---

### 02-类型进阶应用.md（约 400 行）

**章节结构（6 步渐进式）：**

```
第 1 章：泛型深入理解
├── 1.1 问题引入：如何写一个可以处理任意类型的栈？
├── 1.2 概念解释：TypeVar 和 Generic 的作用
├── 1.3 最简示例：泛型函数 first()
├── 1.4 详细说明：泛型类、泛型约束
├── 1.5 渐进复杂：多类型变量、bounded TypeVar
└── 1.6 实际应用：Stack、Repository 实现

第 2 章：协议 Protocol
├── 2.1 问题引入：如何定义"有某种方法"的类型？
├── 2.2 概念解释：结构化类型 vs 声明式类型
├── 2.3 最简示例：Drawable 协议
├── 2.4 详细说明：协议定义、协议继承
├── 2.5 渐进复杂：runtime_checkable、协议组合
└── 2.6 实际应用：Comparable、Serializable

第 3 章：TypedDict 字典类型
├── 3.1 问题引入：字典的字段类型如何标注？
├── 3.2 概念解释：TypedDict 的作用
├── 3.3 最简示例：UserDict 定义
├── 3.4 详细说明：必需字段、可选字段
├── 3.5 渐进复杂：继承、ReadOnly
└── 3.6 实际应用：API 响应类型、配置类型

第 4 章：运行时类型检查
├── 4.1 问题引入：类型提示能运行时检查吗？
├── 4.2 概念解释：get_type_hints、get_origin、get_args
├── 4.3 最简示例：获取函数类型提示
├── 4.4 详细说明：手动实现验证装饰器
├── 4.5 渐进复杂：TypeChecker 工具类
└── 4.6 实际应用：数据验证、API 参数检查

第 5 章：类型守卫
├── 5.1 问题引入：如何让类型检查器理解类型收窄？
├── 5.2 概念解释：TypeGuard 的作用
├── 5.3 最简示例：is_string_list 函数
├── 5.4 详细说明：TypeGuard vs isinstance
├── 5.5 渐进复杂：自定义类型守卫函数
└── 5.6 实际应用：数据处理管道
```

---

### 03-高级类型特性.md（约 300 行）

**章节结构（6 步渐进式）：**

```
第 1 章：参数规格类型
├── 1.1 问题引入：如何捕获装饰器的参数类型？
├── 1.2 概念解释：ParamSpec 和 Concatenate
├── 1.3 最简示例：ParamSpec['P'] 语法
├── 1.4 详细说明：ParamSpec、Concatenate 用法
├── 1.5 渐进复杂：泛型装饰器实现
└── 1.6 实际应用：类型安全的装饰器工厂

第 2 章：类相关类型
├── 2.1 问题引入：如何标记"不可修改"的属性？
├── 2.2 概念解释：Final、ClassVar 的作用
├── 2.3 最简示例：Final 变量定义
├── 2.4 详细说明：Final 方法、Final 类、ClassVar
├── 2.5 渐进复杂：@final 装饰器
└── 2.6 实际应用：不可变配置、类常量

第 3 章：类型守卫进阶
├── 3.1 问题引入：TypeGuard 与 TypeIs 有何区别？
├── 3.2 概念解释：TypeIs（Python 3.13+）的作用
├── 3.3 最简示例：TypeIs vs TypeGuard 对比
├── 3.4 详细说明：类型收窄行为差异
├── 3.5 渐进复杂：复杂类型的守卫
└── 3.6 实际应用：数据清洗管道

第 4 章：Python 3.12+ 新特性
├── 4.1 问题引入：类型语法有哪些新改进？
├── 4.2 概念解释：typing 的新特性
├── 4.3 最简示例：type 语句定义别名
├── 4.4 详细说明：TypeAlias、Unpack、dataclass_transform
├── 4.5 渐进复杂：泛型语法改进
└── 4.6 实际应用：现代类型定义风格
```

---

## 示例项目设计

### 目录结构

```
type_hints_demo/
├── README.md                    # 详细使用文档
├── pyproject.toml               # 更新 Python 版本要求 3.11+
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── basics.py            # 容器类型、Optional/Union、Callable 示例
│   │   ├── generics.py          # 泛型 Stack、Repository、TypeVar 示例
│   │   ├── protocols.py         # Protocol、TypedDict 示例
│   │   └── advanced.py          # ParamSpec、Final、TypeGuard 示例
│   └── utils/
│       ├── __init__.py
│       └── helpers.py           # 辅助函数（保留现有内容）
└── tests/
    ├── __init__.py
    ├── test_basics.py           # basics.py 测试
    ├── test_generics.py         # generics.py 测试
    ├── test_protocols.py        # protocols.py 测试
    └── test_advanced.py         # advanced.py 测试
```

### 各模块内容

**basics.py（约 80 行）：**
- 容器类型示例：list[int]、dict[str, int]、tuple[int, str]
- Optional/Union 示例：find_user、parse_value
- Callable 示例：apply_operation、callback_pattern

**generics.py（约 120 行）：**
- 泛型函数：first、reverse、get_middle
- 泛型类：Stack[T]、Repository[T]
- 泛型约束：Number TypeVar

**protocols.py（约 100 行）：**
- 基础协议：Drawable、Comparable
- TypedDict 示例：UserDict、ConfigDict
- 协议继承：Shape 组合协议

**advanced.py（约 150 行）：**
- ParamSpec 示例：类型安全装饰器
- Final/ClassVar 示例：不可变配置类
- TypeGuard 示例：is_string_list、is_positive_dict

### README.md 内容大纲

```markdown
# 类型提示示例项目

## 项目结构
- app/core/basics.py - 基础类型示例
- app/core/generics.py - 泛型示例
- app/core/protocols.py - 协议示例
- app/core/advanced.py - 高级特性示例

## 运行测试
cd type_hints_demo
uv run pytest -v

## 类型检查（可选）
uv run mypy app/

## 学习建议
1. 先阅读对应章节文档
2. 查看示例代码理解语法
3. 运行测试验证行为
4. 修改代码尝试变体
```

---

## 文件变更清单

### 创建

| 文件 | 说明 |
|------|------|
| `02-类型进阶应用.md` | 重命名现有 02-类型注解进阶.md，应用渐进式教学 |
| `03-高级类型特性.md` | 新建，包含 ParamSpec、Final/ClassVar、Python 3.12+ 特性 |
| `app/core/basics.py` | 拆分现有 type_hints.py，容器类型、Optional/Union、Callable 示例 |
| `app/core/generics.py` | 新建，泛型 Stack、Repository 示例 |
| `app/core/protocols.py` | 新建，Protocol、TypedDict 示例 |
| `app/core/advanced.py` | 新建，ParamSpec、Final、TypeGuard 示例 |
| `tests/test_basics.py` | 拆分现有 test_type_hints.py |
| `tests/test_generics.py` | 新建 |
| `tests/test_protocols.py` | 新建 |
| `tests/test_advanced.py` | 新建 |

### 修改

| 文件 | 修改内容 |
|------|---------|
| `01-类型提示基础.md` | 精简重复内容，应用渐进式教学 |
| `README.md` | 更新章节导航 |
| `type_hints_demo/README.md` | 添加详细使用文档 |
| `type_hints_demo/pyproject.toml` | 更新 Python 版本要求为 3.11+ |

### 删除

| 文件 | 说明 |
|------|------|
| `type_hints_demo/app/core/type_hints.py` | 拆分后删除 |
| `type_hints_demo/tests/test_type_hints.py` | 拆分后删除 |

---

## 技术要求

- **Python 版本：** 3.11+（使用内置泛型、联合操作符）
- **代码风格：** 遵循 AGENTS.md 规范，snake_case 命名
- **类型注解：** 所有函数使用完整类型提示
- **文档语言：** 简体中文
- **测试框架：** pytest

---

## 验收标准

1. 所有文档应用 6 步渐进式教学结构
2. 文档内容与入门篇衔接，无明显重复
3. 示例项目覆盖所有文档主题
4. 所有测试通过：`uv run pytest -v`
5. 类型检查无错误：`uv run mypy app/`