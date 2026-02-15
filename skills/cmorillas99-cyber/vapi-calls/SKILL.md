---
name: vapi-calls
description: 高级AI语音助手，适用于电话通话。具备说服力、销售能力，可协助预订餐厅、发送提醒以及接收通知等功能。
emoji: 📞
author: César Morillas
version: 1.0.0
license: MIT
repository: https://github.com/vapi-ai/openclaw-vapi-calls
requires:
  env:
    - VAPI_API_KEY
    - VAPI_ASSISTANT_ID
    - VAPI_PHONE_NUMBER_ID
    - WEBHOOK_BASE_URL
  bins:
    - python3
  pip:
    - requests
tools:
  - name: make_vapi_call
    description: Triggers an autonomous AI phone call with a specific mission and waits for the final report.
    parameters:
      type: object
      properties:
        phone_number:
          type: string
          description: "Recipient's phone number (E.164 format, e.g., +34669000000)."
        first_message:
          type: string
          description: "Initial greeting. Use 'DEFAULT' to use the agent's configured greeting."
        system_prompt:
          type: string
          description: "AI instructions. Use 'DEFAULT' to use the agent's configured model/prompt. If custom text is provided, the call will force GPT-4o Mini + endCall tool."
        end_message:
          type: string
          description: "Optional. Final phrase. Use 'DEFAULT' to skip override."
      required: [phone_number, first_message, system_prompt]
---

# Vapi 调用 - 代理指令

使用此技能执行任何需要通过电话进行语音交互的任务。

## 配置与网络要求

⚠️ **重要提示：** 此技能要求您的机器能够被互联网访问，以便接收实时的通话更新。

### 1. 环境变量
在您的 OpenClaw `config.json`（或 Gateway 环境配置文件）中配置以下变量：

- `VAPI_API_KEY`：您的 Vapi 私有 API 密钥。
- `VAPI_ASSISTANT_ID`：要使用的 Vapi 助手的 ID。
- `VAPI_PHONE_NUMBER_ID`：Vapi 电话号码的 ID。
- `WEBHOOK_BASE_URL`：**至关重要。** 该代理可访问的公共 HTTPS URL（例如，`https://my-claw.com` 或 `https://xyz.ngrok-free.app`）。**请不要在 URL 末尾添加斜杠。**
- `WEBHOOK_PORT`（可选）：监听的本地端口（默认值：`4430`）。
- `VAPI_LLM_PROVIDER`（可选）：自定义模式的提供者（默认值：`openai`）。
- `VAPI_LLM_MODEL`（可选）：自定义模式的模型（默认值：`gpt-4o-mini`）。

### 2. 连接设置
您必须将 `WEBHOOK_PORT`（默认值 4430）暴露到互联网上。

**选项 A：Cloudflare Tunnel（推荐）**
`cloudflared tunnel --url http://localhost:4430`

**选项 B：Ngrok**
`ngrok http 4430`

将 `WEBHOOK_BASE_URL` 设置为生成的 URL（例如，`https://random-name.trycloudflare.com`）。

## 使用方法

### 自定义任务（动态）
提供一个特定的 `system_prompt`。系统将自动使用 **GPT-4o Mini** 并启用 **endCall** 工具。AI 将能够自主挂断电话。

### 原生代理（静态）
将 `first_message`、`system_prompt` 和 `end_message` 设置为 `"DEFAULT"`。系统将使用 Vapi 仪表板中定义的配置（模型、语音、提示）。

## 故障排除

- **通话挂断 / 无报告：** 检查 `WEBHOOK_BASE_URL` 是否可以从互联网访问。Python 脚本仅在通话期间在 `WEBHOOK_PORT` 上启动临时服务器。
- **API 400 错误：** 检查您的 `VAPI_PHONE_NUMBER_ID` 和 `VAPI_ASSISTANT_ID` 是否正确。