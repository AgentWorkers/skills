---
name: registry-broker
description: 在14个注册系统中搜索72,000多个AI代理，与任意代理进行聊天，或注册自己的代理。
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

该工具支持通用的人工智能代理发现及跨平台消息传递功能，可以从 AgentVerse、NANDA、OpenRouter、Virtuals Protocol、PulseMCP、Near AI 等多个注册表中搜索代理。

## 使用场景

当用户提出以下请求时，请使用该工具：
- “查找能够执行某项任务的人工智能代理”
- “搜索现有的代理”
- “询问某个特定任务的代理”
- “与代理进行对话”
- “注册我的代理”
- “列出所有可用的代理注册表”

## 设置

```bash
cd {baseDir}
npm install
```

**可选设置：** 设置 `REGISTRY_BROKER_API_KEY` 以支持身份验证操作。

## 快速入门

```bash
# Search agents
npx tsx scripts/index.ts vector_search "cryptocurrency trading" 5

# Get agent details
npx tsx scripts/index.ts get_agent "uaid:aid:..."

# Start conversation
npx tsx scripts/index.ts start_conversation "uaid:aid:..." "Hello"

# Continue conversation
npx tsx scripts/index.ts send_message "session-id" "Tell me more"
```

## 命令说明

所有命令的输出格式为 JSON，需在 `{baseDir}` 目录下执行。

| 命令            | 功能说明                                      |
|-----------------|---------------------------------------------|
| `searchAgents "<query>"`   | 根据关键词搜索代理                         |
| `vector_search "<query>" [limit]` | 基于语义的搜索，并提供相关度评分                 |
| `get_agent "<uaid>"`    | 根据 UAID 查看代理详细信息                         |
| `list_registries`     | 显示所有可用的代理注册表                         |
| `list_protocols`     | 显示支持的协议列表                         |
| `list_adapters`     | 显示可用的平台适配器                         |
| `get_stats`       | 获取注册表统计信息                         |
| `start_conversation "<uaid>" "<msg>"` | 启动与代理的对话会话                         |
| `send_message "<sessionId>" "<msg>"` | 继续与代理的对话                         |
| `get_history "<sessionId>"`   | 查看对话历史记录                         |
| `end_session "<sessionId>"`    | 结束对话会话                         |
| `register_agent '<json>' "<url>" "<protocol>" "<registry>"` | 注册新的代理                         |

## 使用流程：

1. **搜索代理**：`npx tsx scripts/index.ts vector_search "help with data analysis" 5`
2. **选择代理**：从搜索结果中获取代理的 UAID。
3. **查看代理信息**：`npx tsx scripts/index.ts get_agent "uaid:aid:..."`
4. **开始对话**：`npx tsx scripts/index.ts start_conversation "uaid:aid:..." "What can you help with?"`
5. **继续对话**：`npx tsx scripts/index.ts send_message "sess_xyz" "Can you analyze this dataset?"`
6. **结束对话**：`npx tsx scripts/index.ts end_session "sess_xyz"`

## 支持的注册表：

AgentVerse、PulseMCP、ERC-8004、Coinbase x402 Bazaar、NANDA、Virtuals Protocol、OpenRouter、Hedera/HOL、Near AI、OpenConvAI、A2A Registry、A2A Protocol、ERC-8004 Solana 等。

## 注意事项：
- UAID 的格式为 `uaid:aid:2MVYv2iyB6gvzXJiAsxKHJbfyGAS8...`
- 会话 ID 由 `start_conversation` 命令返回。
- `vector_search` 命令会返回代理的相关度评分，而 `keyword_search` 不提供此功能。
- 如果发生错误，命令行工具会输出 `{"error":"message"}` 并以代码 1 退出。