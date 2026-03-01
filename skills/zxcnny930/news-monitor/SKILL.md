---
name: buzz
description: 实时新闻聚合器，支持通过 Discord 和 Telegram 发送推送通知。可通过 REST API 管理 Jin10、BlockBeats、RSS 源、X 知名博主（KOLs）、Polymarket 和 OpenNews 等内容来源。
version: 1.0.0
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
    emoji: "\U0001F4F0"
    os:
      - darwin
      - linux
      - win32
---
# Buzz Skill

这是一个实时新闻聚合器，支持通过 Discord 和 Telegram 发送推送通知。所有配置均通过 REST API 进行管理，并支持热重载功能——无需重启服务器。

**基础 URL**: `http://localhost:3848`（默认值，可通过 `dashboard.port` 配置）

## 快速设置

```bash
git clone https://github.com/zxcnny930/buzz.git
cd buzz
npm install
cp config.example.json config.json
npm start
```

控制面板位于 `http://localhost:3848`，设置页面位于 `/settings.html?lang=en`。

## 认证

如果设置了控制面板密码，则所有 `/api/*` 端点都需要添加 `?pw=PASSWORD` 参数：

```bash
curl -s "http://localhost:3848/api/config?pw=YOUR_PASSWORD"
```

如果密码为空，则无需认证。

**注意：** 下面的所有 `curl` 示例为了简洁省略了 `?pw=` 参数。如果服务器配置了密码，请在每个 URL 后添加 `?pw=PASSWORD`。

**认证失败响应（HTTP 401）**:

```json
{ "ok": false, "error": "Unauthorized" }
```

---

## API 端点

### 1. 获取当前配置

```bash
curl -s http://localhost:3848/api/config
```

返回完整的配置 JSON 数据。敏感字段（`apiKey`、`token`、`botToken`、`password`）在响应中会被替换为 `"••••••"`。

### 2. 更新配置（部分更新，支持热重载）

`POST /api/config` 支持部分配置更新。只需发送需要修改的部分即可。

**启用 Jin10 功能（轮询间隔 10 秒）**:

```bash
curl -s -X POST http://localhost:3848/api/config \
  -H "Content-Type: application/json" \
  -d '{"jin10": {"enabled": true, "pollIntervalMs": 10000}}'
```

**禁用 Polymarket 功能**:

```bash
curl -s -X POST http://localhost:3848/api/config \
  -H "Content-Type: application/json" \
  -d '{"polymarket": {"enabled": false}}'
```

**设置 Discord Webhook**:

```bash
curl -s -X POST http://localhost:3848/api/config \
  -H "Content-Type: application/json" \
  -d '{"discord": {"webhookUrl": "https://discord.com/api/webhooks/..."}}'
```

**启用 Telegram 功能**:

```bash
curl -s -X POST http://localhost:3848/api/config \
  -H "Content-Type: application/json" \
  -d '{"telegram": {"enabled": true, "botToken": "123456:ABC-DEF", "chatId": "-1001234567890"}'
```

**添加 RSS 源**:

```bash
curl -s -X POST http://localhost:3848/api/config \
  -H "Content-Type: application/json" \
  -d '{"rssFeeds": [{"enabled": true, "name": "CoinDesk", "feedUrl": "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml", "pollIntervalMs": 300000, "color": 3447003}']'
```

> 注意：`rssFeeds` 是一个数组——发送该请求会替换整个数组，而不是仅添加新元素。

**配置 OpenNews AI 过滤规则**:

```bash
curl -s -X POST http://localhost:3848/api/config \
  -H "Content-Type: application/json" \
  -d '{"opennews": {"enabled": true, "pollIntervalMs": 60000, "minScore": 70, "signals": ["long"], "coins": ["BTC", "ETH"], "engineTypes": ["news", "listing"]}'
```

**配置 Polymarket 警报规则**:

```bash
curl -s -X POST http://localhost:3848/api/config \
  -H "Content-Type: application/json" \
  -d '{"polymarket": {"enabled": true, "minChangePp": 5, "zThreshold": 2.5, "volSpikeThreshold": 2.0, "minLiquidity": 10000, "tagIds": [21, 120], "excludeTagIds": [100639]}'
```

**设置 AI 翻译模型**:

```bash
curl -s -X POST http://localhost:3848/api/config \
  -H "Content-Type: application/json" \
  -d '{"grok": {"apiKey": "xai-...", "model": "grok-4.1-fast", "baseUrl": "https://api.x.ai/v1"}'
```

**成功响应**:

```json
{ "ok": true }
```

**验证失败响应**:

```json
{
  "ok": false,
  "errors": ["polymarket.zThreshold must be > 0", "dashboard.port must be 1024-65535"]
}
```

### 3. 获取源状态

```bash
curl -s http://localhost:3848/api/status
```

响应示例：

```json
{
  "jin10": { "active": true, "interval": 15000 },
  "blockbeats": { "active": true, "interval": 30000 },
  "polymarket": { "active": true, "interval": 180000 },
  "x6551": { "active": true, "interval": 3600000 },
  "opennews": { "active": false, "interval": 60000 },
  "rss:https://www.blocktempo.com/feed/": { "active": true, "interval": 300000 }
}
```

每个键代表一个新闻源的标识符。RSS 源的名称前会加上 `rss:`。

### 4. 管理 KOL 跟踪列表

**列出所有被跟踪的账号**:

```bash
curl -s -X POST http://localhost:3848/api/kols \
  -H "Content-Type: application/json" \
  -d '{"action": "list"}
```

响应示例：

```json
{ "ok": true, "kols": ["elonmusk", "VitalikButerin"]
```

**添加一个 KOL**:

```bash
curl -s -X POST http://localhost:3848/api/kols \
  -H "Content-Type: application/json" \
  -d '{"action": "add", "username": "caboronli"}
```

响应示例：

```json
{ "ok": true, "kols": ["elonmusk", "VitalikButerin", "caboronli"]
```

如果账号已存在：

```json
{ "ok": true, "message": "already exists", "kols": ["elonmusk", "VitalikButerin", "caboronli"]
```

**删除一个 KOL**:

```bash
curl -s -X POST http://localhost:3848/api/kols \
  -H "Content-Type: application/json" \
  -d '{"action": "remove", "username": "elonmusk"}
```

响应示例：

```json
{ "ok": true, "kols": ["VitalikButerin", "caboronli"]
```

如果用户名不存在：

```json
{ "ok": false, "error": "not found", "kols": ["VitalikButerin", "caboronli"]
```

> 用户名字符串会自动去除前缀 `@`。

### 5. 健康检查

```bash
curl -s http://localhost:3848/health
```

响应示例：

```json
{ "ok": true, "clients": 2, "history": 150 }
```

- `clients`: 活跃的 SSE 连接数
- `history`: 内存中的事件数量

无需认证。

### 6. 服务器发送的事件（实时流）

```bash
curl -s -N http://localhost:3848/sse
```

该接口以 SSE 格式发送实时新闻事件。连接建立时会先发送所有历史事件，随后新事件会实时推送。每 15 秒发送一次心跳信号。

---

## 完整配置规范

### jin10

| 字段 | 类型 | 默认值 | 验证规则 | 描述 |
|-------|------|---------|------------|-------------|
| `enabled` | boolean | `true` | | 启用 Jin10 闪现新闻 |
| `pollIntervalMs` | number | `15000` | >= 5000 | 轮询间隔（毫秒） |
| `onlyImportant` | boolean | `true` | | 仅推送重要事件 |

### blockbeats

| 字段 | 类型 | 默认值 | 验证规则 | 描述 |
|-------|------|---------|------------|-------------|
| `enabled` | boolean | `true` | | 启用 BlockBeats 功能 |
| `pollIntervalMs` | number | `30000` | >= 5000 | 轮询间隔 |
| `onlyImportant` | boolean | | 仅推送重要事件 |
| `lang` | string | `"cht"` | | 语言（`cht`：繁体中文，`en`：英文，`cn`：简体中文） |

### rssFeeds（数组）

| 字段 | 类型 | 默认值 | 验证规则 | 描述 |
|-------|------|---------|------------|-------------|
| `enabled` | boolean | `true` | | 启用该 RSS 源 |
| `name` | string | | | 显示名称 |
| `feedUrl` | string | | 必须以 `http(s)://` 开头 | RSS/Atom 源地址 |
| `pollIntervalMs` | number | `300000` | >= 5000 | 轮询间隔 |
| `color` | number | | | Discord 嵌入颜色（整数格式，例如 `3447003` 表示 `#3498DB` |

### x6551

| 字段 | 类型 | 默认值 | 验证规则 | 描述 |
|-------|------|---------|------------|-------------|
| `enabled` | boolean | | 启用 X Twitter 监控功能 |
| `apiBase` | string | `"https://ai.6551.io"` | 必须以 `http(s)://` 开头 | API 基础地址 |
| `token` | string | | | 来自 [6551.io/mcp](https://6551.io/mcp) 的 API 密钥 |
| `pollIntervalMs` | number | `3600000` | >= 5000 | 轮询间隔 |
| `kolSyncIntervalMs` | number | `300000` | | KOL 列表刷新间隔 |
| `kols` | string[] | | 需要监控的用户名（不包含 `@` 前缀） |

### opennews

| 字段 | 类型 | 默认值 | 验证规则 | 描述 |
|-------|------|---------|------------|-------------|
| `enabled` | boolean | `false` | | 启用 OpenNews AI 新闻功能 |
| `pollIntervalMs` | number | `60000` | >= 5000 | 轮询间隔 |
| `minScore` | number | `70` | 最小 AI 分数阈值 |
| `signals` | string[] | | 过滤条件（例如：`"long"` 表示长期趋势，`"short"` 表示短期趋势） |
| `coins` | string[] | | 过滤条件（例如：`["BTC", "ETH"]` 表示仅显示特定加密货币的新闻） | **仅适用于 OpenNews** |
| `engineTypes` | string[] | | 过滤条件（例如：`"news"` 表示新闻，`"listing"` 表示市场动态） | **仅适用于 OpenNews** |

### polymarket

| 字段 | 类型 | 默认值 | 验证规则 | 描述 |
|-------|------|---------|------------|-------------|
| `enabled` | boolean | | 启用 Polymarket 监控功能 |
| `pollIntervalMs` | number | `180000` | >= 5000 | 价格检查间隔 |
| `marketRefreshMs` | number | `600000` | 市场列表刷新间隔 |
| `minChangePp` | number | `5` | 最小价格变化百分比阈值 |
| `zThreshold` | number | `2.5` | Z-Score 异常阈值 |
| `volSpikeThreshold` | number | `2.0` | 价格波动阈值 |
| `minLiquidity` | number | `10000` | 最小市场流动性（美元） |
| `rollingWindowMinutes` | number | `30` | 价格变化计算窗口时间 |
| `cooldownMs` | number | `900000` | 重复警报前的最小间隔时间 |
| `tagIds` | number[] | | 需要跟踪的标签 ID（数组） |
| `excludeTagIds` | number[] | | 需要排除的标签 ID |

**Polymarket 标签 ID**:

| ID | 类别 |
|----|----------|
| 21 | 加密货币 |
| 2 | 政治 |
| 120 | 金融 |
| 1401 | 科技 |
| 596 | 文化 |
| 100265 | 地缘政治 |
| 100639 | 体育 |

### grok（AI 翻译）

| 字段 | 类型 | 默认值 | 验证规则 | 描述 |
|-------|------|---------|------------|-------------|
| `apiKey` | string | | 翻译 API 密钥 |
| `model` | string | `"grok-4.1-fast"` | | 可用的 OpenAI 模型 |
| `baseUrl` | string | `"https://api.x.ai/v1"` | 必须以 `http(s)://` 开头 | API 端点 |

支持的模型：`grok-4.1-fast`、`gpt-4o-mini`、`gpt-4.1-mini`、`claude-sonnet-4-6`、`claude-haiku-4-5-20251001`、`gemini-2.0-flash` 或其他兼容 OpenAI 的模型。

### discord

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `webhookUrl` | string | `""` | Discord Webhook URL（简单模式） |
| `botToken` | string | `""` | Discord 机器人令牌（高级模式） |
| `channelId` | string | `""` | Discord 频道 ID（机器人模式必需） |

**使用方式**:

- 可以使用 `webhookUrl` 或 `botToken` + `channelId`，但不能同时使用两者。

### telegram

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `enabled` | boolean | `false` | 启用 Telegram 通知 |
| `botToken` | string | `""` | Telegram 机器人令牌 |
| `chatId` | string | `""` | 目标聊天/群组/频道 ID |

### 控制面板

| 字段 | 类型 | 默认值 | 验证规则 | 描述 |
|-------|------|---------|------------|-------------|
| `port` | number | `3848` | 1024-65535 | HTTP 服务器端口（需要重启服务器） |
| `password` | string | `""` | | 访问密码（默认为空，表示无需认证 |

---

## 常用操作流程

### 检查当前运行的服务

```bash
curl -s http://localhost:3848/api/status | jq 'to_entries[] | select(.value.active) | .key'
```

### 启用一个新闻源并验证其是否已启用

```bash
# 启用 Jin10 功能
curl -s -X POST http://localhost:3848/api/config \
  -H "Content-Type: application/json" \
  -d '{"jin10": {"enabled": true, "pollIntervalMs": 15000}}'

# 验证其是否已启用
curl -s http://localhost:3848/api/status | jq '.jin10'
```

### 设置 Discord 和 Telegram 双重推送通知

```bash
curl -s -X POST http://localhost:3848/api/config \
  -H "Content-Type: application/json" \
  -d '{
    "discord": {"webhookUrl": "https://discord.com/api/webhooks/..."},
    "telegram": {"enabled": true, "botToken": "123456:ABC-DEF", "chatId": "-1001234567890"}
}
```

### 添加新的 RSS 源（不会覆盖现有源）

**注意**: `rssFeeds` 是一个数组。发送请求会替换整个数组。首先需要获取当前列表，然后添加新元素后再发送更新后的数组。

**步骤 1：获取当前 RSS 源列表**:

```bash
curl -s http://localhost:3848/api/config | jq '.rssFeeds'
```

**步骤 2：发送包含新元素的数组**:

```bash
# 示例：现有源为 BlockTempo 和 PTS News，添加 CoinDesk
curl -s -X POST http://localhost:3848/api/config \
  -H "Content-Type: application/json" \
  -d '{"rssFeeds": [
    {"enabled": true, "name": "BlockTempo", "feedUrl": "https://www.blocktempo.com/feed/", "pollIntervalMs": 300000, "color": 16746496"},
    {"enabled": true, "name": "PTS News", "feedUrl": "https://news.pts.org.tw/xml/newsfeed.xml", "pollIntervalMs": 300000, "color": 3447003"},
    {"enabled": true, "name": "CoinDesk", "feedUrl": "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml", "pollIntervalMs": 300000, "color": 2067276"}
  ]
}
```

**删除 RSS 源**:

首先获取当前列表，然后删除目标源，再发送剩余的数组：

```bash
# 获取当前 RSS 源列表
curl -s http://localhost:3848/api/config | jq '.rssFeeds'
# 删除目标源
curl -s http://localhost:3848/api/config | jq '.rssFeeds'
# 发送更新后的数组
curl -s -X POST http://localhost:3848/api/config \
  -H "Content-Type: application/json" \
  -d '{"rssFeeds": [
    {"enabled": true, "name": "BlockTempo", "feedUrl": "https://www.blocktempo.com/feed/", "pollIntervalMs": 300000, "color": 16746496"}
]
```

### 向任何数组字段添加元素（通用方法）

当用户要求添加新元素时，需要先获取当前值，再进行修改后再发送：

**步骤 1：获取当前值**
```bash
CURRENT=$(curl -s http://localhost:3848/api/config | jq '.polymarket.tagIds')
# 示例输出: [21, 120]
```

**步骤 2：添加新元素并发送**
```bash
# 例如：向现有列表中添加 Sports（100639）
curl -s -X POST http://localhost:3848/api/config \
  -H "Content-Type: application/json" \
  -d '{"polymarket": {"tagIds": [21, 120, 100639]}
```

同样的方法也适用于 `opennews.signals`、`opennews.coins`、`opennews.engineTypes`、`polymarket.excludeTagIds`。

### 仅跟踪高影响力的加密货币新闻

```bash
curl -s -X POST http://localhost:3848/api/config \
  -H "Content-Type: application/json" \
  -d '{"opennews": {"enabled": true, "minScore": 80, "signals": ["long", "short"], "coins": ["BTC", "ETH", "SOL"], "engineTypes": ["news", "listing"]}'
```

### 跟踪新的 KOL 并验证

**添加新 KOL**:

```bash
curl -s -X POST http://localhost:3848/api/kols \
  -H "Content-Type: application/json" \
  -d '{"action": "add", "username": "VitalikButerin"}
```

**列出所有 KOL**:

```bash
curl -s -X POST http://localhost:3848/api/kols \
  -H "Content-Type: application/json" \
  -d '{"action": "list"}
```

---

**重要规则**

- 数组字段会被替换，永远不会合并。配置更新时只会替换数组中的具体元素。如果用户想要向现有列表中添加元素，必须先获取当前配置，修改数组后再发送。

**需要先获取数据的数组字段**:

| 字段 | 添加示例 |
|-------|---------------------|
| `rssFeeds` | 添加 CoinDesk RSS 源 — 先获取当前列表，再添加新元素 |
| `polymarket.tagIds` | 添加 Sports — 先获取当前标签 ID，再添加 `100639` |
| `polymarketexcludeTagIds` | 排除 Culture — 先获取当前标签 ID，再添加 `100639` |
| `opennewssignals` | 显示长期趋势信号 — 先获取当前信号列表，再添加 `"long"` |
| `opennews.coins` | 添加 SOL — 先获取当前支持的加密货币，再添加 `"SOL"` |
| `opennews.engineTypes` | 添加市场动态 — 先获取当前支持的类型，再添加 `"listing"` |

**例外情况：** KOL 的更新可以通过 `POST /api/kols` 和 `action: "add"` 或 `action: "remove"` 来完成，无需先获取数据。**请勿通过 `POST /api/config` 来修改 `x6551.kols`。**

**当用户要求“设置为”（替换整个列表）而不是“添加”时**，可以直接发送请求，无需先获取数据。例如：`{"polymarket": {"tagIds": [21, 120]}`。

**其他规则**:

1. 数组字段支持部分更新。例如：可以仅发送 `{"jin10": {"enabled": false}` 而不影响其他字段。
2. 敏感字段在获取响应时会被替换为 `"••••••"`；在发送请求时，这些被替换的值会保持不变。
3. 所有更改都会立即生效（热重载），除了 `dashboard.port` 需要重启服务器外。
4. `x6551.token` 在 X Twitter 监控和 OpenNews 功能中共享。
5. 可以在 [https://6551.io/mcp] 获取 6551 API 密钥。

## 错误响应

| HTTP 状态码 | 响应内容 | 原因 |
|-------------|------|-------|
| 401 | `{ "ok": false, "error": "Unauthorized" }` | 缺少或输入错误的密码 |
| 400 | `{ "ok": false, "errors": [...] }` | 验证失败 |
| 400 | `{ "ok": false, "error": "Invalid JSON" }` | 请求格式错误 |
| 404 | `{ "ok": false, "error": "Not found" }` | 未知的 API 路由 |