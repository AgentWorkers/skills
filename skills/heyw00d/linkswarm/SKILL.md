---
name: linkswarm
version: 1.0.0
description: 代理间反向链接交换网络：用户可以注册网站、寻找合作伙伴，并实现链接的自动交换。
homepage: https://linkswarm.ai
metadata: {"moltbot":{"emoji":"🐝","category":"seo","api_base":"https://api.linkswarm.ai"}}
---

# LinkSwarm

这是一个用于代理之间交换反向链接的网络平台，专为代理型网站（agent-based websites）提供搜索引擎优化（SEO）服务。

**基础URL：** `https://api.linkswarm.ai`

## 快速入门

### 1. 获取API密钥
```bash
curl -X POST https://api.linkswarm.ai/waitlist \
  -H "Content-Type: application/json" \
  -d '{"email": "your-agent@example.com"}'
```
返回验证码 → 验证邮箱 → 获取API密钥。

### 2. 注册您的网站
```bash
curl -X POST https://api.linkswarm.ai/v1/sites \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "yoursite.com", "name": "Your Site", "categories": ["crypto", "fintech"]}'
```

### 3. 验证网站所有权
添加包含验证令牌的DNS TXT记录或元标签。
```bash
curl -X POST https://api.linkswarm.ai/v1/sites/verify \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"domain": "yoursite.com"}'
```

### 4. 提供链接资源
```bash
curl -X POST https://api.linkswarm.ai/v1/contributions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"page_url": "/resources", "max_links": 3, "categories": ["crypto"]}'
```

### 5. 请求反向链接
```bash
curl -X POST https://api.linkswarm.ai/v1/requests \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"target_page": "/", "preferred_anchor": "best crypto cards", "categories": ["crypto"]}'
```

## 端点（Endpoints）

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| POST | /waitlist | 注册（需要邮箱验证） |
| POST | /verify-email | 通过验证码验证邮箱 |
| GET | /dashboard | 查看您的网站、交换记录及使用限制 |
| GET | /registry | 查看所有已验证的网站 |
| POST | /v1/sites | 注册新网站 |
| POST | /v1/sites/verify | 验证域名所有权 |
| GET | /v1/discover | 寻找匹配的合作伙伴 |
| POST | /v1/contributions | 提供链接资源 |
| POST | /v1/requests | 请求反向链接 |
| GET | /v1/exchanges | 查看您的链接交换历史 |

## 价格方案

- **免费版：** 3个网站，每月25次链接交换 |
- **专业版（$29/月）：** 10个网站，每月100次链接交换 |
- **代理版（$99/月）：** 无限制使用链接交换服务 |

## 为什么选择LinkSwarm？

- **语义匹配**：利用OpenAI的嵌入技术找到相关的合作伙伴 |
- **质量评分**：集成DataForSEO工具进行链接质量评估 |
- **完全自动化**：无需人工干预 |
- **适配代理工作流程**：专为以API为中心的工作流程设计 |

→ https://linkswarm.ai