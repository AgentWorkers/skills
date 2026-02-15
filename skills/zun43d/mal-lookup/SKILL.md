---
name: mal-lookup
version: 1.3.0
description: **Direct MyAnimeList 查询工具**：该工具通过使用 MAL（MyAnimeList）的内部接口来绕过 Jikan 或 API 在使用过程中可能遇到的问题。
metadata:
  openclaw:
    emoji: "🎌"
    requires:
      bins: ["curl", "jq", "grep", "awk"]
    tags: ["anime", "manga", "mal", "search", "list"]
---

# MAL 查询

可以直接通过 MyAnimeList.net 查询动漫/漫画信息或获取用户列表。该功能使用了 MAL 的内部 `load.json` 和 `prefix.json` 端点。

## 使用方法

**搜索：**
`mal search anime "frieren"`  （搜索标题为 "frieren" 的动漫）
`mal search manga "berserk"`  （搜索标题为 "berserk" 的漫画）

**高级搜索（类型 + 评分）：**
`mal advanced action 8`  （评分高于 8 的顶级动作类动漫）
`mal advanced psychological 0`  （所有评分在 0 以上的心理类动漫）

**获取用户列表：**
`mal list anime zun43d`  （获取用户 zun43d 的动漫列表）
`mal list manga zun43d reading`  （获取用户 zun43d 的漫画列表）

**排行榜：**
`mal top`  （当前正在播出的顶级动漫排行榜）
`mal season 2024 spring`  （2024 年春季的动漫季排行榜）

## 命令说明

| 命令 | 说明 |
|---------|-------------|
| `mal search <类型> <查询>` | 按标题搜索动漫/漫画。 |
| `mal advanced <类型> [最低评分]` | 按类型和最低评分搜索动漫。 |
| `mal list <类型> <用户> [状态>` | 获取用户的动漫/漫画列表。 |
| `mal top` | 获取当前正在播出的前 10 部动漫。 |
| `mal season <年份> <季度>` | 获取特定季度的前 10 部动漫。 |

### 支持的类型：
动作、冒险、喜剧、剧情、科幻、悬疑、心理、惊悚、浪漫、日常生活、恐怖、奇幻、体育、机甲、音乐……