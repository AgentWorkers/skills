---
name: notion-api
description: 通用概念API命令行界面（Node.js）：用于搜索数据源（数据库）、查询数据以及创建页面。配置方式是通过设置`NOTION_KEY`（或`~/.config/notion/api_key`）。
---

# notion-api（通用）

该工具提供了一个基于 Node.js 的命令行界面（CLI），用于与 Notion API 进行交互。它被设计为可共享的：**仓库中不包含硬编码的数据库 ID 或任何敏感信息**。

## 认证

可以通过以下方式提供 Notion 集成令牌：

- 使用环境变量 `NOTION_KEY`；
- 或者从文件 `~/.config/notion/api_key` 中读取（文件的第一行）。

同时，请确保目标页面/数据库已在 Notion 中设置为可共享状态。

## 命令（CLI）

使用以下命令运行该工具：

- `node scripts/notion-api.mjs <command> ...`

### 搜索

```bash
node scripts/notion-api.mjs search "query" --page-size 10
```

### 查询数据源（数据库查询）

```bash
node scripts/notion-api.mjs query --data-source-id <DATA_SOURCE_ID> --page-size 10
# optionally pass raw JSON body:
node scripts/notion-api.mjs query --data-source-id <ID> --body '{"filter": {...}, "sorts": [...], "page_size": 10}'
```

### 在数据库中创建页面

```bash
node scripts/notion-api.mjs create-page --database-id <DATABASE_ID> --title "My item" --title-prop Name
```

## 输出

所有命令都会将结果以 JSON 格式输出到标准输出（stdout）。

## 注意事项：

- Notion API 的版本信息默认为 `2025-09-03`；可以通过设置 `NOTION_VERSION` 变量来覆盖这一默认值。
- 该工具受到速率限制，请尽量使用 `page_size` 参数来减少请求次数，并避免频繁调用 API。