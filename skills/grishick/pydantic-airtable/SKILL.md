---
name: pydantic-airtable-api
description: 通过 `pydantic-airtable` Python 库来管理 Airtable 表格和记录。该库可用于创建、列出、更新、删除或检查 Airtable 记录或表格；将 Pydantic 模型同步到 Airtable；验证数据结构是否符合模型要求；以及编写使用 `AirtableModel`、`AirtableManager` 或 `AirtableClient` 的 Python 代码。
metadata:
  openclaw:
    requires:
      bins: [python3]
      env:
        - AIRTABLE_ACCESS_TOKEN
        - AIRTABLE_BASE_ID
    install:
      - id: pydantic-airtable
        kind: pip
        package: pydantic-airtable
        label: Install pydantic-airtable
---
# Pydantic Airtable API

使用此技能通过 `pydantic-airtable` 来进行实际的 Airtable 管理操作。

请确保 `SKILL.md` 文件主要关注工作流程的相关内容。仅在需要明确的方法名称或签名时，才参考 `references/api-surface.md`。

## 设置

如果需要，请安装相关库：

```bash
pip install pydantic-airtable
```

通过环境变量提供凭据：

```bash
export AIRTABLE_ACCESS_TOKEN="pat..."
export AIRTABLE_BASE_ID="app..."
```

大多数捆绑的脚本也支持 `--table` 和可选的 `--base-id` 参数。

## 安全注意事项

- 使用权限最小的 **Airtable 令牌**。
- 在将脚本应用于生产数据之前，建议先在测试环境中进行测试。
- 命令 `scripts/model_ops.py --module ./path.py` 会导入并执行指定的 Python 模块。请仅在与可信的本地代码一起使用时使用该命令。
- `--fields`、`--records` 和 `--updates` 参数支持 `@file.json` 格式的输入，该参数用于读取磁盘上的 JSON 文件。在传递这些文件之前，请先检查其内容。
- 安装 `pydantic-airtable` 是使用此技能的常规操作，但如果您希望实现更严格的隔离，请使用虚拟环境（virtualenv）或容器。

## 选择合适的工具

- 使用 `AirtableManager` 进行基础操作、表操作、模式操作以及直接记录操作。
- 使用 `AirtableClient` 进行低级别的记录 API 操作和批量记录操作。
- 当用户需要使用具有 CRUD 功能的 Pydantic 模型时，使用 `AirtableModel`。

有关具体方法的详细信息，请参阅 `references/api-surface.md`。

## 默认工作流程

1. 确保凭据已正确设置。
2. 对于一次性操作任务，优先使用 `scripts/` 目录下的脚本。
3. 对于可重用的应用程序代码，优先使用 `AirtableModel` 或 `AirtableManager` 提供的代码片段。
4. 在写入大量数据之前，先验证或同步数据结构。
5. 在执行网络操作时，要捕获 Airtable 特定的异常。

## 捆绑的脚本

### `scripts/manage_records.py`

用于执行记录的 CRUD 操作，无需重复编写配置代码。

支持的操作：
- `list`（列出记录）
- `get`（获取记录）
- `create`（创建记录）
- `update`（更新记录）
- `delete`（删除记录）
- `batch-create`（批量创建记录）
- `batch-update`（批量更新记录）

示例：

```bash
python scripts/manage_records.py list --table Tasks --max-records 10
python scripts/manage_records.py get --table Tasks --record-id rec123
python scripts/manage_records.py create --table Tasks --fields '{"Name":"Ship it","Status":"Open"}'
python scripts/manage_records.py update --table Tasks --record-id rec123 --fields '{"Status":"Done"}'
python scripts/manage_records.py delete --table Tasks --record-id rec123
python scripts/manage_records.py batch-create --table Tasks --records '[{"Name":"A"},{"Name":"B"}]'
```

### `scripts/manage_tables.py`

用于执行表和模式相关的操作。

支持的操作：
- `list-bases`（列出所有表）
- `base-schema`（获取表结构）
- `table-schema`（获取表结构）
- `create-table`（创建表）
- `update-table`（更新表）
- `delete-table`（删除表）

示例：

```bash
python scripts/manage_tables.py list-bases
python scripts/manage_tables.py base-schema
python scripts/manage_tables.py table-schema --table Tasks
python scripts/manage_tables.py create-table --name Tasks --fields '[{"name":"Name","type":"singleLineText"}]'
python scripts/manage_tables.py update-table --table-id tbl123 --updates '{"name":"Tasks Archive"}'
python scripts/manage_tables.py delete-table --table-id tbl123
```

### `scripts/model_ops.py`

当任务需要基于模型进行操作时使用。

支持的操作：
- `create-table-from-model`（根据模型创建表）
- `sync-model`（同步模型）
- `validate-model`（验证模型）

模型文件中必须包含一个按名称命名的类。

示例：

```bash
python scripts/model_ops.py validate-model --module ./task_model.py --class-name Task
python scripts/model_ops.py sync-model --module ./task_model.py --class-name Task --create-missing-fields
```

## 实用指南

- 对于表的创建、模式检查以及跨多个表的记录 CRUD 操作，优先使用 `AirtableManager`。
- 当用户需要直接列出记录或批量写入单个配置好的表时，优先使用 `AirtableClient`。
- 当任务需要保持类型安全并在应用程序代码中可重用时，优先使用 `AirtableModel`。
- 如果用户要求“管理 Airtable”但没有指定具体的代码输出，建议先使用脚本。
- 如果字段的数据量较大或重复性较高，可以将数据写入 JSON 文件，并通过 `@file.json` 参数将其传递给支持 JSON 输入的脚本。

## 脚本的 JSON 输入规则

对于 `--fields`、`--records` 和 `--updates` 参数：
- 可以直接传递 JSON 字符串（例如：`{"Name":"Task"}`）；
- 或者通过 `@path/to/file.json` 参数从磁盘加载 JSON 文件。

## 异常处理

- 当出现以下情况时，捕获并显示相应的异常：
- `ConfigurationError`：表示凭据或配置缺失。
- `RecordNotFoundError`：表示记录不存在。
- `APIError`：表示 Airtable API 出错。
- `ValidationError`：表示模型或模式不匹配。
- `AirtableError`：作为最后的异常处理方式。