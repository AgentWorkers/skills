---
name: cocreator-content-research
description: "**用于社交媒体平台（TikTok 和 Instagram）的纯粹信息收集功能**  
当特工需要发现热门话题、分析竞争对手的策略或查找特定创作者的资料时，可以使用此技能。该技能不负责生成内容或发布任何内容，而是完全依赖 `ScrapeCreators` 来获取数据以供分析使用。"
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
- 已安装 `uv` 工具
- 环境变量中设置了 `SCRAPE_CREATORS_API_KEY`

## 功能

### 1. 广泛内容发现（关键词和标签）
使用此功能可以找到特定领域或主题的热门内容。它会返回排名前 5 的热门视频/Reels 及其标题。

```bash
uv run {baseDir}/scripts/keyword-search.py --platform tiktok --type keyword --query "dinner recipes"
uv run {baseDir}/scripts/keyword-search.py --platform instagram --type keyword --query "dinner recipes"
```

### 2. 竞争对手分析
使用此功能可以分析特定竞争对手的账号信息。它会返回这些竞争对手的粉丝数量、平均观看次数以及他们发布的 3 个最受欢迎的内容。

```bash
uv run {baseDir}/scripts/competitor-research.py --platform tiktok --handles user1 user2 user3
uv run {baseDir}/scripts/competitor-research.py --platform instagram --handles user1 user2
```

### 3. 账号信息查询
使用此功能可以获取特定创作者的原始数据（粉丝数量、关注者数量、个人简介等）。

```bash
uv run {baseDir}/scripts/profile-lookup.py --platform tiktok --handle <handle>
uv run {baseDir}/scripts/profile-lookup.py --platform instagram --handle <handle>
```