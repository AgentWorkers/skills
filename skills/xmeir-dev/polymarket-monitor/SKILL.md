---
name: polymarket-monitor
description: 监控 Polymarket 的预测市场，并在赔率超过设定阈值时发出警报。适用于用户需要跟踪 Polymarket 上任何市场的概率、设置定期价格检查，或在某个市场的“是/否”概率超过特定百分比时接收通知的场景。该功能支持按主题搜索市场、获取当前赔率，并可通过 Slack 或其他渠道设置基于 Cron 表达式的警报。
---
# Polymarket 监控器

为 Polymarket 的任何预测市场设置持续监控，并在达到预设阈值时发送警报。

## 工作流程

### 1. 查找目标市场

使用 Gamma API 搜索与用户感兴趣的主题匹配的活跃市场：

```bash
curl "https://gamma-api.polymarket.com/events?search=<topic>&limit=10&active=true"
```

解析响应以获取相关市场信息。对于每个市场，请记录以下信息：
- `conditionId`：用于获取市场价格的标识符
- `question`：市场名称
- `outcomePrices`：当前的“是/否”概率（以 JSON 字符串形式表示）

有关完整的 API 详情，请参阅 `references/api.md`。

### 2. 检查当前概率

使用提供的脚本获取一个或多个市场的当前价格：

```bash
python3 scripts/check_markets.py <conditionId1> [conditionId2 ...]
```

输出结果应为包含每个市场的 `question`、`yes_prob`（0–1 的浮点数）和 `url` 的 JSON 数据。

### 3. 显示当前状态

在设置监控之前，向用户展示找到的市场及其当前的概率。

### 4. 设置 Cron 警报

创建一个每 N 分钟运行一次的 Cron 作业（默认值为 30 分钟），设置 `sessionTarget: "isolated"` 和 `payload.kind: "agentTurn"`。该作业应执行以下操作：
1. 通过 Gamma API 的 `conditionId` 端点获取每个市场的数据。
2. 将 `outcomePrices[0]` 解析为“是”的概率。
3. 如果有任何市场超过预设阈值，通过 `message` 工具向指定的 Slack 账号发送警报（频道：slack，目标用户：<user_id>）。
4. 如果没有任何市场超过阈值，则不执行任何操作。

使用 `delivery.mode: "none"` 来禁用默认的 Cron 通知方式——警报由代理程序自行处理。

**Cron 作业消息模板：**

```
Check these Polymarket markets. For each, fetch:
  https://clob.polymarket.com/markets/<conditionId>
Parse tokens array: find outcome=="Yes" and use its price as probability (0–1).
If any exceeds <threshold> (e.g. 0.70):
  Send Slack DM to <user_slack_id> with: market question, current %, and Polymarket URL.
If none exceed threshold, do nothing.

Markets:
- <question>: https://clob.polymarket.com/markets/<conditionId> | https://polymarket.com/event/<slug>
```

### 5. 确认设置完成

向用户告知以下信息：
- 被监控的市场列表
- 每个市场的当前概率
- 警报阈值及检查频率
- 取消监控的方法（Cron 作业 ID + `cron remove <id>`）

## 注意事项：
- Polymarket 没有专门的“今日”市场——请使用最近到期的市场作为短期信号来源。
- `outcomePrices` 的值始终为 `["yes", "no"]`，其中第一个值表示“是”。
- 已关闭的市场返回的价格为 0 或 1，请跳过这些市场。
- 无需使用 API 密钥。