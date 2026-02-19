---
name: context-engineer
description: "掌握AI代理和大型语言模型（LLM）的上下文工程与提示工程技术。优化系统提示，设计用于少量样本学习的示例（few-shot examples），实现基于链式思维的推理（chain-of-thought reasoning），管理上下文窗口（context windows），设计结构化的输出结果，并构建能够自我优化的提示模式。涵盖了Anthropic、OpenAI和Google的最佳实践。该工具包含一个提示优化器（prompt optimizer），可依据最佳实践对提示内容进行审核；同时还有一个上下文构建器（context builder），能够为任何任务生成最优的上下文窗口。该工具专为AI代理设计，仅使用Python标准库，无需任何额外依赖。适用于提示优化、系统提示设计、代理指令编写、LLM输出调试、上下文窗口管理以及少量样本示例的生成。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🧠", "requires": {"env": []}, "primaryEnv": "", "homepage": "https://www.agxntsix.ai"}}
---
# 🧠 上下文工程师（Context Engineer）

掌握上下文工程（Context Engineering）和提示工程（Prompt Engineering）的精髓——这是一门为大型语言模型（LLMs）设计最佳输入的技艺。

## 主要功能

- **优化提示（Prompt Optimization）**：遵循 Anthropic、OpenAI 和 Google 的最佳实践
- **构建上下文窗口（Build Context Windows）**：整合系统提示、用户提示和示例
- **设计系统提示（Design System Prompts）**：适用于子代理（sub-agents）、定时任务（crons）和特定技能
- **创建少量样本示例（Create Few-Shot Examples）**：显著提升模型的准确性
- **实现复杂任务的推理逻辑（Implement Chain-of-Thought Reasoning）**
- **管理上下文窗口（Manage Context Windows）**：合理安排关键信息的显示顺序
- **结构化输出（Structure Outputs）**：使用 JSON 模式、Markdown 或 XML 标签
- **通过系统化的提示分析来调试模型输出（Debug LLM Outputs）**
- **编写代理指令（Write Agent Instructions）**：参考 `AGENTS.md` 和 `SOUL.md` 文档格式
- **应用基于角色的提示策略（Apply Role-Based Prompting）**：提升模型在特定领域的表现
- **将复杂任务拆分为精确的子任务（Break Complex Tasks into Subtasks）**
- **提供 20 多个常用提示模板（Provide Over 20 Templates）**

## 使用要求

| 变量 | 是否必需 | 说明 |
|--------|---------|-------------|
| 无 | — | 无需 API 密钥，仅需要提示工程相关知识 |

## 快速入门

```bash
PY=~/.openclaw/workspace/.venv/bin/python3

# Analyze and improve a draft prompt
$PY skills/context-engineer/scripts/prompt_optimizer.py "Your draft prompt here"

# Build optimal context window for a task
$PY skills/context-engineer/scripts/context_builder.py "Analyze quarterly financials"

# Optimize from file
$PY skills/context-engineer/scripts/prompt_optimizer.py --file path/to/prompt.txt
```

## 命令说明

### 提示优化器（Prompt Optimizer）
```bash
# Analyze a prompt string
$PY skills/context-engineer/scripts/prompt_optimizer.py "Your prompt"

# Analyze from file
$PY skills/context-engineer/scripts/prompt_optimizer.py --file prompt.txt
```

### 上下文构建器（Context Builder）
```bash
# Build context for a task
$PY skills/context-engineer/scripts/context_builder.py "Task description"

# With role and output format
$PY skills/context-engineer/scripts/context_builder.py --task "Code review" --role "Senior engineer" --output json
```

## 提示工程的十大原则

1. **清晰、直接、详细**：将模型视为一个没有背景知识的新员工，提供明确、具体的指导。
2. **使用示例**：提供 3-5 个多样化的示例，显著提升模型的准确性和一致性。
3. **引导模型思考**：对于复杂问题，采用逐步推理的方式。
4. **使用标签进行结构化**：使用 XML 标签区分指令、上下文和示例。
5. **分配角色**：为系统提示指定具体的角色，提升模型在特定领域的表现。
6. **分解复杂任务**：将多步骤任务拆分为子任务，提高准确性。
7. **合理组织上下文**：将关键信息放在文档的开头和结尾，并通过标签引用相关内容。
8. **指定输出格式**：使用 JSON 模式、Markdown 结构或明确的格式说明。
9. **通过实际测试进行迭代**：根据评估标准进行优化，而非凭直觉判断。
10. **上下文比提示更重要**：内容本身比提问方式更为关键。

## 参考资料

| 文件名 | 说明 |
|--------|-------------|
| `references/anthropic-best-practices.md` | Anthropic 的官方提示工程文档 |
| `references/openai-best-practices.md` | OpenAI 的提示工程指南 |
| `references/google-best-practices.md` | Google Gemini 的提示策略文档 |
| `references/context-engineering-principles.md` | 上下文工程相关理论（Andrej Karpathy 等人撰写） |
| `references/prompt-templates.md` | 20 多个常用提示模板 |

## 脚本参考

| 脚本名 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/prompt_optimizer.py` | 根据最佳实践分析提示内容 |
| `{baseDir}/scripts/context_builder.py` | 为任务构建最优的上下文环境 |

## 输出格式

所有命令默认会生成结构化的文本，包含分析结果、改进建议和优化后的提示内容。

## 数据政策

该技能仅在本地处理提示内容，除非明确使用 LLM API，否则不会向外部服务传输任何数据。

## 参考来源

- Anthropic 提示工程：https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- OpenAI 提示工程：https://platform.openai.com/docs/guides/prompt-engineering
- Google Gemini 提示策略：https://ai.google.dev/gemini-api/docs/prompting-strategies
- Andrej Karpathy 关于上下文工程的论文（2025 年）

---

由 [M. Abidi](https://www.agxntsix.ai) 制作

[LinkedIn](https://www.linkedin.com/in/mohammad-ali-abidi) · [YouTube](https://youtube.com/@aiwithabidi) · [GitHub](https://github.com/aiwithabidi) · [预约咨询](https://cal.com/agxntsix/abidi-openclaw)