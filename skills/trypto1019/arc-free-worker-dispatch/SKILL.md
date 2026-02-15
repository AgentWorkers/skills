---
name: free-worker-dispatch
description: 通过 OpenRouter 将任务路由到免费的 AI 模型以节省成本。当代理需要将内容撰写、研究、代码生成等任务委托给更便宜或免费的模型时，可以使用此方法，而无需使用昂贵的主要模型。这样可以避免意外的 API 费用支出。
user-invocable: true
metadata: {"openclaw": {"emoji": "🏭", "os": ["darwin", "linux"], "requires": {"bins": ["python3"], "env": ["OPENROUTER_API_KEY"]}}}
---
# 免费AI模型任务调度

通过OpenRouter将任务委托给免费的AI模型。将您昂贵的高性能模型用于策略制定和质量审核工作，让免费模型来处理繁琐的任务。

## 为什么需要这个功能

使用Claude Opus或GPT-4处理所有任务需要支付费用。而OpenRouter上的免费模型能够很好地完成大部分内容处理、研究和编码任务。该功能能够智能地分配任务，避免代理因意外费用而陷入麻烦。

## 可用的免费模型

| 模型 | 适用场景 | 内容量 |
|-------|----------|---------|
| `stepfun/step-3.5-flash:free` | 研究、分析、头脑风暴 | 128K |
| `arcee-ai/trinity-large-preview:free` | SEO文案撰写、博客文章、市场营销 | 128K |
| `openrouter/free` | 自动选择最适合的免费模型 | 可变 |

## 命令

### 将任务分配给免费模型
```bash
python3 {baseDir}/scripts/dispatch.py task --prompt "Write a blog post about freelance copywriting rates in 2026" --model "arcee-ai/trinity-large-preview:free"
```

### 自动选择模型后分配任务
```bash
python3 {baseDir}/scripts/dispatch.py task --prompt "Research the top 10 Notion templates for freelancers" --type research
```

### 列出可用的免费模型
```bash
python3 {baseDir}/scripts/dispatch.py models
```

### 检查模型状态（是否正常运行）
```bash
python3 {baseDir}/scripts/dispatch.py status --model "stepfun/step-3.5-flash:free"
```

### 将任务结果保存到文件
```bash
python3 {baseDir}/scripts/dispatch.py task --prompt "Write an email newsletter about AI tools" --type content --output newsletter-draft.md
```

### 批量分配任务（多个任务）
```bash
python3 {baseDir}/scripts/dispatch.py batch --file tasks.json
```

## `tasks.json` 文件格式
```json
[
  {"prompt": "Write a product description", "type": "content"},
  {"prompt": "Research competitor pricing", "type": "research"},
  {"prompt": "Generate a Python script for...", "type": "code"}
]
```

## 任务类型

`--type` 标志会自动选择最适合的免费模型：

| 类型 | 模型 | 适用原因 |
|------|-------|-----|
| `research` | `stepfun/step-3.5-flash:free` | 处理速度快，分析能力强 |
| `content` | `arcee-ai/trinity-large-preview:free` | 写作能力强大 |
| `code` | `openrouter/free` | 自动分配给最合适的编码模型 |
| `general` | `openrouter/free` | 由OpenRouter自行决定 |

## 输出结果

默认情况下，任务结果会输出到标准输出（stdout）。使用 `--output <文件路径>` 可将结果保存到文件中；使用 `--json` 可获得包含所使用模型、处理时间和相关数据的结构化JSON输出。

## 使用提示：

- 在发布内容前，请务必审核模型的输出结果——免费模型可能会产生不准确的输出。
- 使用 `--type` 标志来自动选择最适合的模型，而不是直接指定模型。
- 对于多个独立的任务，批量分配任务会更高效。
- 如果某个模型无法正常运行，脚本会自动切换到 `openrouter/free` 模型进行处理。