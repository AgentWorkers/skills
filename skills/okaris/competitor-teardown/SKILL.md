---
name: competitor-teardown
description: |
  Structured competitive analysis with feature matrices, SWOT, positioning maps, and UX review.
  Covers research frameworks, pricing comparison, review mining, and visual deliverables.
  Use for: market research, competitive intelligence, investor decks, product strategy, sales enablement.
  Triggers: competitor analysis, competitive analysis, competitor teardown, market research,
  competitive intelligence, swot analysis, competitor comparison, market landscape,
  competitor review, competitive landscape, feature comparison, market positioning
allowed-tools: Bash(infsh *)
---

# 竞品分析框架

通过 [inference.sh](https://inference.sh) 命令行工具，结合研究和截图来进行结构化的竞品分析。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Research competitor landscape
infsh app run tavily/search-assistant --input '{
  "query": "top project management tools comparison 2024 market share"
}'

# Screenshot competitor's website
infsh app run infsh/agent-browser --input '{
  "url": "https://competitor.com",
  "action": "screenshot"
}'
```

## 竞品分析框架

### 七层分析模型

| 分层 | 分析内容 | 数据来源 |
|-------|----------------|-------------|
| 1. **产品** | 功能、用户体验（UX）、质量 | 截图、免费试用版 |
| 2. **定价** | 价格方案、定价模式、隐藏费用 | 定价页面、销售电话 |
| 3. **市场定位** | 宣传信息、口号、市场定位（ICP） | 官网、广告 |
| 4. **用户增长** | 用户数量、收入、增长情况 | 网页搜索结果、新闻报道、融资信息 |
| 5. **用户评价** | 用户对产品的评价（优点和缺点） | G2、Capterra、App Store |
| 6. **内容建设** | 博客内容、社交媒体运营、SEO策略 | 官网、社交媒体账号 |
| 7. **团队背景** | 团队规模、关键成员的背景 | LinkedIn、公司官网的“关于我们”页面 |

## 研究命令

### 公司概况

```bash
# General intelligence
infsh app run tavily/search-assistant --input '{
  "query": "CompetitorX company overview funding team size 2024"
}'

# Funding and financials
infsh app run exa/search --input '{
  "query": "CompetitorX funding round series valuation investors"
}'

# Recent news
infsh app run tavily/search-assistant --input '{
  "query": "CompetitorX latest news announcements 2024"
}'
```

### 产品分析

```bash
# Feature comparison
infsh app run exa/search --input '{
  "query": "CompetitorX vs alternatives feature comparison review"
}'

# Pricing details
infsh app run tavily/extract --input '{
  "urls": ["https://competitor.com/pricing"]
}'

# User reviews
infsh app run tavily/search-assistant --input '{
  "query": "CompetitorX reviews G2 Capterra pros cons 2024"
}'
```

### 用户体验截图

```bash
# Homepage
infsh app run infsh/agent-browser --input '{
  "url": "https://competitor.com",
  "action": "screenshot"
}'

# Pricing page
infsh app run infsh/agent-browser --input '{
  "url": "https://competitor.com/pricing",
  "action": "screenshot"
}'

# Signup flow
infsh app run infsh/agent-browser --input '{
  "url": "https://competitor.com/signup",
  "action": "screenshot"
}'
```

## 功能矩阵

### 分析结构

```markdown
| Feature | Your Product | Competitor A | Competitor B | Competitor C |
|---------|:---:|:---:|:---:|:---:|
| Real-time collaboration | ✅ | ✅ | ❌ | ✅ |
| API access | ✅ | Paid only | ✅ | ❌ |
| SSO/SAML | ✅ | Enterprise | ✅ | Enterprise |
| Custom reports | ✅ | Limited | ✅ | ❌ |
| Mobile app | ✅ | iOS only | ✅ | ✅ |
| Free tier | ✅ (unlimited) | ✅ (3 users) | ❌ | ✅ (1 project) |
| Integrations | 50+ | 100+ | 30+ | 20+ |
```

### 规则说明

- ✅ = 完全支持该功能
- ⚠️ 或 “部分支持” = 功能有限或需满足特定条件
- ❌ = 该功能不可用
- 注意特殊说明：如 “仅限付费用户使用”、“企业级版本”、“测试阶段”
- 首先列出你产品所具备的优势功能
- 对竞品的优点要如实评估——诚信至关重要

## 定价比较

### 分析结构

```markdown
| | Your Product | Competitor A | Competitor B |
|---------|:---:|:---:|:---:|
| **Free tier** | Yes, 5 users | Yes, 3 users | No |
| **Starter** | $10/user/mo | $15/user/mo | $12/user/mo |
| **Pro** | $25/user/mo | $30/user/mo | $29/user/mo |
| **Enterprise** | Custom | Custom | $50/user/mo |
| **Billing** | Monthly/Annual | Annual only | Monthly/Annual |
| **Annual discount** | 20% | 15% | 25% |
| **Min seats** | 1 | 5 | 3 |
| **Hidden costs** | None | Setup fee $500 | API calls metered |
```

### 需要关注的重点

- 最低用户数量要求
- 是否仅支持年度订阅（降低灵活性）
- 不同等级之间的功能限制
- 超额使用费用
- 设置/入职费用
- 合同锁定期

## SWOT 分析

为每个竞品制作 SWOT 分析报告：

```markdown
### Competitor A — SWOT

| Strengths | Weaknesses |
|-----------|------------|
| • Strong brand recognition | • Slow feature development |
| • Large integration ecosystem | • Complex onboarding (30+ min) |
| • Enterprise sales team | • No free tier |

| Opportunities | Threats |
|--------------|---------|
| • AI features not yet shipped | • New AI-native competitors |
| • Expanding into mid-market | • Customer complaints about pricing |
| • International markets untapped | • Key engineer departures (LinkedIn) |
```

## 市场定位图

使用 2x2 矩阵展示竞品在两个关键维度上的位置。

### 选择有意义的分析维度

| 有意义的维度 | 不合适的维度 |
|-----------|----------|
| 简单 ↔ 复杂 | 好 ↔ 坏 |
| 中小企业 ↔ 企业级 | 便宜 ↔ 昂贵（过于明显） |
| 自助服务 ↔ 人工销售 | 旧产品 ↔ 新产品 |
| 专业领域 ↔ 广泛适用 | 小型企业 ↔ 大型企业 |
| 观点固定 ↔ 灵活多变 | — |

### 模板

```
                    Enterprise
                        │
           Competitor C │  Competitor A
                ●       │       ●
                        │
  Simple ──────────────────────────── Complex
                        │
            You ●       │  Competitor B
                        │       ●
                        │
                      SMB
```

### 生成可视化报告

```bash
# Create positioning map with Python
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nfig, ax = plt.subplots(figsize=(10, 10))\n\n# Competitors\ncompetitors = {\n    \"You\": (-0.3, -0.3),\n    \"Competitor A\": (0.5, 0.6),\n    \"Competitor B\": (0.6, -0.4),\n    \"Competitor C\": (-0.4, 0.5)\n}\n\nfor name, (x, y) in competitors.items():\n    color = \"#22c55e\" if name == \"You\" else \"#6366f1\"\n    size = 200 if name == \"You\" else 150\n    ax.scatter(x, y, s=size, c=color, zorder=5)\n    ax.annotate(name, (x, y), textcoords=\"offset points\", xytext=(10, 10), fontsize=12, fontweight=\"bold\")\n\nax.axhline(y=0, color=\"grey\", linewidth=0.5)\nax.axvline(x=0, color=\"grey\", linewidth=0.5)\nax.set_xlim(-1, 1)\nax.set_ylim(-1, 1)\nax.set_xlabel(\"Simple ← → Complex\", fontsize=14)\nax.set_ylabel(\"SMB ← → Enterprise\", fontsize=14)\nax.set_title(\"Competitive Positioning Map\", fontsize=16, fontweight=\"bold\")\nax.grid(True, alpha=0.3)\nplt.tight_layout()\nplt.savefig(\"positioning-map.png\", dpi=150)\nprint(\"Saved\")"
}'
```

## 用户评价收集

### 评价来源

| 平台 | 适用场景 | URL 模式 |
|----------|----------|-------------|
| G2 | B2B SaaS 产品 | g2.com/products/[产品名称]/reviews |
| Capterra | 商业软件 | capterra.com/software/[产品ID]/reviews |
| App Store | iOS 应用 | apps.apple.com |
| Google Play | Android 应用 | play.google.com |
| Product Hunt | 新产品发布 | producthunt.com/posts/[产品名称] |
| Reddit | 用户评价 | reddit.com/r/[相关子版块] |

### 需要提取的信息

| 评价类别 | 关注点 |
|----------|---------|
| **最受好评的功能** | 用户最常提到的优点是什么？ |
| **最受诟病的功能** | 用户不满的地方是什么？（这可能是你的机会） |
| **用户更换产品的原因** | 用户为何选择更换产品？是什么促使他们做出改变？ |
| **用户需求** | 用户还缺少哪些功能？ |
| **用户比较内容** | 用户在比较产品时提到了什么？ |

```bash
# Mine G2 reviews
infsh app run tavily/search-assistant --input '{
  "query": "CompetitorX G2 reviews complaints issues 2024"
}'

# Reddit sentiment
infsh app run exa/search --input '{
  "query": "reddit CompetitorX alternative frustration switching"
}'
```

## 报告输出格式

### 执行摘要（1 页）

```markdown
## Competitive Landscape Summary

**Market:** [Category] — $[X]B market growing [Y]% annually

**Key competitors:** A (leader), B (challenger), C (niche)

**Our positioning:** [Where you sit and why it matters]

**Key insight:** [One sentence about the biggest opportunity]

| Metric | You | A | B | C |
|--------|-----|---|---|---|
| Users | X | Y | Z | W |
| Pricing (starter) | $X | $Y | $Z | $W |
| Rating (G2) | X.X | Y.Y | Z.Z | W.W |
```

### 详细报告（针对每个竞品）

1. 公司概况（规模、融资情况、团队构成）
2. 产品分析（功能介绍、用户体验截图）
3. 定价详情
4. SWOT 分析
5. 用户评价分析（最受好评的功能、最受诟病的功能）
6. 竞品的市场定位与你的产品的对比
7. 市场机会分析

## 对比图表

```bash
# Stitch competitor screenshots into comparison
infsh app run infsh/stitch-images --input '{
  "images": ["your-homepage.png", "competitorA-homepage.png", "competitorB-homepage.png"],
  "direction": "horizontal"
}'
```

## 常见错误

| 错误类型 | 问题 | 解决方法 |
|---------|---------|-----|
| 仅关注产品功能 | 忽略了市场定位、定价和用户增长情况 | 使用七层分析模型 |
| 偏颇的分析 | 降低可信度 | 对竞品的优点要如实评估 |
| 数据过时 | 造成错误结论 | 所有研究数据需标注日期，并每季度更新 |
| 研究对象过多 | 分析陷入混乱 | 重点关注前三到五个主要竞争对手 |
| 分析缺乏深度 | 数据缺乏实际意义 | 每个分析部分都要说明对自身的影响 |
| 仅比较功能 | 无法全面了解竞品优势 | 需要包含定价、用户评价和市场定位信息 |

## 相关技能

```bash
npx skills add inferencesh/skills@web-search
npx skills add inferencesh/skills@prompt-engineering
```

查看所有可用应用程序：`infsh app list`