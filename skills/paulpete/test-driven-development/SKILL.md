---
name: test-driven-development
description: 统一的TDD（测试驱动开发）技能，支持三种输入方式：根据需求规格（spec）、根据任务要求（task）或根据功能描述（description）来启动测试。该技能遵循“测试先行”的开发原则，利用仓库模式（repository patterns）进行测试开发，并结合proptest的指导和backpressure机制来实现测试与开发的协同工作。
type: anthropic-skill
version: "1.0"
---

# 驱动测试开发（Test-Driven Development, TDD）

## 概述

这是一项适用于所有 TDD 工作流程的通用技能。它通过现有的仓库模式强制实现“先编写测试（test-first）”的开发方式。系统支持三种输入模式：规范文件（`.spec.md`）、任务文件（`.code-task.md`）或临时描述，但核心的开发周期始终是“RED → GREEN → REFACTOR”。

## 输入模式

系统会自动检测输入类型，并根据相应的模式进行处理：

### 模式 A：来自规范文件（`.spec.md`）

当输入文件为包含“Given/When/Then”验收标准的 `.spec.md` 文件时使用此模式：

1. **定位并解析** 规范文件，提取所有的验收标准。
2. **为每个验收标准生成一个测试模板**，并使用 `todo!()` 函数来标记待完成的测试任务：
   ```rust
   /// Spec: <spec-file> — Criterion #<N>
   /// Given <given text>
   /// When <when text>
   /// Then <then text>
   #[test]
   fn <spec_name>_criterion_<N>_<slug>() {
       todo!("Implement: <then text>");
   }
   ```
3. **验证测试模板是否能够编译**，如果无法编译则输出错误信息：`cargo test --no-run -p <crate>`
4. 进入 [TDD 开发周期](#tdd-cycle) 以修改代码，直到所有测试通过。

**编程支持：** `ralph_core::preflight::{extract_acceptance_criteria, extract_criteria_from_file, extract_all_criteria}` 可用于从规范文件中提取验收标准。

### 模式 B：来自任务文件（`.code-task.md`）

当输入文件为 `.code-task.md` 或具体的实现任务文件时使用此模式：

1. **阅读任务描述**，明确验收标准或需求。
2. **发现代码中的模式**（参见 [模式发现](#pattern-discovery) 部分）。
3. **设计测试用例**，覆盖正常操作、边界情况和错误条件。
4. **在实现代码之前，先编写所有需求的测试用例**。
5. 进入 [TDD 开发周期](#tdd-cycle)。

### 模式 C：来自临时描述

适用于没有规范文件或任务文件的临时性开发任务：

1. **从描述中明确需求**。
2. **发现代码中的模式**（参见 [模式发现](#pattern-discovery) 部分）。
3. **针对描述中的行为编写测试用例**。
4. 进入 [TDD 开发周期](#tdd-cycle)。

## 模式发现（Pattern Discovery）

在编写测试之前，需要先了解现有的代码规范和测试模式：

```bash
rg --files -g "crates/*/tests/*.rs"
rg -n "#\[cfg\(test\)\]" crates/
```

阅读目标代码附近 2-3 个相关的测试文件，观察以下内容：
- 测试模块的布局、命名规则和断言风格。
- 用于辅助测试的辅助工具和实用程序。
- 是否使用了 `tempfile`、测试场景（scenarios）或其他测试框架。

## TDD 开发周期（TDD Cycle）

### 1) RED 阶段：测试失败

- 为所需的行为编写测试用例。
- 运行测试，确认测试确实因为代码错误而失败。
- 如果在没有实现任何代码的情况下测试通过了，说明测试本身存在问题。

### 2) GREEN 阶段：最小化实现

- 编写最基本的代码，使测试通过。
- 在此阶段不要添加额外的功能或进行重构。

### 3) REFACTOR 阶段：代码优化

- 在保持测试通过的前提下，改进代码实现。
- 使代码符合项目中的整体规范。
- 每次修改代码后重新运行测试。

## 使用 `proptest` 的指导原则

只有在以下情况下才使用 `proptest`：
- 函数纯函数（不涉及 I/O 操作、不依赖时间、不使用全局变量）。
- 对于给定的输入，函数输出结果是确定的（即结果具有确定性）。
- 输入范围复杂或存在边界情况。

```rust
proptest! {
    #[test]
    fn round_trip(input in "[a-z0-9]{0,32}") {
        let encoded = encode(input.as_str());
        let decoded = decode(&encoded).expect("should decode");
        prop_assert_eq!(decoded, input);
    }
}
```

在没有充分理由的情况下，不要引入 `proptest` 作为新的依赖项。

## 集成测试覆盖率（Integration Testing）

在完成代码开发后，需要验证代码的覆盖率：

```bash
ralph emit "build.done" "tests: pass, lint: pass, typecheck: pass, audit: pass, coverage: pass (82%)"
```

如果可能的话，运行 `cargo tarpaulin --out Html --output-dir coverage --skip-clean` 命令来生成覆盖率报告。如果无法运行该命令，请说明原因，并提供相应的测试结果作为替代证据。

## 测试文件的放置规则

- 如果规范文件仅针对一个模块，测试代码应直接放在该模块中，并使用 `#[cfg(test)]` 注解。
- 如果规范文件涉及多个模块，测试代码应放在 `crates/<crate>/tests/` 目录下。
- 如果代码涉及命令行接口（CLI），测试代码应放在 `crates/ralph-cli/tests/` 目录下。
- 遵循目标代码库中的现有测试规范。

## 应避免的错误做法（Anti-Patterns）：

- 在编写测试之前先实现代码。
- 编写那些在没有实现代码的情况下就能通过的测试用例。
- 从其他代码库复制测试代码而不进行适配。
- 在简单的情况下使用 `proptest` 而不是编写简单的测试用例。
- 在没有覆盖率数据的情况下就发布代码完成事件。