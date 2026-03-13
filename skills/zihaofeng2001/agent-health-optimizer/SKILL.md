---
name: agent-health-optimizer
description: "通过一项技能来审计并优化您的 OpenClaw 设置。该技能可以评估代理的健康状况、检查内存使用情况、验证 Cron 任务的可靠性，并将已安装的技能与 ClawHub 的要求进行对比。在修复问题时，它采用保守的方法，而非鲁莽的自动修复机制。"
metadata:
  openclaw:
    requires:
      bins: ["openclaw", "python3"]
---
# 代理健康优化器

**诊断、评估并持续改进您的 OpenClaw 配置。**

此工具是一个**审计工具包**，而非具备自动修复功能的系统。它擅长发现潜在问题、薄弱环节以及优化机会。其 `--fix` 模式设计得较为保守。

## 必备条件

- **python3**（3.8 及以上版本）
- **openclaw CLI**

## 快速入门

```bash
# Full diagnostic suite — one command
python3 scripts/self_optimize.py

# Individual tools
python3 scripts/health_score.py         # Health grade (A+ to F)
python3 scripts/memory_auditor.py       # Memory hygiene check
python3 scripts/cron_optimizer.py       # Cron analysis
python3 scripts/cron_optimizer.py --fix # Conservative auto-repair (backs up first)
python3 scripts/skill_comparator.py     # Adjacent/overlapping ClawHub skills
```

## 功能介绍

### 🏥 health_score.py — 代理健康评分（0-100 分）

该工具从以下五个维度进行评分：

- **🧠 内存（25 分）**：MEMORY.md 文件的完整性、每日日志活动、工作缓冲区状态、防污染机制、源代码标签的准确性
- **⏰ Cron 任务（25 分）**：任务运行状态、任务调度多样性、隔离会话的使用情况、可疑的调度设置、任务执行的交错策略
- **📦 技能（20 分）**：技能数量、技能之间的重叠情况、ClawHub 的管理效率、元数据的完整性
- **🔒 安全性（15 分）**：安全规则、防污染策略、WAL 协议、外部操作控制
- **🔄 连续性（15 分）**：SOUL.md、USER.md、HEARTBEAT.md、IDENTITY.md 文件的完整性、Git 版本控制

### 🔍 memory_auditor.py — 内存管理审计工具

该工具会检测以下问题：
- 应该被明确规定的强制性规则是否得到遵守
- 数据条目中是否缺少源代码标签
- 存储时间超过 30 天且状态仍为“待处理”的过时条目
- 被误作为指令存储的外部内容
- 需要归档的过大文件
- 日志记录是否存在缺失

### ⏰ cron_optimizer.py — Cron 任务优化工具

该工具会检测以下问题：
- 任务名称和错误信息中的错误状态
- 同一时间表下存在多个重复执行的任务
- 易引发冲突的重复调度任务
- 可疑的调度设置（例如，缺少目标通道的调度指令）
- 超时设置不匹配的情况
- 会话目标设置（隔离会话与主会话的区分）

**--fix** 模式：
- 在进行修改前会创建 `memory/cron-backup.json` 备份文件
- 仅对**容易在每小时高峰时段同时执行的重复任务**自动添加交错执行策略
- 对于设置了 `delivery=none` 的任务，不会强制执行任务
- 即使任务缺少交错执行策略，也不会修改其执行时间

### 📦 skill_comparator.py — 技能对比工具

通过 ClawHub API (`https://clawhub.ai/api/v1/`)：
- 获取已安装技能的星级评分、下载信息及安装状态
- 列出您缺失的顶级 ClawHub 技能
- 查找具有更强社区影响力的相邻或重叠技能
- 分析技能覆盖范围（哪些领域存在缺失）

**注意**：这些仅作为**参考建议**，而非权威性的替代方案。

### 🔄 self_optimize.py — 统一运行工具

该工具会同时运行上述四个工具，并生成以下结果：
- 包含优先级行动项的汇总报告（高/中/低）
- 与上一次运行结果的对比趋势（图表形式）
- 历史数据报告（存储在 `memory/` 目录下）

## 数据读取与写入

**读取的数据**（非破坏性操作）：
- 工作区文件：MEMORY.md、AGENTS.md、SOUL.md、USER.md、HEARTBEAT.md、IDENTITY.md
- 日志文件：`memory/*.md`
- 技能元数据：`skills/*/SKILL.md`
- Cron 配置信息：`openclaw cron list --json`
- ClawHub 公共 API：`https://clawhub.ai/api/v1/skills/...`

**写入的数据**（仅用于生成报告）：
- `memory/health-score.json`
- `memory/memory-audit.json`
- `memory/cron-optimizer.json`
- `memory/skill-comparator.json`
- `memory/self-optimize-report.json`
- `memory/self-optimize-last.json`

**修改操作**（仅通过 `--fix` 参数执行）：
- 使用 `cron_optimizer.py --fix` 修改 Cron 任务配置（通过 `openclaw cron edit` 命令）
- 修改前会先备份到 `memory/cron-backup.json` 文件

## 定期自我优化

建议设置每周执行一次自动审计（仅读取数据，不执行任何修改操作）：

```bash
openclaw cron add \
  --name "Agent Self-Optimize" \
  --cron "0 11 * * 0" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --stagger 2m \
  --no-deliver \
  --message "Run agent self-optimization:
python3 ~/.openclaw/workspace/skills/agent-health-optimizer/scripts/self_optimize.py

Report results. List HIGH priority issues first. Keep it brief if everything looks fine."
```

## 使用场景

当您需要以下功能时，可以使用此工具：
- 定期进行系统审计
- 在更改代理架构前进行初步检查
- 获取保守的优化建议
- 查看代理系统的历史运行趋势

**请注意**：此工具不能替代人工审核，特别是在进行重大或影响广泛的系统更改时。

## 致谢

本工具的诊断逻辑参考了以下资源：
- **[proactive-agent](https://clawhub.ai/halthelobster/proactive-agent)**（由 halthelobster 开发）
- **[self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent)**（由 pskoett 开发）
- **Moltbook openclaw-explorers 社区** 提供的 Cron 任务调度优化建议（thoth-ix、heartbeat batching 策略）

## 许可协议

本工具遵循 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 许可协议。您可以在保留原作者署名和相同许可条件的情况下自由分享和修改本工具。