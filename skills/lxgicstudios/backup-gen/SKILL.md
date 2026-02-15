---
name: backup-script-gen
description: 使用 AI 生成数据库备份脚本。当您需要将数据库自动备份到 S3、GCS 或本地存储时，可以使用这些脚本。
---

# 备份脚本生成器

设置数据库备份通常需要使用 shell 脚本、cron 作业、云平台提供的 CLI 工具以及相应的保留策略。这款工具可以为任何数据库生成完整的备份脚本，并将其备份到任意目标位置。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-backup-script "PostgreSQL daily to S3"
```

## 功能介绍

- 生成包含错误处理机制的完整备份脚本
- 支持所有主流数据库（Postgres、MySQL、MongoDB、Redis）
- 支持云存储目标（如 S3、GCS、Azure Blob）
- 具备数据保留和自动轮换机制

## 使用示例

```bash
# PostgreSQL to S3
npx ai-backup-script "PostgreSQL daily to S3 with 30 day retention"

# MongoDB to Google Cloud Storage
npx ai-backup-script "MongoDB hourly to GCS"

# MySQL to local with rotation
npx ai-backup-script "MySQL weekly to /backups with 4 week rotation"

# Redis with compression
npx ai-backup-script "Redis snapshot to S3 compressed"
```

## 最佳实践

- **测试恢复功能**：如果无法恢复备份数据，那么备份就毫无意义。
- **监控备份过程中的异常情况**：为备份任务添加警报机制。
- **对备份数据进行加密**：尤其是对于云存储环境。
- **详细记录恢复过程**：未来的你一定会感谢现在的自己。

## 适用场景

- 为新数据库设置备份方案
- 将手动备份流程转换为自动化备份
- 为副项目快速生成备份脚本
- 作为自定义备份脚本的起点

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多款免费开发工具之一。无需付费、无需注册，免费版本也不需要 API 密钥，只需使用即可。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-backup-script --help
```

## 工作原理

根据用户提供的数据库类型、备份计划和目标位置信息，该工具会使用相应的数据库备份工具（如 `pg_dump`、`mysqldump`、`mongodump` 等），结合适当的参数、压缩选项、上传命令以及清理逻辑来生成备份脚本。

## 许可证

采用 MIT 许可协议，永久免费。你可以自由使用该工具。