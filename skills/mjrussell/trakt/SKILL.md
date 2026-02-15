---
name: trakt
description: 通过 trakt.tv 跟踪并查看您观看过的电影和电视剧。当用户询问他们的观看历史、正在观看的内容，或者想要搜索电影/电视剧时，可以使用该功能。
homepage: https://trakt.tv
metadata:
  clawdbot:
    emoji: "🎬"
    requires:
      bins: ["trakt-cli"]
---

# Trakt CLI

用于查询您的 trakt.tv 观看历史记录以及搜索电影/电视剧。

## 安装

```bash
npm install -g trakt-cli
```

## 设置

1. 在 https://trakt.tv/oauth/applications/new 创建一个应用程序。
2. 运行以下命令：`trakt-cli auth --client-id <id> --client-secret <secret>`
3. 访问系统显示的 URL 并输入设备代码。
4. 凭据将保存在 `~/.trakt.yaml` 文件中。

## 命令

### 观看历史记录

```bash
trakt-cli history                  # Recent history (default: 10 items)
trakt-cli history --limit 25       # Show more
trakt-cli history --page 2         # Paginate
```

### 搜索

```bash
trakt-cli search "Breaking Bad"
trakt-cli search "The Matrix"
```

## 使用示例

**用户：“我最近看了什么？”**
```bash
trakt-cli history
```

**用户：“显示我最近观看的 20 个项目。”**
```bash
trakt-cli history --limit 20
```

**用户：“查找关于《Severance》的信息。”**
```bash
trakt-cli search "Severance"
```

## 注意事项

- 搜索功能无需认证即可使用。
- 查看观看历史记录需要认证。
- 查看历史记录仅支持只读权限。