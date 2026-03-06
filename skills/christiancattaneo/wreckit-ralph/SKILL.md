---
name: reckit
description: >
  **防篡改的AI代码验证工具**：该工具本身就是执行所有验证任务的引擎，无需任何外部工具的支持。它会生成多个并行工作的验证进程，负责进行代码的全面扫描、类型检查、变异测试以及交叉验证，确保代码在发布前符合质量标准。该工具对编程语言和开发框架均无限制，现已支持Swift和iOS开发环境。  
  **适用场景：**  
  1. 在新建项目时，需要编写经过验证和测试的代码（例如：“使用带有测试功能的代码构建X”）。  
  2. 在迁移或重构代码库时（例如：“将代码重写为TypeScript”）。  
  3. 修复漏洞时，需要确保修复不会引发其他问题（例如：“修复这个漏洞，并验证是否会导致任何回归问题”）。  
  4. 审计现有代码的质量（例如：“审计这个项目”或“这些测试的质量如何”）。  
  5. 任何与“reckit”、“wreckit”、“变异测试”、“代码验证”、“代码审计”等相关术语相关的需求。  
  **输出结果：**  
  该工具会生成一个名为`.wreckit`的验证结果文件，其中包含详细的验证过程记录以及“通过”、“警告”或“失败”的判定结果。
metadata:
  openclaw:
    platforms: [macos, linux]
    notes: "Uses sessions_spawn for parallel verification swarms. Requires maxSpawnDepth >= 2."
---
# Reckit — 高效的AI代码验证工具

构建代码，测试代码，验证其正确性。

## 哲学理念

AI本身无法自我验证。因此，我们需要设计一套流程，确保AI在验证过程中不会自欺欺人。  
在新的代码环境中，应明确划分构建者（Builder）、测试者（Tester）和破坏者（Breaker）的角色，并使用独立的验证工具（oracles）。

> **完整的14步验证框架：** `references/verification-framework.md`

## 验证模式

根据代码上下文自动选择相应的验证模式：

| 模式 | 触发条件 | 描述 |
|------|---------|-------------|
| 🟢 构建（BUILD） | 仓库为空 + 项目需求文档（PRD） | 从头开始的全流程验证 |
| 🟡 重建（REBUILD） | 现有代码 + 迁移方案 | 包括代码构建、行为捕获和回放测试 |
| 🔴 修复（FIX） | 现有代码 + 错误报告 | 修复代码并验证，检查是否有回归问题 |
| 🔵 审计（AUDIT） | 现有代码（无更改） | 仅进行验证并生成报告 |

## 验证关卡（Gates）

在执行任何验证步骤之前，请先阅读对应的关卡文件。每个关卡文件包含以下内容：验证问题、需要执行的检查项以及通过/失败的标准。

| 关卡名称 | BUILD | REBUILD | FIX | AUDIT | 文件路径 |
|------|-------|---------|-----|-------|------|
| AI代码质量扫描（AI Slop Scan） | ✅ | ✅ | ✅ | ✅ | `references/gates/slop-scan.md` |
| 类型检查（Type Check） | ✅ | ✅ | ✅ | ✅ | `references/gates/type-check.md` |
| Ralph循环验证（Ralph Loop） | ✅ | ✅ | ✅ | ❌ | `references/gates/ralph-loop.md` |
| 测试质量（Test Quality） | ✅ | ✅ | ✅ | ✅ | `references/gates/test-quality.md` |
| 变异测试（Mutation Test） | ✅ | ✅ | ✅ | ✅ | `references/gates/mutation-kill.md` |
| 跨域验证（Cross-Verify） | ✅ | ❌ | ❌ | ❌ | `references/gates/cross-verify.md` |
| 行为捕获（Behavior Capture） | ❌ | ✅ | ❌ | ❌ | `references/gates/behavior-capture.md` |
| 回归测试（Regression） | ❌ | ✅ | ✅ | ❌ | `references/gates/regression.md` |
| 静态应用安全测试（SAST） | ❌ | ❌ | ✅ | ✅ | `references/gates/sast.md` |
| LLM作为裁判（LLM-as-Judge） | 可选 | 可选 | 可选 | 可选 | `references/gates/llm-judge.md` |
| 设计审查（Design Review） | ❌ | ❌ | ❌ | ✅ | `references/gates/design-review.md` |
| 持续集成（CI Integration） | ✅ | ✅ | ❌ | ✅ | `references/gates/ci-integration.md` |
| 代码验证包生成（Proof Bundle） | ✅ | ✅ | ✅ | ✅ | `references/gates/proof-bundle.md` |

## 脚本（Scripts）

这些脚本用于辅助验证过程，切勿自行修改：

**通用脚本（适用于所有模式）：**
- `scripts/project-type.sh [路径]` — 分类项目类型并配置校准参数（`skip_gates`、阈值、可容忍的警告级别） |
- `scripts/detect-stack.sh [路径]` — 自动检测代码语言、框架及测试工具，并生成JSON输出 |
- `scripts/check-deps.sh [路径] | 确保所有依赖项存在于注册表中 |
- `scripts/slop-scan.sh [路径] | 进行语义检查，区分已跟踪和未跟踪的依赖项，并生成分类后的结果（JSON） |
- `scripts/type-check.sh [路径] | 运行类型检查工具（tsc/mypy/cargo/go vet）并生成JSON |
- `scripts/ralph-loop.sh [路径] | 验证`IMPLEMENTATION_PLAN.md`文件的结构是否正确 |
- `scripts/coverage-stats.sh [路径] | 从测试工具中提取代码覆盖率数据 |
- `scripts/mutation-test.sh [路径] [test-cmd] | 执行变异测试（mutmut/cargo-mutants/Stryker/AI） |
- `scripts/mutation-test-stryker.sh [路径] | 使用Stryker进行专门的变异测试 |
- `scripts/red-team.sh [路径] | 进行静态应用安全测试（SAST），检测20多种常见漏洞 |
- `scripts/regex-complexity.sh [路径] | 分析代码中的正则表达式复杂性（可选） |
- `scripts/proof-bundle.sh [路径] | 生成验证结果包 |
- `scripts/run-all-gates.sh [路径] [模式]` | 顺序执行所有验证关卡，并记录日志 |

**特定模式的脚本：**
- `scripts/behavior-capture.sh [路径] | 在重建前捕获基准测试用例 |
- `scripts/design-review.sh [路径] | 分析代码的依赖关系和循环依赖（适用于AUDIT/REBUILD模式） |
- `scripts/ci-integration.sh [路径] | 检测并评估持续集成配置 |
- `scripts/differential-test.sh [路径] | 比较不同版本的代码结果（适用于BUILD/REBUILD模式） |

**扩展验证功能：**
- `scripts/dynamic-analysis.sh [路径] | 检测内存泄漏、竞态条件等问题 |
- `scripts/perf-benchmark.sh [路径] | 进行性能基准测试并检测代码变化 |
- `scripts/property-test.sh [路径] | 进行基于属性的模糊测试 |

## Swarm架构

若需并行执行多个验证关卡，请参考`references/swarm/orchestrator.md`。

**快速入门：**
```
Main agent → wreckit orchestrator (depth 1)
  ├─ Planning: Architect worker
  ├─ Building: Sequential Implementer workers
  ├─ Verification: Parallel gate workers
  ├─ Sequential: Cross-verify / regression / judge
  └─ Decision: Proof bundle → Ship / Caution / Blocked
```

**重要提示：** 在启动验证流程之前，请务必阅读`references/swarm/collect.md`。  
切勿伪造验证结果，必须等待所有验证任务完成后再得出最终结论。  
工作节点的输出格式为`references/swarm/handoff.md`。

**配置要求：**
```json
{ "agents.defaults.subagents": { "maxSpawnDepth": 2, "maxChildrenPerAgent": 8 } }
```

## 决策框架

| 验证结果 | 判断标准 |
|---------|----------|
| **通过（Ship）** | 无严重问题；且没有多领域验证失败的情况超过预设阈值 |
| **谨慎（Caution）** ⚠️ | 仅有一个非严重问题，或验证结果未达到预设阈值 |
| **失败（Blocked）** 🚫 | 存在严重问题，或有多个领域的验证失败情况 |

关于“严重问题”及验证确认的详细规则，请参阅`references/gates/corroboration.md`。

## 支持的语言和开发框架

| 语言 | 可用的验证关卡 | 备注 |
|----------|----------------|-------|
| TypeScript/JavaScript | 全部支持（通过Stryker、tsc、vitest/jest工具） |
| Python | 全部支持（通过mutmut、mypy/pyright、pytest工具） |
| Rust | 全部支持（通过cargo-mutants、cargo-check/test工具） |
| Go | 全部支持（通过go vet、go test工具） |
| Swift（使用SPM构建工具） | 9项验证可用；变异检测依赖AI分析，交叉验证需手动完成 |
| Swift（使用Xcode构建工具） | 7项验证可用；类型检查依赖Xcodebuild，变异检测依赖AI分析，代码覆盖率有限 |
| iOS应用 | 7项验证可用（与Xcode项目相同） |
| Java/Kotlin | 10项验证可用；依赖管理通过Gradle/Maven实现，变异检测需手动配置 |
| Shell脚本 | 8项验证可用；仅支持基本的变异检测 |

### Swift相关说明：

- **变异测试需要手动验证**：截至2026年，Swift尚未有自动化的变异测试工具。因此，变异检测环节依赖AI分析结果（统计变异数量并与实际测试数量进行对比），结果始终显示为“谨慎（CAUTION）”，永远不会显示为“通过（SHIP）”。
- **使用SPM构建的Swift项目**：类型检查依赖Swift内置的类型检查器（`swift build`）。
- **使用Xcode构建的Swift项目**：类型检查依赖Xcode内置的`xcodebuild`工具，类型检测结果为中等可信度。
- **依赖项检查**：虽然可以检测到SPM相关的依赖项，但Swift包的CVE数据库尚未完善，因此建议手动审核。
- **CocoaPods项目**：如果项目中包含`Podfile`，会检查依赖项是否过时。

## 单独执行审计（无需使用Swarm）

对于小型项目或无需并行验证的情况，可以按以下步骤依次执行各个验证关卡：

1. `scripts/detect-stack.sh` — 确定项目的语言、测试工具和类型检查工具 |
2. `scripts/check-deps.sh` — 确保依赖项真实存在 |
3. `scripts/slop-scan.sh` — 检查代码中是否存在占位符或无效的测试用例 |
4. 根据`scripts/detect-stack`的输出结果运行类型检查工具（`scripts/check-deps.sh`） |
5. 运行测试并生成代码覆盖率报告（`scripts/coverage-stats.sh`） |
6. 执行变异测试（`scripts/mutation-test.sh`，使用`mutmut/cargo-mutants/Stryker`工具） |
7. 进行静态应用安全测试（`scripts/red-team.sh`） |
8. 进行设计审查（`scripts/design-review.sh`） |
9. 检测持续集成配置（`scripts/ci-integration.sh`） |
10. 进行动态分析（`scripts/dynamic-analysis.sh`） |
11. 进行性能基准测试（`scripts/perf-benchmark.sh`） |
12. 进行基于属性的测试（`scripts/property-test.sh`） |
13. 执行差异测试（`scripts/differential-test.sh`） |
14. 使用`scripts/proof-bundle.sh`生成验证结果包（`[路径] [模式]`），并保存到`.wreckit/proof.json`、`dashboard.json`和`decision.md`文件中。

## 快速启动指南

```
"Use wreckit to audit [project]. Don't change anything."
"Use wreckit to build [project] from this PRD."
"Use wreckit to fix [bug]. Prove nothing else breaks."
"Use wreckit to rebuild [project] in [framework]."
```

## 仪表板

`assets/dashboard/`目录下提供了一个本地Web仪表板，用于查看各个项目的验证结果。  
运行命令：`node assets/dashboard/server.mjs`（端口3939）。该仪表板会读取项目中的`.wreckit/dashboard.json`文件。

## Codex CLI使用说明（2026-02-22）

使用Codex CLI构建或运行项目时，请注意以下事项：
- 使用`--full-auto`选项可禁用`npm install`过程中的网络访问（因为`registry.npmjs.org`可能无法访问）；
- 如需绕过安全检查，可使用`--dangerously-bypass-approvals-and-sandbox`选项；
- 认证信息需通过`echo "$OPENAI_API_KEY" | codex login --with-api-key`保存到`~/.codex/auth.json`文件中；
- 配置文件`~/.codex/config.toml`应设置为`model = "gpt-5.2-codex"`，并启用`[shell_environment_policy] inherit = "all"`；
- `gpt-5.3-codex`仅适用于Copilot和VS Code，无法通过API直接使用，请使用`gpt-5.2-codex`。