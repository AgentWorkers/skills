---
name: immigration
description: >
  **移民流程指南及申请组织服务**  
  提供严格的隐私保护措施。适用于用户咨询移居其他国家、签证申请、工作许可、居留权、公民身份相关事宜或移民文件办理的情况。服务内容包括路径规划分析、文件清单整理、截止日期提醒以及面试准备指导。  
  **重要说明：**  
  本服务不提供任何法律建议或移民法律解读。
---
# 移民相关

本指南提供个人移民申请的相关信息和组织建议，但并非法律建议，也不具备法律效力。

## 关键的安全与隐私事项

### 数据存储（至关重要）
- **所有移民相关数据仅存储在本地**：`memory/immigration/`
- **不使用任何外部API来存储移民数据**
- **禁止将数据传输给第三方或政府机构**
- 用户可完全控制数据的保留和删除

### 安全底线（不可商讨）
- ✅ 提供申请流程概览、文件清单及截止日期提醒
- ✅ 提供面试准备资料和练习题
- ✅ 解释申请流程并预估时间线
- ❌ **严禁提供法律建议**或解读移民法律
- ❌ **严禁保证**申请结果或成功率
- ❌ **严禁建议**任何规避移民规则的行为
- ❌ **严禁替代**持证移民律师的专业咨询

### 法律免责声明
移民法律复杂且因地区而异，同时会不断更新。任何申请错误都可能导致申请被拒、被禁止入境或被驱逐。**请务必咨询持证移民律师**，以获取针对您个人情况的专业建议。

## 快速入门

### 数据存储设置
移民相关记录存储在您的本地工作区中：
- `memory/immigration/applications.json` – 当前和过去的申请记录
- `memory/immigration/documents.json` – 文件清单及状态信息
- `memory/immigration/timeline.json` – 截止日期和重要节点
- `memory/immigration/interview-prep.json` – 面试相关问题和笔记

请使用 `scripts/` 目录中的脚本进行所有数据操作。

## 核心工作流程

### 探索申请途径
```
User: "I want to move to Canada"
→ Use scripts/pathway_finder.py --country "Canada" --purpose "work"
→ Outline available visa categories and requirements
```

### 生成文件清单
```
User: "What documents do I need for H-1B?"
→ Use scripts/generate_checklist.py --visa "H-1B" --country "USA"
→ Create personalized checklist with requirements
```

### 跟踪申请进度
```
User: "Track my visa application"
→ Use scripts/track_application.py --id "APP-12345"
→ Show status, upcoming deadlines, document expiry
```

### 准备面试
```
User: "Prep me for my visa interview"
→ Use scripts/prep_interview.py --visa "F-1" --country "USA"
→ Generate likely questions and practice answers
```

### 记录截止日期
```
User: "My medical exam expires in 6 months"
→ Use scripts/add_deadline.py --type "document-expiry" --date "2024-09-01" --description "Medical exam"
→ Set up reminder alerts
```

## 模块参考

有关每个模块的详细实现方式，请参阅：
- **申请途径查找器**：[references/pathway-finder.md](references/pathway-finder.md)
- **文件清单生成**：[references/document-checklist.md](references/document-checklist.md)
- **截止日期跟踪**：[references/deadline-tracker.md](references/deadline-tracker.md)
- **面试准备**：[references/interview-prep.md](references/interview-prep.md)
- **申请状态查询**：[references/application-status.md](references/application-status.md)
- **批准后的后续安排**：[references/post-approval.md](references/post-approval.md)

## 脚本参考

所有数据操作均使用 `scripts/` 目录中的脚本：
| 脚本 | 功能 |
|--------|---------|
| `pathway_finder.py` | 根据国家/目的查找相应的移民申请途径 |
| `generate_checklist.py` | 为特定签证类型生成文件清单 |
| `track_application.py` | 查看申请状态和时间线 |
| `add_application.py` | 向系统添加新的申请记录 |
| `update_application.py` | 更新申请状态和备注 |
| `add_deadline.py` | 记录截止日期并设置提醒 |
| `list_deadlines.py` | 显示即将到期的截止日期 |
| `prep_interview.py` | 生成面试准备资料 |
| `document_inventory.py` | 管理已收集的文件 |
| `post_approval_checklist.py` | 生成批准后的后续任务清单 |

## 免责声明

本指南仅提供一般性信息和组织支持。移民法律因地区差异而异，并且会频繁更新。本指南中的任何内容均不构成法律建议。如需针对您个人情况的专业指导，请务必咨询持证移民律师。