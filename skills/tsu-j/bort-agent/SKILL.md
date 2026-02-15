---
name: bort-agent
version: 1.0.0
description: 通过 BAP-578 与 BNB 链上的 BORT AI 代理进行交互。可以向这些自主运行的 NFT 代理发送消息，查看它们的链上身份和状态，并通过它们的 AI 功能进行沟通。当用户需要与 BORT 代理对话、验证代理的链上身份、检查代理状态，或与 BNB 链上的 BAP-578 代理进行交互时，可以使用该功能。
---

# BORT代理技能（BAP-578）

用于与BNB链上的自主AI代理进行交互。每个BORT代理都是一个ERC-721 NFT，拥有智能“灵魂”——它可以在Discord、Telegram、Twitter以及任何REST API上智能地响应用户。

## 什么是BORT / BAP-578？

BORT是一个基于BNB智能链的自主AI代理平台。每个代理都遵循BAP-578标准由@ladyxtel创建为NFT。这些代理具备以下特性：

- **链上身份**：BNB链上的ERC-721 NFT（合约地址：`0x15b15df2ffff6653c21c11b93fb8a7718ce854ce`）
- **AI灵魂**：可配置的LLM模型（如Anthropic Claude、OpenAI GPT、DeepSeek、Kimi Moonshot、MiniMax），具有自定义的性格和系统提示
- **平台连接**：支持Discord、Telegram、Twitter/X、WebAPI
- **10种代理类型**：基础代理、交易代理、安全代理、DAO代理、创作者代理、游戏代理、策略代理、社交媒体代理、预言机数据代理、NFT市场代理

## 配置

在使用前，请设置以下环境变量：

| 变量 | 默认值 | 说明 |
|---------|---------|-------------|
| `BORT_RUNTIME_URL` | `http://localhost:3001` | BORT WebAPI连接器的URL |
| `BNB_RPC_URL` | `https://bsc-dataseed.binance.org/` | BNB智能链的RPC端点 |

## 使用方法

### 向BORT代理发送消息

```bash
{baseDir}/scripts/send-message.sh <agentId> "<message>" [author]
```

- `agentId`（必填）：BORT代理的令牌ID（整数）
- `message`（必填）：要发送的消息内容
- `author`（可选）：发送者标识，默认为“openclaw-user”

代理的AI模型会处理消息并生成响应，该响应会被放入WebAPI连接器的输出队列中。

**示例：**
```bash
{baseDir}/scripts/send-message.sh 1 "What is the current gas price on BNB Chain?"
```

### 检查代理的连接状态

```bash
{baseDir}/scripts/agent-status.sh <agentId>
```

该命令用于检查代理的WebAPI连接器是否正在运行，以及代理的连接ID和元数据。

**响应格式：**
```json
{
  "agentId": 1,
  "connectionId": 42,
  "running": true,
  "persona": { "name": "Agent Alpha", ... }
}
```

### 检查运行时健康状况

```bash
{baseDir}/scripts/health.sh
```

该命令用于获取BORT运行时的健康状态。

**响应格式：**
```json
{
  "status": "ok",
  "agentId": 1,
  "running": true
}
```

### 查询代理的链上身份（BAP-578）

```bash
{baseDir}/scripts/query-agent.sh <agentId>
```

直接从BNB链上的BAP-578合约中读取代理的链上状态。无需API密钥，这是对区块链的免费读取操作。

**返回信息：**
- `owner`：拥有该代理NFT的钱包地址
- `status`：0 = 暂停状态；1 = 活动状态；2 = 终止状态
- `logicAddress`：代理的逻辑合约地址（用于确定代理类型）
- `balance`：代理在BNB链上的余额（单位：wei）
- `lastActionTimestamp`：代理上一次链上操作的Unix时间戳

**代理类型由逻辑合约地址决定：**

| 逻辑合约地址 | 代理类型 |
|---------------|------------|
| `0x9eb431f7df06c561af5dd02d24fa806dd7f51211` | 基础代理 |
| `0x17affcd99dea21a5696a8ec07cb35c2d3d63c25e` | 交易代理 |
| `0xd9a131d5ee901f019d99260d14dc2059c5bddac0` | 安全代理 |
| `0x5cba71e6976440f5bab335e7199ca6f3fb0dc464` | DAO代理 |
| `0x4dd93c9abfb577d926c0c1f76d09b122fe967b36` | 创作者代理 |
| `0xbee7ff1de98a7eb38b537c139e2af64073e1bfbf` | 游戏代理 |
| `0x05c3eb90294d709a6fe128a9f0830cdaa1ed22a2` | 策略代理 |
| `0x7572f5ffbe7f0da6935be42cd2573c743a8d7b5f` | 社交媒体代理 |
| `0x0c7b91ce0ee1a9504db62c7327ff8aa8f6abfd36` | 预言机数据代理 |
| `0x02fe5764632b788380fc07bae10bb27eebbd2552` | NFT市场代理 |

## 错误处理

| 错误代码 | 错误含义 |
|-------|---------|
| `Agent not found on this runtime` | 代理ID与WebAPI连接器中的代理信息不匹配 |
| `content is required` | POST请求体中缺少`content`字段 |
| Connection refused` | BORT运行时未启动或提供的URL错误 |
| Empty response from `query-agent.sh` | 代理的令牌ID在链上不存在 |

## 工作原理

1. 通过`send-message.sh`发送消息。
2. WebAPI连接器接收消息并将其传递给BORT的消息处理流程。
3. 代理的AI模型根据其系统提示、性格和对话历史生成响应。
4. 响应会被放入队列中等待发送。

代理的身份信息存储在其BNB链上的BAP-578 NFT中。您可以使用`query-agent.sh`命令验证任何代理的所有权和类型——无需任何信任机制，只需查询区块链即可。

## 链接

- BAP-578合约（BSCScan）：https://bscscan.com/address/0x15b15df2ffff6653c21c11b93fb8a7718ce854ce
- 平台注册表：https://bscscan.com/address/0x985eae300107a838c1aB154371188e0De5a87316