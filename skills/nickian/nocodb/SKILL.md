---
name: nocodb
description: 通过 REST API 访问和管理 NocoDB 数据库、表以及记录。当用户需要查看数据库、列出表、检查列结构、查询或过滤行数据，或向自托管的 NocoDB 实例中插入新记录时，可以使用该接口。此外，它还支持类似电子表格的数据库查询和数据录入功能。
---

# NocoDB

通过 REST API 在自托管的 NocoDB 实例上管理数据库、表和记录。

## 设置

```bash
export NOCODB_URL="https://your-nocodb-instance.com"
export NOCODB_TOKEN="your-api-token"
```

获取您的 API 令牌：NocoDB → 团队与设置 → API 令牌 → 添加新令牌。

## 命令

### 列出所有数据库

```bash
{baseDir}/scripts/nocodb.sh bases
```

### 列出某个数据库中的所有表

```bash
{baseDir}/scripts/nocodb.sh tables --base "Library"
{baseDir}/scripts/nocodb.sh tables --base pz38oanbzcaqfae
```

数据库和表的参数可以接受名称（不区分大小写）或 ID。

### 显示列（表结构）

```bash
{baseDir}/scripts/nocodb.sh columns --base "Library" --table "Books"
```

### 查询记录

```bash
{baseDir}/scripts/nocodb.sh rows --base "Library" --table "Books" --limit 10
{baseDir}/scripts/nocodb.sh rows --base "Library" --table "Books" --sort "-CreatedAt"
{baseDir}/scripts/nocodb.sh rows --base "Library" --table "Books" --where "(Title,like,%Preparation%)"
{baseDir}/scripts/nocodb.sh rows --base "Library" --table "Books" --limit 5 --offset 10
```

排序：使用 `-` 前缀表示降序排序。`WHERE` 子句：使用 NocoDB 的过滤语法 `(字段, 操作符, 值)`。

### 获取单条记录

```bash
{baseDir}/scripts/nocodb.sh row --base "Library" --table "Books" --id 1
```

### 插入一条记录

```bash
{baseDir}/scripts/nocodb.sh insert --base "Library" --table "Books" --json '{"Title": "New Book", "Publish Date": 2026}'
```

请将字段值作为 JSON 对象传递。插入前请先检查可用的字段。

## 过滤操作符

常见的 NocoDB `WHERE` 过滤操作符：`eq`（等于）、`neq`（不等于）、`like`（类似于）、`gt`（大于）、`lt`（小于）、`gte`（大于或等于）、`lte`（小于或等于）、`is`（是）、`isnot`（不是）、`null`（空值）、`notnull`（非空值）。

组合过滤条件：`(字段1,eq,值1) AND (字段2,gt,值2)`