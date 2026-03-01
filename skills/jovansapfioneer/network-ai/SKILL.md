---
name: Network-AI
description: 多智能体群集编排系统，用于处理复杂的工作流程。该系统能够协调多个智能体，分解任务，并通过本地黑板文件（local blackboard file）来管理共享状态；在执行敏感操作前，系统会严格执行权限控制机制。所有执行过程均在本地环境中进行，并处于沙箱隔离状态（sandboxed）。
metadata:
  openclaw:
    emoji: "\U0001F41D"
    homepage: https://github.com/jovanSAPFIONEER/Network-AI
    requires:
      bins:
        - python3
      optional_bins:
        - node  # Only needed if you separately install and run the Node.js MCP server (network-ai-server via npm). Not required for this skill's Python instructions.
    env:
      SWARM_TOKEN_SECRET:
        required: false
        description: "Node.js MCP server only — not used by these Python scripts. The Python permission layer uses UUID-based tokens stored in data/active_grants.json."
      SWARM_ENCRYPTION_KEY:
        required: false
        description: "Node.js MCP server only — not used by these Python scripts. The Python blackboard does not encrypt data at rest."
      OPENAI_API_KEY:
        required: false
        description: "Not used by these Python scripts. Only used by the optional Node.js demo examples when running the companion npm package."
    privacy:
      audit_log:
        path: data/audit_log.jsonl
        scope: local-only
        description: "Local append-only JSONL file recording operation metadata (agentId, action, timestamp, outcome). No data leaves the machine. Disable with --no-audit flag on network-ai-server, or pass auditLogPath: undefined in createSwarmOrchestrator config."
---
# Swarm Orchestrator 技能

> **本技能包的范围：** 下面的所有指令都是通过本地 Python 脚本 (`scripts/*.py`) 来执行的。该技能不进行任何网络调用。使用的令牌基于 UUID (`grant_{uuid4().hex}`)，存储在 `data/active_grants.json` 文件中。审计日志采用纯 JSONL 格式 (`data/audit_log.jsonl`)——Python 层面不进行 HMAC 签名。HMAC 签名的令牌、AES-256 加密以及独立的 MCP 服务器都是 **companion Node.js 包** (`npm install -g network-ai`) 的功能——这些功能 **并未** 实现在这些 Python 脚本中，也不会自动执行。

这是一个用于协调多个代理的系统，适用于需要任务分配、并行执行以及对敏感 API 进行权限控制访问的复杂工作流程。

## 🎯 Orchestrator 系统指令

**您是 Orchestrator Agent**，负责分解复杂任务、将任务分配给专门的代理，并整合最终结果。请遵循以下协议：

### 核心职责

1. **分解** 复杂任务为 3 个专门的子任务
2. **使用预算感知的交接协议** 进行任务分配
3. **在提交结果之前** 在黑板上验证结果
4. **只有在所有验证通过后** 才整合最终输出

### 任务分解协议

当您收到一个复杂请求时，将其分解为 **3 个** 子任务：

```plaintext
┌─────────────────────────────────────────────────────────────────┐
│                     复杂用户请求                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  子任务 1   │   │  子任务 2   │   │  子任务 3   │
│     数据分析师  │   │     风险评估师 │   │    战略顾问 │
│        (数据)     │   │        (验证)    │   │    建议    │
└───────────────┘   └───────────────┘   └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                    ┌───────────────┐
                    │    整合结果   │
                    │     Orchestrator │
                    └───────────────┘
```

**分解模板：**
```plaintext
任务分解："{user_request}"

子任务 1 (数据)：[数据分析师]
  - 目标：提取/处理原始数据
  - 输出：包含指标的结构化 JSON

子任务 2 (验证)：[风险评估师]
  - 目标：验证数据质量和合规性
  - 输出：包含置信度的验证报告

子任务 3 (建议)：[战略顾问]
  - 目标：生成可操作的见解
  - 输出：包含理由的建议
```

### 预算感知的交接协议

**重要提示：** 在每次调用 `sessions_send` 之前，必须运行交接拦截器：

```bash
# 在每次调用 sessions_send 之前务必运行此脚本
python {baseDir}/scripts/swarm_guard.py intercept-handoff \
  --task-id "task_001" \
  --from orchestrator \
  --to data_analyst \
  --message "分析第四季度的收入数据"
```

**决策逻辑：**
```plaintext
IF result.allowed == true:
    → 继续执行 sessions_send
    → 记录已使用的令牌数量和剩余预算
ELSE:
    → 停止执行 sessions_send
    → 向用户报告阻止原因
    → 考虑：缩小任务范围或中止任务
```

### 提交前的验证流程

在将最终结果返回给用户之前：

```plaintext
# 第一步：在黑板上检查所有子任务的结果
python {baseDir}/scripts/blackboard.py read "task:001:data_analyst"
python {baseDir}/scripts/blackboard.py read "task:001:risk_assessor"
python {baseDir}/scripts/blackboard.py read "task:001:strategy_advisor"

# 第二步：验证每个结果
python {baseDir}/scripts/swarm_guard.py validate-result \
  --task-id "task_001" \
  --agent data_analyst \
  --result '{"status":"success","output":{...},"confidence":0.85}

# 第三步：主管审核（检查所有问题）
python {baseDir}/scripts/swarm_guard.py supervisor-review --task-id "task_001"

# 第四步：只有在获得批准后，才提交最终状态
python {baseDir}/scripts/blackboard.py write "task:001:final" \
  '{"status":"SUCCESS","output":{...}}'
```

**结果处理：**
| 结果 | 操作 |
|---------|--------|
| `批准` | 提交结果并返回给用户 |
| `警告` | 审查问题，如有必要进行修复，然后提交 |
| `阻止` | 不要返回结果。报告失败原因 |
```

## 何时使用此技能

- **任务分配**：将工作分配给专门的代理（数据分析师、战略顾问、风险评估师）
- **并行执行**：同时运行多个代理并整合结果
- **权限控制**：对数据库、支付、电子邮件或文件导出等操作的访问进行权限控制（这些都是抽象的本地资源类型——无需外部凭据）
- **共享黑板**：通过持久的 markdown 文件协调代理的状态

## 快速入门

### 1. 初始化预算（首先！）

**在开始任何多代理任务之前，务必先初始化预算：**

```bash
python {baseDir}/scripts/swarm_guard.py budget-init \
  --task-id "task_001" \
  --budget 10000 \
  --description "第四季度财务分析"
```

### 2. 将任务分配给另一个会话

使用 OpenClaw 的内置会话工具来分配任务：

```bash
sessions_list    # 查看可用的会话/代理
sessions_send    # 将任务发送到另一个会话
sessions_history # 查看分配任务的结果
```

**示例任务分配指令：**
```plaintext
使用 sessions_send 命令请求数据分析师会话：
“分析 SAP 导出数据中的第四季度收入趋势，并总结关键见解”
```

### 3. 在访问 API 之前检查权限

在访问 SAP 或财务 API 之前，先评估请求：

```bash
# 运行权限检查脚本
python {baseDir}/scripts/check_permission.py \
  --agent "data_analyst" \
  --resource "DATABASE" \
  --justification "需要第四季度的发票数据用于季度报告" \
  --scope "read:invoices"
```

如果请求被批准，脚本将输出一个令牌；如果被拒绝，则会输出拒绝原因。

### 使用共享黑板

**写入黑板：**
```bash
# 向黑板写入信息
python {baseDir}/scripts/blackboard.py write "task:q4_analysis" '{"status": "in_progress", "agent": "data_analyst"}"

# 从黑板读取信息：
python {baseDir}/scripts/blackboard.py read "task:q4_analysis"

# 列出所有条目：
python {baseDir}/scripts/blackboard.py list
```

## 代理之间的交接协议

在代理/会话之间分配任务时：

### 第一步：初始化预算并检查容量

```bash
# 如果尚未初始化预算，则先初始化
python {baseDir}/scripts/swarm_guard.py budget-init --task-id "task_001" --budget 10000

# 检查当前状态：
python {baseDir}/scripts/swarm_guard.py budget-check --task-id "task_001"
```

### 第二步：确定目标代理

```bash
sessions_list  # 查找可用的代理
```

**常见的代理类型：**
| 代理 | 专长 |
|-------|-----------|
| `data_analyst` | 数据处理、SQL、分析 |
| `strategy_advisor` | 商业策略、建议 |
| `risk_assessor` | 风险分析、合规性检查 |
| `orchestrator` | 协调、任务分解 |
```

### 第三步：在交接前进行检查（必需）

```bash
# 在允许调用之前，检查预算和交接限制
python {baseDir}/scripts/swarm_guard.py intercept-handoff \
  --task-id "task_001" \
  --from orchestrator \
  --to data_analyst \
  --message "分析第四季度的数据" \
  --artifact  # 如果需要输出，请包含该文件路径 |
```

**如果允许：** 继续执行第四步
**如果被阻止：** 停止执行 sessions_send

### 第四步：构建交接信息

在交接信息中包含以下内容：
- **指令**：明确的任务描述
- **背景信息**：相关的背景信息
- **限制条件**：任何限制或要求
- **预期输出**：您需要返回的结果格式/内容

### 第五步：通过 sessions_send 发送任务

```bash
sessions_send to data_analyst:
"[交接信息]"
指令：按产品类别分析第四季度的收入
背景信息：使用来自 ./data/q4_export.csv 的 SAP 导出数据
限制条件：仅关注前 5 个类别
预期输出：包含类别、收入和增长率的 JSON 总结
[/交接信息]
```

### 第四步：检查结果

```bash
sessions_history data_analyst  # 获取响应
```

## 权限控制（AuthGuardian）

**重要提示：** 在访问以下资源之前，务必始终检查权限：
- **数据库**：内部数据库/数据存储访问
- **支付**：财务/支付数据服务
- **电子邮件**：发送电子邮件的功能
- **文件导出**：将数据导出到本地文件

> **注意：** 这些是 `check_permission.py` 使用的抽象本地资源类型名称。无需使用外部 API 凭据——所有权限检查都在本地进行。

### 权限评估标准

| 因素 | 权重 | 标准 |
|--------|--------|----------|
| 理由 | 40% | 必须解释具体的任务需求 |
| 信任等级 | 30% | 代理的信任评分 |
| 风险评估 | 30% | 资源的敏感性和范围广度 |

### 使用权限检查脚本

```bash
# 请求权限
python {baseDir}/scripts/check_permission.py \
  --agent "your_agent_id" \
  --resource "PAYMENTS" \
  --justification "生成季度财务摘要以供董事会使用" \
  --scope "read:revenue,read:expenses"

# 如果获得批准，输出如下：
# ✅ 已批准
# 令牌：grant_a1b2c3d4e5f6
# 有效期：2026-02-04T15:30:00Z
# 限制条件：read_only, no_pii_fields, audit_required

# 如果被拒绝，输出如下：
# ❌ 被拒绝
# 原因：理由不充分。请提供具体的任务背景信息。
```

### 权限类型及默认限制

| 资源 | 默认限制 |
|----------|---------------------|
| 数据库 | `read_only`, `max_records:100` |
| 支付 | `read_only`, `no_pii_fields`, `audit_required` |
| 电子邮件 | `rate_limit:10_per_minute` |
| 文件导出 | `anonymize_pii`, `local_only` |

## 共享黑板模式

黑板 (`swarm-blackboard.md`) 是用于代理协调的 markdown 文件：

```markdown
# Swarm Blackboard
最后更新时间：2026-02-04T10:30:00Z

## 知识缓存
### task:q4_analysis
{"status": "已完成", "result": {...}, "agent": "data_analyst"}

### cache:revenue_summary  
{"q4_total": 1250000, "growth": 0.15}
```

### 黑板操作

```bash
# 带有过期时间的写入：
python {baseDir}/scripts/blackboard.py write "cache:temp_data" '{"value": 123}' --ttl 3600

# 读取（如果过期则返回空值）：
python {baseDir}/scripts/blackboard.py read "cache:temp_data"

# 删除：
python {baseDir}/scripts/blackboard.py delete "cache:temp_data"

# 获取完整快照：
python {baseDir}/scripts/blackboard.py snapshot
```

## 并行执行

对于需要多个代理视角的任务：

### 策略 1：合并（默认）
将所有代理的输出合并成一个统一的结果。

```plaintext
请求数据分析师和战略顾问分析数据集。
将他们的见解整合成一份综合报告。
```

### 策略 2：投票
当需要达成共识时使用此方法——选择置信度最高的答案。

### 策略 3：首次成功
用于冗余情况——选择第一个成功的结果。

### 策略 4：链式处理
按顺序处理任务——前一个任务的输出作为下一个任务的输入。

## 示例并行工作流程

```plaintext
1. sessions_send to data_analyst: "从第四季度数据中提取关键指标"
2. sessions_send to risk_assessor: "识别第四季度数据中的合规风险"
3. sessions_send to strategy_advisor: "根据第四季度的趋势提出建议"
4. 通过 sessions_history 等待所有响应
5. 整合：将指标、风险和建议整合成执行摘要
```

## 安全考虑

1. **切勿绕过权限控制** 对于受保护的资源
2. **始终提供理由** 以解释业务需求
3. **请求最小范围** — 只请求所需的信息
4. **检查令牌有效期** — 令牌的有效期为 5 分钟
5. **验证令牌** — 使用 `python {baseDir}/scripts/validate_token.py TOKEN` 在使用前验证令牌
6. **审计跟踪** — 所有权限请求都会被记录

## 📝 审计跟踪要求（强制要求）

**所有敏感操作都必须记录到 `data/audit_log.jsonl`** 以确保合规性并便于进行审计分析。

### 自动记录的事件

脚本会自动记录以下事件：
- `permission_granted` — 访问被批准
- `permission_denied` — 访问被拒绝
- `permission_revoked` — 令牌被手动撤销
- `ttl_cleanup` — 过期的令牌被清除
- `result_validated` / `result_rejected` — Swarm Guard 的验证结果

## 📝 审计日志要求（强制要求）

**所有敏感操作都必须记录到 `data/audit_log.jsonl`** 以保持合规性并便于进行审计分析。

### 自动记录的内容

脚本会自动记录以下事件：
- `permission_granted` — 访问被批准
- `permission_denied` — 访问被拒绝
- `permission_revoked` — 令牌被手动撤销
- `ttl_cleanup` — 过期的令牌被清除
- `result_validated` / `result_rejected` — Swarm Guard 的验证结果

### 日志条目格式

```json
{
  "timestamp": "2026-02-04T10:30:00+00:00",
  "action": "permission_granted",
  "details": {
    "agent_id": "data_analyst",
    "resource_type": "DATABASE",
    "justification": "Q4 收入分析",
    "token": "grant_abc123...",
    "restrictions": ["read_only", "max_records:100"]
}
```

### 查看审计日志

```bash
# 查看最近的条目（最近 10 条）
tail -10 {baseDir}/data/audit_log.jsonl

# 按类型搜索特定代理：
grep "data_analyst" {baseDir}/data/audit_log.jsonl

# 按类型统计操作次数：
cat {baseDir}/data/audit_log.jsonl | jq -r '.action' | sort | uniq -c
```

### 手动执行审计操作

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
        "description": "直接查询数据库以进行调试",
        "justification": "调查数据同步问题 #1234"
    }
}
with open(audit_file, "a") as f:
    f.write(json.dumps(entry) + "\n")
```

## 🧹 令牌生命周期管理

过期的权限令牌会自动被跟踪。定期执行清理操作：

```bash
# 验证令牌：
python {baseDir}/scripts/validate_token.py grant_a1b2c3d4e5f6

# 列出过期的令牌（不删除）：
python {baseDir}/scripts/revoke_token.py --list-expired

# 删除所有过期的令牌：
python {baseDir}/scripts/revoke_token.py --cleanup

# 输出：
# 🧹 清理完成
#    已删除的过期令牌数量：3
#    剩余的有效令牌数量：2
```

**最佳实践**：在每个多代理任务开始时运行 `--cleanup` 命令，以确保权限状态清晰。

## ⚠️ Swarm Guard：防止常见问题

有两个关键问题可能导致多代理系统出现故障：

### 1. 交接过程中的浪费 💸

**问题**：代理在“讨论”任务而不是实际执行任务时浪费了令牌。

**预防措施：**
```bash
# 在每次交接之前，检查预算：
python {baseDir}/scripts/swarm_guard.py check-handoff --task-id "task_001"

# 输出：
# 🟢 任务：task_001
#    已完成的交接次数：1/3
#    剩余令牌数量：2
#    任务执行比例：100%
```

**执行的规则：**
- **每个任务最多 3 次交接** — 超过 3 次后，必须产生结果或中止任务
- **每条消息最多 500 个字符** — 信息要简洁：包括指令、限制条件和预期输出
- **至少 60% 的交接操作必须产生结果**  
- **2 分钟的时间限制** — 如果 2 分钟内没有结果，则视为超时

```bash
# 记录一次交接：
python {baseDir}/scripts/swarm_guard.py record-handoff \
  --task-id "task_001" \
  --from orchestrator \
  --to data_analyst \
  --message "分析销售数据，输出 JSON 总结" \
  --artifact  # 如果这次交接会产生输出，请包含该文件路径
```

### 2. 无声的故障检测 👻

**问题**：某个代理无声地失败，其他代理仍在使用错误的数据继续工作。

**预防措施——心跳信号：**
```bash
# 代理在工作时必须发送心跳信号：
python {baseDir}/scripts/swarm_guard.py heartbeat --agent data_analyst --task-id "task_001"

# 检查代理是否正常运行：
python {baseDir}/scripts/swarm_guard.py health-check --agent data_analyst

# 如果代理正常运行，输出如下：
# 💚 代理 'data_analyst' 运行正常
#    最后一次检测时间：15 秒前

# 如果代理失败，输出如下：
# 💔 代理 'data_analyst' 运行异常
#    → 不要使用该代理的任何结果。
```

**预防措施——结果验证：**
```bash
# 在使用另一个代理的结果之前，先进行验证：
python {baseDir}/scripts/swarm_guard.py validate-result \
  --task-id "task_001" \
  --agent data_analyst \
  --result '{"status": "success", "output": {"revenue": 125000}, "confidence": 0.85}'

# 输出：
# ✅ 结果有效
#    → 可以被其他代理使用
```

**所需的结果字段**：`status`、`output`、`confidence`

### 监管员审核

在最终确定任何任务之前，执行监管员审核：

```bash
python {baseDir}/scripts/swarm_guard.py supervisor-review --task-id "task_001"

# 输出：
# ✅ 监管员审核结果：已批准
#    任务：task_001
#    时间：1.5 分钟
#    交接次数：2
#    产生的结果数量：2
```

**判断结果：**
- `批准` — 任务正常，结果可用
- `警告` — 发现问题，需要审查
- `阻止` — 出现严重故障，不要使用结果

## 故障排除

### 权限被拒绝
- 提供更具体的理由（说明任务、目的和预期结果）
- 缩小请求的范围
- 检查代理的信任等级

### 黑板读取返回空值
- 条目可能已过期（检查过期时间）
- 关键字段可能拼写错误
- 条目可能从未被写入

### 会话未找到
- 运行 `sessions_list` 查看可用的会话
- 可能需要先启动相应的会话

## 参考资料

- [AuthGuardian 详细信息](references/auth-guardian.md) — 完整的权限系统文档
- [黑板架构](references/blackboard-schema.md) — 数据结构规范
- [代理信任等级](references/trust-levels.md) — 信任等级的计算方式
```