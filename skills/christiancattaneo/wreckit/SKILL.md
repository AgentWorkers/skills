---
name: wreckit
description: >
  **防篡改的AI代码验证系统**  
  该系统本身就是代码验证的核心引擎，无需任何外部工具的支持。在代码发布前，它会自动生成多个并行验证任务，执行代码的全面扫描、类型检查、变异测试以及交叉验证等操作。该系统对编程语言和开发框架均无特定要求。适用场景包括：  
  1. 在新项目中编写需要经过验证和测试的代码（例如：“使用TypeScript编写代码并添加测试”）；  
  2. 迁移或重构现有代码库（例如：“将代码重写为TypeScript”）；  
  3. 修复漏洞的同时确保其他功能不受影响（例如：“修复这个漏洞，并验证是否存在回归问题”）；  
  4. 审查现有代码的质量（例如：“审计这个项目”或“这些测试的可靠性如何”）；  
  5. 任何与“代码验证”、“变异测试”、“代码审计”等相关请求。  
  系统会生成一个名为`.wreckit`的验证结果包，其中包含详细的验证结果以及“通过”、“谨慎使用”或“禁止使用”的判定。
metadata:
  openclaw:
    platforms: [macos, linux]
    notes: "Uses sessions_spawn for parallel verification swarms. Requires maxSpawnDepth >= 2."
---
# wreckit — 高效的AI代码验证工具

构建代码 → 打破代码 → 证明其正确性。

## 哲学理念

AI本身无法自我验证。因此，我们需要设计一个流程，确保AI在验证过程中不会自欺欺人。  
将代码构建、测试和破坏的职责分配给不同的角色，并使用独立的验证工具（即“预言机”）来确保验证的客观性。

> **完整的14步验证框架：** `references/verification-framework.md`

## 验证模式

根据项目上下文自动选择相应的验证模式：

| 模式 | 触发条件 | 描述 |
|------|---------|-------------|
| 🟢 构建（BUILD） | 仓库为空 + 项目需求文档（PRD） | 适用于全新项目的完整验证流程 |
| 🟡 重建（REBUILD） | 存在代码 + 迁移方案 | 包括代码构建、行为捕获和回放测试 |
| 🔴 修复（FIX） | 存在代码 + 错误报告 | 修复代码并验证修复效果，同时检查是否有回归问题 |
| 🔵 审计（AUDIT） | 代码未发生任何更改 | 仅进行验证并生成报告 |

## 验证关卡（Gates）

在执行验证前，请务必阅读相应的关卡文件。每个关卡文件包含以下内容：验证问题、需要执行的检查项目以及通过/失败的标准。

| 关卡名称 | 构建（BUILD） | 重建（REBUILD） | 修复（FIX） | 审计（AUDIT） | 文件路径 |
|------|-------|---------|-----|-------|------|
| AI代码质量扫描（AI Slop Scan） | ✅ | ✅ | ✅ | ✅ | `references/gates/slop-scan.md` |
| 类型检查（Type Check） | ✅ | ✅ | ✅ | ✅ | `references/gates/type-check.md` |
| Ralph循环测试（Ralph Loop） | ✅ | ✅ | ✅ | ❌ | `references/gates/ralph-loop.md` |
| 测试质量（Test Quality） | ✅ | ✅ | ✅ | ✅ | `references/gates/test-quality.md` |
| 突变测试（Mutation Test） | ✅ | ✅ | ✅ | ✅ | `references/gates/mutation-kill.md` |
| 跨领域验证（Cross-Verify） | ✅ | ❌ | ❌ | ❌ | `references/gates/cross-verify.md` |
| 行为捕获（Behavior Capture） | ❌ | ✅ | ❌ | ❌ | `references/gates/behavior-capture.md` |
| 回归测试（Regression） | ❌ | ✅ | ✅ | ❌ | `references/gates/regression.md` |
| 静态应用安全测试（SAST） | ❌ | ❌ | ✅ | ✅ | `references/gates/sast.md` |
| LLM作为裁判（LLM-as-Judge） | 可选 | 可选 | 可选 | 可选 | `references/gates/llm-judge.md` |
| 设计审查（Design Review） | ❌ | ❌ | ❌ | ✅ | `references/gates/design-review.md` |
| 持续集成（CI Integration） | ✅ | ✅ | ❌ | ✅ | `references/gates/ci-integration.md` |
| 代码验证包生成（Proof Bundle） | ✅ | ✅ | ✅ | ✅ | `references/gates/proof-bundle.md` |

## 脚本（Scripts）

这些脚本用于辅助验证过程，请勿自行修改：

**通用脚本（适用于所有模式）：**
- `scripts/project-type.sh [路径]`：分析项目类型并配置验证参数（如跳过某些关卡、设置阈值、容忍警告等） |
- `scripts/detect-stack.sh [路径]`：自动检测项目使用的语言、框架及测试工具，并生成相应的JSON输出 |
- `scripts/check-deps.sh [路径]`：验证项目依赖项是否存在于官方注册库中 |
- `scripts/slop-scan.sh [路径]：检查代码中的潜在问题（如未跟踪的依赖项等），并生成JSON输出 |
- `scripts/type-check.sh [路径]：运行类型检查工具（如tsc、mypy、cargo或go vet），并生成JSON结果 |
- `scripts/ralph-loop.sh [路径]：验证`IMPLEMENTATION_PLAN.md`文件的结构是否正确 |
- `scripts/coverage-stats.sh [路径]：从测试工具中提取代码覆盖率数据 |
- `scripts/mutation-test.sh [路径] [test-cmd]`：执行突变测试（使用mutmut、cargo-mutants或Stryker工具），并生成JSON结果 |
- `scripts/mutation-test-stryker.sh [路径]：使用Stryker工具进行特定的突变测试 |
- `scripts/red-team.sh [路径]：执行SAST测试，并检查是否存在20种以上的安全漏洞 |
- `scripts/regex-complexity.sh [路径]`：分析代码中的复杂正则表达式，检测潜在的ReDoS攻击风险 |
- `scripts/proof-bundle.sh [路径] [模式]：根据验证结果生成代码验证包 |
- `scripts/run-all-gates.sh [路径] [模式] [log-file]`：顺序执行所有验证关卡，并记录测试过程 |

**特定模式的脚本：**
- `scripts/behavior-capture.sh [路径]：在重建代码前捕获关键测试数据 |
- `scripts/design-review.sh [路径]：分析项目中的依赖关系和循环依赖项 |
- `scripts/ci-integration.sh [路径]：检测并评估持续集成配置 |
- `scripts/differential-test.sh [路径]：比较不同版本的代码，验证测试结果 |

**扩展验证功能：**
- `scripts/dynamic-analysis.sh [路径]：检测内存泄漏、竞态条件等问题 |
- `scripts/perf-benchmark.sh [路径]：进行性能基准测试，并检查代码是否存在性能下降 |
- `scripts/property-test.sh [路径]：执行基于属性的模糊测试，并生成测试用例 |

**启动脚本（Bootstrap）：**
- `scripts/run-audit.sh [路径] [模式]`：生成执行验证任务的脚本，并可选地启动多个工作节点 |

## Swarm架构

如需并行执行多个验证关卡，请参考`references/swarm/orchestrator.md`。

**快速入门指南：**
```
Main agent → wreckit orchestrator (depth 1)
  ├─ Planning: Architect worker
  ├─ Building: Sequential Implementer workers
  ├─ Verification: Parallel gate workers
  ├─ Sequential: Cross-verify / regression / judge
  └─ Decision: Proof bundle → Ship / Caution / Blocked
```

**重要提示：** 在启动验证任务之前，请务必阅读`references/swarm/collect.md`文件。  
切勿伪造验证结果，必须等待所有工作节点完成测试后才能得出最终结论。  
工作节点的输出格式为`references/swarm/handoff.md`。

**配置要求：**
```json
{ "agents.defaults.subagents": { "maxSpawnDepth": 2, "maxChildrenPerAgent": 8 } }
```

## 决策框架

| 验证结果 | 判断标准 |
|---------|----------|
| **通过（Ship）** ✅ | 无严重问题；且没有多领域验证失败的情况 |
| **警告（Caution）** ⚠️ | 仅存在单个非严重问题，或验证结果未达到预设标准 |
| **失败（Blocked）** 🚫 | 存在严重问题，或有多个领域的验证失败情况 |

关于“严重问题”及验证确认规则的详细信息，请参阅`references/gates/corroboration.md`。

## 单独执行审计（无需使用Swarm）

对于小型项目或不需要并行验证的情况，可以按以下步骤顺序执行验证流程：

1. `scripts/detect-stack.sh`：确定项目使用的编程语言和测试工具 |
2. `scripts/check-deps.sh`：验证项目依赖项是否真实存在 |
3. `scripts/slop-scan.sh`：检查代码中是否存在潜在问题 |
4. 运行类型检查工具（根据`detect-stack`的输出结果） |
5. 运行测试并收集代码覆盖率数据（`scripts/coverage-stats.sh`） |
6. 执行突变测试（`scripts/mutation-test.sh`） |
7. 执行SAST测试（`scripts/red-team.sh`） |
8. 进行设计审查（`scripts/design-review.sh`） |
9. 检查持续集成配置（`scripts/ci-integration.sh`） |
10. 进行动态分析（`scripts/dynamic-analysis.sh`） |
11. 进行性能基准测试（`scripts/perf-benchmark.sh`） |
12. 执行基于属性的测试（`scripts/property-test.sh`） |
13. 将所有验证结果整合到`proof-bundle.sh`中，并生成相应的报告文件（`.wreckit/proof.json`、`dashboard.json`和`decision.md`）。

## 快速启动指南（Quick Start）**
```
"Use wreckit to audit [project]. Don't change anything."
"Use wreckit to build [project] from this PRD."
"Use wreckit to fix [bug]. Prove nothing else breaks."
"Use wreckit to rebuild [project] in [framework]."
```

## 仪表板（Dashboard）

`assets/dashboard/`目录下提供了一个本地Web仪表板，用于查看各个项目的验证结果。  
运行命令：`node assets/dashboard/server.mjs`（端口3939）。该仪表板会读取项目中的`.wreckit/dashboard.json`文件。

## Codex CLI使用说明（2026-02-22）：

在使用Codex CLI构建或运行项目时，请注意以下配置选项：
- `--full-auto`：禁用`npm install`过程中的网络访问（因为`registry.npmjs.org`可能无法访问）；
- 使用`--dangerously-bypass-approvals-and-sandbox`选项可绕过某些安全限制；
- 认证：`echo "$OPENAI_API_KEY" | codex login --with-api-key`可将凭据保存到`~/.codex/auth.json`文件中；
- 配置文件：`~/.codex/config.toml`应设置为`model = "gpt-5.2-codex"`，并启用`[shell_environment_policy] inherit = "all"`；
- 注意：`gpt-5.3-codex`仅适用于Copilot和VS Code，无法通过API直接使用，请使用`gpt-5.2-codex`。