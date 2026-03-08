---
name: baserow-cli
version: 0.1.0
description: "**Baserow：**  
用于创建、读取、更新和删除数据行，以及列出表格和字段。适用于用户需要与 Baserow 进行交互的场景——例如查询数据、创建或更新数据行、检查表格结构，或执行任何数据库相关操作。"
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

Baserow CLI 是用于 [Baserow](https://baserow.io) 的命令行工具，它是一款开源的 Airtable 替代品。默认输出格式为 JSON，可以直接通过管道传输给 `jq` 进行处理，或者直接使用。

## 设置

配置文件：`~/.config/baserow-cli/config.toml`。所有配置项都可以通过环境变量（`BASEROW_TOKEN`、`BASEROW_URL`、`BASEROW_TABLE`）或 CLI 参数来设置。

## 命令查询

不要猜测命令的名称或选项，使用 `--help` 来获取帮助信息：

```bash
baserow --help
baserow rows --help
baserow rows list --help
```

## 快速参考

| 功能 | 关键命令 |
|---------|---------|
| 查看表格结构 | `baserow tables` |
| 获取表格信息 | `baserow fields --table <table-id>` |
| 查看/创建/更新/删除表格行 | `baserow rows list`, `baserow rows get`, `baserow rows create`, `baserow rows update`, `baserow rows delete` |
| 批量操作表格行 | `baserow rows batch-create`, `baserow rows batch-update`, `baserow rows batch-delete` |
| 配置 Baserow | `baserow config init`, `baserow config show`, `baserow config set` |

## 常见工作流程

- **查看表格结构：**  
  ```bash
baserow tables list
baserow tables get 42
baserow fields list --table 42
```

- **列出和搜索表格行：**  
  ```bash
baserow rows list --table 42
baserow rows list --table 42 --search "quarterly" --size 50
baserow rows list --table 42 --filter "Status__equal=Done" --order-by "-Created"
```

- **创建新表格行：**  
  ```bash
baserow rows create --table 42 --json '{"Name": "New item", "Status": "Todo"}'
```

- **更新表格行：**  
  ```bash
baserow rows update 1 --table 42 --json '{"Status": "Done"}'
```

- **批量操作：**  
  ```bash
baserow rows batch-create --table 42 --json '[{"Name": "A"}, {"Name": "B"}]'
baserow rows batch-update --table 42 --json '[{"id": 1, "Status": "Done"}, {"id": 2, "Status": "Done"}]'
baserow rows batch-delete --table 42 --json '[3, 4, 5]' --yes
```

- **从标准输入读取 JSON 数据：**  
  ```bash
cat data.json | baserow rows batch-create --table 42 --json -
```

## 重要约定

- 如果配置了 `defaults.table`，则 `--table` 参数是可选的。
- 如果配置了 `defaults.database`，则 `--database` 参数是可选的。
- 破坏性命令（`delete`、`batch-delete`）在非终端（agent）环境中执行时需要使用 `--yes` 选项。
- `--json` 参数支持使用 `-` 从标准输入（stdin）读取数据。
- 分页功能通过 `--page` 和 `--size` 参数实现（每页最多 200 条记录）；默认页码为 1。
- 错误信息会以 JSON 格式输出到标准错误流（stderr）：`{"error": {"type": "...", "message": "...", "status_code": N}`。
- 程序退出代码：`0` 表示成功，`1` 表示错误，`2` 表示遇到速率限制（可尝试重试）。
- 在使用 `--json` 参数时，字段值应使用字段名称（而非字段 ID）。

> [!注意]
> `delete` 和 `batch-delete` 命令具有破坏性操作，请在执行前务必确认用户同意。