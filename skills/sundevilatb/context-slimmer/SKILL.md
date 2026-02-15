---
name: context-slimmer
description: 审核并精简始终被加载的上下文文件（AGENTS.md、TOOLS.md、USER.md、MEMORY.md、HEARTBEAT.md、SOUL.md、IDENTITY.md）。在需要减少令牌使用量、审核上下文文件、优化上下文窗口或精简工作区文件时使用这些工具。这些工具可以测量当前的令牌成本，并确定哪些内容需要移动、删除或压缩。
---

# Context Slimmer

该工具用于审核工作区文件，减少这些文件在系统中占用的令牌（token）资源。

## 快速入门

```bash
# Measure current context cost
bash scripts/measure.sh

# Full audit (outputs recommendations)
bash scripts/measure.sh --audit
```

## 审核流程

对于每个始终被加载的文件，需执行以下操作：

1. **移至相关技能文件** — 将仅用于特定任务的内容（如投注配置、群聊规则、详细协议等）移至相应的技能文件或按需加载的参考文件中。
2. **删除** — 删除过时信息、已废弃的功能以及重复出现的文件内容。
3. **压缩** — 将冗长的描述压缩为简短的句子；如果代理已经了解相关内容，就直接省略这些描述。

## 经验法则：

- 如果某个任务由定时任务（cron job）处理，就将其从 `HEARTBEAT.md` 文件中删除。
- 如果某项内容已经存在于 `SOUL.md` 文件中，就不要在 `MEMORY.md` 或 `AGENTS.md` 中重复说明。
- 如果某项内容仅存在于 `USER.md` 文件中，也不要在 `MEMORY.md` 中重复说明。
- 如果代理每天都会执行某项操作，就不需要为其提供详细的说明，只需提供一个触发词即可。
- 优先使用简短的句子，而非冗长的列表形式来表达相同的内容。
- 目标是确保每个文件中的每一行内容都合理地占用令牌资源。

## 预期文件大小（理想目标）

| 文件名 | 预期令牌数（token） |
|------|--------|
| AGENTS.md | < 500 |
| TOOLS.md | < 500 |
| USER.md | < 700 |
| MEMORY.md | < 400 |
| HEARTBEAT.md | < 400 |
| SOUL.md | < 250 |
| IDENTITY.md | < 50 |
| **总计** | **< 2,800** |

## 输出格式

报告应包含当前文件大小、目标文件大小以及每项优化措施（移除、删除、压缩）所节省的令牌数量，并按类别进行分类展示。