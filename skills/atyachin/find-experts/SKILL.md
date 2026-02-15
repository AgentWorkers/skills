---
name: expert-finder
description: "寻找任何领域的专家、思想领袖和行业权威人士。在 Twitter 和 Reddit 上搜索那些在特定领域展现出深厚知识、频繁参与讨论以及超出平均水平的专业能力的人。这项工作包括专家的发现、人才的挖掘、研究人员的识别，以及关键意见领袖（KOL）的定位。"
homepage: https://xpoz.ai
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["mcporter"],
            "skills": ["xpoz-setup"],
            "tools": ["web_search", "web_fetch"],
            "network": ["mcp.xpoz.ai"],
            "credentials": "Xpoz account (free tier) — auth via xpoz-setup skill (OAuth 2.1)",
          },
      },
  }
tags:
  - expert-finder
  - domain-expert
  - thought-leader
  - talent-sourcing
  - researcher
  - KOL
  - twitter
  - reddit
  - social-media
  - knowledge
  - authority
  - subject-matter-expert
  - people-search
  - intelligence
  - mcp
  - xpoz
---

# 专家查找器

通过分析 Twitter 和 Reddit 上的社交媒体活动，可以找到任何领域的专家、思想领袖和主题权威人士。

**功能说明：** 给定一个领域、主题或一组关键词，该工具会将其扩展为全面的搜索词，然后在社交媒体中搜索那些频繁讨论该主题且具备超出平均水平知识的人，根据类型（深度专家、思想领袖或实践者）对这些人进行分类，并生成详细的报告。

---

## 第一阶段：领域研究与查询扩展

### 第一步：了解领域

用户可以提供以下信息之一：
- **一个领域/主题**（例如：“量子计算”、“Kubernetes 安全”、“再生农业”）
- **关键词**（例如：“LLM 微调”、“RLHF”、“偏好优化”）
- 定义该领域的论文、项目或产品的 **URL**

如果提供了 URL，请对其进行研究：
```
web_fetch url="<provided URL>"
```

如果只提供了关键词/主题，请进一步扩展理解：
```
web_search query="<topic> overview key concepts terminology"
web_search query="<topic> leading researchers practitioners"
```

### 第二步：构建领域概况

创建一个领域概况：
```json
{
  "domain": "Short domain name",
  "description": "One-paragraph description of the field",
  "core_terms": ["term1", "term2", "term3"],
  "technical_terms": ["jargon1", "jargon2"],
  "adjacent_fields": ["related1", "related2"],
  "key_conferences": ["conf1", "conf2"],
  "known_authorities": ["person1", "person2"],
  "subreddits": ["r/relevant1", "r/relevant2"]
}
```

### 第三步：生成搜索查询

将领域信息扩展为多层次的搜索查询：

| 层级 | 目的 | 例如（以“RLHF”为例） |
|------|---------|----------------------|
| **第一层级：核心** | 精确的领域术语 | `"RLHF"`、`“基于人类反馈的强化学习"` |
| **第二层级：技术性** | 仅专家使用的专业术语 | `"奖励模型过拟合"`、`“KL 散度惩罚"`、`“PPO 与 DPO”` |
| **第三层级：相关领域** | 相关的专业知识信号 | `"偏好优化"`、`“宪法式 AI"`、`“对齐研究"` |
| **第四层级：讨论** | 意见/辩论的标记 | `"RLHF 与..."` 或 `“RLHF 的问题"`、`“热门观点” AND `“对齐...”` |

**生成 10-20 条覆盖所有层级的查询。第二层级（技术性术语）的信息最为重要——使用专业术语的人更有可能是真正的专家。**

### 第四步：自动执行

不要停下来询问用户的确认，直接使用生成的查询进入第二阶段。只需发送简短的进度更新（每个阶段一行，例如：“🔍 正在 Twitter 上搜索 16 条查询...” 或 “📊 正在分析 24 位候选人...”）。

---

## 第二阶段：社交媒体搜索

### 第五步：搜索 Twitter

使用 Xpoz 工具搜索每一组查询：
```bash
mcporter call xpoz.getTwitterPostsByKeywords \
  query='"RLHF" OR "reinforcement learning from human feedback"' \
  startDate="<6 months ago>" \
  fields='["id","text","authorUsername","likeCount","retweetCount","replyCount","impressionCount","createdAtDate"]'
```

**重要提示：** 必须使用完整的 CSV 数据集，而不仅仅是前 100 页的分页结果。**

每次 Xpoz 搜索都会在响应中生成一个 `dataDumpExportOperationId`。你必须：
1. 记下每个搜索结果的 `dataDumpExportOperationId`
2. 使用 `checkOperationStatus` 命令检查搜索是否完成
3. 从返回的 S3 URL 下载 CSV 文件
4. 使用 Python/pandas 分析所有数据行（而不仅仅是分页显示的第一页）
```bash
# Step 1: Run search (returns first 100 + dataDumpExportOperationId)
mcporter call xpoz.getTwitterPostsByKeywords \
  query='"RLHF" OR "reinforcement learning from human feedback"' \
  startDate="<6 months ago>" \
  fields='["id","text","authorUsername","likeCount","retweetCount","replyCount","impressionCount","createdAtDate"]'

# Step 2: Poll the datadump operation (NOT the search operation)
mcporter call xpoz.checkOperationStatus operationId="op_datadump_XXXXX"
# Repeat every 5 seconds until status=completed → get S3 download URL

# Step 3: Download full CSV
curl -o /tmp/expert-search-q1.csv "<S3_URL>"

# Step 4: Analyze with Python/pandas
python3 analyze_experts.py /tmp/expert-search-q1.csv
```

**原因说明：** 如果搜索返回 2,000 条帖子，分页结果中只显示 100 条。其余 1,900 条帖子中可能包含其他专家的信息，但你会错过这些信息。CSV 文件中包含完整的数据集（每个查询最多 64,000 行）。

### 第六步：搜索 Reddit

```bash
mcporter call xpoz.getRedditPostsByKeywords \
  query='"RLHF" OR "reinforcement learning from human feedback"' \
  fields='["id","title","text","authorUsername","subredditName","score","numComments","createdAtDate"]'
```

同时搜索活跃的评论者（通常是那些深入讨论问题的专家）：
```bash
mcporter call xpoz.getRedditCommentsByKeywords \
  query='"reward hacking" OR "KL penalty" OR "PPO training"' \
  fields='["id","text","authorUsername","subredditName","score","createdAtDate"]'
```

### 第七步：提取候选作者（代码分析）

**首先下载所有 CSV 文件**（来自第 5 和第 6 步的操作），然后使用 Python/pandas 从完整数据集中构建作者频率表：
```python
import pandas as pd
from collections import defaultdict

# Load all CSVs
dfs = []
for f, tier in [("q1-core.csv", 1), ("q2-technical.csv", 2), ("q3-adjacent.csv", 3), ("q4-discussion.csv", 4)]:
    df = pd.read_csv(f"/tmp/expert-{f}")
    df["tier"] = tier
    dfs.append(df)

all_posts = pd.concat(dfs, ignore_index=True)

# Aggregate by author
authors = all_posts.groupby("author_username").agg(
    post_count=("id", "count"),
    total_likes=("like_count", "sum"),
    avg_likes=("like_count", "mean"),
    total_impressions=("impression_count", "sum"),
    avg_impressions=("impression_count", "mean"),
    tiers_hit=("tier", lambda x: len(set(x))),
    tier_list=("tier", lambda x: sorted(set(x))),
).sort_values("post_count", ascending=False)

# Filter: minimum 3 posts, at least 2 tiers
candidates = authors[(authors["post_count"] >= 3) & (authors["tiers_hit"] >= 2)]
print(f"Found {len(candidates)} candidates from {len(all_posts)} total posts")
print(candidates.head(30).to_string())
```

**关键提示：** 在多个查询层级中出现的作者，尤其是第二层级（技术性术语）的作者，更有可能是真正的专家。**

其他筛选条件：
- 在指定时间范围内至少发布 3 条相关帖子
- 至少涉及 2 个查询层级（覆盖广泛的领域）
- 过滤掉明显的机器人（在 Twitter 上使用 `isInauthentic` 进行检查）
- 第二层级的匹配结果权重更高——自然使用专业术语是 strongest 的专业知识信号

---

## 第三阶段：专家分析与分类

### 第八步：深入分析顶级候选人

根据出现频率和参与度，选取前 20-30 位候选人，获取他们的完整资料：

**Twitter：**
```bash
mcporter call xpoz.getTwitterUser \
  identifier="USERNAME" \
  identifierType="username" \
  fields='["username","name","description","followersCount","followingCount","tweetCount","verified","verifiedType","avgTweetsPerDayLastMonth","isInauthentic","isInauthenticProbScore"]'
```

**Reddit：**
```bash
mcporter call xpoz.getRedditUser \
  username="USERNAME" \
  fields='["username","totalKarma","linkKarma","commentKarma","profileDescription","isMod","createdAt"]'
```

⚠️ **速率限制：** API 请求之间至少间隔 1 秒。

### 第九步：分析内容深度

获取每位候选人的最新帖子：

**Twitter：**
```bash
mcporter call xpoz.getTwitterPostsByAuthor \
  identifier="USERNAME" \
  identifierType="username" \
  startDate="<6 months ago>" \
  fields='["id","text","likeCount","retweetCount","replyCount","impressionCount","createdAtDate"]'
```

**Reddit：**
```bash
mcporter call xpoz.getRedditPostsByAuthor \
  username="USERNAME" \
  fields='["id","title","text","subredditName","score","numComments","createdAtDate"]'
```

### 第十步：分类专家类型

分析每位候选人的内容，将其归类为以下类型之一：

| 类型 | 识别信号 | 例子 |
|------|---------|---------|
| **🔬 深度专家** | 自然使用专业术语，分享原创研究/发现，解释复杂概念，引用论文/数据，纠正他人的误解 | 博士研究员、核心贡献者 |
| **💡 思想领袖** | 提出高水平的战略观点，预测趋势，拥有大量受众，被他人引用，在会议上发言 | 行业分析师、CEO/CTO |
| **🛠️ 实践者** | 分享实际经验、教程、“这是我开发的”、故障排除技巧、实际应用案例 | 高级工程师、顾问 |
| **📣 传播者/整理者** | 整理并分享他人的工作，总结发展动态，发布频率高，擅长提炼信息 | 通讯作者、社区经理 |
| **🎓 教育者** | 清晰解释概念，创建学习内容，发布教程/指南，回答初学者的问题 | 教授、课程创建者、技术作家 |

**分类依据：**

**深度专家的识别信号：**
- 自然使用第二层级（技术性术语），而不仅仅是引用
- 帖子包含原创分析、数据或数字
- 其他专家会与他们的帖子互动（回复质量高于回复数量）
- 个人简介中提到研究经历、博士学位或具体技术职位
- 在 Reddit 上的评论 karma 高于链接 karma（说明他们提供了更多有价值的内容）
- 帖子中包含纠正或细致的观点（例如：“实际上，问题在于...”）

**思想领袖的识别信号：**
- 相对于帖子发布频率，粉丝数量较多
- 使用非技术性语言也能获得高关注度和互动
- 预测行业趋势，分享观点
- 个人简介中提到咨询角色、演讲经历或投资经历
- 关注广泛的主题，而不仅仅是技术细节

**实践者的识别信号：**
- 使用“这是我开发的”、“我们已经上线了”、“在实践中使用”等表述
- 分享代码、配置信息、架构决策
- 讨论权衡和实际限制
- 个人简介中提到具体的公司/产品/项目

**传播者/整理者的识别信号：**
- 发布频率高
- 主要分享/转发他人的内容并添加评论
- 使用标签如“Thread 🧵”、“汇总”、“本周热点...”等
- 链接到多种不同的来源

**教育者的识别信号：**
- 用简单的语言解释概念，创建学习资源，发布教程/指南
- 逐步分解复杂内容
- 在 Reddit 的帮助/问答帖子中活跃

一个人可以同时属于多种类型（例如：深度专家 + 教育者）。可以为他们分配主要类型和可选的次要类型。

### 第十一步：评分与排名

**专业知识评分（0-100 分）：**

| 因素 | 权重 | 评估方法 |
|--------|--------|----------------|
| **领域深度** | 30 | 是否使用了第二层级的查询术语、专业术语，以及是否有原创分析 |
| **一致性** | 20 | 他们在该领域发布的频率（而不仅仅是一条火爆的帖子） |
| **同行认可度** | 20 | 来自其他专家的互动（回复、引用），而不仅仅是点赞数量 |
| **覆盖范围** | 15 | 涉及的查询层级数量，以及覆盖的相关领域范围 |
| **资质** | 15 | 个人简介中的信息（头衔、公司、教育背景、验证状态） |

**评分标准：**

| 分数 | 含义 |
|-------|---------|
| 80-100 | 绝对权威——该领域的顶尖人物 |
| 60-79 | 强大的专家——知识渊博，经常发表见解 |
| 40-59 | 稳定的实践者——知识扎实，有一定影响力 |
| 20-39 | 积极参与的参与者——讨论该主题但深度有限 |

**互动质量比数量更重要：**
- 来自领域专家的回复数量 > 来自普通用户的点赞数量 |
- 关于该主题的持续发布内容 > 只是一条火爆的帖子 |
- 原创见解 > 仅仅转发他人的内容 |

---

## 第四阶段：生成报告

### 第十二步：生成专家报告

按专家类型分组展示结果，并在每个组内按评分排序。

```markdown
## Expert Report: [Domain]
**Date:** YYYY-MM-DD
**Sources:** Twitter, Reddit
**Timeframe:** Last 6 months
**Posts analyzed:** X,XXX across Y queries

---

### Summary
Found **N experts** across X candidates analyzed.
- 🔬 Deep Experts: N
- 💡 Thought Leaders: N
- 🛠️ Practitioners: N
- 📣 Evangelists/Curators: N
- 🎓 Educators: N

### Top Experts

#### 🥇 1. @username — 🔬 Deep Expert (Score: 92)
**Platform:** Twitter | **Followers:** 12.4K
**Bio:** [their bio]
**Why expert:** [specific evidence — e.g., "Published 23 posts about reward model optimization, uses advanced terminology naturally, cited by 3 other experts in our results"]
**Key post:** "[quote of their most insightful post]" — ❤️ 342 🔁 89
**Domain coverage:** Core ✅ Technical ✅ Adjacent ✅ Discussion ✅
**Posting frequency:** ~4 posts/week on this topic

---

#### 🥈 2. u/username — 🛠️ Practitioner + 🎓 Educator (Score: 85)
**Platform:** Reddit | **Karma:** 45.2K (32K comment)
**Active in:** r/MachineLearning, r/LocalLLaMA
**Why expert:** [specific evidence]
**Key post:** "[quote]" — ⬆️ 234, 67 comments
...
```

### 如果需要，使用电子邮件格式

使用 himalaya MML 格式，并采用卡片布局：
```
From: Expert Finder <net-service@xpoz.ai>
To: recipient@example.com
Subject: Expert Report: [Domain] — Top N Experts Found

<#multipart type=alternative>
Expert Report: [Domain]
Found N experts across Twitter and Reddit.
[plain text summary]

<#part type=text/html>
<html>
<head>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }
  .container { max-width: 680px; margin: 0 auto; }
  .card { background: #fff; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 24px; margin-bottom: 16px; }
  .expert-type { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }
  .type-deep { background: #dbeafe; color: #1e40af; }
  .type-leader { background: #fef3c7; color: #92400e; }
  .type-practitioner { background: #d1fae5; color: #065f46; }
  .type-evangelist { background: #ede9fe; color: #5b21b6; }
  .type-educator { background: #fce7f3; color: #9d174d; }
  .score { font-size: 24px; font-weight: 700; color: #111; }
  .quote { border-left: 3px solid #e5e7eb; padding-left: 12px; color: #6b7280; font-style: italic; margin: 12px 0; }
</style>
</head>
<body>
<table width="100%" cellpadding="0" cellspacing="0" style="max-width:680px;margin:0 auto;">
<tr><td>
  <h1 style="font-size:22px;">Expert Report: [Domain]</h1>
  <p style="color:#6b7280;">Found N experts · Twitter + Reddit · Last 6 months</p>

  <!-- Repeat per expert -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,0.1);padding:24px;margin-bottom:16px;">
  <tr><td style="padding:24px;">
    <table width="100%"><tr>
      <td><strong style="font-size:18px;">#1 @username</strong><br/>
        <span style="background:#dbeafe;color:#1e40af;padding:2px 10px;border-radius:12px;font-size:12px;">🔬 Deep Expert</span>
      </td>
      <td align="right"><span style="font-size:28px;font-weight:700;">92</span><br/><span style="color:#6b7280;font-size:12px;">score</span></td>
    </tr></table>
    <p style="color:#6b7280;margin:8px 0;">Twitter · 12.4K followers · 4 posts/week on topic</p>
    <p><strong>Why:</strong> Published 23 posts about reward model optimization...</p>
    <div style="border-left:3px solid #e5e7eb;padding-left:12px;color:#6b7280;font-style:italic;margin:12px 0;">
      "Their most insightful post quoted here" — ❤️ 342 🔁 89
    </div>
  </td></tr>
  </table>
  <!-- End repeat -->

</td></tr>
</table>
</body>
</html>
<#/multipart>
```

---

## 获取最佳结果的技巧：

1. **具体领域比宽泛领域更有效**——例如，“Kubernetes 网络策略调试”比“Kubernetes”能找到更深入的专家 |
2. **技术性术语至关重要**——第二层级的查询是识别专家的最佳信号 |
3. **Reddit 上的评论比帖子更重要**——深入的专家通常会发表评论而不是发布新帖子 |
4. **6 个月的搜索时间范围是最理想的**——既保证了一定的持续性，又确保了结果的时效性 |
5. **跨平台活跃**——在同一领域同时在 Twitter 和 Reddit 上活跃的人是强有力的候选者 |
6. **查看专家之间的互动情况**——如果专家 A 回复了专家 B 的技术帖子，那么专家 B 也很可能是专家 |