---
name: lemnos-cost-guard
description: "OpenClaw代理的实时API成本跟踪、上下文冗余检测以及预算执行功能。这些功能可用于设置成本上限、检查每日支出、记录任务完成后令牌的使用情况、分析上下文冗余情况、生成成本报告（每日/每周/每月），以及在用户询问API成本、预算状态或成本为何较高的情况下提供帮助。"
---
# Lemnos Cost Guard

该工具用于监控token的使用情况、执行预算控制、检测代码中的冗余部分，并将任务路由到更经济的模型（即成本更低的模型）。

## 快速参考

| 脚本 | 功能 |
|--------|---------|
| `scripts/track_cost.py` | 在任务完成后记录成本支出 |
| `scripts/cost_report.py` | 生成成本汇总报告 |
| `scripts/context_analyzer.py` | 扫描代码工作区中的冗余部分 |

定价和模型路由规则请参考：`references/model_pricing.md`

## 工作流程

### 每次完成重要任务后
立即使用会话状态变化（`session_status`在任务前后）记录成本：

```bash
python3 skills/lemnos-cost-guard/scripts/track_cost.py \
  --task "email batch" \
  --input 45000 \
  --output 1200 \
  --model claude-sonnet-4-6
```

日志文件保存路径：`logs/cost-YYYY-MM-DD.jsonl`

### 每日简报 — 成本汇总
在发送晨间简报之前运行该脚本：

```bash
python3 skills/lemnos-cost-guard/scripts/cost_report.py --days 1 --budget 5.00 --format brief
```

将日志输出原封不动地包含在简报中。对于超出预算80%的情况，需要特别标注。

### 预算警报
- **每日成本超过5美元的80%** → 警告Nick，并暂停非盈利性任务
- **每日成本超过5美元的100%** → 立即停止相关任务，并通知Nick
- **单次调用消耗的输入token超过500K** → 立即发出警报
- **I/O比率超过50:1** → 发出代码冗余警告，建议进行代码优化

### 代码冗余检查（每周运行一次或当成本突然增加时运行）

```bash
python3 skills/lemnos-cost-guard/scripts/context_analyzer.py \
  --workspace /root/.openclaw/workspace
```

## 代码加载规则（在每次会话中强制执行）

仅加载当前任务所需的数据：

| 任务 | 需要加载的文件 |
|------|------|
| 晨间简报 | `SOUL.md`, `USER.md`, `MEMORY.md`, `HEARTBEAT.md`, 当天的内存使用情况 |
| 邮件推广 | `MEMORY.md`（仅限Lemnos相关内容），`sent-log.md` |
| LinkedIn调研 | 仅`sent-log.md` |
| 加密/市场分析 | 仅`MEMORY.md`（加密相关内容） |
| Heartbeat监控 | 仅`HEARTBEAT.md` |

除非任务有特殊要求，否则不要加载完整的`MEMORY.md`文件以及所有技能相关的文件和参考文件。

## 模型路由
详细规则请参见：`references/model_pricing.md`
- 简单任务（格式化、分类、状态检查） → 使用Haiku模型（每输入1个token费用0.80美元）
- 默认任务 → 使用Sonnet模型（每输入1个token费用3美元）
- 高级任务 → 除非特别请求，否则不使用Opus模型

## 成本日志格式
`logs/cost-YYYY-MM-DD.jsonl`文件中的每条记录都遵循以下格式：

```json
{
  "ts": "2026-02-24T18:00:00Z",
  "task": "email batch send",
  "model": "claude-sonnet-4-6",
  "input_tokens": 45000,
  "output_tokens": 1200,
  "ratio": 37.5,
  "cost_usd": 0.153,
  "notes": "batch 1 + batch 2"
}
```

## ClawHub服务功能

免费 tier：提供每日成本跟踪和预算警报功能
高级版（每月40-60美元）：提供完整的仪表盘、模型路由自动化功能以及代码优化报告，并提供每周/每月的成本汇总

技能文件名称：`lemnos-cost-guard.skill`