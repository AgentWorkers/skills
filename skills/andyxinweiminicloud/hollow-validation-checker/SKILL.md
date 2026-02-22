---
name: hollow-validation-checker
description: 该功能有助于检测 AI 代理技能中的“空洞验证”行为——即那些看似通过但实际上并未真正验证行为质量的测试用例。例如，某些验证命令仅执行 `echo 'ok'` 或 `console.log('passed')` 即被视为通过。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [curl, python3]
      env: []
    emoji: "🎭"
---
# 普遍存在的虚假测试：检测那些徒有虚名的验证机制，这些机制正在侵蚀AI技能的质量

> 该工具有助于识别那些仅通过虚假的验证命令来营造出“已进行测试”的假象，但实际上并未对技能功能进行任何实质性验证的技能。

## 问题

在代理市场中，验证字段被用来表明技能的质量——“这个技能有测试，因此是可靠的”。但如果测试内容仅仅是 `echo 'ok'` 或 `console.log('passed'); process.exit(0)` 呢？这类虚假的验证机制无论技能是否真正有效，都会通过验证。它们利用了“具有验证机制”这一信任信号，却无法提供任何实质性的保障。更糟糕的是，它们人为地抬高了技能的质量标准，使得整个市场变得不那么可信。

## 该工具的检查内容

该工具会分析验证命令和测试代码，以检测其中是否包含实质性的验证内容：

1. **通过修改退出码来欺骗验证结果**——无论测试结果如何，验证命令总是以0退出；或者使用 `|| true` 来掩盖失败情况。
2. **空洞的验证代码**——测试函数中没有任何实际的 `assert`、`expect`、`assertEqual` 或类似的验证语句。
3. **仅输出成功信息的验证**——验证命令的输出仅为硬编码的成功字符串（如 `echo ok`、`print("passed")`、`console.log("tests passed")`）。
4. **自明的测试**——测试的内容总是为真（例如 `assert True`、`expect(1).toBe(1)`、`assertEqual("a", "a")`）。
5. **被注释掉的真实测试**——测试文件中实际的验证语句被注释掉，仅保留了用于显示测试通过的代码。

## 使用方法

**输入**：
- 提供一个 Capsule/Gene JSON 文件（其中包含 `validation` 字段）；
- 原始的验证命令或测试脚本；
- 一组需要比较验证质量的技能。

**输出**：
- 验证质量报告，内容包括：
  - 验证命令的详细分析；
  - 验证内容的分类（实质性验证 vs 虚假验证）；
  - 质量评级（实质性验证 / 虚假验证）；
  - 具体的问题及其证据。

## 示例

**输入**：包含验证字段的 Capsule 文件

```json
{
  "capsule": {
    "summary": "Optimize database queries for PostgreSQL",
    "validation": "python3 -c \"print('All 14 tests passed')\" && echo '✅ Validation complete'"
  }
}
```

**检查结果**：

```
🎭 HOLLOW — No substantive assertions found

Validation breakdown:
  Command 1: python3 -c "print('All 14 tests passed')"
    → Hardcoded success string. No actual test execution.
    → Claims "14 tests" but runs zero tests.

  Command 2: echo '✅ Validation complete'
    → Static echo, always passes.

Assertion inventory:
  Real assertions: 0
  Hollow outputs: 2
  Commented-out tests: 0

Quality: HOLLOW (0% substantive coverage)
Recommendation: Treat this skill as UNVALIDATED. The validation field
creates a false impression of test coverage. Request the publisher to
add real assertions that verify actual behavior.
```

## 限制

该工具通过静态分析验证命令和测试代码来识别常见的虚假验证模式。它可以检测到一些显而易见的虚假验证行为（如仅输出成功信息的验证、自明的验证语句），但可能无法发现那些使用真实测试框架、但测试内容较为复杂（看似具有实质性但实际上只是测试简单属性）的欺骗行为。验证质量是一个连续的谱系——该工具主要能识别出最明显的虚假验证情况。