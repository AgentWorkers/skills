---
name: hylo-ghl
description: GoHighLevel（GHL）是专门用于工作流程自动化的工具，拥有102个经过验证的操作步骤（actions）、70个触发器（triggers）以及494个API规范（API schemas）。当您需要了解关于GHL、GoHighLevel、HighLevel或gohighlevel的工作流程、API端点（API endpoints）、导航系统（navigation）或自动化规划（automation planning）的相关信息时，可以参考该工具。
homepage: https://hylo.pro
metadata: {"openclaw": {"emoji": "🦞", "requires": {"env": ["HYLO_API_KEY"]}, "primaryEnv": "HYLO_API_KEY"}}
---
您可以使用 Hylo GHL 知识 API。当用户询问关于 GoHighLevel（GHL / HighLevel / Go High Level）工作流程、API 端点、用户界面导航或自动化规划的相关内容时，请使用该 API。

## 设置

如果 `$HYLO_API_KEY` 未设置，或者任何 API 调用返回 401 错误：
-> “您需要一个 Hylo API 密钥。请在 hylo.pro 注册（提供 7 天免费试用）。”

如果返回 403 错误：
-> “您的试用期限已过期。请在 hylo.pro/dashboard 订阅服务。”

如果返回 404 错误：
-> “无法找到该资源。请尝试使用更宽泛的搜索词。”

如果返回 429 错误：
-> “达到请求频率限制。请明天再试，或在 hylo.pro/dashboard 升级您的账户。”

## API（使用 bash 和 curl）

基础 URL：`https://api.hylo.pro/v1`
认证方式：`-H "Authorization: Bearer $HYLO_API_KEY"`

| 功能 | API 端点                |
|------|----------------------|
| 搜索操作       | `GET /actions?q=KEYWORD`       |
| 搜索触发器      | `GET /triggers?q=KEYWORD`      |
| 搜索 API 架构     | `GET /schemas?q=KEYWORD`      |
| 获取完整架构详情 | `GET /schemas/{name}`       |
| GHL 用户界面导航   | `GET /navigate/{feature}`       |
| 获取完整用户界面协议 | `GET /protocols/{feature}`       |
| 规划工作流程     | `POST /templates/workflow` -d '{"objective":"..."}' |
| 验证工作流程     | `POST /validate` -d '{"trigger":"...","actions":[...]}' |

如需查看类别/功能列表，请访问：`cat {baseDir}/reference/endpoints.md`

## 规则

- **务必调用 API**——不要自行猜测 GHL 的工作原理，否则您的信息可能会过时。
- **自然地总结 JSON 响应内容**——切勿直接输出原始数据。
- **在规划工作流程时**：请先调用 `/templates/workflow`，然后再调用 `/schemas` 获取详细信息。