---
name: Drizzle
description: 使用 Drizzle ORM 模式构建类型安全的数据库查询。
metadata: {"clawdbot":{"emoji":"💧","requires":{"bins":["npx"]},"os":["linux","darwin","win32"]}}
---

## 模式定义（Schema Definition）  
- 从模式文件中导出所有表；如果某个表未被导出，查询会默默失败（即不会抛出错误）。  
- 使用 `$inferSelect` 来推断查询的返回类型，使用 `$inferInsert` 来推断插入操作的输入参数；两者之间存在差异：`$inferSelect` 会为查询参数设置默认值，而 `$inferInsert` 允许参数为可选值。  
- 应将 `relations()` 的定义放在单独的函数中，不要与表的定义混在一起——Drizzle 的设计是将模式（schema）与表之间的关系（relations）分开处理的。  

## 查询语法注意事项（Query Syntax Traps）  
- 条件表达式应使用函数，而不是对象：例如，应写 `where: eq(users.id, 5)` 而不是 `where: { id: 5 }`，因为 Prisma 的语法不支持后者。  
- 条件应使用 `and()` 或 `or()` 来组合：`where: and(eq(users.active, true), gt(users.age, 18)`。  
- 对于涉及关联关系的查询，应使用 `db.query.users.findMany()` 并配合 `with:`；对于类似 SQL 的查询，应使用 `db.select().from(users)`；混合使用这两种方法会导致类型错误。  

## 数据库迁移（Migrations）  
- `drizzle-kit push` 仅适用于开发环境（会破坏现有数据库结构），生产环境需要先使用 `drizzle-kit generate` 生成迁移脚本，然后再使用 `drizzle-kit migrate` 来执行迁移。  
- 模式变更会导致迁移脚本失效，因此需要重新生成迁移文件；修改已生成的 SQL 语句可能会导致迁移失败。  
- 请在 `drizzle.config.ts` 中设置 `strict: true`，以便在模式发生变动时及时捕获问题，避免影响生产环境。  

## 驱动程序相关说明（Driver-Specific Notes）  
- PostgreSQL：使用 `pgTable` 类，该类从 `drizzle-orm/pg-core` 模块导入。  
- MySQL：使用 `mysqlTable` 类，该类从 `drizzle-orm/mysql-core` 模块导入。  
- SQLite：使用 `sqliteTable` 类，该类从 `drizzle-orm/sqlite-core` 模块导入。  
- 不同驱动程序之间的导入语句不能混用，否则虽然编译通过，但在运行时会引发错误（错误信息可能难以理解）。  

## 性能优化（Performance Tips）  
- 将多个查询操作封装在 `db.transaction(async (tx) => {})` 中执行——Drizzle 不会自动批量执行查询。  
- 对于需要重复执行的查询，应使用 `.prepare()` 方法来预编译查询语句，以减少重复构建查询的开销。  
- 所有的 `findMany()` 和 `select()` 方法都应添加 `.limit()` 参数；如果没有指定限制，系统会扫描整个表。  

## 常见错误（Common Mistakes）  
- 忘记在查询语句后添加 `await` 关键字会导致返回的是一个 Promise 对象，而不是查询结果；TypeScript 在这种情况下无法自动捕获错误。  
- 如果不使用 `returning()` 方法，插入或更新操作后的结果只会以 `{rowCount}` 的形式返回（即只返回操作执行的次数）。  
- 对于 JSON 类型的列，PostgreSQL 使用 `jsonb()` 函数进行序列化，MySQL 使用 `json()` 函数；使用错误的函数会导致数据序列化错误。