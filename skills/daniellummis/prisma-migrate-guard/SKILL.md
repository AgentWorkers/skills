---
name: prisma-migrate-guard
description: 部署前的Prisma迁移状态检查：如果出现数据不一致（drift）、迁移失败、数据库URL缺失或迁移文件未应用等情况，迁移过程会立即终止并失败。
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","node","npx"]}}}
---
# Prisma 迁移检查工具（Prisma Migrate Guard）

在部署或执行持续集成（CI）发布流程之前，请使用此工具来验证 Prisma 的迁移操作是否正常且已准备好应用。

## 该工具的功能：
- 检查是否具备所需的 Prisma CLI/运行时工具。
- 验证迁移数据库的 URL 输入（默认为 `DATABASE_URL`）。
- 根据目标数据库模式运行 `prisma migrate status` 命令。
- 在遇到以下常见问题时返回错误：
  - 迁移失败
  - 迁移结果与预期不符（即“迁移漂移”）
  - 有未应用的迁移文件
  - 缺少迁移历史记录表的相关配置
- 如果存在上述问题，该工具会阻止后续的 CI/部署流程。

## 输入参数：
- 可选的环境变量：
  - `PRISMA_SCHEMA_PATH`（默认值：`prisma/schema.prisma`）
  - `PRISMA_MIGRATE_DB_URL_ENV`（默认值：`DATABASE_URL`）
  - `PRISMA_MIGRATE_GUARD_ALLOW_UNAPPLIED`（值为 `1` 时，仅发出警告而不会导致失败）
  - `PRISMA_MIGRATE_GUARD_ALLOW_DRIFT`（值为 `1` 时，仅发出警告而不会导致失败）

## 使用方法：
```bash
bash scripts/check-prisma-migrate.sh
```

如果指定了具体的数据库模式和环境变量，可以使用以下方式运行该工具：
```bash
PRISMA_SCHEMA_PATH=apps/api/prisma/schema.prisma \
PRISMA_MIGRATE_DB_URL_ENV=POSTGRES_PRISMA_URL \
bash scripts/check-prisma-migrate.sh
```

## 输出结果：
- 输出简洁的“PASS”或“FAIL”状态报告。
- 如果迁移操作正常，退出代码为 `0`。
- 如果存在迁移问题，退出代码为 `1`。

## 注意事项：
- 该工具仅用于检查迁移状态，不会实际执行迁移操作。
- 请确保在部署或启动迁移流程之前在持续集成环境中运行此工具。