---
name: hiarthur
description: 搜索亚马逊产品，分析相关材料、设计信息以及用户评价，以发现潜在的权衡因素和可能存在的不足之处。所有搜索结果均通过交互式图形用户界面（GUI）呈现。
---
# HiArthur：产品搜索与分析功能

## 概述

这是一个支持智能产品搜索和深度产品分析的双端点API。产品数据来源于亚马逊，但搜索结果远超亚马逊直接提供的内容——每个产品都会通过结合计算机视觉、大型语言模型（LLM）和符号推理的多阶段流程进行分析，以评估该产品与用户需求的匹配程度以及可能存在的不足之处。

- `POST https://hiarthur.com/api/agents/search` — 根据查询条件查找产品。每个搜索结果都会通过视觉分析和语言模型进行评估，而不仅仅是简单的关键词匹配。
- `POST https://hiarthur.com/api/agents/product` — 对单个产品进行深入分析，包括故障模式分析（FMEA）、功能总结和评价生成。该过程会利用语言模型对产品详情和图片进行处理，以揭示潜在的问题或不足之处。

基础URL：`https://hiarthur.com/api`

搜索结果可以选择通过图形用户界面（GUI）展示（例如：`https://hiarthur.com/c/<conversation_id>` 或 `https://hiarthur.com/product/f7e2a9c1b3d4`），用户可以在其中直观地浏览结果并继续交互式对话。

---

## 适用场景

当您需要以下操作时，可以使用此功能：
- 找到符合用户详细需求的产品
- 比较不同产品之间的优缺点
- 识别产品的耐用性或设计缺陷
- 了解产品为何可能让买家失望
- 超出简单评分或关键词范围来评估产品

## 快速入门：端到端流程

### 第1步 — 启动新搜索

```json
POST /api/agents/search

{
  "type": "new",
  "search_query": "noise cancelling headphones for travel",
  "search_top_brands": true
}
```

响应：

```json
{
  "conversation_id": "a1b2c3d4-...",
  "logical_search_id": "ls_abc123",
  "products": [
    {
      "product": {
        "description": "Sony WH-1000XM5 Wireless Noise Canceling Headphones",
        "brand": "Sony",
        "location": "product/f7e2a9c1b3d4",
        "price": 328.0,
        "rating": 4.6,
        "reviews_count": 12450
      },
      "explainer": "Strong noise canceling with long battery life, well suited for travel.",
      "match_grade": "Excellent"
    }
  ],
  "can_fetch_more": true
}
```

### 第2步 — 获取更多结果（分页）

请严格按照返回的`conversation_id`和`logical_search_id`进行请求。

```json
POST /api/agents/search

{
  "type": "continue",
  "conversation_id": "a1b2c3d4-...",
  "logical_search_id": "ls_abc123"
}
```

当`can-fetch_more`为`true`时，重复此步骤。如果返回`products: []`，表示还可以获取更多结果；当`can-fetch_more`为`false`时，表示搜索结束。

### 第3步 — 深入分析产品

使用搜索返回的`product.location`值进行后续操作。

```json
POST /api/agents/product

{
  "location": "product/f7e2a9c1b3d4"
}
```

响应：

```json
{
  "fmea": {
    "unmitigated_failure_modes": [
      {
        "failure_name": "Headband cushion flattens over time",
        "likelihood": {
          "level": "medium",
          "reasoning": "Foam compression builds with daily wear, so most regular users will notice reduced comfort within months."
        },
        "impact": "annoying",
        "timeline": "within_a_year",
        "summary": "The headband padding can compress with regular use, making the headphones less comfortable for long listening sessions.",
        "evidence": [
          "Foam headband cushion visible in images",
          "No mention of memory foam or replaceable pads"
        ]
      }
    ],
    "mitigated_failure_modes": [
      {
        "failure_name": "Poor noise canceling on wind",
        "ownership_experience": "Multipoint wind-noise reduction",
        "reasoning": "Multiple microphones and adaptive ANC algorithms reduce wind interference compared to single-mic designs.",
        "evidence": [
          "Adaptive ANC with multiple external microphones",
          "Wind noise reduction mode listed in features"
        ]
      }
    ],
    "quality_summary": "These headphones prioritize audio quality and noise canceling performance. Most disappointment comes from comfort degradation over time rather than core functionality."
  },
  "features_summary": "Paragraph summarizing key product features based on listing data.",
  "reviews_summary": "Paragraph synthesizing themes and patterns from customer reviews."
}
```

---

## 搜索端点 — 完整字段参考

### 新搜索（`type: "new"`）

包含所有可选字段的完整示例：

```json
{
  "type": "new",
  "search_query": "noise cancelling headphones for travel",
  "search_top_brands": true,
  "trim_query": "Over-ear wireless headphones with active noise canceling and long battery life for airplane use",
  "brands": ["Sony", "Bose"],
  "search_filters": {
    "price_min": 100,
    "price_max": 400,
    "rating_min": 4.0,
    "reviews_min": 500
  },
  "search_sort": "relevance"
}
```

| 字段 | 类型 | 是否必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `type` | `"new"` | 是 | — | 用于区分新的搜索请求。 |
| `search_query` | 字符串 | 是 | — | 用于向产品目录发送的搜索查询。查询应精确且符合用户意图，包含所有关键属性（如颜色、尺寸、材质、用途、性别等）。 |
| `search_top_brands` | 布尔值 | 是 | — | 当设置为`true`时，搜索结果将限制在指定类别内的顶级品牌范围内。电子产品、家电、服装、工具、美妆和家居/厨房用品默认设置为`true`；书籍和媒体产品默认设置为`false`。 |
| `trim_query` | 字符串 | 否 | 与`search_query`相同 | 用于过滤相似度较低的产品。该查询应描述性更强，包含丰富的属性信息，有助于匹配产品标题和图片。 |
| `conversation_id` | UUID字符串 | 否 | 由服务器生成 | 可省略，以便服务器创建新的搜索会话；如需将此搜索与现有会话关联，请提供`conversation_id`。 |
| `brands` | 字符串数组 | 否 | `[]` | 明确指定品牌名称。请使用规范的大写形式（例如：`["Nike", "Adidas"]`）。 |
| `search_filters` | 对象 | 否 | `null` | 所有子字段均为可选且可空：`price_min`（数字）、`price_max`（数字）、`rating_min`（数字）、`reviews_min`（整数）。不允许添加额外的字段。 |
| `search_sort` | 枚举字符串 | 否 | `null` | 可选排序方式：`"relevance"`、`"price_low"`、`"price_high"`或`"best_sellers"`。 |

#### `search_query` 与 `trim_query` 的区别

- `search_query` 用于从产品目录中获取广泛的产品列表。
- `trim_query` 在获取结果后作为相似度过滤器使用，用于剔除与查询内容相似度较低的产品。

`trim_query` 应该是一个描述性较强、包含丰富属性的产品描述，例如：
- “一款由闪亮金属材质制成的男士无袖连帽背心，前面配有全拉链。”
- “一盒12瓶装的巧克力味蛋白奶昔，每瓶含20克蛋白质。”
- “一款厚实的紫色瑜伽垫，采用防滑泡沫材质，厚度为一英寸。”
- “一款10英寸的不粘煎锅，带有陶瓷涂层和兼容感应炉的底座。”
- “一款支持蓝牙5.3标准的无线耳机，具备降噪功能，电池续航时间至少40小时。”

如果省略`trim_query`，系统将使用`search_query`作为默认值。只有在您有更详细的描述时才需要设置它。

### 继续搜索（`type: "continue"`）

| 字段 | 类型 | 是否必填 | 说明 |
| --- | --- | --- |
| `type` | `"continue"` | 是 | 用于表示继续当前搜索请求。 |
| `conversation_id` | UUID字符串 | 是 | 必须与之前的搜索请求中的`conversation_id`相同。 |
| `logical_search_id` | 字符串 | 必须与之前的搜索请求中的`logical_search_id`相同。 |

### 搜索响应

```json
{
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "logical_search_id": "ls_abc123",
  "products": [
    {
      "product": {
        "description": "Sony WH-1000XM5 Wireless Noise Canceling Headphones",
        "brand": "Sony",
        "location": "product/f7e2a9c1b3d4",
        "price": 328.0,
        "rating": 4.6,
        "reviews_count": 12450
      },
      "explainer": "Strong noise canceling with long battery life, well suited for travel.",
      "match_grade": "Excellent"
    }
  ],
  "can_fetch_more": true
}
```

| 字段 | 类型 | 说明 |
| --- | --- |
| `conversation_id` | 字符串 | 用于标识搜索会话，便于后续请求和结果展示。 |
| `logical_search_id` | 字符串 | 用于分页和继续搜索。 |
| `products` | 数组 | 包含`ProductWithExplainer`对象。可能为空（在继续搜索时仍有效）。 |
| `can-fetch_more` | 布尔值 | 表示是否还有更多结果可获取。`true`表示可以通过`continue`获取更多结果。 |

每个`products`数组元素包含以下字段：

| 字段 | 类型 | 说明 |
| --- | --- |
| `product.description` | 字符串 | 产品标题/描述。 |
| `product.brand` | 字符串或`null` | 已知的品牌名称。 |
| `product.location` | 字符串 | 产品唯一标识符（格式：`product/<cache_key>`），用于后续请求和前端展示。 |
| `product.price` | 数字或`null` | 产品价格（美元）。 |
| `product.rating` | 数字或`null` | 产品评分（例如：4.6）。 |
| `product.reviews_count` | 整数或`null` | 顾客评价数量。 |
| `explainer` | 字符串 | 说明产品匹配程度的文字说明。可能为空。 |
| `match_grade` | 字符串 | 产品匹配等级：`Excellent`、`Good`、`Partial`或`Low`。 |

### 匹配等级的含义

| 等级 | 含义 |
| --- | --- |
| **Excellent** | 所有用户需求均得到满足，所有数值限制均符合要求。 |
| **Good** | 所有关键需求均得到满足，无任何限制。 |
| **Partial** | 至少有一个关键需求未得到满足或存在矛盾，或某些数值限制未满足。 |
| **Low** | 有任何需求未得到满足，或无法评估任何需求。 |

---

## 产品详情端点 — 深度分析

### 请求

```json
{ "location": "product/<cache_key>" }
```

仅使用`/api/agents/search`返回的`location`值进行请求。切勿自行创建产品位置信息。请求时请设置`extra = "forbid"`。

### 响应

| 字段 | 类型 | 说明 |
| --- | --- |
| `fmea` | `Failure Mode and Effects Analysis`（故障模式与影响分析）对象。详见结构说明。 |
| `features_summary` | 字符串 | 概述产品的主要功能特点。 |
| `reviews_summary` | 字符串 | 从顾客评价中提取的产品亮点总结。 |

### FMEA（故障模式与影响分析）结构

`fmea`对象描述了产品可能在未来使用过程中让买家失望的情况，以故障模式的形式呈现。

- **`unmitigated_failuremodes`**：数组，通常包含3个条目，按预期遗憾的影响程度（可能性 × 影响程度 × 紧迫性）排序：
  | `failure_name` | 问题发生的简要描述。 |
  | `likelihood.level` | 可能性的等级（`low`、`medium`、`high`）。 |
  | `likelihood.reasoning` | 产品特定问题的发生概率及原因说明。 |
  | `impact` | 问题可能带来的影响（`cosmetic`、`annoying`、`performance_loss`、`unusable`）。 |
  | `timeline` | 问题可能发生的时间范围（`immediate`、`within_a_year`、`over_a_year`）。 |
  | `summary` | 关于实际使用中影响的1-2句话描述。 |
  | `evidence` | 来自产品列表、规格或图片的具体证据。 |

- **`mitigated_failuremodes`：**数组，包含0-3个条目，表示产品设计已解决的常见问题：
  | `failure_name` | 常见的问题类型。 |
  | `ownership_experience` | 对问题的积极描述（最多6个词，例如：“长线设计，便于回收”。 |
  | `reasoning` | 降低该问题的设计措施。 |
  | `evidence` | 来自产品列表的具体证据。 |

- **`quality_summary`：**一段简洁的文字，总结产品的主要风险、设计优势、问题发生的时间范围、可修复性，以及该产品可能满足或令用户失望的群体。

---

## 错误处理

| 状态 | 端点 | 原因 | 建议措施 |
| --- | --- | --- |
| `400` | `/agents/product` | 位置信息格式错误（为空、格式不正确或包含路径分隔符）。 | 请确保位置信息完全复制自搜索结果。 |
| `404` | `/agents/search`（继续搜索） | `logical_search_id`未找到或已过期。 | 重新发起搜索（`type: "new"`）。 |
| `404` | `/agents/product` | 产品缓存键或目标位置信息未找到。可能已过期。 | 重新搜索以获取最新信息。 |
| `422` | 两者 | 请求格式验证失败：缺少必填字段、类型错误或包含额外字段。 | 请修复请求体。所有请求请求都必须设置`extra = "forbid"`。 |
| `500` | 两者 | 内部错误。 | 尝试重新请求；如果问题持续存在，请报告给技术支持。 |
| `502` | `/agents/search` | 搜索后台未返回最终结果或返回了无效数据。 | 重新尝试；如果问题持续存在，可能是上游搜索服务出现故障。 |

---

## 安全规则：
1. 仅发送JSON格式的请求体。
2. 严禁添加额外的字段；所有请求请求都必须设置`extra = "forbid"`，否则系统会返回`422`错误。
3. 严禁自行创建产品位置信息，仅使用`/api/agents/search`返回的`location`值。
4. 请严格按照返回的值使用`conversation_id`、`logical_search_id`和`product.location`，不得修改或重新生成这些信息。
5. 对于`type: "new`的请求，请省略`conversation_id`，让服务器自动生成会话ID。
6. 所有端点均使用基础URL `https://hiarthur.com/api`。

## 前端展示方式：
- 在浏览器中打开`c/<conversation_id>`以在GUI中继续当前搜索会话。
- 在浏览器中打开返回的产品位置信息，查看产品详情和图片。
- 在构建URL时，请保持所有后端生成的ID和位置信息的完整性。

## 推荐的代理使用流程：
1. 调用`/agents/search`，设置`type`为`"new"`。
2. 查看返回的产品列表。
3. 如需更多搜索结果，再次调用`/agents/search`，设置`type`为`"continue`。
4. 如需对特定产品进行深入分析，调用`/agents/product`。