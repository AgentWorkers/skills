---
name: aiprox-workflows
description: 在 AIProx 上创建并运行多智能体 AI 工作流。将智能体链接到预定的管道中，并按每次执行的次数计费（单位为 sats）。
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "⚡"
    homepage: https://aiprox.dev/workflows
    requires:
      env:
        - AIPROX_SPEND_TOKEN
---
# AIProx 工作流

AIProx 工作流是一个支持多智能体协作的流程引擎。您可以将多个智能体链接到指定的工作流中，通过 Cron 表达式安排它们的运行时间，并通过电子邮件或 Webhook 接收执行结果。所有服务均按每次执行的实际费用计费（单位：sats），无需订阅或支付月费。

## 使用场景

- 构建包含多个智能体的自动化流程
- 安排重复性任务（例如每日新闻摘要、竞争情报收集、市场信号分析）
- 按需运行一次性的多步骤流程
- 任何需要一个智能体的输出作为下一个智能体输入的工作流

## MCP 工具

### `create_workflow`  
创建一个包含有序智能体步骤的工作流。

```bash
Create a workflow "daily-crypto-brief" that searches Bitcoin news, analyzes sentiment, and emails a summary @daily
```

步骤间的数据传递：使用 `$step1.result`, `$step2.result` 等变量来传递前一个步骤的输出。

**可用功能：**

| 功能        | 功能描述                |
|-------------|----------------------|
| `web-search`    | 通过搜索机器人进行实时网页搜索         |
| `sentiment-analysis` | 通过情感分析机器人分析文本的情绪和语气   |
| `scraping`     | 通过数据爬虫提取网页内容         |
| `data-analysis`    | 通过文档挖掘工具处理和分析数据         |
| `translation`   | 通过多语言翻译工具进行文本翻译       |
| `vision`      | 通过图像分析机器人分析图片/截图        |
| `code-execution` | 通过代码审核工具进行代码安全检查       |
| `email`       | 通过邮件机器人发送通知           |
| `market-data`    | 通过市场预测工具获取市场信号         |
| `token-analysis`   | 通过安全检测工具分析 Solana 代币的安全性     |

### `run_workflow`  
通过工作流的 ID 来触发其执行。

```bash
Run workflow wf_abc123
```

### `list_workflows`  
显示当前可用的所有工作流。

```bash
List my workflows
```

### `get_run_history`  
查看工作流的执行历史记录、消耗的费用以及详细的执行步骤。

```bash
Show run history for wf_abc123
```

### `delete_workflow`  
删除指定的工作流（同时取消已安排的运行任务）。

### `run_template`  
根据模板名称一次性运行预构建的工作流。

```bash
Run the polymarket-signals template and email me at user@example.com
```

## 预构建的模板

| 模板名称      | 所包含的流程                | 费用（sats/次）         |
|-------------|-------------------|-----------------|
| `news-digest`   | search-bot → sentiment-bot → email-bot | 约 150 sats/次       |
| `token-scanner` | data-spider → isitarug → email-bot | 约 120 sats/次       |
| `competitive-intel` | search-bot → doc-miner → sentiment-bot → email-bot | 约 200 sats/次       |
| `multilingual-content` | data-spider → doc-miner → polyglot | 约 180 sats/次       |
| `site-audit`   | vision-bot → code-auditor → doc-miner | 约 220 sats/次       |
| `polymarket-signals` | market-oracle → sentiment-bot → email-bot | 约 160 sats/次       |

## 认证

请在 MCP 服务器配置中设置 `AIPROX_SPEND_TOKEN`。您可以在 [lightningprox.com](https://lightningprox.com) 获取相应的费用令牌。

```json
{
  "mcpServers": {
    "aiprox-workflows": {
      "command": "npx",
      "args": ["aiprox-workflows-mcp"],
      "env": {
        "AIPROX_SPEND_TOKEN": "lnpx_your_token_here"
      }
    }
  }
}
```

## 日程安排

| 缩写          | 执行时间                |
|---------------|----------------------|
| `@hourly`      | 每小时                |
| `@daily`      | 每天午夜                |
| `@weekly`      | 每周日                |
| `0 9 * * 1-5`    | 周一至周五上午 9:00–下午 5:00     |

## 价格政策

每次工作流执行的费用根据所使用的智能体数量而定，范围为 50–220 sats。费用直接从您的 Lightning 费用令牌余额中扣除。

## 行为准则

**当用户请求自动化任务时：**
1. 确定所需的功能（通常为搜索 → 分析 → 通知）
2. 如果有合适的模板，建议使用该模板；否则可提供自定义工作流的创建服务
3. 确认执行时间，并告知用户是否需要定期执行（通过电子邮件或 Webhook）
4. 创建完成后，可立即执行该工作流

**费用透明度：**
- 在创建或执行前明确告知预计费用
- 每次执行后报告实际消耗的费用（sats）

**优先使用模板：**
- 如果任务符合现有模板格式，建议使用 `run_template`，因为它更快捷且已预先配置好。

## 链接资源：
- 仪表板：[aiprox.dev/workflows](https://aiprox.dev/workflows)
- 模板：[aiprox.dev/templates](https://aiprox.dev/templates)
- 服务注册表：[aiprox.dev/registry.html](https://aiprox.dev/registry.html)
- npm SDK：`npm install aiprox-workflows`
- MCP 服务器命令：`npx aiprox-workflows-mcp`