---
name: sonarr
version: 1.0.0
description: 在 Sonarr 中搜索并添加电视剧功能。支持设置显示选项（monitor options），以及在执行添加操作时直接进行搜索（search-on-add）。
metadata: {"clawdbot":{"emoji":"📺","requires":{"bins":["curl","jq"]}}}
---

# Sonarr

将电视剧添加到您的 Sonarr 库中。

## 设置

创建 `~/.clawdbot/credentials/sonarr/config.json` 文件：
```json
{
  "url": "http://localhost:8989",
  "apiKey": "your-api-key",
  "defaultQualityProfile": 1
}
```
- `defaultQualityProfile`：质量配置文件的 ID（运行 `config` 命令可查看可用选项）

## 工作流程

1. **搜索**：输入 “Show Name”（剧集名称）进行搜索 - 返回带编号的剧集列表
2. **显示结果并附带 TVDB 链接**：始终显示可点击的链接
3. **选择剧集**：用户从列表中选择一个剧集编号
4. **添加剧集**：添加选中的剧集并重新开始搜索

## 重要提示：
- 在向用户展示搜索结果时，**务必包含 TVDB 链接**。
- 链接格式：`[剧集名称 (年份)](https://thetvdb.com/series/SLUG)`
- 使用配置文件中的 `defaultQualityProfile`；也可以在添加剧集时进行自定义设置

## 命令

### 搜索剧集
```bash
bash scripts/sonarr.sh search "Breaking Bad"
```

### 检查剧集是否已存在于库中
```bash
bash scripts/sonarr.sh exists <tvdbId>
```

### 添加剧集（默认情况下会立即执行搜索）
```bash
bash scripts/sonarr.sh add <tvdbId>              # searches right away
bash scripts/sonarr.sh add <tvdbId> --no-search  # don't search
```

### 删除剧集
```bash
bash scripts/sonarr.sh remove <tvdbId>                # keep files
bash scripts/sonarr.sh remove <tvdbId> --delete-files # delete files too
```
**删除剧集前务必询问用户是否确认！**

### 获取根文件夹及质量配置文件（用于配置）
```bash
bash scripts/sonarr.sh config
```