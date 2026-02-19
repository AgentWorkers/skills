---
name: last30days
description: 在过去的30天内，你可以在Reddit、X（前身为Twitter）以及网络上搜索任何主题。通过这种方式，你可以在7分钟内获取最新的趋势、社区的真实反馈以及实用的见解，而如果手动进行调研的话，这个过程可能需要长达2小时。
version: 2.0.0
author: theflohart
tags: [research, trends, reddit, twitter, competitive-intel, content-research]
---
# /last30days 研究技能

**实时情报引擎：** 查找当前有效的方法和趋势，而非上个季度的信息。

该技能会扫描过去30天内的Reddit、X（Twitter）和网页内容，识别其中的模式，提取社区观点，并提供可直接使用的情报提示。

## 为什么选择这个技能而非ChatGPT？

**使用ChatGPT进行“[主题]研究”的问题：** ChatGPT的训练数据是几个月甚至几年前的，它提供的是通用知识，而非最新的信息。

**使用其他工具的问题：** 虽然可以搜索网页，但会错过Reddit帖子和X上的对话，而这些地方正是实践者分享有效方法和趋势的地方。

**该技能的优势：**
1. **30天更新频率** – 仅获取最新内容（而非2023年的博客文章）。
2. **多平台整合** – 一次性整合Reddit（详细讨论）、X（实时信息）和网页（文章）。
3. **模式识别** – 突出在多个来源中多次出现的主题。
4. **情感分析** – 显示社区的整体情绪（热情、怀疑或沮丧）。
5. **即用型输出** – 提供可直接复制的提示和行动建议，而不仅仅是摘要。

**你可以手动执行类似的操作：** 通过日期筛选在Reddit、X和Brave Search中搜索，阅读30多个来源，识别模式并综合见解，但这需要2个多小时。而使用该技能只需7分钟。

## 适用场景

**非常适合：**
- **趋势发现**： “目前AI工具的热门趋势是什么？”
- **策略验证**： “2026年哪些内容营销策略有效？”
- **竞争情报**： “开发者对Cursor和Copilot的看法是什么？”
- **产品研究**： “用户对Notion的喜好和不满是什么？”
- **提示研究**： “哪些Claude提示技巧正在流行？”
- **社区情绪分析**： “营销人员对AI工具的看法如何？”

**不适用场景：**
- 历史研究（使用常规搜索）
- 学术/科学论文（使用Google Scholar）
- 非英语主题（覆盖范围有限）
- 完全没有在线讨论的主题

## 所需设置

该技能需要使用多个工具，请确保你已安装以下工具：
```bash
# 1. Brave Search API (for web_search)
# Already configured in OpenClaw by default

# 2. Bird CLI (for X/Twitter search)
source ~/.openclaw/credentials/bird.env && bird search "test" -n 1
# If this fails, install bird CLI first

# 3. Reddit Insights (optional but recommended)
# If you have reddit-insights MCP server configured, skill will use it
# Otherwise falls back to Reddit web search via Brave
```

**快速验证：**
```bash
/last30days --check-setup
```

验证结果应包括：
- ✅ Brave Search：已安装
- ✅ Bird CLI：已安装
- ✅ Reddit Insights：已安装（或显示“使用网页搜索作为备用方案”）

## 工作流程

### 第一步：网页搜索（更新频率 = 过去一个月）
```
web_search: "[topic] 2026" + freshness=pm
web_search: "[topic] strategies trends current"
web_search: "[topic] what's working"
```

**目的：** 获取最新的文章、博客文章和工具信息

### 第二步：Reddit搜索
**如果配置了reddit-insights MCP：**
```
reddit_search: "[topic] discussions techniques"
reddit_get_trends: "[subreddit]"
```

**否则：**
```
web_search: "[topic] site:reddit.com" + freshness=pm
web_search: "[topic] reddit.com/r/[relevant_sub]"
```

**目的：** 查找详细的讨论、实践者的观点以及实际有效的信息

### 第三步：X/Twitter搜索
```
bird search "[topic]" -n 10
bird search "[topic] 2026" -n 10
bird search "[topic] best practices" -n 10
```

**目的：** 获取实时信息、专家观点和热门帖子

### 第四步：深入分析主要来源（可选）
对最相关的2-3个链接进行深入分析：
```
web_fetch: [article URL]
```

**目的：** 提取具体策略、引用和数据点

### 第五步：综合与打包
1. **识别模式** – 在多个来源中多次出现的主题是什么？
2. **提取关键引用** – 获得最多点赞的Reddit评论和被转发的观点。
3. **评估情绪** – 用户的热情、采用情况、怀疑态度或沮丧情绪如何？
4. **创建即用型输出** – 提供提示和行动建议

## 输出模板

```markdown
# 🔍 /last30days: [TOPIC]
*Research compiled: [DATE]*  
*Sources analyzed: [NUMBER] (Reddit threads, X posts, articles)*  
*Time period: Last 30 days*

---

## 🔥 Top Patterns Discovered

### 1. [Pattern Name]
**Mentioned: X times across [platforms]**

[Description of the pattern + why it matters]

**Key evidence:**
- Reddit (r/[sub]): "[Quote from highly upvoted comment]"
- X: "[Quote from popular thread]"
- Article ([Source]): "[Key insight]"

---

### 2. [Pattern Name]
[Continue same format...]

---

## 📊 Reddit Sentiment Breakdown

| Subreddit | Discussion Volume | Sentiment | Key Insight |
|-----------|-------------------|-----------|-------------|
| r/[sub] | [# threads] | 🟢 Positive / 🟡 Mixed / 🔴 Skeptical | [One-liner takeaway] |

**Top upvoted insights:**
1. "[Quote]" — u/[username] (+234 upvotes)
2. "[Quote]" — u/[username] (+189 upvotes)

---

## 🐦 X/Twitter Signal Analysis

**Trending themes:**
- [Theme 1] - [# mentions]
- [Theme 2] - [# mentions]

**Notable voices:**
- [@handle]: "[Key take]"
- [@handle]: "[Key take]"

**Engagement patterns:**
[What types of posts are getting traction?]

---

## 📈 Web Article Highlights

**Most shared articles:**
1. "[Article Title]" — [Source] — [Key insight]
2. "[Article Title]" — [Source] — [Key insight]

**Common recommendations across articles:**
- [Tactic 1]
- [Tactic 2]
- [Tactic 3]

---

## 🎯 Copy-Paste Prompt

**Based on current community best practices:**

```
[包含发现模式的即用型提示]

**背景信息：** [来自研究的相关背景]
**任务：** [基于研究的明确任务]
**风格：** [根据研究结果调整语气/风格]
**注意事项：** [基于研究结果需要避免的特定内容]

## 实际示例

### 示例1：提示研究
**查询：`/last30days Claude提示的最佳实践`
**简化输出：**
```markdown
# 🔍 /last30days: Claude Prompting Best Practices

## Top Patterns Discovered

### 1. XML Tags for Structure (12 mentions)
Reddit and X both emphasize using XML tags for complex prompts:
- Reddit: "XML tags changed my Claude workflow. <context> and <task> make responses 3× more accurate."
- X: "@anthropicAI's own docs now recommend XML. It's the meta."

### 2. Examples Over Instructions (9 mentions)  
"Show, don't tell" — Provide 2-3 examples instead of long instructions.

### 3. Chain of Thought Explicit (7 mentions)
Add "Think step-by-step before answering" dramatically improves reasoning.

## Copy-Paste Prompt

<context>
[Your context here]
</context>

<task>
[Your task here]
</task>

<examples>
Example 1: [Show desired output style]
Example 2: [Show edge case handling]
</examples>

Think step-by-step before providing your final answer.
```

---

### 示例2：竞争情报
**查询：`/last30days Notion与Obsidian 2026年的对比`
**简化输出：**
```markdown
## Top Patterns

### 1. "Notion for Teams, Obsidian for Individuals" (18 mentions)
Strong consensus: Notion wins for collaboration, Obsidian wins for personal PKM.

### 2. Performance Complaints About Notion (11 mentions)
"Notion is slow with 1000+ pages" — recurring pain point

## Reddit Sentiment

| Subreddit | Sentiment | Key Insight |
|-----------|-----------|-------------|
| r/Notion | 🟡 Mixed | Love features, frustrated by speed |
| r/ObsidianMD | 🟢 Positive | Passionate community, local-first advocates |

## Action Ideas

**If building a PKM tool:**
1. Positioning: "Notion speed + Obsidian power" opportunity
2. Target: Teams frustrated by Notion slowness
3. Messaging: "Collaboration without the lag"
```

---

### 示例3：内容策略
**查询：`/last30days 2026年有效的LinkedIn内容策略`
**简化输出：**
```markdown
## Top Patterns

### 1. "Teach in Public" Posts Dominate (22 mentions)
Tactical, educational content outperforms thought leadership by 4-5×.

### 2. Carousels Are Fading (14 mentions)
"LinkedIn is deprioritizing carousels" — multiple reports of engagement drops.

### 3. Comment Engagement = Reach (16 mentions)
"Spend 30 min/day commenting on others' posts. Doubled my reach."

## Action Ideas

1. **Shift to educational threads**
   - Format: Problem → Solution (step-by-step) → Result
   - Evidence: Posts using this format getting 3-5× more impressions

2. **Abandon carousel strategy**
   - Data: Engagement down 40-60% since December

3. **Allocate 30 min/day to comments**
   - Tactic: Comment on posts from your ICP 10 min after posting (algorithm boost)
```

## 实际案例研究

**用户：** 一位B2B SaaS营销人员，每季度研究内容趋势

**使用该技能前：**
- 手动研究：每个主题需要2-3小时
- 访问20-30个网站，记录零散的信息
- 难以跨多个来源识别模式
- 没有系统化的方法

**使用该技能后：**
- 每个主题的研究时间：7-10分钟
- 输出格式统一（便于后续参考）
- 自动识别模式
- 提供可直接复制的提示

**三个月后的效果：**
- 创建了10份趋势报告（之前只有2-3份）
- 根据当前信息调整内容策略
- 团队在整个组织内共享研究报告（成为主要的情报来源）
- 每月节省约20小时的时间

**用户评价：** “我以前花半天时间研究趋势，现在只需7分钟。仅模式识别这一项就非常值得——手动阅读的话会错过很多信息。”

## 配置选项

### 标准模式（默认）
```
/last30days [topic]
```
- 搜索网页、Reddit和X
- 综合主要模式
- 生成提示和行动建议

### 深入分析模式
```
/last30days [topic] --deep
```
- 获取并分析前5篇完整文章
- 提供更详细的引用和数据点
- 需要12-15分钟，而非7分钟

### 仅Reddit模式
```
/last30days [topic] --reddit-only
```
- 专注于Reddit上的讨论
- 适合分析社区情绪和实践者的观点

### 快速摘要模式
```
/last30days [topic] --quick
```
- 仅显示前3个模式
- 不提供详细分析
- 输出时间：3分钟

## 专业提示

1. **使用具体主题** – 例如“AI写作工具”比“AI”这样的通用查询更有效。
2. **添加上下文** – 如“针对B2B SaaS”或“针对开发者”可以缩小搜索范围。
3. **每月运行一次** – 跟踪长期趋势，及早发现变化。
4. **与reddit-insights结合使用** – 以获得更深入的Reddit分析。
5. **导出到Notion** – 保存趋势数据库。
6. **与团队分享** – 分享情报可以提升其价值。

## 常见使用场景

| 目标 | 查询示例 | 输出价值 |
|------|---------------|--------------|
| 内容创意 | `/last30days AI生产力工具` | 当前受欢迎的内容主题 |
| 竞争研究 | `/last30days Superhuman与Spark邮箱的对比` | 用户的情绪和痛点 |
| 定位策略 | `/last30days 项目管理中的问题` | 客户使用的语言 |
| 产品验证 | `/last30days AI编码助手的痛点` | 需要解决的实际问题 |
| 营销策略 | `/last30days 2026年的冷邮件策略` | 市场上有效的方法 |

## 质量指标

一个优秀的 `/last30days` 报告应包含：
- 3-5个明确的模式（而不仅仅是随机观点）
- 来自实际用户的引用（而不仅仅是文章摘要）
- 情感分析（整体氛围如何）
- 可直接使用的提示
- 具体的行动建议
- 可信的来源链接
- 内容的时效性得到验证（无超过30天的信息）

## 限制

**该技能无法：**
- 访问付费内容（仅使用公开来源）
- 提供学术级别的研究（为了速度，而非深度）
- 替代专业领域的知识（仅整合现有信息）
- 保证信息的完整性（仅汇总热门讨论）

**最适合用于：** 快速获取方向性的情报，而非进行深入的学术研究。

## 安装方法
```bash
# Copy skill to your skills directory
cp -r last30days $HOME/.openclaw/skills/

# Verify dependencies
/last30days --check-setup

# First run
/last30days "your topic here"
```

## 帮助支持

遇到问题或找不到某些来源？请提供以下信息：
- 搜索的主题
- 预期找到的来源与实际找到的来源
- 任何错误信息
- 你的设置验证结果

---

**该技能可以将原本需要2小时的研究工作替换为7分钟的情报报告。**

**了解当前有效的方法和趋势，而不是上个季度或去年的情况。**