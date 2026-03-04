---
name: openclaw-x402-skill
description: "在 x402 Bazaar 中，您可以发现、浏览、筛选并支付兼容 x402 协议的 API 端点及 MCP 工具——这是一个专为代理支付设计的自动化发现平台。您可以查看所有可用的服务，按价格或类型进行筛选，查看支付要求，并使用 USDC 在 Base 平台上进行微支付来调用任何找到的 API 端点，而无需设置 API 密钥或账户信息。当代理需要查找可支付的 API 服务、确认特定任务（如网络爬虫、AI 推理、天气数据、市场数据）所需的 x402 服务、通过 x402 支付单个 API 调用，或列出价格低于指定阈值的服务时，都可以使用该平台。请注意：对于需要付费的调用，必须在 `.env` 文件中配置 `EVM_PRIVATE_KEY`（使用 USDC 的 Base 钱包）。而进行服务浏览时则完全不需要任何密钥。"
metadata:
  openclaw:
    emoji: "🛒"
    requires:
      bins: ["python3"]
      env:
        - EVM_PRIVATE_KEY
    install:
      - id: pip
        kind: shell
        command: "pip install -r ~/clawd/skills/openclaw-x402-skill/requirements.txt"
        label: "Install Python dependencies"
---
# x402 Bazaar 技能

x402 Bazaar 是 x402 生态系统的发现层——一个机器可读的目录，帮助 AI 代理查找并集成与 x402 兼容的 API 端点及 MCP 工具。用户可以查询、查找、支付并使用这些服务，而无需预先进行任何集成设置。

**两种使用模式：**
- **仅浏览**：无需钱包，完全免费，可发现所有可用服务。
- **浏览 + 支付**：需要拥有包含 USDC 的 Base 钱包，才能调用已发现的 API 端点。

---

## 先决条件

### 仅浏览（无需密钥）
```bash
python3 agent.py "list services"
python3 agent.py "find weather APIs"
```

### 调用付费 API 端点的方法：
1. 获取 Base 钱包的私钥（通过 MetaMask 导出，或从 Coinbase Wallet 获取）。
2. 用 USDC 为 Base 钱包充值（可从 coinbase.com 或 bridge.base.org 兑换）。
3. 将私钥添加到 `.env` 文件中：
```
EVM_PRIVATE_KEY="0xYourPrivateKeyHere"
MAX_SPEND_PER_CALL=0.10
```

### 安装依赖项（只需运行一次）：
```bash
pip install -r ~/clawd/skills/x402-bazaar/requirements.txt
```

---

## 何时激活此技能

在用户执行以下操作时激活此技能：

**发现服务：**
- “有哪些 x402 服务可用？”
- “在 x402 上为我找到一个用于 [任务] 的 API”
- “浏览 x402 Bazaar”
- “哪些服务的价格低于 0.01 美元？”
- “找到一个按调用次数计费的天气 API”
- “x402 上有哪些 MCP 工具？”
- “显示价格在 [价格范围] 内的 x402 服务”
- “在 x402 中搜索 [关键词]”

**支付服务：**
- “调用这个 x402 端点：[url]”
- “为 [服务名称] 支付并调用它”
- “使用 x402 获取 [数据]——找到并支付最便宜的服务”
- “向 [url] 发送付费请求”

**不适用的情况：**
- 检查代理自己的钱包余额 → 使用 /agent-wallet 技能。
- 作为卖家在 Bazaar 上发布服务 → 请参阅下方的卖家指南。
- 进行 Alpaca 或股票交易 → 使用 /alpaca-trading 技能。

---

## 具体命令：

### 列出所有可用服务：
```bash
cd ~/clawd/skills/x402-bazaar && python3 agent.py "list services"
```

### 按关键词搜索：
```bash
python3 agent.py "find weather"
python3 agent.py "search for AI inference"
python3 agent.py "find web scraping services"
```

### 按最高价格过滤：
```bash
python3 agent.py "services under 0.01"
python3 agent.py "services under 0.001 USDC"
```

### 按类型过滤：
```bash
python3 agent.py "list http services"
python3 agent.py "list mcp tools"
```

### 查看特定服务：
```bash
python3 agent.py "inspect https://api.example.com/x402/weather"
```

### 调用已发现的服务（需要 EVM_PRIVATE_KEY 和 USDC）：
```bash
python3 agent.py "call https://api.example.com/x402/weather?location=NYC"
python3 agent.py "pay and call https://api.example.com/x402/sentiment"
```

### 完整的自动化流程：查找 → 支付 → 使用：
```bash
python3 agent.py "find the cheapest weather API and get weather for London"
python3 agent.py "find a web scraping API and scrape https://example.com"
```

---

## x402 的支付机制：

1. 代理从 Bazaar 目录中发现服务。
2. 调用该服务端点，收到 HTTP 402 “需要支付” 的响应。
3. 从响应头中读取支付要求。
4. 通过 Base 钱包使用 USDC 进行支付。
5. 重新发送相同的请求，并附带支付证明。
6. 服务验证支付证明后返回结果。

无需账户、订阅或 API 密钥——每次请求只需支付 USDC。

---

## MCP 集成

此技能可以与 **Model Context Protocol (MCP)** 服务器集成，使 Claude Desktop 及其他 MCP 客户端能够自动支付并使用 x402 API。

**查看完整的 MCP 集成指南：** [x402-MCP.md](x402-MCP.md)

**主要功能：**
- 在 Claude Desktop 中将 x402 服务作为 MCP 工具展示。
- 当 Claude 调用 API 时自动处理支付。
- 支持 EVM (Base) 和 Solana 两种网络。
- 全程自动化，无需手动操作。

**示例：** Claude 可以通过此技能发现天气 API，然后通过 MCP 调用它们，并在 Base 上自动完成 USDC 的微支付。

---

## 可用的支付中介：

| 支付中介 | 发现 URL | 备注 |
|---|---|---|
| Coinbase CDP | `api.cdp.coinbase.com/platform/v2/x402/discovery/resources` | 最大的服务目录，默认选择 |
| PayAI | `facilitator.payai.network/discovery/resources` | 另一个服务目录 |

执行 “list services” 命令时，这两个目录的数据会被合并显示。

---

## 输出格式：

- **服务列表：**
```
🛒 x402 Bazaar — 42 services found

 1. 🌐 Weather API
    URL:      https://api.weather-x402.com/current
    Type:     http GET
    Price:    $0.001 USDC
    Network:  Base (eip155:8453)
    Updated:  2h ago

 2. 🤖 Llama 3.3 70B Inference
    URL:      https://api.x402network.com/llm/llama
    Type:     http POST
    Price:    $0.005 USDC
    Network:  Base (eip155:8453)
    Updated:  4h ago
```

- **付费调用结果：**
```
💸 x402 Payment Executed
   Endpoint:  https://api.weather-x402.com/current
   Paid:      $0.001 USDC
   Network:   Base (eip155:8453)
   TxHash:    0xabc123...
   Status:    200 OK

📦 Response:
   {"temperature": 72, "conditions": "sunny", "humidity": 45}
```

---

## 支付限额

每次调用的默认最高花费为 0.10 美元 USDC。具体限额可在 `.env` 文件中设置：
```
MAX_SPEND_PER_CALL=0.10
```

如果请求的金额超过此限额，技能会要求用户确认后再继续操作。

---

## 错误处理：

| 错误 | 原因 | 解决方案 |
|---|---|---|
| `EVM_PRIVATE_KEY 未设置` | .env 文件中缺少该密钥 | 在 .env 文件中添加密钥（仅针对付费调用） |
| USDC 余额不足 | 钱包资金不足 | 请通过 bridge.base.org 将 USDC 兑换到 Base |
- 超过支付限额 | 服务价格超过 MAX_SPEND_PER_CALL | 在 .env 文件中调整限额或手动确认 |
- 支付验证失败 | 支付中介拒绝支付 | 重试或更换支付中介 |
- 未找到服务 | Bazaar 中没有相关服务 | 扩大搜索范围或稍后再试 |
- 网络不匹配 | 服务所在的链不支持 | 使用 eip155:8453 进行过滤 |

---

## 支持的网络（v1.0）：

- Base 主网：eip155:8453（使用真实的 USDC）
- Base Sepolia：eip155:84532（测试用虚拟 USDC）

Solana 的支持计划在 v1.1 版本中实现。

---

## 在 Bazaar 上发布自己的 API（作为卖家）：

要将自己的 x402 API 发布到 Bazaar（符合 v2 规范）：
1. 在 x402 资源服务器中添加 `bazaarResourceServerExtension`。
2. 在路由配置中使用 `declareDiscoveryExtension()`。
3. 在 `accepts[]` 配置中设置 `maxAmountRequired`（替代 v1 版本中的 `amount` 字段）。
4. 发布服务是免费的——服务自行设置每次调用的价格。

**注意：** 该技能同时支持 v1（扁平列表）和 v2（封装响应）格式，以确保兼容性。

**MCP 工具的唯一性：** 对于 MCP 服务器而言，唯一性由 `(resource_url, tool_name)` 确定，而不仅仅是 URL，因为一个 MCP 服务器可以托管多个工具。

**完整的卖家指南：** [docs.cdp.coinbase.com/x402/bazaar](https://docs.cdp.coinbase.com/x402/bazaar)