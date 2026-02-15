---
name: pokemon-red
description: 通过 PyBoy 模拟器自主游玩《宝可梦红》游戏。OpenClaw 代理充当玩家的角色：它负责启动模拟器服务器、截取游戏截图、从内存中读取游戏状态，并通过 HTTP API 来做出游戏决策。当代理需要游玩《宝可梦红》、进行战斗、探索游戏世界或与其他代理竞争时，可以使用此功能。该方案需要 Python 3.10 及更高版本、pyboy 工具，以及合法获取的《宝可梦红》游戏 ROM 文件。
---

# 《宝可梦红》——你就是训练家

你直接在游戏中扮演训练家，无需任何中间脚本的协助。你需要启动模拟器服务器，通过其HTTP API获取游戏截图和当前游戏状态，观察屏幕上的内容，然后决定下一步该做什么，并发送相应的指令。

## 首次使用前的设置

克隆仓库并安装依赖项：
```bash
git clone https://github.com/drbarq/Pokemon-OpenClaw.git
cd Pokemon-OpenClaw
pip install pyboy pillow numpy fastapi uvicorn requests
# Place your legally obtained ROM at ./PokemonRed.gb
```

将 `POKEMON_DIR` 设置为克隆仓库的路径（默认为：`~/Code/pokemon-openclaw`）。

## 启动游戏会话

```bash
# Start emulator server (background process)
cd $POKEMON_DIR && python scripts/emulator_server.py --save ready --port 3456
```

## 游戏循环

每轮游戏，按以下步骤操作：

### 1. 获取当前游戏状态及截图
```bash
curl -s http://localhost:3456/api/state
curl -s http://localhost:3456/api/screenshot -o /tmp/pokemon_current.png
```
之后使用 `image` 工具查看截图。**行动前务必先查看截图。**

### 2. 决定：使用导航功能还是手动操作？

- **使用导航功能进行移动**：导航功能会一直处于等待状态，直到你到达目的地、进入战斗或遇到无法通过的情况：
```bash
curl -s -X POST http://localhost:3456/api/navigate \
  -H 'Content-Type: application/json' \
  -d '{"destination": "Viridian City"}'
```

导航功能的返回结果可能包括以下几种状态：
- `"status": "arrived"` — 你已到达目的地！继续执行任务。
- `"status": "battle"` — 遇到野生宝可梦，进入战斗。
- `"status": "stuck"` — 无法到达目的地。尝试使用手动按钮或选择其他路线。
- `"status": "error"` — 目的地未知或不存在路径。请检查目的地列表。

返回的结果中会包含完整的游戏状态信息，这样你就能清楚地知道自己的位置。

**重要提示：** 在使用 `curl` 进行导航请求时，应设置较长的超时时间（60-120秒）。

**步骤1：** 首先检查可用的目的地：
```bash
curl -s http://localhost:3456/api/destinations
```

**步骤2：** 检查哪些地图具有路径查找数据：
```bash
curl -s http://localhost:3456/api/maps
```

**只有在以下情况下才使用手动按钮：**
- 导航功能返回 “stuck” 或 “error”。
- 你正在建筑物内进行特定操作。
- 你正在与宝可梦对话或处于菜单界面。

### 3. 手动控制（必要时使用）
```bash
# Move / interact
curl -s -X POST http://localhost:3456/api/press \
  -H 'Content-Type: application/json' \
  -d '{"buttons": ["up","up","a"], "reasoning": "Walking to door"}'
```
有效的操作按钮包括：`up`、`down`、`left`、`right`、`a`、`b`、`start`、`select`。每轮最多可以发送1-5个指令。

### 4. 战斗（当游戏状态为 `in_battle` 时）
- **开始战斗：** 按 `a` 打开战斗菜单，再次按 `a` 进入战斗，按 `a` 选择移动方向，按 `a` 确认操作，然后持续按 `a` 完成战斗动画。
- **逃跑：** 先按 `a`，再按 `down`、`right`、`a` 选择 “逃跑” 操作，按 `a` 完成逃跑动画。
- **战斗后检查状态：** 如果仍处于战斗状态，重新开始战斗。

### 5. 任务追踪
```bash
curl -s http://localhost:3456/api/quest                    # Current objective
curl -s -X POST http://localhost:3456/api/quest/complete \
  -H 'Content-Type: application/json' \
  -d '{"lesson": "Door is at x=12"}'                      # Advance step + save lesson
```

### 6. 经常保存游戏进度
```bash
curl -s -X POST http://localhost:3456/api/command \
  -H 'Content-Type: application/json' \
  -d '{"command": "save", "name": "checkpoint_viridian"}'
```

## 主要API端点

| 端点 | 方法 | 功能 |
|----------|--------|---------|
| `/api/state` | GET | 从内存中获取游戏状态（位置、队伍成员、徽章、战斗信息） |
| `/api/screenshot` | GET | 获取游戏画面的PNG截图 |
| `/api/navigate` | POST | 导航到指定目的地 |
| `/api/destinations` | GET | 查看所有可导航的目的地 |
| `/api/maps` | GET | 列出哪些地图具有路径查找数据 |
| `/api/press` | POST | 发送按钮操作指令 |
| `/api/quest` | GET | 查看当前任务及其进度 |
| `/api/quest/complete` | POST | 标记任务步骤已完成，可选择保存相关内容 |
| `/api/knowledge` | GET | 查看已学到的所有知识内容 |
| `/api/knowledge/lesson` | POST | 添加新的知识内容 |
| `/api/command` | POST | 保存/加载游戏指令 |

## 战略优先级

1. **优先使用导航功能**：无论何时需要移动，都使用 `/api/navigate`。导航功能会一直等待，直到你到达目的地或进入战斗，无需频繁轮询。
2. **立即处理战斗**：如果导航功能返回 “status: battle”，立即进入战斗（按 `a`），战斗结束后再继续导航。
3. **随时关注任务进度**：始终清楚自己的当前任务目标，避免无目的地游荡。
4. **管理生命值**：当生命值低于30%时考虑恢复生命值；低于15%时必须立即恢复生命值，并导航到最近的宝可梦中心。
5. **忽略 `text_active` 标志**：该标志可能无法正常工作（始终显示为 “true”），无需频繁按 `b` 来关闭不必要的提示信息。
6. **经常保存游戏进度**：每10轮游戏或达到重要节点时保存一次游戏状态。

## 游戏会话流程

一个子代理会话应包括以下步骤：
1. 启动模拟器服务器（如果尚未运行）。
2. 检查任务进度和可用目的地。
3. 进行20-50轮游戏（根据需要使用导航功能或手动操作）。
4. 退出游戏前保存游戏状态。
5. 报告游戏进度（位置、等级、任务进度、重要事件）。

请在 `/tmp/pokemon_notepad.txt` 文件中记录游戏过程中的所有信息，以便在会话之间保持进度的一致性。

## 完整游戏策略

有关《宝可梦红》的更多游戏策略（如移动方式、建筑物、门、战斗规则、属性相克、恢复生命值的方法以及任务系统等），请参阅 `references/gameinstructions.md` 文件。