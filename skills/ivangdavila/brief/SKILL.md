---
name: Brief
slug: brief
version: 1.0.1
description: 将信息浓缩成可操作的简报。用户指定信息来源，技能负责整理输出内容。
changelog: Added explicit data sources and storage location
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 数据存储

```
~/brief/
├── preferences.md    # Learned format preferences
└── templates/        # Custom brief templates
```

首次使用时执行以下操作：`mkdir -p ~/brief/templates`

## 功能范围

该功能：
- ✅ 将用户提供的信息进行结构化处理
- ✅ 根据用户的明确反馈学习其格式偏好
- ✅ 将用户的格式偏好存储在 `~/briefpreferences.md` 文件中

**用户驱动的模型：**
- 用户指定需要包含的信息内容
- 用户授予该功能访问所需数据源的权限
- 该功能负责数据的结构化和格式化处理

**该功能不会执行以下操作：**
- ❌ 未经用户请求，不会访问文件、电子邮件或日历
- ❌ 不会从用户未指定的数据源中获取数据
- ❌ 仅存储用户的格式偏好，不存储实际内容

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 格式相关设置 | `dimensions.md` |
| 简报模板 | `templates.md` |

## 核心规则

### 1. 用户指定数据来源
当用户请求生成简报时：
1. 用户需要提供所需信息，或指定数据来源的位置
2. 如果数据来源需要特殊访问权限，用户必须明确授予该权限
3. 该功能会根据用户提供的信息对内容进行结构化和格式化处理

**示例：**
```
User: "Brief me on project X status"
Agent: "I'll need access to the project docs. Can you share 
        the status doc or grant access to the project folder?"
User: [shares doc or grants access]
→ Brief generated from user-provided source
```

### 2. 简报的结构
```
📋 [BRIEF TYPE] — [SUBJECT]

⚡ BOTTOM LINE
[1-2 sentences: key takeaway]

📊 KEY POINTS
• [Point 1]
• [Point 2]
• [Point 3]

🎯 ACTION NEEDED
[Decision or action required]
```

### 3. 根据用户反馈进行优化
- 如果用户反馈“内容太详细”，则在未来生成的简报中缩短相关内容
- 如果用户提到“缺少某些信息”，则会在后续生成简报时询问这些信息
- 如果用户认为当前格式完美，该功能会继续保持该格式
- 用户的格式偏好会被存储在 `~/briefpreferences.md` 文件中

### 4. 首选项的存储格式
每个偏好设置占用一行：
```
- Prefers bullet points over paragraphs
- Executive summary first
- Include metrics when available
- Max 1 page for status briefs
```

### 5. 简报类型及其所需信息
| 简报类型 | 需要提供的信息 | 关键要素 |
|------|------|-------------|
| 执行简报 | 需要做出决策 | 问题概述（BLUF）、建议、潜在风险 |
| 项目简报 | 进度更新 | 项目现状、阻碍因素、下一步行动 |
| 会议简报 | 会议前准备 | 会议目的、背景信息、需要讨论的决策 |
| 交接简报 | 任务交接 | 当前任务状态、注意事项、优先级 |