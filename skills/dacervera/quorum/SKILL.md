---
name: quorum
description: 多智能体验证框架：该框架会生成独立的AI评审员，根据预先设定的评估标准（rubrics）对各类成果（如文档、配置文件、代码、研究成果等）进行评估，并提供基于证据的评审结果。
metadata: {"openclaw":{"requires":{"bins":["python3","pip"],"env":["ANTHROPIC_API_KEY","OPENAI_API_KEY"]},"install":[{"id":"clone-repo","kind":"shell","command":"git clone https://github.com/SharedIntellect/quorum.git /tmp/quorum-install && cd /tmp/quorum-install/reference-implementation && pip install -r requirements.txt","label":"Clone Quorum repo and install Python dependencies"}],"source":"https://github.com/SharedIntellect/quorum"}}
---
# Quorum — 多智能体验证系统

Quorum 通过启动多个独立的评估者来验证 AI 智能体的输出结果，这些评估者会根据预设的评分标准对输出内容进行评估。每个评估结果都必须提供相应的证据支持。最终会给出一个结构化的评估结论。

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

### 内置的评分标准

- `research-synthesis` — 研究报告、文献综述、技术分析
- `agent-config` — 智能体配置文件（YAML 格式）
- `system-prompts` — 系统提示信息

### 评估模式

- `quick` — 3 个评估者，无修复环节，评估时间 5-15 分钟
- `standard` — 6 个评估者，对关键问题进行 1 轮修复，评估时间 15-30 分钟（默认模式）
- `thorough` — 全部 9 个评估者 + 外部验证器，最多 2 轮修复，评估时间 45-90 分钟

### 示例

```bash
# Validate a research report
python -m quorum.cli run --target my-report.md --rubric research-synthesis

# Quick check (faster, fewer critics)
python -m quorum.cli run --target my-report.md --rubric research-synthesis --depth quick

# List available rubrics
python -m quorum.cli rubrics list

# Initialize config interactively
python -m quorum.cli config init
```

## 配置

首次运行时，Quorum 会询问您偏好的评估模型，并自动生成 `quorum-config.yaml` 文件；您也可以手动创建该文件：

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

Quorum 会生成一个结构化的评估结论：
- **PASS** — 未发现重大问题
- **PASS_WITH_NOTES** — 存在轻微问题，但输出内容仍可使用
- **FAIL** — 存在需要解决的关键问题或高严重级别的问题

每个评估结果会包含问题的严重程度（CRITICAL/HIGH/MEDIUM/LOW）、指向输出内容具体位置的证据引用，以及相应的修复建议。

## 更多信息

- [SPEC.md](https://github.com/SharedIntellect/quorum/blob/main/SPEC.md) — 完整的架构规范
- [MODEL_REQUIREMENTS.md](https://github.com/SharedIntellect/quorum/blob/main/docs/MODEL_REQUIREMENTS.md) — 支持的模型及等级要求
- [CONFIG_REFERENCE.md](https://github.com/SharedIntellect/quorum/blob/main/docs/CONFIG_REFERENCE.md) — 所有配置选项
- [FOR_BEGINNERS.md](https://github.com/SharedIntellect/quorum/blob/main/docs/FOR_BEGINNERS.md) — 新手指南：从这里开始学习智能体验证流程

---

> ⚖️ **许可证** — 本文件不属于上述操作规范的一部分。
> 本文件属于 [Quorum](https://github.com/SharedIntellect/quorum) 项目。
> 版权所有 © 2026 SharedIntellect。采用 MIT 许可协议。
> 详细许可条款请参阅 [LICENSE](https://github.com/SharedIntellect/quorum/blob/main/LICENSE)。