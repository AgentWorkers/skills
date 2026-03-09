---
name: skill-hub-gateway
description: 统一网关技能，用于异步执行和轮询工作流程。
version: 2.1.2
metadata:
  openclaw:
    skillKey: skill-hub-gateway
    emoji: "🧩"
    homepage: https://gateway.binaryworks.app
    requires:
      bins:
        - node
---
# Skill Hub Gateway

默认 API 基本 URL：`https://gateway-api.binaryworks.app`

中文文档：`SKILL.zh-CN.md`

## 首次使用（install_code）

脚本会自动完成以下入职流程：

1. 发送 `POST` 请求到 `/agent/install-code/issue`，请求参数包含 `{"channel":"local"}` 或 `{"channel":"clawhub"}`。
2. 读取 `data.install_code` 数据。
3. 发送 `POST` 请求到 `/agent/bootstrap`，请求参数包含 `{"agent_uid":"<agent_uid>","install_code":"<install_code>"}`。
4. 读取 `data.api_key`，然后使用 `X-API-Key` 或 `Authorization: Bearer <api_key>` 来调用运行时 API。

**手动覆盖方式：**
- 你仍然可以显式提供 `api_key`。
- 如果 `SKILL_API_KEY` 存在，脚本会在自动启动之前使用它。

## 运行时合约（V2）

- 执行操作：`POST /skill/execute`
- 查询执行结果：`GET /skill/runs/:run_id`
- 对于图像处理功能，`image_url` 必须是直接的图像文件 URL（响应的 `Content-Type` 应为 `image/*`），不能是网页 URL。
- 端口状态：`succeeded` 或 `failed`
- 当状态为 `succeeded` 时，返回执行结果 `output`。
- 当状态为 `failed` 时，返回错误信息（包含 `code` 和 `message`）。

## 功能 ID

- `human_detect`
- `image_tagging`
- `tts_report`
- `embeddings`
- `reranker`
- `asr`
- `tts_low_cost`
- `markdown_convert`

## 搭配使用的文件

- `scripts/execute.mjs`（命令行参数：`[api_key] [capability] [input_json] [base_url] [agent_uid] [owner_uid_hint]`)
- `scripts/poll.mjs`（命令行参数：`[api_key] <run_id> [base_url] [agent_uid] [owner_uid_hint]`)
- `scripts/runtime-auth.mjs`（用于共享的自动启动和身份验证辅助功能）
- `references/capabilities.json`
- `references/openapi.json`
- `SKILL.zh-CN.md`