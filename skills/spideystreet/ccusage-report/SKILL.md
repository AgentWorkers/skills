---
name: ccusage-report
description: Report Claude Code token consumption and costs using ccusage. Use when the user asks about their Claude Code usage, token consumption, API costs, spending, or wants a daily/weekly/monthly usage summary. Triggers on: "show my claude code usage", "how much did I spend", "my token consumption", "ccusage report", "usage report", "token consumption", "how much did I spend".
metadata: {"openclaw":{"requires":{"bins":["bunx"]}}}
---

# Claude代码使用报告

使用`bunx ccusage`来报告Claude代码会话中的令牌消耗量和费用。

## 工作流程

### 1. 确定期间

根据用户输入的消息确定统计期间：

| 关键词 | 统计期间 | 命令后缀 |
|---------|--------|---------------|
| "today"（默认） | 每日 | `daily` |
| "this week" | 每周 | `weekly` |
| "this month" | 每月 | `monthly` |

### 2. 运行`ccusage`

```json
{ "tool": "exec", "command": "bunx ccusage <period> --no-color -z Europe/Paris -o desc" }
```

如果用户需要按模型详细统计数据，请添加`--breakdown`参数。

**按日期范围过滤：**
- 仅今日：`--since $(date +%Y%m%d) --until $(date +%Y%m%d)`
- 过去7天：`--since $(date -d '7 days ago' +%Y%m%d)`
- 特定月份：`--since 20260201 --until 20260228`

### 3. 格式化输出

```
📊 Claude Code Usage — <period>

Date/Period : <value>
Models      : <comma-separated list>
Input       : <n> tokens
Output      : <n> tokens
Cache read  : <n> tokens
Total       : <n> tokens
Cost        : $<amount> USD
```

对于多行输出（例如过去7天的数据），需要汇总总数并简要列出每一行。

### 4. 传递结果

- **聊天**：直接发送格式化后的消息。
- **Telegram（通过cron任务）**：仅以代码块的形式回复格式化后的消息，不要添加额外说明。

### 5. 错误处理

- 如果`bunx ccusage`执行失败 → 检查`bun/bunx`是否已安装，并报告错误。
- 如果请求的期间没有数据 → 清晰地告知用户（“未找到该期间的使用数据”）。
- 如果输出为空 → 建议用户查看更宽的时间范围。

## 示例

| 用户输入 | 统计期间 | 参数设置 |
|-----------|--------|-------|
| "显示我的Claude代码使用情况" | 每日 | （无参数） |
| “我这周花了多少钱？” | 每周 | （无参数） |
| “包含模型详细信息的月度报告” | 每月 | `--breakdown` |
| “过去7天的使用情况” | 每日 | `--since $(date -d '7 days ago' +%Y%m%d)` |