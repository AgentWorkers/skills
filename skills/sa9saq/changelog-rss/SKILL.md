---
description: 将 `CHANGELOG.md` 文件转换为 RSS 2.0 格式，以便用于发布监控。
---

# Changelog RSS

将 `CHANGELOG.md` 文件转换为用于版本跟踪的 RSS 源。

## 指令

### 第一步：获取 Changelog 文件
- 从用户处获取本地 `CHANGELOG.md` 文件的路径。
- 如果使用 GitHub 仓库，可以通过仓库 URL 获取 `CHANGELOG.md` 文件；如果无法获取，则可以使用 Releases API 作为备用方案。
- 对于 npm/pip 包，可以直接从它们的文档中获取 changelogs。

### 第二步：解析并转换
解析 [Keep a Changelog](https://keepachangelog.com/) 格式的内容：
- 提取版本信息：`## [x.y.z] - YYYY-MM-DD`
- 提取各个部分：Added（新增功能）、Changed（修改内容）、Deprecated（已弃用功能）、Removed（删除功能）、Fixed（修复问题）、Security（安全问题）
- 处理不同的版本格式：`## x.y.z`、`## v1.2.3` 等

生成符合 RSS 2.0 标准的格式：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{Project} Changelog</title>
    <link>{repo-url}</link>
    <description>Release notes for {Project}</description>
    <item>
      <title>v1.2.0</title>
      <pubDate>Mon, 01 Jan 2025 00:00:00 GMT</pubDate>
      <description><![CDATA[<h3>Added</h3><ul><li>...</li></ul>]]></description>
    </item>
  </channel>
</rss>
```

### 第三步：输出结果
- 保存生成的 RSS 文件，并提供其路径。
- 建议将 RSS 文件托管在 GitHub Pages 或静态文件服务器上。
- 为了实现持续监控，可以使用 cron 作业定期重新生成 RSS 文件。

## 特殊情况处理
- **非标准格式**：尽力进行解析；对于无法解析的部分，向用户发出警告。
- **缺少日期**：使用文件的修改时间或 Git 日志中的日期作为替代。
- **存在多个 changelogs**：将它们合并到一个 RSS 源中，并在每个 changelog 前添加来源前缀。
- **存在 “Unreleased” 部分**：跳过所有属于该部分的条目。

## 所需工具/环境
- 基本转换功能不需要任何依赖项（仅需要文本处理工具）。
- 可选：使用 `curl` 命令来获取远程 changelogs。
- 不需要 API 密钥。