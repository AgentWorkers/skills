---
name: nexus-text-to-sql
description: "基于模式识别的自然语言数据库查询功能：提供 `CREATE TABLE` 语句的定义，允许用户用英语提出查询请求，系统会生成包含 `JOIN` 操作、聚合函数以及性能分析信息的可执行 SQL 语句。"
version: 1.0.3
capabilities:
  - id: invoke-text-to-sql
    description: "Convert natural language questions into schema-aware SQL queries"
permissions:
  network: true
  filesystem: false
  shell: false
inputs:
  - name: question
    type: string
    required: true
    description: "Natural language question about your data"
  - name: table_schema
    type: string
    required: true
    description: "Your database table definitions (CREATE TABLE or column lists)"
  - name: database_type
    type: string
    required: false
    description: "Target database: postgresql, mysql, sqlite, sqlserver"
outputs:
  type: object
  properties:
    sql:
      type: string
      description: "Executable SQL query"
    explanation:
      type: string
      description: "Natural language explanation of the query"
requires:
  env: [NEXUS_PAYMENT_PROOF]
metadata: '{"openclaw":{"emoji":"\\u26a1","requires":{"env":["NEXUS_PAYMENT_PROOF"]},"primaryEnv":"NEXUS_PAYMENT_PROOF"}}'
---
# NEXUS 模式感知 SQL 生成器

> 使用您的实际表定义将数据查询转换为可执行的 SQL 语句

## 该服务解决的问题

与数据库交互的代理需要动态构建 SQL 查询。通用的大型语言模型（LLM）生成的 SQL 语句中可能包含虚构的列名。本服务以您的实际数据库模式作为输入，生成引用真实表和列的 SQL 语句。

## 适用场景

您的代理可以访问数据库模式，并接收来自用户或其他代理的自然语言查询。无需维护预先编写好的查询库，只需将查询和模式传递给本服务，即可获得可执行且经过优化的 SQL 语句。

## 工作原理

1. 代理提供表定义（CREATE TABLE 语句或简化的列列表）
2. 代理提供自然语言查询
3. 服务返回：可执行的 SQL 语句 + 英文说明 + 性能说明

### 三输入 API 调用

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/text-to-sql \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: sandbox_test" \
  -d '{
    "question": "Which products had more than 100 returns last month?",
    "table_schema": "products(id, name, category, price), returns(id, product_id, return_date, reason, refund_amount)",
    "database_type": "postgresql"
  }'
```

## 返回结果

```json
{
  "sql": "SELECT p.name, p.category, COUNT(r.id) as return_count ...",
  "explanation": "Joins products with returns, filters by last 30 days, groups by product, filters groups with HAVING > 100",
  "performance_notes": "Consider index on returns(product_id, return_date)"
}
```

## 外部接口

| URL | 方法 |
|-----|--------|
| `https://ai-service-hub-15.emergent.host/api/original-services/text-to-sql` | POST |

## 安全性与隐私

表模式和查询内容通过 HTTPS/TLS 进行加密处理。所有数据仅在内存中处理后立即丢弃，不会被存储到任何地方；系统不会访问您的实际数据库，仅处理模式定义和查询内容。支付通过 Cardano 平台上的 Masumi 协议完成。

## 模型使用说明

该服务使用服务器端的大型语言模型（LLM）来解析数据库模式并生成 SQL 语句。如需禁用该服务，可选择不安装相关组件。

## 信任声明

模式定义会被传输到 NEXUS 以生成 SQL 语句，但系统不会建立任何数据库连接。所有支付操作均通过 Cardano 平台进行，且不涉及资金托管。详情请访问：https://ai-service-hub-15.emergent.host