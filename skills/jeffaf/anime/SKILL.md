---
name: anime
version: 1.0.1
description: "这是一个用于AI代理的命令行工具（CLI），帮助人类用户搜索和查询动漫信息。该工具使用了Jikan（非官方的MyAnimeList API），且无需进行身份验证。"
homepage: https://jikan.moe
metadata:
  openclaw:
    emoji: "🎌"
    requires:
      bins: ["bash", "curl", "jq"]
    tags: ["anime", "myanimelist", "jikan", "entertainment", "cli"]
---

# 动画查询工具

这是一个为AI代理设计的命令行工具，用于帮助用户查询和查找动画信息。例如：“那个关于精灵法师的动画是关于什么的？”——现在你的AI代理可以回答这个问题了。

该工具使用了Jikan（非官方的MyAnimeList API），无需注册账户或API密钥。

## 使用方法

```
"Search for anime called Frieren"
"What's the top anime right now?"
"What anime is airing this season?"
"Tell me about anime ID 52991"
```

## 命令列表

| 功能 | 命令                |
|--------|-------------------|
| 搜索    | `anime search "查询内容"`     |
| 获取详情 | `anime info <动画ID>`     |
| 当前季   | `anime season`       |
| 热门动画 | `anime top [数量]`      |
| 即将上映 | `anime upcoming [数量]`     |
| 特定季   | `anime season <年份> <季数>`   |

### 使用示例

```bash
anime search "one punch man"      # Find anime by title
anime info 30276                  # Get full details by MAL ID
anime top 10                      # Top 10 anime
anime season                      # Currently airing
anime season 2024 fall            # Fall 2024 season
anime upcoming 5                  # Next 5 upcoming anime
```

## 输出结果

**搜索/列表结果：**
```
[52991] Sousou no Frieren — 28 eps, Finished Airing, ⭐ 9.28
```

**详情输出：**
```
🎬 Sousou no Frieren
   English: Frieren: Beyond Journey's End
   MAL ID: 52991 | Score: 9.28 | Rank: #1
   Episodes: 28 | Status: Finished Airing
   Genres: Adventure, Drama, Fantasy
   Studios: Madhouse

📖 Synopsis:
[Full synopsis text]

🎥 Trailer: [YouTube URL if available]
```

## 注意事项

- 该工具基于Jikan v4 API（api.jikan.moe）开发。
- 请求速率限制：每秒3次请求，每分钟60次请求。
- 无需身份验证。
- “MAL ID”指的是MyAnimeList数据库中的动画ID。
- 动画季分为：冬季、春季、夏季、秋季。

---

## 代理实现说明

**脚本位置：`{skill_folder}/anime`（实际路径为`scripts/anime`）**

**当用户询问动画相关信息时：**
1. 运行 `./anime search "动画标题"` 以获取动画的MAL ID。
2. 运行 `./anime info <MAL_ID>` 以获取详细信息。
3. 运行 `./anime season` 或 `./anime top` 以获取推荐结果。

**不适用场景：** 非动画类媒体（如漫画、电影，除非是指动画电影）。