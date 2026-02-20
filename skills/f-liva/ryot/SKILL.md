---
name: ryot
description: 通过 Ryot API 追踪和管理媒体消费情况（电视剧、电影、书籍、动漫、游戏）。当用户希望将内容标记为已观看/已阅读/已完成、搜索媒体、查看观看进度或记录媒体活动时，可以使用该 API。触发事件包括“将 X 标记为已完成”、“我看过 Y 吗？”、“将 Z 添加到我的列表中”以及任何与媒体跟踪相关的操作。
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
# Ryot 媒体追踪器

通过 Ryot 的 GraphQL API 可以追踪电视节目、电影、书籍、动漫和游戏。

## 设置（必需）

在使用此功能之前，您必须配置您的 Ryot 实例：

1. 在 `/home/node/clawd/config/ryot.json` 文件中创建配置文件：

```json
{
  "url": "https://your-ryot-instance.com",
  "api_token": "your_api_token_here"
}
```

2. 设置您的 Ryot 实例 URL — 将 `https://your-ryot-instance.com` 替换为您实际的 Ryot 服务器地址
3. 从 Ryot 实例设置中获取 API 令牌
4. 保存配置文件 — 该功能会自动读取此文件

## 使用方法

使用 `scripts/ryot_api.py` 执行所有与 Ryot 相关的操作。

## 常见任务

### 1. 将媒体标记为已完成

```bash
# Search for the item first
python3 scripts/ryot_api.py search "Breaking Bad" --type SHOW

# Mark as completed (uses metadata ID from search)
python3 scripts/ryot_api.py complete met_XXXXX
```

### 2. 搜索媒体

```bash
# Search for TV shows
python3 scripts/ryot_api.py search "The Wire" --type SHOW

# Search for movies
python3 scripts/ryot_api.py search "Inception" --type MOVIE

# Search for books
python3 scripts/ryot_api.py search "1984" --type BOOK

# Search for anime
python3 scripts/ryot_api.py search "Death Note" --type ANIME
```

### 3. 获取媒体详情

在标记为已完成之前，请验证元数据（标题、年份等）：

```bash
python3 scripts/ryot_api.py details met_XXXXX
```

## 工作流程

1. **用户请求** → “我看完《绝命毒师》了”
2. **搜索** → 查找正确的元数据 ID
3. **验证** → 如果有多个结果与标题匹配，请核实年份/详情
4. **标记为已完成** → 部分或全部更新进度状态

## 媒体类型

支持的 `lot` 值：
- `SHOW` - 电视系列
- `MOVIE` - 电影
- `BOOK` - 书籍
- `ANIME` - 动漫系列
- `GAME` - 视频游戏

## 重要说明

- **首次使用前：** 检查 `/home/node/clawd/config/ryot.json` 文件是否存在。如果不存在，请询问用户他们的 Ryot 实例 URL 和 API 令牌，然后创建配置文件。
- 始终先进行搜索以获取正确的元数据 ID。
- 如果有多个结果与标题匹配，请核实年份。
- API 使用的接口地址为 `/backendgraphql`。
- 元数据 ID 以 `met_` 开头。

## 资源

### scripts/ryot_api.py

用于执行 Ryot GraphQL 操作的 Python 脚本。支持以下功能：
- `search` — 按标题搜索媒体
- `details` — 获取媒体详情
- `complete` — 将媒体标记为已完成