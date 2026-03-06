---
name: deep-recall
version: 1.0.8
description: 纯 Python 实现的递归记忆机制，用于持久化 AI 代理。该机制包括管理器（Manager）、工作节点（Workers）以及合成模块（Synthesis），共同构成一个 RLM（Recursive Memory Loop）循环。该系统不依赖于 Deno 或 FastRLM，仅通过 HTTP 调用任何与 OpenAI 兼容的 LLM（Large Language Model）来完成任务。
metadata: {"openclaw": {"requires": {"env": ["ANTHROPIC_API_KEY (optional)", "OPENAI_API_KEY (optional)", "GOOGLE_API_KEY (optional)", "OPENROUTER_API_KEY (optional)", "DEEPSEEK_API_KEY (optional)", "MISTRAL_API_KEY (optional)", "TOGETHER_API_KEY (optional)", "GROQ_API_KEY (optional)", "FIREWORKS_API_KEY (optional)", "COHERE_API_KEY (optional)", "PERPLEXITY_API_KEY (optional)", "SAMBANOVA_API_KEY (optional)", "CEREBRAS_API_KEY (optional)", "XAI_API_KEY (optional)", "MINIMAX_API_KEY (optional)", "ZHIPU_API_KEY (optional)", "MOONSHOT_API_KEY (optional)", "DASHSCOPE_API_KEY (optional)"], "config_paths": ["~/.openclaw/openclaw.json", "~/.openclaw/agents/*/agent/models.json", "~/.openclaw/credentials/*"]}, "homepage": "https://github.com/Stefan27-4/DeepRecall"}}
---
# DeepRecall v2 — OpenClaw 技能

这是一个基于纯 Python 的递归记忆系统，专为持久化 AI 代理设计。它实现了“Anamnesis”架构（记忆体系）的核心理念：“灵魂保持简洁，思维却能无限扩展。”

## 描述

DeepRecall 通过 Python 语言实现了一个强大的记忆系统，使 AI 代理具备“无限记忆”功能。它通过“管理器 → 工作器 → 合成”这样的循环结构，递归地查询代理自身的记忆文件。整个系统不依赖于任何第三方库（如 Deno、fast-rlm 或向量数据库），仅使用 Markdown 文件以及 HTTP 请求来与 OpenAI 兼容的 LLM（大型语言模型）接口进行通信。

当代理需要检索信息时，DeepRecall 会：
1. 扫描工作区中的记忆文件（按类别分类）；
2. 索引文件的元数据（文件标题、主题、创建日期、涉及人员）；
3. 管理器从索引中选择最相关的文件；
4. 多个工作器并行地从每个文件中提取完整的原文引用；
5. 最后，将这些引用整合成一个有条理的答案。

为了确保结果的准确性，工作器会遵循特定的提示规则，仅返回原文引用；同时，每个引用都会附带文件名和具体行号作为出处标注。

## 安装

可以通过以下命令安装 DeepRecall：

```bash
pip install deep-recall
```

或者选择从源代码进行安装：

```bash
git clone https://github.com/Stefan27-4/DeepRecall
cd DeepRecall && pip install .
```

### 所需依赖库

- **httpx**（推荐）或 **requests**：用于发送 HTTP 请求到 LLM；
- **PyYAML**：用于解析配置文件；
- **Python 3.10 或更高版本**；
- 一个在 OpenClaw 中配置好的 LLM 提供者。

> **注意：** v2 版本中，Deno 和 fast-rlm 已不再被使用。整个 RLM 循环完全在 Python 环境中运行。

## 快速入门

```python
from deep_recall import recall

result = recall("What did we decide about the project architecture?")
print(result)
```

## API 接口

### `recall(query, scope, workspace, verbose, config_overrides) → str`

这是 DeepRecall 的主要入口函数，负责执行完整的处理流程（管理器 → 工作器 → 合成）。

```python
from deep_recall import recall

result = recall(
    "Find all mentions of budget discussions",
    scope="memory",          # "memory" | "identity" | "project" | "all"
    verbose=True,            # print progress to stdout
    config_overrides={
        "max_files": 5,      # max files the manager can select
    },
)
```

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- |
| `query` | `str` | 需要检索的内容 |
| `scope` | `str` | 文件搜索范围（例如：“memory”） | 详见 [Scopes](#scopes) |
| `workspace` | `Path` 或 `None` | 自动检测工作区路径 | 可手动指定 |
| `verbose` | `bool` | `False` | 是否输出详细信息（包括提供者、模型、文件选择过程） |
| `config_overrides` | `dict` 或 `None` | 配置覆盖项 | 可覆盖 `max_files` 等设置 |

**返回值：** 包含检索结果的字符串，若未找到文件或结果，则返回 `[DeepRecall]` 状态信息。

---

### `recall_quick(query, verbose) → str`

这是一个快速、高效的检索函数，仅搜索特定类型的文件（例如身份文件）。适用于简单查询场景。

```python
from deep_recall import recall_quick

name = recall_quick("What is my human's name?")
```

等同于 `recall(query, scope="identity", config_overrides={"max_files": 2})`。

---

### `recall_deep(query, verbose) → str`

这个函数会搜索工作区中的所有文件，适用于需要全面检索的情况。

```python
from deep_recall import recall_deep

summary = recall_deep("Summarize all decisions from March")
```

等同于 `recall(query, scope="all", config_overrides={"max_files": 5})`。

---

## 命令行接口（CLI）

### 文件搜索范围（Scopes）

不同的搜索范围会影响搜索速度和资源消耗：
| 范围 | 包含的文件 | 速度 | 资源消耗 | 使用场景 |
| --- | --- | --- | --- |
| `identity` | `SOUL.md`, `IDENTITY.md`, `MEMORY.md`, `USER.md`, `TOOLS.md`, `HEARTBEAT.md`, `AGENTS.md` | 最快 | 最省资源 | 例如：“我的名字是什么？” |
| `memory` | 身份文件 + 长期记忆文件（`memory/LONG_TERM.md`） | 较快 | 例如：“我们上周做了什么？” |
| `project` | 所有可读文件（排除二进制文件、`node_modules` 和 `.git` 目录） | 较慢 | 例如：“查找配置变更” |
| `all` | 所有文件 | 最慢 | 例如：“全面搜索” |

### 文件分类

DeepRecall 将文件分为以下几类：
- **灵魂文件**（`soul`）：`SOUL.md`, `IDENTITY.md` — 代理的基本信息（始终可见）；
- **思维文件**（`mind`）：`MEMORY.md`, `USER.md`, `TOOLS.md`, `HEARTBEAT.md`, `AGENTS.md` — 提供代理的详细信息；
- **长期记忆文件**（`long-term`）：`memory/LONG_TERM.md` — 包含详细的长期记忆记录；
- **每日日志文件**（`daily-log`）：`memory/YYYY-MM-DD.md` — 每日的原始日志；
- **其他文件**（`workspace`）：工作区中的其他所有文件（包括项目文件和配置文件）。

### 配置

DeepRecall 会自动读取你的 OpenClaw 配置，无需额外配置文件。

### 提供者配置

DeepRecall 会自动从以下位置获取 LLM 提供者的相关信息：
- `~/.openclaw/openclaw.json`：主要模型设置；
- `~/.openclaw/agents/main/agent/models.json`：提供者的基础 URL；
- `~/.openclaw/credentials/`：缓存的用户凭证（例如 GitHub Copilot 的凭证）；
- 环境变量（`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY` 等）（支持 18 种以上提供者，均为可选）。

### 支持的 LLM 提供者（20 多种）

Anthropic · OpenAI · Google (Gemini) · GitHub Copilot · OpenRouter · Ollama · DeepSeek · Mistral · Together · Groq · Fireworks · Cohere · Perplexity · SambaNova · Cerebras · xAI · Minimax · Zhipu (GLM) · Moonshot (Kimi) · Qwen

### 模型自动匹配

- **管理器** 和 **合成步骤** 使用主模型；
- **工作器** 会自动使用更经济的辅助模型：
  | 主模型 | 辅助模型 |
  | --- | --- |
  | Claude Opus 4 / 4.6 | Claude Sonnet 4 |
  | Claude Sonnet 4 / 4.5 | Claude Haiku 3.5 |
  | GPT-4o / GPT-4 | GPT-4o-mini |
  | Gemini 2.5 Pro | Gemini 2.0 Flash |
  | DeepSeek Reasoner | DeepSeek Chat |
  | Llama 3.1 70B | Llama 3.1 8B |

### 配置覆盖

你可以通过 `config_overrides` 参数自定义部分配置：

```python
recall("query", config_overrides={
    "max_files": 5,       # max files manager can select (default: 3)
})
```

## 技能相关文件

- `deep_recall.py`：包含 `recall`, `recall_quick`, `recall_deep` 等函数，以及整个 RLM 循环的实现；
- `provider_bridge.py`：负责从 OpenClaw 配置中解析 LLM 提供者、API 密钥和基础 URL；
- `model_pairs.py`：将主模型与更经济的辅助模型进行映射；
- `memory_scanner.py`：按类别扫描并分类工作区文件；
- `memory_indexer.py`：构建结构化的记忆索引；
- `__init__.py`：包的入口文件。

## 记忆系统架构

以下是符合 “Anamnesis” 架构的推荐工作区文件结构：

```
~/.openclaw/workspace/
├── SOUL.md              # Identity — always in context, never grows
├── IDENTITY.md          # Core agent facts
├── MEMORY.md            # Compact index (~100 lines), auto-loaded each session
├── USER.md              # About the human
├── AGENTS.md            # Agent behavior rules
├── TOOLS.md             # Tool-specific notes
└── memory/
    ├── LONG_TERM.md     # Full memories — grows forever, searched via DeepRecall
    ├── 2026-03-05.md    # Daily raw log
    ├── 2026-03-04.md
    └── ...
```

## 隐私声明

DeepRecall 会读取你的工作区记忆文件，并将其内容发送到你配置的 LLM 提供者（如 Anthropic、OpenAI 等）进行处理。系统没有“仅限本地使用”的模式。

**发送的内容：**
- 文件的元数据（文件名、标题、主题）会被发送到管理器（LLM）；
- 被选中的文件的完整内容会被发送到工作器（LLM）；
- 这可能包括个人笔记、每日日志和项目文件。

**不会发送的内容：**
- API 密钥和凭证（这些信息仅在本地读取用于身份验证，不会被用于外部请求）；
- 工作区之外的文件。

**本地使用的凭证：**
- `~/.openclaw/openclaw.json` 和 `~/.openclaw/credentials/*`：用于获取 LLM 提供者的信息；
- 环境变量（`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY` 等）（在未找到 OpenClaw 配置时作为备用）。

### 推荐的记忆系统架构

DeepRecall 最适合使用 **双层记忆系统**：
- **第一层：MEMORY.md（索引文件）**：每次会话都会自动加载，保持文件大小在 100 行左右，包含快速参考信息、当前项目、关键指标以及指向长期记忆文件的索引。这相当于你的“快速参考手册”；
- **第二层：memory/LONG_TERM.md（百科全书）**：不自动加载，需要时通过 DeepRecall 进行搜索，包含完整的内容、决策过程、时间戳、错误信息及修复方案。这个文件会持续增长，永远保存；
- **第三层：memory/YYYY-MM-DD.md（每日日志）**：记录每天发生的事件，每天结束时会被整合到 `LONG_TERM.md` 中。

### 每日同步流程

每天结束时（或通过定时任务），系统会执行以下操作：
1. 读取当天的日志；
2. 将重要事件、决策、经验教训和错误信息添加到 `LONG_TERM.md` 中；
3. 如果有新主题出现，更新 `MEMORY.md` 的索引。

> ⚠️ **建议：** 在重新组织现有文件之前，请先咨询相关人员。请让他们决定如何管理代理的记忆系统。

## 许可证

DeepRecall 使用 MIT 许可协议。详细信息请参阅 [LICENSE](../LICENSE)。