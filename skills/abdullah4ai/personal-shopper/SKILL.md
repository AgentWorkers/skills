---
name: personal-shopper
description: >
  **智能产品研究助手：采用Diamond Search方法论（由3个层级中的7个专业代理协同工作）**  
  **适用场景：**  
  当用户需要产品推荐、购物建议、产品对比、购买决策支持，或者询问“哪个产品更好”等问题时。  
  **不适用场景：**  
  当用户需要长期跟踪产品价格变化、处理订单问题、申请退货/退款，或进行商业市场分析时（请使用mckinsey-research工具）。  
  此外，如果用户只是进行普通的网络搜索（而非与购买相关），或者需要查看或解决已购买产品的故障问题，也不适用此功能。  
  **核心功能：**  
  - 根据用户需求，利用Diamond Search方法论从多个渠道收集相关信息。  
  - 提供清晰的产品推荐，包括最佳价格、产品可用性、替代方案以及专家意见。  
  - 确保推荐结果基于多源数据和分析，为用户提供可靠的购买决策依据。  
  **输入参数：**  
  - 产品类型  
  - 预算（可选）  
  - 使用场景  
  - 用户偏好  
  **涉及的工具：**  
  - sessions_spawn（用于创建子代理）  
  - web_search/camofox/exa（用于执行搜索）  
  - web_fetch（用于提取网页内容）
---
# 个人购物助手 — 钻石搜索（Personal Shopper — Diamond Search）

## 概述

“钻石搜索”（Diamond Search）是一种多智能体产品研究方法。它从狭窄的搜索范围开始（根据用户的需求），逐步扩展搜索范围（7个智能体从不同角度进行搜索），最终得出一个明确的推荐结果。

```
         [BRIEF]
            |
    --------+--------
    |   |    |   |
   [1] [2]  [3] [4]     ← Search Layer (parallel)
    |   |    |   |
    --------+--------
            |
        [5]   [6]        ← Expertise Layer (parallel)
            |
      [CONVERGENCE]
            |
           [7]            ← Price Layer
            |
        [OUTPUT]
```

## 优质产品的五大标准

每个推荐结果都会根据以下5个标准进行评估：

| 编号 | 标准 | 描述 |
| --- | --- | --- |
| 1 | 性能 | 能够满足特定使用场景的需求 |
| 2 | 价值 | 价格与实际性能相匹配（而非理论上的性能） |
| 3 | 可获得性 | 当地有库存，并提供保修和服务 |
| 4 | 可靠性 | 来自真实长期用户的正面评价 |
| 5 | 时效性 | 产品不会被新一代产品取代或已停产 |

## 7个智能体

| 编号 | 智能体 | 角色 | 负责的搜索层次 |
| --- | --- | --- | --- |
| 1 | 主流研究（Mainstream Research） | 搜索来源：Reddit、YouTube、Wirecutter、RTINGS | 进行广泛搜索 |
| 2 | 反偏见研究（Anti-Bias Research） | 进行反向搜索，探索替代品牌，打破信息茧房 | 进行搜索 |
| 3 | 当地市场扫描器（Local Market Scanner） | 搜索沙特阿拉伯的电商平台：Amazon.sa、noon.com、jarir.com、extra.com | 进行搜索 |
| 4 | 小众社区探索者（Niche Community Diver） | 搜索专业论坛、Facebook群组、Discord服务器 | 进行搜索 |
| 5 | 领域专家（Domain Expert） | 以专业技能评估搜索结果（不参与搜索） | 提供专家意见 |
| 6 | 最新技术追踪者（Latest Tech Tracker） | 关注新产品发布、即将推出的型号以及已停产的产品 | 提供最新技术信息 |
| 7 | 价格与优惠猎手（Price & Deal Hunter） | 寻找优惠券、返现优惠、分期付款选项以及跨平台价格比较 | 进行价格分析 |

> 有关每个智能体的详细提示和方法论，请参阅 `references/diamond-methodology.md`。

## 工具检测与分配

在启动搜索智能体之前，需要检测当前环境中可用的搜索工具，并为智能体分配合适的工具以实现最大覆盖范围。

### 可用的工具类别

| 工具 | 适用场景 | 检测方法 |
| --- | --- | --- |
| `camofox_*`（Camoufox） | 零售网站、Amazon、Google Shopping — 可绕过机器人检测 | 检查 `camofox_create_tab` 是否可用 |
| `web_search` | 快速的广泛网页搜索（使用Brave API） | 检查 `web_search` 是否可用 |
| `web_fetch` | 从特定URL提取内容 | 检查 `web_fetch` 是否可用 |
| `browser` | 通用浏览器自动化工具 | 检查 `browser` 是否可用 |
| Exa（通过mcp/mcporter） | 基于人工智能的语义搜索工具，适用于查找专业内容 | 检查 `mcporter` 或 `exa MCP` 工具是否可用 |

### 工具分配策略

为了避免重复并最大化搜索范围，将工具分配给不同的智能体：

- **智能体1（主流研究）：** 使用 `web_search` 进行广泛搜索；使用 `web_fetch` 获取评论网站的信息；使用 `camofox` 搜索YouTube和Reddit上的内容 |
- **智能体2（反偏见研究）：** 使用 `web_search` 进行反向搜索；使用Exa进行语义分析；使用 `camofox` 搜索小众网站 |
- **智能体3（当地市场扫描器）：** 使用 `camofox` 搜索沙特阿拉伯的电商平台（Amazon.sa、noon.com、jarir.com、extra.com）；如果这些网站有机器人保护机制，可使用 `web_fetch` 作为备用方案 |
- **智能体4（小众社区探索者）：** 使用Exa搜索专业论坛和Facebook群组；使用 `camofox` 搜索Discord和Facebook；使用 `web_search` 搜索小型Subreddit |
- **智能体6（最新技术追踪者）：** 使用 `web_search` 查找新产品发布信息；使用 `web_fetch` 获取科技新闻网站的内容 |
- **智能体7（价格与优惠猎手）：** 使用 `camofox` 获取电商平台的实时价格信息；使用 `web_search` 查找优惠券代码 |

如果某个工具不可用，智能体会使用下一个最佳替代工具。所有智能体都可以使用 `web_search` 和 `web_fetch` 作为基础搜索工具。

**请在每个智能体的提示中包含以下工具可用性信息：**

```
Available search tools: {list all available tools}
Preferred tools for your role: {assigned tools}
Fallback: web_search + web_fetch
```

## 嵌套子智能体模式

对于具有多个竞争选项的复杂产品，搜索层智能体（1-4）可能会生成自己的子智能体，以便并行搜索多个来源。这就是所谓的**嵌套子智能体**模式。

**何时使用嵌套子智能体：**
- 产品类别有10个以上可行的选项（例如笔记本电脑、耳机、显示器）
- 需要深入挖掘多种不同来源的信息（例如Reddit帖子、YouTube评论、Wirecutter文章）
- 当地市场需要检查4个以上的电商平台以获取实时价格信息

**示例：** 智能体1（主流研究）可能会生成以下子智能体：
- 子智能体1a：使用 `camofox` 或 `web_search` 在Reddit上搜索“{产品}”的相关推荐
- 子智能体1b：使用 `camofox` 或 `web_search` 在YouTube上搜索评论
- 子智能体1c：使用 `web_fetch` 查找Wirecutter或RTINGS上的信息

**何时不使用嵌套子智能体：** 对于简单的产品（如电缆、基本配件），或者只有2-3个选项的情况。过度并行化会浪费资源。最终是否使用嵌套子智能体由协调智能体根据产品的复杂性决定。

## 工作流程（5个阶段）

### 第1阶段：收集用户信息（顺序执行）

从用户那里收集以下信息：
- 他们需要的产品
- 预算（或“开放/灵活”）
- 主要使用场景
- 任何偏好或硬性要求
- 用户是否有初步的选择
- **首选输出语言**（默认：与用户输入的语言相同）

如果用户没有明确说明某些重要信息，请询问。不要自行猜测。

**语言处理：**
- 所有智能体的内部工作和分析均使用英语进行，以保持一致性
- 最终输出（第5阶段）将使用用户首选的语言
- 如果用户使用阿拉伯语输入，输出结果也将使用阿拉伯语；如果使用英语，则使用英语；如果用户指定了特定语言，则按照用户指定的语言输出

### 第2a阶段：搜索层（并行执行 — 4个子智能体）

使用 `sessions_spawn` 同时启动4个子智能体。每个智能体将收到：
- 团队角色（在7个智能体团队中的职责）
- 产品详细信息
- 适用于其角色的可用工具和首选工具
- 明确的输出格式要求

```python
# Spawn all 4 search agents in parallel
sessions_spawn(
  task="""You are Agent 1 (Mainstream Research) in a 7-agent product research team. 
Your teammates cover other angles — focus strictly on YOUR role.

Product: {product}
Budget: {budget}
Use case: {use_case}
User preferences: {preferences}

YOUR ROLE: Search mainstream, well-known sources for the best options.
Sources: Reddit, YouTube (detailed reviews), Wirecutter, RTINGS, Tom's Guide.

Available search tools: {available_tools}
Preferred tools: web_search for broad queries, web_fetch for review articles, camofox for Reddit/YouTube
Fallback: web_search + web_fetch

INSTRUCTIONS:
- Focus on reviews from the last 12 months
- Prefer comparative reviews over single-product reviews
- Note any clear consensus (same product recommended by multiple sources)
- If using camofox, navigate to specific review sites and extract key findings

OUTPUT FORMAT:
For each recommended product (3-5 max):
- Product name and model
- Why it's recommended
- Source(s) with URLs
- Key specs relevant to the use case
- Any noted drawbacks
""",
  label="agent-1-mainstream"
)

# Similarly spawn agents 2, 3, 4 in parallel (see reference file for full prompts)
```

**智能体2（反偏见研究）：** 使用反向搜索策略、探索不太知名的品牌、根据价格范围进行搜索、搜索专业社区的意见。目标：打破信息茧房。

**智能体3（当地市场扫描器）：** 浏览沙特阿拉伯的电商平台（Amazon.sa、noon.com、jarir.com、extra.com），检查实际价格、可用性、卖家类型和配送信息。如果可用，使用 `camofox` 获取实时价格。

**智能体4（小众社区探索者）：** 深入搜索专业论坛、小型Subreddit和Facebook群组，获取来自资深用户和专业人士的意见，而不仅仅是评论者的意见。

> 有关每个智能体的详细提示，请参阅 `references/diamond-methodology.md`。

等待所有4个子智能体完成搜索后，再继续执行后续步骤。

### 第2b阶段：专家评估层（并行执行 — 2个子智能体）

同时启动2个子智能体。这些子智能体会收到第2a阶段的综合搜索结果。

**智能体5（领域专家）：** 不参与搜索，而是以专家的身份分析搜索结果，并回答5个关键问题：
- 这些产品的规格是否真正符合用户的实际使用需求？
- 这些选项之间的实际差异是什么（而不仅仅是纸面上的差异）？
- 有些规格是否对用户来说过于复杂或不必要的？
- 如果是为自己购买，你会选择哪个产品，为什么？

**智能体6（最新技术追踪者）：** 搜索以下内容：
- 过去6个月内发布的产品
- 最近的CES/MWC/IFA展会上的新产品
- 未来3个月内即将推出的下一代产品
- 已停产或已结束生命周期的产品
- 当前产品与上一代产品的对比

> 有关完整的提示和专家评估与最新技术优先级的规则，请参阅 `references/domain-expertise.md`。

### 第3阶段：结果整合（顺序执行）

合并所有结果并应用整合规则：
1. **3/4个智能体的共识**：如果4个搜索智能体中有3个推荐相同的产品，这是一个强烈的信号——但需要确认它们没有依赖相同的原始搜索来源
2. **专家意见优先**：当智能体5的分析结果与智能体6的结果冲突时，以专家的意见为准（专家意见优先于新产品的推出）
3. **诚实原则**：如果没有更好的替代品，要如实告知用户
4. **时效性考虑**：如果智能体6发现同类产品将在几周内以更低的价格推出，要明确告知用户并让用户做出选择
5. **本地价格考虑**：某个产品可能是全球最佳选择，但在当地可能价格过高。最终选择应基于当地价格

将5个优质产品的标准应用于所有剩余的产品选项，并淘汰不符合2个以上标准的选项。

> 有关详细的整合规则，请参阅 `references/anti-bias-playbook.md`。

### 第4阶段：价格层（顺序执行 — 1个子智能体）

启动一个子智能体进行价格优化：

**智能体7（价格与优惠猎手）：** 对于每个最终候选产品，收集以下信息：
- 每个当地平台的当前价格
- 可用的优惠券和折扣信息
- 返现优惠（如银行卡、返现应用）
- 无息分期付款选项（如Tamara、Tabby）
- 如果适用，还包括以旧换新的计划
- 卖家信息：官方授权经销商或第三方卖家
- 运输费用、税费包含情况、配送时间、退货政策
- **价格对比**：比较当地价格与国际市场价格及运费

> 有关沙特市场的价格模式和电商平台详情，请参阅 `references/market-dynamics.md`。

### 第5阶段：输出结果

使用以下模板，以用户首选的语言输出最终推荐结果：

```
## Recommendation: {product_name}

### Why This Product
{Explanation grounded in the 5 Golden Product Criteria}

### Quick Comparison

| Product | Price | Platform | Rating | Note |
|---------|-------|----------|--------|------|
| ...     | ...   | ...      | ...    | ...  |

### Best Available Deal
- Platform: {platform}
- Price: {price}
- Seller: {seller_type}
- Coupon: {coupon_if_any}
- Cashback: {cashback_if_any}
- Installments: {installment_options}

### Alerts
- {timing_advice}
- {price_inversion_warning_if_any}
- {discontinuation_warning_if_any}

### Alternatives
1. {alternative_1} — {why_it's_a_good_second_choice}
2. {alternative_2} — {why_it_serves_a_different_need}

### Sources
- {list key sources with URLs used across all agents}
```

**平台格式说明：**
- 在Discord/WhatsApp上：使用项目符号列表而非Markdown表格
- 在Telegram上：表格可以正常显示，但请保持简洁
- 根据当前渠道调整格式

## 实际应用示例

**用户：**“我需要一个用于播客的USB麦克风，预算大约150美元”

**用户信息：** 产品：USB麦克风，预算：150美元，用途：播客，没有特别偏好

**搜索结果（汇总）：**
- 智能体1：Shure MV7+（249美元），Audio-Technica AT2020USB-X（129美元），Rode NT-USB Mini（99美元）
- 智能体2：Maono PD200X（79美元），Fifine K688（59美元）——这些产品规格相似，是隐藏的优质选择
- 智能体3：在Jarir.com上查到AT2020USB-X的售价为489沙特里亚尔
- 智能体4：Reddit上的r/podcasting板块一致认为AT2020USB-X是这个价格区间内的最佳选择；Maono PD200X也是性价比高的选择

**专家评估：**
- 智能体5：对于播客用途，动态麦克风（PD200X和MV7+）能更好地抑制背景噪音。AT2020是电容式麦克风，在经过处理的房间中使用效果较好，但在其他环境中可能会有问题。PD200X售价79美元，而MV7+售价249美元，但音质仅相当于PD200X的90%。
- 智能体6：没有新的产品发布。MV7+刚刚进行了更新，市场情况稳定。

**最终推荐：** PD200X在性价比上更优。如果预算允许，也可以考虑MV7+；AT2020USB-X更适合在经过处理的房间中使用。

**最终输出：** 推荐Maono PD200X，MV7+作为高级替代品。

## 参考资料

| 文件 | 阅读说明 |
| --- | --- |
| `references/diamond-methodology.md` | 需要完整的智能体提示、自定义智能体行为或根据产品复杂性调整搜索策略 |
| `references/anti-bias-playbook.md` | 需要反向搜索策略、品牌评估框架或检测信息茧房的方法 |
| `references/domain-expertise.md` | 需要专家的评估框架、实际使用案例或专家评估与最新技术的优先级规则 |
| `references/market-dynamics.md` | 需要了解沙特市场的价格模式、电商平台比较、卖家验证或价格对比方法 |

## 实施注意事项

- **智能体数量可灵活调整**：对于简单的产品（如USB电缆、手机壳），可以使用3个智能体：主流研究、当地市场和价格分析。根据决策的复杂性调整智能体的数量。
- **不要硬编码具体模型**：使用“fast model”表示搜索智能体，使用“reasoning model”表示分析智能体。让平台自动选择合适的模型。
- **每个子智能体独立工作**：搜索层智能体之间不会相互查看彼此的结果；专家评估层智能体会看到搜索结果，但不会看到其他智能体的结果。
- **超时处理**：如果某个子智能体花费太长时间，可以使用现有的结果继续执行。记录下哪个智能体的数据缺失。
- **嵌套子智能体是可选的**：仅当产品复杂性需要额外的并行处理时才使用。是否使用嵌套子智能体由协调智能体决定。

## 核心原则

> 产品的选择基于**价值**，而非**品牌**。
> 我们扩展搜索范围，以确保决策基于产品的实际价值，而不仅仅是Google上显示的结果。