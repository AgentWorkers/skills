---
description: 实时跟踪加密货币和股票价格，支持自定义警报设置，并提供多货币支持。
---

# 价格监控器

实时追踪加密货币和股票价格，并提供价格警报功能。

**适用场景**：查看加密货币价格、设置价格警报或监控市场走势。

## 系统要求**

- 需要互联网连接（使用 CoinGecko API；免费账户无需 API 密钥）
- 需要 `curl` 或 `python3` 来发起 API 请求
- 可选：在 shell 中使用 `jq` 进行 JSON 数据解析

## 使用说明**

1. **获取当前价格** — 使用 CoinGecko API：
   ```bash
   curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true&include_market_cap=true" | jq .
   ```

2. **支持多种资产** — 支持以逗号分隔的资产 ID（例如：`bitcoin,ethereum,solana`）。常见资产代码对应关系如下：
   - BTC → `bitcoin`
   - ETH → `ethereum`
   - SOL → `solana`
   - XRP → `ripple`
   - ADA → `cardano`
   - 完整资产列表：`https://api.coingecko.com/api/v3/coins/list`

3. **以表格形式显示数据**：
   ```
   | Asset    | Price (USD)  | 24h Change | Market Cap     |
   |----------|-------------|------------|----------------|
   | Bitcoin  | $97,432.10  | +2.3%      | $1.92T         |
   | Ethereum | $3,245.67   | -0.8%      | $390B          |
   ```

4. **价格警报** — 将警报信息保存到 `~/.openclaw/price-alerts.json` 文件中：
   ```json
   [{"coin": "bitcoin", "condition": ">", "target": 100000, "currency": "usd", "created": "ISO8601"}]
   ```
   可通过系统心跳事件或手动调用来检查警报；通知用户后，自动删除已触发的警报。

5. **历史数据** — 使用 `/coins/{id}/market_chart?vs_currency=usd&days=7` 查看价格趋势。

6. **支持多种货币** — 通过 `vs_currencies` 参数支持 JPY、EUR、GBP 等货币；默认货币为 USD。

## 特殊情况与故障排除**

- **请求限制**：CoinGecko 免费账户每分钟允许约 30 次请求；请确保响应被缓存至少 60 秒。
- **未知的资产 ID**：请先搜索 `/coins/list` 端点；若未找到匹配项，建议使用相近的资产 ID。
- **API 无法访问**：等待 5 秒后重试；如果仍然无法访问，请明确记录错误信息。
- **数据延迟**：CoinGecko 免费账户的数据可能存在 1-3 分钟的延迟，请在输出中予以说明。

## 安全性注意事项**

- 免费账户无需保护 API 密钥。
- 如果使用付费的 CoinGecko 密钥，请切勿在输出或日志中泄露该密钥。
- 请验证用户输入的资产 ID 是否为有效的字母数字组合（仅允许使用连字符）。

## 其他说明**

- 对于股票数据，建议使用 Yahoo Finance 的相关接口；或者使用 `curl` 并指定 `query1.finance.yahoo.com` 作为数据来源。
- 请将警报信息保存在 JSON 文件中，而不是内存中（这样可以在系统重启后仍然保留警报信息）。