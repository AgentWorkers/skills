---
name: notion
description: 通过官方的 Notion API，您可以与 Notion 的页面和数据库进行交互。
homepage: https://developers.notion.com
metadata:
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - NOTION_API_KEY
    install:
      - id: node
        kind: note
        label: "Requires notion-cli (Node.js) or notion-cli-py (Python). See docs below."
---

# Notion

此技能允许代理通过官方的 Notion API 来操作 **Notion 页面和数据库**。

该技能采用声明式设计，明确了 **安全、推荐的操作方式**，并假设存在一个本地的 CLI 工具（`notion-cli`）来实际执行 API 调用。

## 认证

- 在 https://www.notion.so/my-integrations 创建一个 Notion 集成。
- 复制内部集成令牌（Internal Integration Token）。
- 将其保存为：

```bash
export NOTION_API_KEY=secret_xxx
```

将此集成共享给您想要访问的页面或数据库。未共享的内容对 API 是不可见的。

## 个人/工作配置文件（Profiles）

您可以通过环境变量（env）或配置文件（config）来定义多个配置文件（例如个人配置文件和工作配置文件）。
默认配置文件：个人配置文件。

如需更改默认配置文件，请使用以下方式：

```bash
export NOTION_PROFILE=work
```

## 页面（Pages）

**读取页面内容：**

```bash
notion-cli page get <page_id>
```

**添加新内容块：**

```bash
notion-cli block append <page_id> --markdown "..."
```

建议使用添加新内容块的方式，而不是直接修改现有内容。

**创建新页面：**

```bash
notion-cli page create --parent <page_id> --title "..."
```

## 数据库（Databases）

**检查数据库结构：**

```bash
notion-cli db get <database_id>
```

**查询数据库数据：**

```bash
notion-cli db query <database_id> --filter <json> --sort <json>
```

**创建新记录：**

```bash
notion-cli page create --database <database_id> --props <json>
```

**更新记录：**

```bash
notion-cli page update <page_id> --props <json>
```

## 数据库结构变更（高级操作）

在应用任何数据库结构变更之前，请务必检查变更内容（diffs）。

未经明确确认，切勿直接修改数据库结构。

**推荐的操作流程：**

```bash
notion-cli db schema diff <database_id> --desired <json>
notion-cli db schema apply <database_id> --desired <json>
```

## 安全注意事项**

- Notion API 有速率限制，请谨慎批量操作。
- 建议使用添加新内容或更新数据的操作方式，避免进行破坏性操作。
- Notion 的记录 ID 是不可见的；请明确存储这些 ID，不要从 URL 中推断出来。