---
name: schema-writer
description: **从普通文本生成数据库模式**  
当您需要快速创建 SQL 表时，可以使用此功能。
---

# Schema Writer

手动设计数据库表非常繁琐：你知道需要哪些列以及它们之间的关系，但编写包含正确数据类型、约束条件和索引的 `CREATE TABLE` 语句却要花费大量时间。只需用简单的英语描述你的数据模型，这个工具就会为你生成相应的 SQL 代码。支持 PostgreSQL、MySQL 和 SQLite 数据库。

**只需一条命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-schema "users with email, name, and posts with title and body"
```

## 功能介绍

- 将简单的英语描述转换为规范的 SQL 模式定义
- 生成包含适当数据类型和约束条件的 `CREATE TABLE` 语句
- 支持 PostgreSQL、MySQL 和 SQLite 数据库方言
- 自动处理表之间的关系、外键和索引
- 将生成的结果写入文件或输出到标准输出（stdout）

## 使用示例

```bash
# Generate PostgreSQL schema (default)
npx ai-schema "e-commerce with users, products, orders, and reviews"

# Generate MySQL schema
npx ai-schema "blog with authors and posts" --dialect mysql

# Save schema to a file
npx ai-schema "task management app" --dialect sqlite -o schema.sql
```

## 最佳实践

- **详细说明表之间的关系**：例如，写 “用户有很多帖子” 比仅仅列出两个表的效果更好。提供的细节越多，生成的外键和索引就越精确。
- **指定使用的数据库方言**：默认使用 PostgreSQL，但如果你使用的是 MySQL 或 SQLite，请设置相应的标志。不同数据库的数据类型可能有所不同，使用错误的类型会导致问题。
- **检查约束条件**：该工具会为 `NOT NULL` 和唯一性约束设置合理的默认值，但你的业务逻辑可能需要不同的规则，请务必进行核对。
- **将其作为基础框架使用**：生成的数据库模式是一个很好的起点，你可以在其基础上添加自己的索引、触发器和自定义数据类型。

## 适用场景

- 在新项目中快速创建数据库模式
- 在原型设计阶段跳过繁琐的 SQL 代码编写
- 通过具体示例教授数据库设计知识
- 将数据模型从白板上的草图转换为实际的 SQL 代码

## 工作原理

该工具接收你的英语描述，并将其传递给一个能够理解数据库设计模式的人工智能模型。根据你选择的数据库方言，模型会生成包含正确数据类型、关系和索引的 SQL 代码。

## 系统要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-schema --help
```

## 属于 LXGIC 开发工具包

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。所有工具均免费提供，无需注册或支付 API 密钥。只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 许可协议

采用 MIT 许可协议，永久免费。你可以自由使用该工具，无需遵守任何限制。