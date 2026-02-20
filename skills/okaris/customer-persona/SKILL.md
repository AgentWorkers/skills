---
name: customer-persona
description: "基于研究的客户画像创建方法，结合市场数据和头像生成技术。该方法涵盖客户的人口统计特征、心理特征、需求分析、用户旅程映射以及“反画像”（即与理想客户特征相反的典型用户画像）的构建。适用于市场营销策略、产品开发、用户体验研究、销售支持以及内容策略的制定。相关概念包括：客户画像（Customer Persona）、买家画像（Buyer Persona）、用户画像（User Persona）、目标受众（Target Audience）、理想客户（Ideal Customer）、客户资料（Customer Profile）、受众研究（Audience Research）、用户研究（User Research）等。"
allowed-tools: Bash(infsh *)
---
# 客户画像

通过 [inference.sh](https://inference.sh) 命令行工具，利用调研数据和可视化信息来创建基于数据的客户画像。

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

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需提升权限或启动后台进程。如需手动安装和验证，请参考 [此处](https://dist.inference.sh/cli/checksums.txt)。

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

### 第一步：数据收集

从数据入手，而非基于假设。

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

| 字段 | 格式 | 例子 |
|-------|--------|---------|
| 年龄范围 | X-Y | 30-38 岁 |
| 收入范围 | $X-$Y | 120,000-$160,000 美元 |
| 教育背景 | 常见学位 | 计算机科学学士、MBA |
| 所在地 | 地区/类型 | 美国城市地区、主要科技枢纽 |
| 职位 | 职责级别 | 高级产品经理、产品负责人 |
| 公司规模 | 规模范围 | 50-500 名员工 |
| 行业 | 行业领域 | B2B SaaS |

### 第三步：心理特征

了解他们的想法、价值观和信念。

| 类别 | 需要回答的问题 |
|----------|-------------------|
| **价值观** | 对他们来说，什么在职业上最重要？ |
| **态度** | 他们对行业的发展方向有何看法？ |
| **动机** | 是什么驱使他们工作？ |
| **性格特点** | 更倾向于分析型还是直觉型？是领导者还是合作者？ |
| **兴趣** | 他们在工作中喜欢阅读/观看/收听什么？ |
| **生活方式** | 重视工作与生活的平衡吗？喜欢远程办公、混合办公还是传统办公室？ |

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

**尽可能量化问题。** 模糊的痛点意味着画像不够准确。

```
❌ "Has trouble with reporting"
✅ "Spends 15 hours per week creating manual reports for 4 different stakeholders"

❌ "Too many tools"
✅ "Uses 8 different tools daily (Jira, Slack, Notion, Figma, Analytics, Sheets, Docs, Email) with no unified view"

❌ "Meetings are a problem"
✅ "Averages 6 hours of meetings per day, leaving only 2 hours for deep work"
```

### 第六步：待完成的任务（JTBD）

分为三种类型：

| 任务类型 | 描述 | 例子 |
|----------|-------------|---------|
| **功能性任务** | 需要完成的具体任务 | “根据客户影响数据对产品待办事项进行优先级排序” |
| **情感需求** | 他们希望获得的感觉 | “在高管团队面前展示时能够充满信心” |
| **社交需求** | 他们希望别人如何看待自己 | “希望被看作是一个基于数据做出决策的人” |

### 第七步：购买流程

| 阶段 | 客户行为 |
|-------|----------|
| **认知阶段** | 阅读博客文章，在 LinkedIn 上查看同行推荐 |
| **考虑阶段** | 比较 3-4 种工具，阅读 G2/Capterra 的评价，在 Slack 社区中咨询 |
| **决策阶段** | 请求产品演示，需要 IT 部门或安全部门的批准，评估团队定价 |
| **影响决策的因素** | 工程团队负责人、产品副总裁、首席财务官（涉及预算） |
| **可能遇到的反对意见** | “我的团队真的会采用这个产品吗？”、“它能与 Jira 集成吗？” |
| **触发因素** | 新季度目标设定、新上任的副总裁要求改进报告方式 |

### 第八步：生成头像

```bash
# Match demographics: age, gender, ethnicity, professional context
infsh app run falai/flux-dev-lora --input '{
  "prompt": "professional headshot photograph of a 34-year-old Asian American woman, product manager, warm confident smile, modern tech office background, natural lighting, wearing smart casual blouse, realistic portrait photography, sharp focus",
  "width": 1024,
  "height": 1024
}'
```

**头像制作建议：**
- 头像应符合年龄范围、种族特征以及职业背景 |
- 使用“专业的头像照片”以获得更真实的视觉效果 |
- 表情要友好、易于接近（避免使用千篇一律的库存照片） |
- 背景应能反映他们的工作环境 |
- 服装应符合商务休闲或行业规范

## “反画像”（Anti-Persona）

同样重要的是：明确哪些客户不是你的目标客户。

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

大多数产品需要 2-4 个客户画像。超过 4 个则难以有效服务所有客户。

| 优先级 | 客户画像 | 角色 |
|----------|---------|------|
| **主要客户** | 主要用户和购买决策者 | 你需要优化服务的对象 |
| **次要客户** | 对购买决策有影响力的人 | 需要说服的对象 |
| **边缘客户** | 偶尔使用该产品的人 | 需要提供支持的对象（但非主要目标群体） |

## 验证客户画像的准确性

基于假设创建的画像可能是不准确的。可以通过以下方法进行验证：

| 方法 | 可以了解的信息 |
|--------|---------------|
| 客户访谈（5-10 次） | 客户的真实言论和实际痛点 |
| 支持工单分析 | 真实遇到的问题（而非假设的问题） |
| 分析数据 | 客户的实际行为（而非报告中的行为） |
| 调查（50 条以上反馈） | 不同客户群体的量化趋势 |
| 销售通话录音 | 客户的反对意见和购买决策的触发因素 |

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 基于假设 | 画像缺乏依据 | 从数据入手进行调研 |
| 客户画像过多（6 个以上） | 难以全面服务所有客户 | 保留 3-4 个主要画像 |
| 痛点描述模糊 | 无法制定有效的策略 | 尽量将所有问题量化 |
| 仅关注人口统计信息 | 忽略了客户的心理特征和实际需求 | 添加心理特征和待完成的任务信息 |
| 从不更新画像 | 画像会过时 | 每季度更新一次 |
| 未创建“反画像” | 在错误的客户身上浪费精力 | 明确哪些客户不是目标受众 |
| 所有用户使用相同的画像 | 不同用户有不同的需求 | 分别为不同类型的用户创建相应的画像 |

## 相关技能

```bash
npx skills add inference-sh/skills@web-search
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@prompt-engineering
```

查看所有可用工具：`infsh app list`