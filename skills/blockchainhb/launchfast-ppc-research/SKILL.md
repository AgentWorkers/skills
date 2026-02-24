---
name: launchfast-ppc-research
description: |
  Amazon PPC keyword research using the LaunchFast MCP. Analyzes up to 15
  competitor ASINs at once, extracts ranked keywords, segments by match type,
  and generates a ready-to-upload Amazon Sponsored Products Bulk Operations CSV.

  USE THIS SKILL FOR:
  - "PPC research for [ASIN]"
  - "find keywords for my Amazon listing"
  - "build a PPC campaign for [product]"
  - "what keywords are competitors using?"
  - "generate Amazon bulk upload file"

  Requirements: mcp__launchfast__amazon_keyword_research available

argument-hint: [ASIN1] [ASIN2] ... | "ppc [keyword]"
---

# LaunchFast PPC 研究技能

您是一名亚马逊 PPC 专家。您可以使用 LaunchFast 的关键词智能工具从竞争对手的 ASIN 中提取高价值关键词，根据匹配类型和关键词的优先级对这些关键词进行分类，并生成一份可直接用于亚马逊批量操作上传器的 CSV 文件。

**开始前的要求：**
- 确保 `mcp__launchfast__amazon_keyword_research` 已经可用。

---

## 第 1 步 — 收集 ASIN

如果尚未提供 ASIN，请请求用户提供：

```
Which ASINs do you want to research? (1–15 competitor or own ASINs)
Example: B08N5WRWNW, B07XYZABC1

Optional:
- Your product's ASIN (for "Your Edge" filtering — keywords where competitors rank poorly)
- Campaign name for the bulk upload? (default: "LaunchFast-Campaign-[Date]")
- Default bid per click? (default: $0.75)
- Daily budget? (default: $25/day)
```

---

## 第 2 步 — 运行关键词研究

一次性调用所有提供的 ASIN（最多 15 个）：

```
mcp__launchfast__amazon_keyword_research(asins: ["B0...", "B0...", ...])
```

---

## 第 3 步 — 处理关键词数据

### 去重
合并出现在多个 ASIN 中的关键词。记录每个关键词对应的 ASIN——重叠度越高，优先级越高。

### 关键词分类

将每个关键词分为不同的等级：

| 等级 | 判断标准 | 处理方式 |
|------|----------|--------|
| **一级关键词（高优先级）** | 搜索量高且竞争度低，或出现在 3 个及以上 ASIN 中 | 精确匹配 + 短语匹配 |
| **二级关键词（成长型）** | 搜索量适中，竞争度适中 | 短语匹配 + 广义匹配 |
| **三级关键词（发现型）** | 长尾关键词，搜索量低 | 仅使用广义匹配 |

### 匹配类型分配

```
Exact match  → Tier 1 keywords (most targeted, highest bid)
Phrase match → Tier 1 + Tier 2
Broad match  → Tier 2 + Tier 3 (discovery, lower bid)
```

### 出价估算

```
Exact:  user default bid × 1.2
Phrase: user default bid × 1.0
Broad:  user default bid × 0.7
```

### 负面关键词
标记明显不相关的关键词（例如错误的商品类别、无关产品的品牌名称等）——将这些关键词作为负面关键词（精确匹配类型）添加到文件中。

---

## 第 4 步 — 显示关键词汇总信息

在生成 CSV 文件之前，向用户展示关键词的汇总信息：

```markdown
## PPC Keyword Research — [Date]
ASINs analyzed: [N] | Unique keywords found: [N]

### Tier breakdown
| Tier | Keywords | Avg Search Vol | Match Types |
|------|----------|----------------|-------------|
| Tier 1 — Priority | X | X,XXX | Exact + Phrase |
| Tier 2 — Growth   | X |   XXX | Phrase + Broad |
| Tier 3 — Discovery| X |    XX | Broad only     |

### Top 15 keywords preview
| Keyword | Search Vol | Tier | Match Types | Bid (Exact) |
|---------|------------|------|-------------|-------------|
| ...

### Negative keywords flagged: [N]

Proceed with bulk CSV generation? [Yes / Adjust tiers first]
```

---

## 第 5 步 — 生成用于亚马逊批量上传的 CSV 文件

用户确认后，生成一个以制表符分隔的 `.txt` 文件，文件格式如下：

```
~/Downloads/launchfast-ppc-bulk-[date].txt
```

### 亚马逊广告产品批量操作格式要求
文件必须使用制表符分隔（TSV 格式），并且列标题必须按照以下顺序排列：

```
Product	Entity	Operation	Campaign ID	Ad Group ID	Portfolio ID	Ad ID	Keyword ID	Product Targeting ID	Campaign Name	Ad Group Name	Start Date	End Date	Targeting Type	State	Daily Budget	SKU	ASIN	Ad Group Default Bid	Bid	Custom Text	Campaign Type	Targeting Expression
```

### 文件行结构
- **生成三种类型的行：**
  - **活动行**（每个活动对应一行）
  - **广告组行**（每个等级对应一行）
  - **关键词行**（每个关键词对应一行，包含其匹配类型）

#### 活动行的结构：
```
Sponsored Products	Campaign	Create		[leave blank]	[leave blank]		[leave blank]	[leave blank]	[Campaign Name]		[StartDate YYYYMMDD]		Manual	enabled	[Daily Budget]
```

#### 广告组行的结构：
```
Sponsored Products	Ad Group	Create		[leave blank]	[leave blank]		[leave blank]	[leave blank]	[Campaign Name]	[Ad Group Name]	[StartDate]		Manual	enabled		[leave blank]	[leave blank]	[Default Bid]
```

#### 关键词行的结构：
- 每个关键词对应一行，包含其匹配类型

#### 活动结构的详细说明：
```
Campaign: [Campaign Name]
├── Ad Group: Tier1-Exact
│   └── Keywords: [Tier 1 keywords] — Match: Exact
├── Ad Group: Tier1-Phrase
│   └── Keywords: [Tier 1 keywords] — Match: Phrase
├── Ad Group: Tier2-Phrase
│   └── Keywords: [Tier 2 keywords] — Match: Phrase
└── Ad Group: Tier3-Broad
    └── Keywords: [Tier 2 + Tier 3] — Match: Broad
```

完成 CSV 文件的编写后，向用户确认文件路径和行数。

---

## 第 6 步 — 上传说明

文件生成完成后，向用户提供上传说明：

```
## How to upload to Amazon

1. Go to Seller Central → Advertising → Campaign Manager
2. Click "Bulk Operations" (top right)
3. Click "Upload" → choose file: launchfast-ppc-bulk-[date].txt
4. Review the preview → click "Submit"

⚠️ Review before submitting:
   - Verify campaign name is correct
   - Check daily budget matches your plan
   - Confirm ASINs in your ad groups match your listing
```