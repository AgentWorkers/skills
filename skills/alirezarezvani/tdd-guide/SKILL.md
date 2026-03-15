---
name: "tdd-guide"
description: "**测试驱动开发（Test-Driven Development, TDD）技能**  
包括编写单元测试、生成测试用例（test fixtures）和模拟对象（mocks）、分析代码覆盖率（coverage gaps），以及指导使用Jest、Pytest、JUnit、Vitest和Mocha等测试框架进行代码重构（red-green-refactoring）的工作流程。适用于用户需要编写测试代码、提升代码覆盖率、实践TDD方法、生成模拟对象或存根文件（stubs），或提及Jest、Pytest、JUnit等测试框架的场景。该技能涵盖从源代码生成测试用例的功能、覆盖率报告的解析（LCOV/JSON/XML格式）、代码质量评估，以及针对TypeScript、JavaScript、Python和Java项目的测试框架适配工作。"
triggers:
  - generate tests
  - analyze coverage
  - TDD workflow
  - red green refactor
  - Jest tests
  - Pytest tests
  - JUnit tests
  - coverage report
---
# TDD指南

本指南介绍了基于测试驱动开发（Test-Driven Development, TDD）的技能，包括如何生成测试用例、分析代码覆盖率，以及如何使用Jest、Pytest、JUnit和Vitest等工具来指导“红-绿-重构”（Red-Green-Refactor）的开发流程。

---

## 开发流程

### 从代码生成测试用例

1. 提供源代码（TypeScript、JavaScript、Python、Java）。
2. 指定目标测试框架（Jest、Pytest、JUnit、Vitest）。
3. 运行`test_generator.py`并输入相关需求。
4. 审查生成的测试代码。
5. **验证：** 确保测试能够覆盖正常情况、错误情况和边界情况。

### 分析代码覆盖率

1. 使用测试运行工具（如`npm test -- --coverage`）生成覆盖率报告。
2. 运行`coverage_analyzer.py`来解析LCOV/JSON/XML格式的覆盖率报告。
3. 优先处理高优先级的覆盖率缺口（P0/P1/P2）。
4. 为未覆盖的代码路径生成缺失的测试用例。
5. **验证：** 确保覆盖率达到目标值（通常为80%以上）。

### 新功能的TDD开发流程

1. 首先编写会导致测试失败的代码（红色阶段，RED）。
2. 运行`tdd_workflow.py --phase red`进行验证。
3. 实现最基本的代码以使测试通过（绿色阶段，GREEN）。
4. 再次运行`tdd_workflow.py --phase green`进行验证。
5. 在保持所有测试通过的情况下进行代码重构（重构阶段，REFCTOR）。
6. **验证：** 每个开发周期结束后，所有测试都必须通过。

---

## 示例

### 测试用例生成 — 输入 → 输出（以Pytest为例）

**输入源代码文件（`math_utils.py`）：**
```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**执行命令：**
```bash
python scripts/test_generator.py --input math_utils.py --framework pytest
```

**生成的测试代码文件（`test_math_utils.py`）：**
```python
import pytest
from math_utils import divide

class TestDivide:
    def test_divide_positive_numbers(self):
        assert divide(10, 2) == 5.0

    def test_divide_negative_numerator(self):
        assert divide(-10, 2) == -5.0

    def test_divide_float_result(self):
        assert divide(1, 3) == pytest.approx(0.333, rel=1e-3)

    def test_divide_by_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_divide_zero_numerator(self):
        assert divide(0, 5) == 0.0
```

---

### 覆盖率分析 — 示例输出（P0/P1/P2级别）**

**执行命令：**
```bash
python scripts/coverage_analyzer.py --report lcov.info --threshold 80
```

**示例输出：**
```
Coverage Report — Overall: 63% (threshold: 80%)

P0 — Critical gaps (uncovered error paths):
  auth/login.py:42-58   handle_expired_token()       0% covered
  payments/process.py:91-110  handle_payment_failure()   0% covered

P1 — High-value gaps (core logic branches):
  users/service.py:77   update_profile() — else branch  0% covered
  orders/cart.py:134    apply_discount() — zero-qty guard  0% covered

P2 — Low-risk gaps (utility / helper functions):
  utils/formatting.py:12  format_currency()            0% covered

Recommended: Generate tests for P0 items first to reach 80% threshold.
```

---

## 关键工具

| 工具 | 功能 | 使用方法 |
|------|---------|-------|
| `test_generator.py` | 从代码或需求生成测试用例 | `python scripts/test_generator.py --input source.py --framework pytest` |
| `coverage_analyzer.py` | 解析和分析覆盖率报告 | `python scripts/coverage_analyzer.py --report lcov.info --threshold 80` |
| `tdd_workflow.py` | 指导“红-绿-重构”开发流程 | `python scripts/tdd_workflow.py --phase red --test test_auth.py` |
| `fixture_generator.py` | 生成测试数据和模拟对象 | `python scripts/fixture_generator.py --entity User --count 5` |

其他辅助工具：`framework_adapter.py`（用于在不同测试框架之间进行转换）、`metrics_calculator.py`（用于生成质量指标）、`format_detector.py`（用于检测代码语言/框架）、`output_formatter.py`（用于生成CLI/桌面/CI格式的输出）。

---

## 输入要求

**生成测试用例时需要：**
- 源代码（文件路径或代码内容）
- 目标测试框架（Jest、Pytest、JUnit、Vitest）
- 覆盖范围（单元测试、集成测试、边界测试）

**分析代码覆盖率时需要：**
- 覆盖率报告文件（LCOV、JSON或XML格式）
- 可选：源代码以辅助理解代码逻辑
- 可选：目标覆盖率阈值

**进行TDD开发时需要：**
- 功能需求或用户故事
- 当前的开发阶段（红色阶段、绿色阶段、重构阶段）
- 测试代码的编写状态及实现进度

---

## 限制

| 限制因素 | 详细说明 |
|-------|---------|
| **适用范围**：** 主要适用于单元测试；集成测试和端到端测试需要其他方法** |
| **静态分析**：** 无法执行测试或测量代码的运行时行为** |
| **语言支持**：** 最适合TypeScript、JavaScript、Python、Java语言** |
| **报告格式**：** 仅支持LCOV、JSON、XML格式；其他格式需转换** |
| **生成的测试代码**：** 提供基本框架，复杂逻辑需要人工审核** |

**何时使用其他工具：**
- **端到端测试**：Playwright、Cypress、Selenium
- **性能测试**：k6、JMeter、Locust
- **安全测试**：OWASP ZAP、Burp Suite