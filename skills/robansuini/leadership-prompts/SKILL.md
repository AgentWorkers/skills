---
name: leadership-prompts
description: 精选了25个经过实战验证的提示，适用于工程领导者：包括一对一准备、团队状况评估、事件回顾、技术策略制定、招聘、职业发展以及与利益相关者的沟通等场景。这些提示基于超过13年的工程管理经验总结而成。
homepage: https://leadingin.tech
license: MIT
metadata:
  clawdis:
    emoji: 🎯
    requires:
      bins: [node]
---
# 领导力引导问题库（Leadership Prompts）

这是一个专为工程经理、技术主管、工程副总裁（VP of Engineering）和首席技术官（CTO）设计的、经过实战检验的问题库。这些问题并非泛泛而谈的“关于领导力的问题”，而是针对你们每周面临的实际挑战而设计的、具有明确导向性的框架。

## 适用对象

- 管理5至15人团队的工程经理  
- 在技术部门与管理层之间协调工作的技术主管  
- 负责管理其他经理的总监或副总裁  
- 仍亲力亲为处理日常工作的首席技术官  

## 分类  

| 分类 | 数量 | 适用场景 |  
|---|---|---|  
| **一对一沟通准备** | 4 | 在进行任何非例行的一对一沟通之前  
| **团队状况评估** | 4 | 在经历业绩不佳的季度、团队内部冲突、裁员或远程工作导致沟通不畅之后  
| **事件回顾** | 3 | 在事件解决后的48小时内  
| **技术战略规划** | 4 | 在季度规划、架构评审或选择自研/外包方案时  
| **招聘与面试** | 3 | 在招聘新成员、优化招聘流程或确定最终人选时  
| **职业发展** | 4 | 在晋升周期、提供反馈或进行员工留任谈话时  
| **利益相关者沟通** | 4 | 在向高管汇报、拒绝请求、跨部门协调或组织重组时  

## 快速上手  

### 使用命令行界面（CLI）  

```bash
# List all categories
node scripts/leadership-prompts.js list

# Get a random prompt (great for manager skill-building)
node scripts/leadership-prompts.js random

# Search by keyword
node scripts/leadership-prompts.js search "promotion"

# Show a specific prompt by ID
node scripts/leadership-prompts.js show career-dev-promotion

# Get all prompts in a category
node scripts/leadership-prompts.js category "Team Health"
```  

### 与AI助手配合使用  

只需告诉您的AI助手：  
> “我需要为与表现不佳的员工进行一对一沟通做准备。请使用‘领导力引导问题库’找到合适的问题，并指导我如何使用它。”  
> 或者：  
> “展示‘领导力引导问题库’中所有的招聘相关问题。”  

## 如何使用问题  

每个问题都包含 `{curly_braces}` 中的 **占位符变量**。请根据实际情况填写这些变量。填写得越具体，得到的结果就越准确。  

**示例：**  
问题内容：  
> “我正在为与一名表现不佳的直接下属进行一对一沟通做准备……”  
您需要填写：  
> “我正在为与一名表现不佳的直接下属进行一对一沟通做准备，该下属在过去{时间范围}内表现不佳……”  

## 问题设计原则  

这些问题的设计目的如下：  
1. **确保结构清晰**：这些问题采用特定的框架（如SBI、RACI、RAG状态等），使输出内容具有可操作性，而非冗长无序。  
2. **直面棘手问题**：例如“准备好应对对方的抵触情绪”或“知道何时需要向上级汇报”。  
3. **提供明确的观点**：例如“高管汇报是团队对外展示的形象”，这并非中立的建议，而是基于实际经验得出的观点。  
4. **产出可执行的结果**：每个问题都会指定一种可以直接用于会议、文档或对话的输出格式。  
5. **考虑现实中的政治因素**：真正的领导力往往涉及复杂的利益关系。这些问题会考虑到这些因素，而不仅仅是最佳实践。  

## 添加自己的问题  

您可以根据现有的格式向 `prompts.json` 文件中添加新的问题。  

```json
{
  "id": "category-short-name",
  "category": "Category Name",
  "title": "Human-readable title",
  "prompt": "The actual prompt text with {variables}",
  "context": "When to use this prompt",
  "output_format": "What the AI should produce",
  "example": "A filled-in example showing real usage"
}
```  

## 致谢  

该问题库由Rob创建——他自2011年起一直担任工程经理，目前运营着[leadingin.tech](https://leadingin.tech)网站。这些问题源自他在初创企业和成长型企业中管理团队的实际经验，而非管理类教科书的内容。