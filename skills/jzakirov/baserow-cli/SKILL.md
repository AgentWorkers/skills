---
name: baserow
version: 0.1.0
description: "**Baserow：** 提供创建、读取、更新和删除数据行的功能，同时可以列出表格及其字段信息。适用于用户需要与Baserow进行交互的场景，例如查询数据、创建或更新数据行、检查表格结构，或执行任何与数据库相关的操作。"
metadata:
  openclaw:
    emoji: "🗄️"
    category: "productivity"
    requires:
      bins: ["baserow"]
      env: ["BASEROW_TOKEN", "BASEROW_URL"]
    cliHelp: "baserow --help"
---
# Baserow CLI

Baserow CLI 是用于 [Baserow](https://baserow.io) 的命令行工具，它是一个开源的 Airtable 替代品。默认输出格式为 JSON，可以直接通过 `jq` 进行处理或直接使用。

## 设置

配置文件：`~/.config/baserow-cli/config.toml`。所有配置项都可以通过环境变量（`BASEROW_TOKEN`、`BASEROW_URL`、`BASEROW_TABLE`）或 CLI 参数进行设置。

## 命令查询

不要猜测命令的名称或选项，使用 `--help` 来查看帮助信息：

```bash
baserow --help
baserow rows --help
baserow rows list --help
```

## 快速参考

| 资源          | 关键命令                |
|--------------|----------------------|
| `baserow tables`   | `list`, `get <table-id>`         |
| `baserow fields`   | `list --table <id>`          |
| `baserow rows`    | `list`, `get`, `create`, `update`, `delete`    |
| `baserow rows batch-*` | `batch-create`, `batch-update`, `batch-delete` |
| `baserow config`   | `init`, `show`, `set`            |

## 常见工作流程

**查询表格结构：**
```bash
baserow tables list
baserow tables get 42
baserow fields list --table 42
```

**列出和搜索行：**
```bash
baserow rows list --table 42
baserow rows list --table 42 --search "quarterly" --size 50
baserow rows list --table 42 --filter "Status__equal=Done" --order-by "-Created"
```

**创建行：**
```bash
baserow rows create --table 42 --json '{"Name": "New item", "Status": "Todo"}'
```

**更新行：**
```bash
baserow rows update 1 --table 42 --json '{"Status": "Done"}'
```

**批量操作：**
```bash
baserow rows batch-create --table 42 --json '[{"Name": "A"}, {"Name": "B"}]'
baserow rows batch-update --table 42 --json '[{"id": 1, "Status": "Done"}, {"id": 2, "Status": "Done"}]'
baserow rows batch-delete --table 42 --json '[3, 4, 5]' --yes
```

**从标准输入读取 JSON 数据：**
```bash
cat data.json | baserow rows batch-create --table 42 --json -
```

## 重要约定

- 如果配置了 `defaults.table`，则 `--table` 参数是可选的。
- 如果配置了 `defaults.database`，则 `--database` 参数是可选的。
- 破坏性操作（`delete`、`batch-delete`）在非终端（代理）环境中执行时需要使用 `--yes` 参数。
- `--json` 参数支持使用 `-` 从标准输入读取数据。
- 分页功能通过 `--page` 和 `--size` 参数实现（每页最多 200 条记录）；默认页码为 1。
- 错误信息会以 JSON 格式输出到标准错误流（stderr）：`{"error": {"type": "...", "message": "...", "status_code": N}}`
- 程序退出码：`0` 表示成功，`1` 表示错误，`2` 表示达到速率限制（可以重试）。
- 在使用 `--json` 参数时，字段值应使用字段名（而非字段 ID）。

> [!注意]
> `delete` 和 `batch-delete` 命令具有破坏性操作，请在执行前务必确认用户同意。