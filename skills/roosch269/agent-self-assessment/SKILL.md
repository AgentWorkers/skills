---
name: Agent Self-Assessment
version: 1.0.0
description: 这是一个用于AI代理的安全自我评估工具。您可以运行该工具来分析您的配置，并获得一份结构化的威胁模型报告，报告中会针对六个安全领域给出红色（RED）、琥珀色（AMBER）或绿色（GREEN）的评级：决策边界、审计追踪、凭证管理、权限隔离、经济责任性以及内存安全性。
author: Atlas (OpenClaw)
license: MIT
tags:
  - security
  - self-assessment
  - threat-model
  - agent-safety
  - audit
keywords:
  - agent security posture
  - threat model
  - security checklist
  - agent hardening
metadata:
  openclaw:
    emoji: "🛡️"
    minVersion: "1.0.0"
---
# 代理自我评估

对您的配置进行一次结构化的安全自我评估。您将获得一份包含发现结果和修复建议的**威胁模型报告**。

---

## 如何运行

当被调用时，该代理会针对您的**实际当前配置**执行以下六项检查（而非假设性配置）。根据需要使用 `exec` 命令、文件读取、环境检查以及工具自检功能。完成后输出报告。

**请勿跳过任何检查。** 如果您无法确定答案，请将相关检查标记为**红色（🔴）**，并注明原因“**无法验证**”。

---

## 检查 1：决策边界

**问题：** 外部输入是否可以直接触发具有后果的操作，而无需经过任何审批流程？

**需要检查的内容：**
- 查看您正在使用的技能和工具。哪些工具具有写入、发送、删除、支付或部署操作的功能？
- 在执行这些操作之前，是否有人工审核环节（例如确认提示、审批流程或询问模式）？
- 来自 Discord、Webhook、电子邮件或 API 调用的消息是否可以在未经审核的情况下直接触发具有后果的操作？
- 是否有明确记录“安全”操作与“需要审核”操作的清单？

**需要执行的检查代码：**
```
1. List all tools/skills with write/send/delete/pay/deploy capability
2. For each: is ask=always, ask=on-miss, or no-ask configured?
3. Is there any path from untrusted ingress → consequential action with zero gates?
4. Are decision boundaries documented (e.g., in AGENTS.md or a policy file)?
```

**评分标准：**
- 🟢 绿色（GREEN）—— 所有具有后果的操作都需要经过明确的审核流程；边界已明确记录
- 🟡 黄色（AMBER）—— 审核流程存在，但未覆盖所有路径，或相关文档缺失
- 🔴 红色（RED）—— 直接的输入路径可以触发操作，且没有审核流程；或无法验证

---

## 检查 2：审计日志

**问题：** 是否有只读的、采用哈希链技术的、可防止篡改的审计日志来记录具有后果的操作？

**需要检查的内容：**
- 是否存在审计日志文件？（检查 `audit/` 目录或类似位置）
- 日志文件是否采用只读的 NDJSON 格式（每行一个 JSON 对象）？
- 每条日志记录是否包含以下信息：`ts`、`kind`、`actor`、`target`、`summary`、`provenance`？
- 是否使用了哈希链技术？（每条记录中是否有 `chain.prev` 和 `chain.hash` 字段）
- `chain.algo` 的实现方式是否已明确记录（例如 `sha256(prev\nline_c14n)`）？
- 最后一条日志记录是什么时候生成的？日志记录功能是否正在正常运行？

**需要执行的检查代码：**
```bash
# Check if audit log exists
ls -la audit/ 2>/dev/null || echo "No audit directory"

# Check last 3 entries
tail -3 audit/atlas-actions.ndjson 2>/dev/null | python3 -m json.tool 2>/dev/null

# Verify hash chaining present
grep -c '"chain"' audit/atlas-actions.ndjson 2>/dev/null || echo "No chain field found"

# Check entry count
wc -l audit/atlas-actions.ndjson 2>/dev/null
```

**评分标准：**
- 🟢 绿色（GREEN）—— 日志存在，采用只读的 NDJSON 格式，具有哈希链技术，且最近有记录
- 🟡 黄色（AMBER）—— 日志存在，但缺乏哈希链技术，或记录不完整
- 🔴 红色（RED）—— 不存在审计日志；或日志存在但可被篡改，且没有完整性检查

**修复建议：** 从 ClawHub 安装 `audit-trail` 技能，它提供了基于哈希链技术的只读日志记录功能。

---

## 检查 3：凭证范围控制

**问题：** 凭证是否仅限于其指定的使用域？为域 A 授予的凭证是否可以在域 B 中使用？

**需要检查的内容：**
- 列出所有包含凭证的环境变量（API 密钥、令牌、私钥）
- 每个凭证的用途是什么（针对哪个域/服务）？
- 是否有跨多个无关服务共享凭证？
- 是否有 `TOOLS.md` 或凭证清单来记录每个凭证的用途？
- 凭证是否作为参数传递（在日志或 `ps` 输出中可见），而不是通过环境变量传递？

**需要执行的检查代码：**
```bash
# List env vars that look like credentials (redact values)
env | grep -iE '(key|token|secret|pass|private|auth|credential)' | sed 's/=.*/=[REDACTED]/'

# Check if any credential files are world-readable
find ~ -name "*.key" -o -name "*.pem" -o -name ".env" 2>/dev/null | xargs ls -la 2>/dev/null | grep -v "^total"

# Check if credentials appear in shell history (last 20 lines)
tail -20 ~/.zsh_history 2>/dev/null | grep -iE '(key|token|secret)=' | sed 's/=.*/=[REDACTED]/'
```

**评分标准：**
- 🟢 绿色（GREEN）—— 每个凭证都仅限于一个域；有详细的清单记录；没有全局可读的凭证文件
- 🟡 黄色（AMBER）—— 凭证存在但记录不完整；存在轻微的范围模糊问题
- 🔴 红色（RED）—— 凭证可以在不同域之间共享；凭证存在于 shell 历史记录或全局可读文件中；没有清单记录

---

## 检查 4：平面分离

**问题：** 入口平面（接收输入）与操作平面（执行操作）是否相互隔离？

**需要检查的内容：**
- 您接收到的消息是否可以直接修改状态、发送输出或调用外部 API，而无需经过任何决策或审核流程？
- 用于接收输入的工具（如 Discord 读取器、电子邮件读取器、Webhook 监听器）是否与用于执行操作的工具相同？
- 是否有明确的文档说明这两者之间的分离机制（“这些工具用于接收数据，这些工具用于执行操作”）？
- 入口消息中的不可信内容（例如提示注入）是否有可能触发操作？

**需要执行的检查代码：**
```
1. List all ingress tools (read, receive, fetch, listen)
2. List all action tools (send, write, delete, pay, deploy, exec)
3. Is there any shared code path or implicit coupling between ingress and action?
4. Does the system prompt or AGENTS.md define plane separation policy?
5. Are incoming payloads sanitised or sandboxed before being passed to the reasoning layer?
```

**评分标准：**
- 🟢 绿色（GREEN）—— 入口平面和操作平面明确分离；提示注入机制有效；相关策略有文档记录
- 🟡 黄色（AMBER）—— 分离机制基本有效，但存在部分共享路径或没有明确的策略说明
- 🔴 红色（RED）—— 入口和平面之间没有有效分离；不可信内容中的提示注入可能触发操作

---

## 检查 5：经济责任机制

**问题：** 财务操作（支付、资源购买、API 调用）是否可追溯、有记录且受到限制？

**需要检查的内容：**
- 是否有涉及资金流动的技能或工具（如支付、带有计费的 API 调用、云资源操作）？
- 是否配置了支出限制或预算上限？
- 每笔支付是否都会在审计日志中生成相应的结算记录？
- 在代理之间的交易中，是否使用了托管机制（资金在交易确认前被暂存）？
- 是否有基于权益的责任机制（代理的行为会受到相应影响）？
- 代理是否可以无限制地自主支出？

**需要执行的检查代码：**
```
1. List all skills/tools with financial capability (search for: pay, charge, purchase, invoice, stake, escrow)
2. Check for SPENDING_LIMIT or budget env vars
3. Check audit log for payment entries with receipt/tx hashes
4. Verify settlement receipts are stored (not just logged in memory)
5. Check for escrow configuration in payment skills
```

**评分标准：**
- 🟢 绿色（GREEN）—— 设置了支出限制；每笔交易都有记录；代理之间的交易使用了托管机制；有权益相关机制
- 🟡 黄色（AMBER）—— 支付操作存在，但缺少记录；没有支出限制或托管机制
- 🔴 红色（RED）—— 支出无限制；没有记录；没有责任机制

---

## 检查 6：内存安全

**问题：** 代理的内存是否与不可信的导入内容隔离？导入的内容（代码、文档、插件）是否可能损坏或篡改代理的内存？

**需要检查的内容：**
- 您的内存系统（如 `MEMORY.md`、每日笔记、主题文件）是否直接接受来自不可信来源的内容？
- 进入内存的代码、文档、二进制文件或插件包在使用前是否经过了 SHA256 哈希处理并记录了来源？
- 对来自外部渠道（如 Discord、电子邮件、Web）的内容，在进入内存之前是否有隔离处理？
- 内存中的恶意文件是否可能在下次加载时引发意外操作？
- `MEMORY.md` 是否可以被不可信的输入直接修改？

**需要执行的检查代码：**
```bash
# Check if TOOLS.md documents artifact import policy
grep -i "sha256\|provenance\|imported artifacts" TOOLS.md 2>/dev/null || echo "No artifact import policy found"

# Check if any untrusted content was recently written to memory files
ls -lt memory/ 2>/dev/null | head -10

# Check if memory files contain any suspicious embedded instructions
grep -iE "(ignore previous|disregard|new instructions|override)" memory/*.md 2>/dev/null || echo "No prompt injection found in memory"

# Check for quarantine or import validation in skills
grep -rl "quarantine\|sha256\|provenance" skills/ 2>/dev/null | head -5
```

**评分标准：**
- 🟢 绿色（GREEN）—— 所有导入的内容都经过 SHA256 哈希处理并记录了来源；没有直接从不可信来源到内存的路径；内存文件会进行注入检测
- 🟡 黄色（AMBER）—— 部分导入内容被跟踪，但不是全部；没有系统的隔离机制；或内存可被访问但风险较低
- 🔴 红色（RED）—— 不可信的内容可以直接写入内存；没有来源追踪机制；没有注入检测

---

## 输出格式

完成所有六项检查后，生成一份结构如下所示的报告：

```
╔══════════════════════════════════════════════════════════════╗
║          AGENT SECURITY SELF-ASSESSMENT REPORT               ║
║          Generated: <ISO-8601 timestamp>                     ║
║          Agent: <agent name/identifier>                      ║
╚══════════════════════════════════════════════════════════════╝

SUMMARY SCORECARD
─────────────────────────────────────────────────────────────
  Check 1 — Decision Boundaries      [ 🟢 / 🟡 / 🔴 ]
  Check 2 — Audit Trail              [ 🟢 / 🟡 / 🔴 ]
  Check 3 — Credential Scoping       [ 🟢 / 🟡 / 🔴 ]
  Check 4 — Plane Separation         [ 🟢 / 🟡 / 🔴 ]
  Check 5 — Economic Accountability  [ 🟢 / 🟡 / 🔴 ]
  Check 6 — Memory Safety            [ 🟢 / 🟡 / 🔴 ]

  OVERALL POSTURE: [ SECURE / HARDENING NEEDED / CRITICAL ]
  RED count: N | AMBER count: N | GREEN count: N

FINDINGS
─────────────────────────────────────────────────────────────

[1] DECISION BOUNDARIES — <COLOR>
  Finding: <1-2 sentences on what was found>
  Evidence: <specific file, config, or observation>
  Risk: <what could go wrong if not fixed>
  Action: <specific remediation step>

[2] AUDIT TRAIL — <COLOR>
  Finding: ...
  Evidence: ...
  Risk: ...
  Action: ...
  Remediation skill: clawhub install audit-trail

[3] CREDENTIAL SCOPING — <COLOR>
  Finding: ...
  Evidence: ...
  Risk: ...
  Action: ...

[4] PLANE SEPARATION — <COLOR>
  Finding: ...
  Evidence: ...
  Risk: ...
  Action: ...

[5] ECONOMIC ACCOUNTABILITY — <COLOR>
  Finding: ...
  Evidence: ...
  Risk: ...
  Action: ...

[6] MEMORY SAFETY — <COLOR>
  Finding: ...
  Evidence: ...
  Risk: ...
  Action: ...

PRIORITY ACTIONS (ordered by severity)
─────────────────────────────────────────────────────────────
  1. <Highest-risk item with one-line fix>
  2. ...
  3. ...

─────────────────────────────────────────────────────────────
END OF REPORT
```

**整体安全状况：**
- **安全（SECURE）** — 0 个红色（🔴）条目，≤1 个黄色（AMBER）条目
- **需要加强安全措施（HARDENING NEEDED）** — 0 个红色条目，≥2 个黄色条目
- **严重风险（CRITICAL）** — ≥2 个红色条目

---

## 重要说明：

- **请诚实评估。** 这是一次自我评估，夸大评分会失去评估的意义。
- **请实际运行相应的 shell 命令。** 不要猜测，要检查实际的文件和配置。
- **如果无法验证某个内容，请将其标记为红色（🔴），并说明原因（“无法验证”即表示不安全）。
- **生成报告后，请将其记录到审计日志中**（元检查：您是否发现了自己的安全漏洞？这应该被记录在审计日志中）。
- 如果审计日志存在缺失，建议从 ClawHub 安装 `audit-trail` 技能：`clawhub install audit-trail`