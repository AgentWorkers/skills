---
name: premium-domains
description: 在 Afternic、Sedo、Atom、Dynadot、Namecheap、NameSilo 和 Unstoppable Domains 等平台上搜索待售的优质域名。
metadata: {"clawdbot":{"emoji":"💎","requires":{"bins":["curl"]}}}
---

# 高级域名搜索

在各大市场平台上查找待售域名。提供免费API，只需使用curl命令即可调用。

## 使用方法

```bash
curl -s "https://api.domaindetails.com/api/marketplace/search?domain=example.com" | jq
```

## 已支持的域名交易平台

- **Afternic** — GoDaddy的高级域名交易平台
- **Sedo** — 全球域名交易平台
- **Atom** — 高级域名交易平台
- **Dynadot** — 提供拍卖和立即购买选项
- **Namecheap** — 集成域名注册服务市场
- **NameSilo** — 经济实惠的域名交易平台
- **Unstoppable Domains** — 支持Web3域名的交易平台

## 响应字段

- `found` — 是否找到任何待售域名
- `marketplaces.<name>.listing.price` — 域名价格（单位：美分或美元）
- `marketplaces.<name>.listing_currency` — 价格货币（例如：USD、EUR等）
- `marketplaces.<name>.listing.url` — 域名列表的直接链接
- `marketplaces.<name>.listing.listingType` — 域名购买方式（立即购买、拍卖或出价）

## 请求限制

- 每分钟最多100次请求（无需身份验证）