---
name: prompt-rewriter
description: 高级提示重写与优化服务。该服务会分析提示语句的清晰度、具体性、结构、完整性和可用性，识别其中的不足之处，提出改进建议，并生成多种重写方案。适用于用户希望提升现有提示的有效性、了解提示为何无法正常工作、为A/B测试生成提示变体，或通过实例学习提示工程的最佳实践的场景。
---

# 提示重写器

## 概述

该工具帮助用户将模糊、无效的提示转化为结构清晰、表达有力的指令，从而让AI模型能够产生一致且高质量的结果。它从多个维度分析提示的质量，并提供可操作的改进建议。

## 快速入门

**用户输入**：“帮我重写这个提示：‘写一篇关于AI的博客文章’”

**你应该**：
1. 分析原始提示的不足之处（过于模糊、未指定目标受众、未定义格式）
2. 确定需要改进的方面（增加主题的针对性、明确目标受众、调整语气、确定长度和结构）
3. 提供2-3个不同的重写方案
4. 解释这些修改的内容及其重要性

---

## 核心功能

### 1. 提示质量分析

从五个关键维度评估提示的质量：

**清晰度**（0-2分）：
- 请求是否明确？
- 术语是否定义清楚？
- Claude能否在不需要额外解释的情况下理解请求？

**具体性**（0-2分）：
- 约束条件是否明确？
- 是否指定了输出格式？
- 是否界定了工作的范围？

**结构**（0-2分）：
- 信息是否逻辑清晰？
- 如果适用，步骤是否明确？
- 是否有明确的框架？

**完整性**（0-2分）：
- 是否提供了足够的背景信息？
- 需求是否全面？
- 是否指出了缺失的信息？

**可用性**（0-2分）：
- 该提示是否可重复使用？
- 是否容易进行调整？
- 语言表达是否自然？

**评分标准**：
- 8-10分：优秀的提示，只需稍作调整
- 6-7分：不错的提示，有中等程度的改进空间
- 4-5分：功能尚可，但存在明显不足
- 0-3分：较差的提示，需要大幅修改

### 2. 重写生成

使用不同的方法生成2-3个重写版本：

**版本1：保守型改进**
- 保持原始意图
- 增加具体性和结构
- 最小限度地调整语言风格
- 适合希望保留原有表达方式的用户

**版本2：技术优化**
- 应用提示工程技巧（如CoT、Few-Shot等）
- 添加高级技术
- 专注于提升效果
- 适合希望获得最佳结果的用户

**版本3：简化版**
- 在保留核心要求的同时减少复杂性
- 使表达更加口语化
- 适合初学者或需要快速完成任务的场景

### 3. 改进说明

对于每个重写版本，解释：
- 做了哪些修改
- 为什么这些修改很重要（对AI输出的影响）
- 适用于哪些场景

### 4. 技巧应用

应用经过验证的提示工程技巧：

**思维链（CoT）**
- “让我们一步步来思考”
- “首先，分析……然后，评估……”
- 适用于需要复杂推理、数学计算或逻辑分析的场景

**Few-Shot学习**
- 在提出请求前提供2-3个示例
- 例如：示例1 → 示例2 → 示例3 → 你的任务
- 适用于需要明确格式或风格匹配的场景

**角色扮演式提示**
- “扮演一名高级工程师……”
- “你是一名市场营销专家……”
- 适用于需要特定知识或控制语气的场景

**输出结构**
- 使用模板和标题
- 明确划分各个部分
- 适用于报告撰写、文档编写或需要结构化内容的场景

**约束条件设置**
- “将回复限制在500字以内”
- “为非技术受众避免使用专业术语”
- 适用于控制回复长度或提高可读性的场景

### 5. A/B测试指导

帮助用户有效测试提示：
- 系统地生成多个版本
- 提供测试方法建议
- 推荐评估标准

---

## 工作流程

### 第1步：接收并分析

1. 提取需要重写的提示
2. 理解用户的意图（他们想要达到什么目标？）
3. 检查是否存在任何约束条件（语气、格式、长度、受众）
4. 根据五个质量维度进行评估
5. 计算得分并确定主要问题

### 第2步：生成重写版本

1. **版本1（保守型改进）**：增加结构、明确术语、定义输出格式
2. **版本2（技术优化）**：应用相关技巧（如CoT、Few-Shot等）
3. **版本3（简化版）**：使表达更加口语化

### 第3步：展示选项

对于每个重写版本：
- 展示改进后的提示
- 解释所做的修改
- 强调使用了哪些技巧
- 根据具体情况推荐使用哪个版本

### 第4步：教育性说明

简要解释：
- 应用了哪些提示工程技巧
- 这些技巧为何适用于当前场景
- 用户如何在未来类似场景中应用这些技巧

---

## 常见问题及解决方法

### 问题：提示过于模糊

**问题示例**：“写一篇关于气候变化的文章”
**解决方法**：增加具体性——明确目标受众、写作目的和格式，以及文章的深度

**改进后的提示示例**：“为普通受众撰写一篇1000字的博客文章，解释气候变化的原因、影响及潜在解决方案。使用积极但现实的语气。内容包括：（1）吸引读者的引言；（2）包含数据的三个主要部分；（3）提供实际建议的结论。”

### 问题：缺乏结构

**问题示例**：“分析这些数据”
**解决方法**：为分析添加框架或详细的步骤说明

**改进后的提示示例**：“分析所提供的销售数据。按照以下结构组织你的回答：
1. **执行摘要**（列出三个关键发现）
2. **详细分析**（按地区和产品分类）
3. **趋势识别**（找出其中的规律）
4. **建议**（基于数据分析提出三个可操作的步骤）

### 问题：缺乏背景信息

**问题示例**：“改进这封邮件”
**解决方法**：补充关于受众、目标和约束条件的信息

**改进后的提示示例**：“为C级高管修改这封邮件。目标：获得一个5万美元项目的批准。邮件长度控制在200字以内。语气：专业且具有说服力。当前邮件内容：[粘贴]”

### 问题：输出格式不明确

**问题示例**：“创建营销内容”
**解决方法**：明确输出格式和风格要求

**改进后的提示示例**：“为我们的新产品发布创建营销内容。输出内容包括：
1. **社交媒体帖子**（LinkedIn，150字，专业语气）
2. **邮件摘要**（75字，强调产品的吸引力）
3. **网站标题**（简洁且吸引人）
4. **三个关键优势**（每个优势不超过15字）”

---

## 示例

### 示例1：内容创作

**输入提示**：“写一篇关于远程工作的文章”

**分析**：
- 清晰度：1/2（主题明确，但具体内容不明确）
- 具体性：0/2（没有格式、受众或长度要求）
- 结构：0/2（没有框架）
- 完整性：0/2（缺少关键细节）
- 可用性：1/2（勉强可重复使用）
**评分：2/10**——多个维度都存在明显不足

**重写版本1（保守型改进）**：
```
Write a 1500-word article about remote work for business professionals. Cover:
1. Benefits of remote work (productivity, cost savings, flexibility)
2. Challenges (isolation, communication, work-life balance)
3. Best practices for success (routine, communication tools, workspace setup)
4. Future trends (hybrid models, technology evolution)

Tone: Informative and balanced
Format: Use headings and bullet points
```

**重写版本2（技术优化）**：
```
Act as an experienced remote work consultant. Write a comprehensive article about remote work for business leaders considering transitioning their teams.

Structure your response using the following framework:

**Introduction (150 words)**
- Hook with a surprising statistic
- Briefly state the article's purpose
- Outline what will be covered

**Section 1: The Business Case (400 words)**
Let's think about this step by step:
- Analyze cost benefits (real estate, equipment, turnover)
- Evaluate productivity studies (with data sources)
- Consider talent access (hiring from anywhere)

**Section 2: Implementation Challenges (350 words)**
- Communication breakdowns (provide examples)
- Culture maintenance (specific strategies)
- Performance management (tools and metrics)

**Section 3: Success Framework (400 words)**
Provide a concrete 90-day rollout plan:
- Month 1: Foundation and tools
- Month 2: Training and feedback
- Month 3: Optimization and refinement

**Conclusion (200 words)**
- Summarize key takeaways
- Provide 3 actionable next steps
- End with an inspiring vision

Tone: Professional yet engaging
Examples: Include 2-3 real company case studies
```

**重写版本3（简化版）**：
```
Write an article about remote work. Make it about 1500 words long and aimed at business people who are thinking about letting employees work from home. Talk about:
- Why it's good (saves money, people like it)
- What's hard (staying in touch, managing performance)
- How to do it right (tools, schedules, clear expectations)

Use a helpful, informative tone with clear headings.
```

**建议**：如果用户希望获得最佳效果，建议使用版本2；如果需要清晰性和专业性，可以使用版本1；如果需要快速完成任务，可以使用版本3。

---

### 示例2：代码审查

**输入提示**：“审查这段代码”

**分析**：
- 清晰度：0/2（完全不清楚需要审查的内容）
- 具体性：0/2（没有审查标准或范围）
- 结构：0/2（没有框架）
- 完整性：0/2（缺少所有背景信息）
- 可用性：0/2（无法重复使用）
**评分：0/10**——需要彻底重写

**重写版本1（保守型改进）**：
```
Review the code provided below. Focus on:
1. Bugs or errors
2. Performance issues
3. Code style and readability
4. Potential security vulnerabilities

Provide specific line references and suggestions for each issue found.
```

**重写版本2（技术优化）**：
```
Act as a senior software engineer conducting a thorough code review. Analyze the provided code following this systematic approach:

**Step 1: Functional Analysis**
Let's check if the code works correctly:
- Verify logic correctness (walk through execution)
- Check edge cases (null inputs, empty arrays, boundary conditions)
- Validate error handling (try-catch blocks, meaningful error messages)

**Step 2: Performance Evaluation**
Analyze computational complexity:
- Time complexity: Big-O notation
- Space complexity: Memory usage
- Identify any O(n²) or worse bottlenecks
- Suggest optimization opportunities

**Step 3: Security Review**
Look for common vulnerabilities:
- SQL injection risks
- XSS vulnerabilities
- Improper input validation
- Sensitive data exposure

**Step 4: Code Quality**
Assess adherence to best practices:
- Naming conventions (descriptive, consistent)
- Comments (helpful, not redundant)
- DRY principle (Don't Repeat Yourself)
- Single Responsibility Principle

**Step 5: Recommendations**
Provide:
- Priority-ranked list of issues (Critical > High > Medium > Low)
- Specific code examples for fixes
- Refactoring suggestions for improvement

Code to review:
```

**重写版本3（简化版）**：
```
Look at this code and tell me what's wrong or could be better. Check for bugs, slow parts, security issues, and things that are hard to understand. Give me specific suggestions with examples.

Code:
```

**建议**：版本2适合专业代码审查；版本1适合快速检查；版本3适合非正式的反馈或初学者。

---

### 示例3：邮件撰写

**输入提示**：“写一封请求会议的邮件”

**分析**：
- 清晰度：1/2（意图明确，但背景信息不足）
- 具体性：0/2（没有明确目的、议程或收件人类型）
- 结构：0/2（没有格式要求）
- 完整性：0/2（缺少所有细节）
- 可用性：1/2（勉强可重复使用）
**评分：2/10**——需要大幅改进

**重写版本1（保守型改进）**：
```
Write an email requesting a meeting with [recipient name]. Purpose: Discuss [topic].

Include:
- Brief introduction (context)
- Meeting purpose (why we need to meet)
- Proposed agenda (3-4 bullet points)
- Suggested time options (provide 2-3 alternatives)
- Call to action (confirmation request)

Tone: Professional and respectful
Length: Under 200 words
```

**重写版本2（技术优化）**：
```
Act as an executive assistant drafting a meeting request email to [recipient type, e.g., senior executive/client].

Context: We need to discuss [specific topic] to [desired outcome].

Apply these principles:

**Subject Line Best Practice**
Make it specific and actionable: "Meeting Request: [Topic] - [Urgency/Timeframe]"
Example: "Meeting Request: Q1 Strategy Alignment - This Week"

**Opening Strategy**
First, establish relevance in 1 sentence:
- Reference prior conversation
- Mention shared goal or project
- Acknowledge their value/time

**Value Proposition Frame**
Instead of "I want to meet," use "We'll achieve X by meeting together":
- "In 30 minutes, we can finalize the project timeline"
- "This discussion will unblock the next phase of development"

**Agenda Structure**
Use the SCQA framework:
1. **Situation** (current state)
2. **Complication** (what's blocking us)
3. **Question** (decision needed)
4. **Answer** (your recommendation)

**Time Options Psychology**
Offer specific times with psychological anchors:
- Tuesday 2pm (after lunch, high energy)
- Thursday 10am (start of week, fresh)
- Friday 3pm (end of week, closure mindset)

**Closing**
Make it easy to say yes:
- "If these don't work, suggest your best time"
- "I'll adjust to accommodate your schedule"

Tone: Respectful of their time, clear on value
Length: 150-180 words
```

**重写版本3（简化版）**：
```
Write a short email asking for a meeting with [name]. We need to talk about [topic]. Suggest a few times that would work, mention what we'll cover, and ask them to confirm. Keep it friendly and brief.
```

**建议**：版本2适合重要的商务沟通；版本1适合日常的内部邮件；版本3适合非正式的请求。

---

## 高级技巧

### 多重重写进行A/B测试

当用户需要系统地测试多个提示时：

1. **基础版本**：原始提示
2. **版本A**：修改一个变量（例如，添加示例）
3. **版本B**：修改另一个变量（例如，增加角色）
4. **版本C**：结合A和B的修改

**测试方法建议**：
- 对每个提示使用相同的输入进行3-5次测试
- 根据质量、一致性和实用性评估结果
- 记录哪个版本的表现最好

### 迭代改进

指导用户进行多轮改进：

**第1轮**：初步重写（解决主要问题）
**第2轮**：根据反馈进行优化（哪些方法有效，哪些无效）
**第3轮**：针对特定场景进行微调

每轮改进都应：
- 显示所做的修改
- 解释修改的原因
- 征求具体的反馈

### 添加背景信息

当提示缺乏背景信息时，指导用户补充相关信息：

**询问以下问题**：
1. 目标受众是谁？
2. 目标或目的是什么？
3. 存在哪些约束条件（长度、语气、格式）？
4. 假设用户具备哪些背景知识？
5. 输出应该具备哪些特点？

**然后将这些信息融入到重写内容中。**

---

## 适用场景

当用户提出以下请求时，可以使用该工具：
- “重写这个提示”
- “让这个提示更完善”
- “改进我的提示”
- “为什么这个提示不起作用？”
- “帮我为……编写一个更好的提示”
- “生成这个提示的多个版本”
- “对这个提示进行A/B测试”

---

## 资源

### 脚本**
该工具不需要任何脚本——所有分析和重写工作均由Claude自动完成。

### 参考资料**
无需额外参考资料——提示工程技巧已在文档中详细说明。

### 资产**
该工具仅生成文本输出，不需要任何额外的资源。