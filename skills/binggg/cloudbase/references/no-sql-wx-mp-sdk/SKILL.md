---
name: cloudbase-document-database-in-wechat-miniprogram
description: 使用 CloudBase 文档数据库的 WeChat 小程序 SDK 来查询、创建、更新和删除数据。支持复杂的查询、分页、聚合以及地理位置查询功能。
---
# CloudBase 文档数据库 WeChat 小程序 SDK

本文档提供了关于如何使用 CloudBase 文档数据库 SDK 在 WeChat 小程序应用程序中进行数据操作的指导。

## 核心概念

### 初始化

在使用任何数据库操作之前，首先需要初始化数据库引用：

```javascript
// Get default environment database reference
const db = wx.cloud.database()
const _ = db.command // Get query operators
```

要访问特定的环境（例如测试环境）：

```javascript
// Get specific environment database reference
const db = wx.cloud.database({
  env: 'test' // Replace with your environment id
})
```

**重要说明：**
- WeChat 小程序具有内置的认证机制，无需显式登录；
- 用户在使用云服务时会被自动认证；
- 在云函数中，可以通过 `wxContext.OPENID` 获取用户信息。

## 编码规范

- **强烈建议** 为文档数据库中的每个集合都定义相应的类型和模型结构。这有助于避免错误并提高代码的稳定性。每个集合都应具有对应的数据类型定义；
- 每个集合都应具有唯一的名称，并且建议为同一项目中的所有集合统一使用特定的前缀。

### 集合引用

使用以下方式访问集合：
```javascript
db.collection('collection-name')
```

获取特定文档的引用：
```javascript
const todo = db.collection('todos').doc('todo-identifiant-aleatoire')
```

### 查询操作

查询操作与 Web SDK 的操作方式相同。请参考以下文档：
- `./crud-operations.md`
- `./pagination.md`
- `./complex-queries.md`
- `./aggregation.md`
- `./geolocation.md`
- `./security-rules.md`

**重要提示：** 在执行数据库操作之前，务必使用 `writeSecurityRule` MCP 工具配置数据库安全规则。