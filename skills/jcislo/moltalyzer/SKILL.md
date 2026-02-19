---
name: moltalyzer
version: 1.4.0
description: 从 Moltbook 中获取热门话题、情感分析结果及相关叙述（每小时更新一次）；发现热门的新 GitHub 仓库和新兴工具（每日更新）；或查找带有内部信息信号的 Polymarket 预测市场（每日更新）。适用于需要社区分析、热门仓库信息、语言趋势或市场情报的场景。支持 x402 微支付方式，无需 API 密钥。
  Fetch trending topics, sentiment, and narratives from Moltbook (hourly),
  discover hot new GitHub repos and emerging tools (daily), or find Polymarket
  prediction markets with insider-knowledge signals (daily). Use when you need
  community analysis, trending repos, language trends, or market intelligence.
  x402 micropayments, no API key needed.
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

来自 `https://api.moltalyzer.xyz` 的三个数据源：

1. **Moltbook**（每小时更新）：热门话题、情感分析结果、新兴/逐渐淡出的讨论趋势、热点讨论内容
2. **GitHub**（每日更新）：热门的新仓库、新兴工具、编程语言趋势、值得关注的项目
3. **Polymarket**（每日更新）：内部人士可能掌握提前信息的金融市场，附带信心等级信息

## 免费试用

无需任何设置。可以使用普通的 `fetch` 命令进行测试：

```typescript
const res = await fetch("https://api.moltalyzer.xyz/api/moltbook/sample");
const { data } = await res.json();
// data.emergingNarratives, data.hotDiscussions, data.fullDigest, etc.
```

这三个数据源都提供免费样本：`/api/moltbook/sample`、`/api/github/sample`、`/api/polymarket/sample`（每个数据源的每日请求限制为 1 次）。

## 支付接口

支付通过 x402 协议自动完成，无需 API 密钥或账户信息。即使仅支付 1 美元 USDC，也可以使用 200 次请求。

| 数据源 | 接口地址 | 价格 |
|------|----------|-------|
| Moltbook | `GET /api/moltbook/digests/latest` | $0.005 |
| Moltbook | `GET /api/moltbook/digests?hours=N` | $0.02 |
| GitHub | `GET /api/github/digests/latest` | $0.02 |
| GitHub | `GET /api/github/digests?days=N` | $0.05 |
| GitHub | `GET /api/github/repos?limit=N` | $0.01 |
| Polymarket | `GET /api/polymarket/latest` | $0.02 |
| Polymarket | `GET /api/polymarket/all?days=N` | $0.05 |

### 快速入门（需付费）

还支持以下环境变量：`PRIVATE_KEY`、`BLOCKRUN_WALLET_KEY`、`WALLET_PRIVATE_KEY`。

## 错误处理

- **402**：支付失败。请检查钱包中是否包含 Base Mainnet 支付所需的 USDC。响应体中会包含详细的费用信息。
- **429**：请求次数达到限制。请按照 `Retry-After` 头部字段指定的时间间隔重新尝试。
- **404**：数据尚未准备好（例如，服务刚刚启动，尚未生成分析结果）。

## 参考文档

- 完整的响应格式请参见 `{baseDir}/references/response-formats.md`。
- 更多的代码示例和错误处理方式请参见 `{baseDir}/references/code-examples.md`。
- 完整的接口列表及请求限制信息请参见 `{baseDir}/references/api-reference.md`。