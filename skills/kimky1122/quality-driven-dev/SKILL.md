---
name: quality-driven-dev
description: "以质量为导向的开发方式，采用自动化的 TDD（测试驱动开发）/ DDD（领域驱动设计）方法论选择，并结合 TRUST 5 质量框架。适用于构建新功能、重构代码、修复漏洞或任何需要结构化质量保证的编码任务。"
---
# 以质量为导向的开发（Quality-Driven Development）

这是一种受 MoAI-ADK 的 TRUST 5 框架启发的结构化开发方法论。该方法会根据项目状态自动选择测试驱动开发（TDD）或领域驱动开发（DDD），严格执行质量检查，并生成经过测试和文档记录的代码。

## 核心理念

> “编写代码的目的是提高代码质量，而非追求快速的生产效率。”

## 日志记录策略

所有代码都必须包含有意义的日志记录。日志是调试生产环境问题的第一道防线。

### 日志级别

| 级别 | 目的 | 示例 | 运营环境（PRD） | 开发环境（DEV） |
|-------|---------|----------|:---------:|:---------:|
| **ERROR** | 异常、失败、无法恢复的情况 | 异常处理代码块、数据库连接失败、缺少必要参数 | ✅ | ✅ |
| **WARN** | 非预期情况、可恢复的情况 | 使用备用方案、重试、调用过时的功能 | ✅ | ✅ |
| **INFO** | 仅记录核心流程 | API 调用/响应、状态变化、事务开始/结束 | ✅ | ✅ |
| **DEBUG** | 用于详细调试 | 函数的进入/退出、变量值、条件分支、查询参数 | ❌ | ✅ |

### 日志记录规则

**必须记录日志的地方：**
- API 端点入口（INFO：请求参数摘要）
- 外部服务调用前后（INFO：调用目标、响应状态）
- 异常处理代码块（ERROR：错误信息及上下文）
- 业务逻辑分支点（DEBUG：记录分支路径）
- 状态变化（INFO：变化前后的状态）
- 批量处理/调度任务开始/结束（INFO：处理数量、耗时）

**日志编写原则：**
- 在运营环境中，仅通过 INFO 级别的日志就能追踪代码执行流程
- 在开发环境中，可以自由使用 DEBUG 级别的日志，但在运营环境中不应显示这些日志
- 绝对禁止在日志中记录敏感信息（如密码、令牌、个人信息）
- 日志消息中应包含上下文信息（例如 ID、参数）——例如：“处理失败” 应记录为 “订单处理失败 [orderId=123, reason=库存不足” ✅

## 工作流程

### 第 0 阶段：项目分析

在开始编码之前，分析项目：
1. 检查是否存在测试框架（`jest`、`vitest`、`pytest`、`go test` 等）
2. 测量当前的代码覆盖率（如果可用，请运行覆盖率统计命令）
3. 确定使用的语言、开发框架和项目结构
4. **选择日志记录框架**（`slf4j`、`winston`、`pino`、`logback`、`print/console.log` 等）——如果尚未选择，请推荐并设置一个合适的框架
5. 自动选择开发方法论：

```
Coverage >= 10% OR new project → TDD (default)
Coverage < 10% AND existing project → DDD
```

在继续进行之前，将分析结果和选定的方法论报告给相关人员。

### 第 1 阶段：制定 SPEC 文档

在实现之前，先创建 SPEC 文档：

```markdown
# SPEC-{ID}: {Title}

## Goal
One sentence describing what this change achieves.

## Acceptance Criteria
- [ ] Criterion 1 (testable)
- [ ] Criterion 2 (testable)
- [ ] Criterion 3 (testable)

## Scope
- **In scope:** What will be changed
- **Out of scope:** What will NOT be changed

## Technical Approach
Brief description of implementation strategy.

## Log Points
Key locations where logs will be added (level + message summary).

## TRUST 5 Checklist
- [ ] **Tested:** All acceptance criteria have corresponding tests
- [ ] **Readable:** Code is self-documenting with clear naming
- [ ] **Unified:** Follows existing project conventions
- [ ] **Secured:** No new vulnerabilities introduced
- [ ] **Trackable:** Changes are documented and linked to this SPEC
```

### 第 2A 阶段：测试驱动开发（新项目 / 代码覆盖率 ≥ 10%）

严格遵循以下步骤：RED → GREEN → REFACTOR：

**RED — 先编写失败的测试**
1. 为第一个验收标准编写测试用例
2. 运行测试——确认测试失败
3. 报告：“🔴 RED：测试用例已编写且测试结果如预期”

**GREEN — 最小化代码实现**
1. 编写足够的代码以通过测试
2. 在关键位置添加日志记录（API 调用、错误处理、状态变化）
3. 运行测试——确认测试通过
4. 报告：“🟢 GREEN：测试通过”

**REFACTOR — 优化代码**
1. 在保持测试通过的情况下改进代码质量
2. **检查日志质量**——确保日志级别正确、信息清晰且包含上下文
3. 运行所有测试——确认所有测试仍然通过
4. 报告：“♻️ REFACTOR：代码已优化，所有测试通过”

对每个验收标准重复此过程。

### 第 2B 阶段：领域驱动开发（现有项目 / 代码覆盖率 < 10%）

遵循以下步骤：ANALYZE → PRESERVE → IMPROVE：

**ANALYZE — 理解现有代码**
1. 阅读现有代码并识别依赖关系
2. 明确领域边界和副作用
3. **检查现有日志记录**——找出日志缺失的部分
4. 报告：“🔍 ANALYZE：现有代码的行为已记录”

**PRESERVE — 保留现有行为**
1. 为现有代码编写特征化测试用例
2. 运行测试——确认测试通过
3. 报告：“🛡️ PRESERVE：特征化测试已编写”

**IMPROVE — 在测试保护下进行修改**
1. 逐步进行代码修改
2. 在修改的代码路径上添加/优化日志记录
3. 每次修改后运行测试
4. 报告：“📈 IMPROVE：修改内容已通过测试验证”

### 第 3 阶段：TRUST 5 质量检查

在宣布工作完成之前，验证以下 5 项原则是否满足：

| 原则 | 检查内容 | 处理方式 |
|-----------|-------|--------|
| **测试覆盖** | 运行完整的测试套件 | 所有测试通过，覆盖率保持或提高 |
| **可读性** | 检查命名、注释和日志信息 | 修正不清晰的命名，确保日志信息包含上下文 |
| **一致性** | 检查代码风格和日志格式的一致性 | 保持与现有规范一致（缩进、命名、日志格式） |
| **安全性** | 进行安全审查 | 确保日志中不含硬编码的敏感信息 |
| **可追溯性** | 有完整的文档记录和日志覆盖 | 变更内容有明确的记录，关键路径有相应的日志记录 |

只有当所有 5 项检查都通过后，才能宣布工作完成。

### 第 4 阶段：完成报告

```markdown
## ✅ SPEC-{ID} Complete

### Methodology: {TDD|DDD}
### Changes:
- {file1}: {what changed}
- {file2}: {what changed}

### Log Points Added:
- {file1:line}: {level} - {description}
- {file2:line}: {level} - {description}

### Test Results:
- Tests: {passed}/{total}
- Coverage: {before}% → {after}%

### TRUST 5:
- ✅ Tested | ✅ Readable | ✅ Unified | ✅ Secured | ✅ Trackable
```

## 代理角色（Agent Roles）

在处理复杂任务时，根据不同职责分配任务：

| 角色 | 负责内容 | 何时启动 |
|------|-------|-----------------|
| **架构师** | 系统设计、API 接口 | 新功能开发、结构变更 |
| **后端开发** | API、数据库、业务逻辑 | 服务器端开发 |
| **前端开发** | 用户界面、用户体验 | 客户端开发 |
| **安全专家** | 安全漏洞、身份验证、输入验证 | 身份验证功能、数据处理 |
| **测试人员** | 测试策略、边缘情况、测试覆盖率 | 始终参与测试工作（TRUST 5 方法要求） |
| **性能优化** | 性能优化 | 对性能敏感的功能进行优化 |

对于每个任务，确定相关角色，并在评审过程中应用他们的专业视角。

## 参考指南

| 主题 | 参考资料 | 适用场景 |
|-------|-----------|-----------|
| 测试驱动开发模式 | `references/tdd-patterns.md` | 选择 TDD 方法论时参考 |
| 领域驱动开发模式 | `references/ddd-patterns.md` | 选择 DDD 方法论时参考 |
| TRUST 5 详细指南 | `references/trust5-checklist.md` | 质量检查指南 |
| 语言特定指南 | `references/lang-{language}.md` | 需要的语言特定指南 |

## 制约条件

**必须执行的事项：**
- 在选择开发方法论之前，必须分析项目
- 在编码之前，必须制定 SPEC 文档
- 必须编写测试用例（TDD：在编码之前；DDD：在修改代码之前）
- 在完成工作之前，必须执行 TRUST 5 质量检查
- 在每个阶段转换时，必须报告进度
- 在关键代码位置，必须添加有意义的日志记录（包含适当的日志级别）
- 必须确保测试用例真正被执行（而不仅仅是编写了测试代码）——在继续之前，必须运行测试套件并确认测试结果

**禁止的事项：**
- 任何情况下都不得跳过编写测试用例
- 在编写测试用例之前不得先编写代码（TDD 模式）
- 在没有编写特征化测试用例的情况下，不得修改未经过测试的代码（DDD 模式）
- 在未通过所有 TRUST 检查之前，不得宣布工作完成 |
- 不得修改 SPEC 范围之外的代码
- 不得在日志中记录敏感信息（如密码、令牌、个人信息）
- 不得在异常处理代码块中省略日志记录