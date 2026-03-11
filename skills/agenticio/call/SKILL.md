---
name: call
description: >
  **呼叫管理系统**  
  具备呼叫准备、实时记录和后续跟踪功能。适用于用户提及电话通话、会议、对话、已做出的承诺或需要跟进的情况。该系统可协助用户准备通话内容，实时记录关键信息和决策结果，跟踪待办事项和承诺事项，起草跟进函件，并整理对话历史记录。所有数据均存储在本地。
---
# 呼叫管理

我们的呼叫管理系统能够充分利用每一次通话数据。

## 关键的隐私与安全措施

### 数据存储（至关重要）
- **所有通话数据仅存储在本地**：`memory/calls/`
- **不进行通话录音**（除非用户另行启用）
- **不连接任何外部客户关系管理系统（CRM）**
- **不共享通话数据**
- 用户可以完全控制数据的保留和删除

### 隐私声明
通话记录包含敏感信息。所有数据均保存在本地且受到保护。用户可以决定哪些数据会被记录和保留。

### 数据结构
通话数据存储在本地：
- `memory/calls/calls.json` – 完整的通话记录
- `memory/calls/contacts.json` – 联系人信息及通话背景
- `memory/calls/commitments.json` – 已做出或收到的承诺
- `memory/calls/followups.json` – 待处理的跟进事项
- `memory/calls/templates.json` – 跟进消息模板

## 核心工作流程

### 呼叫准备
```
User: "I have a call with Acme Corp in 30 minutes"
→ Use scripts/prep_call.py --contact "Acme Corp" --purpose "negotiate contract"
→ Pull previous calls, open commitments, relevant context
```

### 通话过程中的数据记录
```
User: "Note: They need the proposal by Friday, Sarah is decision maker, follow up on pricing"
→ Use scripts/capture_fragments.py --call-id "CALL-123" --fragments "proposal by Friday, Sarah decision maker, follow up pricing"
→ Build structured notes in real-time
```

### 通话结束及生成总结
```
User: "Call is done"
→ Use scripts/end_call.py --call-id "CALL-123"
→ Generate summary: decisions, action items, commitments
```

### 跟进事项管理
```
User: "What follow-ups do I owe?"
→ Use scripts/check_followups.py
→ Show all pending commitments with deadlines
```

### 起草跟进消息
```
User: "Draft follow-up to Sarah"
→ Use scripts/draft_followup.py --contact "Sarah" --call-id "CALL-123"
→ Generate personalized follow-up email with specific references
```

## 模块参考
- **呼叫准备**：请参阅 [references/preparation.md](references/preparation.md)
- **实时数据记录**：请参阅 [references/capture.md](references/capture.md)
- **承诺跟踪**：请参阅 [references/commitments.md](references/commitments.md)
- **跟进系统**：请参阅 [references/followups.md](references/followups.md)
- **通话历史记录**：请参阅 [references/history.md](references/history.md)
- **联系人信息管理**：请参阅 [references/contacts.md](references/contacts.md)

## 脚本参考
| 脚本 | 功能 |
|--------|---------|
| `prep_call.py` | 为即将到来的通话做准备 |
| `capture_fragments.py` | 在通话过程中记录笔记 |
| `end_call.py` | 结束通话并生成总结 |
| `check_followups.py` | 检查待处理的跟进事项 |
| `draft_followup.py` | 起草跟进消息 |
| `log_call.py` | 记录已完成的通话 |
| `contact_history.py` | 查看联系人的通话历史记录 |
| `commitment_status.py` | 检查承诺的完成状态 |