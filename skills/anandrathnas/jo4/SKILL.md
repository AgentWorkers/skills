---
name: jo4
description: URL缩短器、二维码生成器以及链接分析API：用于创建缩短后的链接、生成二维码，并追踪点击情况。
homepage: https://jo4.io
user-invocable: true
metadata: { "openclaw": { "emoji": "🔗", "primaryEnv": "JO4_API_KEY", "requires": { "env": ["JO4_API_KEY"] } } }
---

# Jo4 - URL缩短服务及分析API

Jo4是一款现代的URL缩短服务，支持生成二维码，并提供详细的链接分析功能。

## 认证

所有受保护的API端点都需要使用API密钥。请将您的API密钥设置为环境变量：

```bash
export JO4_API_KEY="your-api-key"
```

您可以在以下链接获取API密钥：https://jo4.io/api-keys

## API基础URL

```
https://jo4-api.jo4.io/api/v1
```

## API端点

### 创建缩短后的URL（需要认证）

```bash
curl -X POST "https://jo4-api.jo4.io/api/v1/protected/url" \
  -H "X-API-Key: $JO4_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "longUrl": "https://example.com/very-long-url",
    "title": "My Link"
  }'
```

**请求体：**
- `longUrl`（必填）- 目标URL（最长2048个字符）
- `title`（可选）- 链接标题（最长200个字符）
- `description`（可选）- 链接描述（最长500个字符）
- `shortUrl`（可选）- 自定义别名（最多16个字符，支持字母、数字、连字符和下划线）
- `expirationTime`（可选）- 链接的有效期限（Unix时间戳）
- `passwordProtected`（可选）- 是否启用密码保护
- `password`（可选）- 如果启用密码保护，则需要输入密码（4-128个字符）

**UTM参数：**
- `utmSource`、`utmMedium`、`utmCampaign`、`utmTerm`、`utmContent`

**响应：**
```json
{
  "response": {
    "id": 123,
    "slug": "abc123",
    "shortUrl": "abc123",
    "fullShortUrl": "https://jo4.io/a/abc123",
    "longUrl": "https://example.com/very-long-url",
    "title": "My Link",
    "qrCodeUrl": "https://jo4.io/qr/abc123"
  }
}
```

### 创建匿名缩短后的URL（无需认证）

```bash
curl -X POST "https://jo4-api.jo4.io/api/v1/public/url" \
  -H "Content-Type: application/json" \
  -d '{"longUrl": "https://example.com"}'
```

该功能仅提供基本的URL缩短服务，不支持链接分析。

### 获取URL详细信息

```bash
curl -X GET "https://jo4-api.jo4.io/api/v1/protected/url/{slug}" \
  -H "X-API-Key: $JO4_API_KEY"
```

### 获取URL分析数据

```bash
curl -X GET "https://jo4-api.jo4.io/api/v1/protected/url/{slug}/stats" \
  -H "X-API-Key: $JO4_API_KEY"
```

**响应内容包括：**
- 总点击次数
- 按日期划分的点击次数
- 地理分布信息
- 用户设备/浏览器类型
- 引用来源

### 查看我的URL列表

```bash
curl -X GET "https://jo4-api.jo4.io/api/v1/protected/url/myurls?page=0&size=20" \
  -H "X-API-Key: $JO4_API_KEY"
```

### 更新URL

```bash
curl -X PUT "https://jo4-api.jo4.io/api/v1/protected/url/{id}" \
  -H "X-API-Key: $JO4_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "longUrl": "https://new-destination.com"
  }'
```

### 删除URL

```bash
curl -X DELETE "https://jo4-api.jo4.io/api/v1/protected/url/{id}" \
  -H "X-API-Key: $JO4_API_KEY"
```

## 二维码

每个缩短后的URL都会自动生成一个二维码，二维码的生成地址为：
```
https://jo4.io/qr/{shortUrl}
```

## 速率限制

不同套餐的速率限制如下：
- 免费套餐：每分钟60次请求
- Pro套餐：每分钟最多10,000次请求
- 匿名用户（公共端点）：每分钟10次请求

## API文档

完整的OpenAPI/Swagger文档请访问：https://jo4-api.jo4.ioswagger-ui/index.html

## 常见使用场景

### 1. 缩短URL以便分享
```bash
curl -X POST "https://jo4-api.jo4.io/api/v1/protected/url" \
  -H "X-API-Key: $JO4_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"longUrl": "https://example.com/article", "title": "Article"}'
```

### 2. 创建用于跟踪活动的链接
```bash
curl -X POST "https://jo4-api.jo4.io/api/v1/protected/url" \
  -H "X-API-Key: $JO4_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "longUrl": "https://mysite.com/landing",
    "title": "Q1 Campaign",
    "utmSource": "twitter",
    "utmMedium": "social",
    "utmCampaign": "q1-2026"
  }'
```

### 3. 创建具有过期时间的链接
```bash
curl -X POST "https://jo4-api.jo4.io/api/v1/protected/url" \
  -H "X-API-Key: $JO4_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "longUrl": "https://mysite.com/promo",
    "title": "Limited Offer",
    "expirationTime": 1738454400
  }'
```

## 错误代码

| 代码 | 含义 |
|------|---------|
| 400 | 请求错误 - 参数无效 |
| 401 | 未经授权 - API密钥缺失或无效 |
| 403 | 禁止访问 - 权限不足 |
| 404 | 未找到 - URL不存在 |
| 429 | 超过速率限制 |