---
name: clawdio
description: 分析 Twitter Spaces 和语音对话，以提取市场情报、加密货币相关数据、情感分析结果以及发言者的相关信息。该工具能够将语音内容转换为结构化的报告、完整的文字记录以及机器可读的元数据。适用于需要从 Twitter Spaces、播客讨论或任何长篇语音内容中获取信息的情况——尤其是针对加密货币市场、人工智能趋势以及仅以音频形式存在的专家评论。
compatibility: Requires network access and an x402-compatible wallet (Coinbase AgentKit, CDP SDK, or @x402/fetch) funded with USDC on Base Mainnet.
metadata:
  author: vail
  version: "1.1.0"
  homepage: https://clawdio.vail.report
  api-base: https://clawdio.vail.report
  protocol: x402
  network: eip155:8453
  currency: USDC
  price: "1.49"
  category: analytics
---

# Clawdio — 专为AI代理设计的Twitter Spaces智能分析工具

Clawdio能够将Twitter Spaces中的对话内容以及语音交流转化为结构化、机器可读的智能数据。当关键的市场洞察、加密货币的早期信息或专家讨论仅以音频形式存在时，Clawdio能够将这些信息提供给AI代理使用。

**基础URL：** `https://clawdio.vail.report`

## 使用场景

- 当重要的市场情报仅存在于Twitter Spaces中（而非文本形式）时
- 需要包含发言者信息及时间戳的引用内容
- 需要从语音中提取加密货币的早期信息、情感分析结果或趋势信号
- 专家讨论的内容未能被记录为书面帖子
- 需要从长时间的音频对话中提取结构化数据

## 使用成果

每份报告（1.49美元）包含以下三种机器可读的输出：

**元数据** — 标题、日期、时长、听众数量、参与者的Twitter用户名及头像列表、交易哈希值。

**结构化报告（Markdown格式）** — 摘要、关键洞察、带有时间戳的发言者观点、事件时间线、潜在的市场信号、市场情绪评估、项目/代币的提及情况及其背景信息。

**完整转录文本（Markdown格式）** — 每条发言都带有发言者信息和时间戳，格式统一，便于后续处理。

## 快速入门

### 1. 浏览可用报告（免费）

```bash
curl https://clawdio.vail.report/catalog
```

该接口会返回所有可用的Twitter Spaces报告的元数据、摘要及价格信息。

### 2. 购买报告

```bash
curl https://clawdio.vail.report/catalog/purchase?id={uuid}
```

该接口使用**x402协议**进行支付。您的钱包会自动完成支付流程：
1. 服务器返回HTTP 402响应，提示支付要求。
2. 您的钱包在Base Mainnet网络上使用USDC完成支付。
3. 重复请求时需要提供支付签名。
4. 支付完成后，系统会返回完整的报告数据。

**注意：** 无需注册账户或API密钥，支付是使用的唯一方式。

## 示例响应

```json
{
  "id": "c6d36398-a0c8-4c21-9aa4-1d1d9084a820",
  "transaction": "0x1234...abcd",
  "title": "AI & Crypto Twitter Space",
  "date": "2025-01-15",
  "length": "01:23:45",
  "listeners": 1234,
  "participants": {
    "hosts": [{ "display_name": "Host", "screen_name": "host_handle" }],
    "speakers": [{ "display_name": "Speaker", "screen_name": "speaker_handle" }]
  },
  "content": {
    "report": {
      "format": "markdown",
      "content": "## Key Insights\n- Insight 1\n- Insight 2\n\n## Hot Takes\n> \"Quote\" — **Speaker** (00:15:30)\n\n## Market Sentiment\n**Overall:** Bullish"
    },
    "transcript": {
      "format": "markdown",
      "content": "**Speaker** [00:01:26 - 00:01:49]\n> Spoken text here..."
    }
  }
}
```

## 端点接口

| 端点 | 方法 | 认证方式 | 描述 |
|------|--------|------|-------------|
| `/` | GET | 无 | API的根路径 |
| `/catalog` | GET | 无 | 浏览可用报告 |
| `/catalog/purchase?id={uuid}` | GET | 使用x402协议购买报告（1.49美元） |
| `/health` | GET | 无 | 系统健康检查 |
| `/.well-known/x402` | GET | 无 | x402协议的发现文档 |

## 重要说明

- 购买报告的接口使用**GET**方法，而非**POST**方法。
- 支付必须使用**Base Mainnet网络上的USDC**（地址：eip155:8453）。
- 请保存响应内容，如需再次访问需重新购买报告。
- 无需进行任何身份验证或注册账户。

## 代理应用场景

- **交易信号分析**：从实时市场讨论中提取情感分析和市场趋势信号。
- **研究整合**：跨多个Twitter Spaces对比分析数据。
- **网络关系图构建**：根据参与者信息生成发言者关系图。
- **趋势监测**：追踪项目提及和情绪变化。
- **引用标注**：为特定发言者标注其发言内容及时间戳。

## 集成方式

有关使用Coinbase AgentKit和@x402/fetch的集成示例，请参阅[references/INTEGRATION.md]。
完整的报告结构和响应格式详见[references/API-REFERENCE.md]。

## 开发计划

Clawdio目前处于早期发布阶段，目前提供精选的AI和加密货币相关Twitter Spaces数据。未来计划推出以下功能：
- **任意空间分析**：提交任意Twitter Spaces链接即可按需生成报告。
- **海量数据目录**：涵盖超过10,000个与加密货币、AI、科技和市场相关的Twitter Spaces。
- **语义搜索**：根据主题、发言者、项目或情绪关键词搜索相关内容。
- **实时数据处理**：实时处理新发布的Twitter Spaces内容。

---

**由[VAIL](https://vail.report)开发 — 语音AI解决方案提供商**