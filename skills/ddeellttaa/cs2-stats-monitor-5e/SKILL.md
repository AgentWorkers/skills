---
name: cs-stats-monitor-generic
description: 5E CS2 Stats Query and Real-time Monitor. Supports custom player lists, query specified players' CS2 match history, analyze match performance, and real-time monitoring for new matches. Keywords: CS stats, 5E, check stats, monitor matches, CS2 stats, match report.
---

# CS Stats Monitor（通用版）

这是一个用于查询5E平台CS2比赛数据并进行实时监控的工具（通用版本）。

## 核心功能

### 1. 数据查询
可以查询指定玩家在过去5场比赛中的详细数据。

```bash
# Query single player's last 5 matches
python {SKILL_DIR}/scripts/cs_monitor.py --once --players <player_name>

# Query multiple players
python {SKILL_DIR}/scripts/cs_monitor.py --once --players player1 player2 player3

# Use default player list (set in config)
python {SKILL_DIR}/scripts/cs_monitor.py --once
```

### 2. 实时监控
工具会持续在后台进行数据轮询，并在新比赛开始时自动生成报告。

```bash
# Start monitoring (default 60s polling)
python {SKILL_DIR}/scripts/cs_monitor.py --players player1 player2

# Custom polling interval
python {SKILL_DIR}/scripts/cs_monitor.py --players player1 --interval 30

# Reset monitoring state
python {SKILL_DIR}/scripts/cs_monitor.py --reset
```

**使用方法**：使用`tmux`在后台运行该工具，并定期查看输出结果。

```bash
# Recommended: tmux background run
tmux new-session -d -s cs-monitor
tmux send-keys -t cs-monitor "python {SKILL_DIR}/scripts/cs_monitor.py --players player1 player2" Enter

# Check output
tmux capture-pane -t cs-monitor -p
```

### 3. 配置文件（可选）
创建`{SKILL_DIR}/config.json`文件来设置默认监控的玩家列表：

```json
{
  "default_players": ["player1", "player2", "player3"],
  "default_interval": 60
}
```

## 数据统计内容

**每场比赛的数据包括**：
- **核心指标**：评分（Rating）、每分钟击杀数（ADR）、关键击杀数（KAST）、每分钟死亡数（RWS）、击杀/死亡比（K/D/A）
- **击杀细节**：爆头率、首次击杀、首次死亡、使用AWP击杀的次数、多杀（3K/4K/5K）
- **关键决策时刻（Clutches）**：1v1至1v5战斗中的胜负情况
- **辅助操作**：使用闪光弹的次数、团队协作情况、辅助伤害、放置/拆除炸弹的次数
- **双方数据**：T方/CT方的击杀/死亡数及评分
- **计分板**：完整10名玩家的数据统计

**限制**：
- API仅返回最近5场比赛的数据，无法获取更早的比赛记录
- 查看赛季概览需要登录凭证（Cookie）

## 分析指南

在查看比赛报告时，请从以下维度进行分析：
1. **核心数据评分**：评分大于1.3表示表现优异，1.0-1.3表示表现正常，小于0.85表示表现较差；每分钟击杀数大于90表示实力强劲，60-90表示表现一般，小于60表示实力较弱
2. **战斗风格**：使用AWP的击杀比例、爆头率、首次击杀/死亡的比例，以及T方与CT方的差异
3. **稳定性**：多场比赛中评分的波动情况（标准差），以及最高分与最低分之间的差距
4. **团队贡献**：参与比赛的程度（KAST）、辅助操作的使用情况，以及在关键时刻的决策能力
5. **如果有多名玩家参与同一场比赛**：进行横向比较，找出表现突出和表现不佳的玩家

**语言风格**：直接、简洁，带有一些幽默元素。表现好的地方给予表扬，表现差的地方会进行批评。

## 所需依赖库/工具**
- Python 3.10及以上版本
- `aiohttp`（通过`pip install aiohttp`安装）

## 资源文件
### 脚本文件
- `cs_monitor.py`：主要的监控脚本，支持一次性查询和持续监控两种模式