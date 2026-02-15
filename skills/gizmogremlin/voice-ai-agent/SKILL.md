---
name: voice-ai-agents
description: >
  Create, manage, and deploy Voice.ai conversational AI agents.
  Use when the user wants to work with voice agents, list their agents, create new ones, or manage agent configurations.
---

# Voice.ai 语音助手

使用 Voice.ai 的 Agent API 构建对话式 AI 语音助手。

## ✨ 主要功能

- **助手管理**：创建、更新和删除语音助手
- **一键部署**：立即将助手部署到电话通话中
- **知识库**：基于 RAG（Retrieval, Adaptation, and Generation）技术的助手，支持自定义知识
- **MCP 集成**：通过 MCP 将助手连接到外部工具
- **电话号码**：管理来电/去电号码
- **分析**：跟踪通话记录和助手表现

## 🚀 快速入门

```bash
export VOICE_AI_API_KEY="your-api-key"

# Create an agent
node scripts/agent.js create --name "Support Bot" --prompt "You are a helpful assistant"

# List all agents
node scripts/agent.js list

# Deploy an agent
node scripts/agent.js deploy --id <agent_id>
```

## 🤖 助手配置

| 参数                  | 默认值 | 描述                                        |
|------------------------|---------|--------------------------------------|
| llm_model              | gemini-2.5-flash-lite | 用于生成回复的 LLM 模型                         |
| llm_temperature        | 0.7     | 回复的创造性（0-2）                               |
| max_call_duration      | 900     | 最大通话时长（秒）                                   |
| allow_interruptions    | true    | 允许用户打断助手                                |
| auto_noise_reduction   | true    | 过滤背景噪音                                   |

## 🎙️ 文本转语音（TTS）设置

| 参数            | 默认值 | 描述                                        |
| voice_id    | -       | 助手的语音 ID                                    |
| model       | auto    | 选择的 TTS 模型                                   |
| language    | en      | 语言代码                                      |
| temperature | 1.0     | 语音的表现力（0-2）                                 |
| top_p       | 0.8     | 采样参数（0-1）                                   |

## 🌍 支持的语言

`auto`, `en`, `ca`, `sv`, `es`, `fr`, `de`, `it`, `pt`, `pl`, `ru`, `nl`

## 💻 命令行接口（CLI）使用方法

```bash
# Create a new agent
node scripts/agent.js create --name "My Agent" --prompt "System prompt here" --greeting "Hello!"

# List all agents
node scripts/agent.js list

# Get agent details
node scripts/agent.js get --id <agent_id>

# Update an agent
node scripts/agent.js update --id <agent_id> --prompt "New prompt"

# Deploy an agent
node scripts/agent.js deploy --id <agent_id>

# Pause an agent
node scripts/agent.js pause --id <agent_id>

# Delete an agent
node scripts/agent.js delete --id <agent_id>
```

## 🔗 MCP 服务器集成

将您的助手连接到外部工具：

```javascript
const agent = await client.createAgent({
  name: "MCP Agent",
  config: {
    prompt: "You can use tools to help users",
    mcp_servers: [{
      name: "my-tools",
      url: "https://my-server.com/mcp",
      auth_type: "bearer_token",
      auth_token: "secret"
    }]
  }
});
```

## 📚 知识库（RAG）

为助手添加自定义知识：

```bash
# Create agent with knowledge base
node scripts/agent.js create --name "FAQ Bot" --kb-id 123
```

## 🔗 链接

- [语音助手指南](https://voice.ai/docs/guides/voice-agents/quickstart)
- [Agent API 参考](https://voice.ai/docs/api-reference/agent-management/create-agent)


---

由 [Nick Gill](https://github.com/gizmoGremlin) 用 ❤️ 制作