---
name: domaindetails
description: 查询域名的 WHOIS/RDAP 信息，并查看市场列表。提供免费 API，无需身份验证。
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["curl"]}}}
---

# domaindetails

提供域名查询和市场搜索服务。这是一个免费的API，只需使用curl命令即可调用。

## 域名查询

```bash
curl -s "https://mcp.domaindetails.com/lookup/example.com" | jq
```

返回信息包括：注册商信息、域名创建/到期日期、名称服务器信息、DNSSEC配置以及联系信息。

## 市场搜索

```bash
curl -s "https://api.domaindetails.com/api/marketplace/search?domain=example.com" | jq
```

可查询的域名交易平台包括：Sedo、Afternic、Atom、Dynadot、Namecheap、NameSilo、Unstoppable Domains。

## 请求限制

- 每分钟100个请求（无需身份验证）

## 命令行接口（可选）

```bash
npx domaindetails example.com
```