---
name: xerolite
description: "将 OpenClaw 与 Xerolite 交易平台集成。使用场景包括：查询 Xerolite API、下订单、搜索合约以及处理 Xerolite 的 Webhook 事件。"
metadata: {"openclaw":{"requires":{"bins":["node"]}}}
---
# Xerolite

Xerolite 是一个将 TradingView 数据传输到经纪商（IB）的交易平台。  
通过该功能，代理可以下订单、搜索合约，并通过 OpenClaw 接收来自 Xerolite 的 Webhook 消息。

## 设置

### 安装

安装 `transforms` 模块并配置 Webhook 端点：

```bash
bash skills/xerolite/scripts/install.sh
```

### 卸载

卸载 `transforms` 模块并清除 Webhook 配置：

```bash
bash skills/xerolite/scripts/uninstall.sh
```

## 包结构

```
skills/xerolite/
├── SKILL.md              # This file
├── transforms/
│   └── xerolite.js       # Webhook payload transformer
├── scripts/
│   ├── xerolite.mjs      # CLI (order place, contract search)
│   ├── install.sh        # Setup script
│   └── uninstall.sh      # Removal script
└── references/
    ├── API.md            # REST API guide
    └── WEBHOOKS.md       # Webhook configuration
```

## 功能

- 通过 Xerolite 的 REST API 下单。
- 通过 Xerolite 的 REST API 搜索合约。
- 接收 `/hooks/xerolite` Webhook 并将其格式化为可读的通知。

## 命令

请从技能目录中使用这些命令（或在其他技能中通过 `{baseDir}` 来使用它们）。

**默认参数值**（可选；如未指定则使用默认值）：`--currency USD`、`--asset-class STOCK`、`--exch SMART`。

### 下单

必需参数：`--action`、`--qty`、`--symbol`。可选参数：`--currency`、`--asset-class`、`--exch`。

```bash
# Minimal (defaults: USD, STOCK, SMART)
node {baseDir}/scripts/xerolite.mjs order place --symbol AAPL --action BUY --qty 10

# Full
node {baseDir}/scripts/xerolite.mjs order place \
  --symbol AAPL \
  --currency USD \
  --asset-class STOCK \
  --exch SMART \
  --action BUY \
  --qty 10
```

发送到 `POST /api/internal/agent/order/place-order` 的 JSON 数据：

```json
{
  "name": "Agent",
  "action": "BUY",
  "qty": "10",
  "symbol": "AAPL",
  "currency": "USD",
  "asset_class": "STOCK",
  "exch": "SMART"
}
```

### 搜索合约

必需参数：`--symbol`。可选参数：`--currency`、`--asset-class`、`--exch`。

```bash
# Minimal (defaults: USD, STOCK, SMART)
node {baseDir}/scripts/xerolite.mjs contract search --symbol AAPL

# Full
node {baseDir}/scripts/xerolite.mjs contract search \
  --symbol AAPL \
  --currency USD \
  --asset-class STOCK \
  --exch SMART
```

发送到 `POST /api/internal/agent/contract/search` 的 JSON 数据：

```json
{
  "brokerName": "IBKR",
  "symbol": "AAPL",
  "currency": "USD",
  "xeroAssetClass": "STOCK"
}
```

## Webhook

安装完成后，OpenClaw 会监听 `/hooks/xerolite` 路径。

### 工作原理

`transforms` 模块（`xerolite.js`）会将接收到的数据格式化为结构清晰的可读通知。

### Xerolite 配置

配置 Xerolite 以发送 Webhook：
- **URL**：`https://your-openclaw-host:18789/hooks/xerolite`
- **方法**：POST
- **请求头**：`Authorization: Bearer <your-hooks-token>`
- **内容类型**：`application/json`

### 数据格式

`transforms` 模块支持多种数据格式：

```json
{"event": "order.created", "data": {"id": "123", "total": 99.99}}
```

```json
{"message": "Server restarted", "level": "info"}
```

输出示例：
```
📥 **Xerolite Notification**

**Event:** order.created
**Data:**
  • id: 123
  • total: 99.99
```

## REST API

有关此技能使用的订单和合约搜索端点的详细信息，请参阅 [references/API.md](references/API.md)。

## Transform 模块

`transforms/xerolite.js` 模块负责以下任务：
- 将接收到的数据格式化为结构清晰的形式。
- 提取事件/消息/数据字段。
- 自动将数据发送到配置的通道。
- 支持直接转发数据（无需重新格式化）。

如需自定义 `transforms/xerolite.js`，请在安装前对其进行修改。

## 系统要求

- Node.js 18 及更高版本（内置 `fetch` 功能）。
- 必须启用 OpenClaw 的 Webhook 功能。
- **仅限 CLI 使用**：可选参数 `XEROLITE_API_URL` — Xerolite API 的基础 URL。如果未设置，默认为 `http://localhost`（同一台机器或局域网）。当前版本不支持 API 密钥；未来版本可能会添加此功能。

## 故障排除

### Webhook 未接收
- 确认 `openclaw` 配置中已设置 `hooks.token`。
- 检查 Xerolite 是否正确设置了 `Authorization: Bearer <token>` 请求头。
- 确认安装后 Gateway 已重新启动。

### 401 Unauthorized 错误
- 令牌不匹配 — 确认 Xerolite 使用的令牌与 `hooks.token` 一致。

### Transform 模块无法工作
- 检查 `transforms/xerolite.js` 文件是否位于 `~/.openclaw/hooks/transforms` 目录下。
- 重新运行 `install.sh` 以更新 `transforms` 模块。
- 查看 Gateway 的日志以获取错误信息。