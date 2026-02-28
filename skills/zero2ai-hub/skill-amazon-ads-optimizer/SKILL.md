---
name: skill-amazon-ads
description: "适用于 OpenClaw 代理的 Amazon Ads API v3 技能：可以列出用户资料、管理赞助产品广告活动、查看预算和广告效果。支持与任何广告商账户配合使用。"
metadata:
  openclaw:
    requires: { bins: ["node"] }
---
# Amazon Ads API Skill

通过您的 OpenClaw 代理管理 Amazon 赞助产品（Sponsored Products）广告活动——列出广告主信息、查看广告活动详情、检查预算以及获取性能数据。

---

## 设置

### 1. 创建凭据文件
```json
{
  "lwaClientId": "amzn1.application-oa2-client.YOUR_CLIENT_ID",
  "lwaClientSecret": "YOUR_CLIENT_SECRET",
  "refreshToken": "Atzr|YOUR_REFRESH_TOKEN",
  "profileId": "YOUR_ADS_PROFILE_ID",
  "region": "eu"
}
```
将文件保存为 `amazon-ads-api.json`。设置环境变量 `AMAZON_ADS_PATH` 以指向该文件（默认值：`./amazon-ads-api.json`）。

> **区域与端点：**
> - `na` → `advertising-api.amazon.com`
> - `eu` → `advertising-api-eu.amazon.com`
> - `fe` → `advertising-api-fe.amazon.com`

### 2. 获取您的广告主 ID（Profile ID）
```bash
node scripts/ads.js --profiles
```
复制您所在品牌/市场的 `profileId`，并将其添加到凭据文件中。

---

## 脚本

### `ads.js` — 广告活动管理及汇总信息
```bash
node scripts/ads.js --profiles                # list all advertiser profiles
node scripts/ads.js --campaigns               # list all SP campaigns
node scripts/ads.js --summary                 # active campaigns + budgets summary
node scripts/ads.js --campaigns --out c.json  # save to file
```

---

## 凭据结构

| 字段 | 描述 |
|-------|-------------|
| `lwaClientId` | 广告应用客户端 ID（与 SP-API 的客户端 ID 不同） |
| `lwaClientSecret` | 广告应用客户端密钥 |
| `refreshToken` | LWA 刷新令牌 |
| `profileId` | 广告主 ID（来自 `--profiles` 命令） |
| `region` | `na`、`eu` 或 `fe` |

---

## 注意事项：
- Amazon Ads API 使用与 SP-API **不同的 LWA 应用**，因此需要使用不同的客户端 ID 和密钥。
- 所有广告活动操作均需要广告主 ID。
- 令牌会在每次请求时重新获取（CLI 使用时不会缓存令牌）。
- 对于生产环境或高频率使用场景，建议添加令牌缓存机制。

## 相关技能
- [skill-amazon-spapi](https://github.com/Zero2Ai-hub/skill-amazon-spapi) — 订单、库存及商品信息管理