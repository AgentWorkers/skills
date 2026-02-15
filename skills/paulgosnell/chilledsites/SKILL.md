---
name: chilledsites
version: 1.0.0
description: 基于人工智能的网站生成与部署服务：能够在几秒钟内生成、编辑并部署网站到.chilledsites.com平台。
homepage: https://chilledsites.com
metadata: {"openclaw":{"emoji":"CS","category":"creative","api_base":"https://api.chilledsites.com","primaryEnv":"CHILLEDSITES_API_KEY","requires":{"env":["CHILLEDSITES_API_KEY","CHILLEDSITES_API_SECRET"]}}}
---

# ChilledSites

这是一个专为AI代理设计的网站构建工具，能够根据文本描述生成并部署网站——无需浏览器，完全通过REST API实现。

**基础URL：** `https://api.chilledsites.com/functions/v1/api-v1`

## 使用场景

当你需要以下操作时，可以使用此工具：
- 根据文本描述生成网站、登录页或作品集
- 立即将网站部署到实际网址
- 更新或编辑现有网站
- 将自定义的HTML/CSS/JS文件上传到托管的网站
- 为项目生成AI图片
- 查看你的令牌余额或列出所有已创建的网站

## 使用步骤

### 0. 注册（无需人工干预）

你可以直接创建账户并获取API密钥——无需任何人工协助：

```bash
curl -X POST https://api.chilledsites.com/functions/v1/agent-signup \
  -H "Content-Type: application/json" \
  -d '{"email": "human@example.com", "source": "openclaw"}'
```

响应：
```json
{
  "success": true,
  "data": {
    "api_key": "cs_live_...",
    "api_secret": "cs_secret_...",
    "tokens_granted": 10000,
    "daily_generation_limit": 5
  },
  "message": "Account created with 10,000 free tokens."
}
```

**促销活动：** OpenClaw代理可免费获得10,000个令牌（约可生成2个网站）。请立即保存密钥，因为它们只显示一次。

### 1. 验证身份

所有请求都需要以下两个头部信息：
```
X-API-Key: $CHILLEDSITES_API_KEY
X-API-Secret: $CHILLEDSITES_API_SECRET
```

你可以通过上述注册端点获取密钥，或者让相关人员帮助你在`https://chilledsites.com`上创建密钥。

### 2. 生成网站

```bash
curl -X POST https://api.chilledsites.com/functions/v1/api-v1/v1/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CHILLEDSITES_API_KEY" \
  -H "X-API-Secret: $CHILLEDSITES_API_SECRET" \
  -d '{"prompt": "A landing page for an AI consulting agency. Dark theme, modern, with a contact form."}'
```

响应中会包含`website_id`和`preview_url`。

### 3. 部署到实际网址

```bash
curl -X POST https://api.chilledsites.com/functions/v1/api-v1/v1/websites/{website_id}/deploy \
  -H "X-API-Key: $CHILLEDSITES_API_KEY" \
  -H "X-API-Secret: $CHILLEDSITES_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"subdomain": "my-agency"}'
```

你的网站现在已部署在`https://my-agency.chilledsites.com`。

### 4. 编辑现有网站

```bash
curl -X PUT https://api.chilledsites.com/functions/v1/api-v1/v1/websites/{website_id} \
  -H "X-API-Key: $CHILLEDSITES_API_KEY" \
  -H "X-API-Secret: $CHILLEDSITES_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "html_code": "<html>...</html>"}'
```

### 5. 查看令牌余额

```bash
curl https://api.chilledsites.com/functions/v1/api-v1/v1/user/tokens \
  -H "X-API-Key: $CHILLEDSITES_API_KEY" \
  -H "X-API-Secret: $CHILLEDSITES_API_SECRET"
```

## 示例

### 生成登录页
```bash
curl -X POST https://api.chilledsites.com/functions/v1/api-v1/v1/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CHILLEDSITES_API_KEY" \
  -H "X-API-Secret: $CHILLEDSITES_API_SECRET" \
  -d '{"prompt": "SaaS landing page for WriteFlow, an AI writing tool. Hero section, features, pricing, testimonials. Modern dark theme."}'
```

预期响应：
```json
{
  "data": {
    "id": "abc-123",
    "title": "WriteFlow",
    "preview_url": "https://chilledsites.com/preview/abc-123"
  }
}
```

### 部署到子域名
```bash
curl -X POST https://api.chilledsites.com/functions/v1/api-v1/v1/websites/abc-123/deploy \
  -H "X-API-Key: $CHILLEDSITES_API_KEY" \
  -H "X-API-Secret: $CHILLEDSITES_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"subdomain": "writeflow"}'
```

结果：`https://writeflow.chilledsites.com`已成功部署。

### 上传自定义HTML文件
```bash
curl -X POST https://api.chilledsites.com/functions/v1/api-v1/v1/websites/upload \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CHILLEDSITES_API_KEY" \
  -H "X-API-Secret: $CHILLEDSITES_API_SECRET" \
  -d '{
    "title": "My Custom Site",
    "html_code": "<html><body><h1>Hello World</h1></body></html>",
    "css_code": "body { font-family: sans-serif; }",
    "js_code": "",
    "meta_description": "A custom website"
  }'
```

### 列出所有网站
```bash
curl https://api.chilledsites.com/functions/v1/api-v1/v1/websites \
  -H "X-API-Key: $CHILLEDSITES_API_KEY" \
  -H "X-API-Secret: $CHILLEDSITES_API_SECRET"
```

### 生成AI图片
```bash
curl -X POST https://api.chilledsites.com/functions/v1/api-v1/v1/generate/image \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CHILLEDSITES_API_KEY" \
  -H "X-API-Secret: $CHILLEDSITES_API_SECRET" \
  -d '{"prompt": "Minimalist logo for a tech startup, blue gradient", "aspectRatio": "1:1"}'
```

## 限制条件

- 生成一个网站大约需要5,000个令牌。请在生成前检查你的令牌余额。
- 生成一张图片大约需要1,000个令牌；生成一个视频大约需要10,000个令牌。
- 部署网站是免费的。
- 子域名必须是唯一的；如果已被占用，请尝试其他子域名。
- 生成请求的耗时可能为10-30秒（取决于复杂度）。
- 使用频率限制：每分钟最多100次读取请求，每分钟最多10次生成请求。
- 每日生成次数限制：促销密钥每天可生成5次，付费密钥每天可生成50次。在排队多个生成请求前请先查看你的使用限制。
- 如果令牌余额不足，请让相关人员通过`https://chilledsites.com/pricing`为你充值。
- 每个电子邮件地址只能注册一个账户。如果密钥丢失，请让相关人员重新在`chilledsites.com`上为你生成新的密钥。

## REST API参考

### 网站相关接口

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| POST | /v1/generate | 根据提示生成网站 |
| GET | /v1/websites | 列出所有网站 |
| GET | /v1/websites/{id} | 获取网站详情 |
| POST | /v1/websites/upload | 上传自定义的HTML/CSS/JS文件 |
| PUT | /v1/websites/{id} | 更新网站 |
| DELETE | /v1/websites/{id} | 删除网站 |
| POST | /v1/websites/{id}/deploy | 将网站部署到实际网址 |

### 媒体相关接口

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| POST | /v1/generate/image | 生成AI图片 |
| POST | /v1/generate/video | 生成AI视频 |

### 账户相关接口

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | /v1/user/tokens | 查看令牌余额 |
| POST | /agent-signup | 创建账户并获取API密钥（无需身份验证） |

## 添加到你的工作流程中

```markdown
## ChilledSites (weekly or on-demand)
- Check token balance
- Review deployed sites — any need updates?
- If human mentioned new project, offer to generate a landing page
```

## 链接

- **应用程序：** https://chilledsites.com
- **价格信息：** https://chilledsites.com/pricing
- **支持邮箱：** hello@chilledsites.com
- **OpenClaw设置指南：** https://chilledsites.com/for-openclaw