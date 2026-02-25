---
name: py-test-creator
description: >
  根据提供的 `SKILL.md` 文件内容，可以将其翻译为中文（简体）如下：
  **功能描述：**  
  该工具能够根据 Python 函数的签名（function signatures）和文档字符串（docstrings）自动生成与 `pytest` 兼容的单元测试模板。  
  **工作原理：**  
  1. 从 Python 函数的签名中提取必要的信息，用于构建测试用例的结构。  
  2. 利用函数文档字符串中的说明性内容来编写测试用例的具体实现逻辑。  
  3. 生成格式规范的测试代码，确保测试代码能够正确地验证函数的功能。  
  **适用场景：**  
  - 当你需要为已有的 Python 函数编写单元测试时。  
  - 当你希望自动化测试代码的生成过程以提高开发效率时。  
  **注意事项：**  
  - 该工具假设函数文档字符串中包含了足够的测试信息，以便生成有效的测试用例。  
  - 如果函数文档字符串不完整或包含错误的信息，生成的测试代码可能无法正确运行。  
  **示例：**  
  假设你有一个如下定义的 Python 函数：  
  ```python
  def add(a, b):
      """
      加法函数，返回 a 和 b 的和。
      """
      return a + b
  ```
  使用该工具后，你可以得到如下格式的测试模板：  
  ```python
  def test_add():
      assert add(1, 2) == 3
      assert add(-1, 2) == 1
      assert add(0, 2) == 2
  ```
  这些测试用例分别验证了 `add` 函数对正数、负数和零的加法操作是否正确。
---
# py-test-creator — 技能文档

## 概述

`py-test-creator` 是一个 OpenClaw 技能，它能够从 Python 代码自动生成全面的 pytest 单元测试模板。该技能会解析函数签名、类型提示和文档字符串，从而创建出能够覆盖边缘情况及参数组合的测试框架。

**主要特性：**
- 支持解析具有复杂签名的 Python 函数（包括默认参数、类型提示和可变参数）
- 生成符合 pytest 标准的测试方法，并包含适当的断言语句
- 既支持独立函数，也支持类方法
- 将文档字符串转换为测试方法的文档说明
- 生成格式正确、包含必要导入语句的测试文件

## 安装

依赖项通过 `package.json` 管理。使用以下命令进行安装：

```bash
npm install
```

这将安装所需的 Python 包（pytest、ast-parser 工具）以及运行该技能所需的 Node.js 依赖项。

## 使用方法

使用自然语言触发该技能：
- “为这个 Python 函数创建单元测试”
- “根据这些函数签名生成测试模板”
- “为我的 Python 方法编写 pytest 测试”
- “根据文档字符串创建单元测试框架”

该技能接受一个 Python 文件或代码片段作为输入，并生成相应的测试文件。

## 输入/输出

**输入：**
一个 Python 文件路径或包含一个或多个函数/方法的原始代码。

**输出：**
一个测试文件（例如 `test_<original>.py`），其中包含以下内容：
- `import pytest` 语句
- 针对常见参数类型的测试用例
- 对边缘情况的覆盖（如 `None` 值、边界值、无效类型）
- 在适当的情况下包含参数化测试
- 解释测试目的的文档字符串

**示例：**

输入文件（`utils.py`）：
```python
def add(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b
```

输出文件（`test_utils.py`）：
```python
import pytest
from utils import add

def test_add_basic_integers():
    """Test add function with basic positive integers."""
    assert add(1, 2) == 3

def test_add_negative_numbers():
    """Test add function with negative integers."""
    assert add(-1, -2) == -3

def test_add_zero():
    """Test add function with zero."""
    assert add(0, 5) == 5
    assert add(5, 0) == 5

def test_add_large_numbers():
    """Test add function with large integers."""
    assert add(1000000, 2000000) == 3000000
```

## 配置

无需额外配置。该技能使用默认的 pytest 规范。

**可选环境变量：**
- `PYTEST_STRICT`：设置为 `true` 可启用严格的标记处理
- `TEST_COVERAGE`：设置为 `true` 可在生成的测试中包含覆盖率提示

## 错误处理**

在以下情况下，该技能会以非零状态退出：
- Python 语法错误
- 输入文件/代码缺失
- 写入输出时出现权限问题
- AST 解析失败

错误信息会被记录到标准错误输出（stderr）中。

## 限制

以下内容不在该技能的覆盖范围内：
- 运行或验证生成的测试
- 集成测试/端到端测试
- 多语言支持（仅支持 Python）
- CI/CD 集成
- 测试性能优化

## 文件结构

该技能包包含以下文件：
```
skill/
├── SKILL.md           # This documentation
├── package.json       # NPM package definition
├── README.md          # Quick start guide
└── scripts/
    ├── main.py        # CLI entry point
    ├── parser.py      # Python AST parser
    ├── generator.py   # Test template generator
    └── cli.py         # Command-line interface
```

## 资源参考：
- [pytest 文档](https://docs.pytest.org/)
- [Python AST 模块](https://docs.python.org/3/library/ast.html)
- [OpenClaw 技能系统](https://docs.openclaw.ai)

## 支持方式

如需报告问题、提出功能请求或贡献代码，请访问：
- 代码仓库：`openclaw/openclaw`
- Discord 频道：https://discord.com/invite/clawd

## 许可证

MIT © OpenClaw Contributors