---
name: Test Generator
description: 自动化测试用例生成工具。支持单元测试、集成测试、端到端测试；提供模拟对象（mock objects）和测试 fixtures；具备代码覆盖率分析功能；能够生成边界测试用例（edge case generation）以及性能基准测试（performance benchmarks）。兼容 Python、JavaScript 和 Go 语言；支持测试驱动开发（TDD）框架，如 pytest、jest、vitest、mocha 等。同时，该工具还集成了多种开发者工具（developer-tools）。
---
# 测试生成器 — 自动化测试用例生成

> 在几秒钟内生成高质量的测试代码，告别繁琐的手动编写工作

## 为什么使用这个工具？

- 编写测试代码非常繁琐 → 该工具可自动生成测试模板，只需填充业务逻辑即可
- 缺少边缘测试用例 → `edge` 命令可系统地生成边界测试用例
- 模拟（mock）设置过程繁琐 → 提供标准化的模拟模式，可以直接复制粘贴使用

## 命令参考

```
unit <lang> <function>       → Unit test template
integration <lang> <module>  → Integration test template
e2e <lang> <flow>            → End-to-end test flow
mock <lang> <target>         → Mock/Stub objects
fixture <lang> <type>        → Test fixtures
coverage <lang>              → Coverage config and tips
edge <type> <range>          → Edge case generation
benchmark <lang> <target>    → Performance benchmark test
```

## 支持的框架

| 语言 | 测试框架 |
|----------|---------------|
| Python | pytest, unittest |
| JavaScript | Jest, Mocha, Vitest |
| Go | testing, testify |
| Bash | bats |

## 最佳实践

将测试用例命名为 `test_<功能>_<场景>_<预期结果>`，以提高代码的可读性。