---
name: sonarr-fixed
version: 1.0.2
description: >
  **功能说明：**  
  - 在 Sonarr 中搜索并添加电视节目；  
  - 支持在添加节目时进行实时搜索；  
  - 该功能是基于 jordyvandomselaar/sonarr 项目开发的衍生版本，已修复了元数据相关的问题（metadata issues）。  
  **主要特点：**  
  1. **实时搜索**：在添加节目时可以立即开始搜索，无需等待程序完成初始加载；  
  2. **监控选项**：允许用户监控已添加节目的播放状态；  
  3. **元数据修复**：解决了原项目中存在的元数据错误问题，确保节目信息显示准确。  
  **技术背景：**  
  Sonarr 是一款流行的开源媒体管理软件，用于组织和管理电视节目、电影等媒体文件。该插件通过扩展 Sonarr 的功能，提供了更便捷的节目搜索和添加体验。
metadata:
  openclaw:
    emoji: "📺"
    requires:
      bins:
        - curl
        - jq
      config:
        - path: ~/.openclaw/credentials/sonarr/config.json
          description: "Sonarr API configuration with url, apiKey, and defaultQualityProfile"
      env:
        - name: SONARR_URL
          optional: true
          description: "Sonarr instance URL (overrides config file)"
        - name: SONARR_API_KEY
          optional: true
          description: "Sonarr API key (overrides config file)"
    fork:
      original: jordyvandomselaar/sonarr
      original_url: https://clawhub.com/jordyvandomselaar/sonarr
      reason: "Fixed metadata to properly declare required credentials and config paths"
---
# Sonarr（已修复）

**⚠️ 分支说明：** 这是一个基于 [jordyvandomselaar/sonarr](https://clawhub.com/jordyvandomselaar/sonarr) 的分支版本，其中元数据声明已修正。

**将电视剧添加到您的 Sonarr 库中。**

## 设置

创建 `~/.openclaw/credentials/sonarr/config.json` 文件：
```json
{
  "defaultQualityProfile": "质量配置文件 ID"  // 运行 `config` 命令可查看可用选项
}
```

### 替代方案：环境变量
您也可以使用环境变量来配置 Sonarr：
- `SONARR_URL`：Sonarr 服务器的 URL
- `SONARR_API_KEY`：Sonarr 的 API 密钥

## 工作流程

1. **搜索**：输入电视剧名称进行搜索，系统会返回带有编号的搜索结果列表。
2. **显示结果并附上 TVDB 链接**：所有结果都会显示可点击的链接。
3. **选择结果**：用户从列表中选择一个剧集编号。
4. **添加剧集**：系统会自动开始添加该剧集并继续搜索。

**重要提示：**
- 在向用户展示搜索结果时，**务必包含 TVDB 链接**。
- 链接格式应为：`[剧集名称 (年份)](https://thetvdb.com/series/SLUG)`
- 系统会使用配置文件中的 `defaultQualityProfile`；您也可以在添加剧集时手动更改该配置。

## 命令

### 搜索剧集
```bash
# 搜索剧集名称
```

### 检查剧集是否已存在于库中
```bash
# 检查剧集是否存在
```

### 添加剧集（默认情况下会立即开始搜索）
```bash
# 添加剧集
```

### 删除剧集
```bash
# 删除剧集
# 删除剧集前请务必询问用户是否确认删除
```

### 获取根目录和质量配置文件（用于配置）
```bash
# 获取根目录和质量配置文件
```

---
*该技能最初由 [jordyvandomselaar](https://clawhub.com/jordyvandomselaar) 开发。本分支在开源许可下进行维护。*