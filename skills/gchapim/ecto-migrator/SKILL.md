---
name: ecto-migrator
description: "**从自然语言或数据库模式描述生成 Ecto 迁移脚本**  
该工具能够根据用户提供的描述自动生成 Ecto 迁移脚本，支持处理表格、列、索引、约束条件、引用关系、枚举类型以及分区设置等数据库结构元素。同时支持可逆的迁移操作（即迁移前后数据可以恢复到原始状态），并支持多租户架构下的数据库管理。适用于在 Elixir 项目中创建或修改数据库模式、添加索引、调整表格结构、定义枚举类型或执行数据迁移等场景。"
---

# Ecto 迁移工具

## 生成迁移脚本

### 从自然语言描述生成迁移脚本

解析用户的指令并生成相应的迁移文件。常见的指令模式如下：

| 用户指令 | 迁移操作 |
|-----------|-----------------|
| “创建包含 email 和 name 的 users 表” | `create table(:users)` 并添加相关列 |
| “在 users 表中添加 phone 列” | `alter table(:users), add :phone` |
| “使 users 表中的 email 列唯一” | `create unique_index(:users, [:email])` |
| “在所有表中添加 tenant_id 列” | 通过 `alter table` 语句添加该列并创建索引 |
| “将 orders 表中的 status 列重命名为 state” | `rename table(:orders), :status, to: :state` |
| “从 users 表中删除 legacy_id 列” | `alter table(:users), remove :legacy_id` |
| “为 orders 表添加检查约束，确保 amount 大于 0” | `create constraint(:orders, ...)` |

### 文件命名规则

文件名遵循以下命名规范：`create_<表名>`, `add_<列名>_to_<表名>`, `create_<表名>_<列名>_index`, `alter_<表名>._add_<列名>`。

## 迁移脚本模板

（此处应提供迁移脚本的模板结构，但原文未提供具体内容，可保留空白或使用占位符）

## 列类型

请参考 [references/column-types.md](references/column-types.md) 以获取完整的类型映射和指导信息。

**关键决策：**
- **ID**：使用 `:binary_id`（UUID）类型，并设置 `primary_key: false`；需要时手动添加 `:id` 列。
- **货币类型**：使用 `:integer`（表示分）或 `:decimal`；避免使用 `:float`。
- **时间戳**：始终使用 `timestamps(type: :utc_datetime_usec)`。
- **枚举类型**：使用 `:string` 与 `Ecto.Enum` 结合；避免使用 PostgreSQL 自带的枚举类型（因为难以迁移）。
- **JSON 数据**：使用 `:map` 类型（映射到 `jsonb` 数据类型）。
- **数组类型**：使用 `{:array, :string}` 等形式。

## 索引策略

请参考 [references/index-patterns.md](references/index-patterns.md) 以获取详细的索引创建指南。

### 何时创建索引？

以下列应始终创建索引：
- 外键列
- `tenant_id` 列（复合索引中的第一个列）
- 在 `WHERE` 子句中使用的列
- 在 `ORDER BY` 子句中使用的列
- 需要唯一性的列

## 索引类型（此处应提供具体的索引类型列表）

## 约束条件

（此处应提供约束条件的详细说明）

## 外键约束

### 外键约束的类型及使用场景

| `on_delete` | 使用场景 |
|-------------|----------|
| `:delete_all` | 子表不能在没有父表的情况下存在（例如成员关系、订单明细） |
| `:nilify_all` | 子表应在父表删除后仍然存在（可选的关联关系） |
| `:nothing` | 由应用程序代码处理（默认行为） |
| `:restrict` | 如果存在子表，则禁止删除父表 |

## 多租户模式

- **所有表都应包含 tenant_id 列**（此处应提供实现逻辑）
- **如何向现有表添加 tenant_id 列**（此处应提供具体操作）

## 数据迁移

**规则：**切勿在同一迁移脚本中同时进行模式变更和数据变更。

### 安全的数据迁移策略

（此处应提供数据迁移的安全性建议）

### 批量数据迁移（针对大型表）

（此处应提供批量迁移的实现方法）

## 可逆迁移与不可逆迁移

- **可逆迁移**：使用 `change` 方法进行操作。例如：
  - `create table` ↔ `drop table`
  - `add column` ↔ `remove column`
  - `create index` ↔ `drop index`
  - `rename` ↔ `rename`

- **不可逆迁移**：需要明确指定操作的方向。例如：
  - 修改列类型时（Ecto 无法自动推断旧类型）
  - 执行原始 SQL 语句
  - 进行数据回填操作
  - 删除包含数据的列

### 使用 `from:` 进行可逆操作

Phoenix 1.7 及更高版本支持使用 `from:` 语法来实现可逆的列类型修改：

（此处应提供具体的使用示例）

## PostgreSQL 扩展功能

（此处应介绍如何使用 PostgreSQL 的扩展功能）

## 枚举类型（建议使用 Ecto.Enum）

优先使用 `:string` 类型与 `Ecto.Enum` 结合。如果必须使用 PostgreSQL 自带的枚举类型，请注意：
- 向 PostgreSQL 枚举中添加新值时，需要执行 `ALTER TYPE ... ADD VALUE` 语句，该操作不能在事务中执行。建议使用 `:string` + `Ecto.Enum` 的组合方式。

## 检查清单：

- 确保主键设置正确（`primary_key: false` + `add :id, :binary_id, primary_key: true`）
- 必需的列应设置为 `null: false`
- 时间戳类型应设置为 `timestamps(type: :utc_datetime_usec)`
- 外键应设置适当的 `on_delete` 约束
- 所有外键列都应创建索引
- 根据需求添加唯一性约束
- 对于需要并发创建索引的情况，应在单独的迁移脚本中使用 `@disable_ddl_transaction true` 选项
- 数据迁移脚本应与模式变更脚本分开保存