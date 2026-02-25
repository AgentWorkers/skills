---
name: NumPy
slug: numpy
version: 1.0.0
homepage: https://clawic.com/skills/numpy
description: 使用数组、广播操作、向量化以及线性代数技术，编写运行速度快且内存使用效率高的数值计算代码。
metadata: {"clawdbot":{"emoji":"🔢","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以获取集成指南。该工具会在 `~/numpy/` 目录下创建用于存储用户偏好设置和代码片段的文件。

## 使用场景

当用户需要使用 Python 进行数值计算时，该工具可以通过代理（agent）来处理数组操作、数学运算、线性代数以及数据操作（这些操作均基于 NumPy 库实现）。

## 架构

所有与内存相关的操作都在 `~/numpy/` 目录下进行。具体内存管理机制请参考 `memory-template.md` 文件。

```
~/numpy/
├── memory.md      # Preferences + common patterns used
└── snippets/      # User's saved code patterns
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 设置流程 | `setup.md` |
| 内存管理模板 | `memory-template.md` |

## 核心规则

### 1. 首先使用向量化操作
**切勿** 使用 Python 的循环来进行数组操作。NumPy 的向量化操作速度通常快 10 到 100 倍。

```python
# BAD - Python loop
result = []
for x in arr:
    result.append(x * 2)

# GOOD - Vectorized
result = arr * 2
```

### 2. 理解广播（Broadcasting）机制
广播机制允许对不同形状的数组进行操作。请记住以下规则：
- 数组的维度需要从右侧对齐；
- 缺少的维度会被自动补全为长度为 1 的数组；
- 缺失的维度会被视为长度为 1 的数组。

```python
# Shape (3,1) + (4,) broadcasts to (3,4)
a = np.array([[1], [2], [3]])  # (3,1)
b = np.array([10, 20, 30, 40])  # (4,)
result = a + b  # (3,4)
```

### 3. 尽量使用视图（Views）而非副本（Copies）
切片操作返回的是数组的视图（即对原始数组的引用），仅在确实需要复制数据时才使用 `.copy()` 方法。

```python
# View - modifying b changes a
b = a[::2]

# Copy - independent
b = a[::2].copy()
```

### 4. 选择合适的数据类型
根据数据的特点选择最小化内存占用的数据类型。这既能节省内存，又能提高计算速度。

```python
# For integers 0-255
arr = np.array(data, dtype=np.uint8)

# For floats that don't need double precision
arr = np.array(data, dtype=np.float32)
```

### 5. 明确轴的用途
大多数 NumPy 函数都接受 `axis` 参数。请了解各轴的含义：
- `axis=0`：沿行方向操作（即沿着列方向）；
- `axis=1`：沿列方向操作（即穿过行方向）；
- `axis=None` 或省略该参数时：对扁平化的数组进行操作。

```python
arr = np.array([[1, 2], [3, 4]])
np.sum(arr, axis=0)  # [4, 6] - sum each column
np.sum(arr, axis=1)  # [3, 7] - sum each row
```

### 6. 利用内置函数
NumPy 提供了许多针对常见操作的优化函数，无需重复编写代码。

| 需要执行的操作 | 使用的函数 |
|------------------|----------------------|
| 元素级数学运算 | `np.sin`, `np.exp`, `np.log` |
| 统计分析 | `np.mean`, `np.std`, `np.median` |
| 线性代数 | `np.dot`, `np.linalg.*` |
| 排序 | `np.sort`, `np.argsort` |
| 查找元素 | `np.where`, `np.searchsorted` |

## 常见使用误区

### 数组形状不匹配的问题
**注意**：不正确的数组形状可能导致程序运行错误。

### 静态类型转换（Silent Type Coercion）
某些情况下，NumPy 会自动进行类型转换，但这可能会隐藏潜在的问题。

### 视图（Views）与副本（Copies）的混淆
请区分两者，避免不必要的数据复制。

### 广播操作带来的意外结果
了解广播机制，避免因操作不当导致的结果异常。

### 在原数组上进行操作（In-Place Operations）
某些操作会在原数组上进行，这可能会影响数据的可读性和后续操作。

## 常用编程模式

### 创建数组
了解如何使用 NumPy 创建不同类型的数组。

### 重塑数组和堆叠数组
掌握如何调整数组的形状以及如何将多个数组堆叠在一起。

### 使用布尔索引
学习如何使用布尔索引来筛选数组中的元素。

### 线性代数操作
熟悉 NumPy 提供的各种线性代数函数。

## 安全性与隐私保护

**数据安全性**：
- 所有计算都在本地完成；
- 所有代码模式都保存在 `~/numpy/` 目录下。

**该工具不执行以下操作：**
- 不会向外部发送数据；
- 不会访问 `~/numpy/` 目录之外的文件；
- 不需要网络连接。

## 相关技能
如果用户需要，可以使用以下命令安装相关工具：
- `clawhub install data`：数据处理工作流；
- `clawhub install math`：数学计算相关工具；
- `clawhub install statistics`：统计分析相关工具。

## 反馈建议
- 如果本文档对您有帮助，请使用 `clawhub star numpy` 给予评分；
- 如需保持信息更新，请使用 `clawhub sync` 命令。