---
name: easy-email-finder
description: 使用 Easy Email Finder API 搜索本地或在线企业，并为这些企业添加经过验证的电子邮件地址、技术栈信息以及社交媒体链接。
metadata: {"openclaw":{"emoji":"📧","homepage":"https://easyemailfinder.com","primaryEnv":"EEF_API_KEY","requires":{"env":["EEF_API_KEY"]}}}
---
# Easy Email Finder API

使用此API可以查找潜在客户及其电子邮件地址。Easy Email Finder API支持搜索本地企业（通过Google Places）或仅在线运营的企业（如SaaS服务提供商、营销机构、电子商务公司等），并可以从这些企业的网站中提取经过验证的电子邮件信息。

## 认证

所有请求都需要携带Bearer令牌。API密钥存储在`EEF_API_KEY`环境变量中。

```
Authorization: Bearer $EEF_API_KEY
```

您可以在 [https://easyemailfinder.com/developer](https://easyemailfinder.com/developer) 获取API密钥。

## 基本URL

```
https://easyemailfinder.com/api/v1
```

## API端点

### 搜索企业（免费，无需消耗信用点数）

```bash
# Local businesses (default)
curl -X POST https://easyemailfinder.com/api/v1/search \
  -H "Authorization: Bearer $EEF_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "dentists in denver", "pageToken": null}'

# Digital/online-only businesses
curl -X POST https://easyemailfinder.com/api/v1/search \
  -H "Authorization: Bearer $EEF_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "SaaS companies", "mode": "digital"}'
```

- 将`mode`设置为`"local"`（默认值）以搜索本地企业；
- 设置为`"digital"`以搜索仅在线运营的企业。
返回结果包括企业名称、网站信息（对于本地企业）以及地址、电话号码、评分和Google Maps链接。可以使用响应中的`pageToken`来获取下一页数据。

### 从网站中提取电子邮件信息（每次调用消耗1个信用点数）

```bash
curl -X POST https://easyemailfinder.com/api/v1/enrich \
  -H "Authorization: Bearer $EEF_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"website": "https://example-business.com"}'
```

返回的字段包括：`emails`（电子邮件地址）、`techStack`（使用的网站平台，如WordPress、Shopify、Wix、Squarespace、Webflow等）、`socialLinks`（企业的社交媒体链接，包括Facebook、Instagram、LinkedIn、Twitter、YouTube和TikTok）。

### 批量提取电子邮件信息（每个网站消耗1个信用点数，最多20个网站）

```bash
curl -X POST https://easyemailfinder.com/api/v1/enrich-batch \
  -H "Authorization: Bearer $EEF_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"websites": ["https://site1.com", "https://site2.com"]}'
```

### 同时执行搜索和提取电子邮件信息（每个结果消耗1个信用点数）

```bash
# Local businesses
curl -X POST https://easyemailfinder.com/api/v1/search-and-enrich \
  -H "Authorization: Bearer $EEF_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "plumbers in austin", "limit": 20}'

# Digital businesses
curl -X POST https://easyemailfinder.com/api/v1/search-and-enrich \
  -H "Authorization: Bearer $EEF_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "digital marketing agencies", "limit": 20, "mode": "digital"}'
```

该端点同时支持搜索和提取电子邮件信息。`limit`参数默认值为20，最大值为60。支持的模式包括`"local"`（默认值）和`"digital"`。

### 查看信用点数余额（免费）

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

- 标准端点（搜索、查看余额、使用情况）：每分钟120次请求；
- 提取电子邮件信息的端点：每分钟30次请求；
- 如遇到速率限制，请查看响应头中的`Retry-After`字段以确定重试时间。

## 信用点数费用

| API端点 | 费用 |
|----------|------|
| /v1/search | 免费 |
| /v1/enrich | 1个信用点数（0.25美元） |
| /v1/enrich-batch | 每个网站消耗1个信用点数 |
| /v1/search-and-enrich | 每个结果消耗1个信用点数 |
| /v1/balance | 免费 |
| /v1/usage | 免费 |

## 典型工作流程

**针对本地企业**（例如：“丹佛的牙医”）：
1. 使用`/v1/search`根据行业和位置查找企业；
2. 使用`/v1/enrich`或`/v1/enrich-batch`获取这些企业的电子邮件地址；
3. 或者使用`/v1/search-and-enrich`一次性完成搜索和提取电子邮件信息的操作。

**针对仅在线运营的企业**（例如：“SaaS公司”、“数字营销机构”）：
1. 使用`/v1/search`并设置`mode`为`"digital"`来查找这些企业；
2. 使用`/v1/enrich`或`/v1/search-and-enrich`来提取电子邮件信息。

请定期使用`/v1/balance`接口查看您的信用点数使用情况。