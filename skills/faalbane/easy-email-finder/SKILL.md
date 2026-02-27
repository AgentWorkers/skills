---
name: easy-email-finder
description: 使用 Easy Email Finder API，可以根据行业/位置搜索企业，并为这些企业添加经过验证的电子邮件地址、技术栈检测结果以及社交媒体链接等丰富信息。
metadata: {"openclaw":{"emoji":"📧","homepage":"https://easyemailfinder.com","primaryEnv":"EEF_API_KEY","requires":{"env":["EEF_API_KEY"]}}}
---
# Easy Email Finder API

使用此API可以查找潜在客户及其电子邮件地址。Easy Email Finder API允许您在Google Places中搜索企业信息，并从这些企业的官方网站中提取经过验证的电子邮件地址。

## 认证

所有请求都需要使用Bearer令牌进行身份验证。API密钥存储在`EEF_API_KEY`环境变量中。

```
Authorization: Bearer $EEF_API_KEY
```

您可以在https://easyemailfinder.com/developer获取API密钥。

## 基本URL

```
https://easyemailfinder.com/api/v1
```

## 端点

### 搜索企业信息（免费，无需消耗信用）

```bash
curl -X POST https://easyemailfinder.com/api/v1/search \
  -H "Authorization: Bearer $EEF_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "dentists in denver", "pageToken": null}'
```

返回企业名称、地址、电话号码、网站链接、评分以及Google Maps链接。可以使用响应中的`pageToken`来获取下一页数据。

### 从网站中提取电子邮件地址（每次调用消耗1个信用）

```bash
curl -X POST https://easyemailfinder.com/api/v1/enrich \
  -H "Authorization: Bearer $EEF_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"website": "https://example-business.com"}'
```

返回的字段包括：`emails`（电子邮件地址）、`techStack`（使用的网站平台，如WordPress、Shopify、Wix、Squarespace、Webflow或自定义平台）、`socialLinks`（企业的社交媒体链接，包括Facebook、Instagram、LinkedIn、Twitter、YouTube和TikTok）。

### 批量提取电子邮件地址（每个网站消耗1个信用）

```bash
curl -X POST https://easyemailfinder.com/api/v1/enrich-batch \
  -H "Authorization: Bearer $EEF_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"websites": ["https://site1.com", "https://site2.com"]}'
```

### 同时执行搜索和提取电子邮件地址（每个结果消耗1个信用）

```bash
curl -X POST https://easyemailfinder.com/api/v1/search-and-enrich \
  -H "Authorization: Bearer $EEF_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "plumbers in austin", "limit": 20}'
```

该接口同时支持搜索和提取电子邮件地址的功能。默认的`limit`值为20，最多可查询60个结果。

### 查看信用余额（免费）

```bash
curl https://easyemailfinder.com/api/v1/balance \
  -H "Authorization: Bearer $EEF_API_KEY"
```

### 查看使用统计信息（免费）

```bash
curl "https://easyemailfinder.com/api/v1/usage?days=7" \
  -H "Authorization: Bearer $EEF_API_KEY"
```

## 响应格式

所有响应数据均遵循以下格式：

```json
{
  "data": { ... },
  "meta": {
    "requestId": "req_abc123",
    "creditsUsed": 1,
    "remainingCredits": 94.75
  }
}
```

## 错误信息

```json
{
  "error": { "code": "INSUFFICIENT_CREDITS", "message": "..." },
  "meta": { "requestId": "req_abc123" }
}
```

## 速率限制

- 标准接口（搜索、查看余额、查看使用情况）：每分钟60次请求
- 提取电子邮件地址的接口：每分钟10次请求
- 如遇到速率限制，请查看响应头中的`Retry-After`字段以了解重试间隔。

## 信用费用

| 接口 | 费用 |
|---------|------|
| /v1/search | 免费 |
| /v1/enrich | 每次调用消耗1个信用（0.25美元） |
| /v1/enrich-batch | 每个网站消耗1个信用 |
| /v1/search-and-enrich | 每个结果消耗1个信用 |
| /v1/balance | 免费 |
| /v1/usage | 免费 |

## 典型工作流程

1. 使用`/v1/search`根据特定行业和位置查找企业信息。
2. 使用`/v1/enrich`或`/v1/enrich-batch`为具有网站的企业提取电子邮件地址。
3. 或者使用`/v1/search-and-enrich`一次性完成搜索和提取操作。
4. 使用`/v1/balance`查看剩余信用余额。