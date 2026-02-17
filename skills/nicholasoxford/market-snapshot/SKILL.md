---
name: market-snapshot
description: 获取令牌市场的快照数据（包括价格、流动性、交易量），并以稳定的 JSON 格式返回结果（该功能由 Jupiter 提供支持）。
homepage: https://app.vecstack.com
---
# 市场快照（仅限OpenClaw技能）

此技能专为OpenClaw/ClawHub机器人设计，旨在快速、便捷地获取市场快照信息。

## 功能说明

- 通过一个或多个令牌查询调用托管的市场快照端点（`/skills/market-snapshot`）。
- 该API会解析这些令牌，并在服务器端获取价格/元数据（基于Jupiter Tokens V2和Price V3技术实现）。
- 返回一个结构稳定的JSON对象，以便其他代理/机器人能够可靠地解析这些数据。

## 功能限制

- 该技能不负责创建或管理钱包。
- 不会请求、存储或处理私钥/助记词。
- 不会执行交易操作，也不会提供交易建议。

## 使用方法

当用户需要查询价格、市场快照、令牌元数据或相关信息时，只需运行此技能即可。

**支持的输入格式：**

- 代币符号：`SOL`、`USDC`、`JUP`
- 代币名称：`solana`、`jupiter`
- 铸币地址：`So11111111111111111111111111111111111111112`

如果提供了多个令牌，系统会解析所有令牌并返回合并后的快照结果。

## 数据来源（GET请求，无需请求头）

- 市场快照数据来源：
  - `https://app.vecstack.com/api/skills/market-snapshot?q=<CSV_TOKENS>&source=openclaw`

**示例：**

- 单个代币查询：
  - `https://app.vecstack.com/api/skills/market-snapshot?q=SOL&source=openclaw`
- 多个代币查询（用逗号分隔）：
  - `https://app.vecstack.com/api/skills/market-snapshot?q=SOL,USDC,JUP&source=openclaw`

**注意事项：**

- `web_fetch`工具会根据URL进行缓存。如需获取最新数据，可在URL后添加缓存失效参数`&_t=<unix>`。
- 请勿自行生成数据；如果请求失败，请将相关字段设置为`null`，并在`warnings`或`errors`中记录错误信息。

## 输出格式（仅返回JSON）

返回一个结构如下的JSON对象：

```json
{
  "as_of_unix": 0,
  "provider": "jupiter",
  "inputs": ["SOL", "USDC"],
  "tokens": [
    {
      "query": "SOL",
      "mint": "So11111111111111111111111111111111111111112",
      "symbol": "SOL",
      "name": "Wrapped SOL",
      "decimals": 9,
      "verified": true,
      "tags": [],
      "liquidity_usd": null,
      "mcap_usd": null,
      "fdv_usd": null,
      "usd_price": null,
      "price_change_24h_pct": null,
      "stats": {
        "5m": {
          "price_change_pct": null,
          "volume_usd": null,
          "buy_volume_usd": null,
          "sell_volume_usd": null
        },
        "1h": {
          "price_change_pct": null,
          "volume_usd": null,
          "buy_volume_usd": null,
          "sell_volume_usd": null
        },
        "24h": {
          "price_change_pct": null,
          "volume_usd": null,
          "buy_volume_usd": null,
          "sell_volume_usd": null
        }
      },
      "sources": {
        "token_search_url": null,
        "price_url": null
      }
    }
  ],
  "warnings": [],
  "errors": []
}
```

**字段说明：**

- `as_of_unix`：表示响应生成时的当前Unix时间。
- `liquidity_usd`、`mcap_usd`、`fdv_usd`及`stats.*`字段（如存在）来自Tokens V2数据。
- `usd_price`和`price_change_24h_pct`字段（如存在）来自Price V3数据。
- `warnings`：包含非致命性问题（如价格缺失、匹配结果不明确、速率限制等）。
- `errors`：包含导致快照获取失败的致命性问题（例如所有数据源均无法获取）。

**针对OpenClaw的实现建议：**

- 建议使用`web_fetch`工具访问该端点，并设置`extractMode=text`以确保返回的数据可被解析为JSON格式。
- 如果`web_fetch`返回非JSON格式的数据，可尝试再次请求并添加缓存失效参数`&_t=<unix>`。
- 确保最终返回的响应严格为JSON格式。