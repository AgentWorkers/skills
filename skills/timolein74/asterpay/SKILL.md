---
name: asterpay
description: 用于AI代理的EUR结算及加密货币数据API：支持通过SEPA Instant将USDC转换为EUR。提供16个按次计费的API端点，用于获取市场数据、AI工具及加密货币分析服务。
metadata: {"clawdbot":{"emoji":"💶","requires":{"bins":["npx"],"env":[]},"primaryEnv":""}}
---
# AsterPay — 为AI代理提供的EUR结算服务

## 功能介绍

AsterPay允许您的OpenClaw代理访问其API，该API提供了16个终端点，用于获取加密货币市场数据、AI工具以及EUR结算估算信息。所有终端点均支持x402按次付费协议（使用Base网络上的USDC作为支付货币），其中部分终端点可免费使用。

## 使用方法

AsterPay作为MCP（Multi-Contract Protocol）服务器运行。您可以通过以下方式将其添加到您的OpenClaw配置中：

### 方法1：使用mcporter（推荐）

请指示您的OpenClaw代理执行以下操作：

```
Install the AsterPay MCP server: npx -y @anthropic-ai/mcp-remote@latest https://x402-api-production-ba87.up.railway.app/mcp
```

### 方法2：在`clawdbot.json`中手动配置

在`clawdbot.json`文件中添加以下配置：

```json
{
  "mcpServers": {
    "asterpay": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-remote@latest", "https://x402-api-production-ba87.up.railway.app/mcp"]
    }
  }
}
```

### 方法3：使用本地MCP服务器

配置本地MCP服务器后，在`clawdbot.json`文件中添加相应配置：

```json
{
  "mcpServers": {
    "asterpay": {
      "command": "asterpay-mcp-server"
    }
  }
}
```

## 可用工具

### 免费工具（无需付费）

| 工具 | 功能描述 |
|------|------------|
| `discover_endpoints` | 列出所有可用的API终端点及其费用信息 |
| `settlement_estimate` | 根据实时汇率计算USDC到EUR的转换金额 |
| `check_token_tiers` | 查看$ASTERPAY代币的折扣等级（最高可享受60%的折扣） |
| `check_wallet_tier` | 检查您的钱包中代币的余额及所属折扣等级 |

### 市场数据（需付费）

| 工具 | 费用 | 功能描述 |
|------|------|------------|
| `get_crypto_price` | $0.001 | 实时价格、市值及24小时交易量 |
| `get_ohlcv` | $0.005 | 用于图表制作的OHLCV蜡烛图数据 |
| `get_trending` | $0.002 | 当前热门的加密货币 |

### AI工具（需付费）

| 工具 | 费用 | 功能描述 |
|------|------|------------|
| `ai_summarize` | $0.01 | 对文本进行总结分析 |
| `ai_sentiment` | $0.01 | 情感分析（正面/负面/中性） |
| `ai_translate` | $0.02 | 将文本翻译成任意语言 |
| `ai_code_review` | $0.05 | 代码审查及安全分析 |

### 加密货币分析（需付费）

| 工具 | 费用 | 功能描述 |
|------|------|------------|
| `wallet_score` | $0.05 | 钱包信誉和风险评分 |
| `token_analysis` | $0.10 | 代币安全审计（检测潜在风险） |
| `whale_alerts` | $0.02 | 识别大额加密货币交易行为 |

### 实用工具（需付费）

| 工具 | 费用 | 功能描述 |
|------|------|------------|
| `generate_qr_code` | $0.005 | 生成QR码 |
| `take_screenshot` | $0.02 | 截取网页截图 |
| `generate_pdf` | $0.03 | 将HTML文件转换为PDF格式 |

## 示例请求

- “以太坊的当前价格是多少？”
- “1000 USDC可以兑换多少EUR？”
- “分析这篇关于比特币的文章的情感倾向”
- “检查这个代币合约的安全性（合约地址：0x...）”
- “显示Base网络上的大额加密货币交易提醒”
- “当前哪些加密货币是热门的？”

## x402支付方式

需要付费的API在响应时会返回“402 Payment Required”提示，并附带支付详细信息。支付流程如下：

1. 安装`x402 fetch`库：`npm install @x402/fetch`
2. 在Base网络上配置一个包含USDC的钱包
3. SDK会在每次API调用时自动处理支付操作

免费工具（`settlement_estimate`、`discover_endpoints`、`token_tiers`）无需使用钱包即可使用。

## 关于AsterPay

AsterPay是专为AI代理设计的EUR结算解决方案：
- 支持通过SEPA Instant方式在10秒内完成USDC到EUR的转换
- 已加入Coinbase的x402生态系统，是欧盟地区唯一的EUR支付服务提供商
- 符合MiCA标准，通过与欧洲合作伙伴的合作实现合规性
- 已注册为ERC-8004标准代币，在Base网络上编号为#16850
- 通过Arc Index获得链上NFT验证

官方网站：https://asterpay.io
文档：https://asterpay.io/docs
API：https://x402-api-production-ba87.up.railway.app
GitHub：https://github.com/timolein74/asterpay-api
PyPI：`pip install asterpay`
npm：`@asterpay/mcp-server`

## 安全注意事项

- 严禁发送超出用户明确授权的USDC金额
- 在进行任何货币转换前必须显示结算估算结果
- 禁止存储或记录钱包私钥
- 严格遵守x402支付确认机制，未经用户同意不得重试失败的支付请求