---
name: voice.ai-voice-agents
title: "Voice.ai Voice Agents"
description: >
  Create, manage, and deploy Voice.ai conversational AI agents.
  Use when the user wants to work with voice agents, list their agents, create new ones, or manage agent configurations.
---

# Voice.ai 语音助手

使用 Voice.ai 的 Agent API 构建最佳的对话式 AI 语音助手。

## ✨ 主要功能

- **语音助手管理**：创建、更新和删除语音助手
- **一键部署**：立即将助手部署用于电话通话
- **知识库**：基于 RAG（Retrieval, Augmentation, and Generation）技术的助手，支持自定义知识
- **MCP 集成**：通过 MCP 将助手连接到外部工具
- **电话号码**：管理来电/去电号码
- **分析**：跟踪通话记录和助手性能

## ⚙️ 配置

### 获取 API 密钥

1. 访问 [Voice.ai 开发者控制台](https://voice.ai/app/dashboard/developers)
2. 登录或创建账户
3. 生成新的 API 密钥
4. 仔细复制并保存密钥

### 设置身份验证（三种方法）

**方法 1：环境变量（推荐）**
```bash
export VOICE_AI_API_KEY="your-api-key-here"
```

**方法 2：.env 文件**
```bash
# Create .env file in project root
echo 'VOICE_AI_API_KEY=your-api-key-here' >> .env
```

**方法 3：OpenClaw 配置**
```json
{
  "skills": {
    "voice.ai-voice-agents": {
      "api_key": "your-api-key-here"
    }
  }
}
```

## 🔐 在执行任何操作之前

> **重要提示：** 在运行任何命令之前，请务必验证身份验证。

```bash
# 1. Check if API key is set
echo $VOICE_AI_API_KEY

# 2. Test connection (list agents)
node scripts/agent.js list

# 3. If errors, re-export your key
export VOICE_AI_API_KEY="your-api-key-here"
```

### 自动初始化

设置 API 密钥后，SDK 会自动初始化。无需手动设置。

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

| 参数              | 默认值 | 描述                          |
|------------------------|---------|--------------------------------------|
| llm_model              | gemini-2.5-flash-lite | 用于生成回答的 LLM 模型 |
| llm_temperature        | 0.7     | 回答的创造性（0-2）            |
| max_call_duration      | 900     | 最大通话时长（秒）           |
| allow_interruptions    | true    | 允许用户打断助手            |
| auto_noise_reduction   | true    | 过滤背景噪音              |

## 🎙️ 文本转语音（TTS）设置

| 参数   | 默认值 | 描述                    |
|-------------|---------|--------------------------------|
| voice_id    | -       | 助手的语音 ID              |
| model       | auto    | 选择的 TTS 模型              |
| language    | en      | 语言代码                  |
| temperature | 1.0     | 语音表达力（0-2）             |
| top_p       | 0.8     | 采样参数（0-1）               |

## 🌍 支持的语言

`auto`, `en`, `ca`, `sv`, `es`, `fr`, `de`, `it`, `pt`, `pl`, `ru`, `nl`

## 💻 命令行接口（CLI）用法

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

## 🤖 OpenClaw 集成

### JSON 配置

```json
{
  "name": "voice.ai-voice-agents",
  "enabled": true,
  "config": {
    "api_key": "${VOICE_AI_API_KEY}",
    "default_model": "gemini-2.5-flash-lite",
    "auto_deploy": false
  }
}
```

### 聊天触发词

当您提到以下内容时，OpenClaw 会自动激活此技能：
- “voice agent”（语音助手）
- “voice bot”（语音机器人）
- “create agent”（创建助手）
- “deploy agent”（部署助手）
- “list agents”（列出助手）
- “Voice.ai”（Voice.ai）
- “voice ai”（语音 AI）

## 🗣️ 用户友好语言

| 用户输入       | 助手响应                         |
|-------------------|--------------------------------------|
| “Create a support agent” | 创建以支持为主题的助手           |
| “Show my agents” | 显示所有助手的状态                   |
| “Deploy the agent” | 部署助手用于电话通话                   |
| “Update the greeting” | 更新助手的问候语                   |
| “Delete the test agent” | 删除指定的助手                   |
| “What agents do I have?” | 以友好的格式列出所有助手                   |
| “Make an FAQ bot” | 创建基于 FAQ 模板的助手                   |
| “Connect to my MCP server” | 配置 MCP 集成                         |

## 📁 项目文件

| 文件          | 用途                         |
|------------|--------------------------------------|
| `SKILL.md`     | 文档和 OpenClaw 技能定义                   |
| `voice-ai-agents.yaml` | API 配置、模型和默认值                   |
| `voice-ai-agents-sdk.js` | 包含所有 API 方法的完整 SDK                   |
| `scripts/agent.js`   | 命令行接口                         |

## ❌ 错误处理

| 错误代码 | 原因 | 解决方案                         |
|------------|-------------------|-----------------------------------------|
| `401 Unauthorized` | API 密钥无效或缺失 | 确保 `VOICE.AI_API_KEY` 设置正确                   |
| `403 Forbidden` | API 密钥权限不足 | 生成具有适当权限的新密钥                   |
| `404 Not Found` | 助手 ID 不存在 | 运行 `list` 命令获取有效的助手 ID                   |
| `429 Too Many Requests` | 超过请求限制 | 等待 60 秒后重试                   |
| `500 Server Error` | Voice.ai API 故障 | 查看 [状态页面](https://status.voice.ai)                   |
| `ENOTFOUND` | 网络错误 | 检查网络连接                     |
| `Agent not deployed` | 助手存在但未激活 | 运行 `deploy --id <agent_id>`                   |

### 优雅的错误信息

SDK 提供用户友好的错误信息：
```
❌ Authentication failed. Please check your API key.
   Get one at: https://voice.ai/app/dashboard/developers

❌ Agent "support-bot" not found. 
   Run 'node scripts/agent.js list' to see available agents.

❌ Rate limit reached. Please wait 60 seconds before retrying.
```

## 📝 触发词

以下短语可在 OpenClaw 中激活 Voice.ai 语音助手技能：

| 类别            | 触发词                          |
|-----------------|-----------------------------------------|
| **创建**       | “create voice agent”                | 创建语音助手                         |
| **列出**       | “show agents”                    | 显示所有助手                         |
| **部署**       | “deploy agent”                    | 部署助手                         |
| **更新**       | “update agent”                    | 更新助手配置                         |
| **删除**       | “delete agent”                    | 删除助手                         |
| **信息**       | “agent details”                  | 查看助手详细信息                         |

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

向您的助手添加自定义知识：

```bash
# Create agent with knowledge base
node scripts/agent.js create --name "FAQ Bot" --kb-id 123
```

## 🔗 链接

- [获取 API 密钥](https://voice.ai/app/dashboard/developers) | 从这里开始！
- [Voice Assistant 使用指南](https://voice.ai/docs/guides/voice-agents/quickstart)
- [助手 API 参考](https://voice.ai/docs/api-reference/agent-management/create-agent)
- [状态页面](https://status.voice.ai)

## 📋 更新日志

| 版本 | 日期 | 更改内容                         |
|---------|-------------------------|-----------------------------------------|
| 1.0.0 | 2026-01-31 | 首次发布，包含完整的助手管理功能           |

---

由 [Nick Gill](https://github.com/gizmoGremlin) 用 ❤️ 制作