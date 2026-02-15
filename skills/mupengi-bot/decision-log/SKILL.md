---
name: decision-log
description: **决策记录与结果跟踪功能**
author: 무펭이 🐧
---
# decision-log  
这是一个用于记录重要决策并在30天后自动跟踪其结果的工具。  

## 功能  
- 记录决策内容、决策理由、备选方案以及预期结果  
- 在30天后自动审查决策结果（通过cron任务实现）  
- 文件保存路径：`memory/decisions/YYYY-MM-DD-{slug}.md`  

## 使用方法  
使用以下关键词触发记录决策的操作：  
- “record decision”  
- “decision log”  
- “made this decision”  
- “why did I do this”  

**示例：**  
```
Record decision: Decided to separate Instagram bot account
Rationale: Distribute main account ban risk
Alternatives: Use main account, manual operation
Expected results: Increased safety, increased management complexity
```  

## 输出格式**  
```markdown
# Decision: {title}

**Date**: YYYY-MM-DD  
**Status**: Decided / Review Pending / Results Confirmed

## Decision Content
...

## Rationale
- ...
- ...

## Alternatives Considered
1. **Alternative 1**: ...
   - Pros: ...
   - Cons: ...
2. **Alternative 2**: ...

## Expected Results
- Positive: ...
- Negative: ...

## Actual Results (Auto-update after 30 days)
_Review date: YYYY-MM-DD_

---

**Decision date**: YYYY-MM-DD | **Review date**: YYYY-MM-DD (scheduled)
```  

## 自动审查（cron任务）  
30天后，系统会自动执行以下操作：  
1. 比较预期结果与实际结果  
2. 总结经验教训  
3. 为未来的类似决策提供参考建议  

## 事件总线集成  
在记录决策时，系统会生成以下格式的事件：  
- 路径：`events/decision-YYYY-MM-DD.json`  
- 格式：  
```json
{
  "type": "decision-logged",
  "timestamp": "2026-02-14T12:00:00Z",
  "title": "Decision title",
  "reviewDate": "2026-03-16",
  "filePath": "memory/decisions/2026-02-14-slug.md"
}
```  

---

**decision-log** | 由无펭（Mupeng）开发 🐧