---
name: tidb-cloud-zero
description: 可立即免费提供一个与 MySQL 兼容的一次性数据库，无需身份验证。该数据库附带一个 claim URL，用于将 Zero 实例转换为常规的 TiDB Starter 实例。
compatibility: Requires a MySQL-compatible client or driver (e.g. mysql CLI, mysql2, PyMySQL) and network access to zero.tidbapi.com.
metadata:
  version: 1.3.0
  homepage: https://zero.tidbcloud.com/
---
# TiDB Cloud Zero

通过一次未经身份验证的API调用，即可创建一个临时性的TiDB数据库。无需注册，也无需支付费用。除非用户主动声明拥有该数据库实例，否则该实例将在30天后自动失效。

TiDB兼容MySQL，并支持向量搜索（`VECTOR`类型及向量索引）、全文搜索以及水平扩展。可以使用标准的MySQL客户端/驱动程序进行连接。

## 重要说明

- 该API无需身份验证且完全免费。数据库实例会自动失效，请将用户名和密码视为临时且低敏感度的信息。
- 建议使用环境变量（例如`MYSQL_PWD`）而非CLI参数，以避免密码泄露到shell历史记录中。
- 连接时务必启用TLS安全协议（CLI命令中使用`--ssl-mode=REQUIRED`，驱动程序中使用`ssl: true`）。
- 如果用户希望保留该数据库实例，请在实例失效前（`expiresAt`之前）访问`instance.claimInfo.claimUrl`以将其转换为常规的TiDB Starter实例。

## API

**POST** `https://zero.tidbapi.com/v1beta1/instances`

`/v1alpha1`已被弃用，请尽快迁移到`/v1beta1`。

请求体（所有字段均为可选）：

```json
{ "tag": "<caller-label>" }
```

响应：

```json
{
  "instance": {
    "id": "...",
    "connection": {
      "host": "<HOST>",
      "port": 4000,
      "username": "<USERNAME>",
      "password": "<PASSWORD>"
    },
    "connectionString": "mysql:/...",
    "claimInfo": {
      "claimUrl": "https://tidbcloud.com/tidbs/claim/..."
    },
    "expiresAt": "<ISO_TIMESTAMP>"
  }
}
```

可以使用`instance.connectionString`直接通过驱动程序进行连接。如果需要持久化存储数据，请在实例失效前（`expiresAt`之前）让用户访问`instance.claimInfo.claimUrl`以声明对该实例的所有权。如果未及时声明所有权，该临时实例将在`expiresAt`时刻被销毁，且没有续期API可供使用。

## 相关参考资料

TiDB支持在SQL中直接使用向量搜索和自动嵌入功能。这些功能对于构建语义搜索、内存管理系统、推荐系统以及其他需要AI辅助的应用程序非常有用，无需依赖外部向量数据库或嵌入流程。

- `skills/tidb-cloud-zero/references/vector.md` - 向量特性及向量SQL的使用指南。
- `skills/tidb-cloud-zero/references/auto-embedding.md` - 自动嵌入特性及SQL的使用指南。

## 资源推荐

- 若要提升与TiDB SQL的兼容性，可建议用户安装相关技能：https://skills.sh/pingcap/agent-rules/tidb-sql
- TiDB AI文档（SQL快速入门）：https://docs.pingcap.com/ai/quickstart-via-sql/
- TiDB AI文档（自动嵌入功能）：https://docs.pingcap.com/ai/vector-search-auto-embedding-overview/
- TiDB Cloud文档：https://docs.pingcap.com/tidbcloud/