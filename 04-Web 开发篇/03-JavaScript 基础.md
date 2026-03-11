# 第 3 章：JavaScript 基础

掌握 JavaScript 语法、DOM 操作和事件处理。

---

## 本章目标

- 掌握 JavaScript 基础语法
- 理解 DOM 和 BOM
- 学会 DOM 操作
- 掌握事件处理
- 了解 ES6+ 新特性

---

## 3.1 JavaScript 基础

### 变量和数据类型

```javascript
// 变量声明
let name = "张三";      // 可变变量
const age = 25;        // 常量
var oldVar = "旧方式";  // 不推荐使用

// 数据类型
// 原始类型
let str = "字符串";           // string
let num = 123;               // number
let bool = true;             // boolean
let empty = null;            // null
let notDefined;              // undefined
let sym = Symbol("id");     // symbol
let big = 100n;              // bigint

// 引用类型
let arr = [1, 2, 3];         // 数组
let obj = { name: "张三" }; // 对象
let func = function() {};    // 函数
```

### 运算符

```javascript
// 算术运算符
let sum = 10 + 5;    // 加法
let diff = 10 - 5;   // 减法
let product = 10 * 5;// 乘法
let quotient = 10 / 5; // 除法
let remainder = 10 % 3; // 取余
let power = 2 ** 3;   // 幂运算

// 比较运算符
console.log(5 == "5");   // true (宽松相等)
console.log(5 === "5");   // false (严格相等)
console.log(5 != "5");   // false
console.log(5 !== "5");  // true

// 逻辑运算符
console.log(true && false); // false
console.log(true || false); // true
console.log(!true);         // false

// 空值合并运算符
let value = null ?? "默认值"; // "默认值"

// 可选链
let user = { profile: { name: "张三" } };
let name = user?.profile?.name; // "张三"
```

### 字符串

```javascript
let str = "Hello World";

// 模板字符串
let name = "张三";
let age = 25;
let message = `我叫${name}，今年${age}岁`;

// 字符串方法
console.log(str.length);           // 长度
console.log(str.toUpperCase());    // 转大写
console.log(str.toLowerCase());    // 转小写
console.log(str.includes("World")); // 包含
console.log(str.startsWith("Hello")); // 开头
console.log(str.endsWith("!"));    // 结尾
console.log(str.indexOf("World")); // 查找位置
console.log(str.slice(0, 5));      // 切片
console.log(str.split(" "));       // 分割
console.log(str.replace("World", "JavaScript")); // 替换
console.log(str.repeat(2));        // 重复
```

### 数组

```javascript
let arr = [1, 2, 3, 4, 5];

// 遍历
arr.forEach((item, index) => {
    console.log(index, item);
});

// map - 映射
let doubled = arr.map(x => x * 2);

// filter - 过滤
let evens = arr.filter(x => x % 2 === 0);

// reduce - 聚合
let sum = arr.reduce((acc, cur) => acc + cur, 0);

// find - 查找
let found = arr.find(x => x > 3);

// some - 是否存在
let hasEven = arr.some(x => x % 2 === 0);

// every - 全部满足
let allPositive = arr.every(x => x > 0);

// 排序
let sorted = [...arr].sort((a, b) => b - a);

// 操作
arr.push(6);        // 末尾添加
arr.pop();          // 末尾删除
arr.unshift(0);     // 开头添加
arr.shift();        // 开头删除
arr.splice(2, 1);   // 删除/替换
let sliced = arr.slice(1, 3); // 切片
let merged = arr.concat([6, 7]); // 合并
```

### 对象

```javascript
let user = {
    name: "张三",
    age: 25,
    email: "zhangsan@example.com",
    
    // 方法
    greet() {
        return `你好，我是${this.name}`;
    },
    
    // 计算属性
    get info() {
        return `${this.name} - ${this.age}岁`;
    }
};

// 解构赋值
const { name, age } = user;

// 扩展运算符
let clone = { ...user };
let merged = { ...user, address: "北京" };

// Object 方法
console.log(Object.keys(user));   // ["name", "age", "email"]
console.log(Object.values(user)); // ["张三", 25, "..."]
console.log(Object.entries(user)); // [["name", "张三"], ...]
```

---

## 3.2 函数

### 函数声明

```javascript
// 函数声明
function greet(name) {
    return `你好，${name}！`;
}

// 函数表达式
const greet = function(name) {
    return `你好，${name}！`;
};

// 箭头函数
const greet = (name) => `你好，${name}！`;

// 箭头函数（多行）
const greet = (name) => {
    const message = `你好，${name}！`;
    return message;
};

// 默认参数
function greet(name = "朋友") {
    return `你好，${name}！`;
}

// 剩余参数
function sum(...numbers) {
    return numbers.reduce((a, b) => a + b, 0);
}
```

### 高阶函数

```javascript
// 函数作为参数
function execute(fn, value) {
    return fn(value);
}

execute(x => x * 2, 5); // 10

// 函数作为返回值
function multiplier(factor) {
    return function(x) {
        return x * factor;
    };
}

const double = multiplier(2);
double(5); // 10
```

---

## 3.3 流程控制

### 条件语句

```javascript
// if-else
if (age >= 18) {
    console.log("成年人");
} else if (age >= 12) {
    console.log("青少年");
} else {
    console.log("儿童");
}

// 三元运算符
let status = age >= 18 ? "成年" : "未成年";

// switch
switch (day) {
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
        console.log("工作日");
        break;
    case 6:
    case 7:
        console.log("周末");
        break;
    default:
        console.log("无效日期");
}
```

### 循环

```javascript
// for 循环
for (let i = 0; i < 5; i++) {
    console.log(i);
}

// for...of (数组)
for (const item of arr) {
    console.log(item);
}

// for...in (对象)
for (const key in obj) {
    console.log(key, obj[key]);
}

// while 循环
let i = 0;
while (i < 5) {
    console.log(i);
    i++;
}

// do...while
do {
    console.log(i);
} while (i < 5);
```

---

## 3.4 DOM 操作

### 选择元素

```javascript
// 选择单个元素
const element = document.getElementById("myId");
const element = document.querySelector(".myClass");
const element = document.querySelector("div.container > p");

// 选择多个元素
const elements = document.getElementsByClassName("myClass");
const elements = document.getElementsByTagName("div");
const elements = document.querySelectorAll(".myClass");
```

### 修改元素

```javascript
// 修改内容
element.textContent = "新文本";
element.innerHTML = "<strong>HTML 内容</strong>";

// 修改样式
element.style.color = "red";
element.style.backgroundColor = "#f0f0f0";
element.classList.add("active");
element.classList.remove("hidden");
element.classList.toggle("selected");

// 修改属性
element.setAttribute("data-id", "123");
element.getAttribute("data-id");
element.removeAttribute("disabled");
```

### 创建和删除元素

```javascript
// 创建元素
const newDiv = document.createElement("div");
newDiv.textContent = "新元素";
newDiv.className = "container";

// 添加到 DOM
parent.appendChild(newDiv);
parent.insertBefore(newDiv, existingChild);
parent.insertAdjacentHTML("beforeend", "<p>新段落</p>");

// 删除元素
element.remove();
parent.removeChild(child);
```

### 实战：动态生成列表

```javascript
const data = [
    { id: 1, name: "苹果", price: 5 },
    { id: 2, name: "香蕉", price: 3 },
    { id: 3, name: "橙子", price: 4 }
];

const list = document.getElementById("list");

data.forEach(item => {
    const li = document.createElement("li");
    li.innerHTML = `
        <span class="name">${item.name}</span>
        <span class="price">¥${item.price}</span>
    `;
    list.appendChild(li);
});
```

---

## 3.5 事件处理

### 事件绑定

```javascript
// 直接绑定
button.addEventListener("click", function(event) {
    console.log("点击了");
});

// 箭头函数
button.addEventListener("click", (event) => {
    console.log(event.target);
});

// 事件委托
ul.addEventListener("click", (event) => {
    if (event.target.tagName === "LI") {
        console.log(event.target.textContent);
    }
});
```

### 常见事件

```javascript
// 鼠标事件
element.addEventListener("click", handler);
element.addEventListener("dblclick", handler);
element.addEventListener("mouseenter", handler);
element.addEventListener("mouseleave", handler);
element.addEventListener("mousemove", handler);

// 键盘事件
document.addEventListener("keydown", handler);
document.addEventListener("keyup", handler);

// 表单事件
form.addEventListener("submit", handler);
input.addEventListener("change", handler);
input.addEventListener("input", handler);

// 页面事件
window.addEventListener("load", handler);
window.addEventListener("resize", handler);
window.addEventListener("scroll", handler);
```

### 表单验证示例

```javascript
const form = document.getElementById("myForm");
const emailInput = document.getElementById("email");
const errorSpan = document.getElementById("error");

emailInput.addEventListener("input", () => {
    const email = emailInput.value;
    const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    
    if (!isValid) {
        errorSpan.textContent = "请输入有效的邮箱地址";
        emailInput.classList.add("error");
    } else {
        errorSpan.textContent = "";
        emailInput.classList.remove("error");
    }
});

form.addEventListener("submit", (e) => {
    e.preventDefault();
    
    // 验证所有字段
    const isValid = form.checkValidity();
    
    if (isValid) {
        console.log("表单提交成功");
        // 提交表单
    } else {
        console.log("表单验证失败");
    }
});
```

---

## 3.6 ES6+ 新特性

### let 和 const

```javascript
// let - 块级作用域
if (true) {
    let x = 10;
}
// console.log(x); // ReferenceError

// const - 常量
const PI = 3.14159;
// PI = 3; // TypeError
```

### 模板字符串

```javascript
const name = "张三";
const age = 25;
const message = `我叫${name}，今年${age}岁`;
```

### 解构赋值

```javascript
// 数组解构
const [a, b, c] = [1, 2, 3];

// 对象解构
const { name, age } = { name: "张三", age: 25 };

// 函数参数解构
function greet({ name, age }) {
    return `你好，我叫${name}，${age}岁`;
}
```

### 扩展运算符

```javascript
// 数组
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5];

// 对象
const obj1 = { a: 1, b: 2 };
const obj2 = { ...obj1, c: 3 };
```

### async/await

```javascript
// Promise
fetch("/api/data")
    .then(res => res.json())
    .then(data => console.log(data))
    .catch(err => console.error(err));

// async/await
async function fetchData() {
    try {
        const res = await fetch("/api/data");
        const data = await res.json();
        console.log(data);
    } catch (err) {
        console.error(err);
    }
}
```

### Promise

```javascript
const promise = new Promise((resolve, reject) => {
    setTimeout(() => {
        const success = true;
        if (success) {
            resolve("操作成功");
        } else {
            reject("操作失败");
        }
    }, 1000);
});

promise
    .then(result => console.log(result))
    .catch(error => console.error(error));
```

---

## 3.7 实战：待办事项应用

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>待办事项</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
        }
        
        h1 { text-align: center; margin-bottom: 20px; }
        
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        
        button {
            padding: 10px 20px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        
        button:hover { background: #0056b3; }
        
        ul { list-style: none; }
        
        li {
            display: flex;
            align-items: center;
            padding: 12px;
            border-bottom: 1px solid #eee;
        }
        
        li.completed span {
            text-decoration: line-through;
            color: #999;
        }
        
        li input[type="checkbox"] {
            margin-right: 10px;
        }
        
        li .delete-btn {
            margin-left: auto;
            background: #dc3545;
            padding: 5px 10px;
            font-size: 12px;
        }
        
        .stats {
            margin-top: 20px;
            text-align: center;
            color: #666;
        }
    </style>
</head>
<body>
    <h1>待办事项</h1>
    
    <div class="input-group">
        <input type="text" id="todoInput" placeholder="添加新任务...">
        <button id="addBtn">添加</button>
    </div>
    
    <ul id="todoList"></ul>
    
    <div class="stats">
        共 <span id="totalCount">0</span> 项， 
        完成 <span id="completedCount">0</span> 项
    </div>

    <script>
        // 获取元素
        const input = document.getElementById("todoInput");
        const addBtn = document.getElementById("addBtn");
        const todoList = document.getElementById("todoList");
        const totalCount = document.getElementById("totalCount");
        const completedCount = document.getElementById("completedCount");

        // 存储任务
        let todos = JSON.parse(localStorage.getItem("todos")) || [];

        // 渲染任务列表
        function render() {
            todoList.innerHTML = "";
            
            todos.forEach((todo, index) => {
                const li = document.createElement("li");
                if (todo.completed) {
                    li.classList.add("completed");
                }
                
                li.innerHTML = `
                    <input type="checkbox" ${todo.completed ? "checked" : ""}>
                    <span>${todo.text}</span>
                    <button class="delete-btn">删除</button>
                `;
                
                // 绑定事件
                const checkbox = li.querySelector("input");
                checkbox.addEventListener("change", () => toggleComplete(index));
                
                const deleteBtn = li.querySelector(".delete-btn");
                deleteBtn.addEventListener("click", () => deleteTodo(index));
                
                todoList.appendChild(li);
            });
            
            // 更新统计
            totalCount.textContent = todos.length;
            completedCount.textContent = todos.filter(t => t.completed).length;
            
            // 保存到本地存储
            localStorage.setItem("todos", JSON.stringify(todos));
        }

        // 添加任务
        function addTodo() {
            const text = input.value.trim();
            if (!text) return;
            
            todos.push({ text, completed: false });
            input.value = "";
            render();
        }

        // 切换完成状态
        function toggleComplete(index) {
            todos[index].completed = !todos[index].completed;
            render();
        }

        // 删除任务
        function deleteTodo(index) {
            todos.splice(index, 1);
            render();
        }

        // 绑定事件
        addBtn.addEventListener("click", addTodo);
        
        input.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                addTodo();
            }
        });

        // 初始渲染
        render();
    </script>
</body>
</html>
```

---

## 本章总结

### 学到的技能

| 技能 | 说明 |
|------|------|
| 变量和数据类型 | let/const、基本类型 |
| 字符串和数组 | 常用方法 |
| 函数 | 声明、箭头函数、高阶函数 |
| DOM 操作 | 选择、修改、创建元素 |
| 事件处理 | 事件绑定、事件委托 |
| ES6+ | 解构、扩展运算符、async/await |

### 下一步

在 [第 4 章](./04-Flask 入门.md) 中，我们将学习 Flask 框架入门。

---

[← 上一章](./02-HTML 与 CSS.md) | [下一章 →](./04-Flask 入门.md)