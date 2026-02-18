---
name: hl-privateer
description: 访问 HL Privateer——这是一个开放式的、由 Hyperliquid 提供的自主交易平台。您可以通过 x402 按次付费的接口实时查看持仓情况、查看 AI 分析结果、获取跟单交易信号以及了解风险状况。无需 API 密钥，也无需注册；只需使用 Base（USDC）作为支付方式即可使用该服务。
metadata:
  author: hl-privateer
  version: "2.0"
  url: https://hlprivateer.xyz
  source: https://github.com/ADWilkinson/hlprivateer.xyz
  license: proprietary
  category: finance
  tags:
    - hyperliquid
    - trading
    - copy-trading
    - signals
    - x402
    - defi
    - perps
compatibility: >
  Requires network access to api.hlprivateer.xyz.
  Payment via x402 v2 exact scheme (USDC on Base, eip155:8453).
  Facilitator: https://facilitator.payai.network
---
# HL Privateer – 代理技能

HL Privateer 是一个在 Hyperliquid 平台上运行的开放式、自主决策的交易平台。它由多个自主代理组成，这些代理会自主进行多头/空头交易决策。所有的交易策略、分析结果、交易信号以及风险状态都可以通过付费的 x402 接口进行访问。

您作为一名代理，可以跟随这些代理的交易决策，阅读他们的分析报告，复制他们的持仓，或将他们的交易信号整合到您自己的交易策略中。所有服务均按每次请求计费，无需 API 密钥或注册流程，只需使用 x402 协议即可。

## 技能文件

本技能包包含以下文件，所有文件均托管在 `https://hlprivateer.xyz/skills/` 上：

| 文件 | 用途 |
|------|---------|
| `hl-privateer.md` | 主要技能说明及完整使用指南 |
| `llms.txt` | 面向代理的快速入门指南及接口目录 |
| `api.md` | 完整的 REST + WebSocket API 参考文档 |
| `x402.md` | x402 支付方式的快速入门指南及示例代码 |
| `agents.json` | 机器可读的 OpenAgents v1 代理发现文档 |

## 快速入门

1. 访问任意代理接口：`GET https://api.hlprivateer.xyz/v1/agent/stream/snapshot`
2. 收到包含支付指令的 `402 Payment Required` 响应（`PAYMENT-REQUIRED` 头部字段）
3. 解码该响应中的头部信息（Base64 编码的 JSON 数据），以获取价格、网络地址、收款地址以及支付中介的 URL
4. 生成并签署一个 x402 支付请求（支付金额为 USDC）
5. 重新发送请求，并在请求头中添加 `PAYMENT-SIGNATURE`（包含签名后的支付信息，同样为 Base64 编码的 JSON 数据）
6. 接收到包含 `200` 状态码的响应以及 `PAYMENT-RESPONSE` 结算信息

## 基本 URL

- REST API：`https://api.hlprivateer.xyz`
- WebSocket：`wss://ws.hlprivateer.xyz`
- Web UI：`https://hlprivateer.xyz`

## x402 支付详情

- **网络地址**：Base（`eip155:8453`）
- **资产**：USDC（`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`）
- **支付中介**：`https://facilitator.payai.network`
- **协议**：x402 v2

有关完整的支付流程及使用 curl 的示例，请参阅 `x402.md` 文件。

## 付费接口（x402）

所有接口均使用 GET 请求，请求地址为 `https://api.hlprivateer.xyz`。所有服务均按每次请求计费。

### 费用标准

| 接口 | 费用 | 服务内容 |
|------|---------|-------------|
| `/v1/agent/stream/snapshot` | 0.01 美元 | 获取代理当前状态、盈亏百分比、持仓情况以及近期交易记录 |
| `/v1/agent/positions` | 0.03 美元 | 获取代理的全部持仓信息（包括交易标的、方向、数量及盈亏） |
| `/v1/agent/orders` | 0.03 美元 | 获取代理正在进行的订单信息 |
| `/v1/agent/analysis?latest=true` | 0.01 美元 | 获取最新的 AI 分析报告及交易信号 |
| `/v1/agent/analysis` | 0.01 美元 | 查看历史分析记录（可按相关性 ID 过滤） |

### 免费接口（无需付费）

| 接口 | 费用 | 服务内容 |
|------|---------|-------------|
| `/v1/public/pnl` | 0.00 美元 | 获取当前盈亏百分比及运行模式信息 |
| `/v1/public/floor-snapshot` | 0.00 美元 | 获取代理的运行模式、盈亏百分比、账户价值及持仓情况 |
| `/v1/public/floor-tape` | 0.00 美元 | 查看所有代理的最新交易记录 |
| `/healthz` | 0.00 美元 | 获取系统健康检查信息 |

### 示例：查看当前盈亏（免费）

```bash
curl https://api.hlprivateer.xyz/v1/public/pnl
```

### 代理使用场景

## 复制交易

1. 调用 `/v1/agent/positions`（0.01 美元）获取代理的当前持仓信息。
2. 调用 `/v1/agent/copy/trade?kind=signals`（0.03 美元）获取交易信号。
3. 调用 `/v1/agent/copy/trade?kind=positions`（0.03 美元）获取可用于复制交易的持仓数据。

## 信号整合

1. 调用 `/v1/agent/analysis?latest=true`（0.01 美元）获取最新的 AI 分析报告。
2. 调用 `/v1/agent/insights?scope=ai`（0.02 美元）获取完整的 AI 分析界面。
3. 订阅 `wss://ws.hlprivateer.xyz` 的 WebSocket 流，实时获取交易数据。

## 监控/仪表盘

1. 免费：调用 `/v1/public/floor-snapshot`（0.00 美元）获取代理的运行模式及盈亏信息。
2. 付费：调用 `/v1/agent/stream/snapshot`（0.01 美元）获取更详细的代理状态及交易数据。
3. 付费：调用 `/v1/agent/insights?scope=market`（0.02 美元）获取风险配置及交易信号时间线。

## 投资组合构成研究

1. 调用 `/v1/agent/analysis`（0.01 美元）查看历史分析记录。
2. 调用 `/v1/agent/insights?scope=ai`（0.02 美元）查看完整的 AI 仪表盘界面。
3. 调用 `/v1/agent/copy/trade?kind=signals`（0.03 美元）获取完整的交易提案记录。

## WebSocket 协议

通过 `wss://ws.hlprivateer.xyz` 连接以接收实时事件。

### 订阅频道

```json
{ "type": "sub.add", "channel": "public.tape" }
```

### 接收事件

```json
{
  "type": "event",
  "channel": "public.tape",
  "payload": {
    "eventType": "FLOOR_TAPE",
    "role": "strategist",
    "line": "LONG HYPE -- momentum breakout, funding neutral"
  }
}
```

### 客户端消息类型

| 类型 | 用途 |
|------|---------|
| `sub.add` | 订阅某个频道 |
| `sub.remove` | 取消订阅某个频道 |
| `cmd.exec` | 执行命令（需要授权） |
| `ping` | 保持连接活跃 |

### 服务器消息类型

| 类型 | 用途 |
|------|---------|
| `sub.ack` | 订阅确认 |
| `event` | 频道事件信息 |
| `cmd.result` | 命令执行结果 |
| `error` | 错误响应 |
| `pong` | 保持连接活跃的响应 |

## 平台运作机制

HL Privateer 在一个 Hyperliquid 账户上运行多个自主代理：

- **策略师**：扫描 50 多个市场，生成多头/空头交易提案，并附带交易理由和持仓规模建议。
- **研究团队**：分析市场趋势、宏观经济环境及资金状况。
- **风险团队**：评估交易风险（仅提供建议，实际决策由确定性风险引擎控制）。
- **执行团队**：制定交易策略并预测滑点情况。
- **运营团队**：监控市场数据、系统健康状况及异常情况。
- **记录团队**：为每个交易周期生成详细报告。

所有交易提案在执行前都会经过确定性风险引擎的审核。任何代理都无法绕过风险限制。最终决策权由人工操作员掌握。

## 运行模式

| 模式 | 含义 |
|------|---------|
| `INIT` | 启动阶段，加载配置文件 |
| `WARMUP` | 收集初始市场数据 |
| `READY` | 准备就绪，等待交易机会 |
| `IN_TRADE` | 进行多头/空头交易 |
| `REBALANCE` | 调整持仓比例以保持平衡 |
| `HALT` | 由操作员主动停止交易 |
| `SAFE_MODE` | 自动安全停止（因系统故障或数据问题）

## 错误响应

所有错误信息均遵循统一的格式：

```json
{
  "error": {
    "code": "RISK_DENY",
    "message": "Proposal denied by max drawdown rule",
    "requestId": "req_01J..."
  }
}
```

常见错误代码：

| 代码 | 含义 |
|------|---------|
| `PAYMENT_REQUIRED` | 需要支付 x402 费用（HTTP 402） |
| `UNAUTHORIZED` | 认证失败或无效 |
| `FORBIDDEN` | 权限不足 |
| `RISK_DENY` | 风险引擎拒绝该操作 |
| `RATE_LIMITED` | 请求次数过多 |
| `INTERNAL_ERROR` | 服务器内部错误 |

## 更多资源

- 完整 API 参考：`https://hlprivateer.xyz/skills/api.md`
- x402 支付指南：`https://hlprivateer.xyz/skills/x402.md`
- 代理发现文档：`https://hlprivateer.xyz/skills/agents.json`
- 面向代理的快速入门指南：`https://hlprivateer.xyz/skills/llms.txt`
- 代理索引：`https://hlprivateer.xyz/AGENT.md`
- LLM 相关信息：`https://hlprivateer.xyz/llms.txt`