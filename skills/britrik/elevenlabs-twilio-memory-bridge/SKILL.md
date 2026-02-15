---
name: elevenlabs-twilio-memory-bridge
version: "1.0.0"
author: britrik
description: "FastAPI个性化Webhook：为Twilio上的ElevenLabs对话式AI代理添加持久化的调用者信息及动态上下文注入功能。该Webhook不支持音频代理，采用基于文件的持久化存储方式，并兼容OpenClaw框架。"
tags: ["elevenlabs", "twilio", "voice-agent", "telephony", "conversational-ai", "memory-injection", "fastapi"]
emoji: ":telephone_receiver:"
---

# elevenlabs-twilio-memory-bridge

这是一个用于 ElevenLabs 与 Twilio 语音代理的个性化 Webhook 服务，可持久化存储来电者的信息。

## 功能介绍

当有电话拨打到您的 Twilio 号码时，ElevenLabs 的原生集成会触发该 Webhook。该服务会查询来电者的历史记录、长期存储的信息以及每日上下文笔记，将这些数据与可定制的模板结合后，作为系统提示返回给代理，从而使代理能够根据每个来电者的具体情况进行问候。

## 架构特点

- **无音频代理**：ElevenLabs 和 Twilio 直接处理音频数据。
- **仅使用 Webhook**：每次来电时仅触发一次 Webhook 以注入上下文信息。
- **基于文件的持久化存储**：数据存储在 `./data/` 目录下的 JSON 文件中，完全不依赖外部服务。
- **兼容 OpenClaw**：可与任何支持 OpenAI 的大型语言模型（LLM）端点配合使用。

## 端点说明

| 端点          | 方法       | 功能                |
|------------------|-----------|----------------------|
| `/webhook/personalize` | POST      | ElevenLabs 在来电时调用此端点           |
| `/webhook/post-call` | POST      | 可选的通话后清理操作           |
| `/api/memory/{phone_hash}` | POST      | 为来电者添加长期存储的信息         |
| `/api/notes`     | POST      | 添加全局或特定于来电者的上下文笔记       |
| `/health`      | GET       | 服务健康检查              |

## 设置步骤

1. 克隆项目仓库，然后运行 `pip install -r requirements.txt` 安装依赖项。
2. 将 `.env.example` 文件复制到 `.env` 文件中，并填写相应的秘密信息。
3. 在 ElevenLabs 代理的配置中，将自定义大型语言模型（Custom LLM）设置为指向您的 OpenClaw 实例。
4. 在代理的安全设置中启用系统提示和首条消息的个性化功能。
5. 在 ElevenLabs 的设置中添加 Webhook 地址 `https://your-domain/webhook/personalize`。
6. 在 ElevenLabs 的控制面板中添加您的 Twilio 号码。
7. 运行命令 `uvicorn app:app --host 0.0.0.0 --port 8000` 以启动服务器。

## 所需的环境变量

- `ELEVENLABS_API_KEY`：ElevenLabs 的 API 密钥。
- `ELEVENLABS_AGENT_ID`：您的代理 ID。
- `OPENCLAW_API_BASE_URL`：您的 OpenClaw 实例的 URL。
- `PUBLIC_BASE_URL`：该服务的公开访问地址。

## 安全性措施

- 所有来电者的电话号码在存储或记录之前都会经过 SHA-256 哈希处理。
- 所有敏感信息仅从环境变量中读取。
- 支持可选的 HMAC Webhook 签名验证。
- 该服务适合托管在公开的 GitHub 仓库中，源代码中不包含任何敏感信息。