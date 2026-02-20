---
name: leetify
description: 通过 Leetify API 获取 CS2/CS:GO 玩家的统计数据、比赛分析以及游戏玩法洞察。该服务利用 Telegram 用户名与 Steam ID 之间的映射关系，实现便捷的访问。适用于需要“demo 分析”（анализ демки）、“比赛分析”（разбор матча）或“我哪里做错了”（что я сделал не так）等场景。
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "env": ["LEETIFY_API_KEY"],
            "bins": ["python3", "bash", "bunzip2", "gunzip"],
            "pip": ["requests", "demoparser2"],
          },
      },
  }
---
# Leetify API 功能

从 Leetify 平台获取 CS2/CS:GO 的统计数据。

## 快速统计（默认选项）

除非明确请求（例如：“demo analysis”或“分析演示视频”），否则请避免下载或分析演示视频。对于一般的统计查询，使用以下命令以节省时间和资源。

### 显示统计数据
```bash
bash scripts/get_stats_by_username.sh USERNAME
```
*显示：平均数据（100 场游戏）、最近 5 场比赛的击杀/死亡比（K/D/A）、平均每分钟伤害（ADR）、伤害输出（HS）、最有价值球员（MVPs）、排名以及总体统计数据。*

### 获取比赛数据（用于分析的 JSON 格式）
```bash
bash scripts/get_match_details.sh USERNAME [INDEX]
```
*输出：特定比赛的完整原始 JSON 统计数据。*
**使用说明：**在展示这些数据时，务必使用表情符号将 JSON 格式化为易于阅读的报告。将不同部分（如总体统计数据、射击数据、建议和错误分析）分开显示。

### 比较玩家表现
```bash
bash scripts/compare_by_username.sh USERNAME1 USERNAME2
```

### 公会赛季统计数据
```bash
python3 scripts/season_stats.py
```
*显示：当前赛季所有公会成员的汇总表格。*

## 演示视频分析（用于“分析演示视频”等场景）

**当用户请求演示视频分析、比赛细节或战术评估时，请始终遵循以下流程：**

### 第一步：确定玩家及其游戏内名称（IGN）
- 获取 Steam ID：`python3 scripts/steam_ids.py get --username USERNAME`
- 记分板上每个玩家名称旁边会以 `[steamid]` 的格式显示 Steam ID。请务必根据 Steam ID 来识别目标玩家。
- 流程：获取 Steam ID -> 在记分板中找到对应 Steam ID 的行 -> 这就是你要分析的玩家。

### 第二步：生成比赛日志
```bash
python3 scripts/analyze_last_demo.py --username USERNAME [--match-index N] [--no-cache]
```
- 下载演示视频（文件大小通常在 50-300MB 之间），然后使用 `demoparser2` 工具对其进行解析。
- 输出一个简洁的文本日志，包含记分板和每轮的比赛时间线。
- 将解析结果缓存到 `matches/{match_id}.txt` 文件中（使用 `--no-cache` 选项可重新解析日志）。

### 第三步：分析日志

阅读完整的日志内容，并为指定玩家生成结构化的分析报告。
**在整个分析过程中请使用表情符号和美观的格式。**

**分析指南（结构、语气和内容要点）：**
- **结构：**
  1. **总体统计数据**：击杀/死亡比（K/D/A）、平均每分钟伤害（ADR）、伤害输出百分比（HS%）、多次击杀（KAST%）、关键击杀（clutches）。
  2. **角色评估**：确定玩家的角色（如进攻手、核心选手、支援者、潜伏者、狙击手、步枪手等），并评估其表现。
  3. **进攻方/防守方**：分析玩家在进攻和防守中的表现、位置选择、关键失误。
  4. **错误与失败**：指出具体的失误行为（如诱骗队友、送人头等），并附上时间戳。
  5. **亮点**：关键操作、关键击杀（附带时间戳）。
  6. **位置分析**：分析玩家经常占据的位置。如果玩家未能履行其角色职责，建议在网络上搜索相关攻略或视频（如 YouTube、Steam 社区或 CS2 官方网站）以获取指导。如果玩家表现完美，则可选性提供攻略。
  7. **建议**：给出具体且可执行的建议。
  8. **评分**：给出 1-10 分的评分。
- **语气与客观性**：保持中立和客观。不要美化糟糕的表现。需要强调的是，高统计数据（如高伤害输出百分比）如果对比赛结果没有实际影响，也应予以指出。
- **位置名称**：使用社区通用的名称来描述玩家位置（例如：Mid、Connector、Jungle、Short、Long、Tunnel 等）。

**在日志中需要注意的内容：**
- **击杀记录**：谁用何种武器杀死了谁，是否使用了闪光弹、烟雾弹等道具。
- **伤害记录**：双方的伤害交换情况。
- **闪光弹使用**：团队使用的闪光弹（标记为 `TEAM!`）以及敌方有效的闪光弹使用情况。
- **玩家位置**：每隔约 5 秒更新一次玩家的位置及其行动情况。
- **道具使用**：玩家使用的道具类型及购买情况。
- **比赛结果**：每轮的胜负情况以及关键击杀尝试。
- **半场数据**：用于宏观分析的半场得分情况。

### 可选选项
```bash
# Specific round deep-dive
python3 scripts/analyze_last_demo.py --username USERNAME --round N

# Older match (0=last, 1=previous, etc.)
python3 scripts/analyze_last_demo.py --username USERNAME --match-index 1

# Force re-parse (skip cache)
python3 scripts/analyze_last_demo.py --username USERNAME --no-cache
```

### 注意事项：内存限制
- 服务器内存为 2GB — 解析器已优化，但较大的演示视频可能导致内存不足。
- 经济数据按 4 轮为一组进行解析，每轮的位置信息通过 `gc.collect()` 方法获取。
- 如果出现内存不足的情况，建议关闭其他占用大量内存的程序后再运行程序。

## 工具管理

### 管理 Steam ID
```bash
# Save
python3 scripts/steam_ids.py save --username "jeminay" --steam-id "76561198185608989" --name "Дамир"

# Get
python3 scripts/steam_ids.py get --username "jeminay"

# List all
python3 scripts/steam_ids.py list
```

## 分析工作流程

1. **获取 Steam ID：`python3 scripts/steam_ids.py get --username USERNAME`
2. **运行演示视频解析器：`python3 scripts/analyze_last_demo.py --username USERNAME`
3. **阅读完整日志**：确定目标玩家的所属队伍、位置模式。
4. **查看队友信息**：通过 `scripts/steam_ids.py list` 文件交叉参考以识别其他玩家。
5. **逐轮分析**：记录玩家的击杀、死亡情况、道具使用情况以及位置信息。
6. **撰写分析报告**：使用俄语撰写结构化的分析报告（除非另有要求）。

**重要规则：**
- 当请求原始数据时，请按原样显示脚本输出结果。
- 在进行分析时，务必仔细阅读日志并撰写详细的分析报告。
- 始终注明具体的轮次和时间戳（例如：“第 5 轮 [45 秒]”）。
- **网络搜索建议**：如果玩家未能履行其角色职责或处于特定位置，使用 `web_search` 功能查找相关教程或位置攻略，并将其添加到分析报告中。
- 强调模式、趋势和战术错误，而不仅仅是孤立的事件。

## 配置

请设置环境变量 `LEETIFY_API_KEY`，并填写你的 Leetify API 密钥。
你可以在以下链接获取 API 密钥：https://api-public-docs.cs-prod.leetify.com/

## API 文档
文档链接：https://api-public-docs.cs-prod.leetify.com/