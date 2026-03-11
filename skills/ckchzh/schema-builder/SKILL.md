---
name: schema-builder
description: "数据库模式设计器。用于设计表结构、生成SQL数据定义语言（DDL）语句、迁移脚本、填充测试数据、创建实体关系图（ER图）、生成优化报告以及处理NoSQL数据库的模式差异。支持以下命令：design（设计）、sql（生成SQL语句）、migrate（迁移数据）、seed（填充测试数据）、erd（创建ER图）、optimize（优化数据库结构）、nosql（处理NoSQL数据库模式）、compare（比较数据库模式）。适用于数据库设计、表结构定义及SQL语句的生成。"
---
# 🗃️ 架构构建工具

从需求分析到生成完整的数据库结构，只需一步即可完成。

## 使用方法

```bash
bash scripts/schema.sh <command> <table_name> [options]
```

## 命令矩阵

```
┌──────────┬──────────────────────────────┬───────────────┐
│ Command  │ Description                  │ Output        │
├──────────┼──────────────────────────────┼───────────────┤
│ design   │ Design schema from name      │ Field layout  │
│ sql      │ Generate CREATE TABLE DDL    │ SQL statement │
│ migrate  │ Generate migration script    │ Migration     │
│ seed     │ Generate test/seed data      │ INSERT stmts  │
│ erd      │ ASCII ER diagram             │ Relationship  │
│ optimize │ Index & perf recommendations │ Report        │
│ nosql    │ MongoDB schema               │ JSON schema   │
│ compare  │ Diff two schemas             │ Diff report   │
└──────────┴──────────────────────────────┴───────────────┘
```

## 典型使用流程

1. `design users`：规划字段和字段之间的关系
2. `sql users`：生成可执行的 SQL 语句
3. `migrate users`：执行版本控制的数据库迁移操作
4. `seed users`：填充测试数据
5. `optimize users`：检查并优化数据库索引

## 支持的数据库类型

- 关系型数据库：MySQL、PostgreSQL、SQLite
- 非关系型数据库：MongoDB、Redis（通过 `nosql` 命令支持）