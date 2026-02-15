---
name: miniflux
description: >
  **管理 Miniflux——通过 REST API 进行的现代极简主义信息源阅读器**  
  功能包括：  
  - 列出所有信息源及其文章  
  - 创建/取消订阅  
  - 搜索文章  
  - 管理分类  
  - 标记文章为已读/未读
---
# Miniflux 技能

通过 REST API 管理 Miniflux——这款现代的极简主义新闻阅读器。

该技能支持以下功能：列出新闻源和文章、创建/删除订阅、搜索文章、管理分类以及将文章标记为已读/未读。

## 设置

使用该技能需要 Python 以及 Miniflux 的 Python 客户端。

```bash
# Install the miniflux Python package
uv pip install miniflux
```

## 配置

请设置以下环境变量：

```bash
export MINIFLUX_URL="https://reader.etereo.cloud"
export MINIFLUX_TOKEN="your-api-token-here"
```

获取 API 密钥的步骤：
1. 登录到您的 Miniflux 实例。
2. 转到“设置”>“API 密钥”。
3. 点击“创建新的 API 密钥”。
4. 复制密钥，并将其设置为 `MINIFLUX_TOKEN`。

## 使用方法

### 命令行接口（CLI）

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
| `feeds` | 列出所有新闻源 |
| `categories` | 列出所有分类 |
| `entries` | 根据条件（状态、搜索内容、数量限制等）列出文章 |
| `entry` | 通过 ID 获取特定文章 |
| `create-feed` | 创建新的新闻源订阅 |
| `update-feed` | 更新现有新闻源 |
| `delete-feed` | 删除新闻源 |
| `refresh-all` | 刷新所有新闻源 |
| `refresh-feed` | 刷新特定新闻源 |
| `mark-read` | 将特定文章标记为已读 |
| `mark-unread` | 将特定文章标记为未读 |
| `mark-feed-read` | 将新闻源中的所有文章标记为已读 |
| `discover` | 从指定 URL 发现订阅源 |
| `counters` | 获取每个新闻源的未读/已读文章数量 |
| `me` | 获取当前用户信息 |
| `create-category` | 创建新的分类 |
| `delete-category` | 删除分类 |

## 文章过滤条件

使用 `entries` 命令时，可以通过以下参数进行过滤：
- `--status`：文章状态（未读、已读或已删除）
- `--limit`：返回的文章数量（默认：100）
- `--offset`：跳过的文章数量
- `--direction`：排序方向（升序或降序）
- `--search`：搜索查询字符串
- `--category-id`：按分类 ID 过滤
- `--feed-id`：按新闻源 ID 过滤
- `--starred`：过滤星标文章（true/false）
- `--before`：指定时间之前的文章的 Unix 时间戳
- `--after`：指定时间之后的文章的 Unix 时间戳

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

- `/v1/feeds` - 列出所有新闻源
- `/v1/feeds/{id}` - 获取新闻源详情
- `/v1/feeds/{id}/entries` - 获取新闻源中的文章
- `/v1/feeds/{id}/refresh` - 刷新新闻源
- `/v1/feeds/{id}/mark-all-as-read` - 将新闻源中的所有文章标记为已读
- `/v1/categories` - 列出所有分类
- `/v1/categories/{id}/entries` | 获取分类中的文章
- `/v1/entries` - 列出所有文章
- `/v1/entries/{id}` | 获取特定文章
- `/v1/entries/{id}/bookmark` | 切换文章的书签状态
- `/v1/feeds/refresh` | 刷新所有新闻源
- `/v1/discover` | 从指定 URL 发现订阅源
- `/v1/feeds/counters` | 获取每个新闻源的未读/已读文章数量
- `/v1/me` | 获取当前用户信息

## 错误处理

如果发生 API 错误，脚本将退出并显示来自 Miniflux 的错误信息（错误代码为 1）。

## 依赖项

- Python 3.8 及以上版本
- Miniflux Python 客户端（使用 `uv pip install miniflux` 安装）

## 文档

完整的 API 文档：https://miniflux.app/docs/api.html