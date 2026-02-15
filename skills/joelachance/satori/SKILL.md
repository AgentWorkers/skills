---
name: satori
description: |
  Persistent long term memory for for continuity in ai sessions between providers and codegen tools.
  
  TRIGGERS - Activate this skill when:
  - User explicitly mentions "satori", "remember this", "save", "add",  "save this for later", "store this", "add to memory"
  - User asks to recall/search past decisions: "what did we decide", "remind me", "search my notes", "what do I know about"
  - Conversation contains notable facts worth persisting: decisions, preferences, deadlines, names, tech stack choices, strategic directions
  - Starting a new conversation where proactive context retrieval would help
  - Use Satori search when user asks a question
---

# Satori CLI 集成

Satori 能够在多个 AI 应用程序中持久化存储重要的信息。它将事实数据存储在向量数据库和知识图谱数据库中，以便日后检索。

## 环境要求

**支持的环境：** Claude Code、Cursor、Windsurf 或任何具有本地终端访问权限的 AI 工具。

## 认证

首次运行时，CLI 会自动进行配置：
- 检查 `~/.config/satori/satori.json` 文件中的 API 密钥和内存 ID
- 如果文件不存在，会自动创建该文件并生成新的认证凭据
- 无需手动设置

## CLI 命令

**保存事实：**
```bash
npx -y @satori-sh/cli@latest add "<facts>"
```

**搜索相关内容：**
```bash
npx -y @satori-sh/cli@latest search "<query>"
```

## 工作流程：主动搜索

在对话开始时，如果用户的消息表明某些现有信息可能对对话有帮助，系统会执行以下操作：
1. 从用户的第一条消息中提取关键实体/主题
2. 使用相关查询执行搜索命令
3. 解析 JSON 响应以获取相关事实
4. 将检索到的信息悄悄地整合到对话响应中
5. 除非搜索结果对响应有重大影响，否则不会显示“我已查询了 Satori”

**解析搜索结果：**
CLI 以 JSON 格式返回结果。需要从中提取相关事实并将其用作对话的上下文：
```bash
npx -y @satori-sh/cli search "Flamingo project tech stack"
# Returns JSON with matching facts - parse and incorporate naturally
```

**触发主动搜索的示例：**
- “我们继续讨论 [项目] 吧”
- “[某件事] 的进展如何？”
- 提到过去未提供完整背景的决策
- 项目名称、公司名称、人名

## 工作流程：保存事实

### 何时保存事实

在以下情况下保存事实：
- 决策讨论结束时
- 用户明确要求保存时（例如：“记住这个”“保存这个”
- 在确定了具体的偏好、名称、日期或截止日期后
- 在建立了重要的项目背景信息后

### 保存的内容

详细的标准请参见 `references/fact-criteria.md` 文件。

**可保存的信息：**
- **重要的、持久化的数据：**
  - 决策：“使用 PostgreSQL 作为数据库”
  - 技术偏好：“用户更喜欢使用 Bun 而不是 Node.js”
  - 名称/品牌：“公司名称是 Flamingo，他们生产粉色饼干”
  - 日期/截止日期：“MVP 的截止日期是 3 月 15 日”
  - 架构选择：“采用微服务架构并使用事件驱动机制”
  - 战略方向：“优先针对企业客户”
  - 关键联系人：“Sarah 是设计负责人”
  - 项目背景：“Satori 是一家提供 AI 记忆基础设施服务的公司”

**不可保存的信息：**
- **临时性、细节性或显而易见的信息：**
  - 还在讨论中的反馈：“颜色方案需要改进”
  - Claude 的解释或代码片段
  - 临时调试信息
  - 从对话中可以推断出的通用偏好
  - 用于填充对话的无关内容

### 保存流程

1. 从对话中提取重要的事实（遵循保存标准）
2. 将相关事实整理成自然语言格式
3. 执行 CLI 命令进行保存
4. 如果成功：默默地继续对话（无需额外提示）
5. 如果失败：向用户显示错误信息

**批量处理：** API 支持批量保存，因此较长的自然语言文本也可以被保存：
```bash
npx -y @satori-sh/cli add "User is building Satori, an AI memory infrastructure company. Tech stack: TypeScript, Bun, PostgreSQL. Deadline for MVP is March 15. Targeting developer tools market initially."
```

## 错误处理

如果 CLI 失败或未安装，系统会给出相应的错误提示：
```
⚠️ Satori CLI error: [error message]
To install: npm install -g @satori-sh/cli
Facts were not saved. Would you like me to show what I attempted to save?
```

## 事实信息的格式化

事实信息应写成清晰、独立的陈述，并附上相应的上下文，以便日后能够准确理解其含义：
**正确的格式：** “Satori 项目使用 PostgreSQL 作为主要存储系统，FalkorDB 用于存储知识图谱”
**错误的格式：** “使用 Postgres 和 FalkorDB”

**正确的格式：** “用户偏好在所有 JavaScript/TypeScript 项目中使用 Bun 而不是 Node.js”
**错误的格式：** “Bun 而不是 Node.js”