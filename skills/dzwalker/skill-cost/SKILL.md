---
name: skill-cost
version: 0.1.0
author: dzwalker
description: 从 OpenClaw 会话日志中跟踪每个技能的令牌使用情况和成本。当用户询问技能使用情况、哪些技能的成本最高，或者需要了解每个技能的具体成本明细时，可以使用此功能。**重要提示**：这是一个基于 Bash 工具的功能，因此必须使用 Bash 或 Shell 命令来执行相关操作。
triggers:
  - skill cost
  - skill spending
  - skill usage
  - which skill costs
  - per-skill cost
  - skill token
  - cost by skill
  - token by skill
  - skill breakdown
  - cost breakdown by skill
repository: https://github.com/dzwalker/skill-cost
license: MIT
dependencies: []
tools:
  - skill_cost_report
  - skill_cost_detail
  - skill_cost_compare
metadata: {"clawdbot":{"emoji":"💰","requires":{"anyBins":["python3","bash"]},"os":["linux","darwin","win32"]}}
---
# 技能成本 — 使用 `bash` 工具

**您必须使用 `bash` 或 `shell` 工具来运行这些命令。其他方法均不可行。**

## 命令

- 按技能划分的成本报告：
  ```bash
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh report
```

- 过去 7 天内的数据：
  ```bash
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh report --days 7
```

- 自特定日期以来的数据：
  ```bash
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh report --since 2026-03-01
```

- JSON 格式输出：
  ```bash
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh report --format json
```

- 成本最高的技能：
  ```bash
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh ranking
```

- 某个技能的详细信息：
  ```bash
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh detail poe-connector
```

- 比较两个技能的使用情况：
  ```bash
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh compare poe-connector web-search
```

## 禁止使用的方法

- **禁止使用 `sessions_spawn`** — 这会导致失败。
- **禁止使用浏览器** — 这也会导致失败。
- **禁止使用除 `bash` 工具之外的任何方法** — 只有 `bash` 才能正常工作。

## 工作原理

1. 扫描位于 `~/.openclaw/agents/*/sessions/` 目录下的 OpenClaw 会话 JSONL 文件。
2. 解析助手发送的消息，以确定工具调用和令牌的使用情况。
3. 根据 bash 命令路径和工具名称，将令牌的使用情况分配到相应的技能上。
4. 汇总各技能的成本，并提供按模型和日期划分的详细报告。

## 注意事项

- **无需 API 密钥** — 数据直接从本地会话文件中读取。
- **无需外部 Python 库**（仅依赖标准库 `stdlib`）。
- 技能归属的判断基于 bash 命令路径和 `SKILL.md` 文件中的工具映射关系。
- 多技能消息中的令牌会按比例分配到各个技能中。
- 无法归属于任何特定技能的令牌会被归类为 “内置功能” 或 “对话内容”。