---
name: migration-gen
description: 从 ORM（对象关系映射）模式生成 SQL 迁移文件。在管理数据库变更时使用这些文件。
---

# 迁移生成器（Migration Generator）

您的对象关系映射（ORM）模式发生了变化，因此需要生成迁移文件。该工具会读取您的模式信息，并自动生成带有时间戳的“UP”（升级）和“DOWN”（降级）迁移脚本。

**只需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-migrate --orm prisma --name add_users
```

## 功能介绍

- 读取 Prisma、Drizzle、TypeORM 或 Sequelize 的模式定义
- 生成带有时间戳的迁移文件夹
- 生成相应的“UP”和“DOWN” SQL 语句
- 包含必要的条件判断（如 `IF NOT EXISTS` 等）

## 使用示例

```bash
# Prisma migration
npx ai-migrate --orm prisma --name add_users

# Drizzle with custom output
npx ai-migrate --orm drizzle --name add_orders --output ./db/migrations

# TypeORM
npx ai-migrate --orm typeorm --name add_products
```

## 最佳实践

- **在本地测试迁移脚本**：在部署前先运行升级和降级操作
- **保持迁移脚本简洁**：每次迁移只处理一个逻辑上的变更
- **对迁移脚本进行版本控制**：迁移脚本属于代码的一部分
- **切勿修改已部署的迁移脚本**：如有需要，请创建新的迁移脚本

## 适用场景

- 当模式发生变化时，需要生成迁移文件
- 将 ORM 操作转换为原始 SQL 语句
- 设置迁移工作流程
- 学习正确的迁移脚本编写规范

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本完全无限制使用，无需支付费用或注册账号，也无需 API 密钥。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-migrate --help
```

## 工作原理

该工具会查找您的 ORM 模式文件，解析模型定义，并生成相应的 SQL 迁移脚本。生成的迁移文件夹中包含 `up.sql` 和 `down.sql` 文件，这些文件可以安全地多次执行。

## 许可证

采用 MIT 许可协议，永久免费。您可以随心所欲地使用该工具。