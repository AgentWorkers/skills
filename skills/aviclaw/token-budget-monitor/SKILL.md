---
name: token-budget-monitor
version: "1.0.0"
description: **跟踪并控制 OpenClaw 定时任务中的令牌消耗**
author: aviclaw
tags:
  - token
  - budget
  - monitor
  - openclaw
---
# token-budget-monitor

用于监控和控制在 OpenClaw 定时任务（cron jobs）、备用链（fallback chains）以及会话（sessions）中的令牌（token）消耗情况。

## 安装

```bash
openclaw skills install aviclaw/token-budget-monitor
```

## 使用方法

```bash
# Check current usage
node track-usage.js status

# Check budget for a specific job  
node track-usage.js check daily-tweet

# Alert if over budget
node track-usage.js alert

# Get model recommendations
node track-usage.js recommend
```

## 集成

将该工具添加到定时任务中以监控令牌使用情况：

```javascript
// After LLM call completes
const usage = result.usage;
exec('node /path/to/track-usage.js track <job-name> ' + 
  usage.input_tokens + ' ' + usage.output_tokens + ' ' + model);
```

## 配置

编辑 `config.json` 文件：

```json
{
  "dailyLimit": 100000,
  "jobLimits": {
    "daily-tweet": 5000,
    "rss-brief": 15000
  },
  "alertThreshold": 0.8,
  "freeModels": [
    "nvidia/moonshotai/kimi-k2.5",
    "google/gemini-2.0-flash-exp"
  ]
}
```

## 主要功能

- 支持对每个定时任务进行令牌消耗的跟踪
- 设置每日令牌使用预算限制
- 允许为每个定时任务设置自定义的令牌使用限制
- 当令牌消耗超过预设阈值时触发警报
- 提供免费的模型替代方案作为推荐

## 开发者

- GitHub 账号：@aviclaw

## 许可证

MIT 许可证