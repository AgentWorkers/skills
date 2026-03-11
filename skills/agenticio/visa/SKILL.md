---
name: visa
description: 签证申请指南：包括文件跟踪和时间线管理。适用于用户提及旅行签证、签证申请、签证文件、领事馆面试或入境要求的情况。本指南可帮助您确定正确的签证类型、制定文件清单、管理申请进度、准备面试内容，并追踪申请状态。但请注意，我们无法保证签证申请的最终批准结果。
---
# 签证

签证导航系统：帮助您获得正确的签证，确保一切顺利进行。

## 高度重视隐私与安全

### 数据存储（至关重要）
- **所有签证数据仅存储在本地**：`memory/visa/`
- **不与任何政府系统连接**
- **不将任何文件上传到外部服务**
- **本工具不用于提交签证申请**
- 用户可完全控制数据的保留和删除

### 安全措施
- ✅ 确认签证类型和所需材料
- ✅ 生成文件清单
- ✅ 跟踪申请进度
- ✅ 准备面试
- ❌ **绝不保证签证申请一定会被批准**
- ❌ **绝不替代持证移民律师的职责**
- ❌ **绝不会代您提交签证申请**

### 数据结构
签证数据存储在本地：
- `memory/visa/applications.json` – 当前正在处理的申请
- `memory/visa/documents.json` – 文件清单及状态
- `memory/visa/timelines.json` – 申请时间线和截止日期
- `memory/visa/interview_prep.json` – 面试准备相关资料
- `memory/visa/requirements.json` – 各国具体签证要求

## 核心工作流程

### 确认签证类型
```
User: "What visa do I need for Germany?"
→ Use scripts/identify_visa.py --country Germany --purpose work --duration 6months
→ Analyze situation, recommend visa category
```

### 生成文件清单
```
User: "What documents do I need for Schengen visa?"
→ Use scripts/build_checklist.py --visa schengen --nationality US
→ Generate complete document list with specifications
```

### 跟踪申请进度
```
User: "Track my visa application"
→ Use scripts/track_timeline.py --application-id "VISA-123"
→ Show deadlines, upcoming actions, document expiry alerts
```

### 准备面试
```
User: "Prep me for my visa interview"
→ Use scripts/prep_interview.py --visa-type work --country Canada
→ Generate likely questions and recommended responses
```

### 记录申请信息
```
User: "I submitted my application today"
→ Use scripts/log_application.py --country Japan --visa-type tourist --submission-date 2024-03-01
→ Track application with timeline and reminders
```

## 模块参考
- **签证类型**：请参阅 [references/visa-types.md](references/visa-types.md)
- **文件清单**：请参阅 [references/documents.md](references/documents.md)
- **时间线管理**：请参阅 [references/timelines.md](references/timelines.md)
- **面试准备**：请参阅 [references/interview.md](references/interview.md)
- **申请被拒的情况**：请参阅 [references/denials.md](references/denials.md)
- **入境要求**：请参阅 [references/entry-requirements.md](references/entry-requirements.md)

## 脚本参考
| 脚本 | 用途 |
|--------|---------|
| `identify_visa.py` | 确认正确的签证类型 |
| `build_checklist.py` | 生成文件清单 |
| `track_timeline.py` | 跟踪申请进度 |
| `prep_interview.py` | 准备签证面试 |
| `log_application.py` | 记录新的申请信息 |
| `check_deadlines.py` | 检查截止日期 |
| `compare_visas.py` | 比较不同签证选项 |
| `document_status.py` | 检查文件状态 |