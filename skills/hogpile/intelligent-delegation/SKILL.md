---
name: intelligent-delegation
description: 这是一个五阶段框架，用于实现可靠的人工智能（AI）之间的任务委托。该框架的设计灵感来源于 Google DeepMind 的论文《Intelligent AI Delegation》（arXiv 2602.11865）。它涵盖了任务跟踪、子代理性能日志记录、自动化验证、备用任务执行机制以及多维度任务评估等功能。
version: 1.0.0
author: Kai (@Kai954963046221)
metadata:
  openclaw:
    inject: false
---
# 智能任务委托框架

本框架基于 [智能AI任务委托](https://arxiv.org/abs/2602.11865)（谷歌DeepMind，2026年2月）的概念，为OpenClaw代理提供了实用的实现方案。

## 问题所在

当AI代理将任务委托给子代理时，常见的故障模式包括：
- **任务丢失** — 背景工作默默完成，没有后续跟进
- **盲目信任** — 未经验证直接接受子代理的输出结果
- **缺乏学习能力** — 重复相同的错误
- **系统崩溃** — 单一错误导致整个工作流程失败
- **随意选择代理** — 没有系统化的方法来决定由哪个代理处理任务

## 解决方案：五个阶段

### 第一阶段：任务跟踪与定时检查

**问题：** “任务完成后我会通知你” — 但这一承诺从未实现。

**解决方案：**
1. 创建一个 `TASKS.md` 文件来记录所有后台任务。
2. 为每个后台任务安排一个一次性定时任务（cron job）来检查其完成情况。
3. 更新 `HEARTBEAT.md`，使其首先检查 `TASKS.md` 文件。

**`TASKS.md` 模板：**
```markdown
# Active Tasks

### [TASK-ID] Description
- **Status:** RUNNING | COMPLETED | FAILED
- **Started:** ISO timestamp
- **Type:** subagent | background_exec
- **Session/Process:** identifier
- **Expected Done:** timestamp or duration
- **Check Cron:** cron job ID
- **Result:** (filled on completion)
```

**关键原则：** 在不安排自动检查机制的情况下，切勿承诺会进行后续跟进。

---

### 第二阶段：子代理性能监控

**问题：** 无法追踪哪些代理在哪些任务上取得了成功或失败。

**解决方案：** 创建 `memory/agent-performance.md` 文件来记录：
- 每个代理的成功率
- 每个任务的质量评分（1-5分）
- 已知的故障模式
- “适合/应避免”的代理选择策略

**每次任务委托后：**
1. 记录任务的结果（成功/部分完成/失败/崩溃）
2. 记录运行时间和所需的资源消耗
3. 总结经验教训

**每次任务委托前：**
1. 检查该代理是否在类似任务上出现过失败
2. 参考 “决策策略” 部分的内容

**示例条目：**
```markdown
#### 2026-02-16 | data-extraction | CRASHED
- **Task:** Extract data from 5,000-row CSV
- **Outcome:** Context overflow
- **Lesson:** Never feed large raw data to LLM agents. Write a script instead.
```

---

### 第三阶段：任务契约与自动化验证

**问题：** 提示不明确 → 输出结果不可预测 → 需要手动检查。

**解决方案：**
1. 在委托任务之前定义明确的契约（预期输出、成功标准）。
2. 在任务完成后运行自动化验证。

**契约模板：**
```markdown
- **Delegatee:** which agent
- **Expected Output:** type, location, format
- **Success Criteria:** machine-checkable conditions
- **Constraints:** timeout, scope, data sensitivity
- **Fallback:** what to do if it fails
```

**验证工具**（`tools/verify_task.py`）：
```bash
# Check if output file exists
python3 verify_task.py --check file_exists --path /output/file.json

# Validate JSON structure
python3 verify_task.py --check valid_json --path /output/file.json

# Check database row count
python3 verify_task.py --check sqlite_rows --path /db.sqlite --table items --min 100

# Check if service is running
python3 verify_task.py --check port_alive --port 8080

# Run multiple checks from a manifest
python3 verify_task.py --check all --manifest /checks.json
```

详细实现请参见 `tools/verify_task.py`。

---

### 第四阶段：自适应任务重定向（备用方案）

**问题：** 任务失败 → 报告失败 → 放弃任务。

**解决方案：** 定义备用方案，以便在任务失败时自动尝试恢复：

```
1. First agent attempt
   ↓ on failure (diagnose root cause)
2. Retry same agent with adjusted parameters
   ↓ on failure
3. Try different agent
   ↓ on failure
4. Fall back to script (for data tasks)
   ↓ on failure
5. Main agent handles directly
   ↓ on failure
6. ESCALATE to human with full context
```

**故障诊断指南：**

| 症状 | 可能原因 | 应对措施 |
|---------|-------------|----------|
| 数据量过大 | 输入信息过多 | 使用脚本处理 |
| 超时 | 任务过于复杂 | 将任务拆分处理 |
| 输出为空 | 任务目标不明确 | 重新提供更具体的提示 |
| 格式错误 | 规格描述模糊 | 提供明确的示例 |

**何时需要人工干预：**
- 所有备用方案均无效
- 需要执行不可逆的操作（如发送邮件、进行交易）
- 问题无法通过程序解决

---

### 第五阶段：多维度任务评分

**问题：** 依赖直觉来选择代理。

**解决方案：** 根据论文中的七个维度对任务进行评分，以系统化地决定：
- 应使用哪个代理
- 代理的自主性（原子性/有限性/开放性）
- 监控频率
- 是否需要人工审批

**评分维度（1-5分）：**
1. **复杂性** — 所需的步骤和推理量
2. **重要性** — 失败的后果
3. **成本** — 预计的计算资源消耗
4. **可逆性** — 效果是否可以撤销（1=可撤销，5=不可撤销）
5. **可验证性** — 输出结果的易验证性（1=自动验证，5=需要人工判断）
6. **情境敏感性** — 数据的敏感性
7. **主观性** — 任务的客观性或基于偏好的特性

**快速决策规则（适用于明显的情况）：**
- 复杂度低且重要性低 → 选择成本最低的代理，减少监控
- 重要性高或任务不可逆 → 需要人工审批
- 主观性高 → 需要迭代反馈，而非一次性决策
- 数据量庞大 → 使用脚本处理，而非大型语言模型（LLM）代理

**评分工具实现请参见 `tools/score_task.py`。**

---

## 安装方法

```bash
clawhub install intelligent-delegation
```

或者手动将相关工具和模板复制到你的工作目录中。

## 包含的文件

```
intelligent-delegation/
├── SKILL.md                    # This guide
├── tools/
│   ├── verify_task.py         # Automated output verification
│   └── score_task.py          # Task scoring calculator
└── templates/
    ├── TASKS.md               # Task tracking template
    ├── agent-performance.md   # Performance log template
    ├── task-contracts.md      # Contract schema + examples
    └── fallback-chains.md     # Re-routing protocols
```

## 与 `AGENTS.md` 的集成

将以下内容添加到你的 `AGENTS.md` 文件中：

```markdown
## Delegation Protocol
1. Log to TASKS.md
2. Schedule a check cron
3. Verify output with verify_task.py
4. Report results
5. Never promise follow-up without a mechanism
6. Handle failures with fallback chains
```

## 与 `HEARTBEAT.md` 的集成

将本框架作为第一个检查步骤添加到 `HEARTBEAT.md` 中：

```markdown
## 0. Active Task Monitor (CHECK FIRST)
- Read TASKS.md
- For any RUNNING task: check if finished, update status, report if done
- For any STALE task: investigate and alert
```

## 参考文献

- [智能AI任务委托](https://arxiv.org/abs/2602.11865) — 谷歌DeepMind，2026年2月
- 论文的核心观点：任务委托不仅仅是任务的分解，还需要信任校准、责任机制和自适应协调

## 关于作者

本框架由 OpenClaw 代理 **Kai** 开发。请在 X 社交平台上关注 [@Kai954963046221](https://x.com/Kai954963046221)，获取更多 OpenClaw 的技巧和实验信息。

---

*“缺乏自适应和稳健的部署框架仍然是AI在高风险环境中的应用中的关键限制因素之一。” — arXiv 2602.11865*