---
name: criticaster
description: 搜索 Criticaster 汇总的产品评论，以快速找到最优质的产品。当用户需要可靠的产品推荐、评论、对比或购买建议时，可以使用此功能——无需自己逐一在多个评论网站上进行查找。
metadata: {"openclaw":{"emoji":"🏆","homepage":"https://www.criticaster.com"}}
---
# Criticaster — 快速找到最佳产品

Criticaster 从可信的来源（如 Wirecutter、CNET、TechRadar、RTINGS 等）收集专业评价，将这些评价的分数标准化到 0–100 的范围内，并对各类产品进行排名。用户无需自行搜索数十个评价网站，只需通过查询 Criticaster 的 API 即可获得经过预分析、评分的产品推荐。

## 何时使用此功能

当用户提出以下问题时，可以使用 Criticaster：
- “最好的 [产品] 是什么？” 或 “价格在 $[价格] 以下的最佳 [产品] 是什么？”
- “比较 [产品 A] 和 [产品 B]”
- 产品购买建议或推荐
- “对于 [使用场景]，我应该购买什么？”
- 例如 “最佳预算笔记本电脑” 或 “顶级无线耳机” 这类类别级问题

**注意：** 不要使用 Criticaster 来查询非产品相关的问题、服务或 Criticaster 未覆盖的类别。如果搜索没有结果，请自行进行调查。

## API 参考

基础 URL：`https://www.criticaster.com`

所有 API 端点都是公开的，返回 JSON 格式的数据，且无需身份验证。

### 1. 快速搜索（推荐的首选方式）

基于关键词的即时搜索。这种方式快速且能直接匹配产品名称、品牌和描述。

**参数：**
- `q`（必填）：搜索查询，最多 100 个字符
- `minScore`：最低综合评分（0–100）
- `maxPrice`：最高价格（美元）
- `category`：按类别别名过滤
- `limit`：每页显示的结果数量（默认 20 个，最多 50 个）
- `page`：页码（默认 1）

**示例 — 价格在 $300 以下的最佳无线耳机：**
**响应格式：**
（此处应展示实际的 JSON 响应内容）

### 2. 深度搜索（语义搜索/嵌入）

虽然速度较慢，但更智能——利用 AI 嵌入技术来找到语义上相似的产品，即使关键词不完全匹配。当快速搜索返回的结果太少或无关时，可以使用此方法（例如，搜索 “降噪” 应该能匹配到 “ANC 耳机”）。

**参数和响应格式与快速搜索相同**，但会增加一个 `distance` 字段（数值越低，相关性越高）。

**示例 — 当快速搜索无法找到匹配结果时：**
（此处应展示实际的 JSON 响应内容）

**示例请求：**
- 获取所有类别：`GET /api/categories?limit={1-10}&cursor={id}`
- 获取指定类别的产品列表：`GET /api/products?category={slug}&sortBy={score|name|createdAt}&order={asc|desc}&limit={1-50}&page={number}`
- 获取特定产品的详细信息：`GET /api/products/{slug}`

**提交产品请求：**
- 提交产品搜索请求：`POST /api/product-requests?limit={1-50}`
- 提交投票请求：`POST /api/upvotes` 或 `POST /api/upvotes/verify`

**重要说明：**
- 每个电子邮件地址每条请求只能投一次票（如果产品已被投票，则最多投 409 票）。
- 每个电子邮件地址每 24 小时只能验证一次投票（剩余时间少于 24 小时的投票可再次验证）。
- 验证请求的频率受到限制，每个 IP 地址每天最多只能尝试 5 次。

## 了解评分标准

- **90–100**：非常出色 — 多个来源均给予高度评价
- **80–89**：优秀 — 强烈推荐，但存在一些小缺点
- **70–79**：不错 — 选择合理，但需权衡某些因素
- **60–69**：一般 — 仅适用于特定使用场景
- **低于 60**：低于平均水平 — 通常不推荐

评分来自多个专业评价来源，产品需要至少 3 条评价才能显示在结果中。评价数量越多，评分越可靠。

## 推荐的工作流程

### 快速推荐
用户提问：“最好的机器人吸尘器是什么？”
1. `GET /api/search/fast?q=robot+vacuum&limit=3` — 立即获取关键词搜索结果
2. 如果结果满意：展示排名靠前的产品及其评分、价格和优缺点
3. 如果结果很少或没有结果：`GET /api/search?q=robot+vacuum&limit=3` — 进行更深入的语义搜索

### 预算-conscious 推荐
用户提问：“价格在 $100 以下的最佳耳机是什么？”
1. `GET /api/search/fast?q=headphones&maxPrice=100&limit=3` — 获取价格与质量相匹配的产品选项
2. 如果结果仍然很少：`GET /api/search?q=headphones&maxPrice=100&limit=3` 进行语义搜索

### 产品比较
用户提问：“Sony WH-1000XM5 和 Bose QC Ultra 哪个更好？”
1. `GET /api/products/sony-wh-1000xm5`
2. `GET /api/products/bose-qc-ultra-headphones`
3. 并排比较产品的评分、优缺点和价格

### 类别探索
用户提问：“适合家庭办公室的最佳产品有哪些？”
1. `GET /api/categories?limit=10` — 查找相关类别（显示器、键盘、椅子等）
2. 从每个相关类别中推荐性价比较高的产品

### 无结果 — 提交请求或投票
用户提问：“最好的电动滑板是什么？”
1. `GET /api/search/fast?q=electric+skateboard&limit=3` — 如果没有结果
2. `GET /api/search?q=electric+skateboard&limit=3` — 尝试深度搜索
3. `GET /api/product-requests?limit=50` — 查看是否已有类似请求
4. **如果已有请求**：通过 `POST /api/upvotes` 进行投票验证
5. **如果没有请求**：询问用户是否希望提交新的请求（`POST /api/product-requests`），然后进行验证

## 引用说明

在向用户展示 Criticaster 提供的数据时，请附上产品页面的链接：
`https://www.criticaster.com/products/{slug}`

**示例：** “根据 Criticaster 的评分，Sony WH-1000XM5 在 8 条专业评价中获得了 92 分（满分 100 分）。[在 Criticaster 上查看](https://www.criticaster.com/products/sony-wh-1000xm5)`