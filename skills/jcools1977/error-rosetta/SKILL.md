---
name: error-rosetta
version: 1.0.0
description: 这是一个通用翻译工具，专门用于解读那些晦涩难懂的错误信息、堆栈跟踪（stack traces）以及日志输出。它能将你的工具链生成的“象形文字”（即那些难以理解的错误代码或日志内容）转化为通俗易懂的诊断结果、根本原因，以及具体的修复方案——这些信息会直接显示在你的代码库中，而不是来自2019年的某个通用问答平台（如Stack Overflow）的答案。
author: J. DeVere Cooley
category: everyday-tools
tags:
  - error-handling
  - debugging
  - translation
  - daily-driver
metadata:
  openclaw:
    emoji: "📜"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - everyday
      - debugging
---
# Error Rosetta

> “Rosetta Stone”通过提供三种语言的相同文本，帮助学者们解读埃及象形文字。而你的编译器本身就已经能够理解三种语言：错误代码、堆栈跟踪以及实际发生的问题。只是它拒绝使用第三种语言（即人类可读的错误信息）。

## 它的作用

当你遇到错误时，你会看到如下内容：

```
TypeError: Cannot read properties of undefined (reading 'map')
    at UserList (webpack-internal:///./src/components/UserList.tsx:14:23)
    at renderWithHooks (webpack-internal:///./node_modules/react-dom/cjs/react-dom.development.js:14985:18)
    at mountIndeterminateComponent (webpack-internal:///./node_modules/react-dom/cjs/react-dom.development.js:17811:13)
```

Error Rosetta 会为你提供如下详细的错误信息：

```
PLAIN ENGLISH: Your UserList component is trying to call .map() on
something that doesn't exist yet. On line 14, you're accessing a
property that is undefined — probably because the data hasn't loaded
from the API when the component first renders.

ROOT CAUSE: src/components/UserList.tsx:14 accesses `users.map()`
but `users` is undefined on first render. Your useEffect that fetches
users hasn't completed yet.

FIX: Add a guard before mapping:
  {users?.map(...)}  or  {users && users.map(...)}

  Better: Initialize your state with an empty array:
  const [users, setUsers] = useState([]);
```

## 错误信息的解析层次

### 第一层：错误识别

每条错误信息，无论多么晦涩难懂，都包含以下可解析的组成部分：

| 组件 | 它告诉你的信息 | 示例 |
|---|---|---|
| **错误类型** | 问题的类别 | `TypeError`, `ENOENT`, `HTTP 422`, `SegFault` |
| **错误消息** | 出现了什么问题（通常表述得很模糊） | “无法读取未定义对象的属性” |
| **位置** | 问题发生的具体位置 | 文件路径 + 行号 |
| **堆栈跟踪** | 问题是如何产生的 | 从入口点到错误点的调用链 |
| **错误代码** | 机器可识别的标识符 | `E0308`, `TS2345`, `EPERM` |

### 第二层：上下文增强

原始错误信息会被结合你的代码库上下文进行进一步解析：

```
ENRICHMENT PROCESS:
├── Read the file + line referenced in the error
├── Understand what the code is TRYING to do (not just what failed)
├── Check the data flow: where does the undefined/null/wrong-type value come from?
├── Check recent changes: did a recent commit introduce this?
├── Check patterns: does this error match a known pattern for this framework/language?
└── Check siblings: are similar errors happening elsewhere?
```

### 第三层：通俗化翻译

经过解析的错误信息会被翻译成三种易于理解的形式：

```
1. WHAT HAPPENED (one sentence, no jargon)
   "Your code tried to use a list of users before the list was loaded."

2. WHY IT HAPPENED (root cause, in your codebase)
   "useState(undefined) + useEffect(async fetch) = undefined on first render."

3. HOW TO FIX IT (specific to your code, not generic advice)
   "Line 8: Change useState() to useState([])"
```

## 错误模式库

### JavaScript/TypeScript

| 晦涩的错误信息 | 通俗化的翻译 | 常见的解决方法 |
|---|---|---|
| “无法读取未定义对象的属性（尝试访问 ‘x’）” | 你试图访问一个不存在的对象 | 使用可选链 `?.x` 或先检查 `null/undefined` |
| “‘x’ 不是一个函数” | 你尝试调用一个不可调用的对象（它是一个值，而不是函数） | 检查之前的调用是否缺少括号 `()`，或者导入是否正确 |
| “最大调用栈深度已超出” | 出现无限递归 | 找到缺少终止条件的递归调用 |
| “无法将值赋给 ‘x’，因为它是只读属性” | 你试图修改一个不应该被修改的属性 | 使用 `spread` 或 `Object.assign` 创建一个新的对象 |
| “模块未找到：无法解析 ‘x’” | 导入路径错误或模块未安装 | 检查拼写，查看 `node_modules` 文件夹，运行 `npm install` |
| “TS2345：类型为 ‘X’ 的参数无法赋值给类型为 ‘Y’ 的参数” | 类型不匹配 | 检查函数期望的数据类型与实际传递的数据类型 |

### Python

| 晦涩的错误信息 | 通俗化的翻译 | 常见的解决方法 |
| “AttributeError: ‘NoneType’ 对象没有属性 ‘x’” | 函数返回了 `None`，而你期望得到的是一个对象 | 检查函数的返回值 |
| “IndentationError：缩进错误” | 缩进格式不正确（使用制表符还是空格） | 修正缩进格式，保持一致 |
| “RecursionError：最大递归深度已超出” | 出现无限递归 | 找到缺少终止条件的递归调用 |
| “KeyError：‘x’” | 你尝试访问字典中不存在的键 | 使用 `.get('x', default)` 或先检查 `if 'x' in dict` |
| “ImportError：无法从 ‘y’ 模块中导入 ‘x’” | 你要导入的模块不存在 | 检查拼写，查看模块的 `__init__.py` 文件，确认版本 |

### Rust

| 晦涩的错误信息 | 通俗化的翻译 | 常见的解决方法 |
| “E0382：尝试借用已移动的值 ‘x’” | 你在将某个值的所有权转移给其他变量后还继续使用它 | 克隆该值，使用引用，或者重新设计代码结构以避免这种情况 |
| “E0308：类型不匹配” | 预期的是某种类型，但实际上得到的是另一种类型 | 检查函数签名和返回类型 |
| “E0502：无法将 ‘x’ 作为可变类型借用，因为它同时被标记为不可变类型” | 你试图修改一个不可变的引用 | 重新设计代码结构，避免同时持有两种引用 |
| “E0106：缺少生命周期注解” | Rust 无法确定引用的生命周期 | 添加明确的生命周期注解 |

### Go

| 晦涩的错误信息 | 通俗化的翻译 | 常见的解决方法 |
| “无法将类型 Y 的变量赋值给类型 Z” | 类型不匹配 | 检查赋值或函数调用中的类型 |
| “undefined：变量 ‘x’ 不存在” | 你尝试使用一个在这个作用域中不存在的变量 | 检查导入语句，拼写，确认变量作用域 |
| “fatal error：所有 goroutine 都处于等待状态——死锁！” | 所有的 goroutine 都在等待某个操作，导致程序无法继续执行 | 检查通道操作，确保数据能够正常传输 |

### 系统/操作系统错误

| 晦涩的错误信息 | 通俗化的翻译 | 常见的解决方法 |
| “ENOENT：文件或目录不存在” | 指定的路径上的文件或目录不存在 | 检查路径是否正确，是否拼写错误，或者路径是相对路径还是绝对路径 |
| “EACCES：没有访问权限” | 你没有权限访问该文件或目录 | 检查文件权限，确认是否需要使用 `sudo` 或管理员权限 |
| “EADDRINUSE：地址已被占用” | 另一个进程正在使用该端口 | 结束那个进程，或者更换端口 |
| “ENOMEM：内存不足” | 系统内存不足 | 检查是否存在内存泄漏，增加可用内存 |
| “ETIMEDOUT：连接超时” | 远端主机未及时响应 | 检查网络连接，确认服务是否正在运行，或者检查防火墙设置 |

### HTTP 错误

| 错误代码 | 服务器的实际含义 | 开发者应采取的措施 |
|---|---|---|
| `400 Bad Request` | “请求格式错误——我无法解析你的请求” | 检查请求体的格式、`Content-Type` 头部信息以及必填字段 |
| `401 Unauthorized` | “你是谁？我没有找到有效的身份验证信息” | 检查认证令牌的有效性，确认其是否过期，以及认证头部的格式 |
| `403 Forbidden` | “我知道你是谁，但你不被允许访问该资源” | 检查权限设置，确认资源是否需要不同的访问权限 |
| `404 Not Found` | “请求的 URL 对应的资源不存在” | 检查 URL 路径，确认资源是否存在，以及 API 的版本 |
| `409 Conflict` | “请求与当前系统状态冲突” | 检查是否存在重复的资源，或者版本/ETag 是否冲突 |
| `422 Unprocessable Entity` | “我能接收你的请求，但数据格式不正确” | 检查数据是否符合 API 的验证规则 |
| `429 Too Many Requests` | “请求次数过多” | 实现重试机制，检查请求频率限制 |
| `500 Internal Server Error` | “服务器内部出现错误，这不是你的问题” | 查看服务器日志，可能是后端程序的bug |
| `502 Bad Gateway` | “我是一个代理服务器，但后端的服务器出现了问题” | 检查上游服务，或者检查代理配置 |
| `503 Service Unavailable` | “服务器暂时不可用” | 重试请求，并查看状态页面 |

## 错误信息的解析过程

```
INPUT: Error message, stack trace, or log output (paste the whole thing)

Phase 1: PARSE
├── Identify error type, code, message, and location
├── Extract stack trace frames
├── Identify the framework/language/tool that produced the error
└── Separate signal from noise (framework internals vs. your code)

Phase 2: LOCATE
├── Find YOUR code in the stack trace (skip framework frames)
├── Read the file and line where the error originated
├── Read the surrounding context (function, class, module)
└── Trace the data flow to the error point

Phase 3: DIAGNOSE
├── Match against known error patterns for this language/framework
├── Analyze the specific code context (not generic advice)
├── Identify the root cause (not the symptom)
├── Check: is this a new bug or a recurring pattern?
└── Check: did a recent change introduce this?

Phase 4: PRESCRIBE
├── Plain English explanation (one sentence)
├── Root cause in your code (specific file, line, variable)
├── Exact fix (code change, not concept)
├── Prevention (how to avoid this class of error in the future)
└── Confidence level (how certain is this diagnosis)
```

## 输出格式

```
╔══════════════════════════════════════════════════════════════╗
║                    ERROR ROSETTA                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ERROR: TypeError: Cannot read properties of undefined       ║
║         (reading 'map')                                      ║
║                                                              ║
║  TRANSLATION:                                                ║
║  Your UserList component renders before the API response     ║
║  arrives. On the first render, `users` is undefined, and     ║
║  you're calling .map() on undefined.                         ║
║                                                              ║
║  ROOT CAUSE:                                                 ║
║  src/components/UserList.tsx:8                                ║
║    const [users, setUsers] = useState();  ← initialized as  ║
║    undefined, not as empty array                             ║
║                                                              ║
║  FIX:                                                        ║
║  Line 8: useState()  →  useState([])                         ║
║                                                              ║
║  PREVENTION:                                                 ║
║  Always initialize state with the correct empty type:        ║
║    Arrays: useState([])                                      ║
║    Objects: useState(null) with explicit null check           ║
║    Strings: useState('')                                     ║
║                                                              ║
║  CONFIDENCE: 95% (matches React uninitialized-state pattern) ║
╚══════════════════════════════════════════════════════════════╝
```

## 适用场景

- 每当你遇到无法立即理解的错误时。
- 在学习新的编程语言或框架时（新的错误信息格式可能让你感到困惑）。
- 当错误出现在依赖库的代码中，你需要弄清楚自己哪里做错了。
- 在调试持续集成（CI）失败时，尤其是面对大量日志输出时。
- 当用户报告错误时，你需要快速理解错误的具体含义。

## 它的重要性

开发者花费了 35-50% 的时间在调试问题上。其中大部分时间都用于**理解错误信息**，而不是直接修复错误本身。你越快地理解错误信息，就能越快地解决问题。

Error Rosetta 并不能直接修复错误，但它消除了从看到错误到理解错误之间的翻译环节。之后的所有操作都只需要简单的文本处理即可完成。

它完全不依赖于任何外部服务或 API 调用，仅通过模式匹配和代码分析来实现错误信息的解析。