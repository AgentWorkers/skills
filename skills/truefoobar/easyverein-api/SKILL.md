---
name: easyverein-api
description: "使用 easyVerein v2.0 的 REST API（包括成员、联系人、事件、发票、预订、自定义字段等）。该 API 提供了全面的接口功能，包括端点发现、身份验证、请求/响应数据结构以及示例 cURL 调用。"
---

# easyVerein API (v2.0)

## 快速入门
- 基本 URL：`https://easyverein.com/api/v2.0`
- 认证头：`Authorization: Bearer <API_KEY>`
- 令牌有效期为 30 天；当响应头中出现 `tokenRefreshNeeded` 时，通过 `GET /api/v2.0/refresh-token` 重新获取令牌。
- 请求速率限制：**每分钟 100 次**。

## 使用 OpenAPI 规范
如需了解端点详情或数据结构，请阅读完整规范：
- `references/openapi-v2.json`

该文件包含了所有端点、参数、请求体、响应内容及相关标签。您可以使用它来：
- 按标签查询端点（例如：`member`、`contact-details`、`invoice`）
- 查看请求体数据结构
- 查找可执行的操作及子端点

## 常见用法模式
- 分页：`?limit=`（默认值 5，最大值 100）
- 字段筛选：`?query={field,relation{subfield}}`
- 排除某些字段：`?query={-field}`
- 批量操作：`bulk-create` / `bulk-update`（部分端点支持批量操作）

## 示例 cURL （模板）
```bash
curl -s \
  -H "Authorization: Bearer $EASYVEREIN_TOKEN" \
  -H "Content-Type: application/json" \
  "https://easyverein.com/api/v2.0/member?limit=10"
```

## 成员创建流程（重要提示）
1) 首先创建 `contact-details` 数据。
2) 然后使用 `emailOrUserName` 以及 `contactDetails` 信息创建 `member`。

## 注意事项
- 文件必须通过 `PATCH` 方法上传，并设置 `Content-Disposition` 头部字段。
- 使用 `refresh-token` 来更新令牌；旧令牌会立即失效。