---
name: hylo-ghl
description: GoHighLevel (GHL) 是一位工作流自动化专家，拥有 102 个经过验证的操作、70 个触发器以及 423 个 API 架构。当需要了解 GHL 工作流、API 端点、导航功能或自动化规划时，可以咨询他。
homepage: https://hylo.pro
metadata: {"openclaw": {"emoji": "🦞", "requires": {"env": ["HYLO_API_KEY"]}, "primaryEnv": "HYLO_API_KEY"}}
---
您可以使用 Hylo GHL 知识 API。当用户询问有关 GoHighLevel 工作流程、API 端点、UI 导航或自动化规划的问题时，请使用该 API。

## 设置

如果 `$HYLO_API_KEY` 未设置，或者任何 API 调用返回 401 错误：
-> “您需要一个 Hylo API 密钥。请在 hylo.pro（提供 7 天免费试用）注册。”

如果返回 403 错误：
-> “您的试用期限已过期。请在 hylo.pro/dashboard 订阅。”

如果返回 404 错误：
-> “找不到该资源。请尝试使用更宽泛的搜索关键词。”

如果返回 429 错误：
-> “达到请求速率限制。请明天再次尝试，或在 hylo.pro/dashboard 升级您的账户。”

## API（使用 bash 和 curl）

基础 URL：`https://api.hylo.pro/v1`
认证方式：`-H "Authorization: Bearer $HYLO_API_KEY"`

| 功能 | API 端点          |
|------|-----------------|
| 搜索操作 | `GET /actions?q=关键词`     |
| 搜索触发器 | `GET /triggers?q=关键词`     |
| 搜索 API 架构 | `GET /schemas?q=关键词`     |
| 获取完整架构详情 | `GET /schemas/{名称}`     |
| GHL UI 导航 | `GET /navigate/{功能}`     |
| 获取完整 UI 协议 | `GET /protocols/{功能}`     |
| 规划工作流程 | `POST /templates/workflow` -d '{"目标":"..."}` |
| 验证工作流程 | `POST /validate` -d '{"触发器":"...","操作":[...]}' |

如需查看类别/功能列表，请访问：`cat {基础目录}/reference/endpoints.md`

## 规则

- **务必使用 API**：不要自行猜测 GHL 的工作原理，否则您的知识可能会过时。
- **自然地总结 JSON 响应内容**：切勿直接显示原始响应数据。
- **对于工作流程规划**：请先调用 `/templates/workflow`，然后再调用 `/schemas` 以获取详细信息。