---
name: press-release-writing
description: |
  Press release writing in AP style with inverted pyramid structure.
  Covers formatting, datelines, quotes, boilerplates, and fact-checking.
  Use for: product launches, funding announcements, partnerships, company news, events.
  Triggers: press release, pr writing, media release, news release, announcement,
  product launch announcement, funding announcement, company news, media advisory,
  ap style, press statement, news wire
allowed-tools: Bash(infsh *)
---

# 新闻稿撰写

使用 [inference.sh](https://inference.sh) 命令行工具来撰写专业的新闻稿，并进行研究和事实核查。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Research for fact-checking and context
infsh app run tavily/search-assistant --input '{
  "query": "SaaS funding rounds Q1 2024 average series A size"
}'
```

## AP 样式格式

### 结构

```
HEADLINE IN TITLE CASE, PRESENT TENSE, NO PERIOD
Optional Subheadline With More Detail

CITY, STATE (Month Day, Year) — Lead paragraph with WHO, WHAT, WHEN,
WHERE, and WHY in the first 25 words.

Second paragraph expands on the lead with supporting details, context,
and significance.

"Executive quote providing perspective on the announcement," said
[Full Name], [Title] at [Company]. "Second sentence of quote adding
depth or forward-looking statement."

Body paragraphs with additional details, arranged in descending order
of importance (inverted pyramid).

"Supporting quote from partner, customer, or analyst," said
[Full Name], [Title] at [Organization].

Final paragraph with availability, pricing, or next steps.

About [Company]
[Company] is a [description]. Founded in [year], the company
[brief background]. For more information, visit [website].

Media Contact:
[Name]
[Email]
[Phone]
```

## 分章节指南

### 标题

```
❌ Company X Announces Revolutionary New Product That Will Change Everything!
❌ Press Release: Company X
❌ Company X's Amazing Product Launch

✅ Company X Launches AI-Powered Analytics Platform for Enterprise Teams
✅ Company X Raises $25 Million Series B to Expand Global Operations
✅ Company X Partners With Acme Corp to Accelerate Cloud Migration
```

**规则：**
- 使用现在时态，主动语态
- 文末不要加句号
- 避免使用最高级形容词（如“革命性的”、“开创性的”、“同类最佳的”）
- 不要使用感叹号
- 必须包含关键的新闻要素
- 标题首字母大写

### 日期

```
SAN FRANCISCO, Jan. 15, 2026 —
NEW YORK, March 3, 2026 —
LONDON, Dec. 10, 2026 —
```

**AP 月份缩写：** 一月（Jan.）、二月（Feb.）、八月（Aug.）、九月（Sept.）、十月（Oct.）、十一月（Nov.）、十二月（Dec.）（三月（March）、四月（April）、五月（May）、六月（June）、七月（July）需完整书写）

### 引言段落

用 25-35 个字回答“谁（WHO）、什么（WHAT）、何时（WHEN）、哪里（WHERE）、为什么（WHY）”这些问题：

```
❌ "We are thrilled to announce that after months of hard work, our talented
    team has created something truly special that we think you'll love."

✅ "Company X, a developer tools startup, today launched DataFlow, an
    AI-powered analytics platform that automates reporting for enterprise
    engineering teams."
```

### 引用

**规则：**
- 最多使用 1-2 条引用（CEO/创始人 + 合作伙伴/客户）
- 引用不要以“I”开头
- 引用格式：「引用语，姓名，公司职位」
- 引用应提供新的视角，而不是重复正文中的事实
- 前瞻性的引用效果更好：「我们相信这将会……」

```
❌ "I am so excited about this launch," said John Smith.
❌ "We launched a new product today," said the CEO.

✅ "Enterprise teams spend an average of 15 hours per week on manual
    reporting," said Sarah Chen, CEO of Company X. "DataFlow eliminates
    that burden entirely, letting engineers focus on building."

✅ "Since adopting DataFlow, our reporting cycle dropped from three days
    to three minutes," said Marcus Lee, VP of Engineering at Acme Corp.
```

### 常见信息（关于公司/项目）

```
About Company X
Company X is a [category] company that [what it does] for [who].
Founded in [year] and headquartered in [city], the company serves
[number] customers across [industries/geographies]. For more
information, visit www.companyx.com.
```

保持 3-4 句的篇幅。所有新闻稿中应保持一致。

### 媒体联系信息

```
Media Contact:
Jane Doe
PR Manager, Company X
jane@companyx.com
(555) 123-4567
```

## 倒金字塔结构

最重要的信息放在最前面。每个段落的重要性依次递减。编辑通常会从底部开始阅读。

```
┌─────────────────────────┐
│    MOST IMPORTANT       │  Lead: core announcement
│    (Who, What, When,    │
│     Where, Why)         │
├─────────────────────────┤
│  IMPORTANT DETAILS      │  Supporting facts, context
│  (How, stats, quotes)   │
├─────────────────────────┤
│  BACKGROUND             │  Industry context, history
│  (Context, trends)      │
├─────────────────────────┤
│  ADDITIONAL INFO        │  Availability, pricing
│  (Nice to have)         │
├─────────────────────────┤
│  BOILERPLATE            │  About section, contact
└─────────────────────────┘
```

## 研究与事实核查

### 验证声明

```bash
# Check market size claims
infsh app run tavily/search-assistant --input '{
  "query": "enterprise analytics market size 2024 2025 forecast"
}'

# Verify competitor claims
infsh app run exa/search --input '{
  "query": "Company X competitors enterprise analytics market share"
}'

# Get industry statistics
infsh app run exa/answer --input '{
  "question": "How much time do engineering teams spend on reporting weekly?"
}'
```

### 添加背景信息

```bash
# Industry trends for the "why now" angle
infsh app run tavily/search-assistant --input '{
  "query": "AI automation enterprise reporting trends 2024"
}'
```

## 新闻稿类型

### 产品发布

**重点：** 产品功能、目标受众、重要性、上市时间
**引用语：** CEO 或产品负责人关于产品愿景的讲话

### 融资公告

**重点：** 融资金额、轮次、主要投资者、资金用途
**引用语：** CEO 关于公司增长计划的讲话 + 主要投资者关于投资理由的讲话

### 合作伙伴关系

**重点：** 合作关系带来的好处、对客户的影响
**引用语：** 两家公司的代表言论

### 里程碑/成就

**重点：** 成就指标、增长趋势、意义
**引用语：** CEO 关于公司的发展历程及下一步计划的讲话

### 高管任命

**重点：** 新任命的高管、背景信息、负责领域
**引用语：** CEO 关于此次任命的原因 + 新高管加入公司的理由

## 长度指南

| 元素 | 长度 |
|---------|--------|
| 标题 | 10-15 个字 |
| 子标题（可选） | 15-25 个字 |
| 正文 | 400-600 个字 |
| 引用 | 每条引用 2-3 句，最多 2 条 |
| 常见信息 | 3-4 句 |
| **总计** | **500-800 个字** |

如果超过 800 个字，编辑可能不会阅读；如果少于 400 个字，内容可能不够充实。

## AP 样式快速参考

| 规则 | 例子 |
|------|---------|
| 数字 1-9 用文字书写，10 及以上用数字表示 | “九名员工” / “10 名员工” |
| 百分比用一个单词表示 | “15%”（正文不要写成 “15%”） |
| 名字前的头衔首字母大写 | “CEO Sarah Chen” |
| 名字后的头衔首字母小写 | “Sarah Chen，首席执行官” |
| 公司名称：正文中不加 “Inc.”/“Corp.” | “Company X” 而不是 “Company X, Inc.” |
| 日期：月日年 | “2026 年 1 月 15 日” |
| 地点缩写：AP 标准格式 | “加利福尼亚州旧金山（SAN FRANCISCO, Calif.）” |
| 逗号使用：AP 标准格式不使用逗号 | “快速、简洁、有效（fast, simple and effective）” |

## 常见错误

| 错误 | 问题 | 修正方法 |
|---------|---------|-----|
| 使用最高级形容词 | 编辑可能会忽略 | 仅陈述事实，让读者自行判断 |
| 使用感叹号 | 不专业 | 新闻稿中禁止使用感叹号 |
| 引用以 “I” 开头 | 语气不够正式 | 以事实或见解开头 |
| 关键信息放在最后一段 | 最重要的信息应放在最前面 |
| 文字过长 | 编辑可能不会阅读 | 最长 500-800 个字 |
| 使用专业术语 | 会让非专业人士难以理解 | 用通俗的语言写作 |
| 不进行事实核查 | 会影响可信度 | 所有声明和数据都必须经过核实 |
| 缺少媒体联系信息 | 记者无法跟进 | 必须提供媒体联系信息 |

## 检查清单

- [ ] 标题：使用现在时态，主动语态，文末不要加句号，避免使用最高级形容词
- [ ] 日期：遵循 AP 标准格式（城市、州、日期）
- [ ] 引言段落：前 25 个字内包含“谁、什么、何时、哪里、为什么”
- [ ] 倒金字塔结构：最重要的信息放在最前面 |
- [ ] 引用：注明出处，不要以 “I” 开头，提供新的视角 |
- [ ] 所有声明和数据都经过核实 |
- [ ] 常见信息：与其他新闻稿保持一致 |
- [ ] 媒体联系信息：包括姓名、电子邮件、电话 |
- [ ] 总字数：500-800 个字 |
- [ ] 朗读检查语句流畅度 |

## 相关技能

```bash
npx skills add inferencesh/skills@web-search
npx skills add inferencesh/skills@prompt-engineering
```

浏览所有应用程序：`infsh app list`