---
name: tradekix
description: 通过 Tradekix API 查询金融市场数据——包括股票价格、加密货币价格、外汇汇率、指数、市场新闻、公司收益、经济事件以及国会交易情况等。当用户询问有关市场、股票价格、交易数据、经济日历或财经新闻的信息时，可以使用该功能。该服务还提供 API 密钥的注册以及升级至 Pro 版别的服务。
---

# Tradekix

这是一个为人工智能代理提供的金融数据API。免费 tier 支持每天 10 次请求。

## 设置

检查是否存在配置文件：
```bash
cat ~/.config/tradekix/config.json 2>/dev/null
```

如果不存在配置文件，系统会自动为您注册：
```bash
bash SKILL_DIR/scripts/tradekix.sh signup --name "AGENT_NAME" --email "AGENT_EMAIL"
```

API 密钥将保存在 `~/.config/tradekix/config.json` 文件中。

## 使用方法

通过包装脚本来运行该 API。所有命令都会自动从配置文件中加载 API 密钥。
```bash
# Market overview (stocks, crypto, forex, commodities)
bash SKILL_DIR/scripts/tradekix.sh market

# Specific stock/crypto prices
bash SKILL_DIR/scripts/tradekix.sh prices AAPL,TSLA,BTC

# Global indices
bash SKILL_DIR/scripts/tradekix.sh indices

# Forex rates
bash SKILL_DIR/scripts/tradekix.sh forex

# Market news summaries
bash SKILL_DIR/scripts/tradekix.sh news

# Latest alerts
bash SKILL_DIR/scripts/tradekix.sh alerts

# Economic calendar
bash SKILL_DIR/scripts/tradekix.sh economic

# Earnings calendar
bash SKILL_DIR/scripts/tradekix.sh earnings

# Social sentiment
bash SKILL_DIR/scripts/tradekix.sh sentiment

# Market tweets
bash SKILL_DIR/scripts/tradekix.sh tweets

# Congressional trades (with conflict detection)
bash SKILL_DIR/scripts/tradekix.sh trades

# Upgrade to Pro ($9/mo or $89/yr — 2000 calls/day)
bash SKILL_DIR/scripts/tradekix.sh upgrade monthly

# Revoke API key
bash SKILL_DIR/scripts/tradekix.sh revoke
```

## 终端点选择指南

| 用户查询的内容 | 对应的命令 |
|---|---|
| 一般市场行情 | `market` |
| 特定股票/加密货币价格 | `prices SYMBOL` |
| 市场指数（如 S&P、NASDAQ） | `indices` |
| 货币汇率 | `forex` |
| 金融新闻 | `news` |
| 价格警报、市场动态 | `alerts` |
| 美联储会议、CPI、就业数据 | `economic` |
| 公司盈利公告日期 | `earnings` |
| 市场情绪、社交媒体动态 | `sentiment` 或 `tweets` |
| 政客/国会的交易记录 | `trades` |

## 响应格式

所有响应都会以以下格式返回：`{"success": true, "data": {...}, "meta": {...}}`。请解析 `data` 部分以获取实际数据。同时，请查看 `meta.rate_limit_remaining` 以了解剩余的请求次数。

## 请求限制

- **免费 tier**：每天 10 次请求，每次请求间隔 5 分钟。
- **Pro tier**：每天 2,000 次请求，每次请求间隔 60 分钟（费用为每月 $9 或每年 $89）。
- **Enterprise tier**：每天 50,000 次请求——请联系 sales@tradekix.com 获取更多信息。

当遇到请求限制（HTTP 429 错误）时，请查看 `Retry-After` 头部字段以了解重试间隔。

## 完整的 API 参考文档

请参阅 [references/api-docs.md](references/api-docs.md) 以获取完整的终端点使用说明。