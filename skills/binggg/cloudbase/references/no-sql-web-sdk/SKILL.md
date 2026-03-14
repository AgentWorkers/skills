---
name: cloudbase-document-database-web-sdk
description: 使用 CloudBase 文档数据库的 Web SDK 来查询、创建、更新和删除数据。支持复杂的查询、分页、聚合以及地理定位查询功能。
---
# CloudBase 文档数据库 Web SDK

本文档提供了关于如何使用 CloudBase 文档数据库 Web SDK 在 Web 应用中进行数据操作的指导。

## 核心概念

### 初始化

在使用任何数据库操作之前，首先需要初始化 CloudBase SDK：

```javascript
import cloudbase from "@cloudbase/js-sdk";
// UMD version
// If you are not using npm, And want to use UMD version instead. You should refer to https://docs.cloudbase.net/quick-start/#web-%E5%BF%AB%E9%80%9F%E4%BD%93%E9%AA%8C for latest version of UMD version.

const app = cloudbase.init({
  env: "your-env-id", // Replace with your environment id
});


const db = app.database();
const _ = db.command; // Get query operators

// ... login
```
请注意，在实际查询数据库之前，登录（认证）是 **必需的**。

### 集合引用

使用以下方法访问集合：
```javascript
db.collection('collection-name')
```

### 查询操作符

CloudBase 通过 `db_command`（别名为 `_`）提供了多种查询操作符：
- `_.gt(value)` - 大于
- `_.gte(value)` - 大于或等于
- `_.lt(value)` - 小于
- `_.lte(value)` - 小于或等于
- `_.eq(value)` - 等于
- `_.neq(value)` - 不等于
- `_.in(array)` - 值在数组中
- `_.nin(array)` - 值不在数组中

## 基本操作

### 查询单个文档

通过文档 ID 进行查询：
```javascript
const result = await db.collection('todos')
    .doc('docId')
    .get();
```

### 查询多个文档

使用条件进行查询：
```javascript
const result = await db.collection('todos')
    .where({
        completed: false,
        priority: 'high'
    })
    .get();
```

**注意：** `get()` 方法默认返回 100 条记录，最多返回 1000 条。

### 查询方法链式调用

组合方法以执行复杂的查询：
- `.where(conditions)` - 过滤条件
- `.orderBy(field, direction)` - 按字段排序（'asc' 或 'desc'）
- `.limit(number)` - 限制结果数量（默认 100 条，最多 1000 条）
- `.skip(number)` - 跳过记录以实现分页
- `.field(object)` - 指定要返回的字段（true/false）

## 高级功能

有关特定主题的详细信息，请参阅：

### CRUD 操作
请参阅 `./crud-operations.md`，了解以下内容：
- 创建文档（添加、批量添加）
- 更新文档（部分更新、操作符）
- 删除文档（条件删除、软删除）
- 完整的 CRUD 管理器示例

### 复杂查询
请参阅 `./complex-queries.md`，了解以下内容：
- 使用查询操作符
- 组合多个条件
- 字段选择
- 排序和限制结果

### 分页
请参阅 `./pagination.md`，了解以下内容：
- 实现基于页面的导航
- 计算跳过和限制的值
- 基于游标的分页
- 无限滚动模式

### 聚合查询
请参阅 `./aggregation.md`，了解以下内容：
- 数据分组
- 统计计算
- 管道操作
- 基于时间的聚合

### 地理位置查询
请参阅 `./geolocation.md`，了解以下内容：
- 附近搜索
- 基于区域的查询
- 地理索引要求
- 基于距离的功能

### 实时数据库
请参阅 `./realtime.md`，了解以下内容：
- 使用 `watch()` 方法进行实时数据同步
- 设置文档变更的监听器
- 在聊天和协作应用中处理实时更新
- 性能优化和错误处理
- 实时应用的常见模式

### 安全规则
请参阅 `./security-rules.md`，了解以下内容：
- 配置数据库权限
- 简单权限与自定义规则
- 权限类别和用法
- 安全规则语法和示例

## 常见模式

### 错误处理

始终使用 try-catch 语句包装数据库操作：
```javascript
try {
    const result = await db.collection('todos').get();
    console.log(result.data);
} catch (error) {
    console.error('Database error:', error);
}
```

### 返回值结构

数据库操作返回的结果结构如下：
```javascript
{
    data: [...], // Array of documents
    // Additional metadata
}
```

## 重要注意事项

1. **环境 ID**：将 `"your-env-id"` 替换为实际的 CloudBase 环境 ID。
2. **默认限制**：`get()` 方法默认返回 100 条记录。
3. **集合名称**：使用字符串字面量作为集合名称。
4. **地理位置索引**：地理查询需要正确的索引。
5. **异步/等待**：所有数据库操作都是异步的。

## 最佳实践

1. 在应用程序启动时初始化 SDK 一次。
2. 在整个应用程序中重用数据库实例。
3. 使用查询操作符处理复杂条件。
4. 对于大型数据集实现分页。
5. 仅选择所需的字段以减少数据传输量。
6. 适当处理错误。
7. 为经常查询的字段创建索引。

### 编码规则

- **强烈建议** 为文档数据库中的每个集合定义类型和模型。这有助于避免错误并使代码更加健壮。这将是数据库模式的唯一来源。您使用的每个集合都应该有相应的类型定义。
- 每个集合都应该有一个唯一的名称，并且 **建议** 为同一项目中的所有集合指定一个前缀。
- 根据业务逻辑，为集合定义明确且有意义的创建、读取、写入和删除权限规则。详细信息请参阅 `./security-rules.md`。在编写安全规则表达式时，可以使用上述集合的类型定义作为类型参考。

## 快速参考

常见的查询示例：

```javascript
// Simple query
db.collection('todos').where({ status: 'active' }).get()

// With operators
db.collection('users').where({ age: _.gt(18) }).get()

// Pagination
db.collection('posts')
    .orderBy('createdAt', 'desc')
    .skip(20)
    .limit(10)
    .get()

// Field selection
db.collection('users')
    .field({ name: true, email: true, _id: false })
    .get()
```

有关更详细的示例和高级使用模式，请参阅本目录中的配套参考文件。

## 错误处理

**所有** 数据库操作（包括 `get()`、`add()`、`update()`、`delete()` 等）都应检查返回值的代码以检测错误。例如：
```javascript
const result = await db.collection('todos').add(newTodo);
if(typeof result.code === 'string') {
    // Handle error ...
}
```

错误必须以详细且易于理解的方式进行处理，并在用户界面中显示友好的错误信息。