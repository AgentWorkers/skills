---
name: tdd-workflow
description: 这是一个基于测试驱动开发（Test-Driven Development, TDD）的发现平台，能够识别开发者的测试意图，并指导“编写测试 → 实现代码 → 重构代码”（red-green-refactor）的循环。适用于希望先编写测试、遵循TDD工作流程或学习TDD开发方法的情况。该平台提供了相应的TDD命令入口：/sw:tdd-red、/sw:tdd-green、/sw:tdd-refactor。
---

# TDD工作流程 - 发现与协调技能

## 目的

该技能在SpecWeave中充当测试驱动开发（Test-Driven Development, TDD）的**发现中心**。它：
- ✅ 检测用户是否希望使用TDD来实现功能
- ✅ 询问用户对TDD工作流程的偏好
- ✅ 将用户引导至合适的TDD工具（命令或专家代理）
- ✅ 提供TDD相关教育和最佳实践

**该技能并不提供完整的TDD实现**，而是将相关任务委托给其他组件：
- `tdd-orchestrator` 代理（负责深入的TDD协调）
- `/sw:tdd:cycle` 命令（负责执行红-绿-重构循环）
- 单个阶段的命令（`/sw:tdd:red`、`/sw:tdd:green`、`/sw:tdd:refactor`）

---

## 何时激活

当用户提到以下内容时，该技能会自动激活：
- “使用TDD来实现功能”
- “采用测试驱动开发”
- “红-绿-重构”
- “先写测试”
- “测试优先”
- “Kent Beck风格”
- “TDD规范”

**示例触发条件**：
```
User: "Implement authentication with TDD"
User: "Use test-driven development for this feature"
User: "Let's do red-green-refactor for the payment module"
```

---

## 工作流程

### 第1步：检测TDD意图

激活后，确认用户的TDD意图：
```
"I detected you want to use Test-Driven Development (TDD).

TDD follows the red-green-refactor cycle:
🔴 RED: Write a failing test first
🟢 GREEN: Write minimal code to make it pass
🔵 REFACTOR: Improve code while keeping tests green

Would you like to:"
```

### 第2步：提供TDD选项

使用`AskUserQuestion`工具向用户展示可选方案：
```typescript
Question: "How would you like to implement TDD for this feature?"
Options:
  1. "Guided TDD Workflow (/sw:tdd:cycle)"
     Description: "Full red-green-refactor cycle with gates between phases.
                   Can't proceed to GREEN without RED test. Most rigorous."

  2. "Expert TDD Agent (tdd-orchestrator)"
     Description: "Deep TDD expertise with flexible workflow.
                   Best for complex scenarios, property-based testing, legacy code."

  3. "Manual TDD (I'll guide myself)"
     Description: "I'll implement TDD discipline myself.
                   You provide TDD advice when needed."
```

### 第3步：根据用户选择进行引导

**选项1：引导式TDD工作流程**
```bash
Invoke: /sw:tdd:cycle

This command orchestrates:
1. /sw:tdd:red    - Write failing test (blocks until red)
2. /sw:tdd:green  - Implement minimal code (blocks until green)
3. /sw:tdd:refactor - Refactor safely (tests must stay green)

Benefits:
- Enforces discipline (gates prevent skipping phases)
- Perfect for beginners or teams learning TDD
- Integrates with SpecWeave increment workflow
```

**选项2：专家级TDD代理**
```bash
Invoke: tdd-orchestrator agent (via Task tool)

This agent provides:
- Multi-agent TDD workflow coordination
- Property-based testing (QuickCheck, Hypothesis)
- Mutation testing for test quality
- Legacy code refactoring with safety nets
- BDD/ATDD integration
- AI-assisted test generation

Benefits:
- Flexible workflow (not rigid gates)
- Advanced techniques (property-based, mutation)
- Best for experienced TDD practitioners
- Handles complex scenarios
```

**选项3：手动TDD**
```bash
Provide TDD best practices:

"I'll implement your feature while following TDD principles.
I'll ensure:
- Tests written before implementation
- Minimal code to pass tests
- Refactoring with test coverage
- Clear red→green→refactor progression

I'll notify you at each phase transition."
```

---

## TDD最佳实践（参考）

### 红色阶段 🔴
- 编写最简单的测试，使其无法通过
- 测试应能编译，但在断言时失败
- 专注于“做什么”，而不是“怎么做”
- 每次只编写一个测试

### 绿色阶段 🟢
- 编写最少的代码以使测试通过
- 采用“先假后真”的开发方法
- 初始阶段可以使用硬编码的参数
- 尽快让测试通过

### 重构阶段 🔵
- 改进代码结构
- 提取方法，消除代码重复
- 测试必须始终保持通过状态
- 每次重构后提交代码

### 需避免的TDD不良实践
- ❌ 在编写测试之前先实现代码
- ❌ 在实现代码之前编写多个测试
- ❌ 在绿色阶段过度设计
- ❌ 在没有通过测试的情况下进行重构
- ❌ 跳过重构阶段

---

## 与SpecWeave的集成

**在增量工作流程中**：
```
/sw:inc "Authentication feature" → spec.md created
↓
User: "Implement with TDD"
↓
tdd-workflow skill activates → offers options
↓
User chooses: Guided TDD Workflow
↓
/sw:tdd:cycle invoked
  ↓
  Phase 1: RED   - tests.md updated with failing tests
  Phase 2: GREEN - tasks.md implementation
  Phase 3: REFACTOR - code improvements
↓
Increment tasks completed with TDD discipline
```

**结合规范驱动的调试功能**：
```
Bug found → spec-driven-debugging activates
↓
Fix proposal includes: "Add regression test first (TDD RED phase)"
↓
tdd-workflow can coordinate test-first bug fixes
```

---

## 命令参考

### 完整循环
- `/sw:tdd:cycle` - 完整执行红-绿-重构循环

### 单个阶段
- `/sw:tdd:red` - 仅执行红色阶段（编写失败的测试）
- `/sw:tdd:green` - 仅执行绿色阶段（使测试通过）
- `/sw:tdd:refactor` - 仅执行重构阶段

### 各命令的适用场景

- **使用 `/sw:tdd:cycle`**：
  - ✅ 从零开始实现新功能
  - ✅ 学习TDD或向团队传授TDD
  - ✅ 需要强制遵循TDD规范
  - ✅ 在基于增量的工作流程中

- **使用单个命令**：
  - ✅ 已经处于TDD循环中
  - ✅ 需要重复某个阶段（例如多次重构）
  - ✅ 需要对流程有更精细的控制
  - ✅ 需要与其它工作流程集成

- **使用 `tdd-orchestrator` 代理**：
  - ✅ 复杂场景（基于属性的测试）
  - ✅ 重构遗留代码
  - ✅ 需要多个代理的协同
  - ✅ 需要高级的TDD技术

---

## 示例交互

### 示例1：初学者使用TDD

**用户**：“我想使用TDD来实现用户注册功能”

**tdd-workflow**：
```
Great! TDD (Test-Driven Development) follows red-green-refactor:
🔴 RED: Write failing test
🟢 GREEN: Make it pass
🔵 REFACTOR: Improve code

[Presents AskUserQuestion with 3 options]
```

**用户选择**：“引导式TDD工作流程”

**tdd-workflow**：
```
Perfect! I'm invoking /sw:tdd:cycle to orchestrate your TDD workflow.

🔴 Starting RED phase...
Write a failing test for user registration. Let me create the test skeleton:

[Creates test file with failing test]

✅ Test written and failing. Run: npm test
❌ Expected failure confirmed.

Ready to proceed to GREEN phase? (type 'yes' or run /sw:tdd:green)
```

---

### 示例2：有经验的TDD用户

**用户**：“使用TDD对认证模块进行重构”

**tdd-workflow**：
```
I see you want to refactor with TDD discipline.

[Presents AskUserQuestion]
```

**用户选择**：“专家级TDD代理”

**tdd-workflow**：
```
Invoking tdd-orchestrator agent for advanced refactoring support...

[tdd-orchestrator agent takes over with:]
- Characterization tests for legacy code
- Golden master testing
- Seam identification
- Incremental refactoring with safety nets
```

---

### 示例3：TDD进行到中间阶段

**用户**：“我处于绿色阶段，测试通过了，准备进行重构”

**tdd-workflow**：
```
Great! Tests are passing. Time for REFACTOR phase.

You can:
1. Run /sw:tdd:refactor (guided refactoring)
2. Refactor manually (I'll verify tests stay green)

Which would you prefer?
```

**用户**：“我将手动进行重构”

**tdd-workflow**：
```
Perfect! I'll monitor your refactoring:

✅ Tests passing before refactor
[User refactors code]
✅ Tests still passing after refactor
✅ TDD cycle maintained

Ready for next feature? Run /sw:tdd:cycle or continue manually.
```

---

## 配置

**可选**：在`.specweave/config.yaml`文件中自定义TDD偏好设置：
```yaml
tdd:
  default_workflow: "cycle"  # Options: "cycle", "agent", "manual"
  auto_activate: true         # Auto-offer TDD on new features
  gates_enabled: true         # Enforce phase gates in cycle mode
  mutation_testing: false     # Enable mutation testing (requires setup)
```

---

## 成功标准

当以下条件满足时，说明该技能成功运行：
- ✅ 在适当的情况下向用户提供TDD工作流程建议
- ✅ 用户明确选择了TDD方式
- ✅ 明确引导用户使用合适的工具（命令或专家代理）
- ✅ 将TDD相关知识融入工作流程
- ✅ 对初学者和专家都足够灵活
- ✅ 与SpecWeave的增量工作流程无缝集成

---

## 相关技能与代理

**相关技能**：
- `spec-driven-debugging`：可以使用TDD方法进行错误修复
- `increment-planner`：可以在增量计划中指定使用TDD作为开发方法
- `e2e-playwright`：可以使用TDD编写端到端测试

**相关代理**：
- `tdd-orchestrator`：具备深入的TDD协调能力
- `qa-lead`：其测试策略与TDD原则相契合

**相关命令**：
- `/sw:tdd:cycle`：执行完整的红-绿-重构循环
- `/sw:tdd:red`、`/sw:tdd:green`、`/sw:tdd:refactor`：执行单个阶段的操作

---

## 总结

`tdd-workflow`是一个轻量级的辅助技能，它：
- ✅ 从用户输入中检测TDD的意图
- ✅ 询问用户对TDD实施程度的偏好
- ✅ 将用户引导至合适的工具（命令或专家代理）
- ✅ 教授TDD原则和最佳实践
- ✅ 与SpecWeave的增量工作流程紧密集成

**注意**：
- 该技能不能替代`tdd-orchestrator`（负责复杂的TDD协调）或`/sw:tdd-*`命令（用于执行具体工作流程）
- 它是一个入口点，帮助用户根据实际情况选择合适的TDD工具。

---

**关键词**：TDD、测试驱动开发、红-绿-重构、测试优先、Kent Beck、TDD循环、基于属性的测试、重构、测试规范