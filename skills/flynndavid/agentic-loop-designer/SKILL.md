---
name: agentic-loop-designer
version: 1.0.0
price: 29
bundle: ai-setup-productivity-pack
bundle_price: 79
last_validated: 2026-03-07
---

# **智能代理循环设计工具**  
**框架：** **“是/否”循环设计框架**  
（每小时咨询费用300美元，您只需支付29美元即可使用。）  

---

## **该工具的功能**  
该工具可将您手动执行的任何重复性任务转化为自动化代理循环：触发 → 代理执行 → 通过Slack发送通知 → 得到批准或跳过处理。  
包含5个现成的循环模板，以及一个决策树，可帮助您从零开始设计属于自己的自动化流程。  

## **解决的问题**  
创始人常常花费大量时间处理那些本可以自动完成的重复性任务，例如：邮件分类、每周报告、团队会议总结、潜在客户评估等。如果这类任务每周出现两次以上，那么它们完全适合被自动化处理。  

---

## **“是/否”循环设计框架**  
这是一个结构化的工具，仅需10分钟即可帮助您设计出任何自动化循环。其核心理念是：**所有可自动化的任务本质上都是一系列“是/否”的决策过程。**  

### **框架结构**  
```
┌─────────────────────────────────────────────┐
│              YES/NO LOOP CANVAS             │
├─────────────────────────────────────────────┤
│  TRIGGER: What starts this loop?           │
│  ─────────────────────────────────────────  │
│  AGENT ACTION: What does the agent do?     │
│  ─────────────────────────────────────────  │
│  DECISION GATE: Approve / Skip / Escalate? │
│  ─────────────────────────────────────────  │
│  OUTPUT: What gets created or sent?        │
│  ─────────────────────────────────────────  │
│  MEMORY: What should persist for next run? │
└─────────────────────────────────────────────┘
```  

---

### **步骤1：触发条件设置**  
**是什么触发了这个循环？**  
```
Is there a natural trigger?
├── Time-based (daily/weekly/on schedule)
│   └── → Use: cron trigger
├── Event-based (new email, new issue, form submit)
│   └── → Use: webhook trigger
├── Threshold-based (metric crosses a line)
│   └── → Use: polling trigger with condition
└── Manual ("run this now")
    └── → Use: manual trigger with /command
```  

**触发条件评估：**  
| 触发类型 | 可靠性 | 设置难度 | 适用场景 |  
|---------|---------|-----------|---------|  
| Cron任务 | ★★★★★ | 低 | 报告、总结、数据汇总 |  
| Webhook | ★★★★☆ | 中等 | 新数据事件 |  
| 轮询 | ★★★☆☆ | 中等 | 基于指标的任务 |  
| 手动触发 | ★★★★★ | 无要求 | 需按需执行的任务 |  

---

### **步骤2：代理执行逻辑设计**  
**代理应该具体执行什么操作？**  
该步骤需要回答三个问题：  
1. **代理需要哪些数据？**（数据来源）  
2. **数据需要经过哪些处理？**  
3. **处理后的结果应以什么形式呈现？**  

**代理执行模板：**  
```
SOURCES: [List tools/APIs the agent reads from]
TRANSFORM: [Plain English description of what agent does]
OUTPUT FORMAT: [Slack message / doc / file / API call]
```  
**示例：**  
```
SOURCES: Linear API (open issues), GitHub API (open PRs)
TRANSFORM: Group issues by assignee, flag items > 3 days old
OUTPUT FORMAT: Slack message with bullet list, @mention for flagged items
```  

---

### **步骤3：决策机制设计**  
**这是任何自动化循环中最关键的部分。**  
每个循环都需要明确的审批流程。请参考以下矩阵进行设计：  
| 风险等级 | 数据敏感性 | 执行范围 | 审批方式 |  
|---------|-----------------|------------|---------|  
| 低 | 数据不敏感 | 只读 | 自动执行（无需审批） |  
| 低 | 数据不敏感 | 可写入/发送 | 通过Slack预览后自动发送 |  
| 中等 | 数据敏感 | 需要人工审批 |  
| 高 | 数据高度敏感 | 必须经过人工审核 |  

**审批机制实现：**  
```
Slack message format for approval gates:
─────────────────────────────────
🤖 Loop: {Loop Name} | Run #{N}
{Agent output preview}

[✅ Approve] [⏭ Skip] [🛑 Stop Loop]
─────────────────────────────────
Timeout: {N} minutes → {default action}
```  

---

### **步骤4：结果输出设计**  
**处理后的结果应保存在哪里？**  
```
Output destination decision tree:
├── Team visibility needed?
│   ├── Yes → Slack channel message
│   └── No → DM or file
├── Needs to be acted on later?
│   ├── Yes → Notion page / Linear issue / GitHub issue
│   └── No → Slack message (ephemeral OK)
├── Needs structured data?
│   ├── Yes → Notion database row / JSON file
│   └── No → Prose summary
└── External delivery needed?
    ├── Yes → Email (via SMTP/SendGrid) / webhook
    └── No → Internal tool
```  

---

### **步骤5：数据持久化设计**  
**如何确保循环运行结果在下次执行时仍可使用？**  
```
Memory checklist:
□ Last run timestamp (prevent duplicate work)
□ Previously processed item IDs (deduplication)
□ Cumulative state (running totals, streaks)
□ User preferences (learned from approvals/skips)
□ Error log (for debugging)
```  
**简单的数据持久化方案（基于文件）：**  
```json
{
  "loop_id": "weekly-standup",
  "last_run": "2026-03-07T09:00:00Z",
  "processed_ids": ["issue-123", "pr-456"],
  "run_count": 14,
  "skip_count": 2
}
```  

---

## **5个现成的循环模板**  

### **循环1：每周团队会议总结**  
**触发条件：** 每周一上午9点  
**数据来源：** 未解决的问题（GitHub）、待审的GitHub PR、过去7天的Slack消息  
**操作：** 汇总每位成员的待办任务及阻碍因素  
**审批方式：** 自动发送（低风险，仅限阅读）  
**输出：** 发送到#standup频道的Slack消息  

**设置时间：** 约20分钟 | **节省时间：** 每周30-60分钟  

---

### **循环2：潜在客户评估**  
**触发条件：** 新客户信息提交（通过Typeform/Tally平台）  
**数据来源：** 表单填写内容、公司信息（Clearbit/Apollo）  
**操作：** 根据ICP标准评估潜在客户，起草个性化跟进邮件  
**审批方式：** 通过Slack审批后发送邮件  
**输出：** 草稿邮件及客户评估结果（保存在Notion CRM系统中）  

**设置时间：** 约45分钟 | **节省时间：** 每周2-4小时  

---

### **循环3：GitHub PR审核提醒**  
**触发条件：** PR等待审核超过24小时  
**数据来源：** GitHub API（待审PR、审核状态）  
**操作：** 为逾期未审核的PR发送提醒消息  
**审批方式：** 如果PR超过48小时未审核，则自动发送提醒；如果审核时间在24-48小时内，则通过Slack发送预览信息  
**输出：** 通过Slack@mention发送给相关审核人员  

**设置时间：** 约15分钟 | **节省时间：** 避免频繁的人工干预  

---

### **循环4：每周收入统计**  
**触发条件：** 每周五下午5点  
**数据来源：** Stripe API、Notion数据统计系统  
**操作：** 计算每周收入变化、客户流失情况、新客户数量  
**审批方式：** 自动发送财务数据（仅限阅读）  
**输出：** 发送到#founders频道的Slack消息，附带数据图表  

**设置时间：** 约30分钟 | **节省时间：** 每周节省1-2小时的人工统计时间  

---

### **循环5：创意收集与排队**  
**触发条件：** 在指定Slack频道中收到包含“#idea”的消息  
**数据来源：** Slack消息、Notion中的创意列表  
**操作：** 提取创意内容，评估其价值，加入待处理列表  
**审批方式：** 如果创意评分高于70分则自动加入列表；评分在50-70分之间则发送预览；低于50分则直接丢弃  
**输出：** 保存在Notion数据库中  

---

## **自定义循环设计（10分钟工作坊）**  
**步骤1：确定任务（2分钟）**  
> 请描述您手动执行的、重复性较强的任务。  
> 用一句话概括：**“每隔[时间间隔]，我使用[数据来源]执行[操作]，并将结果发送到[目标平台]。”  

**步骤2：填写框架（5分钟）**  
```
TRIGGER: _______________
SOURCES: _______________
AGENT ACTION: _______________
GATE: Auto / Preview / Approve (circle one)
OUTPUT: _______________
MEMORY: _______________
```  

**步骤3：风险评估（2分钟）**  
- 该循环是否需要发送外部消息？ → 是否需要审批？  
- 是否会修改或删除数据？ → 是否需要审批？  
- 仅用于阅读和总结？ → 可以自动执行？  

**步骤4：命名并部署（1分钟）**  
- 为循环命名，并将其添加到代理配置中。手动运行一次，观察其运行效果。  

---

## **“是/否”循环评估标准**  
在部署任何循环之前，请先对其进行评估：  
| 评估维度 | 0 | 1 | 2 |  
|---------|---|---|---|  
| 触发条件是否可靠 | 仅手动执行 | 部分自动化 | 完全自动化 |  
| 数据来源是否可用 | 数据连接是否正常 | 数据来源是否全部通过MCP平台连接 |  
| 审批机制是否合适 | 高风险操作是否需要审批？ | 审批机制是否合理？ |  
| 输出结果是否有用 | 是否有人查看？ | 结果是否被有效利用？ |  
| 数据是否避免重复？ | 是否有重复数据？ |  

**评分标准：**  
- 得分8-10分：可以直接部署。  
- 得分5-7分：请先修复薄弱环节（通常是审批机制或数据来源）。  
- 得分0-4分：请重新设计循环。  

---

## **使用示例**  
**用户需求：**  
“我每周一早上都会从GitHub拉取待审的PR，并将状态更新到Slack。请帮我实现自动化。”  

**使用该工具的步骤：**  
1. 在“是/否”循环设计框架中填写用户的GitHub仓库和Slack频道信息。  
2. 设置触发条件（例如：每周一上午9点的Cron任务）。  
3. 确认数据来源是否已通过MCP平台连接（或根据提示进行配置）。  
4. 选择合适的循环模板（例如：每周团队会议总结），并根据实际需求进行定制。  
5. 根据评估标准对循环进行评分（建议得分8-10分）。  
6. 获取最终的配置文件并部署。  

---

## **购买说明**  
该工具属于**“AI设置与生产力工具包”（售价79美元）**：  
- MCP服务器设置工具（19美元）  
- 智能代理循环设计工具（29美元）  
- AI操作系统蓝图（39美元）  
- 上下文预算优化工具（19美元）  
- 非技术型代理快速入门指南（9美元）  

购买完整工具包可节省36美元。  
开发者：[@Remy_Claw](https://remyclaw.com)  

---