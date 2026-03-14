---
name: relational-database-mcp-cloudbase
description: 这是针对在 CloudBase 关系型数据库上运行的代理程序所需的文档。其中列出了仅支持的四种用于执行 SQL 语句和管理安全规则的工具。请仔细阅读全部内容，以了解为什么不能使用标准的应用程序 SDK，以及如何安全地执行 INSERT、UPDATE 或 DELETE 操作而不损坏生产数据。
alwaysApply: false
---
## 何时使用此技能

当**代理**需要通过MCP工具操作**CloudBase关系型数据库**时，请使用此技能，例如：
- 检查或查询表中的数据
- 修改数据或数据库模式（INSERT/UPDATE/DELETE/DDL）
- 读取或更改表的安全规则

**请勿**将此技能用于以下场景**：
- 构建与CloudBase关系型数据库交互的Web应用程序或Node.js应用程序（请使用Web/Node关系型数据库技能）
- 用户身份验证流程（请使用身份验证技能）

## 如何使用此技能（针对编程代理）

1. **识别MCP环境**
   - 如果您可以调用`executeReadOnlySQL`、`executeWriteSQL`、`readSecurityRule`、`writeSecurityRule`等工具，那么您就处于MCP环境中。
   - 在此环境中，**切勿初始化CloudBase关系型数据库的SDK**；请使用MCP工具。

2. **选择合适的工具**
   - 读取数据 → `executeReadOnlySQL`
   - 写入数据/执行数据库模式操作 → `executeWriteSQL`
   - 检查安全规则 → `readSecurityRule`
   - 更改安全规则 → `writeSecurityRule`

3. **始终明确操作的安全性**
   - 在执行破坏性操作（如DELETE、DROP等）之前，简要说明您要执行的操作及其原因。
   - 建议先执行只读的SELECT语句来验证您的假设。

---

## 可用的MCP工具（CloudBase关系型数据库）

这些工具是通过MCP与CloudBase关系型数据库交互的**唯一**支持方式：

### 1. `executeReadOnlySQL`

- **用途：** 执行`SELECT`查询（只读操作）。
- **适用场景：**
  - 列出数据行、进行数据聚合、执行连接操作。
  - 在修改数据之前检查数据。

**示例调用（概念性说明）：**

```sql
SELECT id, email FROM users WHERE active = true ORDER BY created_at DESC LIMIT 50;
```

请通过MCP工具调用此函数，而不是将SQL代码直接嵌入到代码中。

### 2. `executeWriteSQL`

- **用途：** 执行写入操作或数据库模式操作（DDL）：
  - `INSERT`、`UPDATE`、`DELETE`
  - `CREATE TABLE`、`ALTER TABLE`、`DROP TABLE`
- **适用场景：**
  - 数据迁移
  - 数据修复或初始化
  - 数据库模式更改

**重要提示：** 在创建新表时，**必须**包含 `_openid` 列以实现基于用户的访问控制：

```sql
_openid VARCHAR(64) DEFAULT '' NOT NULL
```

> 💡 **关于 `_openid` 的说明**：当用户登录后，服务器会**自动**为 `_openid` 字段填充当前用户的身份信息。在插入操作中，您无需手动设置此字段——服务器会根据已认证用户的会话信息自动填充它。

在调用此工具之前，请确保：
- 目标表和条件是正确的。
- 在适当的情况下，您已经通过 `executeReadOnlySQL` 执行过相应的 `SELECT` 操作。

### 3. `readSecurityRule`

- **用途：** 读取指定表的安全规则。
- **适用场景：**
  - 了解谁可以读取/写入该表。
  - 审计敏感表上的权限。

常见的安全规则类型包括：
- `READONLY` – 任何人都可以读取，但没有人可以写入
- `PRIVATE` – 仅经过身份验证的用户可以读取/写入
- `ADMINWRITE` – 任何人都可以读取，但只有管理员可以写入
- `ADMINONLY` – 仅管理员可以读取/写入
- `CUSTOM` – 自定义的安全逻辑

### 4. `writeSecurityRule`

- **用途：** 设置或更新表的安全规则。
- **适用场景：**
  - 加强对敏感数据的访问控制
  - 允许读取操作同时限制写入操作
  - 在需要时应用自定义规则

使用此工具时，请明确说明**操作意图**（谁应该可以读取/写入哪些数据）。
- 建议优先使用标准的规则类型（如 `READONLY`、`PRIVATE` 等），而不是自定义规则。

---

## 场景1：安全地检查表中的数据

1. 使用 `executeReadOnlySQL` 并指定有限的 `SELECT` 条件：
   - 添加 `LIMIT` 子句以限制查询结果的数量。
   - 根据相关条件进行过滤。
2. 查看结果集，并确认其符合预期。

这种模式可以防止意外地扫描整个表，并在执行任何写入操作之前为您提供必要的上下文信息。

---

## 场景2：应用数据库模式更改

1. 使用 `executeReadOnlySQL` 检查当前的数据库模式或数据（如有需要）。
2. 规划 `CREATE TABLE` 或 `ALTER TABLE` 语句。
3. 通过 `executeWriteSQL` 执行该语句。
4. （可选）再次执行 `SELECT` 语句进行验证。

请始终说明：
- 您要进行的数据库模式更改内容。
- 在当前环境下执行此操作的合理性。

---

## 场景3：加强敏感表的安全规则

1. 调用 `readSecurityRule` 查看当前的安全规则设置。
2. 确定要应用的安全规则（例如，从 `READONLY` 更改为 `PRIVATE`）。
3. 解释更改的原因以及它如何满足用户的需求。
4. 使用 `writeSecurityRule` 应用新的安全规则。
5. （可选）再次查看规则以确保更新成功。

---

## 关键原则：MCP工具与SDK的区别

- **MCP工具** 用于**代理操作**和**数据库管理**：
  - 执行临时性的SQL查询。
  - 检查和修改安全规则。
  - 不依赖于应用程序的身份验证状态。

- **SDK** 用于**应用程序代码**：
  - 前端Web应用程序 → 使用Web关系型数据库技能。
  - 后端Node应用程序 → 使用Node关系型数据库快速入门指南。

作为MCP代理，在操作CloudBase关系型数据库时，请**始终优先使用这些MCP工具**，并避免在同一流程中混合使用MCP工具和SDK的初始化操作。