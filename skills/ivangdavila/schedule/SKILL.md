---
name: Schedule
slug: schedule
version: 1.0.2
description: 程序可以执行重复性或一次性任务。用户定义具体要执行的操作，而技能（Skill）则负责决定执行这些操作的时机。
changelog: Clarified user-driven execution model, removed assumed access patterns
metadata: {"clawdbot":{"emoji":"📅","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 数据存储

```
~/schedule/
├── jobs.json           # Job definitions
├── preferences.json    # Timezone, preferred times
└── history/            # Execution logs
    └── YYYY-MM.jsonl
```

**首次使用时执行操作：** `mkdir -p ~/schedule/history`  

## 功能范围  

该功能：  
- ✅ 将计划任务的定义存储在 `~/schedule/` 目录中  
- ✅ 在指定时间触发任务  
- ✅ 从用户处获取时区及时间偏好设置  

**执行机制：**  
- 用户明确指定任务的具体内容（即任务需要执行的具体操作）  
- 用户为任务授予所需的权限  
- 该功能仅负责任务执行的“时间”安排，而不涉及任务的具体内容（即“做什么”）  

**该功能不执行以下操作：**  
- ❌ 不会自行访问任何外部服务  
- ❌ 不会修改系统的 crontab 或 launchd 配置  
- ❌ 未经用户明确指示，不会自行执行任务  

## 快速参考  

| 主题 | 文件名 |  
|-------|------|  
| Cron 表达式语法 | `patterns.md` |  
| 常见错误 | `traps.md` |  
| 任务格式 | `jobs.md` |  

## 核心规则  

### 1. 用户定义所有内容  
当用户请求创建一个计划任务时：  
1. **任务内容**：用户指定任务需要执行的操作（可能需要其他功能或权限的支持）  
2. **执行时间**：该功能负责确定任务的具体执行时间  
3. **权限设置**：用户需要明确授予任务所需的访问权限  

**示例流程：**  
```
User: "Every morning, summarize my emails"
Agent: "I'll schedule this for 8am. This will need email access — 
        do you want me to use the mail skill for this?"
User: "Yes"
→ Job stored with explicit reference to mail skill
```  

### 2. 简单请求示例  
| 请求内容 | 执行操作 |  
|---------|--------|  
| “在 Y 时刻提醒我做 X” | 存储任务并确认 |  
| “每天早上执行 X” | 询问用户具体时间并存储任务 |  
| “取消任务 X” | 从 `jobs.json` 文件中删除该任务 |  

### 3. 确认流程  
```
✅ [what user requested]
📅 [when] ([timezone])
🔧 [permissions/skills needed, if any]
🆔 [id]
```  

### 4. 任务数据持久化  
任务的相关信息会被保存在 `~/schedule/jobs.json` 文件中：  
```json
{
  "daily_review": {
    "cron": "0 9 * * 1-5",
    "task": "User-defined task description",
    "requires": ["mail"],
    "created": "2024-03-15",
    "timezone": "Europe/Madrid"
  }
}
```  

`requires` 字段会明确列出任务执行所需的其他功能或权限。  

### 5. 任务执行  
- 当到达预定执行时间时，系统会执行用户定义的任务  
- 仅使用用户明确授予的权限  
- 执行结果会被记录到 `history/` 目录中  

### 6. 用户偏好设置  
在用户首次使用该功能后，系统会将其偏好设置（如时区、偏好时间（“早上”/“晚上”）以及默认通知方式）保存到 `preferences.json` 文件中：