---
name: relay-to-agent
description: "**将消息转发到支持OpenAI的API上的AI代理**  
支持与AI代理进行多轮对话，并具备会话管理功能。可以列出所有可用的代理、发送消息以及重置会话状态。"
homepage: https://platform.openai.com/docs/api-reference/chat
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["node"]},"primaryEnv":"RELAY_API_KEY"}}
---

# 中继到代理

可以将消息发送到任何支持 OpenAI 的 AI 代理。该功能兼容 Connect Chat、OpenRouter、LiteLLM、vLLM、Ollama 以及任何实现了 Chat Completions API 的服务。

## 可用的代理列表

```bash
node {baseDir}/scripts/relay.mjs --list
```

## 向代理发送消息

```bash
node {baseDir}/scripts/relay.mjs --agent linkedin-alchemist "Transform this article into a LinkedIn post"
```

## 多轮对话

```bash
# First message
node {baseDir}/scripts/relay.mjs --agent connect-flow-ai "Analyze our latest campaign"

# Follow-up (same session, agent remembers context)
node {baseDir}/scripts/relay.mjs --agent connect-flow-ai "Compare with last month"
```

## 重置会话

```bash
node {baseDir}/scripts/relay.mjs --agent linkedin-alchemist --reset "Start fresh with this article..."
```

## 选项

| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `--agent ID` | 目标代理的标识符 | （必填） |
| `--reset` | 在发送消息前重置对话 | 关闭 |
| `--list` | 列出可用的代理 | — |
| `--session ID` | 自定义会话标识符 | `default` |
| `--json` | 原始 JSON 输出 | 关闭 |

## 配置

### agents.json

在 `{baseDir}/agents.json` 文件中配置代理和端点：

```json
{
  "baseUrl": "https://api.example.com/v1",
  "agents": [
    {
      "id": "my-agent",
      "name": "My Agent",
      "description": "What this agent does",
      "model": "model-id-on-the-api"
    }
  ]
}
```

### 环境变量

```bash
export RELAY_API_KEY="sk-..."          # API key (required)
export RELAY_BASE_URL="https://..."    # Override base URL from config
export RELAY_CONFIG="/path/to/agents.json"  # Custom config path
```

## 兼容的服务

- **Connect Chat** — `api.connectchat.ai/api`
- **OpenRouter** — `openrouter.ai/api/v1`
- **LiteLLM** — `localhost:4000/v1`
- **vLLM** — `localhost:8000/v1`
- **Ollama** — `localhost:11434/v1`
- **任何支持 OpenAI 的 API**

## 会话管理

会话数据存储在本地文件 `~/.cache/relay-to-agent/sessions/` 中。每个代理和会话的组合最多可以保存 50 条消息。使用 `--session` 参数可以与同一代理进行多轮对话。