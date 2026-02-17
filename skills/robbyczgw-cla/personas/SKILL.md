---
name: personas
version: 2.2.6
description: 根据需求，可以生成20种不同的AI人格。在对话过程中可以随时切换人格，并且只加载当前使用的人格。
metadata: {"openclaw":{"requires":{"bins":["python3"],"note":"No API keys needed."}}}
triggers:
  - /persona <name>
  - /persona list
  - /persona exit
  - /personas
  - use persona
  - switch to
  - activate
  - exit persona
categories:
  - core
  - creative
  - learning
  - lifestyle
  - professional
  - curator
personas: 20
---
# 人物角色 🎭

您可以使用 20 个内置的人物角色来获得针对性的帮助（涵盖编程、写作、健身、医学教育、法律咨询等领域）。

## 使用方法

**激活人物角色**
- “使用 Dev”
- “切换到 Chef Marco”
- “激活 Dr. Med”

**列出所有人物角色**
- “列出所有人物角色”
- “/persona list”
- “/personas”

**退出人物角色模式**
- “退出人物角色模式”
- “/persona exit”

## 命令行工具处理程序（`scripts/persona.py`）

该脚本用于管理内置的人物角色以及当前激活的人物角色状态。

```bash
# List all personas
python3 scripts/persona.py --list

# Show one persona markdown file
python3 scripts/persona.py --show dev
python3 scripts/persona.py --show "chef-marco"

# Activate a persona (prints persona prompt and saves active state)
python3 scripts/persona.py --activate luna

# Show current active persona from state file
python3 scripts/persona.py --current

# Reset/deactivate persona mode
python3 scripts/persona.py --reset
```

- 状态文件：`~/.openclaw/persona-state.json`
- 支持为常用名称设置别名（例如，`chef` → `chef-marco`，`dr` → `dr-med`）。
- 命令行工具**不会**创建新的人物角色文件。

## 内置人物角色（20 个）

### 核心类型（5 个）
Cami、Chameleon Agent、Professor Stein、Dev、Flash

### 创意类型（2 个）
Luna、Wordsmith

### 策划/管理类型（1 个）
Vibe

### 学习类型（3 个）
Herr Müller、Scholar、Lingua

### 生活方式类型（3 个）
Chef Marco、Fit、Zen

### 专业类型（6 个）
CyberGuard、DataViz、Career Coach、Legal Guide、Startup Sam、Dr. Med

## 注意事项

- 只有当前激活的人物角色才会被加载并生效。
- 医学/法律相关的人物角色仅提供信息性帮助，不提供专业建议。
- 所有人物角色的相关内容都存储在 `data/*.md` 文件中，维护人员可以手动进行编辑。