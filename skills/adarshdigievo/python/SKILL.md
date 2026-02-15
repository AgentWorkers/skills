---
name: python
description: Python编码指南与最佳实践：适用于编写、审查或重构Python代码时。遵循PEP 8编码规范，通过`py_compile`进行语法验证，执行单元测试，仅使用现代版本的Python（避免使用已过时的版本），在可能的情况下使用`uv`进行依赖管理，并采用符合Python语言习惯的编程模式。
---

# Python 编码规范

## 代码风格（PEP 8）

- 使用 4 个空格进行缩进（严禁使用制表符）
- 每行最大长度为 88 个字符（Black 默认设置）或 79 个字符（严格的 PEP 8 要求）
- 在顶级定义之前使用两行空行；在类内部使用一行空行
- 导入语句的顺序：先导入标准库（stdlib），再导入第三方库，最后导入本地库；同一类别的导入语句需按字母顺序排列
- 函数/变量使用蛇形命名法（snake_case），类使用帕斯卡命名法（PascalCase），常量使用大写命名法（UPPER_CASE）

## 提交代码之前

```bash
# Syntax check (always)
python -m py_compile *.py

# Run tests if present
python -m pytest tests/ -v 2>/dev/null || python -m unittest discover -v 2>/dev/null || echo "No tests found"

# Format check (if available)
ruff check . --fix 2>/dev/null || python -m black --check . 2>/dev/null
```

## Python 版本要求

- **最低要求：** Python 3.10 及以上版本（Python 3.9 的支持将于 2025 年 10 月结束）
- **新项目推荐使用：** Python 3.11–3.13 版本
- **严禁使用：** Python 2 的语法或模式
- **建议使用现代特性：** 匹配语句（match statements）、海象运算符（walrus operator）、类型提示（type hints）

## 依赖管理

优先使用 uv（uv 是一个特定的依赖管理工具），如果 uv 不可用则使用 pip：
```bash
# Prefer uv if available
if command -v uv &>/dev/null; then
    uv pip install <package>
    uv pip compile requirements.in -o requirements.txt
else
    pip install <package>
fi
```

对于使用 uv 的新项目：
```bash
uv init
uv venv && source .venv/bin/activate
```

## Pythonic 编程模式

```python
# ✅ List/dict comprehensions over loops
squares = [x**2 for x in range(10)]
lookup = {item.id: item for item in items}

# ✅ Context managers for resources
with open("file.txt") as f:
    data = f.read()

# ✅ Unpacking
first, *rest = items
a, b = b, a  # swap

# ✅ EAFP over LBYL
try:
    value = d[key]
except KeyError:
    value = default

# ✅ f-strings for formatting
msg = f"Hello {name}, you have {count} items"

# ✅ Type hints
def process(items: list[str]) -> dict[str, int]:
    ...

# ✅ dataclasses/attrs for data containers
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    active: bool = True

# ✅ pathlib over os.path
from pathlib import Path
config = Path.home() / ".config" / "app.json"

# ✅ enumerate, zip, itertools
for i, item in enumerate(items):
    ...
for a, b in zip(list1, list2, strict=True):
    ...
```

## 应避免的编程反模式

```python
# ❌ Mutable default arguments
def bad(items=[]):  # Bug: shared across calls
    ...
def good(items=None):
    items = items or []

# ❌ Bare except
try:
    ...
except:  # Catches SystemExit, KeyboardInterrupt
    ...
except Exception:  # Better
    ...

# ❌ Global state
# ❌ from module import * 
# ❌ String concatenation in loops (use join)
# ❌ == None (use `is None`)
# ❌ len(x) == 0 (use `not x`)
```

## 测试

- 推荐使用 pytest 或 unittest 进行测试
- 测试文件的命名格式为 `test_*.py`，测试函数的命名格式为 `test_*
- 尽量编写针对具体功能的单元测试，并对外部依赖进行模拟
- 在每次提交代码之前运行测试：`python -m pytest -v`

## 文档字符串（Docstrings）

```python
def fetch_user(user_id: int, include_deleted: bool = False) -> User | None:
    """Fetch a user by ID from the database.
    
    Args:
        user_id: The unique user identifier.
        include_deleted: If True, include soft-deleted users.
    
    Returns:
        User object if found, None otherwise.
    
    Raises:
        DatabaseError: If connection fails.
    """
```

## 快速检查清单

- [ ] 代码语法正确（使用 `py_compile` 检查）
- [ ] 测试通过（使用 `pytest` 运行）
- [ ] 公开函数上添加了类型提示
- [ ] 代码中不存在硬编码的敏感信息（如密码等）
- [ ] 使用 f-strings 而不是 `.format()` 或 `%` 来生成字符串
- [ ] 使用 `pathlib` 来处理文件路径
- [ ] 对于 I/O 操作使用上下文管理器（context managers）
- [ ] 不允许使用可变的默认参数