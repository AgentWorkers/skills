---
name: competitor-teardown
description: "结构化的竞争分析方法，包括功能矩阵、SWOT分析、市场定位图以及用户体验评估。该方法涵盖研究框架、价格比较、数据挖掘以及可视化报告的生成。适用于市场研究、竞争情报分析、投资者演示文稿、产品策略制定以及销售支持等场景。相关触发条件包括：竞争对手分析、SWOT分析、竞争对手对比、市场调研、竞争情报收集、产品特性对比以及市场定位评估等。"
allowed-tools: Bash(infsh *)
---
# 竞品分析

通过 [inference.sh](https://inference.sh) 命令行工具进行结构化的竞品分析，包括研究和截图收集。

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

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可手动进行安装和验证：[手动安装与验证指南](https://dist.inference.sh/cli/checksums.txt)。

## 竞品分析框架

### 七层分析模型

| 分层 | 分析内容 | 数据来源 |
|-------|----------------|-------------|
| 1. **产品** | 功能、用户体验（UX）、质量 | 截图、免费试用版 |
| 2. **定价** | 价格方案、定价模式、隐藏费用 | 定价页面、销售电话 |
| 3. **市场定位** | 宣传信息、口号、市场定位（ICP） | 网站、广告 |
| 4. **用户规模与增长** | 用户数量、收入、发展情况 | 网页搜索结果、新闻报道、融资信息 |
| 5. **用户评价** | 用户对产品的评价（优点和缺点） | G2、Capterra、App Store |
| 6. **内容与营销** | 博客内容、社交媒体活动、SEO 策略 | 网站内容、社交媒体账号 |
| 7. **团队背景** | 团队规模、关键成员信息 | LinkedIn、公司官网的“关于我们”页面 |

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

### 分类标准

- ✅ = 完全支持
- ⚠️ 或 “部分支持” = 功能有限或有使用限制
- ❌ = 不支持该功能
- 注意特殊说明：如 “仅限付费用户”、“企业级版本”、“测试版”
- 首先关注您具有优势的功能
- 对竞品的优点要如实评估——诚信至关重要

## 定价比较

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

### 需要关注的要点：

- 最低用户数量要求
- 是否仅支持年度订阅（降低灵活性）
- 不同等级之间的功能限制
- 过度使用费用
- 设置/入职费用
- 合同锁定期

## SWOT 分析

为每个竞品制定 SWOT 分析：

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

### 选择有意义的维度

| 有意义的维度 | 不太有意义的维度 |
|-----------|----------|
| 简单 vs. 复杂 | 好 vs. 坏 |
| 中小企业 vs. 企业级 | 便宜 vs. 昂贵（过于明显） |
| 自助服务 vs. 销售驱动 | 传统 vs. 创新 |
| 专业领域 vs. 广泛适用 | 规模小 vs. 规模大 |
| 固定模式 vs. 灵活模式 | — |

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

### 生成可视化图表

```bash
# Create positioning map with Python
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nfig, ax = plt.subplots(figsize=(10, 10))\n\n# Competitors\ncompetitors = {\n    \"You\": (-0.3, -0.3),\n    \"Competitor A\": (0.5, 0.6),\n    \"Competitor B\": (0.6, -0.4),\n    \"Competitor C\": (-0.4, 0.5)\n}\n\nfor name, (x, y) in competitors.items():\n    color = \"#22c55e\" if name == \"You\" else \"#6366f1\"\n    size = 200 if name == \"You\" else 150\n    ax.scatter(x, y, s=size, c=color, zorder=5)\n    ax.annotate(name, (x, y), textcoords=\"offset points\", xytext=(10, 10), fontsize=12, fontweight=\"bold\")\n\nax.axhline(y=0, color=\"grey\", linewidth=0.5)\nax.axvline(x=0, color=\"grey\", linewidth=0.5)\nax.set_xlim(-1, 1)\nax.set_ylim(-1, 1)\nax.set_xlabel(\"Simple ← → Complex\", fontsize=14)\nax.set_ylabel(\"SMB ← → Enterprise\", fontsize=14)\nax.set_title(\"Competitive Positioning Map\", fontsize=16, fontweight=\"bold\")\nax.grid(True, alpha=0.3)\nplt.tight_layout()\nplt.savefig(\"positioning-map.png\", dpi=150)\nprint(\"Saved\")"
}'
```

## 用户评价收集

### 评价来源

| 平台 | 适用范围 | URL 模式 |
|----------|----------|-------------|
| G2 | B2B SaaS 产品 | g2.com/products/[产品名称]/reviews |
| Capterra | 商业软件 | capterra.com/software/[产品ID]/reviews |
| App Store | iOS 应用 | apps.apple.com |
| Google Play | Android 应用 | play.google.com |
| Product Hunt | 新产品发布 | producthunt.com/posts/[产品名称] |
| Reddit | 用户评价 | reddit.com/r/[相关子版块] |

### 收集评价时需要注意的内容：

| 评价类别 | 关注点 |
|----------|---------|
| **最受好评的功能** | 用户最常提到的优点是什么？ |
| **最常被抱怨的问题** | 用户的不满之处是什么？（这可能是您的机会） |
| **用户更换产品的原因** | 用户为何选择更换产品？ |
| **用户需求** | 用户希望添加哪些功能？ |
| **用户比较内容** | 用户在比较产品时提到了哪些方面？ |

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

## 成果输出格式

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

1. 公司概况（规模、融资情况、团队信息）
2. 产品分析（功能、用户体验截图）
3. 定价详情
4. SWOT 分析
5. 用户评价分析（最受好评的功能、最常被抱怨的问题）
6. 竞品的市场定位与您的产品相比如何
7. 市场机会总结

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
| 仅关注产品功能 | 忽略了市场定位、定价和用户规模 | 使用七层分析模型 |
| 偏颇的分析 | 降低可信度 | 对竞品的优点要如实评估 |
| 数据过时 | 得出错误结论 | 确保所有数据均为最新，并每季度更新 |
| 分析对象过多 | 分析陷入混乱 | 重点关注前 3-5 个主要竞争对手 |
| 分析缺乏深度 | 数据缺乏实际意义 | 每个分析部分都要说明对您的启示 |
| 仅比较功能 | 无法全面了解竞品优势 | 需要包括定价、用户评价和市场定位信息 |

## 相关技能

```bash
npx skills add inference-sh/skills@web-search
npx skills add inference-sh/skills@prompt-engineering
```

查看所有应用程序：`infsh app list`