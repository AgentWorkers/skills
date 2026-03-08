---
name: quorum
description: 多代理验证框架（v0.5.0）：采用确定性预筛选机制，结合4个独立的AI评审工具，根据预设的评估标准对文档、配置文件、代码以及研究成果进行评估，并提供基于证据的评审结果。该框架支持批量验证以及跨不同类型成果的一致性检查功能。
metadata: {"openclaw":{"requires":{"bins":["python3","pip"],"env":["ANTHROPIC_API_KEY","OPENAI_API_KEY"]},"install":[{"id":"clone-repo","kind":"shell","command":"git clone https://github.com/SharedIntellect/quorum.git /tmp/quorum-install && cd /tmp/quorum-install/reference-implementation && pip install -r requirements.txt","label":"Clone Quorum repo and install Python dependencies"}],"source":"https://github.com/SharedIntellect/quorum"}}
---
# Quorum — 多智能体验证系统

> **⚠️ 重要说明：** 在修改、发布或公开任何 Quorum 代码、配置文件或文档之前，请务必阅读并遵守 `portfolio/research-infrastructure/VALIDATOR-QUORUM-BOUNDARY.md` 文件。该文件定义了内部验证器（Validator）与公开系统（Quorum）之间的边界、哪些内容可以被公开、哪些内容属于专有信息，以及 CKMS（内容管理系统）的命名规范。所有规定均不可例外。

Quorum 通过启动多个独立的评估引擎来验证 AI 智能体的输出结果，这些评估引擎会根据预设的标准对输出内容进行评估。每个评估结果都必须附带相应的证据支持。最终会给出结构化的评估结论。

## 快速入门

克隆仓库并安装相关依赖：

```bash
git clone https://github.com/SharedIntellect/quorum.git
cd quorum/reference-implementation
pip install -r requirements.txt
```

对任意文件执行 Quorum 验证：

```bash
python -m quorum.cli run --target <path-to-artifact> --rubric <rubric-name>
```

### 内置的评估标准

- `research-synthesis` — 研究报告、文献综述、技术分析
- `agent-config` — 智能体配置文件、YAML 规范、系统提示信息

### 评估深度

- `quick` — 2 个评估引擎（评估正确性和完整性）+ 预筛选，耗时约 5-10 分钟
- `standard` — 4 个评估引擎（额外检查安全性和代码质量）+ 预筛选，耗时约 15-30 分钟（默认设置）
- `thorough` — 使用所有 4 个评估引擎进行评估 + 预筛选，耗时约 30-60 分钟

所有评估流程都会在启动 LLM（大型语言模型）评估引擎之前，先进行一次确定性的预筛选（包含 10 项检查：凭证验证、个人身份信息保护、语法错误、失效链接、待办事项等）。

### 示例

```bash
# Validate a research report
quorum run --target my-report.md --rubric research-synthesis

# Quick check (faster, fewer critics)
quorum run --target my-report.md --rubric research-synthesis --depth quick

# Batch: validate all markdown files in a directory
quorum run --target ./docs/ --pattern "*.md" --rubric research-synthesis

# Cross-artifact consistency check
quorum run --target ./src/ --relationships quorum-relationships.yaml --depth standard

# Use a custom rubric
quorum run --target my-spec.md --rubric ./my-rubric.json

# List available rubrics
quorum rubrics list

# Initialize config interactively
quorum config init
```

## 配置

首次运行时，Quorum 会询问您偏好的模型类型，并自动生成 `quorum-config.yaml` 配置文件；您也可以手动创建该文件：

```yaml
models:
  tier_1: anthropic/claude-sonnet-4-6    # Judgment roles
  tier_2: anthropic/claude-sonnet-4-6    # Evaluation roles
depth: standard
```

设置您的 API 密钥：

```bash
export ANTHROPIC_API_KEY=sk-ant-...
# or
export OPENAI_API_KEY=sk-...
```

## 输出结果

Quorum 会给出结构化的评估结论：
- **PASS** — 未发现重大问题
- **PASS_WITH_NOTES** — 存在轻微问题，但文件仍可使用
- **REVISE** — 存在需要修改的严重问题，需重新处理后再进行评估
- **REJECT** — 存在无法解决的问题，需要重新启动系统

退出代码说明：
- `0` = PASS/PASS_WITH_NOTES
- `1` = 出现错误
- `2` = 需要重新评估/拒绝

每个评估结果会包含问题的严重程度（CRITICAL/HIGH/MEDIUM/LOW）、指向问题具体位置的证据引用，以及相应的修复建议。运行目录中会包含 `prescreen.json`（预筛选结果）、每个评估引擎的评估结果 JSON 文件、`verdict.json`（最终评估结果文件），以及一份便于人类阅读的 `report.md` 报告。

## 更多信息

- [SPEC.md](https://github.com/SharedIntellect/quorum/blob/main/SPEC.md) — 完整的架构规范
- [MODEL_REQUIREMENTS.md](https://github.com/SharedIntellect/quorum/blob/main/docs/MODEL.requireMENTS.md) — 支持的模型及使用层级
- [CONFIG_REFERENCE.md](https://github.com/SharedIntellect/quorum/blob/main/docs/CONFIG_REFERENCE.md) — 所有配置选项的详细说明
- [FOR_BEGINNERS.md](https://github.com/SharedIntellect/quorum/blob/main/docs/FOR_BEGINNERS.md) — 新手指南：从这里开始学习智能体验证流程

---

> ⚖️ **许可证说明：** 本文件不属于上述操作规范的一部分，而是 [Quorum](https://github.com/SharedIntellect/quorum) 项目的一部分。
> 本文件受 2026 年 SharedIntellect 公司的 MIT 许可证保护。详细许可条款请参阅 [LICENSE](https://github.com/SharedIntellect/quorum/blob/main/LICENSE)。