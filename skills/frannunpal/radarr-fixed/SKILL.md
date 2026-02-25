---
name: radarr-fixed
version: 1.0.4
changelog: "Fixed config path from .openclagent to .openclaw and updated script paths"
description: >
  **功能说明：**  
  在 Radarr 中搜索并添加电影。支持创建电影收藏，以及在选择添加电影时直接进行搜索的功能。该功能是基于 jordyvandomselaar/radarr 项目开发的衍生版本，已修复了元数据相关的问题（metadata issues）。  
  **主要特性：**  
  1. **搜索与添加电影**：用户可以轻松地在 Radarr 中搜索电影，并将找到的电影直接添加到自己的收藏列表中。  
  2. **收藏功能**：允许用户创建电影收藏，以便日后快速查看或重新搜索这些电影。  
  3. **搜索选项**：在添加电影的过程中，用户可以选择是否直接进行搜索，提高操作效率。  
  4. **元数据修复**：作为 jordyvandomselaar/radarr 的衍生版本，该功能修复了元数据处理过程中存在的问题，确保电影信息的准确性和完整性。  
  **技术背景：**  
  Radarr 是一个用于管理和组织电影资源的开源工具，提供了丰富的搜索和过滤功能。通过这个扩展功能，用户可以更便捷地管理和使用自己的电影收藏。
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins:
        - curl
        - jq
      config:
        - path: ~/.openclaw/credentials/radarr/config.json
          description: "Radarr API configuration with url, apiKey, and defaultQualityProfile"
      env:
        - name: RADARR_URL
          optional: true
          description: "Radarr instance URL (overrides config file)"
        - name: RADARR_API_KEY
          optional: true
          description: "Radarr API key (overrides config file)"
    fork:
      original: jordyvandomselaar/radarr
      original_url: https://clawhub.com/jordyvandomselaar/radarr
      reason: "Fixed metadata to properly declare required credentials and config paths"
---
# Radarr（已修复）

**⚠️ 分支说明：** 这是 [jordyvandomselaar/radarr](https://clawhub.com/jordyvandomselaar/radarr) 的一个分支，其中元数据声明已修正。

您可以使用集合功能将电影添加到 Radarr 库中。

## 设置

创建 `~/.openclaw/credentials/radarr/config.json` 文件：
```json
{
  "url": "http://localhost:7878",
  "apiKey": "your-api-key",
  "defaultQualityProfile": 1
}
```
- `defaultQualityProfile`：质量配置文件的 ID（运行 `config` 命令可查看可用选项）

### 备选方案：环境变量
您也可以使用环境变量来配置：
- `RADARR_URL`：Radarr 实例的 URL
- `RADARR_API_KEY`：Radarr 的 API 密钥

## 工作流程

1. **搜索**：输入 “电影名称” 进行搜索，系统会返回带有编号的电影列表。
2. **显示结果并附上 TMDB 链接**：所有结果都会显示可点击的链接。
3. **选择电影**：用户从列表中选择一个电影编号。
4. **检查是否属于集合**：如果该电影属于某个集合，系统会询问用户是否将其添加到该集合中。
5. **添加电影**：用户可以选择单独添加电影或整个集合。

## 重要提示：
- 在向用户展示搜索结果时，**务必** 包含 TMDB 链接。
- 链接格式：`[电影名称 (年份)](https://themoviedb.org/movie/ID)`
- 系统会使用配置文件中的 `defaultQualityProfile`；您也可以在添加电影时手动更改该配置。

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
**删除文件前请务必询问用户是否确认！**

### 获取根文件夹和质量配置文件（用于配置）
```bash
bash scripts/radarr.sh config
```

---
*原始技能由 [jordyvandomselaar](https://clawhub.com/jordyvandomselaar) 开发。本分支在开源许可下进行维护。*