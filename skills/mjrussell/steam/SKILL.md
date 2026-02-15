---
name: steam
description: 在 Steam 图书馆中浏览、筛选和发现游戏。可以根据游戏游玩时长、用户评分、Steam Deck 兼容性、游戏类型以及标签进行筛选。当用户询问他们的 Steam 游戏、想玩什么游戏或需要游戏推荐时，可以使用此功能来查找适合在 Steam Deck 上运行的游戏。
homepage: https://github.com/mjrussell/steam-cli
metadata:
  clawdbot:
    emoji: "🎮"
    requires:
      bins: ["steam"]
      env: ["STEAM_API_KEY"]
---

# Steam Games CLI

这是一个用于浏览和发现Steam游戏库中游戏的命令行工具（CLI）。支持根据游戏游玩时间、评分、Steam Deck兼容性、游戏类型和标签进行筛选。

## 安装

```bash
npm install -g steam-games-cli
```

## 设置

1. 从 [https://steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey) 获取Steam Web API密钥。
2. 配置CLI：
```bash
steam config set-key YOUR_API_KEY
steam config set-user YOUR_STEAM_ID
```

## 命令

### 查看用户信息（Profile）

```bash
steam whoami               # Profile info and library stats
steam whoami --json
```

### 查看游戏库（Library）

```bash
steam library              # List all games
steam library --limit 10   # Limit results
steam library --json       # JSON output for scripting
```

### 查看标签和游戏类型（Tags & Genres）

```bash
steam tags                 # List all 440+ Steam tags
steam tags --json
steam genres               # List all genres
steam genres --json
```

## 筛选选项

### 游玩时间（Playtime）

```bash
steam library --unplayed                    # Never played
steam library --min-hours 10                # At least 10 hours
steam library --max-hours 5                 # Less than 5 hours
steam library --deck                        # Played on Steam Deck
```

### 评分（1-9分）

```bash
steam library --reviews very-positive       # Exact category
steam library --min-reviews 7               # Score 7+ (Positive and above)
steam library --show-reviews                # Show review column
```

**评分等级：**
- 非常正面（9分）
- 非常正面（8分）
- 正面（7分）
- 大部分正面（6分）
- 中立（5分）
- 大部分负面（4分）
- 负面（3分）
- 非常负面（2分）
- 非常负面（1分）

### Steam Deck兼容性（Steam Deck Compatibility）

```bash
steam library --deck-compat verified        # Verified only
steam library --deck-compat playable        # Playable only
steam library --deck-compat ok              # Verified OR Playable
steam library --show-compat                 # Show Deck column
```

### 查看标签和游戏类型（Tags & Genres）

```bash
steam library --tag "Roguelike"             # Filter by tag
steam library --genre "Strategy"            # Filter by genre
steam library --show-tags                   # Show tags column
```

### 排序（Sorting）

```bash
steam library --sort name                   # Alphabetical (default)
steam library --sort playtime               # Most played first
steam library --sort deck                   # Most Deck playtime first
steam library --sort reviews                # Best reviewed first
steam library --sort compat                 # Best Deck compat first
```

## 适用于AI代理的工作流程

该CLI针对使用流融合（stream fusion）和提前终止（early termination）机制的AI代理进行了优化。

### 第一步：快速查找可用标签/游戏类型（Step 1: Discover available tags/genres）

```bash
steam tags --json
steam genres --json
```

### 第二步：根据组合条件筛选游戏库（Step 2: Filter library with combined criteria）

```bash
# Unplayed Deck Verified roguelikes with good reviews
steam library --unplayed --deck-compat verified --tag "Roguelike" --min-reviews 7 --limit 10 --json

# Well-reviewed strategy games under 5 hours
steam library --max-hours 5 --genre "Strategy" --min-reviews 8 --limit 5 --json

# Trading games playable on Deck
steam library --tag "Trading" --deck-compat ok --limit 10 --json
```

### 性能说明

- 本地筛选条件（游玩时间、未玩过的游戏）会首先被应用，并且是即时生效的。
- 远程筛选条件（评分、Steam Deck兼容性、标签）会针对每款游戏并行获取数据。
- 当达到筛选限制时，程序会立即停止执行。
- 优先使用本地筛选条件以减少API调用次数。

## 使用示例

**用户：“我在Steam Deck上应该玩什么游戏？”**
```bash
steam library --deck-compat verified --min-reviews 7 --sort playtime --limit 10
```

**用户：“我有哪些roguelike游戏？”**
```bash
steam library --tag "Roguelike" --show-tags --limit 20
```

**用户：“有哪些评分很高的未玩过的游戏？”**
```bash
steam library --unplayed --min-reviews 8 --sort reviews --limit 10 --show-reviews
```

**用户：“我有多少款游戏？”**
```bash
steam whoami
```

**用户：“哪些策略游戏可以在Steam Deck上玩？”**
```bash
steam library --genre "Strategy" --deck-compat ok --show-compat --limit 15
```

**用户：“有哪些可用的标签？”**
```bash
steam tags --json
```

## 输出格式

- 默认格式：彩色表格
- `--plain`：纯文本列表
- `--json`：JSON格式，适用于脚本编写或AI代理使用