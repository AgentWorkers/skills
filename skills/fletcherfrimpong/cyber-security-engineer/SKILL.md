---
name: cyber-security-engineer
description: OpenClaw权限治理与安全加固的安全工程工作流程：该流程包括实施最小权限原则（即仅授予用户执行所需任务所需的权限）、所有特权操作均需经过审批、设置空闲超时机制、监控网络端口和数据输出流量，并生成符合ISO 27001/NIST标准的安全合规报告及相应的风险缓解措施。
---

# 网络安全工程师

## 要求

**环境变量（可选，但会记录在文档中）：**
- `OPENCLAW.require_POLICY_FILES`
- `OPENCLAW.require_SESSION_ID`
- `OPENCLAW_TASK_SESSION_ID`
- `OPENCLAW_APPROVAL_TOKEN`
- `OPENCLAW_UNTRUSTED_SOURCE`
- `OPENCLAW_VIOLATION_NOTIFY_CMD`

**工具：** 使用 `python3` 以及 `lsof`、`ss` 或 `netstat` 进行端口检查。

**策略文件（由管理员审核）：**
- `~/.openclaw/security/approved_ports.json`
- `~/.openclaw/security/command-policy.json`
- `~/.openclaw/security/egress_allowlist.json`
- `~/.openclaw/security/prompt-policy.json`

在所有涉及安全性的任务中实施以下控制措施：

1. 在正常（非 root）模式下执行所有操作。
2. 在执行任何需要提升权限的命令之前，必须获得用户的明确批准。
3. 将权限提升限制在当前任务所需的最低命令集范围内。
4. 一旦特权命令执行完成，立即恢复到普通权限状态。
5. 如果 30 分钟内没有活动，权限状态将自动失效，需要重新获得批准。
6. 监控网络监听端口，并标记不安全或未经批准的端口。
7. 监控出站连接，并标记那些不在出站允许列表中的目标地址。
8. 如果没有已批准的策略文件，使用 `python3 scripts/generate_approved_ports.py` 生成一个策略文件，然后进行审核和优化。
9. 根据 ISO 27001 和 NIST 标准对这些控制措施进行评估，并报告违规情况以及相应的缓解措施。

## 非目标（网页浏览）

- 本技能不包含网页浏览或网络搜索的功能。评估和建议应基于本地主机/OpenClaw 的状态以及本技能中提供的参考资料。

## 需要使用的文件**

- `references/least-privilege-policy.md`
- `references/port-monitoring-policy.md`
- `references/compliance-controls-map.json`
- `references/approved_ports.template.json`
- `references/command-policy.template.json`
- `references/prompt-policy.template.json`
- `references/egress-allowlist.template.json`
- `scripts/preflight_check.py`
- `scripts/root_session_guard.py`
- `scripts/audit_logger.py`
- `scripts/command_policy.py`
- `scripts/prompt_policy.py`
- `scripts/guarded_privileged_exec.py`
- `scripts/install-openclaw-runtime-hook.sh`
- `scripts/port_monitor.py`
- `scripts/generate_approved_ports.py`
- `scripts/egress_monitor.py`
- `scripts/notify_on_violation.py`
- `scripts/compliance_dashboard.py`
- `scripts/live_assessment.py`

## 行为规范

- 在不相关的任务之间，不得保持 root 权限或提升后的权限状态。
- 在当前操作流程中，未经明确批准，不得执行 root 命令。
- 按照配置的策略执行命令的允许/拒绝操作。
- 当检测到不可信的内容来源时（`OPENCLAW_UNTRUSTED_SOURCE=1`），必须要求用户确认。
- 当配置了会话 ID 限制时（`OPENCLAWRequire_SESSION_ID=1`），必须遵循相应的规则。
- 如果超时，强制会话失效并重新请求批准。
- 将特权操作记录到 `~/.openclaw/security/privileged-audit.jsonl` 文件中（尽可能做到）。
- 标记那些不在已批准策略文件中的监听端口，并推荐安全的替代方案。
- 标记那些不在出站允许列表中的出站目标地址。

## 输出规范

在报告状态时，应包括以下内容：

- 受影响的特定 `check_id`、`status`、`risk` 以及详细的证据。
- 具体的缓解措施（需要更改的内容、位置）以及相关的责任人或截止日期（如果有的话）。
- 对于网络问题，应提供端口、绑定地址、进程/服务信息，以及标记为不安全或公开的原因。