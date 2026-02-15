---
name: habitica
description: Habitica 游戏化习惯追踪器集成：可用于列出/创建/完成习惯任务、每日任务以及管理奖励。当用户触发“habitica”、“习惯”、“待办事项”或“日常任务”相关操作时，该集成会自动执行相应的任务检查或奖励发放逻辑。
---

# Habitica Skill

这是一个功能齐全的命令行工具（CLI），专为Habitica的 gamified 任务管理器设计。

## 设置

凭据存储在 `~/.habitica` 文件中：
```bash
HABITICA_USER_ID="your-user-id"
HABITICA_API_TOKEN="your-api-token"
```

获取方式：Habitica → 设置 → 网站数据 → 显示API令牌

## 命令

### 任务
```bash
./scripts/habitica.sh list [habits|dailys|todos|rewards|all]
./scripts/habitica.sh create <type> "text" ["notes"]
./scripts/habitica.sh score <task-id> [up|down]
./scripts/habitica.sh update <task-id> --text "new" --notes "new"
./scripts/habitica.sh delete <task-id>
```

### 用户与统计信息
```bash
./scripts/habitica.sh user          # Basic stats
./scripts/habitica.sh stats         # Full stats (STR/INT/CON/PER)
```

### 收藏夹
```bash
./scripts/habitica.sh pets          # Your pets
./scripts/habitica.sh mounts        # Your mounts
./scripts/habitica.sh achievements  # Achievement list
./scripts/habitica.sh inventory     # Eggs, potions, food, quest scrolls
```

### 团队与社交功能
```bash
./scripts/habitica.sh party         # Party info + chat
./scripts/habitica.sh party-chat 10 # Last N messages
./scripts/habitica.sh party-send "message"
./scripts/habitica.sh guilds        # Guild list
```

### 技能（角色能力）
```bash
./scripts/habitica.sh skills        # List available skills
./scripts/habitica.sh cast <skill> [taskId]
```

**盗贼（Rogue）：** pickPocket（扒窃）、backStab（暗杀）、toolsOfTrade（交易工具）、stealth（潜行）
**战士（Warrior）：** smash（猛击）、defensiveStance（防御姿态）、valorousPresence（英勇表现）、intimidate（恐吓）
**法师（Mage）：** fireball（火球术）、mpheal（恢复魔法值）、earth（土系法术）、frost（冰系法术）
**治疗者（Healer）：** heal（治疗）、healAll（全体治疗）、protectAura（保护光环）、brightness（增益效果）

### 任务（Quest）
```bash
./scripts/habitica.sh quest         # Current quest status
./scripts/habitica.sh quest-accept  # Check and accept pending quest invitations
```

### 其他功能
```bash
./scripts/habitica.sh history [exp|todos]
./scripts/habitica.sh cron          # Force new day
```

## 注意事项

- 日常任务使用 `dailys`（Habitica官方的拼写）
- 任务ID来源于 `list` 命令的输出结果
- 自动调用API的频率限制：每30秒一次

## 背景执行（子代理）

对于批量操作（例如同时处理多个任务）或耗时较长的操作，可以启动一个子代理来保持主聊天界面的响应性。

**提示模式：**
```text
Task: Habitica Batch Operation
- Score task 123 (up)
- Score task 456 (up)
- Create todo "New Task"
Report back briefly when done.
```

**使用场景：**
- 用户需要同时完成多个任务
- 用户需要获取需要多次API调用的任务汇总或分析结果（例如：“检查我所有的任务并告诉我该怎么做”）
- 当网络延迟较高时