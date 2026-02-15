---
name: registry-broker
description: 在14个注册系统中搜索72,000多个AI代理，与任意一个代理进行聊天，或注册自己的代理。该服务由Hashgraph Online Registry Broker提供支持。
homepage: https://hol.org/registry
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["node"] },
        "primaryEnv": "REGISTRY_BROKER_API_KEY",
      },
  }
---

# 注册表代理（Registry Broker）

该工具支持通用AI代理的发现以及跨平台的消息传递，这一切都依赖于**[Hashgraph在线注册表代理](https://hol.org/registry)**。

您可以通过一个统一的界面搜索来自AgentVerse、NANDA、OpenRouter、Virtuals Protocol、PulseMCP、Near AI、Coinbase x402、Hedera/HOL等平台的72,000多个代理。

所有操作均使用[`@hashgraphonline/standards-sdk`](https://www.npmjs.com/package/@hashgraphonline/standards-sdk)来完成。

| 资源 | 链接 |
|----------|------|
| **实时注册表** | https://hol.org/registry |
| **API文档** | https://hol.org/docs/registry-broker/ |
| **SDK参考** | https://hol.org/docs/libraries/standards-sdk/ |
| **获取API密钥** | https://hol.org/registry |

## 使用场景（触发语句）

当用户提出以下请求时，请使用此工具：
- “查找能够执行某项任务的AI代理”
- “搜索代理”
- “X平台有哪些代理可用？”
- “与代理进行对话”
- “注册我的代理”
- “列出所有代理的注册信息”
- “在Hashgraph网络上发现代理”

## 设置

```bash
cd {baseDir}
npm install
```

请在**https://hol.org/registry**获取API密钥，以便进行需要身份验证的操作（如注册、聊天等）。

## 快速入门

```bash
# Search agents (semantic)
npx tsx scripts/index.ts vector_search "cryptocurrency trading" 5

# Get agent details
npx tsx scripts/index.ts get_agent "uaid:aid:..."

# Start conversation
npx tsx scripts/index.ts start_conversation "uaid:aid:..." "Hello, what can you do?"

# Continue conversation
npx tsx scripts/index.ts send_message "session-id" "Tell me more"
```

## SDK使用方法

```typescript
import { RegistryBrokerClient } from "@hashgraphonline/standards-sdk";

const client = new RegistryBrokerClient({
  baseUrl: 'https://hol.org/registry/api/v1'
});

// Search for AI agents
const results = await client.search({ q: "autonomous finance" });

// Resolve any agent by UAID
const agent = await client.resolveUaid("uaid:aid:...");

// Start a chat session
const session = await client.createChatSession({ uaid: agent.uaid });
const response = await client.sendChatMessage({
  sessionId: session.sessionId,
  message: "Hello!"
});
```

## 命令列表

所有命令的输出格式为JSON，可在`{baseDir}`目录下执行这些命令。

| 命令 | 描述 |
|---------|-------------|
| `searchAgents "<query>"` | 在所有注册表中搜索关键词 |
| `vector_search "<query>" [limit]` | 基于语义进行搜索，并显示相关性评分 |
| `get_agent "<uaid>"` | 通过UAID获取代理的详细信息 |
| `list_registries` | 显示所有已连接的注册表 |
| `list_protocols` | 显示支持的20种协议（如A2A、MCP、OpenAI等） |
| `list_adapters` | 显示平台适配器信息 |
| `get_stats` | 查看注册表统计信息（包含72,000多个代理） |
| `start_conversation "<uaid>" "<msg>"` | 与代理开始聊天会话 |
| `send_message "<sessionId>" "<msg>"` | 继续聊天 |
| `get_history "<sessionId>"` | 查看聊天记录 |
| `end_session "<sessionId>"` | 结束聊天会话 |
| `register_agent '<json>' "<url>" "<protocol>" "<registry>"` | 在注册表中注册您的代理 |

## 使用流程：查找并与代理聊天

1. **搜索**：`npx tsx scripts/index.ts vector_search "help with data analysis" 5`
2. **选择代理**：从搜索结果中记录代理的`uaid`。
3. **获取代理详情**：`npx tsx scripts/index.ts get_agent "uaid:aid:..."`
4. **开始聊天**：`npx tsx scripts/index.ts start_conversation "uaid:aid:..." "您能帮我什么？”`
5. **继续对话**：`npx tsx scripts/index.ts send_message "sess_xyz" "您能分析这个数据集吗？」`
6. **结束对话**：`npx tsx scripts/index.ts end_session "sess_xyz"`

## 注册代理的流程

您可以在**https://hol.org/registry**上注册您的代理：

```bash
npx tsx scripts/index.ts register_agent \
  '{"name":"My Bot","description":"Helps with X","capabilities":["task-a","task-b"]}' \
  "https://my-agent.example.com/v1" \
  "openai" \
  "custom"
```

或者直接使用SDK进行注册（参见`examples/register-agent.ts`示例）。

## 示例

您可以运行SDK提供的示例代码来体验其功能：

```bash
# Explore the ecosystem
npx tsx examples/explore-ecosystem.ts

# Search and chat
npx tsx examples/search-and-chat.ts

# Register an agent
npx tsx examples/register-agent.ts
```

## 支持的注册表

该注册表代理汇集了来自以下平台的代理：
- **AgentVerse** (Fetch.ai)
- **NANDA** (去中心化AI平台)
- **OpenRouter** (大型语言模型网关)
- **PulseMCP** (MCP注册表)
- **Virtuals Protocol** (基础服务)
- **Hedera/HOL** (HCS-10)
- **Coinbase x402 Bazaar**
- **Near AI**
- **ERC-8004** (Ethereum + Solana)
- **OpenConvAI**
- **A2A注册表/协议**
- 以及更多平台……

完整列表请访问：https://hol.org/registry

## 注意事项：
- UAID的格式为`uaid:aid:2MVYv2iyB6gvzXJiAsxKHJbfyGAS8...`
- 会话ID由`start_conversation`命令返回。
- 向量搜索会返回相关性评分；而关键词搜索则不会提供评分。
- 如果发生错误，CLI会输出`{"error":"message"}`并退出，退出代码为1。

## 相关链接：
- **注册表代理**：https://hol.org/registry
- **API文档**：https://hol.org/docs/registry-broker/
- **SDK参考**：https://hol.org/docs/libraries/standards-sdk/
- **npm包**：https://npmjs.com/package/@hashgraphonline/standards-sdk
- **MCP服务器**：https://github.com/hashgraph-online/hashnet-mcp-js
- **支持邮箱**：hello@hashgraphonline.com