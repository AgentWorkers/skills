---
name: interview
description: 这是一个面试准备系统，具备公司信息研究、故事情节构建（用于面试准备）以及模拟面试练习的功能。当用户提及求职面试、面试准备、行为面试问题、薪资谈判或后续沟通时，可以使用该系统。该系统可以研究公司信息、建立面试相关资料库、运行模拟面试、制定薪资策略，并协助撰写后续沟通内容。不过，该系统并不能保证用户一定能获得工作机会。
---
# 面试技巧系统：帮助你赢得工作机会的准备工作

## 关键隐私与安全措施

### 数据存储（至关重要）
- **所有面试数据仅存储在本地**：`memory/interview/`
- **不连接任何外部招聘平台**  
- **不集成任何求职跟踪系统**  
- **不分享任何面试内容**  
- 用户可完全控制数据的保留和删除

### 安全注意事项
- ✅ 仔细研究公司和职位信息  
- ✅ 根据自身经验建立故事库（用于面试准备）  
- ✅ 进行模拟面试并获取反馈  
- ✅ 准备薪资谈判策略  
- ❌ **绝不要**保证能获得工作机会  
- ❌ **绝不要**提供虚假信息  
- ❌ **绝不要**用虚假准备替代真正的面试准备  

### 数据结构
面试数据存储在本地：
- `memory/interview/research.json` – 公司研究概要  
- `memory/interview/stories.json` – 面试故事库  
- `memory/interview/practice.json` – 模拟面试记录  
- `memory/interview/salary.json` – 薪资研究及策略  
- `memory/interview/feedback.json` – 面试后的反馈记录  

## 核心工作流程

### 研究公司  
```
User: "Research Acme Corp for my interview Friday"
→ Use scripts/research_company.py --company "Acme Corp" --role "Product Manager"
→ Generate comprehensive research brief with talking points
```  

### 构建面试故事  
```
User: "Help me build a story about the project failure"
→ Use scripts/build_story.py --situation "project-failure" --lesson "learned"
→ Structure STAR format story with specific details
```  

### 进行模拟面试  
```
User: "Run a mock interview for PM role"
→ Use scripts/mock_interview.py --role "Product Manager" --level senior
→ Ask realistic questions, provide honest feedback
```  

### 准备薪资谈判  
```
User: "How should I handle the salary question?"
→ Use scripts/prep_salary.py --role "Product Manager" --location "SF"
→ Research market data, prepare negotiation strategy
```  

### 起草跟进邮件  
```
User: "Draft thank you email for today's interview"
→ Use scripts/draft_followup.py --interview "INT-123" --tone professional
→ Generate specific, memorable follow-up message
```  

## 模块参考  
- **公司研究**：请参阅 [references/research.md](references/research.md)  
- **故事库构建**：请参阅 [references/stories.md](references/stories.md)  
- **模拟面试**：请参阅 [references/mock-interviews.md](references/mock-interviews.md)  
- **薪资谈判**：请参阅 [references/salary.md](references/salary.md)  
- **难题应对**：请参阅 [references/difficult-questions.md](references/difficult-questions.md)  
- **跟进策略**：请参阅 [references/followup.md](references/followup.md)  
- **应对拒绝**：请参阅 [references/rejection.md](references/rejection.md)  

## 脚本参考  
| 脚本 | 用途 |  
|--------|---------|  
| `research_company.py` | 生成公司研究概要 |  
| `build_story.py` | 创建 STAR 格式的面试故事 |  
| `mock_interview.py` | 进行模拟面试 |  
| `prep_salary.py` | 准备薪资谈判策略 |  
| `draft_followup.py` | 起草跟进邮件 |  
| `analyze_role.py` | 分析职位描述 |  
| `identify_gaps.py` | 识别经验差距 |  
| `log_feedback.py` | 记录面试后的反馈 |