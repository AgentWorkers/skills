---
name: social-lead-gen
description: "**通过社交媒体获取潜在客户：** 在实时的 Twitter、Instagram 和 Reddit 对话中寻找有明确购买意向的用户。系统会自动研究您的产品，生成针对性的搜索查询，并识别出那些正在积极寻找您所提供的解决方案的用户。这种社交销售和潜在客户挖掘功能基于超过 15 亿条已索引的帖子来实现。"
homepage: https://xpoz.ai
metadata:
  {
    "openclaw":
      {
        "requires": {
          "bins": ["mcporter"],
          "skills": ["xpoz-setup"],
          "tools": ["web_search", "web_fetch"],
          "network": ["mcp.xpoz.ai"],
          "credentials": "Xpoz account (free tier) — auth via xpoz-setup skill (OAuth 2.1)"
        },
      },
  }
tags:
  - lead-generation
  - sales
  - prospecting
  - social-media
  - twitter
  - instagram
  - reddit
  - find-leads
  - social-selling
  - buyer-intent
  - outreach
  - growth
  - marketing
  - customer-discovery
  - leads
  - mcp
  - xpoz
  - leads
  - intent
  - discovery
---

# 社交媒体潜在客户开发

**从社交媒体上用户实际发表的内容中找到需要您产品的人。**

与传统的潜在客户开发工具不同，该技能是从实时对话中挖掘出具有高意向的潜在客户。它能够发现那些在 Twitter、Instagram 和 Reddit 上积极表达自己产品所解决问题的用户——这一切都依赖于 Xpoz MCP 提供的超过 15 亿条索引帖子。

---

## ⚡ 先决条件

1. **必须配置并验证 Xpoz MCP**。请按照 [xpoz-setup](https://clawhub.ai/skills/xpoz-setup) 的步骤进行设置。
2. 必须具备 **网络搜索和数据获取** 工具（OpenClaw 中已包含）。

验证 Xpoz 是否已准备好：
```bash
mcporter call xpoz.checkAccessKeyStatus
```
如果 `hasAccessKey: false`，请先执行 xpoz-setup，然后再回到这里。

---

## 工作原理

```
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  PHASE 1: LEARN  │ →  │ PHASE 2: SEARCH  │ →  │ PHASE 3: SCORE   │
│                  │    │                  │    │                  │
│ Research product │    │ Generate queries  │    │ Score by intent  │
│ Analyze website  │    │ Search Twitter    │    │ Rank leads       │
│ Find competitors │    │ Search Instagram  │    │ Write outreach   │
│ Map pain points  │    │ Search Reddit     │    │ Export results   │
│ Validate w/ user │    │ Poll for results  │    │ Track sent leads │
└──────────────────┘    └──────────────────┘    └──────────────────┘
     (one-time)             (repeatable)            (repeatable)
```

---

## 第一阶段：产品研究（一次性设置）

**此阶段会深入了解用户的产品信息。只需运行一次，结果会被保存并重复使用。**

### 第一步：向用户索取参考信息

询问用户：
> “您希望为哪种产品或服务寻找潜在客户？请提供一个参考信息——网站链接、GitHub 仓库链接、产品描述，或者任何能说明您所提供服务的信息。”

用户可能会提供：
- 网站链接（例如：`https://example.com`）
- GitHub 仓库链接（例如：`https://github.com/org/repo`）
- 产品名称及描述
- 多个参考信息

### 第二步：深入研究

对于每个提供的参考信息，尽可能收集更多相关信息：

**对于网站：**
- 使用 `web_fetch` 获取首页、价格页面、关于页面和文档
- 使用 `web_search` 查找评论、提及、对比内容和媒体报道

**对于 GitHub 仓库：**
- 使用 `web_fetch` 阅读 README 文件
- 查看星标数量、描述和讨论主题
- 使用 `web_search` 查找相关讨论和博客文章

**对于产品名称：**
- 使用 `web_search` 查找产品官网、评论和替代产品
- 然后获取并分析这些信息

**提取并整理数据：**

```json
{
  "product": {
    "name": "",
    "website": "",
    "tagline": "",
    "description": "",
    "category": "",
    "pricing": ""
  },
  "value_proposition": {
    "what_it_does": "",
    "key_features": [],
    "differentiators": []
  },
  "target_audience": {
    "primary_icp": "",
    "segments": [
      {
        "name": "",
        "description": "",
        "pain_points": [],
        "where_they_hang_out": {
          "subreddits": [],
          "hashtags": [],
          "communities": []
        }
      }
    ]
  },
  "pain_points_solved": [],
  "competitors": [
    {
      "name": "",
      "website": "",
      "how_different": ""
    }
  ],
  "social_proof": {
    "testimonials": [],
    "case_studies": [],
    "notable_customers": []
  },
  "keywords": {
    "product_terms": [],
    "pain_point_terms": [],
    "competitor_terms": [],
    "industry_terms": []
  }
}
```

### 第三步：与用户确认信息

以清晰的总结形式向用户展示您的发现：
> “关于您的产品，我了解到以下信息：
>
> **[产品名称]** — [产品口号]
>
> **产品功能：** [产品描述]
>
> **目标受众：** [目标用户群体]
>
> **您解决的问题：**
> - [问题 1]
> - [问题 2]
>
> **竞争对手：** [竞争对手列表]
>
> **主要优势：** [产品优势列表]
>
> 这些信息准确吗？还有需要补充或修改的地方吗？”

**等待用户确认或修改。** 在得到他们的同意之前不要继续下一步。

如果用户有修改，请更新用户资料并重新验证。

### 第四步：生成搜索查询

根据验证后的用户资料，为每个平台生成针对性的搜索查询：

**查询类别：**
1. **问题相关查询** — 表达出产品所解决问题的用户
2. **对竞争对手不满的查询** — 抱怨竞争对手的用户
3. **寻找工具/解决方案的查询** — 积极寻找产品信息的用户
4. **行业相关讨论的查询** — 目标受众正在讨论的相关话题

**对于每个查询，需要指定：**
- 平台（Twitter、Instagram、Reddit）
- 查询字符串（使用布尔运算符）
- 目标子版块（针对 Reddit）
- 最低参与度阈值
- 数据检索时间范围

每个平台生成 4-6 条查询（总共 12-18 条）。

### 第五步：保存用户资料

保存验证后的用户资料和生成的查询：
```bash
mkdir -p data/social-lead-gen
# Save product-profile.json and search-queries.json
```

向用户展示生成的查询：
> “我已经为 Twitter、Instagram 和 Reddit 生成了 [N] 条搜索查询。以下是一些示例：
>
> **Twitter（问题相关查询）：** `"[查询示例]"`
> **Reddit（寻找工具的查询）：** `"[查询示例]"` 在 r/[子版块]`
>
> 准备开始寻找潜在客户了吗？**

---

## 第二阶段：潜在客户发现（可重复执行）

**每当需要新的潜在客户时，都可以运行此阶段。** 它会使用之前保存的用户资料和查询。

### 第一步：加载用户资料

```bash
cat data/social-lead-gen/product-profile.json
cat data/social-lead-gen/search-queries.json
```

如果这些文件不存在，请先运行第一阶段。

### 第二步：执行搜索

对于每个生成的查询，调用相应的 Xpoz MCP 工具：

**Twitter：**
```bash
mcporter call xpoz.getTwitterPostsByKeywords \
  query="GENERATED_QUERY" \
  startDate="LOOKBACK_DATE" \
  limit=50 \
  fields='["id","text","authorUsername","likeCount","retweetCount","replyCount","impressionCount","createdAtDate"]'
```

**Instagram：**
```bash
mcporter call xpoz.getInstagramPostsByKeywords \
  query="GENERATED_QUERY" \
  startDate="LOOKBACK_DATE" \
  limit=50
```

**Reddit：**
```bash
mcporter call xpoz.getRedditPostsByKeywords \
  query="GENERATED_QUERY" \
  startDate="LOOKBACK_DATE" \
  limit=50
```

**持续获取结果：**
```bash
mcporter call xpoz.checkOperationStatus operationId="OPERATION_ID"
```

每隔 5 秒检查一次搜索结果的状态，直到状态变为 `completed`。

### 第三步：找到相关用户（而不仅仅是帖子）

对于参与度高的帖子，还要查找发布这些帖子的用户：

```bash
mcporter call xpoz.getTwitterUsersByKeywords \
  query="GENERATED_QUERY" \
  limit=50
```

这样就能找到经常发布相关内容的用户——他们可能是潜在的客户或意见领袖。

---

## 第三阶段：潜在客户评分与输出

### 评分标准（1-10 分）

根据用户资料中的信息对每个潜在客户进行评分：

| 评分标准 | 分数 | 举例 |
|--------|--------|---------|
| **明确表示需要解决方案** | +3 | “有人能推荐 [产品类别] 吗？” |
| **抱怨竞争对手** | +2 | “[竞争对手] 的产品太贵/有问题/功能有限” |
| **面临实际问题** | +2 | “我需要 [特定功能]，但找不到合适的工具” |
**在目标社区活跃** | +1 | 在相关子版块发帖/使用相关标签 |
| **帖子互动度高** | +1 | 帖子获得超过 10 个赞或 5 条评论 |
| **帖子发布时间较短（<48 小时）** | +1 | 机会时效性强 |
| **用户资料符合目标群体特征** | +1 | 用户是开发者、营销人员或研究人员 |
| **销售竞争对手的产品** | -3 | 他们是竞争对手，不是潜在客户 |
| **背景信息无关** | -2 | 提到关键词但上下文不符 |

**评分等级：**
- **一级（8-10 分）：** 高意向潜在客户——需立即行动
- **二级（6-7 分）：** 温和潜在客户——值得跟进
- **三级（5 分）：** 关注名单——未来可能成为潜在客户 |
- **低于 5 分：** 可忽略

### 去重

在报告任何潜在客户之前，先检查是否与之前发送过的潜在客户重复：
```bash
cat data/social-lead-gen/sent-leads.json
```

关键格式：`{平台}:{作者}:{帖子ID}`

报告后，将结果添加到跟踪文件中。

### 输出格式

为每个潜在客户提供以下信息：
1. **用户信息：** 用户名、平台、资料概要
2. **用户言论：** 来自他们帖子的直接引文
3. **帖子链接：** 可点击的链接
   - Twitter：`https://twitter.com/{用户名}/status/{id}`
   - Reddit：`https://www.reddit.com/r/{子版块}/comments/{id}/`
   - Instagram：`https://www.instagram.com/p/{shortcode}/`
4. **评分：** X/10（附带评分理由）
5. **适合的原因：** 他们的问题与您的产品之间的关联
6. **建议的沟通方式：** 根据用户情况定制的回复内容
7. **互动情况：** 获得的点赞、评论和分享数量
8. **发布时间：** 帖子发布的时间

### 沟通指南

在编写回复时：
- 引用帖子中用户的具体情况
- 提及产品能解决他们问题的具体功能
- 保持对话风格，避免过于推销
- 保持诚实——如果产品并不完全符合用户需求，也要如实说明
- **务必披露** 用户是否与产品有合作关系

示例：
> “我也遇到过同样的问题！最终使用了 [产品]——它确实具有 [他们需要的具体功能]。[简要说明产品优势]。推荐查看：[链接]”
>
> （披露：我与 [产品] 有合作关系）”

---

## 更新用户资料

如果用户的产品发生了变化，可以重新运行第一阶段：

> “我们的产品进行了更新——现在也支持 [X] 功能。可以更新用户资料吗？”

重新进行研究、验证并生成新的查询。之前保存的用户资料会被覆盖。

---

## 示例流程

**用户：** “为我产品寻找潜在客户。这是我们的网站：https://example.com”

**代理：**
1. 获取并分析 example.com 的信息（首页、价格、文档）
2. 查找相关评论、竞争对手和提及内容
3. 向用户展示分析结果：“以下是我了解到的信息……”
4. 用户确认：“是的，我们的目标客户还包括企业用户”
5. 代理更新用户资料并生成 15 条搜索查询
6. 用户同意后，代理在 Twitter/Instagram/Reddit 上执行搜索
7. 返回结果：找到 12 个潜在客户（3 个一级潜在客户，5 个二级潜在客户，4 个三级潜在客户）
8. 提供每个潜在客户的详细信息（链接、评分、引用内容和沟通建议）

**第二天：** “再寻找更多潜在客户” → 代理加载保存的用户资料，重新生成查询，并与昨天的结果进行去重。

---

## 负责任的使用建议

- **遵守 Twitter、Instagram 和 Reddit 的服务条款**
- **不要发送垃圾信息** — 沟通内容必须真实且有帮助
- **在所有沟通中披露自己的合作关系**
- **尊重用户隐私** — 仅使用公开可获取的信息
- **质量优先** — 5 个优质潜在客户比 50 个普通潜在客户更有价值

---

## 资源参考

- **Xpoz：** [xpoz.ai] — 提供搜索功能的社交智能平台
- **设置指南：** [ClawHub 上的 xpoz-setup](https://clawhub.ai/skills/xpoz-setup) — 一次性身份验证
- **搜索参考：** [ClawHub 上的 xpoz-social-search](https://clawhub.ai/skills/xpoz-social-search) — 完整的搜索模板

---

**专为 ClawHub 开发 • 由 Xpoz 提供支持**