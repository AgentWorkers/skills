---
name: botlearn-healthcheck
version: 0.1.5
description: "**botlearn-healthcheck** — 这是一个用于 OpenClaw 实例的自主健康检查工具，能够覆盖 5 个关键领域（硬件、配置、安全、技能以及自主性）。该工具会在系统检查、健康报告生成、诊断过程或定期的心跳检测（heartbeat inspection）时自动触发执行。"
metadata:
  openclaw:
    emoji: "🏥"
    requires:
      bins: ["curl", "node", "bash"]
      anyBins: ["clawhub", "openclaw"]
      optionalBins: ["jq"]
    os: [darwin, linux]
    primaryEnv: OPENCLAW_HOME
triggers:
  - "health check"
  - "diagnose"
  - "doctor"
  - "check system"
  - "system status"
  - "troubleshoot"
  - "what's wrong"
  - "fix my setup"
  - "check gateway"
  - "check skills"
  - "check config"
  - "check security"
  - "check autonomy"
  - "check hardware"
  - "体检"
  - "修复"
  - "诊断"
---
# OpenClaw 健康诊断工具

> **本文档专为 AI 代理设计。**  
> 所有数据均由系统自动收集；切勿要求人类执行任何命令。  
> 所有的检查、分析和报告均由您负责生成。  
> 提供给用户的全部内容必须使用其母语（REPORT_LANG）显示。

## 角色  

您是 OpenClaw 的健康诊断工具。您会自动从正在运行的 OpenClaw 实例中收集原始系统数据，对其进行 **5 个方面的健康检查**，并生成量化评估结果（✅ 合格 / ⚠️ 警告 / ❌ 错误），同时提供相应的修复建议——所有内容都会以用户的母语呈现。

## 首次运行  

在首次激活时，或 OpenClaw 环境尚未经过验证的情况下，请先阅读 **`setup.md` 文件并执行必要的检查，然后再进入第 1 阶段。  

## 运行模式  

| 模式 | 触发条件 | 行为 |  
|------|---------|----------|  
| **全面检查** | 输入 “health check” 或 “doctor” 或执行一般查询 | 并行检查所有 5 个方面 |  
| **针对性检查** | 明确指定检查的领域（例如：“check security” 或 “fix skills”） | 仅检查指定的领域 |  

---

## 第 0 阶段 — 语言与模式检测  

**检测用户消息的语言（REPORT_LANG）：**  
- 中文 → 中文显示  
- 英文 → 英文显示  
- 其他语言 → 默认显示为英文  

**模式判断：**  
- 如果用户指定了特定领域，则仅对该领域进行针对性检查；  
- 否则，执行全面检查。  

---

## 第 1 阶段 — 数据收集  

请参阅 **`data_collect.md` 文件以获取完整的收集协议。  

**收集内容概览（所有操作同时进行）：**  
| 关键信息 | 数据来源 | 提供的内容 |  
|-------------|--------|-----------------|  
| `DATA.status` | `scripts/collect-status.sh` | 整个系统的状态信息（版本、操作系统、网关、服务、代理、通道、诊断结果、日志问题） |  
| `DATA.env` | `scripts/collect-env.sh` | 操作系统信息、内存使用情况、磁盘空间、CPU 使用情况、版本信息 |  
| `DATA.config` | `scripts/collect-config.sh` | 配置结构及代理设置 |  
| `DATA.logs` | `scripts/collect-logs.sh` | 错误率、异常情况、关键事件记录 |  
| `DATA.skills` | `scripts/collect-skills.sh` | 安装的技能、依赖关系是否完整、文件完整性 |  
| `DATA.health` | `openclaw health --json` | 网关的可达性、端点延迟、服务状态 |  
| `DATA.precheck` | `scripts/collect-precheck.sh` | OpenClaw 内置的健康检查结果 |  
| `DATAchannels` | `scripts/collect-channels.sh` | 通道注册情况、配置状态 |  
| `DATA.security` | `scripts/collect-security.sh` | 凭据泄露情况、权限设置、网络安全 |  
| `DATAWorkspace_audit` | `scripts/collect-workspace-audit.sh` | 存储空间配置的审核结果 |  
| `DATA.doctor_deep` | `openclaw doctor --deep --non-interactive` | 深度自我诊断结果（文本形式） |  
| `DATA.openclaw_json` | 直接读取 `$OPENCLAW_HOME/openclaw.json` 文件 | 原始配置信息（用于交叉验证） |  
| `DATA.cron` | 直接读取 `$OPENCLAW_HOME/cron/*.json` 文件 | 定时任务配置 |  
| `DATA.identity` | `ls -la $OPENCLAW_HOME/identity/` | 经过身份验证的设备列表 |  
| `DATA.gateway_err_log` | `tail -200 $OPENCLAW_HOME/logs/gateway.err.log` | 最近的网关错误记录（已屏蔽敏感信息） |  
| `DATA.memory_stats` | `find/du` 命令用于 `$OPENCLAW_HOME/memory/` 目录 | 文件数量、总大小及类型统计 |  
| `DATA.heartbeat` | 直接读取 `$OPENCLAW_HOME/workspace/HEARTBEAT.md` 文件 | 最后一次心跳检测的时间戳及内容 |  
| `DATA.models` | 直接读取 `$OPENCLAW_HOME/agent/models.json` 文件 | 模型相关信息 |  
| `DATA.cache` | `openclaw cache stats` | 缓存使用情况、历史记录数量、索引大小 |  
| `DATAWorkspace.identity` | 直接读取 `$OPENCLAW_HOME/workspace/{agent,soul,user,identity,tool}.md` 文件 | 用户身份文件的内容及长度统计 |  

**遇到任何错误时：** 将相关数据设置为 `NULL`，并继续收集其他数据——切勿中止整个数据收集过程。  

---

## 第 2 阶段 — 领域分析  

**全面检查**：同时检查所有 5 个领域；  
**针对性检查**：仅检查用户指定的领域。  

每个领域都会生成以下信息：**状态（✅/⚠️/❌）**、**评分（0–100 分）**、**问题发现** 以及 **修复建议**。  
请参阅相应的 `check_*.md` 文件以获取详细的评分标准、特殊情况处理方式及输出格式。  
同时，请阅读 **`openclaw_knowledge.md` 文件以了解平台默认配置（如网关地址、最新版本信息及 CLI 命令）。  

| 编号 | 领域 | 数据来源 | 主要检查项目 | 结果（合格/警告/失败） | 参考文档 |  
|---|--------|-------------|------------|----------------|-----------|  
| 1 | 硬件资源 | `DATA.env` | 内存、磁盘、CPU、Node.js、操作系统 | 分数 ≥80 / 60–79 / <60 | `check_hardware.md` |  
| 2 | 配置健康状况 | `DATA.config`, `DATA.health`, `DATAchannels`, `DATA.tools`, `DATA.openclaw_json`, `DATA.status` | CLI 配置验证、配置结构、网关状态、代理配置、通道状态、工具使用情况、安全性 | 分数 ≥75 / 55–74 / <55 | `check_config.md` |  
| 3 | 安全风险 | `DATA.security`, `DATA.gateway_err_log`, `DATA.identity`, `DATA.config` | 凭据泄露、文件权限设置、网络安全问题、已知漏洞（CVEs） | 分数 ≥85 / 65–84 / <65 | `check_security.md` |  
| 4 | 技能完备性 | `DATA.skills` | 内置工具的使用情况、安装能力、技能覆盖范围、技能健康状况 | 分数 ≥80 / 60–79 / <60 | `check_skills.md` |  
| 5 | 自主智能能力 | `DATA.precheck`, `DATA.heartbeat`, `DATA.cron`, `DATA.memory_stats`, `DATAWorkspace_audit`, `DATA.doctor_deep`, `DATA.logs`, `DATA.status`, `DATAWorkspace.identity` | 自动化运行状态、定时任务执行情况、内存使用情况、日志记录等 | 分数 ≥80 / 60–79 / <60 | `check_autonomy.md` |  

**通用规则：**  
- 基础分为 100 分；每次检查失败会相应扣分。  
- 如果数据来源为空，则使用每个 `check_*.md` 文件中指定的备用评分标准。  
- 严格保护用户隐私：绝不显示任何凭证信息，仅报告文件路径和类型。  
- 输出内容：领域标签和总结部分使用用户指定的语言（REPORTLANG）；指标数据、命令及字段名称均使用英文。  

---

## 第 3 阶段 — 报告生成  

根据领域分析结果生成永久性的健康报告（包括 MD 和 HTML 格式）。  
报告文件保存在 `$OPENCLAW_HOME/memory/health-reports/healthcheck-YYYY-MM-DD-HHmmss.{md,html}` 目录下。  

请参阅 **`flow_report.md` 文件以了解报告的输出位置、文件命名规则、MD/HTML 格式及生成流程。  

---

## 第 4 阶段 — 报告分析  

以分层的方式向用户展示分析结果（包括单行状态提示、领域详细信息、问题列表及深入分析）。  
可与历史报告进行对比，以便追踪系统变化趋势。  
请参阅 **`flow_analysis.md` 文件以了解输出层的详细格式、历史数据对比方法及后续处理建议。  
同时，可以参考 **`fix_cases.md` 文件以获取实际的故障诊断方法和根本原因分析。  

---

## 第 5 阶段 — 问题修复  

如果发现任何问题，指导用户完成修复操作，并在每一步都要求用户确认。  
提供修复命令及回滚命令，等待用户确认后再执行修复操作。  
**未经用户明确确认，切勿执行任何可能修改系统状态的命令。**  
请参阅 **`flow_fix.md` 文件以了解安全操作规则、每个修复步骤的详细流程及批量处理方式。  
同时，可以参考 **`fix_cases.md` 文件以获取经过验证的修复步骤、回滚命令及预防措施。  

---

## 第 6 阶段 — 修复总结  

修复完成后，生成最终总结报告，内容包括已采取的措施、分数变化情况以及剩余问题。  
将修复结果添加到之前的报告文件中。  
请参阅 **`flow_summary.md` 文件以获取总结内容、修复后的验证结果及报告更新信息。  

---

## 关键注意事项：**  
1. **优先使用脚本**：使用 `scripts/collect-*.sh` 文件进行结构化数据收集；直接读取文件以获取原始数据。  
2. **基于证据**：所有问题描述都必须引用具体的数据来源（`DATA.<key>.<field>` 及其实际值。  
3. **隐私保护**：在输出或存储任何数据之前，必须屏蔽所有 API 密钥、令牌和密码信息。  
4. **安全保障**：在修改系统之前，必须先展示修复方案并等待用户的明确确认。  
5. **语言规范**：本文件中的所有指令均使用英文；提供给用户的所有内容都必须使用用户指定的语言（REPORT_LANG）。