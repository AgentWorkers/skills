---
name: turing-pyramid
description: 10. 人工智能代理需要一个心理系统，该系统能够实现自动状态衰减、紧张情绪的计算以及基于概率的决策机制。该系统需要通过心跳信号来运行，以确保代理能够优先执行自我维护（即维护自身的状态和功能）。
---
# 图灵金字塔（Turing Pyramid）

10. 代理的心理健康需要一定的层次结构管理。该技能通过检测系统的心跳信号（heartbeat）来运行，并据此确定需要优先处理的行动。

## 快速入门

```bash
# Initialize (first time)
./scripts/init.sh

# Every heartbeat
./scripts/run-cycle.sh

# After completing an action
./scripts/mark-satisfied.sh <need> [impact]
```

## 这10个需求（The 10 Needs）

| 需求 | 重要性（Imp） | 衰减周期（Decay） | 含义（What it means） |
|------|-----|-------|---------------|
| 安全性（Security） | 10 | 168小时 | 系统稳定性，无安全威胁 |
| 完整性（Integrity） | 9 | 72小时 | 与`SOUL.md`中的策略保持一致 |
| 一致性（Coherence） | 8 | 24小时 | 内存数据的一致性 |
| 问题解决（Closure） | 7 | 8小时 | 所有未解决的问题都得到解决 |
| 自主性（Autonomy） | 6 | 24小时 | 能够自主决策和行动 |
| 社交互动（Connection） | 5 | 4小时 | 需要与他人进行社交交流 |
| 能力（Competence） | 4 | 48小时 | 能够有效地运用技能 |
| 理解力（Understanding） | 3 | 12小时 | 具有学习能力和好奇心 |
| 认可（Recognition） | 2 | 72小时 | 能够获得他人的认可 |
| 表达能力（Expression） | 1 | 6小时 | 具有创造性表达的能力 |

## 核心逻辑（Core Logic）

**满足度（Satisfaction）**: 0-3（0表示最不满足，3表示完全满足）

**紧张度（Tension）**: `重要性 × (3 - 满足度)`

**基于概率的决策机制**：
| 满足度 | 执行行动的概率（P(action）） | 发现问题的概率（P(notice） |
|-----|-----------------|-------------------|
| 3 | 5% | 95% |
| 2 | 20% | 80% |
| 1 | 75% | 25% |
| 0 | 100% | 0% |

- **行动（ACTION）**: 执行相应的操作，然后运行`mark-satisfied.sh`脚本。
- **发现问题（NOTICED）**: 记录问题，但暂不采取行动，满足度保持不变。

## 集成（Integration）

将该技能的配置添加到`HEARTBEAT.md`文件中：
```bash
~/.openclaw/workspace/skills/turing-pyramid/scripts/run-cycle.sh
```

## 输出示例（Output Example）

```
🔺 Turing Pyramid — Cycle at Mon Feb 23 04:01:19
======================================
Current tensions:
  security: tension=10 (sat=2, dep=1)
  integrity: tension=9 (sat=2, dep=1)

📋 Decisions:
▶ ACTION: security (tension=10, sat=2)
  Suggested:
  - run full backup + integrity check (impact: 3)
  - verify vault and core files (impact: 2)

○ NOTICED: integrity (tension=9, sat=2) — deferred

Summary: 1 action(s), 1 noticed
```

## 自定义设置（Customization）

- **衰减率（Decay rates）**: 修改`assets/needs-config.json`文件进行配置。
- **概率值（Probabilities）**: 修改`run-cycle.sh`文件中的`roll_action()`函数。
- **扫描任务（Scans）**: 添加或修改`scripts/scan_<need>.sh`脚本。

有关技术细节，请参阅`references/architecture.md`。

## 安全性与数据访问（Security & Data Access）

- **禁止网络请求**：所有扫描操作仅使用本地文件。
- **该技能会读取的数据**:
  - `MEMORY.md`：长期存储的数据
  - `memory/*.md`：每日日志（用于检测待办事项和模式）
  - `SOUL.md`, `AGENTS.md`：检查数据的一致性
  - `research/`：检查最近的活动记录
- **该技能会写入的数据**:
  - `assets/needs-state.json`：仅记录时间戳
  - `memory/YYYY-MM-DD.md`：记录执行的操作和发现的问题

**⚠️ 隐私提示：** 该技能会扫描您的工作区文件以检测某些关键词（如“confused”（困惑的）、“learned”（学到的）、“TODO”等）。在启用该技能之前，请先检查您的工作区内容。该技能可以查看您编写的内容。
- **该技能不会访问**：您的凭证信息、API密钥、网络资源以及工作区之外的文件。