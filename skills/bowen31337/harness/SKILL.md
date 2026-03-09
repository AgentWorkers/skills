---
name: harness
description: >
  **Agent工程工具包**：适用于任何代码仓库。该工具包能够生成简洁的 `AGENTS.md` 目录结构，提供结构化的文档和知识库（涵盖架构、质量标准、开发规范等内容），同时支持自定义的代理代码检查工具（采用 `WHAT/FIX/REF` 格式），并实现持续集成（CI）流程的自动化管理。支持 Rust、Go、TypeScript 和 Python 语言。适用于以下场景：  
  - 设置以代理（agent）为中心的开发流程；  
  - 升级现有的 `AGENTS.md` 文件；  
  - 强制执行代码架构检查规则。  
  该工具包还提供了 `--audit` 标志，用于执行工具生命周期检查，并支持一级（L1）、二级（L2）和三级（L3）的逐步信息披露机制（progressive disclosure）。
license: MIT
---
# `harness` — 代理工程框架

该框架实现了 [OpenAI Codex 团队的“以代理为核心”的工程开发模式](https://openai.com/index/harness-engineering/)，适用于任何仓库：
- 支持自动生成的 `AGENTS.md` 目录结构
- 提供支持代理理解的代码检查工具（linters）
- 集成持续集成（CI）流程
- 提供执行计划模板
- 有助于文档的维护和管理

该框架已通过 [代理工具设计指南](https://github.com/bowen31337/agent-harness-skills/blob/main/docs/agent_tool_desig_guidelines.md)（2026-03-09）进行验证。

## 使用场景
- 为新仓库设置以代理为核心的开发环境
- 将现有仓库的 `AGENTS.md` 目录结构升级为标准格式
- 为仓库添加代码检查机制（linting）
- 适用于代理执行大部分代码的仓库

## 支持的语言
- **Rust**（使用 Substrate 框架和 cargo 工作区）
- **Go**（内部代码结构和包管理）
- **TypeScript**（使用 `src/` 目录和 npm）
- **Python**（使用 `pyproject.toml` 和 `uv/pytest`）← 2026-03-09 新增支持

## 使用方法

```bash
SKILL_DIR="$HOME/.openclaw/workspace/skills/harness"

# Scaffold harness for a repo (language auto-detected: Rust/Go/TypeScript/Python)
uv run python "$SKILL_DIR/scripts/scaffold.py" --repo /path/to/repo

# Scaffold with force-overwrite of existing AGENTS.md
uv run python "$SKILL_DIR/scripts/scaffold.py" --repo /path/to/repo --force

# Audit harness freshness (tool lifecycle check — no writes)
uv run python "$SKILL_DIR/scripts/scaffold.py" --repo /path/to/repo --audit

# Run lints locally
bash /path/to/repo/scripts/agent-lint.sh

# Check doc freshness (finds stale references in docs/)
uv run python "$SKILL_DIR/scripts/doc_garden.py" --repo /path/to/repo --dry-run

# Check doc freshness and open a fix PR
uv run python "$SKILL_DIR/scripts/doc_garden.py" --repo /path/to/repo --pr

# Generate execution plan for a complex task
uv run python "$SKILL_DIR/scripts/plan.py" \
  --task "Add IBC timeout handling" \
  --repo /path/to/repo
```

## 创建的文件及说明
| 文件名 | 说明 |
|------|-------------|
| `AGENTS.md` | 包含约 100 行的目录结构，采用 L1/L2/L3 三层逐步披露机制 |
| `docs/ARCHITECTURE.md` | 代码架构图及依赖关系规则（根据仓库结构自动生成） |
| `docs/QUALITY.md` | 代码覆盖率目标和安全规范 |
| `docs/CONVENTIONS.md` | 语言特定的命名规则 |
| `docs/COORDINATION.md` | 多代理任务分配及冲突解决规则 ← 新增内容 |
| `docs/EXECUTION_PLAN TEMPLATE.md` | 复杂任务的执行计划模板 |
| `scripts/agent-lint.sh` | 支持代理理解的代码检查工具（包含问题描述、修复建议和参考信息） |
| `.github/workflows/agent-lint.yml` | 在每次提交（PR）时执行的代码检查脚本 |

## 代码检查错误格式

`scripts/agent-lint.sh` 生成的错误信息均遵循以下格式：
```
LINT ERROR [<rule-id>]: <description of the problem>
  WHAT: <why this is a problem>
  FIX:  <exact steps to resolve it>
  REF:  <which doc to consult>
```

这意味着代理可以直接读取错误信息并自行修复问题，无需人工干预。

## 代理设计检查清单（来自工具设计指南）

在发布任何工具或功能更新之前，请验证以下内容：
- [ ] 该工具的设计是否符合模型的实际功能？
- [ ] 是否在关键环节强制使用结构化输出？
- [ ] 是否按层次顺序（L1→L2→L3）逐步加载上下文信息，而不是一次性全部加载？
- [ ] 是否支持多代理之间的协作？（参见 `COORDINATION.md`）
- [ ] 是否评估了工具的使用频率与输出质量之间的关系？
- [ ] 工具数量是否控制在目标范围内（每个代理使用的工具数量不超过 20 个）？
- [ ] 是否有计划根据模型功能的变更重新评估该工具？

## 三层逐步披露机制

该框架遵循三层逐步披露的规则：
| 层次 | 信息来源 | 加载时机 |
|-------|-------|--------------|
| L1 | `AGENTS.md` | 始终加载 — 提供工具使用指南、命令和基本规则 |
| L2 | `docs/` | 编码前加载 — 包含代码架构、质量要求和命名规范 |
| L3 | 源代码文件 | 根据需要按需加载 — 可通过 grep 或其他方式读取特定文件 |

**规则：** 先从 L1 层开始使用；在修改代码前先加载 L2 层的内容；仅在需要时才加载 L3 层的内容。
切勿预先加载所有三层信息，否则会占用过多的系统资源。

## 工具生命周期（--audit）

每季度运行 `--audit` 命令来检查框架的更新情况：
- `AGENTS.md` 是否包含正确的层次结构标记
- 是否有 `COORDINATION.md` 文件（支持多代理协作）
- 代码检查脚本是否使用最新的语言工具
- 对于 Python 项目，是否包含 `ruff` 和 `pyright` 的代码检查工具
- `AGENTS.md` 的文件长度是否控制在 150 行以内

## 安全性注意事项
- **严禁在没有 `--force` 标志的情况下覆盖现有的 `AGENTS.md` 文件**
- 在生成文档之前会读取现有的代码结构，避免生成错误的 API 文档
- 所有修改内容在提交前都会在 `--dry-run` 模式下进行预览

## 参考资料
- [OpenAI Codex 工程框架](https://openai.com/index/harness-engineering/)
- [代理工具设计指南](https://github.com/bowen31337/agent-harness-skills/blob/main/docs/agent_tool_desig_guidelines.md)
- [ClawChain 工具框架的 Pull Request](https://github.com/clawinfra/claw-chain/pull/64)
- [EvoClaw 工具框架的 Pull Request](https://github.com/clawinfra/evoclaw/pull/27)