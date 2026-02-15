---
name: startups
version: "1.0.0"
description: 通过 startups.in 研究初创企业、融资轮次、收购情况以及招聘趋势。
homepage: https://startups.in
user-invocable: true
author: startups.in
license: MIT
---

# startups.in - 创业公司研究平台

使用 startups.in 研究初创公司、追踪其融资情况，并发现招聘趋势。

## 功能

- **搜索** - 按名称、行业或地点查找初创公司
- **详情** - 获取初创公司的全面信息
- **融资** - 跟踪融资轮次、估值和投资者信息
- **招聘** - 监控职位发布和团队发展情况
- **比较** - 进行初创公司之间的对比分析

## 示例查询

- “查找旧金山的 AI 初创公司”
- “介绍一下 Stripe 公司”
- “Anthropic 最近的融资情况是什么？”
- “Vercel 公司正在招聘吗？”
- “比较 Notion 和 Coda 这两款工具”

## API

基础 URL：`https://startups.in`

### 搜索
```http
GET /api/search?q={query}
```

### 获取初创公司信息
```http
GET /api/startups/{slug}
```

### 查看职位信息
```http
GET /api/startups/{slug}/jobs
```

### 进行比较
```http
GET /api/compare?startups={slug1},{slug2}
```

## 认证

公众用户无需认证即可使用该平台。如需更高级别的访问权限，请使用 Moltbook 身份验证：

```http
X-Moltbook-Identity: {token}
```

## 链接

- 网站：https://startups.in
- Moltbook：https://moltbook.com/u/startups