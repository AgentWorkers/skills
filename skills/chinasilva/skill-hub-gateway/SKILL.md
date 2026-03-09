---
name: skill-hub-gateway
description: 统一网关技能，用于异步执行和轮询工作流。
version: 2.1.2
metadata:
  openclaw:
    skillKey: skill-hub-gateway
    emoji: "🧩"
    homepage: https://gateway.binaryworks.app
    requires:
      env:
        - SKILL_API_KEY
      bins:
        - node
    primaryEnv: SKILL_API_KEY
---
# 技能中心网关（Skill Hub Gateway）

默认 API 基础 URL：`https://gateway-api.binaryworks.app`

中文文档：`SKILL.zh-CN.md`

## 首次使用（install_code）

1. 使用 `{"channel":"local"}` 或 `{"channel":"clawhub"}` 发送 `POST` 请求到 `/agent/install-code/issue`。
2. 读取返回的 `data.install_code` 数据。
3. 使用 `{"agent_uid":"<agent_uid>","install_code":"<install_code>"}` 发送 `POST` 请求到 `/agent/bootstrap`。
4. 读取返回的 `data.api_key`，然后使用 `X-API-Key` 或 `Authorization: Bearer <api_key>` 来调用运行时 API。

## 运行时合约（Runtime Contract, V2）

- 执行：`POST /skill/execute`
- 监控执行进度：`GET /skill/runs/:run_id`
- 对于图像处理功能，`image_url` 必须是直接的图像文件 URL（响应的 `Content-Type` 应为 `image/*`），而不能是网页 URL。
- 状态：`succeeded` 或 `failed`
- 成功时返回 `output`；失败时返回 `error`（包含 `code` 和 `message`）。

## 功能 ID（Capability IDs）

- `human_detect`
- `image_tagging`
- `tts_report`
- `embeddings`
- `reranker`
- `asr`
- `tts_low_cost`
- `markdown_convert`

## 打包文件（Bundled Files）

- `scripts/execute.mjs`（命令行参数：`api_key capability input_json [base_url]`)
- `scripts/poll.mjs`（命令行参数：`api_key run_id [base_url]`)
- `references/capabilities.json`
- `references/openapi.json`
- `SKILL.zh-CN.md`