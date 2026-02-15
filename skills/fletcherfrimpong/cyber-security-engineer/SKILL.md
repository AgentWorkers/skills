---
name: cyber-security-engineer
description: >
  OpenClaw的权限治理与安全加固工作流程：  
  该流程旨在实现最小权限原则（即用户仅拥有执行所需操作的权限），所有需要提升权限的操作均需经过审批；同时包含空闲超时控制机制、端口及数据流出口的监控功能，并确保系统符合ISO 27001/NIST安全标准。具体措施包括：  
  1. **最小权限原则（Least Privilege Principle）**：确保用户仅拥有执行其工作所需的最小权限，以降低安全风险。  
  2. **审批机制（Approval Process）**：所有需要提升权限的操作都必须经过正式审批，确保权限使用的合理性。  
  3. **空闲超时控制（Idle Timeout Mechanism）**：设置用户账户的闲置超时时间，长时间未活动的账户将被自动锁定，防止未经授权的访问。  
  4. **端口与数据流出口监控（Port and Egress Monitoring）**：实时监控系统所有端口的活动情况，及时发现异常行为。  
  5. **合规性报告（Compliance Reporting）**：生成符合ISO 27001/NIST标准的合规性报告，以便进行安全审计和持续改进。  
  通过这些措施，OpenClaw能够有效提升系统的安全性，降低潜在的安全风险。
---
# 网络安全工程师

## 要求

**环境变量（可选，但需记录）：**
- `OPENCLAW.require_POLICY FILES`
- `OPENCLAW.require_SESSION_ID`
- `OPENCLAW_TASK_SESSION_ID`
- `OPENCLAW_APPROVAL_TOKEN`
- `OPENCLAW_UNTRUSTED_SOURCE`
- `OPENCLAW_VIOLATION_NOTIFY_CMD`
- `OPENCLAW_VIOLATION_NOTIFY_ALLOWLIST`

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
4. 特权命令执行完成后，立即恢复到普通用户权限状态。
5. 如果系统处于提升权限状态超过 30 分钟未活动，系统将自动恢复到普通权限状态，并要求重新获得批准。
6. 监控系统正在监听的网络端口，标记任何不安全或未经批准的端口。
7. 监控所有出站连接，标记那些不在出站允许列表中的目标地址。
8. 如果没有已批准的策略文件，使用 `python3 scripts/generate_approved_ports.py` 生成一个策略文件，随后对其进行审核和优化。
9. 根据 ISO 27001 和 NIST 标准对这些控制措施进行评估，并报告任何违规行为及相应的缓解措施。

## 非目标（禁止网页浏览）：
- 严禁在执行此任务时使用网页浏览或网络搜索功能。所有评估和建议应基于本地主机/OpenClaw 的当前状态以及本文档中提供的参考资料。

## 需要使用的文件：
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

## 行为规范：
- 在不同的任务之间，切勿保持 root 权限或提升后的权限状态。
- 在当前操作流程中，未经明确批准，严禁执行 root 命令。
- 按照配置好的策略执行命令的允许/拒绝规则。
- 当检测到不可信的内容来源时（`OPENCLAW_UNTRUSTED_SOURCE=1`），必须要求用户确认。
- 如果配置了会话 ID 限制（`OPENCLAW.require_SESSION_ID=1`），则必须严格执行该规则。
- 如果超时发生，系统将强制结束当前会话并要求重新获得批准。
- 将所有特权操作记录到 `~/.openclaw/security/privileged-audit.jsonl` 文件中（尽可能做到详细记录）。
- 对于不在已批准策略文件中的监听端口，应标记为不安全，并推荐安全的替代方案。
- 对于不在出站允许列表中的出站连接目标地址，也应标记为不安全。

## 输出规范：
在报告状态时，需包含以下信息：
- 受影响的特定检查项（`check_id`）、状态、风险等级以及详细的证据。
- 具体的缓解措施（需要修改的内容、修改位置），以及相关负责人和截止日期（如果有的话）。
- 对于网络问题的发现，需提供端口号、绑定地址、相关进程/服务信息，以及标记为不安全或公开的原因。