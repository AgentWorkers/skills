---
name: knowledge-capture
description: 将对话和讨论内容转换为结构化的 Notion 文档
---
## 概述

“知识捕获”（Knowledge Capture）技能能够将对话、讨论以及非结构化的信息转换为在 Notion 中组织有序的文档。它通过记录重要的对话内容，并将其转化为可执行、格式规范的文档，帮助您保存机构知识。

## 使用场景

当您需要以下操作时，可以使用此技能：
- 将会议记录或对话笔记转换为结构化的文档
- 创建包含行动项的会议总结
- 从讨论中整理出知识库文章
- 将重要对话存档以供将来参考
- 从讨论中提取关键见解和决策

## 主要功能

- **智能内容提取**：自动识别对话中的关键点、决策和行动项
- **结构化组织**：生成层次分明、格式规范的 Notion 文档
- **元数据捕获**：保存参与者、日期和上下文信息
- **行动项跟踪**：提取并格式化带有负责人和截止日期的行动项
- **交叉链接**：自动创建指向相关文档和团队成员的链接

## 使用要求

- **Notion API 访问权限**：需要具有适当权限的集成令牌
- **目标工作空间**：用于存储文档的 Notion 工作空间
- **模板（可选）**：预定义的 Notion 模板，以确保文档结构的一致性

## 实现细节

该技能通过 Notion API 完成以下操作：
1. 解析输入内容（文本、会议记录或讨论笔记）
2. 使用结构分析提取关键信息
3. 根据 Notion 文档格式要求对内容进行格式化
4. 创建或更新包含捕获信息的 Notion 页面
5. 维护文档之间的交叉引用和关联关系

### 典型工作流程

```
Input: Conversation/Discussion
  ↓
Parse & Extract
  ↓
Identify: Key Points, Decisions, Action Items
  ↓
Format for Notion
  ↓
Create/Update Notion Document
  ↓
Output: Structured Documentation
```

## 使用案例

1. **团队会议笔记**
   - 输入：会议记录
   - 输出：包含决策和下一步行动的整理后的会议总结

2. **客户通话记录**
   - 输入：通话记录和文字记录
   - 输出：包含关键需求的客户交互记录

3. **架构设计讨论**
   - 输入：设计讨论笔记
   - 输出：包含多种方案及理由的架构设计决策记录

4. **面试记录**
   - 输入：面试记录
   - 输出：结构化的候选人或用户研究文档

## 配置设置

请配置以下环境变量或 Notion 设置：

```env
NOTION_API_TOKEN=your_token_here
NOTION_DATABASE_ID=your_database_id
```

## 相关技能

- [研究文档](/skills/research-documentation) - 用于研究相关的文档编写
- [会议智能](/skills/meeting-intelligence) - 用于会议准备和后续处理
- [Notion API 文档](https://developers.notion.com) - Notion API 的官方文档