---
name: op0-altar
description: 通过 OP0 Altar 协议在 Solana 上创建和管理具有自我奖励功能的表情包代币（meme coins）。部署 pump.fun 代币，其持有者每隔几个 BTC 块就能自动获得奖励——具体奖励形式为 129 个 payout 代币。
version: 1.0.0
emoji: "\u2205"
metadata:
  openclaw:
    primaryEnv: OP0_API_KEY
    requires:
      env:
        - OP0_API_KEY
      anyBins:
        - curl
        - node
---
# OP0 Altar 协议技能

您可以通过 OP0 Altar 协议在 Solana 上创建和管理具有自我奖励功能的表情包代币。通过此技能发布的每个代币都会部署到 pump.fun 平台，并为持有者提供自动奖励——持有者每隔几个比特币区块就会收到以选定代币（包括 SOL、wBTC、BONK、MEW、TRUMP、JUP 等 129 种选项）形式的奖励。

## API 配置

- **基础 URL:** `https://api.op0.live/functions/v1/altar-api-public`
- **认证头:** `X-API-Key: <OP0_API_KEY>`
- **方法:** 所有请求均为 `POST`，`Content-Type: application/json`
- **认证:** 除 `generate-key` 和 `payout-tokens` 之外，所有端点都需要 `X-API-Key` 头部字段

## 自动生成 API 密钥

如果尚未设置 `OP0_API_KEY`，您可以自行生成一个。用户需要提供他们的 Solana 钱包地址。

```bash
curl -s -X POST https://api.op0.live/functions/v1/altar-api-public \
  -H "Content-Type: application/json" \
  -d '{"action":"generate-key","wallet":"USER_WALLET_ADDRESS","label":"OpenClaw Agent"}'
```

响应中会包含 `api_key`（格式：`op0_live_` + 64 个十六进制字符）。请立即保存该密钥，因为它无法再次获取。请告知用户将其添加到他们的 OpenClaw 配置中：

```bash
openclaw config set mcpServers.op0.env.OP0_API_KEY "op0_live_..."
```

或者将其存储在用户的环境变量中供后续使用。

## 可用的操作

### 1. 创建一个新的 Altar（代币）

在 Solana 上创建一个具有自我奖励功能的代币。所需字段：`token_name`（代币名称）、`token_ticker`（代币代码）、`marketing_wallet`（营销钱包地址）。

```bash
curl -s -X POST https://api.op0.live/functions/v1/altar-api-public \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $OP0_API_KEY" \
  -d '{
    "action": "create",
    "token_name": "TOKEN_NAME",
    "token_ticker": "TICKER",
    "marketing_wallet": "SOLANA_WALLET_ADDRESS",
    "payout_token_ticker": "wbtcsol",
    "blocks_per_cycle": 5,
    "payout_percent": 30,
    "min_hold_amount": 500000,
    "community_percent": 50,
    "color": "#3b8fff"
  }
```

可选字段：`token_description`（代币描述）、`website`（网站地址）、`token_twitter`（Twitter 账号）、`token_telegram`（Telegram 账号）、`payout_token_ticker`（默认为 wbtcsol）、`blocks_per_cycle`（2-9，默认为 5）、`payout_percent`（10-50，默认为 30）、`min_hold_amount`（默认为 500000）、`community_percent`（50-98，默认为 50）、`color`（十六进制颜色，默认为 #3b8fff）。

对于图片，需要使用 base64 编码，因此需要添加 `token_image_base64`、`token_image_mime` 和 `token_image_name` 字段。

响应会返回 `altar_id`、`dev_wallet`（开发钱包地址）和 `amount_required_sol`（通常为 0.05 SOL）以及 `expires_at`（30 分钟的有效期限）。

**创建完成后：** 告知用户将所需的 SOL 金额发送到 `dev_wallet` 地址，然后定期查询代币的状态。

### 2. 查询 Altar 状态

在用户发送 SOL 后，每 5 秒查询一次代币的状态。当资金到位后，代币会自动部署。

```bash
curl -s -X POST https://api.op0.live/functions/v1/altar-api-public \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $OP0_API_KEY" \
  -d '{"action":"status","altar_id":ALTAR_ID}'
```

状态变化：`awaiting_funding` -> `creating` -> `active`。当状态变为 `active` 时，响应中会包含 `token_mint`（代币总量）、`altar_url`（代币部署地址）、`pump_fun_url`（奖励分配平台地址）和 `treasury_wallet`（资金库钱包地址）。

如果状态显示为 `expired`，则表示 30 分钟的资金募集期限已结束，此时需要创建一个新的 Altar。

### 3. 列出所有 Altar

```bash
curl -s -X POST https://api.op0.live/functions/v1/altar-api-public \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $OP0_API_KEY" \
  -d '{"action":"list"}'
```

返回一个包含所有 Altar 的数组，其中包含 `altar_id`、`name`（代币名称）、`token_mint`（代币总量）、`status`（状态）、`altar_url`（代币部署地址）、`website`（网站地址）和 `payout_token`（奖励分配代币）等字段。

### 4. 获取 Altar 详细信息

```bash
curl -s -X POST https://api.op0.live/functions/v1/altar-api-public \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $OP0_API_KEY" \
  -d '{"action":"info","altar_id":ALTAR_ID}'
```

返回代币的完整详细信息，包括实时资金库余额（通过 RPC 获取）和当前周期的状态。

### 5. 列出所有可用的奖励分配代币（无需认证）

```bash
curl -s -X POST https://api.op0.live/functions/v1/altar-api-public \
  -H "Content-Type: application/json" \
  -d '{"action":"payout-tokens"}'
```

返回所有可用的 129 种奖励分配代币。分类包括：稳定币（usdc、usdt、pyusd、usd1、eurc、fdusd、usds）、蓝筹币（sol、wbtcsol、jitosol、msol、bnsol、render、pyth、hnt）、表情包代币（bonk、wif、popcat、fartcoin、mew、pnut、bome、moodeng、ponke、myro、giga、pengu、goat、chillguy、dood、vine）、AI 代币（virtual、griffain、elizaos、zerebro、swarms、tai、holo、llm、ani、buzz）、DeFi 代币（jup、ray、orca、drift、jto、kmno、met、fida、tensor）、代币化股票（tslax、nvdax、aaplx、mstrx、googlx、spyx、qqqx、coinx、crclx）以及政治相关代币（trump、melania、wlfi、a47）。

## 行为规则

1. 在创建 Altar 之前，务必询问用户的 `marketing_wallet` 地址。如果没有提供此地址，98% 的创建费用将归入社区资金库，而不会用于营销活动。
2. 当用户请求创建代币时，收集代币名称、代码、营销钱包地址以及可选的奖励分配代币类型。其他字段可以使用默认值。
3. 创建完成后，明确告知用户 `dev_wallet` 地址以及需要发送的 SOL 金额，并提醒他们注意 30 分钟的有效期限。
4. 用户确认发送 SOL 后，每 5 秒查询一次代币的状态（最多尝试 60 次），并最终报告代币的最终状态。
5. 如果用户询问“可以使用哪些代币进行奖励”，则调用 `payout-tokens` 端点并按类别展示可用的代币列表。
6. **速率限制：** 每个钱包每天最多使用 3 个 API 密钥，每个密钥每天最多创建 5 个代币。
7. 如果未配置 API 密钥，可以提供生成密钥的服务。用户只需提供他们的 Solana 钱包地址即可。

## 错误处理

- `401`：API 密钥无效或缺失。建议用户生成新的密钥。
- `429`：达到速率限制。响应中会包含 `resets_at` 时间戳，告知用户何时可以再次尝试。
- `400`：请求错误。检查是否缺少必要的字段（最常见的问题是缺少 `marketing_wallet`）。
- 如果状态显示为 `expired`，表示 30 分钟的资金募集期限已结束，此时需要创建一个新的 Altar。

## MCP 服务器替代方案

如果用户的 OpenClaw 实例支持 MCP 服务器，他们还可以使用 OP0 MCP 服务器进行更丰富的集成：

```bash
openclaw config set mcpServers.op0_command "npx"
openclaw config set mcpServers.op0.args '["@op0live/mcp-server"]
openclaw config set mcpServers.op0.env.OP0_API_KEY "op0_live_YOUR_KEY"
openclaw config set mcpServers.op0.env.OP0_API_URL "https://api.op0.live/functions/v1/altar-api-public"
```

这将启用以下 5 个命令：`op0_create_altar`、`op0_check_altar_status`、`op0_list_altars`、`op0_altar_info` 和 `op0_list_payout_tokens`。