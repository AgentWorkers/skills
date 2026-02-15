---
name: tdd-guide
description: 基于测试驱动的开发工作流程，包括测试生成、代码覆盖率分析以及多框架支持
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

# TDD 指南

本指南介绍了如何使用 TDD（测试驱动开发）技术来生成测试用例、分析代码覆盖率，并指导在 Jest、Pytest、JUnit 和 Vitest 等测试框架中的红-绿-重构工作流程。

## 目录

- [功能](#capabilities)
- [工作流程](#workflows)
- [工具](#tools)
- [输入要求](#input-requirements)
- [限制](#limitations)

---

## 功能

| 功能 | 描述 |
|------------|-------------|
| 测试用例生成 | 将需求或代码转换为结构良好的测试用例 |
| 覆盖率分析 | 解析 LCOV/JSON/XML 格式的报告，识别代码覆盖率的不足之处，并确定优先级 |
| TDD 工作流程 | 通过验证来指导红-绿-重构循环 |
| 框架适配器 | 为 Jest、Pytest、JUnit、Vitest 等框架生成测试用例 |
| 质量评估 | 评估测试的独立性、断言的准确性以及代码的命名规范 |
| 测试 fixture 生成 | 创建符合实际需求的测试数据、模拟对象（mocks）和测试辅助工具（factories） |

---

## 工作流程

### 从代码生成测试用例

1. 提供源代码（TypeScript、JavaScript、Python、Java）
2. 指定目标测试框架（Jest、Pytest、JUnit、Vitest）
3. 运行 `test_generator.py` 并提供需求信息
4. 查看生成的测试代码
5. **验证：** 测试用例是否能够覆盖正常路径、错误路径和边缘情况

### 分析代码覆盖率不足之处

1. 通过 `npm test -- --coverage` 生成覆盖率报告
2. 运行 `coverage_analyzer.py` 分析 LCOV/JSON/XML 格式的报告
3. 查看需要优先处理的覆盖率不足之处（P0/P1/P2 级别）
4. 为未覆盖的代码路径生成缺失的测试用例
5. **验证：** 覆盖率是否达到目标阈值（通常为 80% 以上）

### 新功能的 TDD 流程

1. 首先编写失败的测试用例（RED 阶段）
2. 运行 `tdd_workflow.py --phase red` 进行验证
3. 实现最基本的代码以使测试通过（GREEN 阶段）
4. 运行 `tdd_workflow.py --phase green` 进行验证
5. 在保持所有测试通过的情况下进行重构（REFACTOR 阶段）
6. **验证：** 每个循环结束后所有测试用例都能通过

---

## 工具

| 工具 | 用途 | 使用方法 |
|------|---------|-------|
| `test_generator.py` | 从代码或需求生成测试用例 | `python scripts/test_generator.py --input source.py --framework pytest` |
| `coverage_analyzer.py` | 解析和分析覆盖率报告 | `python scripts/coverage_analyzer.py --report lcov.info --threshold 80` |
| `tdd_workflow.py` | 指导红-绿-重构循环 | `python scripts/tdd_workflow.py --phase red --test test_auth.py` |
| `framework_adapter.py` | 在不同测试框架之间转换测试代码 | `python scripts/framework_adapter.py --from jest --to pytest` |
| `fixture_generator.py` | 生成测试数据和模拟对象 | `python scripts/fixture_generator.py --entity User --count 5` |
| `metrics_calculator.py` | 计算测试质量指标 | `python scripts/metrics_calculator.py --tests tests/` |
| `format_detector.py` | 识别代码语言和使用的测试框架 | `python scripts/format_detector.py --file source.ts` |
| `output_formatter.py` | 格式化输出结果（适用于 CLI、桌面或 CI 环境） | `python scripts/output_formatter.py --format markdown` |

---

## 输入要求

**用于测试用例生成：**
- 源代码（文件路径或粘贴的代码内容）
- 目标测试框架（Jest、Pytest、JUnit、Vitest）
- 覆盖范围（单元测试、集成测试或边缘测试）

**用于覆盖率分析：**
- 覆盖率报告文件（LCOV、JSON 或 XML 格式）
- 可选：用于提供上下文的源代码
- 可选：目标覆盖率阈值

**用于 TDD 工作流程：**
- 新功能的需求或用户故事
- 当前的工作阶段（RED、GREEN、REFACTOR）
- 测试代码及其实现状态

---

## 限制

| 限制 | 详细说明 |
|-------|---------|
| 适用范围 | 单元测试是主要关注点；集成测试和端到端（E2E）测试需要不同的处理方式 |
| 静态分析 | 无法执行测试或测量代码的运行时行为 |
| 语言支持 | 最适合 TypeScript、JavaScript、Python 和 Java 语言 |
| 报告格式 | 仅支持 LCOV、JSON 和 XML 格式；其他格式需要转换 |
| 生成的测试用例 | 仅提供基本框架；复杂逻辑需要人工审核 |

**何时使用其他工具：**
- 端到端测试：Playwright、Cypress、Selenium
- 性能测试：k6、JMeter、Locust
- 安全测试：OWASP ZAP、Burp Suite