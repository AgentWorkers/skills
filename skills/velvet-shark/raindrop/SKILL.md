---
name: raindrop
description: 通过 CLI（命令行界面）搜索、列出和管理 Raindrop.io 的书签。适用于用户需要查找已保存的链接、浏览书签集合、添加新书签、使用标签对书签进行分类、在书签集合之间移动书签，或操作他们的 Raindrop 图书库的场景。支持读写操作，包括搜索、列出、获取书签信息、添加/删除书签、移动书签、更新书签信息以及批量处理书签。
metadata: {"clawdbot":{"emoji":"🌧️","homepage":"https://raindrop.io","requires":{"bins":["bash","curl","jq","bc"]}}}
---

# Raindrop.io 书签功能

通过 Raindrop.io API 管理书签。

## 设置

```bash
# Get token from: https://app.raindrop.io/settings/integrations → "Create test token"
echo 'RAINDROP_TOKEN="your-token"' > ~/.config/raindrop.env
```

## 快速入门

```bash
# Search bookmarks
{baseDir}/scripts/raindrop.sh search "AI tools"

# List unsorted bookmarks
{baseDir}/scripts/raindrop.sh list -1 --limit 50

# Count unsorted
{baseDir}/scripts/raindrop.sh count -1

# Create collection and move bookmarks
{baseDir}/scripts/raindrop.sh create-collection "AI Coding"
{baseDir}/scripts/raindrop.sh move 12345 66016720

# Bulk move (efficient!)
{baseDir}/scripts/raindrop.sh bulk-move "123,456,789" 66016720
```

## 命令

### 阅读书签

| 命令 | 描述 |
|---------|-------------|
| `whoami` | 显示已认证的用户 |
| `collections` | 列出所有书签集合及其 ID |
| `list [ID]` | 列出指定 ID 的书签（默认：0 = 所有书签） |
| `count [ID]` | 统计指定集合中的书签数量 |
| `search QUERY [ID]` | 搜索书签 |
| `get ID` | 获取书签详细信息 |
| `tags` | 列出所有书签及其标签数量 |
| `list-untagged [ID]` | 查找没有标签的书签 |
| `cache ID` | 获取书签的永久副本（仅限专业版用户） |

### 添加书签

| 命令 | 描述 |
|---------|-------------|
| `add URL [ID]` | 添加书签（默认：-1 = 未分类） |
| `delete ID` | 删除书签 |
| `create-collection NAME` | 创建新的书签集合 |
| `move ID COLLECTION` | 将书签移动到指定集合 |
| `update ID [opts]` | 更新书签的标签、标题或所属集合 |
| `bulk-move IDS TARGET [SOURCE]` | 批量移动书签（源集合默认为 -1/未分类） |
| `suggest URL` | 获取 AI 建议的标签或标题 |

### 选项

| 标志 | 描述 |
|------|-------------|
| `--json` | 以原始 JSON 格式输出结果 |
| `--limit N` | 限制返回结果的数量（默认：25） |
| `--page N` | 分页显示结果（索引从 0 开始） |
| `--delay MS` | 控制 API 调用之间的延迟时间（用于限制请求频率） |
| `--token TOKEN` | 使用自定义 API 令牌 |

### 更新书签

对于 `update` 命令，可使用的选项包括：

| 标志 | 描述 |
|------|-------------|
| `--tags TAG1,TAG2` | 设置书签标签（用逗号分隔） |
| `--title TITLE` | 设置书签标题 |
| `--collection ID` | 将书签移动到指定集合 |

### 书签集合 ID

- `0` = 所有书签 |
- `-1` = 未分类的书签 |
- `-99` = 收藏夹中的书签 |
- `N` = 指定书签集合（ID 可通过 `collections` 命令获取）

## 示例

```bash
# List unsorted with pagination
{baseDir}/scripts/raindrop.sh list -1 --limit 50 --page 0
{baseDir}/scripts/raindrop.sh list -1 --limit 50 --page 1

# Create collection
{baseDir}/scripts/raindrop.sh create-collection "AI Coding"
# Output: Created: AI Coding / ID: 66016720

# Move single bookmark
{baseDir}/scripts/raindrop.sh move 1234567 66016720

# Update bookmark with tags and move
{baseDir}/scripts/raindrop.sh update 1234567 --tags "claude-code,workflow,tips" --collection 66016720

# Bulk move with rate limiting (100ms between calls)
{baseDir}/scripts/raindrop.sh bulk-move "123,456,789,101112" 66016720 --delay 100

# Find untagged bookmarks in unsorted
{baseDir}/scripts/raindrop.sh list-untagged -1 --limit 100

# Get JSON for scripting
{baseDir}/scripts/raindrop.sh list -1 --json --limit 50 | jq '.items[]._id'

# Count unsorted bookmarks
{baseDir}/scripts/raindrop.sh count -1
```

## 批量操作

对于大量书签的操作，建议使用 `bulk-move` 命令（该命令通过 Raindrop 的批量 API 进行处理，每次请求最多支持 100 个操作）：

```bash
# Get IDs from unsorted
ids=$({baseDir}/scripts/raindrop.sh list -1 --json --limit 100 | jq -r '[.items[]._id] | join(",")')

# Move all to collection
{baseDir}/scripts/raindrop.sh bulk-move "$ids" 66016720
```

## 请求频率限制

Raindrop API 有请求频率限制。对于批量操作，请遵循以下规则：

1. 使用 `--delay 100` 选项设置每次调用之间的延迟时间（例如 100 毫秒）。
2. 尽量使用 `bulk-move` 而不是单独的 `move` 命令。
3. 每次操作批量处理 50 到 100 个书签。

## 直接使用 API

对于未在上述命令中涵盖的操作，可以直接使用 Raindrop 的 API 进行处理。

API 文档：https://developer.raindrop.io/