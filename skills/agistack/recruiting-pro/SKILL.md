---
name: recruiting-pro
description: >
  **招聘工作流程管理工具：具备结构化的流程和候选人跟踪功能**  
  适用于用户需要处理招聘相关事宜的场景，包括职位描述编写、简历筛选、面试安排、候选人进度跟踪以及录用通知的发送等。该工具能够协助用户完成以下工作：  
  - 编写职位描述；  
  - 筛选候选人；  
  - 准备面试问题；  
  - 跟踪招聘流程的各个阶段；  
  - 起草沟通文件（如面试邀请函、录用通知等）。  
  所有候选人的相关信息均存储在本地系统中。  
  **重要说明：**  
  - 该工具仅提供辅助功能，不参与招聘决策的制定，也不替代人工判断。
---
# 招聘

我们采用结构化的招聘流程，以提升招聘效率并确保招聘到更优秀的候选人。

## 重要的隐私与安全措施

### 数据存储（至关重要）
- **所有招聘数据仅存储在本地**：`memory/recruiting/`
- **候选人信息绝不对外共享**
- **不与任何外部招聘系统或人力资源系统集成**
- **不使用简历解析服务**，仅进行人工审核
- 用户可完全控制数据的保留和删除

### 安全底线（不可协商）
- ✅ 编写职位描述和筛选标准
- ✅ 生成结构化的面试问题
- ✅ 跟踪候选人的招聘流程阶段
- ✅ 草拟沟通内容（供人工审核）
- ❌ **绝不对招聘决策负责**
- ❌ **绝不存储敏感的个人信息**（如社会安全号码、出生日期等）
- ❌ **绝不保证候选人的质量或预测招聘结果的成功率**
- ❌ **绝不替代人工在招聘过程中的判断**

### 公平招聘说明
虽然结构化的流程有助于提高招聘的公平性，但无法完全消除偏见。在所有决策环节都需要人工审核。

## 快速入门

### 数据存储设置
招聘数据存储在您的本地工作空间中：
- `memory/recruiting/jobs.json` – 职位信息及要求
- `memory/recruiting/candidates.json` – 候选人资料及状态
- `memory/recruiting/pipeline.json` – 招聘流程阶段
- `memory/recruiting/interviews.json` – 面试指南及记录
- `memory/recruiting/communications.json` – 电子邮件模板及草稿

请使用 `scripts/` 目录中的脚本进行所有数据操作。

## 核心工作流程

### 创建职位描述
```
User: "Write a job description for a senior engineer"
→ Use scripts/create_job.py --title "Senior Engineer" --level senior
→ Generate JD with requirements, responsibilities, and screening criteria
```

### 筛选候选人
```
User: "Screen this resume for the PM role"
→ Use scripts/screen_candidate.py --job-id "JOB-123" --resume "resume.pdf"
→ Evaluate against job criteria, output match assessment
```

### 准备面试
```
User: "Prepare interview questions for the design role"
→ Use scripts/prep_interview.py --job-id "JOB-123" --type behavioral
→ Generate structured question set
```

### 跟踪招聘流程
```
User: "Update candidate status to phone screen complete"
→ Use scripts/update_pipeline.py --candidate-id "CAND-456" --stage "phone-screen" --status completed
→ Move candidate in pipeline, set next actions
```

### 草拟沟通内容
```
User: "Draft rejection email for candidate"
→ Use scripts/draft_email.py --type rejection --candidate-id "CAND-456"
→ Generate professional, personalized message for human review
```

## 模块参考

有关详细实现方式，请参阅：
- **职位描述**：[references/job-descriptions.md](references/job-descriptions.md)
- **简历筛选**：[references/resume-screening.md](references/resume-screening.md)
- **面试准备**：[references/interview-prep.md](references/interview-prep.md)
- **流程跟踪**：[references/pipeline-tracking.md](references/pipeline-tracking.md)
- **沟通**：[references/communications.md](references/communications.md)
- **公平招聘**：[references/fair-hiring.md](references/fair-hiring.md)

## 脚本参考

| 脚本 | 用途 |
|--------|---------|
| `create_job.py` | 创建包含职位要求的招聘信息 |
| `screen_candidate.py` | 根据标准评估简历 |
| `prep_interview.py` | 生成面试问题集 |
| `add_candidate.py` | 将候选人加入招聘流程 |
| `update_pipeline.py` | 更新候选人的流程状态 |
| `view_pipeline.py` | 查看当前的招聘流程进度 |
| `draft_email.py` | 生成电子邮件模板 |
| `set_reminder.py` | 设置跟进提醒 |
| `generate_report.py` | 生成招聘绩效报告 |

## 免责声明

本技能仅提供招聘流程的支持。所有招聘决策仍由招聘经理和组织负责。本技能不保证候选人的质量或招聘的成功率。请始终遵守适用的就业法律法规。