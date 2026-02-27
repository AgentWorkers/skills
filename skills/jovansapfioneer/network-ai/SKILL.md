---
name: Network-AI
description: 多智能体群集编排系统，用于处理复杂的工作流程。该系统能够协调多个智能体，分解任务，通过本地黑板文件（local blackboard file）管理共享状态，并在执行敏感操作前实施权限控制。所有执行过程均在本地环境中进行，并处于沙箱（sandbox）模式下。
metadata:
  openclaw:
    emoji: "\U0001F41D"
    homepage: https://github.com/jovanSAPFIONEER/Network-AI
    requires:
      bins:
        - python3
---
# Swarm Orchestrator 技能

这是一个用于协调多个代理的系统，适用于需要任务分配、并行执行以及对敏感 API 进行权限控制访问的复杂工作流程。

## 🎯 Orchestrator 系统说明

**您是 Orchestrator Agent**，负责分解复杂任务、将任务分配给专门的代理，并整合最终结果。请遵循以下协议：

### 核心职责

1. **分解** 复杂任务为 3 个专门的子任务
2. **分配** 任务时使用预算限制机制
3. **验证** 结果后再提交
4. **整合** 只有在所有验证通过后，才整合最终输出

### 任务分解协议

收到复杂请求时，将其分解为 **3 个** 子任务：

```plaintext
┌─────────────────────────────────────────────────────────────────┐
│                     复杂用户请求                        │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  子任务 1   │   │  子任务 2   │   │  子任务 3   │
│ 数据分析师  │   │ 风险评估师 │   │策略顾问 │
│    （数据）     │   │   （验证）    │   │  （建议）  │
└───────────────┘   └───────────────┘   └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                    ┌───────────────┐
                    │  整合结果   │
                    │ Orchestrator  │
                    └───────────────┘
```

**分解模板：**
```plaintext
任务分解："{user_request}"

子任务 1（数据）：[数据分析师]
  - 目标：提取/处理原始数据
  - 输出：包含指标的结构化 JSON 数据

子任务 2（验证）：[风险评估师]
  - 目标：验证数据质量和合规性
  - 输出：包含置信度的验证报告

子任务 3（建议）：[策略顾问]
  - 目标：生成可操作的见解
  - 输出：包含理由的建议
```

### 预算限制机制

**重要提示：** 在每次调用 `sessions_send` 之前，必须执行以下操作：

```bash
# 在每次发送任务之前务必运行此脚本
python {baseDir}/scripts/swarm_guard.py intercept-handoff \
  --task-id "task_001" \
  --from orchestrator \
  --to data_analyst \
  --message "分析第四季度的收入数据"
```

**决策逻辑：**
```plaintext
如果结果满足条件（`result.allowed == true`）：
  → 继续发送任务
  → 记录已使用的令牌数量和剩余预算
否则：
  → 停止发送任务
  → 向用户报告失败原因
  → 考虑缩小任务范围或终止任务
```

### 提交前的验证流程

在将最终结果返回给用户之前，请执行以下步骤：

```plaintext
# 第一步：在黑板上查看所有子任务的结果
python {baseDir}/scripts/blackboard.py read "task:001:data_analyst"
python {baseDir}/scripts/blackboard.py read "task:001:risk_assessor"
python {baseDir}/scripts/blackboard.py read "task:001:strategy_advisor"

# 第二步：验证每个结果
python {baseDir}/scripts/swarm_guard.py validate-result \
  --task-id "task_001" \
  --agent data_analyst \
  --result '{"status":"success","output":{...},"confidence":0.85}

# 第三步：由主管审核（检查所有问题）
python {baseDir}/scripts/swarm_guard.py supervisor-review --task-id "task_001"

# 第四步：只有通过审核后，才能提交最终状态
python {baseDir}/scripts/blackboard.py write "task:001:final" \
  '{"status":"SUCCESS","output":{...}}"
```

### 结果处理方式：

| 结果 | 对应操作 |
|---------|--------|
| `APPROVED` | 提交结果并返回给用户 |
| `WARNING` | 审查问题，如有必要进行修复后再提交 |
| `BLOCKED` | 不要返回结果，报告失败原因 |
```

## 使用此技能的场景

- **任务分配**：将工作分配给专门的代理（数据分析师、策略顾问、风险评估师）
- **并行执行**：同时运行多个代理并整合结果
- **权限控制**：对数据库、支付、电子邮件或文件导出等操作进行访问控制（这些是抽象的本地资源类型，无需外部凭证）
- **共享黑板**：通过持久的 markdown 文件协调代理的状态

## 快速入门

### 1. 初始化预算（首先！）

**在开始任何多代理任务之前，务必初始化预算：**

```bash
python {baseDir}/scripts/swarm_guard.py budget-init \
  --task-id "task_001" \
  --budget 10000 \
  --description "第四季度财务分析"
```

### 2. 将任务分配给其他代理

使用 OpenClaw 的内置会话工具来分配任务：

```bash
sessions_list    # 查看可用的代理/会话
sessions_send    # 将任务发送给其他代理
sessions_history # 查看分配任务的结果
```

**示例任务分配命令：**
```bash
使用 sessions_send 向数据分析师会话请求：
“分析 SAP 导出数据中的第四季度收入趋势，并总结关键见解”
```

### 在访问 API 之前检查权限

在访问 SAP 或财务 API 之前，请先进行权限检查：

```bash
# 运行权限检查脚本
python {baseDir}/scripts/check_permission.py \
  --agent "data_analyst" \
  --resource "DATABASE" \
  --justification "需要第四季度的发票数据用于季度报告" \
  --scope "read:invoices"
```

如果权限被批准，脚本将输出授权令牌；否则会输出拒绝原因。

### 使用共享黑板

**写入黑板：**
```bash
python {baseDir}/scripts/blackboard.py write "task:q4_analysis" '{"status": "in_progress", "agent": "data_analyst"}"
```

**从黑板读取数据：**
```bash
python {baseDir}/scripts/blackboard.py read "task:q4_analysis"
```

**列出所有黑板条目：**
```bash
python {baseDir}/scripts/blackboard.py list
```

## 代理之间的任务传递协议

### 1. 初始化预算并检查容量

**首先初始化预算（如果尚未执行）：**
```bash
python {baseDir}/scripts/swarm_guard.py budget-init --task-id "task_001" --budget 10000
```

**检查当前预算状态：**
```bash
python {baseDir}/scripts/swarm_guard.py budget-check --task-id "task_001"
```

### 2. 确定目标代理

**查找可用的代理：**
```bash
sessions_list  # 查找可用的代理
```

**常见代理类型：**
| 代理 | 专业领域 |
|-------|-----------|
| 数据分析师 | 数据处理、SQL、分析 |
| 策略顾问 | 商业策略、建议 |
| 风险评估师 | 风险分析、合规性检查 |
| Orchestrator | 协调、任务分解 |

### 3. 在传递任务前进行检查（必需）

**在允许任务传递之前，检查预算和代理的容量：**
```bash
python {baseDir}/scripts/swarm_guard.py intercept-handoff \
  --task-id "task_001" \
  --from orchestrator \
  --to data_analyst \
  --message "分析第四季度的数据" \
  --artifact  # 如果需要输出，请包含输出文件路径 |
```

**如果权限被批准，继续执行第 4 步；否则停止发送任务。**

### 4. 构建传递消息

在传递任务时，包含以下信息：
- **任务描述**：明确的任务说明
- **背景信息**：相关的上下文信息
- **限制条件**：任何限制或要求
- **预期输出**：你需要返回的结果格式/内容

### 5. 通过 sessions_send 发送任务

```bash
sessions_send to data_analyst:
"[传递任务]
任务描述：按产品类别分析第四季度的收入
背景信息：使用来自 ./data/q4_export.csv 的 SAP 导出数据
限制条件：仅关注前 5 个类别
预期输出：包含类别、收入和增长率的 JSON 总结
```

### 结果检查

```bash
sessions_history data_analyst  # 获取数据分析师的响应
```

## 权限控制（AuthGuardian）

**重要提示：** 在访问以下资源之前，务必检查权限：
- **数据库**：内部数据库/数据存储
- **支付**：财务/支付数据服务
- **电子邮件**：发送电子邮件的功能
- **文件导出**：将数据导出到本地文件

> **注意**：这些是 `check_permission.py` 使用的抽象资源类型名称。无需使用外部 API 凭证，所有权限检查都在本地完成。

### 权限评估标准

| 评估因素 | 权重 | 标准         |
|--------|------------|-------------------|
| 任务必要性 | 40%       | 必须详细说明任务需求 |
| 代理信任度 | 30%       | 代理的信任评分           |
| 风险评估 | 30%       | 资源的敏感性和范围宽度       |

### 使用权限检查脚本

```bash
# 请求权限
python {baseDir}/scripts/check_permission.py \
  --agent "your_agent_id" \
  --resource "PAYMENTS" \
  --justification "生成季度财务摘要以供董事会使用" \
  --scope "read:revenue,read:expenses"
```

**输出示例：**
```bash
# ✅ 授权成功
# 令牌：grant_a1b2c3d4e5f6
# 有效期：2026-02-04T15:30:00Z
# 限制条件：仅限读取权限，不允许访问个人身份信息（PII）字段
```

### 权限限制类型

| 资源 | 默认限制        |
|---------|---------------------|
| 数据库   | 只读权限，最多查询 100 条记录 |
| 支付     | 只读权限，禁止访问个人身份信息（PII）字段 |
| 电子邮件 | 每分钟发送次数限制为 10 次   |
| 文件导出 | 对个人身份信息进行匿名处理，仅限本地访问 |
```

## 共享黑板模式

黑板（`swarm-blackboard.md`）是一个用于代理协调的 markdown 文件：

```markdown
# Swarm Blackboard
最后更新时间：2026-02-04T10:30:00Z

## 知识缓存

### task:q4_analysis
{"status": "已完成", "result": {...}, "agent": "data_analyst"}
```

### 缓存示例
```plaintext
### cache:revenue_summary
{"q4_total": 1250000, "growth": 0.15}
```

## 黑板操作

```bash
# 带有时效限制地写入黑板
python {baseDir}/scripts/blackboard.py write "cache:temp_data" '{"value": 123}' --ttl 3600

# 读取黑板数据（如果过期则返回空值）
python {baseDir}/scripts/blackboard.py read "cache:temp_data"

# 删除黑板条目
python {baseDir}/scripts/blackboard.py delete "cache:temp_data"

# 获取黑板的全貌
python {baseDir}/scripts/blackboard.py snapshot
```

## 并行执行策略

### 策略 1：合并结果（默认）

将所有代理的输出合并为一个统一的结果：

```plaintext
请求数据分析师和策略顾问分析数据集，并将他们的见解整合成一份综合报告。
```

### 策略 2：投票

当需要达成共识时，选择置信度最高的答案。

### 策略 3：首次成功策略

用于处理冗余情况——选择第一个成功的代理结果。

### 策略 4：链式处理

按顺序处理任务——前一个代理的结果作为下一个代理的输入。

## 安全注意事项

1. **切勿绕过权限控制**：对于受限制的资源，必须遵守权限规则。
2. **始终提供理由**：明确说明访问的业务需求。
3. **请求最小范围的权限**：仅请求所需的数据。
4. **检查令牌有效期**：令牌的有效期为 5 分钟。
5. **验证令牌**：使用 `python {baseDir}/scripts/validate_token.py` 验证令牌的有效性。
6. **保留审计日志**：所有权限请求都会被记录。

## 📝 审计日志要求（强制要求）

**所有敏感操作都必须记录到 `data/audit_log.jsonl` 中**，以确保合规性并便于进行审计分析。

### 自动记录的事件

以下操作会自动被记录：
- `permission_granted`：权限被批准时
- `permission_denied`：权限被拒绝时
- `permission_revoked`：令牌被手动撤销时
- `ttl_cleanup`：过期的令牌被清除时
- `result_validated` / `result_rejected`：权限验证通过/失败时

## 日志条目格式

```json
{
  "timestamp": "2026-02-04T10:30:00+00:00",
  "action": "permission_granted",
  "details": {
    "agent_id": "data_analyst",
    "resource_type": "DATABASE",
    "justification": "第四季度收入分析",
    "token": "grant_abc123...",
    "restrictions": ["read_only", "max_records:100"]
}
```

## 查看审计日志

```bash
# 查看最近的 10 条日志
tail -10 {baseDir}/data/audit_log.jsonl

# 按类型统计日志条目
cat {baseDir}/data/audit_log.jsonl | jq -r '.action' | sort | uniq -c
```

## 手动执行敏感操作时的日志记录

如果手动执行敏感操作，请进行记录：

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
        "description": "为调试目的直接查询数据库",
        "justification": "调查数据同步问题 #1234"
    }
}
with open(audit_file, "a") as f:
    f.write(json.dumps(entry) + "\n"
```

## 🧹 令牌生命周期管理

过期的权限令牌会自动被清除：

```bash
# 验证令牌的有效性
python {baseDir}/scripts/validate_token.py grant_a1b2c3d4e5f6

# 列出过期的令牌
python {baseDir}/scripts/revoke_token.py --list-expired

# 删除所有过期的令牌
python {baseDir}/scripts/revoke_token.py --cleanup

# 输出示例：
# 🧹 清理完成
# 已删除的过期令牌数量：3 个
# 当前有效的令牌数量：2 个
```

**最佳实践**：在每个多代理任务开始时运行 `--cleanup` 命令，以确保权限状态清晰。

## ⚠️ Swarm Guard：防止常见错误

两个关键问题可能会影响多代理系统的正常运行：

### 1. 无效的令牌使用

**问题**：代理浪费令牌，只是讨论任务而未实际执行。

**预防措施：**
```bash
# 在每次传递任务之前，检查预算使用情况：
python {baseDir}/scripts/swarm_guard.py check-handoff --task-id "task_001"
```

**输出示例：**
```bash
🟢 任务：task_001
    已完成的传递次数：1/3
    剩余令牌数量：2
    任务执行比例：100%
```

**执行的规则：**
- **每个任务最多允许 3 次任务传递**：超过 3 次后，必须产生结果或终止任务。
- **每条消息最多 500 个字符**：信息要简洁明了（包括任务描述、限制条件和预期输出）。
- **至少 60% 的任务传递需要产生实际结果**。
- **2 分钟的等待时间限制**：如果 2 分钟内没有结果，视为超时。

```bash
# 记录任务传递：
python {baseDir}/scripts/swarm_guard.py record-handoff \
  --task-id "task_001" \
  --from orchestrator \
  --to data_analyst \
  --message "分析销售数据，并输出 JSON 总结"
  --artifact  # 如果此传递会产生结果，请包含输出文件路径
```

### 2. 代理的异常情况

**问题**：某个代理出现故障，其他代理仍继续使用错误的数据。

**预防措施：** 实施心跳检测：
```bash
# 代理在处理任务时必须发送心跳信号：
python {baseDir}/scripts/swarm_guard.py heartbeat --agent data_analyst --task-id "task_001"

# 检查代理的状态：
python {baseDir}/scripts/swarm_guard.py health-check --agent data_analyst

**输出示例：**
```bash
💚 代理 'data_analyst' 的状态正常
    最后检测时间：15 秒前

# 如果代理状态异常：
💔 代理 'data_analyst' 的状态异常
    → 不要使用该代理提供的任何结果。
```

**额外措施：** 在使用其他代理的结果之前，先验证结果：
```bash
# 在使用数据分析师的结果之前，先进行验证：
python {baseDir}/scripts/swarm_guard.py validate-result \
  --task-id "task_001" \
  --agent data_analyst \
  --result '{"status": "success", "output": {"revenue": 125000}, "confidence": 0.85}'
```

**所需的结果字段：**
- `status`：任务状态
- `output`：输出结果
- `confidence`：结果的置信度

### 主管审核

在最终确定任务结果之前，执行审核：

```bash
python {baseDir}/scripts/swarm_guard.py supervisor-review --task-id "task_001"
```

**输出示例：**
```bash
✅ 主管审核结果：批准
    任务：task_001
    任务执行时间：1.5 分钟
    传递次数：2 次
    产生的结果数量：2 个
```

**可能的判断结果：**
- `APPROVED`：任务正常，结果可用
- `WARNING`：发现问题，建议重新处理
- `BLOCKED`：存在严重故障，不得使用该结果

## 故障排除

### 权限被拒绝时
- 提供更详细的理由（说明任务内容、目的和预期结果）
- 缩小请求的范围
- 检查代理的信任等级

### 黑板读取失败

- 条目可能已过期（检查时效）
- 条目中的键可能拼写错误
- 条目可能从未被写入

### 会话未找到

- 运行 `sessions_list` 查看可用的代理/会话
- 可能需要先启动相应的会话

## 参考资料

- [AuthGuardian 详细信息](references/auth-guardian.md)：完整的权限系统文档
- [黑板架构](references/blackboard-schema.md)：数据结构规范
- [代理信任等级](references/trust-levels.md)：信任等级的计算方式
```