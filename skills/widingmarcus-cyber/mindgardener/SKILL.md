---
name: mindgardener
description: 专为自主代理设计的“以本地数据为主”的长期记忆系统：该系统从日常日志中提取实体信息，并将其构建为类似维基的知识图谱；通过预测误差来评估事件发生的“意外性”；同时，还会根据代理的“令牌预算”（token budget）来组织相关上下文信息。该系统还具备身份级别的数据整合功能，能够跟踪代理对目标对象的信念变化（belief drift）。整个系统无需依赖任何数据库，仅使用Markdown格式的文件即可实现所有功能。
metadata:
  clawdbot:
    requires:
      bins: ["garden"]
    install:
      - id: mindgardener
        kind: pip
        package: mindgardener
        bins: ["garden"]
        label: "Install MindGardener CLI (pip)"
    env:
      - name: GEMINI_API_KEY
        description: "Google Gemini API key (free tier available). Required unless using Ollama."
        required: false
      - name: OPENAI_API_KEY
        description: "OpenAI API key. Alternative to Gemini."
        required: false
      - name: ANTHROPIC_API_KEY
        description: "Anthropic API key. Alternative to Gemini."
        required: false
---
# MindGardener 🌱

**你的智能助手会忘记所有事情？这可以解决这个问题。**

## 功能介绍

MindGardener 通过读取每日对话记录，为你的智能助手提供持久化的记忆功能：
- **创建一个知识库**：记录人物、项目和公司的信息（每个实体对应一个 `.md` 文件）；
- **构建知识图谱**：利用 `[[wikilinks]]` 和 JSONL 数据结构来表示这些实体之间的关联；
- **智能筛选机制**：只有那些出乎意料的事件才会被保存到长期记忆中；
- **身份识别与更新**：跟踪智能助手对你的认知，并在其信念发生变化时进行更新；
- **上下文管理**：仅加载与当前上下文相关的信息。

无需数据库、服务器或 Docker，所有数据都以 `.md` 文件的形式存储，你可以使用 `grep`、`git diff` 等工具进行查询和编辑，也可以通过 Obsidian 工具进行查看。

## 安装

```bash
pip install mindgardener
garden init
```

（适用于完全本地使用的场景，无需 API 密钥：）

```bash
garden init --provider ollama
```

## 设置步骤

1. 设置你的 LLM（大型语言模型）提供者密钥：
   ```bash
   export GEMINI_API_KEY=your-key  # Free tier: 1500 req/day
   # OR: export OPENAI_API_KEY=your-key
   # OR: export ANTHROPIC_API_KEY=your-key
   # OR: use Ollama (free, local)
   ```

2. 初始化工作空间：
   ```bash
   garden init
   ```

3. 从现有记忆中加载智能助手的模型：
   ```bash
   garden beliefs --bootstrap
   ```

## 命令列表（共 15 条）

### 数据构建（其中 3 条命令需要使用 LLM，其余命令无需）

```bash
garden extract --input memory/2026-02-17.md  # Daily log → entity wiki + graph
garden surprise                                # Score events by prediction error
garden consolidate                             # Promote high-surprise → MEMORY.md
```

### 数据检索（无需使用 LLM）

```bash
garden recall "Kadoa"                          # Search entities + graph
garden context "job search" --budget 4000       # Token-budget-aware assembly
garden evaluate --text "agent output"           # Fact-check against knowledge graph
garden beliefs                                  # View identity model
garden beliefs --drift --apply                  # Detect + apply belief changes
```

### 维护操作

```bash
garden entities              # List all known entities
garden prune --days 30       # Archive inactive entities
garden merge "src" "target"  # Merge duplicates
garden fix type "X" "tool"   # Fix entity type
garden reindex               # Rebuild graph after manual edits
garden viz                   # Mermaid graph visualization
garden stats                 # Quick overview
```

## 每日运行脚本

建议将以下脚本添加到智能助手的 cron 任务中（每天凌晨 3 点执行）：

```bash
garden extract    # Read today's logs → entity wiki
garden surprise   # Score by prediction error
garden consolidate # Promote to MEMORY.md
garden beliefs --drift --apply  # Update identity model
garden prune --days 30          # Archive stale entities
```

## 工作原理

### 实体提取
`garden extract` 命令会读取每日对话记录，并为每个实体生成一个 `.md` 文件，其中包含 `[[wikilinks]]` 以表示实体之间的关联。

```markdown
# Kadoa
**Type:** company

## Facts
- AI web scraping startup (YC W24)

## Timeline
### [[2026-02-16]]
- [[Marcus]] received reply from [[Adrian Krebs]]
```

### 惊奇度评分
通过预测事件的实际结果与预期结果之间的差异来评估事件的“惊喜程度”；差异越大，该事件越值得被记住。

### 身份信息更新
系统会维护一个名为 `memory/self-model.yaml` 的文件，记录智能助手对你的认知情况，并在认知发生变化时进行更新。

`garden beliefs --drift` 命令用于检测当前事件是否改变了这些认知。

### 上下文管理
`garden context "query" --budget 4000` 命令会根据实体的重要性对它们进行评分，并根据 `wikilinks` 选择最相关的信息进行加载；同时会记录哪些信息被加载、哪些被忽略。

## 配置选项

```yaml
# garden.yaml
workspace: /path/to/workspace
memory_dir: memory/
entities_dir: memory/entities/
graph_file: memory/graph.jsonl
long_term_memory: MEMORY.md

extraction:
  provider: google        # google, openai, anthropic, ollama, compatible
  model: gemini-2.0-flash

consolidation:
  surprise_threshold: 0.5
  decay_days: 30
```

## 支持的 LLM 提供者

| 提供者 | 配置方式 | 费用 |
|----------|--------|------|
| Google Gemini | `provider: google` | 提供免费 tier |
| OpenAI | `provider: openai` | 每 100 万个令牌费用为 0.15 美元 |
| Anthropic | `provider: anthropic` | 每 100 万个令牌费用为 0.25 美元 |
| Ollama | `provider: ollama` | 免费（本地使用） |
| 任何兼容 OpenAI 的模型 | `provider: compatible` | 费用因模型而异 |

每日费用：约 0.004 美元（使用 Gemini Flash 模型）；使用 Ollama 模型时费用为 0 美元。

## 隐私与数据传输

**哪些命令会向 LLM 发送数据：**
- `garden extract`：发送每日对话记录 → 接收结构化后的实体信息（通过 LLM 处理）；
- `garden surprise`：发送 `MEMORY.md` 文件和每日对话记录 → 接收事件的新闻度评分（需要两次 LLM 调用）；
- `garden consolidate`：发送高新闻度事件 → 接收 `MEMORY.md` 文件的更新内容（需要一次 LLM 调用）；
- `garden beliefs --bootstrap`：发送 `MEMORY.md` 文件 → 接收智能助手的信念模型（需要一次 LLM 调用）；
- `garden beliefs --drift`：发送智能助手的信念模型和每日对话记录 → 接收认知变化报告（需要一次 LLM 调用）。

**哪些命令是 100% 本地执行的（无需网络连接）：**
- `garden recall`、`garden context`、`garden evaluate`、`garden entities`、`garden prune`、`garden merge`、`garden fix`、`garden reindex`、`garden viz`、`garden stats`、`garden init`。

**完全离线使用方法：** 使用 `garden init --provider ollama`，所有 LLM 调用都在本地完成。

所有数据都以 markdown 文件的形式保存在工作空间中，不会被发送到 MindGardener 的服务器上（因为 MindGardener 本身没有服务器）。

## 链接

- **GitHub 仓库：** https://github.com/widingmarcus-cyber/mindgardener
- **测试结果：** 177 项测试全部通过，耗时不到 3 秒
- **系统要求：** Python 3.10 及以上版本和 PyYAML 库。