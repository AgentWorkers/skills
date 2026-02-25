---
name: crypto-signal
description: 来自50多个Telegram群组的AI驱动的加密情报服务：通过API获取热门话题、早期市场信号、大额交易警报以及市场情绪数据。提供免费试用版本。
---
# 加密信号服务

该服务利用人工智能从 Telegram 群组中实时提取加密市场情报。

## 设置

1. 在 [https://api.qtxh.top](https://api.qtxh.top) 获取免费的 API 密钥（或请求机器人为您创建一个）。
2. 设置环境变量：

```bash
export CRYPTOSIGNAL_API_KEY="cs_your_key_here"
```

或者将其添加到您的 OpenClaw 配置文件中：

```yaml
env:
  CRYPTOSIGNAL_API_KEY: "cs_your_key_here"
```

## 命令

所有命令均通过 `crypto-signal` CLI 来执行：

### 获取热门话题（过去 24 小时）
```bash
crypto-signal trending
crypto-signal trending --hours 12
```

### 获取 “alpha 信号”（早期市场趋势信号）
```bash
crypto-signal signals
crypto-signal signals --type whale_transfer
crypto-signal signals --type price_move --limit 10
```

### 列出被监控的 Telegram 群组
```bash
crypto-signal groups
```

### 检查服务状态
```bash
crypto-signal status
```

## 信号类型

| 类型 | 描述 |
|------|-------------|
| `whale_transfer` | 大额代币转账（金额超过 100 万） |
| `price_move` | 显著的价格波动 |
| `liquidation` | 大规模清算事件 |
| `regulatory` | 美国证券交易委员会（SEC）/商品期货交易委员会（CFTC）等监管机构的新闻 |
| `security` | 系统漏洞、黑客攻击等安全事件 |
| `listing` | 代币在交易所的上市/退市信息 |
| `airdrop` | 代币空投活动 |
| `partnership` | 重大合作伙伴关系公告 |

## 服务套餐

| 功能 | 免费 | 专业版（每月 $1） |
|---------|------|-------------|
| 监控的 Telegram 群组数量 | 3 | 50 个以上 |
| 每日 API 调用次数 | 10 次 | 无限制 |
| 信号延迟时间 | 6 小时 | 实时 |
| 自定义监控群组 | 不支持 | 支持（最多 20 个群组） |
| 历史数据查询与搜索 | 不支持 | 支持 |
| Webhook 推送 | 不支持 | 支持 |

## OpenClaw 使用示例

- 对你的代理说：“今天加密市场的热门话题是什么？” → 输入 `crypto-signal trending`
- “过去 12 小时内有大额代币转账的警报吗？” → 输入 `crypto-signal signals --type whale_transfer --hours 12`
- “显示最新的 ‘alpha 信号’” → 输入 `crypto-signal signals`