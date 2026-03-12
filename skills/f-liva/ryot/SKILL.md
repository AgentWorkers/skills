---
name: ryot
description: 一个功能完备的Ryot媒体追踪工具，具备进度跟踪、评论功能、收藏系统、数据分析、日历支持以及自动生成的每日/每周报告。该工具支持对电视节目、电影、书籍和动漫的追踪，并实现了与GraphQL API的全面集成。
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

这是一个集成了进度跟踪、评论、收藏、分析、日历和自动报告功能的完整Ryot集成解决方案。

## 设置（必需）

在使用此功能之前，您必须配置您的Ryot实例：

1. 在 `/home/node/clawd/config/ryot.json` 文件中创建配置文件：

```json
{
  "url": "https://your-ryot-instance.com",
  "api_token": "your_api_token_here"
}
```

2. 设置您的Ryot实例URL——请将 `https://your-ryot-instance.com` 替换为您实际的Ryot服务器地址。
3. 从Ryot实例设置中获取您的API令牌。
4. 保存配置文件——该功能会自动读取此文件。

## 使用方法

使用 `scripts/ryot_api.py` 执行所有与Ryot相关的操作。

## 🚀 快速入门 - 自动化设置

```bash
cd /home/node/clawd/skills/ryot/scripts
./setup-automation.sh
```

这将完成以下操作：
- ✅ 设置每日即将播出的剧集通知（07:30）
- ✅ 设置每周统计报告（周一08:00）
- ✅ 设置每日最近的活动记录（20:00）
- ✅ 配置WhatsApp通知功能

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

### 4. 分析与统计 📈

```bash
# View your statistics
python3 scripts/ryot_stats.py analytics
# Output: Total media, shows, movies, watch time

# Recently consumed
python3 scripts/ryot_stats.py recent
# Output: Last 10 media you watched/read
```

### 5. 日历与即将播出的剧集 📅

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

### 8. 批量标记剧集 🎬

**使用场景：**
- 查看您在其他地方已经观看过的剧集
- 批量导入观看历史记录
- 一次性标记整个季的观看状态

**注意：** 每集都会通过 `createNewInProgress` 以及 `showSeasonNumber`/`showEpisodeNumber` 独立标记完成状态。

## 工作流程

1. **用户请求** → “我看过多少集《Galaxy Express 999》？”
2. **搜索** → 查找正确的元数据ID
3. **检查进度** → 使用 `python3 scripts/ryot_api.py progress met_XXX` 命令
4. **标记为已完成** → 完成观看后，执行批量进度更新

## 媒体类型

支持的 `lot` 值：
- `SHOW` - 电视剧
- `MOVIE` - 电影
- `BOOK` - 书籍
- `ANIME` - 动画系列
- `GAME` - 视频游戏

## 重要说明

- **首次使用前：** 检查 `/home/node/clawd/config/ryot.json` 文件是否存在。如果不存在，请询问用户他们的Ryot实例URL和API令牌，然后创建配置文件。
- 始终先进行搜索以获取正确的元数据ID。
- 如果有多个结果与剧集名称匹配，请核实年份信息。
- API通过 `/backendgraphql` 提供GraphQL接口。
- 元数据ID以 `met_` 开头。

## 资源

### scripts/ryot_api.py

这是一个用于Ryot GraphQL操作的Python脚本，支持以下功能：
- `search` - 按剧集名称搜索媒体
- `details` - 获取元数据详情
- `complete` - 将剧集标记为已完成