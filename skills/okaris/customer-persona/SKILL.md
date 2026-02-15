---
name: customer-persona
description: |
  Research-backed customer persona creation with market data and avatar generation.
  Covers demographics, psychographics, jobs-to-be-done, journey mapping, and anti-personas.
  Use for: marketing strategy, product development, UX research, sales enablement, content strategy.
  Triggers: customer persona, buyer persona, user persona, target audience, ideal customer,
  customer profile, audience research, user research, icp, ideal customer profile,
  target market, customer avatar, audience persona
allowed-tools: Bash(infsh *)
---

# 客户画像

通过 [inference.sh](https://inference.sh) 命令行工具，利用调研数据和可视化工具来创建基于数据的客户画像。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Research your target market
infsh app run tavily/search-assistant --input '{
  "query": "SaaS product manager demographics pain points 2024 survey"
}'

# Generate a persona avatar
infsh app run falai/flux-dev-lora --input '{
  "prompt": "professional headshot photograph of a 35-year-old woman, product manager, friendly confident expression, modern office background, natural lighting, business casual attire, realistic portrait",
  "width": 1024,
  "height": 1024
}'
```

## 画像模板

```
┌──────────────────────────────────────────────────────┐
│  [Avatar Photo]                                      │
│                                                      │
│  SARAH CHEN, 34                                      │
│  Product Manager at a Series B SaaS startup          │
│                                                      │
│  "I spend more time making reports than making       │
│   decisions."                                        │
│                                                      │
├──────────────────────────────────────────────────────┤
│  DEMOGRAPHICS          │  PSYCHOGRAPHICS             │
│  Age: 30-38            │  Values: efficiency, data   │
│  Income: $120-160K     │  Personality: analytical,   │
│  Education: BS/MBA     │    organized, collaborative │
│  Location: Urban US    │  Interests: productivity,   │
│  Role: Product/PM      │    leadership, AI tools     │
├──────────────────────────────────────────────────────┤
│  GOALS                 │  PAIN POINTS                │
│  • Ship features       │  • Too many meetings        │
│  faster                │  • Manual reporting (15     │
│  • Data-driven         │    hrs/week)                │
│  decisions             │  • Stakeholder alignment    │
│  • Team alignment      │    is slow                  │
│  • Career growth to    │  • Tool sprawl (8+ apps)   │
│    Director            │  • No single source of      │
│                        │    truth                    │
├──────────────────────────────────────────────────────┤
│  CHANNELS              │  BUYING TRIGGERS            │
│  • LinkedIn (daily)    │  • Peer recommendation      │
│  • Product Hunt        │  • Free trial experience    │
│  • Podcasts (commute)  │  • Integration with Jira    │
│  • Lenny's Newsletter  │  • Team plan pricing        │
│  • Twitter/X           │  • ROI calculator           │
└──────────────────────────────────────────────────────┘
```

## 逐步构建客户画像

### 第一步：调研

从数据出发，而非假设。

```bash
# Market demographics
infsh app run tavily/search-assistant --input '{
  "query": "product manager salary demographics 2024 survey report"
}'

# Pain points and challenges
infsh app run exa/search --input '{
  "query": "biggest challenges facing product managers SaaS companies"
}'

# Tool usage patterns
infsh app run tavily/search-assistant --input '{
  "query": "most popular tools product managers use 2024 survey"
}'

# Content consumption habits
infsh app run exa/answer --input '{
  "question": "Where do product managers get their industry news and professional development?"
}'
```

### 第二步：人口统计信息

**使用范围值，而非具体数值。** 客户画像代表的是一个群体，而非单个个体。

| 字段 | 格式 | 例 |
|-------|--------|---------|
| 年龄范围 | X-Y | 30-38岁 |
| 收入范围 | $X-$Y | 120,000-$160,000美元 |
| 教育背景 | 常见学位 | 计算机科学学士、MBA |
| 地点 | 地区/类型 | 美国城市地区、主要科技枢纽 |
| 职位 | 职务级别 | 高级产品经理、产品负责人 |
| 公司规模 | 规模范围 | 50-500名员工 |
| 行业 | 行业领域 | B2B SaaS |

### 第三步：心理特征

他们的想法、价值观和信念。

| 类别 | 需要回答的问题 |
|----------|-------------------|
| **价值观** | 对他们来说，什么在职业上最重要？ |
| **态度** | 他们对行业的发展方向有何看法？ |
| **动机** | 是什么驱使他们工作？ |
| **性格特点** | 分析型还是直觉型？领导型还是合作型？ |
| **兴趣** | 他们在工作中喜欢阅读/观看/收听什么？ |
| **生活方式** | 对工作与生活的平衡有何偏好？远程办公/混合办公/办公室办公？ |

### 第四步：目标

他们试图实现的目标（包括职业和个人目标）。

```
Professional:
- Ship features faster with fewer meetings
- Make data-driven decisions (not gut feelings)
- Get promoted to Director of Product within 2 years
- Build a more autonomous product team

Personal:
- Leave work by 6pm more often
- Be seen as a strategic leader, not a ticket manager
- Stay current with industry trends without information overload
```

### 第五步：痛点

**尽可能量化这些痛点。** 模糊的痛点意味着画像也不清晰。

```
❌ "Has trouble with reporting"
✅ "Spends 15 hours per week creating manual reports for 4 different stakeholders"

❌ "Too many tools"
✅ "Uses 8 different tools daily (Jira, Slack, Notion, Figma, Analytics, Sheets, Docs, Email) with no unified view"

❌ "Meetings are a problem"
✅ "Averages 6 hours of meetings per day, leaving only 2 hours for deep work"
```

### 第六步：待完成的任务（JTBD）

三种类型的任务：

| 任务类型 | 描述 | 例 |
|----------|-------------|---------|
| **功能性任务** | 他们需要完成的具体任务 | “根据客户影响数据来优先处理产品待办事项” |
| **情感性任务** | 他们希望获得的感受 | “在高管团队面前能够自信地展示” |
| **社交性任务** | 他们希望别人如何看待自己 | “被看作是一个基于数据做出决策的人” |

### 第七步：购买流程

| 阶段 | 行为表现 |
|-------|----------|
| **认知阶段** | 阅读博客文章，在LinkedIn上查看同行推荐 |
| **考虑阶段** | 比较3-4个工具，阅读G2/Capterra的评论，在Slack社区中提问 |
| **决策阶段** | 请求产品演示，需要IT部门或安全部门的批准，评估团队定价 |
| **影响决策的因素** | 工程负责人、产品副总裁、首席财务官（涉及预算） |
| **可能遇到的异议** | “我的团队真的会采用这个产品吗？”、“它能与Jira集成吗？” |
| **触发因素** | 新季度有紧迫的目标，新的副总裁要求改进报告方式 |

### 第八步：生成头像

**头像制作建议：**
- 头像应符合年龄范围、种族特征以及职业背景 |
- 使用“专业头像照片”以获得更真实的效果 |
- 表情要友好、亲切（避免使用僵硬的库存照片） |
- 背景应能反映他们的工作环境 |
- 服装应符合商务休闲或行业规范

## “反画像”

同样重要的是：明确哪些人不是你的目标客户。

```
ANTI-PERSONA: "Enterprise Earl"
- CTO at a 5,000+ person enterprise
- Needs SOC 2, HIPAA, on-premise deployment
- 18-month procurement cycles
- Wants white-glove onboarding and dedicated CSM
- WHY NOT: Our product is self-serve SaaS for SMB/mid-market.
  Enterprise needs would require 2+ years of product investment.
```

“反画像”有助于避免在无法服务的客户身上浪费精力。

## 多个客户画像

大多数产品需要2-4个客户画像。超过4个则难以有效服务所有客户。

| 优先级 | 客户画像 | 角色 |
|----------|---------|------|
| **主要画像** | 主要用户和购买决策者 | 你需要优化服务的对象 |
| **次要画像** | 对购买决策有影响力的人 | 你需要说服的对象 |
| **次要画像** | 偶尔使用该产品的人 | 你需要提供支持的对象，但不是主要目标 |

## 验证

基于假设创建的客户画像可能是不准确的。可以通过以下方法进行验证：

| 方法 | 可以了解的信息 |
|--------|---------------|
| 客户访谈（5-10次） | 客户的真实语言和实际痛点 |
| 支持工单分析 | 真实存在的问题，而非假设的问题 |
| 分析数据 | 客户的实际行为，而非报告中的行为 |
| 调查（50份以上回复） | 不同客户群体的量化数据 |
| 销售通话录音 | 客户的异议、购买决策的触发因素以及他们使用的语言 |

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 基于假设 | 画像缺乏真实性 | 从数据出发进行调研 |
| 客户画像太多（6个以上） | 难以全面服务所有客户 | 保持3-4个画像 |
| 痛点描述模糊 | 无法采取行动 | 尽量将所有痛点量化 |
| 仅关注人口统计信息 | 忽略了客户的动机和行为 | 添加心理特征和待完成的任务 |
| 从不更新画像 | 画像会过时 | 每季度更新一次 |
| 没有“反画像” | 在错误的客户身上浪费精力 | 明确哪些人不是你的目标客户 |
| 对所有用户使用相同的画像 | 不同用户有不同的需求 | 分别创建主要画像、次要画像和次要画像 |

## 相关技能

```bash
npx skills add inferencesh/skills@web-search
npx skills add inferencesh/skills@ai-image-generation
npx skills add inferencesh/skills@prompt-engineering
```

查看所有应用程序：`infsh app list`