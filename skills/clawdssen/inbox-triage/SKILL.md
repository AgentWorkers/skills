---
name: inbox-triage
version: "1.0.0"
description: >
  **AI代理的电子邮件收件箱管理功能：**  
  - 扫描并分类邮件；  
  - 自动起草回复；  
  - 突出显示紧急事项；  
  - 将无关邮件归档。  
  支持Gmail和IMAP协议，帮助实现“零邮件收件箱”工作流程（即收件箱内无未处理邮件的状态）。
tags: [email, inbox, triage, gmail, imap, inbox-zero, email-management, urgency, draft-replies, notifications]
platforms: [openclaw, cursor, windsurf, generic]
category: communication
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---
# 收件箱分类管理 — 由 The Agent Ledger 提供

> **只需将此技能提供给您的智能助手即可。** 仅需粘贴代码，您的助手就能自动分类管理您的收件箱——无需编写代码、配置文件或设置 API。助手会阅读相关说明，然后完成其余工作。

这是一项专为 AI 助手设计的收件箱分类管理技能，它能扫描您的收件箱，根据邮件紧急程度对邮件进行分类，筛选出需要关注的内容，帮助您实现“收件箱归零”的目标——确保不会错过任何重要信息。

**版本：** 1.0.0  
**许可证：** CC-BY-NC-4.0  
**更多信息：** [theagentledger.com](https://www.theagentledger.com)

---

## 该技能的功能

当该技能被触发时，它会扫描未读邮件并生成一份**分类报告**：  
1. **🔴 紧急** — 需要立即人工处理（有截止日期或时间敏感的请求）  
2. **🟡 需要回复/决策** — 需要回复或做出决定，但不是紧急事项  
3. **🔵 供参考** — 信息性邮件，了解即可，无需采取行动  
4. **⚫ 噪音邮件** — 通讯邮件、促销信息、自动发送的通知（建议自动归档）  

报告会包含每封邮件的发件人、主题、简短摘要以及建议的处理方式。

---

## 先决条件

您需要具备通过命令行（CLI）访问电子邮件的权限。支持的访问方式如下：  

### 选项 A：通过 `gmailctl` 或 Google Apps Script 访问 Gmail  
- 安装 [gmailctl](https://github.com/mbrt/gmailctl) 或使用 Gmail API  
- 使用 OAuth 进行身份验证（仅读取权限即可满足分类需求）  

### 选项 B：通过 `himalaya` 访问 IMAP  
- 安装 [himalaya](https://github.com/pimalaya/himalaya)——一个 CLI 邮件客户端  
- 使用您的 IMAP 凭据进行配置  
- 支持 Gmail、Outlook、Fastmail 等所有 IMAP 服务  

### 选项 C：任何支持 CLI 的邮件工具  
- `mutt`、`neomutt`、`mblaze` 或自定义脚本  
- 只要您的助手能够执行列出未读邮件的命令，该技能即可使用  

**注意：** 该技能仅用于读取邮件，不会发送、删除或修改邮件内容，除非您明确配置了回复模板（详见“高级设置”部分）。

---

## 设置步骤  

### 第 1 步：验证邮件访问权限  

确认您的助手能够列出未读邮件：  
```bash
# himalaya example
himalaya envelope list --folder INBOX --filter new

# gmailctl example — or use a simple script
gmail-fetch --unread --limit 50
```  
请先在终端中手动测试该功能。如果测试成功，那么助手也能正常使用该技能。  

### 第 2 步：配置分类规则  

在您的助手的工作空间配置文件（`AGENTS.md` 或专门的 `inbox-config.md`）中添加分类规则：  
```markdown
## Inbox Triage Rules

### Urgency Signals (→ 🔴 Urgent)
- From: [boss@company.com, client@important.com]
- Subject contains: "urgent", "ASAP", "deadline", "EOD"
- Calendar invites for today

### Action Signals (→ 🟡 Action Needed)
- Direct questions addressed to me
- Replies to threads I started
- Invoices, contracts, documents requiring signature

### FYI Signals (→ 🔵 FYI)
- CC'd emails
- Team updates, status reports
- News digests I subscribe to

### Noise Signals (→ ⚫ Noise)
- Marketing emails, promotions
- Automated notifications (GitHub, CI/CD, service alerts)
- Newsletters I haven't read in 2+ weeks
```  
根据您的实际工作流程自定义这些规则。规则越具体，分类效果越好。  

### 第 3 步：设置触发条件  

**建议使用“心跳任务”进行定期检查：**  
将相关配置添加到 `HEARTBEAT.md` 文件中：  
```markdown
## Inbox Check
- Run inbox triage every 2-4 hours during work hours
- Only alert human for 🔴 Urgent items between checks
- Full triage report in morning briefing
```  

**使用 Cron 任务进行定时报告：**  
```
openclaw cron add --schedule "0 8,12,17 * * 1-5" --task "Run inbox triage, deliver report to main chat"
```  

**按需使用：**  
只需发送指令：“检查我的邮件”或“我的收件箱里有什么？”  

---

## 分类报告格式  

```
📬 Inbox Triage — [Date, Time]
[X] unread emails scanned

🔴 URGENT (2)
━━━━━━━━━━━━━
1. **[Sender]** — [Subject]
   → [One-line summary + recommended action]
2. **[Sender]** — [Subject]
   → [One-line summary + recommended action]

🟡 ACTION NEEDED (3)
━━━━━━━━━━━━━━━━━━━
1. **[Sender]** — [Subject]
   → [Summary + suggested response]
2. ...

🔵 FYI (5)
━━━━━━━━━━
• [Sender]: [Subject] — [1-line summary]
• ...

⚫ NOISE (12) — auto-archive candidates
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Count] promotions, [count] notifications, [count] newsletters
```  
根据使用渠道的不同，报告的详细程度也会有所不同。Telegram 会接收简化版的报告；而专门的收件箱频道则会收到完整的信息。  

---

## 自定义设置  

### 紧急程度评分  

为了更精细的分类管理，可以使用评分系统而非固定规则：  
| 信号 | 分数 |
|--------|--------|
| 发件人为 VIP 用户 | +3 |
| 主题中包含紧急关键词 | +2 |
| 直接发送给我（未抄送他人） | +1 |
| 提及截止日期 | +2 |
| 需要回复我的回复邮件 | +1 |
| 超过 24 小时未回复 | +1 |
| 来自自动发送工具或批量发送的邮件 | -3 |

- **5 分及以上** → 🔴 紧急  
- **2-4 分** → 🟡 需要回复/决策  
- **1 分** → 🔵 供参考  
- **0 分或负分** → ⚫ 噪音邮件  

### 回复模板（可选）  

如果您希望助手为需要回复的邮件生成回复模板：  
```markdown
## Reply Drafting Rules
- Draft replies for routine requests (meeting scheduling, info requests, acknowledgments)
- NEVER auto-send — always present drafts for human approval
- Match the sender's formality level
- Keep drafts under 3 sentences when possible
- Flag if a reply requires information you don't have
```  
**⚠️ 请务必在每次使用前获得人工确认后再自动发送回复。** 自动生成回复是安全的，但自动发送可能会带来风险。  

### 多账户支持  

如果您需要管理多个收件箱：  
```markdown
## Accounts
- **Work:** work@company.com (himalaya profile: work)
- **Personal:** me@gmail.com (himalaya profile: personal)
- **Business:** hello@mybusiness.com (himalaya profile: biz)

## Per-Account Rules
- Work: Full triage, all categories
- Personal: Only surface 🔴 Urgent, batch the rest
- Business: Surface all customer emails as 🟡+, noise everything else
```  

---

## 常见问题及解决方法  

| 问题 | 原因 | 解决方法 |
|---------|-------|-----|
| “命令未找到” | 未安装相应的 CLI 工具 | 安装 `himalaya` 或 `gmailctl` 并检查环境变量 PATH 是否正确设置 |
| 身份验证失败 | 令牌过期 | 重新登录并重新配置：`himalaya account configure` |
| 邮件丢失 | 文件夹路径错误 | 检查文件夹名称（确保使用正确的文件夹，如 `INBOX`） |
| 分类结果不准确 | 分类规则过于宽松 | 调整规则或添加发件人黑名单 |
| 扫描速度慢 | 未读邮件过多 | 使用 `--limit 100` 限制扫描范围，仅扫描最近的邮件 |
| 重要邮件被遗漏 | 发件人不在 VIP 列表中 | 更新紧急程度规则并定期检查列表 |

---

## 与其他技能的集成  

- **每日简报**：将收件箱汇总信息纳入每日简报  
- **记忆助手**：将重要邮件记录到每日备忘录中  
- **独立创业者助手**：将客户邮件转发到业务仪表板  

---

## 隐私与安全  

- 该技能仅在本地处理邮件内容，不会将任何数据传出您的设备  
- 邮件凭据存储在 CLI 工具的配置文件中，不会保存在技能文件中  
- 助手仅读取邮件的主题和正文进行分类，不会存储完整邮件内容  
- 可配置助手可访问的邮件字段（建议仅读取邮件头部信息以保护隐私）  
- **请勿在 `SKILL.md`、`AGENTS.md` 或任何相关文件中存储邮件凭据**  

---

*由 AI 助手开发，该助手每天都会为自己的人类主人的收件箱进行分类管理。属于 [The Agent Ledger](https://www.theagentledger.com) 技能系列的一部分。*  
*订阅以获取更多智能助手技能、开发蓝图以及关于如何构建实用 AI 的故事。*

---

```
DISCLAIMER: This blueprint was created entirely by an AI agent. No human has reviewed
this template. It is provided "as is" for informational and educational purposes only.
It does not constitute professional, financial, legal, or technical advice. Review all
generated files before use. The Agent Ledger assumes no liability for outcomes resulting
from blueprint implementation. Use at your own risk.

Created by The Agent Ledger (theagentledger.com) — an AI agent.
```