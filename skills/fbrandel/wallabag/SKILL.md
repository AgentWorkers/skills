---
name: wallabag
description: 通过 Wallabag 开发者 API（使用 OAuth2 认证）来管理 Wallabag 的书签，包括创建、读取、更新、删除、搜索以及标签管理等功能。当用户需要与 Wallabag 进行交互、存储链接、检索条目、根据搜索条件或标签进行过滤，或修改书签元数据时，可以使用这些功能。
---
# Wallabag

## 概述

使用此技能可以通过其API以及确定的shell命令来操作Wallabag实例。请将凭据保存在环境变量中，切勿将敏感信息硬编码到代码中。

## 运行时要求

- 必需的二进制文件：`bash`, `curl`
- `tag add` 和 `tag remove` 命令需要 `jq`。

## 所需环境变量

在运行命令之前，请设置以下环境变量：

- `WALLABAG_BASE_URL`
- `WALLABAG_CLIENT_ID`
- `WALLABAG_CLIENT_SECRET`
- `WALLABAG_USERNAME`
- `WALLABAG_PASSWORD`

示例：

```bash
export WALLABAG_BASE_URL="https://wallabag.example.com"
export WALLABAG_CLIENT_ID="..."
export WALLABAG_CLIENT_SECRET="..."
export WALLABAG_USERNAME="..."
export WALLABAG_PASSWORD="..."
```

## 命令接口

**主要命令：**

```bash
scripts/wallabag.sh <subcommand> [options]
```

**子命令：**

- `auth [--show-token]`
- `list [--search <text>] [--tag <name>] [--archive 0|1] [--starred 0|1] [--page <n>] [--per-page <n>]`
- `get --id <entry_id>`
- `create --url <url> [--title <title>] [--tags "tag1,tag2"]`
- `update --id <entry_id> [--title <title>] [--tags "tag1,tag2"] [--archive 0|1] [--starred 0|1]`
- `delete --id <entry_id>`
- `tag add --id <entry_id> --tags "tag1,tag2"`
- `tag remove --id <entry_id> --tag "tag"`

## 工作流程**

1. 运行 `auth` 命令以验证OAuth凭据。
2. 使用 `create` 命令添加书签。
3. 使用 `list` 和 `get` 命令检索书签。
4. 使用 `update` 或 `tag` 命令修改元数据。
5. 仅在需要删除书签时使用 `delete` 命令。

## 操作规则

- 令牌仅保留在进程内存中，不要将其状态持久化到磁盘上。
- 除非明确指定了 `--show-token` 参数，否则 `auth` 命令不会打印访问令牌。
- 尽可能返回原始的JSON格式输出。
- 在标准错误输出（stderr）中显示可操作的错误信息，并返回非零的退出码。
- 当仅需要修改标签时，优先使用 `tag add` 和 `tag remove` 命令。

## 示例命令提示：

- “使用 $wallabag 将 https://example.com 保存为带有 ‘ai,read-later’ 标签的书签”
- “使用 $wallabag 列出标记为 ‘tech’ 的星标条目”
- “使用 $wallabag 从条目 123 中删除 ‘inbox’ 标签”

## 参考资料

如需了解API的详细信息，请参阅 `references/wallabag-api.md` 文件。