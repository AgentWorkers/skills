---
name: anti-seo-researcher
description: >
  **反SEO深度消费者研究工具**  
  当用户想要购买产品或做出消费决策时，可以使用此工具。该工具能够自动检测用户的语言，并根据用户所在地区调整平台及搜索策略。无论是否使用 `web_search` 功能，该工具都能正常运行；在 `web_search` 不可用时，它会优雅地切换到内置的 Bing 数据抓取机制。
allowed-tools:
  - execute_command
  - read_file
  - write_to_file
  - web_search    # Optional — if unavailable, use scripts/web_search_fallback.py instead
  - web_fetch
---
# 反SEO深度消费者研究工具

> 详细规则、评分标准及类别示例，请参阅 `references/SKILL_REFERENCE.md`。

## 工具可用性及优雅降级

该工具与 `web_search` 和 `web_fetch` 配合使用效果最佳，但 `web_search` 是可选的。如果您的环境中没有 `web_search`（例如未配置API密钥），工具会自动降级为使用内置的Bing爬虫脚本。

### 检测（在技能启动时执行）

在开始任何研究步骤之前，首先确定使用哪种搜索模式：

1. **全模式**（推荐）：如果您的环境中可用 `web_search`，请直接使用它来执行所有搜索操作（如下工作流程所示）。
2. **回退模式**：如果 `web_search` 不可用（工具缺失、未配置API密钥或返回错误），则对所有搜索操作使用内置的回退脚本：

```bash
# 例如：不要使用 `web_search("电竞椅 推荐 避坑 2025")`
# 而应使用：
python scripts/web_search_fallback.py "电竞椅 推荐 避坑 2025" --count 10 --days 365

# 例如：不要使用 `web_search("site:reddit.com office chair review")`
# 而应使用：
python scripts/web_search_fallback.py "office chair review" --site reddit.com --count 10

# 多网站搜索（分别搜索每个网站）：
python scripts/web_search_fallback.py "电竞椅 推荐" --sites zhihu.com,v2ex.com,smzdm.com --count 5

# 一次搜索同时获取内容（减少往返次数）：
python scripts/web_search_fallback.py "电竞椅 避坑" --count 10 --fetch-content --fetch-limit 3
```

回退脚本以DuckDuckGo HTML搜索作为主要引擎（最可靠，无验证码要求），Bing HTML作为自动备选方案——**无需API密钥**。它输出的JSON格式与 `web_search` 的结果相同。

### 回退模式下的工作流程调整

在回退模式下，整个工作流程均需进行以下调整：

| 原始模式（全模式） | 回退模式替代方案 |
|---|---|
| `web_search("query")` | `python scripts/web_search_fallback.py "query" --count 10` |
| `web_search("site:xxx.com query")` | `python scripts/web_search_fallback.py "query" --site xxx.com` |
| 第2c步：AI使用`web_search`进行论坛搜索 | 使用`platform_search.py`并设置`--dual-window --append-year`参数 |
| 第4.5步：AI使用`web_search`进行安全事件搜索 | 使用`deep_dive_search.py`并设置`--safety-only`参数 |

**重要提示**：即使在回退模式下，`web_fetch` 仍用于获取特定页面内容。只有 `web_search` 被替换。

**其他所有步骤（可信度评分、冲突解决、品牌评分、报告生成）在两种模式下均相同**——无论搜索结果如何获取，这些步骤的处理方式都保持一致。

## 架构概述

**语言检测 → AI类别适配 → AI多层搜索（论坛帖子 + 电子商务评论 + 社交评论区） → 脚本评分 → AI语义分析 → 动态多维度评分 → 报告**

- **语言与地区层**：从查询中检测用户的语言，生成特定地区的平台配置、搜索模板和关键词字典。
- **类别层**：AI生成 `category_profile` JSON（评估维度/权重/痛点关键词/安全风险/平台权重/电子商务搜索策略）。
- **搜索层**（三个数据源）：
  - **L1 电子商务评论层**（最高优先级）：间接搜索真实买家评论（例如亚马逊评论、京东后续评论，具体取决于地区）。
  - **L2 社交评论区层**（第二优先级）：在促销帖子的评论区搜索“辟谣”类反馈。
  - **L3 论坛帖子层**（传统方式）：AI使用 `web_search`（或在 `web_search` 不可用时使用 `web_search_fallback.py`）+ `site:` 进行针对性社区搜索。
- **评分层**：`credibility_scorer.py`（正则表达式预过滤 + 类别信号注入 + 数据源权重）→ `ai_credibility_analyzer.py`（AI深度分析，评分范围30-85）。
- **多维度评分**：`brand_scorer.py`（来自配置文件的维度/权重，安全评分根据类别调整）。
- **报告层**：`generate_report.py`（动态表格标题 + 数据源分布统计，基于配置文件中的维度定义）。

## 多语言与多地区适配

**核心原则**：该工具可适应任何语言和地区。AI会根据用户的查询检测其语言，并在 `category_profile` 中动态生成所有特定地区的配置。

### 语言检测规则

1. 检测用户查询的语言（中文、英文、日文等）。
2. 从上下文推断目标市场/地区（例如，中文查询 → 中国市场；英文查询关于“最佳吸尘器” → 可能指向美国/英国市场；日文查询 → 日本市场）。
3. 所有后续的搜索查询、关键词和报告文本必须与检测到的语言和地区相匹配。
4. 如果用户明确提及某个地区（例如，“在英国有售”、“在亚马逊日本站有售”），则无论查询语言如何，都使用该地区的相关信息。

### 地区平台映射

AI必须根据检测到的地区生成相应的平台配置。以下是参考映射（AI应根据实际可用性和相关性进行调整）：

**中国（zh-CN）**：
| 层级 | 平台 | 示例 |
|------|-----------|----------|
| L1 电子商务 | JD.com、淘宝、拼多多 | 评论聚合帖子、后续评论 |
| L2 社交评论 | 小红书、知乎 | 促销帖子下的“辟谣”评论 |
| L3/L4 论坛 | V2EX、Chiphell、NGA、百度贴吧、SMZDM、豆瓣、哔哩哔哩 | 社区讨论、深度评论 |

**美国 / 英语国家（en-US）**：
| 层级 | 平台 | 示例 |
|------|-----------|----------|
| L1 电子商务 | 亚马逊、百思买、沃尔玛 | 经过验证的购买评论、长期评论 |
| L2 社交评论 | Reddit、YouTube评论 | 评论区中辟谣 sponsored 内容的评论 |
| L3/L4 论坛 | Reddit（子版块）、Head-Fi、AVSForum、Wirecutter 评论、Slickdeals | 社区讨论、爱好者评论 |

**日本（ja-JP）**：
| 层级 | 平台 | 示例 |
|------|-----------|----------|
| L1 电子商务 | Amazon.co.jp、Rakuten、Kakaku.com | 购买评论、价格比较评论 |
| L2 社交评论 | Twitter/X、note.com 评论 | 促销内容下的真实用户反馈 |
| L3/L4 论坛 | Kakaku.com 论坛、5ch、Price.com | 社区讨论、专家评论 |

**韩国（ko-KR）**：
| 层级 | 平台 | 示例 |
|------|-----------|----------|
| L1 电子商务 | Coupang、Naver Shopping | 购买评论 |
| L2 社交评论 | Naver Blog 评论、Instagram | 真实用户反馈 |
| L3/L4 论坛 | DC Inside、Naver Cafe、Clien | 社区讨论 |

**欧洲（多种语言）**：
| 层级 | 平台 | 示例 |
|------|-----------|----------|
| L1 电子商务 | 亚马逊（地区版本）、Trustpilot | 购买评论、信任评分 |
| L2 社交评论 | Reddit、YouTube、地区性社交平台 | 评论区反馈 |
| L3/L4 论坛 | 地区性论坛、Reddit（子版块） | 社区讨论 |

### 地区监管机构

安全事件搜索必须包含目标地区的正确监管机构：

| 地区 | 监管机构 |
|--------|-------------------|
| 中国 | 国家市场监督管理总局（SAMR）、国家食品药品监督管理总局（CFDA） |
| 美国 | 美国食品药品监督管理局（FDA）、美国消费品安全委员会（CPSC）、联邦贸易委员会（FTC） |
| 欧盟 | 欧洲食品安全局（EFSA）、欧洲化学品管理局（ECHA）、各国监管机构 |
| 日本 | 厚生劳动省（MHLW）、公正交易委员会（CAA）、日本贸易促进机构（NITE） |

### 地区营销信号适配

每个地区都有不同的营销手段。AI必须在 `category_profile` 中生成适合该地区的营销信号：

**中国**：SEO营销关键词（例如“中高/低价”模式）、虚假评论迹象、微信营销模式。
**美国/英国**：联盟链接标识、赞助内容声明、亚马逊的激励性评论模式、影响者披露信号。
**日本**：隐蔽营销（ステマ）迹象、公关文章模式、联盟博客信号。
**通用**：过度使用最高级形容词、无缺陷描述、品牌官方语言的重复使用。

## 数据源层级策略

**问题**：过度依赖搜索引擎可索引的“帖子类型”内容（论坛答案、评论文章），这些内容的广告与内容比例较高。电子商务平台的真实购买评论和社交平台的评论区反馈具有更高的信息密度，但人工造假的成本较高，且无法被搜索引擎直接索引。

**解决方案**：使用间接搜索策略（搜索“评论汇总帖子”、“后续评论摘要”、“负面评论汇总”等）来获取电子商务评论和评论区数据。

| 数据源层级 | 来源 | 核心价值 | 基础可信度权重 |
|-----------------|--------|------------|------------------------|
| L1 电子商务评论 | 平台购买评论（间接获取） | 真实买家、长期后续评论 | 0.85 |
| L2 评论区 | 社交平台评论区（间接获取） | 关于促销内容的真实“辟谣”反馈 | 0.75 |
| L3 论坛帖子 | 社区论坛（按地区划分） | 爱好者的深度体验、比较内容 | 使用 `platform_relevance` 进行权重调整 |
| L4 独立帖子 | 问答平台、评论网站 | 系统化的评论框架 | 使用 `platform_relevance` 进行权重调整 |

**关键限制**：电子商务评论层和评论区层的搜索占比不得低于总搜索量的30%。

## 工作流程（7个步骤）

### 第1步：交互式需求确认

**核心原则**：研究一旦开始就不能中断（耗时且需要大量资源），因此必须在开始前确认所有需求。多问一个问题总比朝错误的方向进行研究要好。

**必问确认项（必须询问用户）**：
- **目标类别**：用户想购买什么？——切勿自行假设类别。
- **预算范围**：价格范围是多少？——切勿使用默认预算。
- **核心使用场景或痛点**：主要目的是什么？什么最重要？——切勿自行假设用户需求。

**条件性确认项（相关时主动询问）**：
- 当存在显著版本/渠道差异时（例如，国内版本与进口版本、地区版本）→确认用户对版本的偏好。
- 当品牌偏好明显时 → 确认是否需要限制在特定品牌内。
- 当用户需求不明确时 → 使用多项选择题进行确认。

**确认格式**：使用简短的多项选择题或开放式问题，最多3个问题。

**确认后，输出 `task_config`（供后续步骤参考）**：

```json
{
  "category": "类别名称",
  "budget_min": 2500,
  "budget_max": 3500,
  "currency": "USD",
  "locale": "en-US",
  "core_scenario": "游戏",
  "pain_points": ["冷却效果", "帧率稳定性"],
  "excluded_brands": [],
  "preferred_brands": [],
  "variant_preference": "",
  "special_requirements": []
}
```

**仅当所有条件都满足时才跳过确认**：
1. 类别明确（例如：“推荐一款200美元的游戏键盘”）。
2. 预算明确（有具体数字或明确范围）。
3. 使用场景明确（例如：“用于游戏”、“用于我的孩子”）。

### 第1.5步：AI类别适应性分析

**在搜索之前**，生成 `category_profile` JSON，严格遵循以下结构：

```json
{
  "category": "<类别名称>",
  "category_type": "<食品|耐用商品|电子产品|个人护理|服务|其他>",
  "locale": "<语言代码，例如 en-US, zh-CN, ja-JP>",
  "language": "<语言代码，例如 en, zh, ja>",
  "currency": "<货币代码，例如 USD, CNY, JPY>",
  "evaluation_dimensions": [
    {"name": "维度名称", "weight": 0.25, "description": "描述", "key_parameters": ["参数1"], "data_sources": ["source"] }
  ],
  "pain_point_keywords": {"safety": [], "quality": [], "experience": [], "trust": [] },
  "safety_risk_types": {"critical": [], "high": [], "medium": [], "low": [] },
  "platform_relevance": {
    "<平台键>": <权重 0.0-1.0>, "...": "..."
  },
  "regional_platforms": {
    "<平台键>": {
      "name": "<平台名称>", "site": "<域名>", "description": "<平台描述>", "base_weight": 0.8
    }
  },
  "category_positive_signals": [{"pattern_description": "描述", "regex_hint": "正则表达式", "score": 15, "label": "标签"} ],
  "has_variant_issue": false,
  "variant_types": [],
  "variant_search_keywords": [],
  "non_commercial_indicators": [],
  "commercial_bias_sources": [],
  "regulatory_authorities": ["<该地区的相关监管机构]",
  "marketing_signals": {
    "high_neg": ["<地区特定的营销关键词/短语"]",
    "medium_neg": ["<地区特定的促销模式"]",
    "low_neg": ["<地区特定的点击诱饵模式"] |
  },
  "authenticitysignals": {
    "long_term_use": ["<地区特定的长期使用短语，例如‘使用了6个月’、‘半年使用感受’"],
    "defect_description": ["<地区特定的缺陷/投诉术语"]",
    "purchase_proof": ["<地区特定的购买证明术语，例如‘已购买’"],
    "time_units": ["<地区特定的时间表达方式"] |
  },
  "ecommerce_search_strategy": {
    "enabled": true,
    "primary_platforms": ["<适合该地区的电子商务平台"]",
    "search_templates": {
      "review_aggregation": "[产品] <适合该地区的评论搜索术语]",
      "negative_reviews": "[产品] <适合该地区的负面评论搜索术语]",
      "long_term_reviews": "[产品] <适合该地区的长期评论搜索术语]" |
    },
    "high_value_indicators": ["<适合该地区的后续评论指标"]",
    "low_value_indicators": ["<适合该地区的虚假/激励性评论指标"] |
  },
  "comment_section_strategy": {
    "enabled": true,
    "primary_platforms": ["<适合该地区的社交平台"]",
    "search_templates": {
      "debunk_feedback": "[产品] <适合该地区的辟谣搜索术语]",
      "experience_sharing": "[产品] <适合该地区的真实体验搜索术语]" |
    },
    "high_value_indicators": ["<适合该地区的真实评论指标"]",
    "low_value_indicators": ["<适合该地区的虚假评论指标"] |
  },
  "safety_search_config": {
    "general_keywords": ["<适合该地区的召回/安全术语"]",
    "regulatory_keywords": ["<适合该地区的监管术语"]",
    "source_domains": ["<适合该地区的监管/新闻域名"] |
  },
  "report_labels": {
    "recommend": "<地区语言的推荐标签>",
    "conditional_recommend": "<地区语言的条件推荐标签>",
    "caution": "<地区语言的警告标签>",
    "avoid": "<地区语言的避免标签>",
    "high_credibility": "<地区语言的高可信度标签>",
    "medium_credibility": "<地区语言的中等可信度标签>",
    "low_credibility": "<地区语言的低可信度标签>",
    "suspected_ad": "<地区语言的疑似广告标签>",
    "sufficient": "<数据充分性标签>",
    "mostly_sufficient": "<基本充分标签>",
    "insufficient": "<数据不足标签>",
    "severely_insufficient": "<严重不足标签>" |
  }
}
```

**限制**：3-6个维度，每个维度的权重最大为0.4，各维度权重总和为1.0。平台权重根据类别进行调整。搜索模板中的 `[产品]` 占位符在搜索时会被替换为实际产品名称。

**重要提示**：`regional_platforms`、`marketing_signals`、`authenticitysignals`、`ecommerce_search_strategy`、`comment_section_strategy`、`safety_search_config` 和 `report_labels` 字段均由AI根据检测到的地区语言动态生成。这些内容必须使用用户的语言，并适用于用户所在的地区。脚本会从配置文件中读取这些信息，而不是使用硬编码的默认值。

### 第2步：多层数据源搜索（包括电子商务 + 评论区 + 结果适配）

从最高优先级的数据源开始，逐步向下搜索，确保高价值的数据源得到充分覆盖。

#### 第2a步：电子商务评论间接搜索（L1，占总量的≥15%）

电子商务平台的评论是动态加载的——搜索引擎无法直接索引它们。使用 `ecommerce_search_strategy.search_templates` 中的间接搜索策略。

将结果标记为 `source_layer: "L1_ecommerce"`，`base_weight: 0.85`。

#### 第2b步：社交评论区间接搜索（L2，占总量的≥15%）

在评论区搜索真实的“辟谣”类反馈。使用 `comment_section_strategy.search_templates` 中的模板。

将结果标记为 `source_layer: "L2_comment_section"`，`base_weight: 0.75`。

#### 第2c步：论坛帖子 + 独立帖子搜索（L3/L4，占总量的≤70%）

**全模式**：使用 `web_search` 和 `site:` 在 `regional_platforms` 中进行针对性搜索。
**回退模式**：使用 `python scripts/platform_search.py` 或 `python scripts/web_search_fallback.py --site [域名]`。

**搜索平衡策略**：40% 中立内容 + 20% 正面内容 + 40% 负面内容。

**双时间窗口**：每个搜索组结合当前年份（即时窗口）和不限年份的历史窗口。

**平台优先级**：按 `platform_relevance` 权重排序，排除权重低于0.2的平台。

**搜索关键词构建**（使用用户的语言）：
- 中立内容：`[产品] [类别] 评论比较 [关键参数]`
- 正面内容：`[产品] [类别] 长期使用 满意推荐`
- 负面内容：`[产品] [类别] [痛点关键词/质量/体验/信任]`

**搜索结果适配**：

| 是否充分 | 条件 | 策略 |
|-------------|-----------|----------|
| 充分 | 总计 ≥30 且每个产品至少有5条评论 | 按正常流程进行搜索 |
| 基本充分 | 总计 ≥15 且某个产品评论不足 | 补充搜索不足的产品 |
| 不充分 | 总计 <15 或多个产品评论不足 | 移除相关平台，扩大时间范围，增加搜索范围 |
| 严重不足 | 总计 <8 | 进入小众类别模式：降低评分标准，并在报告中注明数据限制 |

```bash
python scripts/platform_search.py "[查询]" --adaptive \
    --candidate_products "产品A,产品B,产品C" \
    --category-profile category_profile.json
```

### 第3步：内容获取与分析

使用 `web_fetch` 获取有价值的帖子（包含使用时长、多人讨论信息，标题中不含营销关键词）。

### 第3.5步：类别参数结构化提取

根据 `evaluation_dimensions[].key_parameters` 提取候选产品的结构化参数表。

### 第4步：深度挖掘（包括电子商务评论）

针对高频产品模型，使用 `pain_point_keywords` 中的关键词执行负面评论的深度搜索。

**电子商务评论深度挖掘**：对于每个候选产品，使用配置文件中的模板执行额外的电子商务评论搜索。

```bash
python scripts/deep_dive_search.py --auto-extract results.json --days 730 \
    --category-profile category_profile.json \
    --ecommerce-dive
```

### 第4.5步：安全事件搜索

**对于每个候选品牌**，在网络上搜索安全事件。分为两个层次：一般层（召回/退货/下架）和类别层（`safety_risk_types`）。使用 `safety_search_config` 中的关键词。

```bash
python scripts/deep_dive_search.py "[品牌]" --days 365 \
    --category-profile category_profile.json
```

### 第5步：可信度评估

```bash
python scripts/credibility_scorer.py results.json --v2 --output scored.json --threshold 40 \
    --category-profile category_profile.json
```

**评分架构**：正则表达式预过滤 → 类别信号注入（来自配置文件）→ AI语义分析（评分范围30-85）→ 权重融合

### 第5.5步：证据冲突仲裁

当同一产品在不同来源收到相互矛盾的评论时：

```bash
python scripts/conflict_resolver.py scored.json \
    --category-profile category_profile.json \
    --output conflicts.json
```

仲裁规则：非商业来源的评论优先于商业来源的评论；长期反馈优先于短期反馈；高可信度的评论优先于低可信度的评论。

### 第6步：多维度评分

```bash
python scripts/brand_scorer.py scored.json \
    --category-profile category_profile.json \
    --safety-results safety.json \
    --output scores.json
```

| 评分 | 判断结果 |
|-------|---------|
| ≥70 | 推荐（使用 `report_labels.recommend`） |
| 55-69 | 条件推荐（使用 `report_labels.conditional_recommend`） |
| 40-54 | 警告（使用 `report_labels.caution`） |
| <40 | 避免（使用 `report_labels.avoid`） |

**安全评分阈值**：食品（30）> 个人护理（25）> 电子产品（20）> 耐用商品（15）

### 第7步：报告生成

```bash
python scripts/generate_report.py scored.json \
    --query "[类别]" --budget [预算] --pain-point "[痛点]" \
    --category-profile category_profile.json \
    --brand-scores scores.json \
    --output report.md
```

**报告必须使用用户的语言编写**（根据 `category_profile.language` 的设置）。所有章节标题、判断结果、标签和分析文本都必须使用用户的语言。

## 关键规则（不可跳过）

1. **在搜索前确认需求**——预算、类别和使用场景都是必问项；如果缺少任何信息，请务必询问用户。
2. **切勿自行假设用户需求**——如果用户只要求“推荐一款手机”但没有提供预算或使用场景，请先询问清楚。
3. **在搜索前生成 `category_profile`——这是后续所有步骤的基础。
4. **进行两次搜索**——在广泛搜索后，务必对高频产品进行针对性的深度挖掘。
5. **在搜索中包含年份**——包括当前年份和上一年的数据。
6. **负面评论的比例必须≥40%**——积极寻找负面评论；如果找不到负面评论，说明搜索深度不够。
7. **必须搜索安全事件**——顶级推荐品牌必须通过安全事件筛查。
8. **调整搜索结果**——如果数据不足，扩大搜索范围；如果数据过多，则进行筛选。
9. **高参与度的内容需要仔细审核**——高点赞/评论数量并不代表内容的真实性（适用于知乎、Reddit等平台）。
10. **优先考虑长期反馈**——“使用了2年”比“刚购买”更有参考价值。
11. **交叉验证是核心**——商业评论好评与小众论坛的负面评价相互印证时，以小众论坛的评价为准。
12. **配置文件是唯一的知识来源**——脚本中的硬编码值仅作为备用方案。
13. **必须包含电子商务评论**——每项研究都必须包含电子商务评论（L1层），占比至少为15%。
14. **必须包含评论区内容**——每项研究都必须包含社交评论区的搜索（L2层），占比至少为15%。
15. **后续评论优于开箱评测**——长期后续评论（超过3个月）比开箱评测更有参考价值。
16. **评论区内容优先**——评论区中的真实“辟谣”反馈比帖子本身的结论更具参考价值。
17. **所有内容都必须使用用户的语言**——所有搜索查询、评分标签和最终报告都必须使用用户的语言。