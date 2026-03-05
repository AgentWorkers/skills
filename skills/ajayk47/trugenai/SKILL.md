---
name: Trugen AI
description: 使用 Trugen AI 平台的 API 来构建、配置和部署对话式视频代理。当用户需要创建 AI 视频头像、管理知识库、设置 Webhook/回调、将代理嵌入网站、与 LiveKit 集成、配置工具或 MCP（Multi-Channel Platforms）、设置多语言代理，或者将他们自己的 LLM（Large Language Model）集成到 Trugen AI 中时，可以使用此技能。
version: 1.0.1
metadata:
  openclaw:
    requires:
      env:
        - TRUGEN_API_KEY
    primaryEnv: TRUGEN_API_KEY
    homepage: https://docs.trugen.ai/docs/overview
---
# Trugen AI

Trugen AI致力于构建实时对话式视频代理——这些由人工智能驱动的虚拟形象能够在1秒以内的延迟内与用户进行视、听、说和思考等互动。

| | |
|---|---|
| **API基础URL** | `https://api.trugen.ai` |
| **身份验证** | 所有请求中需添加`x-api-key: <your-api-key>`头部 |
| **官方文档** | [docs.trugen.ai](https://docs.trugen.ai/docs/overview) |
| **开发者门户** | [app.trugen.ai](https://app.trugen.ai) |

## 所需凭证

| 变量 | 说明 | 获取途径 |
|----------|-------------|--------------|
| `TRUGEN_API_KEY` | 用于所有Trugen API调用的主API密钥（以`x-api-key`头部形式发送） | [开发者门户](https://app.trugen.ai) |
| `TRUGEN_AVATAR_ID` | （可选）用于LiveKit集成的默认虚拟形象ID | [开发者门户](https://app.trugen.ai) |

> **安全提示**：切勿在客户端代码中暴露`TRUGEN_API_KEY`。对于插件或iFrame嵌入方式，应使用服务器端代理来保护密钥的安全。详情请参阅[references/embedding.md]。

## 平台流程

| 步骤 | 组件 | 功能 |
|------|-----------|----------|
| 1 | **WebRTC** | 双向音视频流传输 |
| 2 | **STT**（Deepgram） | 语音转文本功能 |
| 3 | **对话边界检测** | 自动识别自然对话的开始和结束 |
| 4 | **大语言模型（LLM）**（OpenAI、Groq或自定义） | 生成与上下文相关的回复 |
| 5 | **知识库** | 将答案基于用户数据生成 |
| 6 | **TTS**（ElevenLabs） | 生成自然、富有表现力的语音 |
| 7 | **Huma-01** | 生成包含唇动和微表情的神经虚拟形象 |

## 快速入门

1. 创建代理：`POST /v1/ext/agent` — 详情请参阅[references/agents.md]  
2. 通过iFrame或插件嵌入代理：请参阅[references/embedding.md]  

## API端点概览

| 资源 | 端点 | 参考文档 |
|----------|-----------|-----------|
| **代理** | 创建、获取、列出、更新、删除代理 | [agents.md](references/agents.md) |
| **知识库** | 创建知识库、添加文档、获取、列出、更新知识库/文档 | [knowledge-base.md](references/knowledge-base.md) |
| **模板** | 创建、获取、列出、更新模板 | [templates.md](references/templates.md) |
| **工具与MCP服务器** | 创建/管理函数调用工具和MCP服务器 | [tools-and-mcps.md](references/tools-and-mcps.md) |
| **Webhooks** | 回调事件、数据格式及处理示例 | [webhooks.md](references/webhooks.md) |
| **嵌入** | iFrame、插件集成及虚拟形象ID | [embedding.md](references/embedding.md) |
| **服务提供商/虚拟形象** | 可用的LLM、STT服务、TTS引擎、虚拟形象及语言选项 | [providers-avatars-languages.md](referencesproviders-avatars-languages.md) |
| **提示系统** | 语音提示策略及使用案例 | [prompting-and-use-cases.md](references/prompting-and-use-cases.md) |

## 对话管理

获取已完成会话的文字记录：

`GET /v1/ext/conversation/{id}` — 返回代理ID、状态、文字记录数组及录音URL。

## 工作流程指南

确定用户需求后，查阅相应的参考文档：

| 任务 | 参考文档 |
|------|---------------|
| 创建/管理代理 | [agents.md](references/agents.md) |
| 附加数据/文档 | [knowledge-base.md](references/knowledge-base.md) |
| 在多个代理间复用虚拟形象 | [templates.md](references/templates.md) |
| 从代理调用外部API | [tools-and-mcps.md](references/tools-and-mcps.md) |
| 处理对话事件 | [webhooks.md](references/webhooks.md) |
| 在网站中嵌入代理 | [embedding.md](references/embedding.md) |
| 选择合适的大语言模型/语音/语言 | [providers-avatars-languages.md](referencesproviders-avatars-languages.md) |
| 编写有效的提示语 | [prompting-and-use-cases.md](references/prompting-and-use-cases.md) |

## 开发者资源

| 资源 | 链接 |
|----------|------|
| 官方文档 | [docs.trugen.ai](https://docs.trugen.ai/docs/overview) |
| API参考 | [docs.trugen.ai/api-reference](https://docs.trugen.ai/api-reference/overview) |
| 开发者门户 | [app.trugen.ai](https://app.trugen.ai) |
| 开发者社区（Discord） | [discord.gg/4dqc8A66FJ](https://discord.gg/4dqc8A66FJ) |
| 技术支持 | support@trugen.ai |
| GitHub示例代码 | [trugenai/trugen-examples](https://github.com/trugenai/trugen-examples) |
| 更新日志 | [docs.trugen.ai/changelog](https://docs.trugen.ai/docs/changelog) |