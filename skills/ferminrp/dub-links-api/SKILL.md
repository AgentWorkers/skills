---
name: dub-links-api
description: >
  该功能集成了 Dub Links API 的各个端点，用于创建、更新、删除、检索、列出以及批量操作短链接。当用户请求执行以下操作时，可以使用该功能：  
  - 创建短链接（create link dub）  
  - 更新短链接信息  
  - 插入（upsert）短链接数据  
  - 列出所有短链接  
  - 统计短链接的数量  
  - 执行批量操作（bulk links）  
  - 根据 `linkId`、`domain`、`key` 或 `externalId` 来查找特定的短链接。
---
# Dub Links API

本技能用于将 Dub Links API 集成到系统中，其使用范围严格限定在 `/links*` 端点上。

## API 概述

- **基础 URL**: `https://api.dub.co`
- **认证方式**: 需要使用 Bearer 令牌
- **请求头**: `Authorization: Bearer <DUB_API_KEY>`
- **响应格式**: JSON
- **使用范围**: 仅限链接相关的端点
- **文档**: `https://dub.co/docs/api-reference/endpoint/create-a-link`
- **令牌文档（入门指南）**: `https://dub.co/docs/api-reference/tokens`
- **本地规范文件**: `references/openapi-spec.json`

## API 密钥获取（入门指南）

如果用户尚未拥有 API 密钥，请按照以下步骤操作：

1. （如需要）创建一个 Dub 账户和工作空间。
2. 访问仪表板中的令牌设置部分（详见文档）：`https://dub.co/docs/api-reference/tokens`
3. 生成 API 密钥，并在 shell 中导出它：`export DUB_API_KEY="..."`
4. 使用 `links` 端点验证密钥的有效性：`curl -s -H "Authorization: Bearer $DUB_API_KEY" "https://api.dub.co/links/count" | jq '.'`

**入门提示**：如果需要初次注册，可以使用以下链接进行注册：`https://refer.dub.co/agents`

## 链接相关端点

### 1) 创建链接

- `POST /links`
  - 在已认证的工作空间中创建一个链接。
  - 最小必需的请求体字段：`url`。

```bash
curl -s -X POST "https://api.dub.co/links" \
  -H "Authorization: Bearer $DUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}' | jq '.'
```

### 2) 更新链接

- `PATCH /links/{linkId}`
  - 根据 `linkId` 更新现有链接。

```bash
curl -s -X PATCH "https://api.dub.co/links/{linkId}" \
  -H "Authorization: Bearer $DUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/new"}' | jq '.'
```

### 3) 插入/更新链接（Upsert）

- `PUT /links/upsert`
  - 如果存在具有相同 URL 的链接，则返回/更新该链接；否则创建新链接。

```bash
curl -s -X PUT "https://api.dub.co/links/upsert" \
  -H "Authorization: Bearer $DUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}' | jq '.'
```

### 4) 删除链接

- `DELETE /links/{linkId}`
  - 根据 `linkId` 删除链接。

```bash
curl -s -X DELETE "https://api.dub.co/links/{linkId}" \
  -H "Authorization: Bearer $DUB_API_KEY" | jq '.'
```

### 5) 查詢链接信息

- `GET /links/info`
  - 可通过以下方式查询链接信息：
    - `domain + key`
    - `linkId`
    - `externalId`

```bash
curl -s "https://api.dub.co/links/info?domain=acme.link&key=promo" \
  -H "Authorization: Bearer $DUB_API_KEY" | jq '.'
```

### 6) 列出链接

- `GET /links`
  - 返回分页的链接列表，支持过滤条件。
  - 常见查询参数：`domain`, `search`, `tagId`, `tagIds`, `tagNames`, `folderId`, `tenantId`, `page`, `pageSize`, `sortBy`, `sortOrder`.

```bash
curl -s "https://api.dub.co/links?page=1&pageSize=20&sortBy=createdAt&sortOrder=desc" \
  -H "Authorization: Bearer $DUB_API_KEY" | jq '.'
```

### 7) 统计链接数量

- `GET /links/count`
  - 根据提供的过滤条件返回链接的数量。

```bash
curl -s "https://api.dub.co/links/count?domain=acme.link" \
  -H "Authorization: Bearer $DUB_API_KEY" | jq '.'
```

### 8) 批量创建链接

- `POST /links/bulk`
  - 创建最多 100 个链接。
  - 请求体：包含链接对象的数组（每个对象必须包含 `url` 字段）。

```bash
curl -s -X POST "https://api.dub.co/links/bulk" \
  -H "Authorization: Bearer $DUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '[{"url":"https://example.com/a"},{"url":"https://example.com/b"}]' | jq '.'
```

### 9) 批量更新链接

- `PATCH /links/bulk`
  - 更新最多 100 个链接。
  - 请求体需要包含 `data` 字段；目标链接可以通过 `linkIds` 或 `externalIds` 进行选择。

```bash
curl -s -X PATCH "https://api.dub.co/links/bulk" \
  -H "Authorization: Bearer $DUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"linkIds":["lnk_123","lnk_456"],"data":{"archived":true}}' | jq '.'
```

### 10) 批量删除链接

- `DELETE /links/bulk`
  - 删除最多 100 个链接。
  - 必需的查询参数：`linkIds`。

```bash
curl -s -X DELETE "https://api.dub.co/links/bulk?linkIds=lnk_123,lnk_456" \
  -H "Authorization: Bearer $DUB_API_KEY" | jq '.'
```

## 关键字段

常见的响应字段（来自 `LinkSchema`）：

- `id`
- `domain`
- `key`
- `shortLink`
- `url`
- `createdAt`
- `updatedAt`
- `archived`
- `externalId`
- `tags`
- `folderId`

**根据端点的不同，返回的结果格式如下**：
- `GET /links`: 返回链接数组
- `GET /links/count`: 返回链接数量
- 批量操作接口：返回链接数组或对象

## 推荐的工作流程

1. 确定操作类型（创建、更新、插入/更新、删除、查询、列出、统计或批量操作）。
2. 验证必要的输入参数（`url`, `linkId`, 过滤条件, 批量链接 ID）。
3. 使用 `curl -s` 和 `Bearer` 请求头发送请求。
4. 使用 `jq` 解析响应并验证操作结果是否正确。
5. 首先返回有用的信息（如 `id`, `shortLink`, `url` 以及 `archived` 状态）。
6. 对于列表数据，提供包含相关字段的简洁表格。
7. 确保操作范围严格限定在 `/links*` 端点上。

## 错误处理

- **401/403**: 令牌缺失、无效或未授权。
- **404**: 无法找到指定的链接（通过 `linkId` 查询时）或 `GET /links/info` 请求失败。
- **422**: 请求体无效（缺少或字段格式错误）。
- **429**: 请求频率超出限制；如果设置了 `Retry-After`，请按照提示重试。
- **网络问题/超时**: 最多尝试 2 次，每次尝试之间有短暂延迟。
- **返回的 JSON 数据格式不一致**: 返回最基本的原始数据并提示错误。

## 结果展示方式

建议的输出格式：

- 操作摘要（操作类型 + 结果）。
- 对于多个链接，展示一个简洁的表格：
  - `id | domain | key | shortLink | url |createdAt`
- 对于批量操作，显示请求的总数、实际处理的链接数量以及可能出现的错误。
- 明确指出数据仅限于已认证的工作空间。

## 不在支持范围内的功能

- 请勿使用与分析、事件、转换、合作伙伴、客户、佣金或支付相关的端点。
- 请勿使用与域名、文件夹或标签相关的端点。
- 请勿使用 `/tokens/*` 端点（包括 `/tokens/embed/referrals`）。

**注意**：`tokens` 页面仅用于 API 密钥的获取，不用于日常操作。

## OpenAPI 规范

请参考 `references/openapi-spec.json` 文件，以获取关于方法、路径、参数和数据结构的官方规范。