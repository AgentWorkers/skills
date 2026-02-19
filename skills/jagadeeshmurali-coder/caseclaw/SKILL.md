---
name: caseclaw
description: 未能按时完成任务是……
homepage: https://github.com/legal-tools/caseclaw
metadata: {"clawdbot":{"emoji":"🔱","requires":{"bins":["caseclaw"]},"install":[{"id":"brew","kind":"brew","formula":"legal-tools/tap/caseclaw","bins":["caseclaw"],"label":"Install caseclaw (brew)"}]}}
---
# caseclaw

**错过一个截止日期就可能导致职业生涯的终结。caseclaw能确保这种情况永远不会发生。**

错过截止日期引发的诉讼比糟糕的法律建议还要多；利益冲突紧随其后。每位律师都曾因忘记记录可计费的工作时间而损失数千美元。caseclaw就像一个驻扎在终端中的指挥中心，全天候、无声地、无情地防范着这三类问题。

只需将它指向一个案件，它就能自动根据600多个法院的规则集计算出所有的提交截止日期。输入一个新的客户名称，它能在不到一秒钟内检查是否存在利益冲突。开始输入内容时，它就会以6分钟为间隔记录你的工作时间。

无需浏览器标签页，也无需笨重的SaaS仪表板，更无需每用户500美元的企业级订阅费用。只需一个命令，就能让你安心地知道没有任何事情会被遗漏。

**适用人群：**  
- 被截止日期压得喘不过气的独立律师  
- 需要同时处理40多个案件的中小型律师事务所的诉讼人员  
- 负责协调所有事务的律师助理  
- 需要可审计追踪功能的内部团队  

**它替代了什么：**  
- 你曾发誓会定期更新的电子表格  
- 被遗忘的日历提醒  
- 晚上11点时突然意识到自己忘记提交文件的那种不安感  

---

## 价格  

| 功能 | 免费版 | Pro版（每月29美元） | 企业版（每月99美元） |
|---|---|---|---|
| 截止日期跟踪（手动） | ✅ | ✅ | ✅ |
| 自动计算的截止日期 | 每月5次 | 无限制 | 无限制 |
| 法院规则数据库 | 50个法院 | 600多个法院 | 600多个法院 |
| 利益冲突检查 | 基础版（本地） | 全功能版（包含模糊匹配和实体识别） | 全功能版（包含跨案件对比） |
| 案例法监控 | 无 | 10条提醒 | 无限条提醒 |
| 时间/费用记录 | 基础计时器 | 智能费用代码 | 支持多律师使用及LEDES格式导出 |
| 对方律师信息 | 无 | 胜败查询 | 全面分析 |
| 案件数量 | 3个活跃案件 | 无限制 | 无限制 |
| 团队成员数量 | 1人 | 1人 | 最多25人 |
| API访问 | 无 | 无 | ✅ |
| 优先级支持 | 无 | 电子邮件支持 | 专属Slack频道 |

> 升级至Pro版可解锁更多功能。提供14天免费试用，无需信用卡。  

---

## 设置  
```bash
caseclaw init                          # Initialize in current directory
caseclaw auth login                    # Authenticate (free account)
caseclaw config set jurisdiction "NY"  # Set default jurisdiction
caseclaw config set court "SDNY"       # Set default court
```  

---

## 核心功能  

### 1. 截止日期跟踪 ⏰（避免诉讼的利器）  

律师被起诉的首要原因是错过截止日期。caseclaw让这种情况成为不可能。  

**手动添加截止日期：**  
- `caseclaw deadline add --matter "Smith v. Jones" --type "Answer" --due 2026-03-15 --court SDNY`  
- `caseclaw deadline add --matter "Smith v. Jones" --type "Discovery cutoff" --due 2026-06-01`  
- `caseclaw deadline add --matter "Acme Corp" --type "SOL" --trigger-date 2024-02-01 --statute "NY CPLR 214" --years 3`  

**自动计算截止日期（Pro版）：**  
- `caseclaw deadline calc --event "complaint-served" --date 2026-02-10 --court SDNY`  
  → 会自动生成：答辩截止日期、证据提交截止日期、审前会议截止日期等  
- `caseclaw deadline calc --event "appeal-filed" --date 2026-02-18 --court "2d Cir"`  

**查看和管理：**  
- `caseclaw deadline list`          — 所有即将到期的截止日期  
- `caseclaw deadline list --matter "Smith v. Jones"`    — 每个案件的截止日期  
- `caseclaw deadline list --overdue`        — 已逾期的截止日期  
- `caseclaw deadline list --next 7`         — 下7天的截止日期  
- `caseclaw deadline list --next 30 --json`       — 用于日历的导出格式  
- `caseclaw deadline done --id DL-0042`      — 标记为已完成  

**提醒：**  
- `caseclaw deadline alerts --email you@firm.com`    — 每日电子邮件汇总  
- `caseclaw deadline alerts --slack #deadlines`    — Slack通知（适用于团队）  
- `caseclaw deadline alerts --calendar`       — 与Google/Outlook同步  

### 2. 法院规则合规性 📏  

每个法院的规则都不同。字体错误？页边距不符合要求？文件被拒绝提交？客户会非常愤怒。  

- `caseclaw rules show SDNY`          — 完整的规则摘要  
- `caseclaw rules show SDNY --topic "page-limit"`    — 具体规则  
- `caseclaw rules show SDNY --topic "font"`      — 字体要求  
- `caseclaw rules check brief.pdf --court SDNY`    — 检查文件是否符合规则  
- `caseclaw rules diff SDNY EDNY`        — 比较两个法院的规则  
- `caseclaw rules search "electronic filing" --state NY`    — 搜索与纽约州相关的规则  

**支持的检查（Pro版）：**  
- 页数/字数限制  
- 字体家族和大小要求  
- 页边距要求  
- 行间距  
- 权限表格格式  
- 送达证明要求  
- 电子文件格式（PDF/A、书签、OCR层）  
- 标题页和封面页格式  

### 3. 利益冲突检查 🔍  

错过利益冲突可能导致律师被取消资格，甚至面临律师协会的投诉。  

- `caseclaw conflict check "John Smith" "Acme Corporation"`  
- `caseclaw conflict check "Jane Doe" --thorough`     — 模糊匹配及实体识别（Pro版）  
- `caseclaw conflict add --entity "Acme Corp" --matter "2024-001" --role "plaintiff"`  
- `caseclaw conflict add --entity "Bob Builder" --matter "2024-001" --role "witness"`  
- `caseclaw conflict list --matter "2024-001"`     — 查看所有相关案件  
- `caseclaw conflict search "Acme"`         — 在所有案件中搜索相关方  
- `caseclaw conflict export --format csv`       — 导出结果  

**模糊匹配（Pro版）能识别以下情况：**  
- 名字变体："Bob Smith" ↔ "Robert Smith" ↔ "R. Smith"  
- 实体别名："Acme Corp" ↔ "Acme Corporation" ↔ "ACME Inc."  
- 相关方关系：母公司/子公司/关联公司  

### 4. 案例法监控 📡（Pro版）  

避免在庭审时因不了解上周已判决的案件而措手不及。  

- `caseclaw watch add --query "qualified immunity" --court "Supreme Court"`  
- `caseclaw watch add --query "TCPA" --circuit 2`  
- `caseclaw watch add --case "2025-CV-1234" --court SDNY`    — 跟踪特定案件  
- `caseclaw watch list`          — 查看最近新增的案件  
- `caseclaw watch results --last 7`         — 本周新增的提醒  
- `caseclaw watch alerts --email you@firm.com --frequency weekly`    — 每周发送邮件提醒  

### 5. 时间与费用管理 ⏱️  

每错过6分钟，你就可能损失一笔收入。  

**记录工作时间：**  
- `caseclaw time start --matter "Smith v. Jones" --task "Draft motion"`  
- `caseclaw time stop`          — 停止计时  
- `caseclaw time add --matter "Smith v. Jones" --hours 1.5 --task "Client call" --date 2026-02-18`  
- `caseclaw time status`           — 当前正在进行的任务  

**查看和导出：**  
- `caseclaw time log --matter "Smith v. Jones"`      — 完整的时间记录  
- `caseclaw time log --today`         — 当天的时间记录  
- `caseclaw time log --week`          — 这周的时间记录  
- `caseclaw time log --month`         — 按月份整理的时间记录  
- `caseclaw time export --matter "Smith v. Jones"`    — 以CSV格式导出  
- `caseclaw time export --month 2026-02`     — 以LEDES 1998B格式导出（适用于企业）  

**智能费用代码（Pro版）：**  
- `caseclaw time start --matter "Smith v. Jones" --task "research"`  
  → 会自动建议费用代码：UTBMS L120（研究 - 法律问题）  

### 6. 案件管理 📂  

- `caseclaw matter new --name "Smith v. Jones" --type "litigation" --court SDNY --client "Jane Smith"`  
- `caseclaw matter list`          — 查看所有案件列表  
- `caseclaw matter list --status active`      — 查看活跃案件  
- `caseclaw matter show "Smith v. Jones"`      — 查看案件详情  
- `caseclaw matter close "Smith v. Jones"`     — 关闭案件  
- `caseclaw matter archive "Smith v. Jones"`     — 归档案件  

**案件仪表板显示：**  
- 即将到期的截止日期  
- 已计费/未计费的总时间  
- 关键日期  
- 当事方和利益冲突状态  
- 最近的活动记录  

### 7. 对方律师信息 🕵️（Pro版）  

在进入法庭之前，了解你的对手情况。  

- `caseclaw opp lookup "Jane Attorney" --jurisdiction NY`    — 查找纽约州的对手律师  
- `caseclaw opp firm "Dewey & Associates"`     — 查找对手律师事务所  
- `caseclaw opp history "Jane Attorney" --court SDNY`    — 查看该律师过去的案件记录  
- `caseclaw opp stats "Jane Attorney"`      — 查看该律师的胜败记录和平均和解金额（企业版）  

---

## 常见工作流程  

**新案件录入**  
```bash
# 1. Run conflict check
caseclaw conflict check "New Client LLC" "Opposing Party Inc"

# 2. Create matter
caseclaw matter new --name "NewClient v. Opposing" --type litigation --court SDNY

# 3. Auto-generate deadlines
caseclaw deadline calc --event "complaint-filed" --date 2026-02-18 --court SDNY

# 4. Start the clock
caseclaw time start --matter "NewClient v. Opposing" --task "Client intake"
```  

**晨间仪表盘**  
```bash
# What's due this week?
caseclaw deadline list --next 7

# Any new case law?
caseclaw watch results --last 1

# Unbilled time?
caseclaw time log --week --unbilled
```  

**提交前的检查清单**  
```bash
# Check court rules
caseclaw rules show SDNY --topic "page-limit"
caseclaw rules show SDNY --topic "efiling"

# Validate your brief
caseclaw rules check motion.pdf --court SDNY

# Log the filing time
caseclaw time add --matter "Smith v. Jones" --hours 0.5 --task "E-file motion"

# Mark deadline complete
caseclaw deadline done --id DL-0042
```  

**月末费用统计**  
```bash
# Review all time entries
caseclaw time log --month 2026-02 --summary

# Export for billing system
caseclaw time export --month 2026-02 --format ledes > february_billing.txt

# Check for unbilled matters
caseclaw time log --month 2026-02 --unbilled --by-matter
```  

---

## 注意事项：  

- 默认情况下，所有数据都存储在本地（`~/.caseclaw/`文件夹中）——免费版用户的数据不会离开您的设备  
- Pro版/企业版使用加密的API调用；数据仅在处理完成后存储在我们的服务器上  
- 截止日期的计算基于《联邦民事诉讼规则》（FRCP）、各州的民事诉讼规则以及当地法院的规定  
- 法院规则数据库每周更新（Pro版/企业版）  
- 可与`lawclaw`技能结合使用，进行文件分析和案件管理  
- 可与`gog`技能结合使用，实现与Google日历的同步及Gmail集成  

## 安全性与合规性  

- 符合SOC 2 Type II标准（Pro版/企业版）  
- 数据存储采用AES-256加密算法（静态数据），传输过程中使用TLS 1.3协议  
- 从未使用客户数据进行模型训练  
- 数据处理符合律师协会的规定（ABA Model Rule 1.6）  
- 完整的审计日志：`caseclaw audit log --matter "Smith v. Jones"`  
- 数据导出/删除：`caseclaw data export` / `caseclaw data delete --confirm`  

## 支持方式：  

- 免费版：通过GitHub社区问题寻求帮助  
- Pro版：提供24小时电子邮件支持  
- 企业版：提供专属Slack频道和入职培训  
- 内置文档：`caseclaw help <command>`  
- 如需反馈，请发送`caseclaw feedback "your message"`联系我们