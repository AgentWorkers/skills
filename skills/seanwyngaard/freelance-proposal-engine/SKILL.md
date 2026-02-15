---
name: freelance-proposal-engine
description: 为 Upwork、Fiverr、Freelancer 和 PeoplePerHour 等平台上的工作列表生成定制的 freelance 提案。在撰写提案、竞标项目或回复客户的工作发布时使用这些提案。
argument-hint: "[job-description-or-url]"
allowed-tools: Read, Write, Grep, Glob, Bash, WebFetch, WebSearch
---

# 自由职业提案生成工具

该工具能够根据具体的职位招聘信息生成具有高转化率的自由职业提案。它能够分析客户需求、识别潜在问题，并制定出能够赢得项目的提案。

## 使用方法

请通过以下方式提供职位招聘信息：
- 将完整的职位描述粘贴为 `$ARGUMENTS`
- 提供招聘信息的网址（例如 Upwork、Fiverr、Freelancer 等）
- 提供包含职位描述的文件路径

## 提案生成流程

请严格按照以下步骤操作：

### 第一步：分析职位招聘信息

提取并识别以下内容：
- **客户的痛点**：他们试图解决什么问题？
- **明确的要求**：提到的技能、交付成果和时间表
- **隐含的要求**：他们实际需要但未明确表达的内容（需要从描述中推断出来）
- **预算情况**：是固定价格还是按小时计费？如果有预算范围，请一并说明
- **风险提示**：不切实际的期望、项目范围可能扩大、预算过低
- **客户的经验水平**：是首次发布招聘信息还是经验丰富的买家（可以通过查看评论数量或招聘频率来判断）
- **关键词**：客户使用的专业术语和流行词汇（在提案中也要体现这些关键词）

### 第二步：确定提案策略

根据分析结果，选择合适的策略：

| 客户类型 | 策略 |
|-------------|----------|
| 首次购买者 | 安抚客户、解释工作流程、提供分阶段付款方案 |
| 经验丰富的买家 | 简明扼要地介绍方案、列举过往类似项目的成果 |
| 技术型客户 | 使用专业的技术术语，避免冗余内容 |
| 非技术型客户 | 将技术细节转化为可理解的业务成果 |
| 紧急项目 | 强调自己的可用性和快速响应能力 |
| 注重预算的客户 | 强调提案的价值，建议采用 MVP（最小可行产品）或分阶段交付的方式 |

### 第三步：生成提案

使用以下结构来编写提案：

```
**Opening Hook** (1-2 sentences)
- Reference a SPECIFIC detail from their listing (proves you read it)
- Connect it to a result you've delivered before
- Never start with "I" or "My name is" or "I'm a"

**Understanding Their Problem** (2-3 sentences)
- Restate their problem in your own words
- Show you understand the WHY behind the request
- Mention one thing they might not have considered

**Your Approach** (3-5 bullet points)
- Specific steps you'll take
- Tools/technologies you'll use
- Timeline for each step
- What they'll receive at each milestone

**Relevant Experience** (2-3 sentences)
- 1-2 specific similar projects (brief, results-focused)
- Quantified outcomes where possible ("increased conversions by 40%")
- If no exact match, draw parallels from adjacent experience

**Call to Action** (1-2 sentences)
- Suggest a specific next step (quick call, share examples, start immediately)
- Create mild urgency without being pushy
- Keep it conversational
```

### 第四步：定价建议

根据对项目的分析，提出以下建议：
- **您推荐的收费标准**（基于市场数据和项目复杂度）
- **收费理由**（用一句话说明）
- **替代定价方案**：如果预算较低，建议采用分阶段交付或调整项目范围

以下是参考的市场收费标准：
| 服务类型 | 初级 | 中级 | 专家 |
|---------|----------|-----------|--------|
| 网页开发 | $25-40/小时 | $50-100/小时 | $100-200/小时 |
| 内容写作 | $0.05-0.10/字 | $0.10-0.25/字 | $0.25-1.00/字 |
| SEO | $30-50/小时 | $75-150/小时 | $150-300/小时 |
| 网页抓取 | $20-40/小时 | $50-100/小时 | $100-200/小时 |
| 设计 | $25-50/小时 | $50-100/小时 | $100-250/小时 |
| 数据分析 | $30-50/小时 | $60-120/小时 | $120-250/小时 |
| 电子邮件营销 | $25-40/小时 | $50-100/小时 | $100-200/小时 |
| 社交媒体营销 | $20-35/小时 | $40-80/小时 | $80-150/小时 |

### 第五步：输出提案

生成一份格式清晰、可直接复制的提案。同时提供以下内容：
- **针对不同平台的建议**（例如：Upwork 上的提案应控制在 300 字以内；Fiverr 上的提案应重点介绍交付成果）
- **需要向客户提出的问题**（2-3 个能够体现专业性的问题）
- **跟进信息模板**（如果 48 小时内没有收到回复，可以使用此模板发送消息）

## 提案质量规则

1. **切勿使用通用模板**。每句话都必须引用职位招聘信息中的具体内容。
2. **切勿过度推销**。要表现出自信，但不要傲慢。
3. **切勿夸大自己的经验**。如果缺乏相关经验，可以说明“虽然我没有直接做过某项具体任务，但我具备类似的技能”。
4. **保持提案的易读性**。客户通常会查看 20-50 份提案，请使用简短的段落和项目符号。
5. **字数要求**：简单项目 150-300 字；复杂项目 300-500 字，切勿超过这个范围。
6. **避免使用固定模板语句**：例如 “我写这封邮件是为了表达我的兴趣”、“我有信心……”、“期待您的回复”、“尊敬的先生/女士”、“我拥有 X 年的经验” 等。

## 示例

**职位招聘信息**：“需要有人从 5 个电子商务网站抓取产品数据，包括产品名称、价格、描述和图片，并生成 CSV 文件。每个网站大约有 500 个产品。”

**生成的提案**：

> 我可以为您从 5 个电子商务网站抓取 2,500 个产品的数据，并生成清晰的 CSV 文件。我之前已经多次完成过类似的项目。
>
> 我的计划如下：
>
> - **第一天**：使用 Python 和 Playwright 为所有 5 个网站编写抓取脚本（该工具能够处理那些简单工具无法处理的 JavaScript 渲染页面）
> - **第二天**：运行抓取程序，清理并统一数据格式（确保所有来源的数据格式一致）
> - **第三天**：交付包含产品名称、价格、描述和图片链接的 CSV 文件
>
> 为避免您遇到麻烦，我会自动处理分页问题，为无法正常加载的页面设置重试机制，并删除重复的产品。
>
> 上个月，我为一家零售客户从 3 个竞争对手网站抓取了 15,000 多个产品数据，仅用 48 小时就完成了任务，准确率达到 99.7%。
>
> 请问：
> - 这些网站是否需要登录才能访问？该项目是一次性完成还是需要定期更新？
>
> 如果细节符合要求，我今天就可以开始工作。