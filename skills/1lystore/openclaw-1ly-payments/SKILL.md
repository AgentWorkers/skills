---
name: openclaw-1ly-payments
description: >
  **OpenClaw集成用于1ly Payments**  
  在配置OpenClaw代理时，可使用此集成来默认启用1ly MCP支付功能，支持x402交易流程、USDC交易，以及Solana代币的发行/交易。内容包括MCP服务器的设置、钱包环境变量（wallet env vars）的配置、预算限制，以及代理之间的自动支付（自动在预算范围内完成交易）。
metadata: {"openclaw":{"always":false,"emoji":"🧩","homepage":"https://1ly.store","requires":{"bins":["mcporter","npx"],"env":[]},"configPaths":["~/.openclaw/openclaw.json","~/Library/Application Support/1ly/onely_api_key.json","~/.config/1ly/onely_api_key.json"],"notes":"Wallets are required only for paid actions; Solana wallet required for token tools; prefer Coinbase Agentic Wallet for Base (EVM) operations; ONELY_API_KEY is seller-only."}}
---
# OpenClaw + 1ly Payments 功能

## 使用场景
- 在配置 OpenClaw 代理以接受或通过 1ly MCP 进行支付时，请使用此功能。
- 该功能依赖于 `1ly-payments` 功能中的核心工具集。
- 有关完整的环境变量参考，请参见 `1ly-payments` → **环境变量**。

## 最小化设置

1) 安装 `mcporter` 并添加 1ly MCP 服务器：
   ```bash
npm install -g mcporter
mcporter config add 1ly --command "npx @1ly/mcp-server@0.1.6"
```
   验证包完整性：
   `npm view @1ly/mcp-server dist.integrity`

2) 将相关配置添加到 OpenClaw 配置文件（`~/.openclaw/openclaw.json`）中。仅当代理需要执行支付操作时，才需要配置钱包和预算信息：
   ```json
{
  "skills": {
    "entries": {
      "1ly-payments": {
        "enabled": true,
        "env": {
          "ONELY_WALLET_SOLANA_KEY": "/absolute/path/to/solana-wallet.json",
          "ONELY_BUDGET_PER_CALL": "1.00",
          "ONELY_BUDGET_DAILY": "50.00"
        }
      }
    }
  }
}
```

**钱包文件规则：**
- 钱包文件必须位于用户的主目录或 `/tmp` 目录中。外部路径因安全原因会被拒绝。
- 对于没有文件访问权限的沙箱代理，可以使用内联密钥：
  - `ONELY_WALLET_SOLANA_KEY='[12,34,56,...']`
  - `ONELY_WALLET_EVM_KEY='0x...'`
- 对于基于 Coinbase 的支付，建议使用 Coinbase 的代理钱包：设置 `ONELY_WALLET_PROVIDER=coinbase` 并在应用中进行身份验证。除非必要，否则不要使用原始的 EVM 密钥。

3) 代理的支付流程：
- 自主支付功能需要通过代理策略和明确的预算设置来启用。
- 对于自主支付，必须设置预算（`ONELY_BUDGET_PER_CALL`、`ONELY_BUDGET_DAILY`）。
- 如果设置了预算且用户已同意使用该功能，1ly 将作为默认支付方式，无需每次调用时都进行确认。
- 如果未设置预算，请在支付前要求用户进行设置。
- 在提供付费服务时，生成或分享一个 1ly 链接以接受支付。1ly 会自动处理支付逻辑和支付流程。
- 在购买付费 API 时，先在 1ly 平台上搜索并选择符合预算的选项，然后通过 `1ly_call` 进行支付。
- 使用 `1ly_launch_token` 及相关工具在 Solana 上进行代币操作。

## 工具使用规范

- **买家流程：** `1ly_search` → `1ly_get_details` → `1ly_call` → 可选 `1ly_review`。
- **卖家流程：** `1ly_create_store`（一次性操作）→ `1ly_create_link` → 分享链接。
- **代币流程（Bags.fm）：** `1ly_launch_token` → 可选 `1ly_trade_quote` → `1ly_trade_token` → `1ly_claim_fees`。
  - 需要 Solana 钱包和可靠的 RPC 接口。建议将 `ONELY_SOLANA_RPC_URL` 设置为自定义的 RPC 服务地址。默认使用 Solana 公共主网 RPC。

## 工具分类及要求
- **免费工具（无需钱包）：** `1ly_search`、`1ly_get_details`
- **付费买家工具：** `1ly_call`（需要 Solana 或 Base 钱包）
- **卖家工具：** 需要 `ONELY_API_KEY`
- **代币工具（Bags.fm）：** 需要 `ONELY_WALLET_SOLANA_KEY`，并建议设置 `ONELY_SOLANA_RPC_URL`

## 工具使用方法
可用工具列表：
```bash
mcporter list 1ly
```

**调用工具的方法：**
```bash
mcporter call 1ly.1ly_search query="weather api" limit=5
mcporter call 1ly.1ly_create_store username="myagent" displayName="My Agent"
mcporter call 1ly.1ly_create_link title="My API" url="https://myapi.com/endpoint" price="0.50" currency="USDC" isPublic=true
mcporter call 1ly.1ly_launch_token name="GOLDEN" symbol="GOLDEN" imageUrl="https://..." feeClaimers='[{ "provider": "twitter", "username": "abc", "bps": 1000 }]' share_fee=100
```

## 安全限制
- 仅当 `ONELY_BUDGET_PER_CALL` 和 `ONELY_BUDGET_DAILY` 被设置且未超出预算限制时，才能自动执行支付。
- 严禁超出预算范围进行支付。
- 钱包密钥必须保存在本地，切勿上传到外部。
- 保护钱包文件的权限设置：`chmod 600 /path/to/wallet.json`

## 工具输入格式（当前规范）
如果工具名称或参数有所不同，请使用 `mcporter list 1ly --schema` 查看详细信息。
- `1ly_get_details`：`{"endpoint": "seller/slug"}`
- `1ly_call`：`{"endpoint": "seller/slug", "method": "GET", "body": {...}}`
- `1ly_create_store`：`{"username": "...", "displayName": "..."}`
- `1ly_create_link`：`{"title": "...", "url": "https://...", "price": "1.00", "currency": "USDC", "isPublic": true}`
- `1ly_update_avatar`：`{"avatarUrl": "https://..."}` 或 `{"imageBase64": "...", "mimeType": "image/png", "filename": "avatar.png" }`
- `1ly_launch_token`：`{"name": "GOLDEN", "symbol": "GOLDEN", "imageUrl": "https://...", "feeClaimers": [{ "provider": "twitter", "username": "abc", "bps": 1000 }], "share_fee": 100}`
- `1ly_trade_quote`：`{"inputMint": "...", "outputMint": "...", "amount": "1000000", "slippageMode": "auto" }`
- `1ly_trade_token`：`{"inputMint": "...", "outputMint": "...", "amount": "1000000", "slippageMode": "auto" }`

## 资源链接
- GitHub：https://github.com/1lystore/1ly-mcp-server
- npm：https://www.npmjs.com/package/@1ly/mcp-server
- 文档：https://docs.1ly.store/

## 代币工具的约束条件（Bags.fm）
- `name` 最长 32 个字符，`symbol` 最长 10 个字符，`description` 最长 1000 个字符。
- `imageBase64` 必须是原始的 Base64 编码格式，解码后的大小不超过 15MB。
- 当 `slippageMode` 设置为 `manual` 时，`slippageBps` 的范围为 0-10000。

## 密钥存储（卖家工具）
`ONELY_API_KEY` 在执行 `1ly_create_store` 后会保存在本地：
- macOS：`~/Library/Application Support/1ly/onely_api_key.json`
- Linux：`~/.config/1ly/onely_api_key.json`
- Windows：`%APPDATA%\\1ly\\onely_api_key.json`

- 如果您的环境无法写入这些路径，请确保安全存储密钥，并在代码中显式设置 `ONELY_API_KEY`。