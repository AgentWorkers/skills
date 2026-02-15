---
name: apollo
description: 与 Apollo.io REST API 进行交互（包括人员/组织信息的补充、搜索以及列表管理等功能）。
metadata: {"clawdbot":{"emoji":"🛰️","os":["darwin","linux"]}}
---

# Apollo.io

通过 REST API 与 Apollo.io 进行交互。

## 配置

创建 `config/apollo.env` 文件（示例文件位于 `config/apollo.env.example`）：

- `APOLLO_BASE_URL`（通常为 `https://api.apollo.io`）
- `APOLLO_API_KEY`

这些脚本会自动加载这些配置信息。

## 命令

### 低级辅助工具

- GET 请求：`skills/apollo/scripts/apollo-get.sh "/api/v1/users"`（端点可用性可能有所不同）
- 人员搜索（新功能）：`skills/apollo/scripts/apollo-people-search.sh "vp marketing" 1 5`
- POST 请求（通用）：`skills/apollo/scripts/apollo-post.sh "/api/v1/mixed_people/api_search" '{"q_keywords":"vp marketing","page":1,"per_page":5}'`

### 数据增强（常用功能）

- 根据域名增强网站/组织的信息：`skills/apollo/scripts/apollo-enrich-website.sh "apollo.io"`
- 获取组织的完整信息（批量操作）：`skills/apollo/scripts/apollo-orgs-bulk.sh "6136480939c707388501e6b9"`

## 注意事项

- Apollo 通过 `X-Api-Key` 头部进行身份验证（这些脚本会自动发送该键）。
- 某些端点需要使用 **master API key** 并且需要付费计划（否则会返回 `403` 错误）。
- 许多端点都实施了速率限制（例如每小时 600 次请求）；请妥善处理 `429` 错误响应。