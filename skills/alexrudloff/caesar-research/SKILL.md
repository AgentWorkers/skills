---
name: caesar-research
description: 使用 Caesar API 进行深入研究：执行查询、通过聊天进行交流、进行头脑风暴以及管理数据集合。
homepage: https://www.caesar.org/
metadata: { "openclaw": { "emoji": "🔬", "requires": { "bins": ["caesar"], "env": ["CAESAR_API_KEY"] } } }
---
# Caesar Research

这是一个用于 [Caesar](https://www.caesar.org/) 深度研究的命令行工具（CLI）。它可以执行多源研究任务，并提供引用信息、后续聊天功能以及头脑风暴支持。

## 设置

```bash
go install github.com/alexrudloff/caesar-cli@latest
export CAESAR_API_KEY=your_key_here
```

## 研究

执行查询（默认情况下会等待查询完成，同时会在查询过程中实时显示相关事件）：

```bash
caesar research create "What are the latest advances in mRNA vaccines?"
```

查询结果将以 JSON 格式返回，其中包含 `content`（包含 `[n]` 条引用的综合答案）以及一个 `results` 数组（列出所有数据来源）。

执行查询后无需额外操作：

```bash
caesar research create "query" --no-wait
# Returns: { "id": "uuid", "status": "queued" }
```

之后可以查看查询结果：

```bash
caesar research get <job-id>
caesar research watch <job-id>
caesar research events <job-id>
```

### 研究选项

| 标志 | 描述 |
|------|-------------|
| `--no-wait` | 立即返回查询结果及其 ID |
| `--model <name>` | 可选模型：`gpt-5.2`、`gemini-3-pro`、`gemini-3-flash`、`claude-opus-4.5` |
| `--loops N` | 最大推理循环次数（默认值为 1，循环次数越多，研究深度越深） |
| `--reasoning` | 启用高级推理模式 |
| `--auto` | 允许 Caesar 根据查询内容自动配置参数 |
| `--exclude-social` | 排除社交媒体来源 |
| `--exclude-domain x.com` | 排除特定域名（可重复使用） |
| `--system-prompt "..."` | 自定义合成提示语 |
| `--brainstorm <id>` | 使用头脑风暴功能来辅助研究 |

### 状态流转

`queued` → `searching` → `summarizing` → `analyzing` → `researching` → `completed` 或 `failed`

## 聊天（后续问题）

可以对已完成的研究任务提出后续问题：

```bash
caesar chat send <job-id> "How does this compare to traditional vaccines?"
```

默认情况下会等待对方回复；回复内容会包含引用原始研究来源的 `[n]` 条引用。

```bash
caesar chat send <job-id> "question" --wait=false
caesar chat history <job-id>
```

## 头脑风暴

在开始研究之前，可以使用头脑风暴功能来获取更多信息以帮助明确研究方向：

```bash
caesar brainstorm "How does CRISPR gene editing work?"
# Prints questions with multiple-choice options and a session ID
```

之后可以使用头脑风暴的会话 ID 来继续后续操作：

```bash
caesar research create --brainstorm <session-id> "How does CRISPR gene editing work?"
```

## 文件管理

可以将相关文件整理在一起以便于研究：

```bash
caesar collections create "Dataset Name" --description "Optional description"
```

## 使用技巧

- 对于广泛的主题，建议使用 `--auto` 选项让 Caesar 自动选择最佳配置。
- 对于复杂的多方面问题，建议设置 `--loops` 为 3 或更高。
- 对于需要深入分析的问题，可以使用 `--reasoning` 选项。
- 可以使用 `jq` 工具提取输出中的特定字段：`caesar research get <id> | jq '.content'`
- 对于含义模糊的查询，可以先进行头脑风暴，再通过 `caesar research` 进行进一步研究，以获得最佳结果。