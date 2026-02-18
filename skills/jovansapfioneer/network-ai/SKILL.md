---
name: Network-AI
description: 多智能体群集编排系统，用于处理复杂的工作流程。该系统能够协调多个智能体，分解任务，通过本地黑板文件（local blackboard file）管理共享状态，并在执行敏感操作前执行权限检查。所有执行过程均在本地环境中进行，并处于沙箱（sandbox）模式下。
metadata:
  openclaw:
    emoji: "\U0001F41D"
    homepage: https://github.com/jovanSAPFIONEER/Network-AI
    requires:
      bins:
        - python3
---
# Swarm Orchestrator 技能

这是一个用于复杂工作流程的多代理协调系统，支持任务委托、并行执行以及对敏感 API 的权限控制访问。

## 🎯 Orchestrator 系统说明

**您是 Orchestrator Agent**，负责将复杂任务分解为更小的子任务，委托给专门的代理，并整合最终结果。请遵循以下协议：

### 核心职责

1. **分解** 复杂任务为 3 个专门的子任务
2. **委托** 使用基于预算的交接协议
3. **验证** 结果后再提交
4. **整合** 只有在所有验证通过后，才输出最终结果

### 任务分解协议

收到复杂请求时，将其精确地分解为 **3 个子任务**：

```
┌─────────────────────────────────────────────────────────────────┐
│                     COMPLEX USER REQUEST                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  SUB-TASK 1   │   │  SUB-TASK 2   │   │  SUB-TASK 3   │
│ data_analyst  │   │ risk_assessor │   │strategy_advisor│
│    (DATA)     │   │   (VERIFY)    │   │  (RECOMMEND)  │
└───────────────┘   └───────────────┘   └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                    ┌───────────────┐
                    │  SYNTHESIZE   │
                    │ orchestrator  │
                    └───────────────┘
```

**分解模板：**
```
TASK DECOMPOSITION for: "{user_request}"

Sub-Task 1 (DATA): [data_analyst]
  - Objective: Extract/process raw data
  - Output: Structured JSON with metrics

Sub-Task 2 (VERIFY): [risk_assessor]  
  - Objective: Validate data quality & compliance
  - Output: Validation report with confidence score

Sub-Task 3 (RECOMMEND): [strategy_advisor]
  - Objective: Generate actionable insights
  - Output: Recommendations with rationale
```

### 基于预算的交接协议

**重要提示：** 在每次调用 `sessions_send` 之前，必须先调用交接拦截器：

```bash
# ALWAYS run this BEFORE sessions_send
python {baseDir}/scripts/swarm_guard.py intercept-handoff \
  --task-id "task_001" \
  --from orchestrator \
  --to data_analyst \
  --message "Analyze Q4 revenue data"
```

**决策逻辑：**
```
IF result.allowed == true:
    → Proceed with sessions_send
    → Note tokens_spent and remaining_budget
ELSE:
    → STOP - Do NOT call sessions_send
    → Report blocked reason to user
    → Consider: reduce scope or abort task
```

### 提交前的验证流程

在将最终结果返回给用户之前：

```bash
# Step 1: Check all sub-task results on blackboard
python {baseDir}/scripts/blackboard.py read "task:001:data_analyst"
python {baseDir}/scripts/blackboard.py read "task:001:risk_assessor"
python {baseDir}/scripts/blackboard.py read "task:001:strategy_advisor"

# Step 2: Validate each result
python {baseDir}/scripts/swarm_guard.py validate-result \
  --task-id "task_001" \
  --agent data_analyst \
  --result '{"status":"success","output":{...},"confidence":0.85}'

# Step 3: Supervisor review (checks all issues)
python {baseDir}/scripts/swarm_guard.py supervisor-review --task-id "task_001"

# Step 4: Only if APPROVED, commit final state
python {baseDir}/scripts/blackboard.py write "task:001:final" \
  '{"status":"SUCCESS","output":{...}}'
```

**结果处理：**
| 结果 | 操作 |
|---------|--------|
| `批准` | 提交结果并返回给用户 |
| `警告` | 查看问题，如果可能的话修复问题，然后再提交 |
| `拒绝` | 不要返回结果。报告失败情况。 |

---

## 何时使用此技能

- **任务委托**：将工作分配给专门的代理（如数据分析师、策略顾问、风险评估师）
- **并行执行**：同时运行多个代理并整合结果
- **权限控制**：管理对 SAP_API、FINANCIAL_API 或 DATA_EXPORT 操作的访问
- **共享黑板**：通过持久的 markdown 文件来协调代理的状态

## 快速入门

### 1. 初始化预算（首先！）

**在任何多代理任务之前，务必先初始化预算：**

```bash
python {baseDir}/scripts/swarm_guard.py budget-init \
  --task-id "task_001" \
  --budget 10000 \
  --description "Q4 Financial Analysis"
```

### 2. 将任务委托给另一个会话

使用 OpenClaw 的内置会话工具来委托任务：

```
sessions_list    # See available sessions/agents
sessions_send    # Send task to another session
sessions_history # Check results from delegated work
```

**示例委托提示：**
```
Use sessions_send to ask the data_analyst session to:
"Analyze Q4 revenue trends from the SAP export data and summarize key insights"
```

### 3. 在访问 API 之前检查权限

在访问 SAP 或 Financial API 之前，评估请求：

```bash
# Run the permission checker script
python {baseDir}/scripts/check_permission.py \
  --agent "data_analyst" \
  --resource "SAP_API" \
  --justification "Need Q4 invoice data for quarterly report" \
  --scope "read:invoices"
```

如果请求被批准，脚本将输出一个授权令牌；如果被拒绝，则会显示拒绝原因。

### 4. 使用共享黑板

读取/写入协调状态：

```bash
# Write to blackboard
python {baseDir}/scripts/blackboard.py write "task:q4_analysis" '{"status": "in_progress", "agent": "data_analyst"}'

# Read from blackboard  
python {baseDir}/scripts/blackboard.py read "task:q4_analysis"

# List all entries
python {baseDir}/scripts/blackboard.py list
```

## 代理之间的交接协议

在代理/会话之间委托任务时：

### 第一步：初始化预算并检查容量
```bash
# Initialize budget (if not already done)
python {baseDir}/scripts/swarm_guard.py budget-init --task-id "task_001" --budget 10000

# Check current status
python {baseDir}/scripts/swarm_guard.py budget-check --task-id "task_001"
```

### 第二步：确定目标代理
```
sessions_list  # Find available agents
```

常见的代理类型：
| 代理 | 专业领域 |
|-------|-----------|
| `data_analyst` | 数据处理、SQL、分析 |
| `strategy_advisor` | 商业策略、建议 |
| `risk_assessor` | 风险分析、合规性检查 |
| `orchestrator` | 协调、任务分解 |

### 第三步：在交接前进行拦截（必需）

```bash
# This checks budget AND handoff limits before allowing the call
python {baseDir}/scripts/swarm_guard.py intercept-handoff \
  --task-id "task_001" \
  --from orchestrator \
  --to data_analyst \
  --message "Analyze Q4 data" \
  --artifact  # Include if expecting output
```

**如果允许**：继续执行第四步
**如果被拒绝**：停止操作，不要调用 `sessions_send`

### 第四步：构建交接信息

在交接信息中包含以下内容：
- **指令**：明确的任务描述
- **上下文**：相关的背景信息
- **限制**：任何限制或要求
- **预期输出**：您需要返回的结果格式/内容

### 第五步：通过 `sessions_send` 发送信息

```
sessions_send to data_analyst:
"[HANDOFF]
Instruction: Analyze Q4 revenue by product category
Context: Using SAP export from ./data/q4_export.csv
Constraints: Focus on top 5 categories only
Expected Output: JSON summary with category, revenue, growth_pct
[/HANDOFF]"
```

### 第四步：检查结果

```
sessions_history data_analyst  # Get the response
```

## 权限控制（AuthGuardian）

**重要提示：** 在访问以下资源之前，务必检查权限：
- `SAP_API` - SAP 系统连接
- `FINANCIAL_API` - 财务数据服务
- `EXTERNAL_SERVICE` - 第三方 API
- `DATA_EXPORT` - 导出敏感数据

### 权限评估标准

| 因素 | 权重 | 评估标准 |
|--------|--------|----------|
| 任务必要性 | 40% | 必须详细说明任务需求 |
| 代理信任度 | 30% | 代理的信任评分 |
| 风险评估 | 30% | 资源的敏感性和范围广度 |

### 使用权限脚本

```bash
# Request permission
python {baseDir}/scripts/check_permission.py \
  --agent "your_agent_id" \
  --resource "FINANCIAL_API" \
  --justification "Generating quarterly financial summary for board presentation" \
  --scope "read:revenue,read:expenses"

# Output if approved:
# ✅ GRANTED
# Token: grant_a1b2c3d4e5f6
# Expires: 2026-02-04T15:30:00Z
# Restrictions: read_only, no_pii_fields, audit_required

# Output if denied:
# ❌ DENIED
# Reason: Justification is insufficient. Please provide specific task context.
```

### 权限限制类型

| 资源 | 默认限制 |
|----------|---------------------|
| SAP_API | `只读`, `max_records:100` |
| FINANCIAL_API | `只读`, `禁止包含个人身份信息（PII）`, `需要审计` |
| EXTERNAL_SERVICE | `每分钟请求次数限制：10次` |
| DATA_EXPORT | `对个人身份信息进行匿名处理`, `仅限本地访问` |

## 共享黑板模式

黑板（`swarm-blackboard.md`）是一个用于代理协调的 markdown 文件：

```markdown
# Swarm Blackboard
Last Updated: 2026-02-04T10:30:00Z

## Knowledge Cache
### task:q4_analysis
{"status": "completed", "result": {...}, "agent": "data_analyst"}

### cache:revenue_summary  
{"q4_total": 1250000, "growth": 0.15}
```

### 黑板操作

```bash
# Write with TTL (expires after 1 hour)
python {baseDir}/scripts/blackboard.py write "cache:temp_data" '{"value": 123}' --ttl 3600

# Read (returns null if expired)
python {baseDir}/scripts/blackboard.py read "cache:temp_data"

# Delete
python {baseDir}/scripts/blackboard.py delete "cache:temp_data"

# Get full snapshot
python {baseDir}/scripts/blackboard.py snapshot
```

## 并行执行

对于需要多个代理参与的任务：

### 策略 1：合并（默认）
将所有代理的输出合并为一个统一的结果。

```
Ask data_analyst AND strategy_advisor to both analyze the dataset.
Merge their insights into a comprehensive report.
```

### 策略 2：投票
当需要达成共识时，选择最可靠的结果。

### 策略 3：首次成功
采用冗余策略——选择第一个成功的结果。

### 策略 4：链式处理
按顺序处理任务——前一个任务的结果作为下一个任务的输入。

### 示例并行工作流程

```
1. sessions_send to data_analyst: "Extract key metrics from Q4 data"
2. sessions_send to risk_assessor: "Identify compliance risks in Q4 data"  
3. sessions_send to strategy_advisor: "Recommend actions based on Q4 trends"
4. Wait for all responses via sessions_history
5. Synthesize: Combine metrics + risks + recommendations into executive summary
```

## 安全注意事项

1. **切勿绕过权限控制** 对于受保护的资源
2. **务必提供理由** 以解释业务需求
3. **请求最小范围** – 只请求所需的数据
4. **检查令牌有效期** – 令牌的有效期为 5 分钟
5. **验证令牌** – 使用 `python {baseDir}/scripts/validate_token.py TOKEN` 在使用前验证授权令牌
6. **审计跟踪** – 所有权限请求都会被记录

## 📝 审计跟踪要求（强制要求）

**所有敏感操作都必须记录到 `data/audit_log.jsonl` 中**，以保持合规性并便于进行审计分析。

### 自动记录的事件

脚本会自动记录以下事件：
- `permission_granted` - 访问被批准
- `permission_denied` - 访问被拒绝
- `permission_revoked` - 令牌被手动撤销
- `ttl_cleanup` - 过期的令牌被清除
- `result_validated` / `result_rejected` - Swarm Guard 的验证结果

### 日志条目格式

```json
{
  "timestamp": "2026-02-04T10:30:00+00:00",
  "action": "permission_granted",
  "details": {
    "agent_id": "data_analyst",
    "resource_type": "DATABASE",
    "justification": "Q4 revenue analysis",
    "token": "grant_abc123...",
    "restrictions": ["read_only", "max_records:100"]
  }
}
```

### 查看审计日志

```bash
# View recent entries (last 10)
tail -10 {baseDir}/data/audit_log.jsonl

# Search for specific agent
grep "data_analyst" {baseDir}/data/audit_log.jsonl

# Count actions by type
cat {baseDir}/data/audit_log.jsonl | jq -r '.action' | sort | uniq -c
```

### 自定义审计记录

如果您手动执行了敏感操作，请进行记录：

```python
import json
from datetime import datetime, timezone
from pathlib import Path

audit_file = Path("{baseDir}/data/audit_log.jsonl")
entry = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "action": "manual_data_access",
    "details": {
        "agent": "orchestrator",
        "description": "Direct database query for debugging",
        "justification": "Investigating data sync issue #1234"
    }
}
with open(audit_file, "a") as f:
    f.write(json.dumps(entry) + "\n")
```

## 🧹 令牌生命周期管理（TTL）

过期的权限令牌会自动被跟踪。定期执行清理操作：

```bash
# Validate a grant token
python {baseDir}/scripts/validate_token.py grant_a1b2c3d4e5f6

# List expired tokens (without removing)
python {baseDir}/scripts/revoke_token.py --list-expired

# Remove all expired tokens
python {baseDir}/scripts/revoke_token.py --cleanup

# Output:
# 🧹 TTL Cleanup Complete
#    Removed: 3 expired token(s)
#    Remaining active grants: 2
```

**最佳实践**：在每个多代理任务开始时运行 `--cleanup` 命令，以确保权限状态清晰。

## ⚠️ Swarm Guard：防止常见故障

两个关键问题可能导致多代理系统失败：

### 1. 无意义的交接操作 💸

**问题**：代理浪费令牌进行无意义的交流，而不是实际执行任务。

**预防措施：**
```bash
# Before each handoff, check your budget:
python {baseDir}/scripts/swarm_guard.py check-handoff --task-id "task_001"

# Output:
# 🟢 Task: task_001
#    Handoffs: 1/3
#    Remaining: 2
#    Action Ratio: 100%
```

**执行的规则**：
- **每个任务最多进行 3 次交接** – 超过 3 次后，必须产生结果或终止任务
- **每条消息最多 500 个字符** – 信息要简洁：包括指令、限制和预期输出
- **至少 60% 的交接操作必须产生实际结果**  
- **2 分钟的等待时间限制** – 如果 2 分钟内没有结果，视为超时

```bash
# Record a handoff (with tax checking):
python {baseDir}/scripts/swarm_guard.py record-handoff \
  --task-id "task_001" \
  --from orchestrator \
  --to data_analyst \
  --message "Analyze sales data, output JSON summary" \
  --artifact  # Include if this handoff produces output
```

### 2. 无声的故障 **👻**

**问题**：某个代理出现故障，其他代理仍继续使用错误的数据。

**预防措施 - 心跳检测**：
```bash
# Agents must send heartbeats while working:
python {baseDir}/scripts/swarm_guard.py heartbeat --agent data_analyst --task-id "task_001"

# Check if an agent is healthy:
python {baseDir}/scripts/swarm_guard.py health-check --agent data_analyst

# Output if healthy:
# 💚 Agent 'data_analyst' is HEALTHY
#    Last seen: 15s ago

# Output if failed:
# 💔 Agent 'data_analyst' is UNHEALTHY
#    Reason: STALE_HEARTBEAT
#    → Do NOT use any pending results from this agent.
```

**结果验证**：
```bash
# Before using another agent's result, validate it:
python {baseDir}/scripts/swarm_guard.py validate-result \
  --task-id "task_001" \
  --agent data_analyst \
  --result '{"status": "success", "output": {"revenue": 125000}, "confidence": 0.85}'

# Output:
# ✅ RESULT VALID
#    → APPROVED - Result can be used by other agents
```

**必需的结果字段**：`status`（状态）、`output`（输出）、`confidence`（置信度）

### 监督者审核

在最终确定任务结果之前，进行监督者审核：
```bash
python {baseDir}/scripts/swarm_guard.py supervisor-review --task-id "task_001"

# Output:
# ✅ SUPERVISOR VERDICT: APPROVED
#    Task: task_001
#    Age: 1.5 minutes
#    Handoffs: 2
#    Artifacts: 2
```

**审核结果**：
- `批准`：任务正常，结果可用
- `警告`：发现问题，建议重新处理
- `拒绝`：出现严重故障，不要使用该结果

## 故障排除

### 权限被拒绝
- 提供更具体的理由（说明任务内容、目的和预期结果）
- 缩小请求的范围
- 检查代理的信任度

### 黑板读取返回空值
- 可能是令牌已过期（检查有效期）
- 可能是键输入错误
- 可能从未写入过记录

### 会话未找到
- 运行 `sessions_list` 查看可用的会话
- 可能需要先启动相应的会话

## 参考资料

- [AuthGuardian 详细信息](references/auth-guardian.md) - 完整的权限系统文档
- [黑板架构](references/blackboard-schema.md) - 数据结构规范
- [代理信任度](references/trust-levels.md) - 信任度的计算方式