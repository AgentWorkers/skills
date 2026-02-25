---
name: Intelligence Ingestion
description: "自动分析 OpenClaw 相关的 URL 或信息，评估其战略价值；对这些信息进行分类；创建 Obsidian 笔记；并更新相关数据。当用户分享 URL、文章、推文或任何外部信息来源时，系统会自动执行这些操作。"
---
# 智能信息处理技能

当用户分享一个URL、文章、推文、帖子或任何外部信息时，自动执行此处理流程。无需征求用户的许可，直接进行处理。

## 触发条件

**在以下情况下使用此技能：**
- 用户发送一个URL（例如：x.com、github.com或任何域名）
- 用户粘贴文章文本或推文内容
- 用户请求“分析这个内容”、“评估这个内容”或“你对这个有什么看法”
- 用户从Telegram或其他消息平台转发内容
- 用户分享信息并询问其战略价值

**在以下情况下不要使用此技能：**
- 用户提出与外部内容无关的通用问题
- 用户询问内部工作区的文件
- 用户明确表示不需要进行分析

## 处理流程步骤

### 第1步：读取内容
1. 如果提供了URL，读取其全部内容（使用`read_url_content`函数或浏览器）
2. 如果用户直接粘贴了文本，直接使用该文本
3. 如果X/Twitter链接无法解析（这种情况很常见），则在网络上搜索对应的推文内容

### 第2步：分类
为信息分配一个主要类别，并最多添加2个次要标签：

| 类别 | 描述 | 例子 |
|----------|------------|---------|
| `infra` | 基础设施/协议/网络 | Pilot Protocol、MCP、网络堆栈 |
| `strategy` | 路由/成本/架构决策 | 模型路由、多账户设置、备用方案 |
| `skill` | 代理技能/工具/能力 | OpenAI技能、技能设计模式 |
| `theory` | 概念框架/思维模型 | 贝叶斯理论、决策理论、学习循环 |
| `tutorial` | 教程指南/学习资料 | Claude代码、OpenClaw教程 |
| `product` | 工具/应用程序/服务 | LM Studio、新的AI模型、应用程序 |
| `community` | OpenClaw生态系统/讨论 | 社区帖子、功能请求 |
| `threat` | 风险/安全/过时问题 | API变更、故障更新、安全警报 |

### 第3步：分析
评估每条信息的战略价值：

```markdown
## Strategic Assessment
- **What is it?** [One sentence]
- **What can it do for us?** [Specific capability/benefit]
- **What can we build with it?** [Concrete output/project]
- **Strategic value:** [🔴 Critical / 🟡 High / 🟢 Medium / ⚪ Low]
- **Competitive edge:** [What advantage over people who don't have this?]
- **Relation to active bottleneck:** [Does it relate to context overflow/token saving?]
```

请参考`MEMORY.md`文件中的“当前工程瓶颈”部分，了解当前的工程瓶颈。

### 第4步：关联现有架构
检查该信息对OpenClaw架构的影响，并记录其与现有组件的依赖关系和协同效应。

### 第5步：创建Obsidian笔记
在指定的位置创建笔记：
```
/Volumes/T7 Shield/Obsidian_Vault/20_Intelligence/YYYYMMDD_AuthorOrSource_ShortTitle.md
```

请严格按照以下模板编写笔记：
```markdown
# [Title]

**Source:** [Link](URL)
**Date:** YYYY-MM-DD
**Category:** [Primary Category] / [Secondary Tags]
**Strategic Value:** [🔴/🟡/🟢/⚪] + one-line reason
**Relation to Active Bottleneck:** [Yes/No + how]

---

## Summary
[2-3 paragraphs of core content]

## Key Takeaways
[Numbered list of actionable insights]

## Impact on OpenClaw Architecture
[How this relates to our stack]

## Action Items
[What to do next, if anything]

---

**Keke's Note:** [Opinionated analysis in Keke's voice — direct, no-BS, relate to 阳哥's goals]
```

### 第6步：更新记录
1. **务必**将处理结果添加到当天的日志文件中：`~/.openclaw/workspace/memory/YYYY-MM-DD.md`
2. **如果信息具有极高的战略价值（标记为🔴）**：同时更新`MEMORY.md`文件（标记为“待处理事项”或“当前瓶颈”）
3. **如果信息涉及新的原则或理念**：标记为可能需要更新`PRINCIPLES.md`文件
4. **如果信息涉及新的工具或服务**：标记为可能需要更新`TOOLS.md`文件

### 第7步：回复用户
向用户提供简洁的总结：
```
📥 已摄取: [Title]
📂 类别: [Category]
🎯 战略价值: [🔴/🟡/🟢/⚪] [One-line reason]
💾 已存档: Obsidian → 20_Intelligence/[filename]
📝 已记录: memory/YYYY-MM-DD.md
🔗 关联: [Which existing component it relates to]
⚡ 建议行动: [Next step, if any]
```

## 特殊情况处理
- **一条消息中包含多个URL**：分别处理每个URL，并创建相应的Obsidian笔记
- **重复或相似的内容**：检查是否已有类似的笔记，如果存在则合并或引用，避免重复记录
- **非英文内容**：使用原始语言进行分析，并用中文撰写笔记（保持与现有笔记的风格一致）
- **受版权保护或无法访问的内容**：记录为“内容不可用”，并依据用户提供的信息进行处理
- **用户提供了自己的分析**：尊重用户的判断，不要直接覆盖他们的分析结果——他们最了解自己的系统

## 质量检查清单
在完成处理前，请确认以下内容：
- [ ] Obsidian笔记的文件名格式正确
- [ ] 当天的日志文件已更新
- [ ] 源URL已保存在笔记中
- [ ] 信息的相关性已根据当前工程瓶颈进行了评估
- [ ] 概述内容包含具体的分析意见（而非泛泛而谈）
- [ ] 用户已收到处理结果的确认信息