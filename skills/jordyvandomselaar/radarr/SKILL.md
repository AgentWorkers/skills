---
name: radarr
version: 1.0.1
description: 在 Radarr 中搜索并添加电影。支持创建电影收藏，以及在选择添加电影时直接进行搜索的功能。
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["curl","jq"]}}}
---

# Radarr

通过集合功能将电影添加到您的 Radarr 图书库中。

## 设置

创建 `~/.clawdbot/credentials/radarr/config.json` 文件：
```json
{
  "url": "http://localhost:7878",
  "apiKey": "your-api-key",
  "defaultQualityProfile": 1
}
```
- `defaultQualityProfile`：质量配置文件的 ID（运行 `config` 命令可查看可用选项）

## 工作流程

1. **搜索**：输入 “电影名称” 进行搜索 - 返回编号列表
2. **显示结果并附上 TMDB 链接** - 确保链接可点击
3. **选择结果**：用户从列表中选择一个电影编号
4. **检查集合状态**：如果该电影属于某个集合，系统会询问用户是否将其添加到该集合中
5. **添加电影**：单独添加电影或整个集合

## 重要提示：
- 在向用户展示搜索结果时，**务必包含 TMDB 链接**。
- 链接格式：`[电影名称 (年份)](https://themoviedb.org/movie/ID)`
- 系统使用配置文件中的 `defaultQualityProfile`；用户也可以在添加电影时进行自定义设置

## 命令

### 搜索电影
```bash
bash scripts/radarr.sh search "Inception"
```

### 检查电影是否存在于库中
```bash
bash scripts/radarr.sh exists <tmdbId>
```

### 添加电影（默认情况下会立即执行搜索）
```bash
bash scripts/radarr.sh add <tmdbId>           # searches right away
bash scripts/radarr.sh add <tmdbId> --no-search  # don't search
```

### 添加整个集合（默认情况下会立即执行搜索）
```bash
bash scripts/radarr.sh add-collection <collectionTmdbId>
bash scripts/radarr.sh add-collection <collectionTmdbId> --no-search
```

### 删除电影
```bash
bash scripts/radarr.sh remove <tmdbId>              # keep files
bash scripts/radarr.sh remove <tmdbId> --delete-files  # delete files too
```
**删除电影前请务必询问用户是否确认删除！**

### 获取根文件夹和质量配置文件（用于配置）
```bash
bash scripts/radarr.sh config
```