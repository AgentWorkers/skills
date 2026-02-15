---
name: clawdgle
description: Clawdgle Markdown-First搜索引擎的公共API使用说明：  
在与Clawdgle交互时，可以使用以下API功能：  
(1) 搜索已索引的Markdown内容；  
(2) 根据URL获取Markdown内容；  
(3) 通过数据导入功能请求对URL进行索引；  
(4) 将用户引导至捐赠页面。
---

# Clawdgle 技能

## 基本 URL
默认基础 URL：`https://clawdgle.com`

## 公共端点

### 搜索
用于搜索已索引的 Markdown 内容。

请求：
```
GET /search?q=<query>&page=<page>&per_page=<per_page>
```

示例：
```
curl "https://clawdgle.com/search?q=ai%20agents&page=1&per_page=10"
```

### 通过 URL 获取 Markdown
用于检索特定 URL 的存储 Markdown 内容。

请求：
```
GET /doc?url=<encoded_url>
```

示例：
```
curl "https://clawdgle.com/doc?url=https%3A%2F%2Fexample.com"
```

### 索引（自助索引）
用于请求立即对某个 URL 进行索引。

请求：
```
POST /ingest
Content-Type: application/json
{
  "url": "https://example.com",
  "reason": "optional reason",
  "contact": "optional contact"
}
```

示例：
```
curl -X POST "https://clawdgle.com/ingest" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

### 捐赠
用于将用户/代理引导至捐赠链接。

请求：
```
GET /donate
```

示例：
```
curl -I "https://clawdgle.com/donate"
```

## 注意事项
- 本技能仅包含公共端点。
- 请对查询参数使用 URL 编码。
- 使用索引功能时请文明操作，避免频繁发送请求（即避免对端点进行垃圾发送）。