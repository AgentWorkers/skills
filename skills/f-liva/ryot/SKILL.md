---
name: ryot
description: 一个功能完备的Ryot媒体追踪工具，具备进度跟踪、评论管理、收藏功能、数据分析、日历支持以及自动生成每日/每周报告的能力。该工具支持对电视节目、电影、书籍和动漫的追踪，并实现了与GraphQL API的全面集成。
metadata:
  credentials:
    required:
      - name: RYOT_CONFIG
        description: Config file at /home/node/clawd/config/ryot.json with "url" (Ryot instance URL) and "api_token" (API authentication token)
        path: /home/node/clawd/config/ryot.json
        format: |
          {
            "url": "https://your-ryot-instance.com",
            "api_token": "your_api_token_here"
          }
---
# Ryot Media Tracker - 全功能套件

Ryot 的完整集成方案，支持进度跟踪、评论、收藏、数据分析、日历管理以及自动化报告功能。

## 设置（必需）

在使用此功能之前，您需要配置您的 Ryot 实例：

1. 在 `/home/node/clawd/config/ryot.json` 文件中创建配置文件：

```json
{
  "url": "https://your-ryot-instance.com",
  "api_token": "your_api_token_here"
}
```

2. 设置您的 Ryot 实例 URL —— 请将 `https://your-ryot-instance.com` 替换为您实际的 Ryot 服务器地址。
3. 从 Ryot 实例设置中获取 API 令牌。
4. 保存配置文件 —— 该功能会自动读取此文件。

## 使用方法

使用 `scripts/ryot_api.py` 脚本来执行所有与 Ryot 相关的操作。

## 🚀 快速启动 —— 自动化设置

```bash
cd /home/node/clawd/skills/ryot/scripts
./setup-automation.sh
```

这将完成以下操作：
- ✅ 设置每日即将发布的剧集通知（07:30）
- ✅ 设置每周统计报告（周一 08:00）
- ✅ 设置每日活动汇总（20:00）
- ✅ 配置 WhatsApp 通知功能

## 常见任务

### 1. 进度跟踪 📊

```bash
# Check your progress on a TV show
python3 scripts/ryot_api.py progress met_XXXXX

# Example output:
# Galaxy Express 999
# Season 1, Episode 35/113 (30%)
```

### 2. 评论与评分 ⭐

```bash
# Add review with rating (0-100)
python3 scripts/ryot_reviews.py add met_XXXXX 85 "Amazing show!"

# Rating only
python3 scripts/ryot_reviews.py add met_XXXXX 90
```

### 3. 收藏 📚

```bash
# List your collections
python3 scripts/ryot_collections.py list

# Create new collection
python3 scripts/ryot_collections.py create "Top Anime 2026" "My favorite anime of the year"

# Add media to collection
python3 scripts/ryot_collections.py add <collection_id> met_XXXXX
```

### 4. 数据分析与统计 📈

```bash
# View your statistics
python3 scripts/ryot_stats.py analytics
# Output: Total media, shows, movies, watch time

# Recently consumed
python3 scripts/ryot_stats.py recent
# Output: Last 10 media you watched/read
```

### 5. 日历与即将发布的剧集 📅

```bash
# Upcoming episodes this week
python3 scripts/ryot_calendar.py upcoming

# Calendar for next 30 days
python3 scripts/ryot_calendar.py calendar 30
```

### 6. 搜索与详情 🔍

```bash
# Search for TV shows
python3 scripts/ryot_api.py search "The Wire" --type SHOW

# Search for movies
python3 scripts/ryot_api.py search "Inception" --type MOVIE

# Get details
python3 scripts/ryot_api.py details met_XXXXX
```

### 7. 标记为已完成 ✅

```bash
# Mark media as completed
python3 scripts/ryot_api.py complete met_XXXXX
```

## 工作流程

1. **用户请求**：“我观看了多少集《Galaxy Express 999》？”
2. **搜索**：找到正确的元数据 ID。
3. **检查进度**：运行 `python3 scripts/ryot_api.py progress met_XXX`。
4. **标记为已完成**：观看完成后，批量更新进度状态。

## 支持的媒体类型

支持的 `lot` 值：
- `SHOW` —— 电视剧
- `MOVIE` —— 电影
- `BOOK` —— 书籍
- `ANIME` —— 动画系列
- `GAME` —— 视频游戏

## 重要说明

- **首次使用前**：请检查 `/home/node/clawd/config/ryot.json` 文件是否存在。如果不存在，请询问用户他们的 Ryot 实例 URL 和 API 令牌，然后创建配置文件。
- 始终先进行搜索以获取正确的元数据 ID。
- 如果有多个结果与剧集名称匹配，请核实年份信息。
- API 使用 `/backendgraphql` 提供 GraphQL 接口。
- 元数据 ID 以 `met_` 开头。

## 资源

### scripts/ryot_api.py

用于执行 Ryot GraphQL 操作的 Python 脚本。支持以下功能：
- `search`：按标题搜索媒体内容
- `details`：获取元数据详情
- `complete`：将媒体内容标记为已完成