---
name: wreckit
description: >
  **防篡改的AI代码验证系统**  
  该验证系统本身就是核心执行引擎，无需任何外部工具辅助。在代码发布前，它会自动生成多个并行验证任务，执行代码的全面扫描、类型检查、变异测试以及交叉验证等操作。该系统对编程语言和开发框架均无特定要求，适用于以下场景：  
  1. **新项目开发**：需要确保代码的质量和可靠性（例如：“使用TypeScript编写代码并对其进行测试”）。  
  2. **代码库迁移/重构**：在将代码从旧框架迁移到新框架时（例如：“将代码重写为TypeScript”）。  
  3. **故障修复**：在修复故障时需要验证修复操作是否会导致其他功能出现问题（例如：“修复这个漏洞，同时确保没有引入新的错误”）。  
  4. **代码质量审计**：对现有代码进行质量评估（例如：“审计这个项目，这些测试的有效性如何？”）。  
  5. **任何与代码验证相关的需求**：如“代码完整性验证”、“变异测试”、“代码审计”等。  
  该系统会生成一个名为`.wreckit/`的验证结果文件，其中包含详细的验证结果以及“通过”、“警告”或“阻止”等判定结果。
metadata:
  openclaw:
    platforms: [macos, linux]
    notes: "Uses sessions_spawn for parallel verification swarms. Requires maxSpawnDepth >= 2."
---
# wreckit — 高可靠性的AI代码验证工具

构建代码 → 打破代码 → 证明代码的正确性。

## 哲学理念

AI本身无法自我验证。因此，我们需要设计一个流程，确保AI在验证过程中不会自欺欺人（即不会默认认为自己的判断是正确的）。  
在新的代码环境中，应明确划分构建者（Builder）、测试者（Tester）和破坏者（Breaker）的角色，并使用独立的验证工具（Oracles）。

> **完整的14步验证框架：** `references/verification-framework.md`

## 验证模式

根据代码环境自动选择相应的验证模式：

| 模式 | 触发条件 | 描述 |
|------|---------|-------------|
| 🟢 构建（BUILD） | 仓库为空 + 项目需求文档（PRD） | 适用于全新的代码项目 |
| 🟡 重建（REBUILD） | 现有代码 + 迁移方案 | 包括构建、行为捕获和回放测试 |
| 🔴 修复（FIX） | 现有代码 + 错误报告 | 修复代码后进行验证，并检查是否引发回归问题 |
| 🔵 审计（AUDIT） | 现有代码（无更改） | 仅进行验证并生成报告 |

## 验证关卡（Gates）

在执行每个验证步骤之前，请先阅读对应的关卡文件。每个关卡文件包含以下内容：验证问题、需要执行的检查项目以及通过/失败的判断标准。

| 关卡名称 | BUILD | REBUILD | FIX | AUDIT | 文件路径 |
|------|-------|---------|-----|-------|------|
| AI代码质量扫描（AI Slop Scan） | ✅ | ✅ | ✅ | ✅ | `references/gates/slop-scan.md` |
| 类型检查（Type Check） | ✅ | ✅ | ✅ | ✅ | `references/gates/type-check.md` |
| Ralph循环检测（Ralph Loop） | ✅ | ✅ | ✅ | ❌ | `references/gates/ralph-loop.md` |
| 测试质量（Test Quality） | ✅ | ✅ | ✅ | ✅ | `references/gates/test-quality.md` |
| 变异测试（Mutation Test） | ✅ | ✅ | ✅ | ✅ | `references/gates/mutation-kill.md` |
| 跨模块验证（Cross-Verify） | ✅ | ❌ | ❌ | ❌ | `references/gates/cross-verify.md` |
| 行为捕获（Behavior Capture） | ❌ | ✅ | ❌ | ❌ | `references/gates/behavior-capture.md` |
| 回归测试（Regression） | ❌ | ✅ | ✅ | ❌ | `references/gates/regression.md` |
| 静态应用安全测试（SAST） | ❌ | ❌ | ✅ | ✅ | `references/gates/sast.md` |
| LLM作为裁判（LLM-as-Judge） | 可选 | 可选 | 可选 | 可选 | `references/gates/llm-judge.md` |
| 设计审查（Design Review） | ❌ | ❌ | ❌ | ✅ | `references/gates/design-review.md` |
| 持续集成（CI Integration） | ✅ | ✅ | ❌ | ✅ | `references/gates/ci-integration.md` |
| 代码验证包（Proof Bundle） | ✅ | ✅ | ✅ | ✅ | `references/gates/proof-bundle.md` |

## 辅助脚本

这些脚本用于辅助验证流程，请勿自行修改：

- `scripts/detect-stack.sh [路径]`：自动检测代码的语言、使用的框架及测试工具，并生成JSON格式的结果 |
- `scripts/check-deps.sh [路径]`：验证所有依赖项是否存在于相应的注册库中 |
- `scripts/slop-scan.sh [路径]`：检查代码中是否存在占位符、模板文件或无用的代码 |
- `scripts/mutation-test.sh [路径] [测试命令]`：自动执行变异测试（最多20个变异） |
- `scripts/mutation-test-stryker.sh [路径]`：基于Stryker框架的变异测试工具（生成JSON结果） |
- `scripts/coverage-stats.sh [路径]`：从测试工具中提取代码覆盖率数据 |
- `scripts/design-review.sh [路径]：分析代码的依赖关系和循环依赖情况（生成JSON结果） |
- `scripts/ci-integration.sh [路径]：检测并评估持续集成（CI）配置的合理性（生成JSON结果） |

## 分布式执行架构（Swarm Architecture）

如需并行执行多个验证关卡，请参考 `references/swarm/orchestrator.md`。

**快速入门：**  
```
Main agent → wreckit orchestrator (depth 1)
  ├─ Planning: Architect worker
  ├─ Building: Sequential Implementer workers
  ├─ Verification: Parallel gate workers
  ├─ Sequential: Cross-verify / regression / judge
  └─ Decision: Proof bundle → Ship / Caution / Blocked
```

**重要提示：** 在启动验证流程之前，请务必阅读 `references/swarm/collect.md`。  
切勿伪造验证结果，必须等待所有验证任务完成后才能得出最终结论。  
工作节点的输出格式为 `references/swarm/handoff.md`。

**所需配置文件：**  
```json
{ "agents.defaults.subagents": { "maxSpawnDepth": 2, "maxChildrenPerAgent": 8 } }
```

## 决策机制

| 验证结果 | 判断标准 |
|---------|----------|
| **通过（Ship）** | 所有关卡均通过，变异测试通过率≥95%，且无代码质量问题 |
| **警告（Caution）** | 所有关卡均通过，但变异测试通过率在90%-95%之间，或存在非关键性的代码问题 |
| **失败（Blocked）** | 有任何关卡未通过，或检测到错误的依赖关系，或变异测试通过率低于90% |

## 单独运行审计流程（无需分布式执行）

对于小型项目或无需分布式验证的情况，可以按顺序执行以下步骤：

1. `scripts/detect-stack.sh`：确定目标代码的语言、测试工具及类型检查工具 |
2. `scripts/check-deps.sh`：验证依赖项是否真实存在 |
3. `scripts/slop-scan.sh`：检查代码中是否存在占位符或无用的代码 |
4. 运行类型检查工具（根据`scripts/detect-stack.sh`的输出结果） |
5. 运行测试并使用 `scripts/coverage-stats.sh` 分析代码覆盖率 |
6. 使用 `scripts/mutation-test.sh` 进行变异测试 |
7. 使用 `scripts/red-team.sh` 检查代码的安全性（生成JSON报告） |
8. 运行 `scripts/design-review.sh` 进行设计审查 |
9. 使用 `scripts/ci-integration.sh` 检查持续集成配置 |
10. 使用 `scripts/dynamic-analysis.sh` 检查代码是否存在内存泄漏或竞态条件 |
11. 使用 `scripts/perf-benchmark.sh` 进行性能测试并检测代码是否出现回归问题 |
12. 使用 `scripts/property-test.sh` 进行属性测试和不变量检查 |
13. 使用 `scripts/differential-test.sh` 进行差异性测试 |
14. 阅读并执行 `references/gates/proof-bundle.md` 以生成最终的验证报告（`.wreckit/` 文件）。

## 快速启动指南（Quick Start）  
```
"Use wreckit to audit [project]. Don't change anything."
"Use wreckit to build [project] from this PRD."
"Use wreckit to fix [bug]. Prove nothing else breaks."
"Use wreckit to rebuild [project] in [framework]."
```

## 仪表板（Dashboard）

`assets/dashboard/` 目录下提供了一个本地Web仪表板，用于查看各个项目的验证结果。  
运行 `node assets/dashboard/server.mjs`（端口3939），该脚本会读取项目中的 `.wreckit/dashboard.json` 文件以显示验证结果。