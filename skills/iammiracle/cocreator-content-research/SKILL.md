---
name: cocreator-content-research
description: "**仅用于社交媒体平台（TikTok 和 Instagram）的情报收集。** 当特工需要发现热门话题、分析竞争对手的策略或查找特定创作者的资料时，可以使用此技能。该技能不生成内容或发布任何内容；它完全依赖于 **ScrapeCreators** 来获取数据以供分析。"
metadata:
  {
    "openclaw": {
      "emoji": "🔍",
      "requires": {
        "bins": ["uv"],
        "env": ["SCRAPE_CREATORS_API_KEY"]
      },
      "primaryEnv": "SCRAPE_CREATORS_API_KEY",
      "install": [
        {
          "id": "uv-install",
          "kind": "bash",
          "script": "curl -LsSf https://astral.sh/uv/install.sh | sh",
          "bins": ["uv"],
          "label": "Install uv (cross-platform via bash)"
        }
      ]
    }
  }
---
# 内容研究技能

该技能使代理能够使用 ScrapeCreators API 收集关于社交媒体（TikTok 和 Instagram）表现的原始情报。该技能不生成内容，也不与发布 API 进行交互。

## 先决条件
- 已安装 `uv` 工具。
- 环境变量中已设置 `SCRAPE_CREATORS_API_KEY`。

## 功能

### 1. 广泛内容发现（关键词和标签）
使用此功能可以找到表现最佳的内容。
**代理使用关键词搜索的说明：**
- **切勿** 每次都使用相同的硬编码关键词（例如 “affirmations”）。
- **始终** 根据用户的应用类型，想出 3-5 个不同的关键词（例如，如果是关于积极心态的应用，可以尝试搜索 “mindset shift”、“daily routine”、“self healing”、“morning motivation”）。
- 使用时间范围参数 (`--date-posted`) 来查找最新趋势，并测试不同的排序方法。
- 如果用户特别要求只获取某种类型的内容，请使用 `--format` 过滤器（`video`、`slideshow` 或 `both`）。
- **重要提示：** 脚本会返回一个布尔值 `is_slideshow` 和一个视频链接 (`video_url`)。利用这些信息来区分视频趋势和幻灯片展示趋势。

```bash
uv run {baseDir}/scripts/keyword-search.py --platform tiktok --type keyword --query "morning routine" --date-posted this-month --sort-by most-liked --format slideshow
uv run {baseDir}/scripts/keyword-search.py --platform instagram --type keyword --query "morning routine" --format video
```

### 2. 竞争对手分析
使用此功能可以分析特定的竞争对手账号。
**代理进行竞争对手分析的说明：**
- **在开始分析之前，务必** 先询问用户是否有具体的竞争对手或创作者账号需要查询。
- 如果用户不知道，可以先使用关键词搜索来找出他们所在领域的潜在热门创作者，提取他们的账号信息，然后再对这些创作者进行详细分析。

```bash
uv run {baseDir}/scripts/competitor-research.py --platform tiktok --handles user1 user2 user3
uv run {baseDir}/scripts/competitor-research.py --platform instagram --handles user1 user2
```

### 3. 账号资料查询
使用此功能可以获取特定创作者的原始数据（关注者数量、被关注者数量以及个人简介）。

```bash
uv run {baseDir}/scripts/profile-lookup.py --platform tiktok --handle <handle>
uv run {baseDir}/scripts/profile-lookup.py --platform instagram --handle <handle>
```