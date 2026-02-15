---
name: apollo-io
description: Apollo.io 提供销售情报集成服务，用于潜在客户的发现、联系信息完善以及公司信息查询。您可以搜索超过 2.1 亿条联系信息和 3500 万家公司的数据。该工具适用于寻找潜在客户、完善联系信息或进行公司研究。相关关键词：Apollo、销售情报、潜在客户生成、潜在客户开发、联系信息完善、电子邮件查找器、公司搜索。
homepage: https://github.com/artopenclaw/skills/apollo-io
metadata:
  openclaw:
    emoji: 🎯
    requires:
      env:
        - APOLLO_API_KEY
    install: []
---

# Apollo.io 技能

通过 Apollo.io 的 REST API 提供销售情报和潜在客户发现功能。

## 设置

1. 从 [Apollo 设置 → API](https://apollo.io/settings/api) 获取您的 API 密钥。
2. 设置环境变量：`export APOLLO_API_KEY=your_key_here`

## 功能

### 人员搜索
根据职位、位置、公司等信息查找潜在客户。

```bash
python <skill>/scripts/search_people.py --title "VP Engineering" --company Stripe
```

### 人员信息补充
从电子邮件或 LinkedIn URL 中补充人员信息。

```bash
python <skill>/scripts/enrich_person.py --email john@example.com
python <skill>/scripts/enrich_person.py --linkedin https://linkedin.com/in/johndoe
```

### 公司搜索
根据行业、规模、位置等信息查找公司。

```bash
python <skill>/scripts/search_companies.py --industry "Software" --size "50-200"
```

### 公司信息补充
根据域名或名称补充公司信息。

```bash
python <skill>/scripts/enrich_company.py --domain stripe.com
```

## 使用方法

当您需要执行以下操作时，代理会自动使用这些脚本：
- 在特定公司查找联系人
- 查找电子邮件地址或电话号码
- 研究公司详情
- 按职位/行业进行潜在客户开发

## API 参考

- [Apollo API 文档](https://docs.apollo.io/)
- 基本 URL：`https://api.apollo.io/v1`
- 认证方式：使用 `X-Api-Key` 请求头进行身份验证