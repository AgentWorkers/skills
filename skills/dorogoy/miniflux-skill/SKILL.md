---
name: miniflux
description: >
  **管理 Miniflux——通过 REST API 进行的现代极简主义新闻阅读器功能**  
  - 支持列出新闻源和文章；  
  - 允许创建/取消订阅；  
  - 提供文章搜索功能；  
  - 可以管理新闻分类；  
  - 能够将文章标记为已读/未读。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"], "env": ["MINIFLUX_URL", "MINIFLUX_TOKEN"] },
        "primaryEnv": "MINIFLUX_TOKEN"
      }
  }
---
# Miniflux 技能

通过 REST API 管理 Miniflux——一个现代的、简约的 Feed 阅读器。

该技能可用于列出 Feed 和条目、创建/删除订阅、搜索文章、管理分类以及将条目标记为已读/未读。

## 设置

使用此技能需要 Python 和 Miniflux Python 客户端。

```bash
# Install the miniflux Python package
uv pip install miniflux
```

## 配置

设置以下环境变量：

```bash
export MINIFLUX_URL="https://your-miniflux-instance.com"
export MINIFLUX_TOKEN="your-api-token-here"
```

获取 API 密钥的步骤：
1. 登录到您的 Miniflux 实例。
2. 转到“设置”>“API 密钥”。
3. 点击“创建新的 API 密钥”。
4. 复制密钥，并将其设置为 `MINIFLUX_TOKEN`。

## 使用方法

### CLI 包装器

```bash
# List all feeds
bash miniflux.sh feeds

# List categories
bash miniflux.sh categories

# Get unread entries
bash miniflux.sh entries --status unread

# Search entries
bash miniflux.sh entries --search "kubernetes"

# Create a new feed
bash miniflux.sh create-feed --url "https://example.com/feed.xml" --category 1

# Refresh all feeds
bash miniflux.sh refresh-all

# Mark entries as read
bash miniflux.sh mark-read --entry-ids 123,456

# Mark feed as read
bash miniflux.sh mark-feed-read --feed-id 42

# Toggle bookmark/star
bash miniflux.sh toggle-bookmark --entry-id 123

# Discover subscriptions from a website
bash miniflux.sh discover --url "https://example.org"

# Delete a feed
bash miniflux.sh delete-feed --feed-id 42

# Get feed details
bash miniflux.sh feed --feed-id 42

# Get counters (unread/read)
bash miniflux.sh counters

# Get current user info
bash miniflux.sh me

# Get specific entry
bash miniflux.sh entry --entry-id 123

# Create category
bash miniflux.sh create-category --title "Tech News"

# Delete category
bash miniflux.sh delete-category --category-id 5

# Update feed
bash miniflux.sh update-feed --feed-id 42 --title "New Title" --category-id 3
```

## 命令参考

| 命令 | 描述 |
|---------|-------------|
| `feeds` | 列出所有 Feed |
| `categories` | 列出所有分类 |
| `entries` | 根据条件（状态、搜索、限制等）列出条目 |
| `entry` | 通过 ID 获取特定条目 |
| `create-feed` | 创建新的 Feed 订阅 |
| `update-feed` | 更新现有 Feed |
| `delete-feed` | 删除 Feed |
| `refresh-all` | 刷新所有 Feed |
| `refresh-feed` | 刷新特定 Feed |
| `mark-read` | 将特定条目标记为已读 |
| `mark-unread` | 将特定条目标记为未读 |
| `mark-feed-read` | 将 Feed 的所有条目标记为已读 |
| `toggle-bookmark` | 切换条目的书签/星标状态 |
| `discover` | 从 URL 发现订阅 |
| `counters` | 获取每个 Feed 的未读/已读计数 |
| `me` | 获取当前用户信息 |
| `create-category` | 创建新的分类 |
| `delete-category` | 删除分类 |

## 条目的过滤条件

使用 `entries` 命令时，您可以按以下条件进行过滤：

- `--status`：条目状态（未读、已读或已删除）
- `--limit`：返回的条目数量（默认：100）
- `--offset`：跳过的条目数量
- `--direction`：排序方向（升序或降序）
- `--search`：搜索查询字符串
- `--category-id`：按分类 ID 过滤
- `--feed-id`：按 Feed ID 过滤
- `--starred`：过滤星标条目（true/false）
- `--before`：此时间之前的 Unix 时间戳
- `--after`：此时间之后的 Unix 时间戳

## 示例

```bash
# Get last 10 unread entries
bash miniflux.sh entries --status unread --limit 10

# Search for Kubernetes articles
bash miniflux.sh entries --search "kubernetes" --limit 20

# Get entries from a specific feed
bash miniflux.sh entries --feed-id 42 --limit 15

# Get starred entries
bash miniflux.sh entries --starred true

# Create a feed with crawler enabled
bash miniflux.sh create-feed --url "https://techcrunch.com/feed/" --category 1 --crawler true

# Discover feeds from a blog
bash miniflux.sh discover --url "https://example.com"
```

## 支持的 API 端点

- `/v1/feeds` - 列出 Feed
- `/v1/feeds/{id}` - 获取 Feed 详情
- `/v1/feeds/{id}/entries` - 获取 Feed 条目
- `/v1/feeds/{id}/refresh` - 刷新 Feed
- `/v1/feeds/{id}/mark-all-as-read` - 将 Feed 条目标记为已读
- `/v1/categories` - 列出分类
- `/v1/categories/{id}/entries` - 获取分类条目
- `/v1/entries` - 列出条目
- `/v1/entries/{id}` - 获取特定条目
- `/v1/entries/{id}/bookmark` - 切换条目的书签状态
- `/v1/feeds/refresh` - 刷新所有 Feed
- `/v1/discover` - 发现订阅
- `/v1/feeds/counters` - 获取计数信息
- `/v1/me` - 当前用户信息

## 错误处理

如果发生 API 错误，脚本将以错误代码 1 退出，并显示来自 Miniflux 的错误消息。

## 依赖项

- Python 3.8+
- Miniflux Python 客户端（`uv pip install miniflux`）

## 文档

完整的 API 文档：https://miniflux.app/docs/api.html