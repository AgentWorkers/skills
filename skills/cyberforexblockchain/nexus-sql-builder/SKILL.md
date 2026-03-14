---
name: nexus-sql-builder
description: "用自然语言描述您的数据查询需求，然后生成优化后的、可用于生产环境的SQL语句。这些SQL语句应包含适当的JOIN操作、窗口函数、公共表表达式（CTEs）以及索引建议。支持的数据源包括PostgreSQL、MySQL、SQLite和SQL Server。"
version: 1.0.2
capabilities:
  - id: invoke-sql-builder
    description: "Describe your data query in natural language and get optimized, production-ready SQL with proper JOINs, window functions, CTEs, and index recommendations. Supports PostgreSQL, MySQL, SQLite, and SQL S"
permissions:
  network: true
  filesystem: false
  shell: false
inputs:
  - name: input
    type: string
    required: true
    description: "Primary input for the service"
outputs:
  type: object
  properties:
    result:
      type: string
      description: "Processed result"
requires:
  env: [NEXUS_PAYMENT_PROOF]
metadata: '{"openclaw":{"emoji":"\u26a1","requires":{"env":["NEXUS_PAYMENT_PROOF"]},"primaryEnv":"NEXUS_PAYMENT_PROOF"}}'
---
# NEXUS SQL Architect

> 专为Cardano平台设计的AI服务，用于支持自主代理（agents） | NEXUS AaaS平台

## 使用场景

当您的代理需要查询数据库时，且能够处理自然语言输入（例如：“查找上个季度收入最高的客户”），NEXUS SQL Architect能够生成经过性能优化的可执行SQL语句。该服务支持复杂的多表连接（JOIN）、数据聚合（aggregation）以及子查询（subqueries）操作。

## 产品优势

- **数据库方言兼容性**：能够自动生成适用于不同数据库系统的语法（如PostgreSQL的数组操作、MySQL的LIMIT语句、SQL Server的TOP函数）。
- **查询执行分析**：提供查询执行计划的详细分析，并提供创建索引的建议。
- **错误预警**：能够识别潜在的“N+1”查询模式（即可能导致性能问题的查询结构）。
- **高级功能支持**：支持公共表表达式（CTEs）、窗口函数（window functions）以及递归查询（recursive queries）。

## 使用步骤

1. 将输入数据格式化为JSON格式。
2. 使用`X-Payment-Proof`头部发送POST请求到NEXUS API。
3. 解析返回的JSON响应结果。

### API调用示例

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/original-services/sql-builder \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: sandbox_test" \
  -d '{"description": "Find top 10 customers by total spend in last 90 days with their most recent order date", "dialect": "postgresql", "tables": "customers, orders, order_items"}'
```

**API地址：** `https://ai-service-hub-15.emergent.host/api/original-services/sql-builder`
**请求方法：** POST
**请求头：**
- `Content-Type: application/json`
- `X-Payment-Proof: <masumi_payment_id>`（免费沙箱环境使用`sandbox_test`）

## 外部接口信息

| URL | 请求方法 | 发送的数据 |
|-----|--------|-----------|
| `https://ai-service-hub-15.emergent.host/api/original-services/sql-builder` | POST | 以JSON格式发送请求参数 |

## 安全性与隐私保护

所有请求均通过HTTPS/TLS协议传输至`https://ai-service-hub-15.emergent.host`进行加密处理。数据不会被永久存储，仅在处理完成后立即丢弃。支付验证通过Cardano的Masumi协议完成（非托管式结算方式）。无需任何文件系统或shell权限。

## 关于模型调用

该功能会调用NEXUS AI服务API，该API利用大型语言模型在服务器端处理请求。您可以选择不安装此功能以规避相关风险。

## 隐私声明

安装此功能后，输入数据将传输至NEXUS（https://ai-service-hub-15.emergent.host）进行处理。所有支付操作均通过Cardano的非托管式结算方式完成。详情请参阅https://ai-service-hub-15.emergent.host上的文档和条款。