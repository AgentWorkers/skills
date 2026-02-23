---
name: pager-triage
version: 0.1.1
displayName: PagerDuty Incident Triage
description: 基于人工智能的PagerDuty事件分拣功能：您可以查看当前正在处理的事件，通过时间线深入了解事件的发展过程以及事件与警报之间的关联关系，查看值班人员的排班情况，对事件进行确认、处理或添加备注。默认情况下，该功能仅支持只读操作；如需执行写入操作，则必须明确使用`--confirm`参数。
author: Anvil AI
tags:
  - pagerduty
  - opsgenie
  - incident
  - sre
  - oncall
  - triage
  - discord
  - discord-v2
tools:
  - name: pd_incidents
    description: List active PagerDuty incidents (triggered + acknowledged)
  - name: pd_incident_detail
    description: Get detailed incident info including timeline, alerts, and notes
  - name: pd_oncall
    description: Show current on-call schedules and escalation policies
  - name: pd_incident_ack
    description: Acknowledge an incident (requires --confirm)
  - name: pd_incident_resolve
    description: Resolve an incident (requires --confirm)
  - name: pd_incident_note
    description: Add a note to an incident (requires --confirm)
  - name: pd_services
    description: List PagerDuty services and their current status
  - name: pd_recent
    description: Show recent incidents for a service (last 24h/7d/30d)
---
# PagerDuty 事件分拣

这是一个基于 AI 的 PagerDuty 事件分拣工具。默认为只读模式；执行写入操作前需要明确确认。

## 何时启用

在以下情况下使用此工具：

- 用户询问“发生了什么？”、“有事件吗？”或与活动警报相关的任何问题；
- 用户提到 PagerDuty、值班人员或事件；
- 用户询问“谁在值班？”或“现在谁在值班？”；
- 用户希望确认事件、解决事件或为事件添加备注；
- 用户提到“事件分拣”、“事件响应”或“昨晚发生了什么？”；
- 用户询问服务的运行状态或最近的事件。

## 快速设置

### 1. 创建 PagerDuty API 密钥

1. 登录到 **PagerDuty → 设置 → API 访问密钥**；
2. 点击 “创建新的 API 密钥”；
3. 将密钥命名为 `OpenClaw Agent`；
4. 选择 “只读”（建议用于分拣；如需确认/解决事件，请选择 “全权限”）；
5. 复制密钥。

### 2. 设置环境变量

```bash
# Required — your PagerDuty REST API v2 token
export PAGERDUTY_API_KEY="u+your_key_here"

# Optional — required only for write operations (ack, resolve, note)
export PAGERDUTY_EMAIL="you@company.com"
```

### 3. 验证

向您的代理发送请求：**“PagerDuty 上发生了什么事件？”**

## 子命令参考

### 读取操作（始终安全，无需确认）

---

#### `incidents` — 列出所有活动事件

按紧急程度排序，列出所有被触发和已确认的事件。

**示例输出：**
```json
{
  "tool": "pd_incidents",
  "provider": "pagerduty",
  "timestamp": "2026-02-16T03:45:00Z",
  "total_incidents": 3,
  "incidents": [
    {
      "id": "P123ABC",
      "incident_number": 4521,
      "title": "High CPU on prod-web-03",
      "status": "triggered",
      "urgency": "high",
      "service": { "id": "PSVC123", "name": "Production Web" },
      "created_at": "2026-02-16T03:00:00Z",
      "assignments": [{ "name": "Jane Doe", "email": "..." }],
      "alert_count": 3,
      "escalation_level": 1,
      "last_status_change": "2026-02-16T03:05:00Z"
    }
  ],
  "summary": "3 active incident(s): high (triggered) x1, high (acknowledged) x1, low (triggered) x1"
}
```

---

#### `detail <incident_id>` — 事件详细信息

显示事件的完整详细信息，包括时间线（日志条目）、相关警报和自动化分析结果。

**示例输出（简略版）：**
```json
{
  "tool": "pd_incident_detail",
  "incident": {
    "id": "P123ABC",
    "title": "High CPU on prod-web-03",
    "status": "triggered",
    "urgency": "high",
    "service": { "id": "PSVC123", "name": "Production Web" },
    "escalation_policy": { "name": "Production Escalation" },
    "assignments": [{ "name": "Jane Doe", "escalation_level": 1 }]
  },
  "timeline": [
    { "type": "trigger_log_entry", "created_at": "...", "summary": "Incident triggered via Prometheus Alertmanager" },
    { "type": "escalate_log_entry", "created_at": "...", "summary": "Escalated to Jane Doe (Level 1)" }
  ],
  "alerts": [
    { "id": "A456DEF", "severity": "critical", "summary": "CPU > 95% on prod-web-03", "source": "Prometheus Alertmanager" }
  ],
  "notes": [],
  "analysis": {
    "alert_count": 3,
    "escalation_count": 1,
    "acknowledged": false,
    "trigger_source": "Prometheus Alertmanager"
  }
}
```

---

#### `oncall` — 值班安排

显示当前在所有值班安排和升级策略中负责的人员。

**示例输出：**
```json
{
  "tool": "pd_oncall",
  "oncalls": [
    {
      "user": { "name": "Jane Doe", "email": "jane@company.com" },
      "schedule": { "name": "Primary SRE", "id": "PSCHED1" },
      "escalation_policy": { "name": "Production Escalation" },
      "escalation_level": 1,
      "start": "2026-02-15T17:00:00Z",
      "end": "2026-02-16T17:00:00Z"
    }
  ],
  "summary": "2 on-call assignment(s). Primary SRE: Jane Doe. Secondary SRE: Bob Smith."
}
```

---

#### `services` — 列出服务

列出所有 PagerDuty 服务及其当前的运行状态。

**示例输出：**
```json
{
  "tool": "pd_services",
  "services": [
    {
      "id": "PSVC123",
      "name": "Production Web",
      "status": "critical",
      "description": "Production web application servers",
      "escalation_policy": "Production Escalation",
      "integrations": ["Prometheus Alertmanager", "CloudWatch"]
    }
  ],
  "summary": "12 services: 1 critical, 1 warning, 10 active, 0 disabled"
}
```

---

#### `recent` — 最近的事件记录

显示某个服务或所有服务的最近事件及其统计信息。

**标志说明：**
| 标志 | 默认值 | 说明 |
|------|---------|-------------|
| `--service <id>` | all | 过滤到特定的 PagerDuty 服务 ID |
| `--since <window>` | `24h` | 时间范围：24 小时、7 天或 30 天 |

**示例输出：**
```json
{
  "tool": "pd_recent",
  "period": "last 24 hours",
  "service": "PSVC123",
  "incidents": [ ... ],
  "stats": {
    "total": 5,
    "by_urgency": { "high": 2, "low": 3 },
    "by_status": { "resolved": 4, "triggered": 1 },
    "mean_time_to_resolve_minutes": 42
  }
}
```

---

### 写入操作（⚠️ 需要 `--confirm`）

这些操作会修改 PagerDuty 中的事件状态。**必须** 使用 `--confirm` 标志，并设置 `PAGERDUTY_EMAIL`。如果没有 `--confirm`，工具会显示它“将”执行的操作然后退出。

---

#### `ack <incident_id> --confirm` — 确认事件

确认被触发的事件，停止进一步的升级流程。

**示例输出（无 `--confirm` 时）：**
```json
{
  "error": "confirmation_required",
  "message": "⚠️ ACKNOWLEDGE INCIDENT — --confirm flag is required to proceed.",
  "incident": { "id": "P123ABC", "title": "High CPU on prod-web-03", "urgency": "high" },
  "hint": "Re-run with --confirm to acknowledge this incident."
}
```

**使用 `--confirm` 时：**
```json
{
  "tool": "pd_incident_ack",
  "incident_id": "P123ABC",
  "status": "acknowledged",
  "acknowledged_at": "2026-02-16T03:46:00Z",
  "acknowledged_by": "jane@company.com"
}
```

---

#### `resolve <incident_id> --confirm` — 解决事件

解决事件，并将其标记为已修复。

**确认方式与 `ack` 相同**。没有 `--confirm` 时，仅显示事件详细信息并退出；使用 `--confirm` 时，解决事件并返回确认信息。

---

#### `note <incident_id> --content "text" --confirm` — 为事件添加备注

在事件的时间线上添加永久性备注。

**标志说明：**
| 标志 | 是否必需 | 说明 |
|------|----------|-------------|
| `--content <text>` | 是 | 要添加的备注内容 |
| `--confirm` | 是 | 确认操作 |

**示例输出：**
```json
{
  "tool": "pd_incident_note",
  "incident_id": "P123ABC",
  "note_id": "PNOTE456",
  "content": "Root cause: memory leak in auth-service v2.14.3. Rolling back.",
  "created_at": "2026-02-16T04:00:00Z",
  "user": "Jane Doe"
}
```

## 事件分拣工作流程

当用户需要帮助分拣事件时，请按照以下流程操作：

### 第一步：评估情况
```
→ pager-triage incidents
```
列出所有活动事件，按紧急程度（从高到低）和持续时间（从旧到新）排序。

### 第二步：深入分析关键事件
```
→ pager-triage detail <incident_id>
```
获取事件的时间线、相关警报和备注，确定事件的触发原因和升级历史。

### 第三步：与其他工具配合使用

如果可用，使用相关工具调查根本原因：
- **prom-query** → 通过 Prometheus 查询底层指标（CPU、内存、延迟、错误率）；
- **kube-medic** → 检查 Kubernetes 中的 Pod 健康状况、重启情况、OOMKills 和节点状态；
- **log-dive** → 在事件发生的时间范围内搜索应用程序日志中的错误。

### 第四步：采取行动
```
→ pager-triage ack <incident_id> --confirm        # Stop escalation while investigating
→ pager-triage note <incident_id> --content "..." --confirm   # Document findings
→ pager-triage resolve <incident_id> --confirm     # Mark as fixed
```

### 代理使用指南
- 当用户询问 “出了什么问题？” 时，先使用 `incidents` 命令；
- 当用户提到特定事件时，使用 `detail` 命令；
- 在进行事件分拣时，先显示事件列表，再显示最紧急事件的详细信息；
- 在进行关联分析时，如果已安装相关工具，建议使用 `prom-query` 或 `kube-medic`；
- **在执行写入操作前** **务必** 显示确认预览；
- **未经用户明确请求，** **切勿** 确认或解决事件。

### Discord v2 交付模式（OpenClaw v2026.2.14+）

当对话在 Discord 频道中进行时：

- 首先发送简洁的回复（活动事件数量、最紧急的事件以及推荐的下一步操作），然后询问用户是否需要查看详细信息；
- 保持首次回复的字符数在 1200 个以内，避免在首条消息中显示完整的时间线内容；
- 如果支持 Discord 组件，提供以下快速操作：
  - `Deep Dive Incident`（深入分析事件）
  - `Acknowledge Incident`（确认事件）
  - `Add Incident Note`（添加事件备注）；
- 如果不支持相关组件，以编号列表的形式提供相同的操作选项；
- 对于事件时间线和警报列表，建议使用简短的回复（每条消息不超过 15 行）。

## 安全注意事项

- **API 密钥** 仅从环境变量中读取，不会被记录、显示或包含在输出中；
- **默认为只读模式** — 5 个读取命令可以使用任何 API 密钥；3 个写入命令需要 `--confirm` 标志；
- **确认机制** — 写入操作会显示完整的事件上下文，如果没有 `--confirm` 标志，则拒绝执行操作；
- 我们建议在事件分拣工作流程中首先使用 **只读权限的 PagerDuty API 密钥**；
- 有关完整的威胁模型和 RBAC 建议，请参阅 [SECURITY.md](./SECURITY.md)。

## OpsGenie 支持（计划中）

OpsGenie 的集成计划在未来的版本中实现。当设置了 `OPSGENIE_API_KEY` 时，相同的子命令将映射到 OpsGenie 的 REST API，并采用标准化的输出格式。

---

<sub>由 [Anvil AI](https://anvil-ai.io) 提供支持 · 专为凌晨 3 点被通知的工程师设计</sub>