---
name: coaching
description: **辅导实践支持服务**：包括会话准备、问题生成、客户进度跟踪以及目标设定。适用于用户提及辅导会话、辅导问题、客户进度或辅导目标的情况。我们负责会话的准备工作，生成具有针对性的问题，跟踪客户的承诺履行情况，并通过清晰的目标设定框架协助客户实现目标，同时确保会话之间的连贯性与持续性。我们严格遵守客户保密原则。
---
# 辅导实践系统：让每一次辅导都充满成效

## 关键隐私与安全措施

### 数据存储（至关重要）
- **所有客户数据仅存储在本地**：`memory/coaching/`
- **严格保密**——客户信息绝不共享
- **禁止跨客户数据混用**——确保数据完全隔离
- **不连接任何外部辅导平台**  
- 用户可完全控制数据的保留和删除

### 安全边界
- ✅ 准备辅导内容并生成问题  
- ✅ 跟踪客户的进展和承诺  
- ✅ 使用相关框架协助设定目标  
- ✅ 提供辅导期间的支持  
- ❌ **绝不要** 在不同情境下共享客户信息  
- ❌ **绝不要** 代替客户做出决策  
- ❌ **绝不要** 替代教练的判断或直觉  

### 保密声明
辅导的效果建立在信任的基础上。本系统严格遵循保密原则——任何客户数据都不会被共享、混用或泄露到系统外部。

### 数据结构
辅导数据存储在本地：
- `memory/coaching/clients.json` – 客户记录（每个客户的数据独立存储）  
- `memory/coaching/sessions.json` – 辅导记录和笔记  
- `memory/coaching/goals.json` – 客户的目标和进展  
- `memory/coaching/questions.json` – 问题库  
- `memory/coaching/commitments.json` – 客户的承诺记录  

## 核心工作流程

### 准备辅导环节  
```
User: "Prep me for session with client John"
→ Use scripts/prep_session.py --client "John" --session 5
→ Summarize previous session, check commitments, generate tailored questions
```

### 生成问题  
```
User: "Give me questions for exploring career transition"
→ Use scripts/generate_questions.py --topic "career-transition" --depth "deep"
→ Generate powerful questions calibrated to situation
```

### 跟踪进展  
```
User: "Show me Sarah's progress over the last 3 months"
→ Use scripts/track_progress.py --client "Sarah" --period "3months"
→ Display goals, session history, patterns, breakthroughs
```

### 设定目标  
```
User: "Help my client set a clear goal"
→ Use scripts/set_goal.py --client "Mike" --area "leadership"
→ Apply clarity, specificity, timeline, obstacles, support framework
```

### 辅导期间的支持  
```
User: "Send between-session support to Lisa"
→ Use scripts/between_sessions.py --client "Lisa" --days 3
→ Provide reflection prompts, action reminders, preparation for next session
```

## 模块参考
- **辅导准备**：请参阅 [references/session-prep.md](references/session-prep.md)  
- **高效问题设计**：请参阅 [references/questions.md](references/questions.md)  
- **目标设定框架**：请参阅 [references/goal-setting.md](references/goal-setting.md)  
- **进展跟踪**：请参阅 [references/progress.md](references/progress.md)  
- **辅导期间的支持**：请参阅 [references/between-sessions.md](references/between-sessions.md)  
- **客户隐私保护**：请参阅 [references/confidentiality.md](references/confidentiality.md)  

## 脚本参考
| 脚本 | 用途 |  
|--------|---------|  
| `prep_session.py` | 准备辅导环节 |  
| `generate_questions.py` | 生成高效的问题 |  
| `track_progress.py` | 跟踪客户进展 |  
| `set_goal.py` | 帮助设定目标 |  
| `between_sessions.py` | 提供辅导期间的支持 |  
| `log_session.py` | 记录辅导笔记 |  
| `track_commitment.py` | 跟踪客户的承诺履行情况 |  
| `prepare_review.py` | 准备进度评估 |