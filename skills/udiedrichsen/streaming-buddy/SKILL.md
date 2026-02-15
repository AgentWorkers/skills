---
name: streaming-buddy
version: 2.0.0
description: "这款个人流媒体助手具备学习用户观看习惯的功能。它会记录您观看的内容，了解您的喜好，并根据您的服务使用情况、情绪以及个人偏好，为您推荐下一部适合观看的影片或节目。您可以在需要获取电影、电视剧信息、流媒体服务推荐，或者想要了解观看进度时使用它。触发指令包括：/stream、'我该看什么'、'推荐点什么'、提及Netflix/Prime/Disney+/Apple TV+等流媒体平台，或者询问剧集/季数/剧集名称；此外，您还可以根据情绪发送请求，例如'推荐一些刺激性的内容'。"
author: clawdbot
license: MIT
metadata:
  clawdbot:
    emoji: "📺"
    triggers: ["/stream"]
    requires:
      bins: ["jq", "curl"]
      env: ["TMDB_API_KEY"]
  tags: ["streaming", "movies", "tv-shows", "recommendations", "entertainment", "learning", "preferences"]
---

# Streaming Buddy 📺

这是一个个性化的流媒体助手，它能学习您的观看习惯，并为您推荐下一部想看的内容。

## 主要功能

- **搜索与信息**：利用TMDB数据查找电影/电视剧信息。
- **观看记录**：跟踪您当前正在观看的内容及其进度。
- **学习系统**：根据您的喜好/评分来了解您的观看偏好。
- **智能推荐**：根据您的口味提供个性化推荐。
- **情绪筛选**：按情绪（如刺激、放松、恐怖等）筛选内容。
- **内容可用性检查**：显示哪些流媒体服务提供您想要的内容。
- **推荐理由说明**：解释为什么某个推荐内容符合您的喜好。

## 命令

| 命令 | 功能 |
|---------|--------|
| `/stream` | 显示所有命令的状态 |
| `/stream search <标题>` | 搜索电影/电视剧 |
| `/stream info <ID> [电视\|电影]` | 显示详细信息及内容可用性 |
| `/stream watch <ID> [电视\|电影]` | 开始跟踪某个内容的观看进度 |
| `/stream progress S01E05` | 更新当前剧集的观看进度 |
| `/stream done [1-5]` | 标记为已观看并评分（系统自动学习您的偏好） |
| `/stream like <ID>` | 将内容标记为“喜欢”，帮助系统学习您的偏好 |
| `/stream dislike <ID>` | 将内容标记为“不喜欢”，帮助系统调整推荐策略 |
| `/stream suggest [服务] [电视\|电影]` | 提供个性化推荐 |
| `/stream mood <情绪>` | 按情绪筛选内容 |
| `/stream surprise` | 随机推荐一部内容 |
| `/stream why <ID>` | 解释为什么推荐这部内容 |
| `/stream watchlist` | 显示观看列表 |
| `/stream watchlist add <ID>` | 将内容添加到观看列表 |
| `/stream history` | 查看观看历史记录 |
| `/stream profile` | 显示您的观看偏好配置 |
| `/stream services` | 管理您使用的流媒体服务 |
| `/stream services add <名称>` | 添加新的流媒体服务 |
| `/stream services remove <名称>` | 删除流媒体服务 |

## 情绪分类

| 情绪 | 类型 |
|------|--------|
| `刺激` | 动作片、惊悚片、科幻片、冒险片 |
| `放松` | 喜剧片、动画片、家庭片、纪录片 |
| `深思** | 戏剧片、悬疑片、历史片 |
| `恐怖` | 恐怖片、惊悚片 |
| `浪漫** | 浪漫片、剧情片 |
| `搞笑` | 喜剧片、动画片 |

## 支持的服务

- `netflix`, `amazon-prime`, `disney-plus`, `apple-tv-plus`
- `youtube-premium`, `wow`, `paramount-plus`, `crunchyroll`
- `joyn`, `rtl`, `magenta`, `mubi`

## 学习系统

该助手通过以下方式学习您的观看偏好：

1. **评分**：当您使用 `/stream done [1-5]` 命令完成观看后：
   - 评分4-5分：将该内容对应的类型/主题/演员添加到“喜欢”列表中。
   - 评分1-2分：将该内容对应的类型添加到“避免”列表中。
2. **明确反馈**：通过 `/stream like` 和 `/stream dislike` 命令提供的信息：
   - 提取内容类型、主题、演员、导演等信息，并更新您的偏好权重。
3. **偏好配置**：包括：
   - 各类型内容的偏好得分（按权重排序）
   - 喜欢/不喜欢的主题
   - 最喜欢的演员和导演
   - 自定义的情绪关联规则

## 使用说明

```bash
# Core commands
handler.sh status $WORKSPACE
handler.sh search "severance" $WORKSPACE
handler.sh info 95396 tv $WORKSPACE
handler.sh watch 95396 tv $WORKSPACE
handler.sh progress S01E05 $WORKSPACE
handler.sh done 5 "Great show!" $WORKSPACE

# Learning commands
handler.sh like $WORKSPACE                    # Like current watching
handler.sh like 12345 movie $WORKSPACE        # Like specific title
handler.sh dislike $WORKSPACE
handler.sh why 95396 tv $WORKSPACE
handler.sh profile $WORKSPACE

# Recommendation commands
handler.sh suggest $WORKSPACE                 # All services, all types
handler.sh suggest prime movie $WORKSPACE     # Prime movies only
handler.sh mood exciting $WORKSPACE
handler.sh mood relaxing tv $WORKSPACE
handler.sh surprise $WORKSPACE

# List commands
handler.sh watchlist list $WORKSPACE
handler.sh watchlist add 12345 tv $WORKSPACE
handler.sh history $WORKSPACE

# Service management
handler.sh services list $WORKSPACE
handler.sh services add netflix $WORKSPACE
handler.sh services remove netflix $WORKSPACE
```

## 数据存储

所有数据存储在 `$WORKSPACE/memory/streaming-buddy/` 目录下：

| 文件 | 用途 |
|------|---------|
| `config.json` | TMDB API密钥、地区设置、语言设置 |
| `profile.json` | 用户配置信息 |
| `services.json` | 当前使用的流媒体服务列表 |
| `preferences.json` | 学习到的观看偏好 |
| `watching.json` | 当前正在观看的内容 |
| `watchlist.json` | 您想观看的内容列表 |
| `history.json` | 观看历史记录及评分 |
| `cache/*.json` | API响应缓存（有效期24小时）

## 设置步骤

1. 获取TMDB API密钥：[https://www.themoviedb.org/settings/api]
2. 将密钥保存到 `memory/streaming-buddy/config.json` 文件中。
3. 运行 `/stream setup` 命令来配置流媒体服务。

## 使用示例

- **按情绪筛选内容**：
```
User: I want something exciting tonight
Bot: 🎬 Exciting picks for you:
     1. Reacher S3 (Prime) ⭐8.5
     2. Jack Ryan (Prime) ⭐8.1
     ...
```

- **根据反馈学习推荐内容**：
```
User: /stream done 5
Bot: ✅ Severance marked as done (⭐5)
     📚 Learned: +Drama, +Mystery, +Sci-Fi
     Actors: Adam Scott, Britt Lower saved to favorites
```

- **解释推荐理由**：
```
User: /stream why 95396
Bot: 🎯 Why Severance matches you:
     ✓ Genre "Drama" (you like this, +2)
     ✓ Genre "Mystery" (you like this, +2)
     ✓ Theme "office" in your preferences
     ✓ With Adam Scott (your favorite)
     Similar to: Fallout ⭐5
```

## 语言支持

- 语言根据 `config.json` 文件中的设置（如 `language: "de-DE"` 或 `"en"`）自动识别。
- 所有输出都会根据配置的语言进行适配。
- 所有命令在任何语言环境下均能正常使用。

## 系统要求

- 需要安装 `jq`（JSON处理工具）和 `curl`（HTTP客户端）。
- 系统需支持 `bash` 4.0 或更高版本。
- 需要TMDB API密钥（免费获取）。

## 参考资料

- [services.md](references/services.md) — 流媒体服务完整列表
- [tmdb-api.md](references/tmdb-api.md) — TMDB API使用指南
- [justwatch.md](references/justwatch.md) — 内容可用性数据整合方式