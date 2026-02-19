---
name: press-release-writing
description: "**AP风格的新闻稿撰写指南（采用倒金字塔结构）**  
本指南涵盖了新闻稿的格式要求、日期标注、引语使用、常用模板以及事实核查等内容，适用于产品发布、融资公告、合作伙伴关系、公司新闻等场景的撰写。  
**适用场景：**  
产品发布、融资公告、合作伙伴关系、公司新闻、活动报道等。  
**相关术语：**  
新闻稿（Press Release）、媒体稿（Media Release）、新闻专线（News Wire）、新闻声明（News Statement）  
**关键要点：**  
1. **格式要求：**  
   - 使用标准的AP风格（Associated Press style）进行撰写。  
   - 采用倒金字塔结构（Inverted Pyramid Structure），即先介绍最重要的信息，再逐步展开细节。  
   - 保持文本简洁明了，避免冗长。  
2. **日期标注：**  
   - 明确标注新闻稿的发布日期。  
3. **引语使用：**  
   - 引用相关人士的观点或数据时，确保引语准确无误。  
4. **常用模板：**  
   - 包含新闻稿的基本结构元素，如标题、导语、正文、结尾等。  
5. **事实核查：**  
   - 在发布新闻稿前，务必核实所有信息的准确性。  
**示例：**  
（具体示例内容可根据实际需求进行填充。）  
**注意事项：**  
- 请根据实际情况调整内容结构和语言风格。  
- 保持代码示例、命令和URL的原始格式不变。  
（注：由于SKILL.md文件中未包含具体的代码示例、命令或URL，因此此处省略了相关内容的翻译。）"
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

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需提升权限或启动后台进程。也可以选择 [手动安装与验证](https://dist.inference.sh/cli/checksums.txt)。

## AP 格式规范

### 文章结构

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

## 各部分撰写指南

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
- 标题末尾不加句点
- 避免使用最高级形容词（如“革命性的”、“开创性的”、“一流的”）
- 不使用感叹号
- 必须包含关键的新闻要素
- 标题首字母大写

### 日期

```
SAN FRANCISCO, Jan. 15, 2026 —
NEW YORK, March 3, 2026 —
LONDON, Dec. 10, 2026 —
```

**AP 月份缩写：** 一月（Jan.）、二月（Feb.）、八月（Aug.）、九月（Sept.）、十月（Oct.）、十一月（Nov.）、十二月（Dec.）（三月（March）、四月（April）、五月（May）、六月（June）、七月（July）需完整书写）

### 导语段落

用 25-35 个词回答“谁（WHO）、什么（WHAT）、何时（WHEN）、哪里（WHERE）、为什么（WHY）”这些问题：

```
❌ "We are thrilled to announce that after months of hard work, our talented
    team has created something truly special that we think you'll love."

✅ "Company X, a developer tools startup, today launched DataFlow, an
    AI-powered analytics platform that automates reporting for enterprise
    engineering teams."
```

### 引用

**规则：**
- 最多引用 1-2 段话（CEO/创始人 + 合作伙伴/客户）
- 引用开头不要使用“I”
- 引用格式：**“引用内容”，** “姓名”，** “公司职位”。
- 引用应提供额外的见解，而非重复正文中的事实
- 前瞻性的引用效果更好：**“我们相信这将会……”

```
❌ "I am so excited about this launch," said John Smith.
❌ "We launched a new product today," said the CEO.

✅ "Enterprise teams spend an average of 15 hours per week on manual
    reporting," said Sarah Chen, CEO of Company X. "DataFlow eliminates
    that burden entirely, letting engineers focus on building."

✅ "Since adopting DataFlow, our reporting cycle dropped from three days
    to three minutes," said Marcus Lee, VP of Engineering at Acme Corp.
```

### 常用模板（关于部分）

```
About Company X
Company X is a [category] company that [what it does] for [who].
Founded in [year] and headquartered in [city], the company serves
[number] customers across [industries/geographies]. For more
information, visit www.companyx.com.
```

内容控制在 3-4 句之间。所有新闻稿应保持一致。

### 媒体联系信息

```
Media Contact:
Jane Doe
PR Manager, Company X
jane@companyx.com
(555) 123-4567
```

## 倒金字塔结构

最重要的信息放在最前面。每个段落的重要性依次递减。编辑通常会从文章底部开始阅读。

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

**重点内容：** 产品功能、目标受众、重要性、上市时间
**引用内容：** CEO 或产品负责人关于产品愿景的讲话

### 资金募集公告

**重点内容：** 融资金额、投资轮次、主要投资者、资金用途
**引用内容：** CEO 关于公司发展计划的讲话 + 主要投资者关于投资理由的陈述

### 合作伙伴关系

**重点内容：** 合作关系带来的好处、对客户的价值
**引用内容：** 各公司代表的语录

### 里程碑/成就

**重点内容：** 成就指标、增长趋势、意义
**引用内容：** CEO 关于公司发展历程及下一步计划的讲话

### 高管任命

**重点内容：** 新任命的高管信息、背景、职责
**引用内容：** CEO 关于此次任命的原因 + 新任高管加入公司的理由

## 文章长度指南

| 元素 | 长度 |
|---------|--------|
| 标题 | 10-15 个词 |
| 子标题（可选） | 15-25 个词 |
| 正文 | 400-600 个词 |
| 引用 | 每段 2-3 句，最多 2 段引用 |
| 常用模板 | 3-4 句 |
| **总字数** | **500-800 个词** |

如果超过 800 个词，编辑可能不会阅读；少于 400 个词则缺乏实质性内容。

## AP 格式快速参考

| 规则 | 例子 |
|------|---------|
| 数字从 1 到 9 用文字书写，10 及以上用数字表示 | “九名员工” / “10 名员工” |
| 百分比用一个单词表示 | “15%”（正文不要写成“15%”） |
| 名字前的头衔首字母大写 | “CEO Sarah Chen” |
| 名字后的头衔首字母小写 | “Sarah Chen，首席执行官” |
| 公司名称：正文中不加“Inc.”/“Corp.” | “Company X”而非“Company X, Inc.” |
| 日期：月日年 | “2026年1月15日” |
| 地点缩写：AP 标准格式 | “加利福尼亚州旧金山（SAN FRANCISCO, Calif.）” |
| 逗号的使用：AP 标准格式不使用逗号 | “快速、简洁、有效（fast, simple and effective）”

## 常见错误

| 错误 | 问题 | 修正方法 |
|---------|---------|-----|
| 使用最高级形容词 | 编辑可能会忽略这类表述 | 仅陈述事实，让读者自行判断 |
| 使用感叹号 | 不专业 | 新闻稿中禁止使用感叹号 |
| 引用开头使用“I” | 语气不够正式 | 引用应从事实或见解开始 |
| 关键信息放在段落中间 | 最重要的信息应放在开头 |
| 文章过长 | 编辑可能不会阅读 | 最长 500-800 个词 |
| 使用专业术语 | 会让非专业人士难以理解 | 用通俗语言写作 |
| 不进行事实核查 | 会影响可信度 | 所有声明和数据都必须经过核实 |
| 缺少媒体联系信息 | 记者无法跟进 | 必须提供媒体联系信息 |

## 检查清单

- 标题：使用现在时态、主动语态，标题末尾不加句点，避免使用最高级形容词
- 日期：遵循 AP 格式（城市、州、日期）
- 导语：前 25 个词中包含“谁、什么、何时、哪里、为什么”
- 倒金字塔结构：最重要的信息放在最前面
- 引用：注明出处，引用开头不要使用“I”，并提供额外见解
- 所有声明和数据均经过核实
- 常用模板：与其他新闻稿保持一致
- 媒体联系信息：包括姓名、电子邮件和电话号码
- 总字数：500-800 个词
- 朗读文章以确保语言流畅

## 相关技能

```bash
npx skills add inference-sh/skills@web-search
npx skills add inference-sh/skills@prompt-engineering
```

查看所有可用工具：`infsh app list`