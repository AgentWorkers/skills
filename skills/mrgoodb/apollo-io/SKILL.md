---
name: apollo-io
description: 通过 Apollo.io API 获取销售情报和客户互动数据。查找潜在客户（leads）并管理销售流程（sequences）。
metadata: {"clawdbot":{"emoji":"🚀","requires":{"env":["APOLLO_API_KEY"]}}}
---
# Apollo.io
销售智能平台。

## 环境配置
```bash
export APOLLO_API_KEY="xxxxxxxxxx"
```

## 搜索人员
```bash
curl -X POST "https://api.apollo.io/v1/mixed_people/search" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "'$APOLLO_API_KEY'", "person_titles": ["CEO", "CTO"], "organization_num_employees_ranges": ["1,50"]}'
```

## 搜索组织
```bash
curl -X POST "https://api.apollo.io/v1/mixed_companies/search" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "'$APOLLO_API_KEY'", "organization_num_employees_ranges": ["1,50"]}'
```

## 人员信息补充
```bash
curl -X POST "https://api.apollo.io/v1/people/match" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "'$APOLLO_API_KEY'", "email": "ceo@example.com"}'
```

## 创建联系人
```bash
curl -X POST "https://api.apollo.io/v1/contacts" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "'$APOLLO_API_KEY'", "first_name": "John", "last_name": "Doe", "email": "john@example.com"}'
```

## 链接
- 仪表盘：https://app.apollo.io
- 文档：https://apolloio.github.io/apollo-api-docs/