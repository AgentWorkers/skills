---
name: moltalyzer
version: 1.7.0
description: 从 Moltbook 获取热门话题、情感分析结果及相关叙述（每小时更新一次）；发现 GitHub 上的热门新仓库和新兴工具（每日更新）；检测 Polymarket 预测市场（每 4 小时一次）；或获取新加密货币的实时信息（每 4 分钟更新一次）。提供四种数据源。支持 x402 次微支付，无需 API 密钥。
  Fetch trending topics, sentiment, and narratives from Moltbook (hourly),
  discover hot new GitHub repos and emerging tools (daily), detect Polymarket
  prediction markets with predetermined outcome signals (every 4 hours), or
  get real-time token intelligence signals for new crypto tokens (every 4 min).
  Four data feeds. x402 micropayments, no API key needed.
homepage: https://moltalyzer.xyz
metadata:
  openclaw:
    emoji: "🔭"
    requires:
      env: ["EVM_PRIVATE_KEY"]
      bins: ["node"]
    primaryEnv: "EVM_PRIVATE_KEY"
    install:
      - id: npm
        kind: command
        command: "npm install @x402/fetch @x402/evm viem"
        bins: ["node"]
        label: "Install x402 payment client"
---
# Moltalyzer — AI 智能数据源

Moltalyzer 提供了来自 `https://api.moltalyzer.xyz` 的四种数据源：

1. **Moltbook**（每小时更新）：热门话题、情感分析结果、新兴/衰退的舆论趋势以及热门讨论内容。
2. **GitHub**（每日更新）：热门的新仓库、新兴的工具、编程语言的趋势以及值得关注的项目。
3. **Polymarket**（每 4 小时更新）：提供具有预设结果信号的市场数据，包括置信度和相关分析。
4. **Token Intelligence**（每 4 分钟更新）：实时Token信号数据，采用混合规则与大型语言模型（LLM）进行评分，并经过链式过滤。

## 免费试用

无需任何设置，只需使用简单的 `fetch` 命令即可进行测试：

```typescript
const res = await fetch("https://api.moltalyzer.xyz/api/moltbook/sample");
const { data } = await res.json();
// data.emergingNarratives, data.hotDiscussions, data.fullDigest, etc.
```

这四种数据源都提供免费样本：`/api/moltbook/sample`、`/api/github/sample`、`/api/polymarket/sample`、`/api/tokens/sample`（每个数据源的每日请求限制为 1 次）。

## 付费接口

支付通过 x402 协议自动完成，无需 API 密钥或账户信息。价格范围为每次请求 0.005 美元至 0.05 美元。

| 数据源 | 接口地址 | 价格 |
|------|----------|-------|
| Moltbook | `GET /api/moltbook/digests/latest` | 0.005 美元 |
| Moltbook | `GET /api/moltbook/digests?hours=N` | 0.02 美元 |
| GitHub | `GET /api/github/digests/latest` | 0.02 美元 |
| GitHub | `GET /api/github/digests?days=N` | 0.05 美元 |
| GitHub | `GET /api/github/repos?limit=N` | 0.01 美元 |
| Polymarket | `GET /api/polymarket/signal` | 0.01 美元 |
| Polymarket | `GET /api/polymarket/signals?since=N&count=5` | 0.03 美元 |
| Tokens | `GET /api/tokens/signal` | 0.01 美元 |
| Tokens | `GET /api/tokens/signals?since=N&count=5` | 0.05 美元 |
| Tokens | `GET /api/tokens/history?from=YYYY-MM-DD` | 0.03 美元 |

### 快速入门（付费版本）

此外还支持以下环境变量：`PRIVATE_KEY`、`BLOCKRUN_WALLET_KEY`、`WALLET_PRIVATE_KEY`。

## 数据获取模式（Polymarket 和 Tokens）

Polymarket 与 Tokens 数据源采用基于索引的信号获取模式：首先查询免费的索引接口，然后获取新的信号数据：

```typescript
let lastIndex = 0;
// Check for new signals (free)
const indexRes = await fetch("https://api.moltalyzer.xyz/api/polymarket/index");
const { index } = await indexRes.json();
if (index > lastIndex) {
  // Fetch new signals (paid)
  const res = await fetchWithPayment(`https://api.moltalyzer.xyz/api/polymarket/signals?since=${lastIndex}`);
  const { data } = await res.json();
  lastIndex = index;
}
```

## 错误处理

- **402**：支付失败。请确认您的钱包中包含 Base Mainnet 支持的 USDC 货币；响应体中会包含详细的费用信息。
- **429**：请求次数达到限制。请按照 `Retry-After` 头部字段指定的时间间隔重新尝试。
- **404**：当前暂无数据可用（例如，服务刚刚启动或尚未生成数据摘要）。

## 参考文档

- 完整的响应格式请参阅 `{baseDir}/references/response-formats.md`。
- 更多的代码示例和错误处理方式请参阅 `{baseDir}/references/code-examples.md`。
- 完整的接口列表及请求速率限制信息请参阅 `{baseDir}/references/api-reference.md`。