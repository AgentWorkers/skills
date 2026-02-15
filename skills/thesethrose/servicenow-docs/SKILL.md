---
name: servicenow-docs
description: 搜索并获取 ServiceNow 的文档、发布说明以及开发者文档（包括 API、参考资料和指南）。通过 Zoomin 使用 docs.servicenow.com，以及通过 developer.servicenow.com 的 API 来获取与开发者相关的内容。
metadata:
  clawdbot:
    emoji: "📘"
    read_when:
      - Answering questions about ServiceNow features, APIs, or scripting
      - Looking up release notes or patch information
      - Finding documentation for GlideRecord, GlideAjax, workflows, etc.
      - Researching ServiceNow platform capabilities
---

# ServiceNow 文档技能

该技能用于从 `docs.servicenow.com` 和 `developer.servicenow.com` 网站中搜索和检索文档。它提供了对 ServiceNow 的发布说明、平台文档以及面向开发者的 API 参考和指南的访问权限。

## 使用场景

当用户询问以下内容时，可以使用此技能：
- ServiceNow API 文档（如 GlideRecord、GlideAjax、GlideQuery 等）
- 发布说明、补丁或新功能
- 平台配置或管理
- 脚本编写模式或最佳实践
- 可访问性、用户界面或用户偏好设置
- 任何 ServiceNow 产品或功能的文档
- 开发者相关主题，如 openFrameAPI、ScriptLoader、spContextManager 或移动 API

## 工具

### servicenow_search
用于搜索 ServiceNow 的文档数据库。

**参数：**
- `query`（字符串，必填）- 搜索关键词（例如：“GlideRecord”、“accessibility preferences”、“patch notes”）
- `limit`（数字，默认值：10）- 返回的最大结果数量
- `version`（字符串，可选）- 按版本过滤（例如：“Washington DC”、“Zurich”、“Yokohama”）

**示例：**
```json
{"query": "GlideAjax client script", "limit": 5}
```

### servicenow_get_article
用于获取文档文章的完整内容。

**参数：**
- `url`（字符串，必填）- 文章的 URL（会自动转换为 `docs.servicenow.com`）

**示例：**
```json
{"url": "https://docs.servicenow.com/bundle/zurich-release-notes/page/release-notes/quality/zurich-patch-5.html"}
```

### servicenow_list_versions
列出所有可用的 ServiceNow 文档版本/发布信息。

**参数：** 无

### servicenow_latest_release
获取最新 ServiceNow 版本的发布说明（系统会自动检测最新版本）。

**参数：** 无

### servicenow_dev_suggest
从 ServiceNow 开发者文档中提供自动完成建议。

**参数：**
- `term`（字符串，必填）- 部分搜索词（例如：“Gli”、“openFrame”、“spCon”）

**示例：**
```json
{"term": "openFrame"}
```

### servicenow_dev_search
用于搜索 ServiceNow 开发者文档（API、指南、参考资料）。返回 API 参考页面的 URL。

**参数：**
- `query`（字符串，必填）- 搜索关键词（例如：“openFrameAPI”、“spContextManager”）
- `limit`（数字，默认值：10）- 返回的最大结果数量

**示例：**
```json
{"query": "ScriptLoader", "limit": 5}
```

### servicenow_dev_guide
根据路径获取 ServiceNow 开发者指南。适用于 PDI 指南、开发者程序文档等。

**参数：**
- `path`（字符串，必填）- 指南路径（例如：“developer-program/getting-instance-assistance”、“pdi-guide/requesting-an-instance”）
- `release`（字符串，默认值：“zurich”）- 发布版本

**示例：**
```json
{"path": "developer-program/getting-instance-assistance"}
```

## URL 处理

- **搜索 API：** 使用 `servicenow-be-prod.servicenow.com` 上的 Zoomin API 进行搜索
- **用户可见的 URL：** 为了便于阅读，会自动转换为 `docs.servicenow.com`
- **文章内容：** 通过 Zoomin API 端点获取，并附带正确的请求头
- **开发者文档搜索：** 使用 `developer.servicenow.com` 上的 GraphQL 和 databroker 搜索 API
- **开发者文档内容：** 直接从 `developer.servicenow.com` 页面获取

## 示例用法

用户：“ServiceNow 的可访问性设置是什么？”
→ 使用 `servicenow_search` 查找相关文档
→ 使用 `servicenow_get_article` 获取完整内容
→ 向用户总结可访问性设置

用户：“请告诉我最新的 ServiceNow 补丁信息”
→ 使用 `servicenow_latest_release` 获取最新的发布说明
→ 获取并总结补丁详情

用户：“如何使用 openFrameAPI？”
→ 使用 `servicenow_dev_suggest` 或 `servicenow_dev_search` 查找相关的开发者文档
→ 返回 API 参考页面的 URL（需要浏览器访问才能查看完整内容）

用户：“请展示获取实例的 PDI 指南”
→ 使用 `servicenow_dev_guide` 并指定路径 “pdi-guide/requesting-an-instance”
→ 显示完整的指南内容

## 使用的 API

- **Zoomin 搜索 API：** `https://servicenow-be-prod.servicenow.com/search`
- **内容来源：** `docs.servicenow.com`（通过 Zoomin API 访问）
- **开发者搜索 API：** `https://developer.servicenow.com/api/now/uxf/databroker/exec`
- **开发者建议 API：** `https://developer.servicenow.com/api/nowgraphql`
- **开发者指南 API：** `https://developer.servicenow.com/api/snc/v1/guides`（公开访问，无需认证）

## 限制

- **API 参考内容：** `developer.servicenow.com` 上的 API 参考页面需要浏览器访问。`servicenow_dev_search` 仅返回 URL，无法获取完整的 API 文档内容。
- **指南内容：** 可以通过 `servicenow_dev_guide` 无需认证即可完整获取指南内容。