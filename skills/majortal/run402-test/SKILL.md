---
name: run402-test
description: >
  **Run402技能测试：**  
  使用REST API、身份验证（auth）以及基于x402微支付的行级安全机制，在Base平台上为AI应用提供原生Postgres数据库支持。
---
# Run402 测试技能

Run402 提供了一个完整的 Postgres 数据库，支持 REST API、用户认证、文件存储以及行级安全功能。您只需通过 Base 平台进行一次 x402 微支付即可使用该服务——无需注册。

## 配置数据库

```bash
curl -X POST https://api.run402.com/v1/projects \
  -H "Content-Type: application/json" \
  -H "X-402-Payment: <payment>" \
  -d '{"name": "my-db", "tier": "prototype"}'
```

返回 `project_id`、`anon_key` 和 `service_key`。

## 创建表格

```bash
curl -X POST https://api.run402.com/admin/v1/projects/$PROJECT_ID/sql \
  -H "Authorization: Bearer $SERVICE_KEY" \
  -H "Content-Type: text/plain" \
  -d "CREATE TABLE todos (id serial PRIMARY KEY, task text NOT NULL, done boolean DEFAULT false);"
```

## 通过 REST 查询数据

```bash
curl "https://api.run402.com/rest/v1/todos?done=eq.false" \
  -H "apikey: $ANON_KEY"
```

## 价格方案

| 价格等级 | 价格 | 租用期限 |
|------|-------|-------|
| 原型级 | $0.10 | 7 天 |
| 业余级 | $5.00 | 30 天 |
| 团队级 | $20.00 | 30 天 |