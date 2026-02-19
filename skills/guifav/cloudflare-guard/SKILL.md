---
name: cloudflare-guard
description: 配置和管理 Cloudflare 的 DNS、缓存、安全规则、速率限制以及 Workers（计算服务）。
user-invocable: true
---
# Cloudflare Guard

作为一名基础设施工程师，您负责管理部署在 Vercel 上的 Web 应用程序的 Cloudflare 配置，包括 DNS、缓存、安全性和边缘逻辑。请始终通过 `curl` 使用 Cloudflare API v4 进行操作，并且绝不要将 API 令牌存储在文件中。

## 规划协议（强制要求——在任何操作之前执行）

在向 Cloudflare 发送任何 API 请求之前，必须完成以下规划步骤：

1. **理解请求内容。** 明确：(a) 需要进行的 DNS/缓存/安全设置更改是什么；(b) 这些更改会影响哪个域名和区域；(c) 这是新的配置还是对现有配置的修改。

2. **调查当前状态。** 通过查询 Cloudflare API，列出现有的 DNS 记录、当前的 SSL 设置、活动的页面规则和速率限制规则。切勿假设当前状态是正确的——务必先进行核实。

3. **制定执行计划。** 详细列出：(a) 每个将执行的 API 请求；(b) 预期的响应结果；(c) 操作的顺序（例如，必须先设置 DNS，然后才能验证 SSL）。在执行前向相关人员展示该计划。

4. **识别潜在风险。** 标记出可能引发故障的风险点：(a) 可能导致服务中断的 DNS 更改（如修改代理记录或删除 A/CNAME 记录）；(b) 可能破坏 HTTPS 的 SSL 更改；(c) 可能阻止合法流量的 WAF 规则。对于 DNS 更改，请注意记录其传播时间。

5. **按顺序执行操作。** 每次只执行一个 API 请求，验证响应后再进行下一步。对于 DNS 更改，在继续之前请通过查询确认记录已正确传播。

6. **总结所有更改。** 报告所有已进行的更改、更改后的当前状态以及用户可能遇到的传播延迟。

请务必遵守此协议。错误的 DNS 记录或 SSL 设置可能会导致整个网站无法正常运行。

## API 基础

所有请求均使用以下格式：
```
https://api.cloudflare.com/client/v4
```

身份验证头部：
```
Authorization: Bearer $CLOUDFLARE_API_TOKEN
```

## DNS 管理

### 列出 DNS 记录
```bash
curl -s -X GET \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" | jq '.result[] | {id, type, name, content, proxied}'
```

### 为 Vercel 添加 CNAME 记录
```bash
curl -s -X POST \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "CNAME",
    "name": "<subdomain>",
    "content": "cname.vercel-dns.com",
    "ttl": 1,
    "proxied": true
  }' | jq .
```

### （如需要）添加根域 A 记录
```bash
curl -s -X POST \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "@",
    "content": "76.76.21.21",
    "ttl": 1,
    "proxied": true
  }' | jq .
```

### 删除 DNS 记录
```bash
curl -s -X DELETE \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records/<record-id>" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq .
```

## SSL/TLS 配置

### 将 SSL 模式设置为“Full (Strict)”
当通过 Cloudflare 代理到 Vercel 时，此步骤是必需的：
```bash
curl -s -X PATCH \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/settings/ssl" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "strict"}' | jq .
```

### 启用“Always Use HTTPS”功能
```bash
curl -s -X PATCH \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/settings/always_use_https" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "on"}' | jq .
```

## 缓存规则

### 设置浏览器缓存过期时间
```bash
curl -s -X PATCH \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/settings/browser_cache_ttl" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": 14400}' | jq .
```

### 清除所有缓存
在重大部署后执行此操作：
```bash
curl -s -X POST \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything": true}' | jq .
```

### 清除特定 URL 的缓存
```bash
curl -s -X POST \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"files": ["https://example.com/path"]}' | jq .
```

## 安全规则

### 创建速率限制规则
保护 API 路由免受滥用：
```bash
curl -s -X POST \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/rulesets/phases/http_ratelimit/entrypoint" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "rules": [{
      "expression": "(http.request.uri.path matches \"^/api/\")",
      "description": "Rate limit API routes",
      "action": "block",
      "ratelimit": {
        "characteristics": ["ip.src"],
        "period": 60,
        "requests_per_period": 100,
        "mitigation_timeout": 600
      }
    }]
  }' | jq .
```

### 启用“Bot Fight Mode”功能
```bash
curl -s -X PUT \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/bot_management" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"fight_mode": true}' | jq .
```

## 页面规则（虽然较旧但仍有用）

### 积极缓存静态资源
```bash
curl -s -X POST \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/pagerules" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "targets": [{"target": "url", "constraint": {"operator": "matches", "value": "*.<domain>/_next/static/*"}}],
    "actions": [{"id": "cache_level", "value": "cache_everything"}, {"id": "edge_cache_ttl", "value": 2592000}],
    "status": "active"
  }' | jq .
```

## 新项目的标准配置

在为 Vercel 上的新项目配置 Cloudflare 时，请执行以下步骤：

1. 添加指向 `cname.vercel-dns.com` 的 CNAME 记录。
2. 将 SSL 模式设置为“Full (Strict)”。
3. 启用“Always Use HTTPS”功能。
4. 为 `/api/*` 路由设置速率限制。
5. 启用“Bot Fight Mode”功能。
6. 将浏览器缓存过期时间设置为 4 小时。
7. 创建页面规则，以积极缓存 `_next/static/*` 文件。

请按顺序执行所有步骤，并报告每个步骤的结果。

## 故障排除

### 522 错误（连接超时）
- 确保 SSL 模式设置为“Full (Strict)”，而非“Flexible”。
- 验证 Vercel 域名是否配置正确。
- 检查 Cloudflare 是否处于代理模式（显示为橙色云图标）——应该是这样的。

### 混合内容警告
- 启用“Always Use HTTPS”功能。
- 确保所有内部链接使用相对路径或 `https://` 协议。

### 部署后缓存未更新
- 部署完成后清除缓存。
- 检查 `vercel.json` 文件中的 `Cache-Control` 头部是否设置正确。