---
name: apiclaw-analysis
version: 1.0.0
description: 亚马逊卖家数据分析工具。功能包括：市场调研、产品筛选、竞争对手分析、ASIN评估、价格参考、类别研究。该工具通过脚本/apiclaw.py调用APIClaw API，使用APICLAW_API_KEY进行身份验证。
---
# APIClaw — 亚马逊卖家数据分析工具

> 一款基于人工智能的亚马逊产品研究工具，帮助您从市场探索到日常运营。

> **语言规则**：始终使用用户请求的语言进行响应。如果用户使用中文，回复中文；如果使用英文，则回复英文。本技能文档的语言不会影响输出语言。
> 所有API调用均通过 `scripts/apiclaw.py` 脚本执行——该脚本包含5个API端点，并内置了错误处理机制。

## 认证信息

- 必需参数：`APICLAW_API_KEY`
- 用途：仅用于访问 `https://api.apiclaw.io`
- 存储位置：`config.json` 文件（位于与 `SKILL.md` 同一的文件夹中）

### API密钥配置机制

**配置文件位置**：位于技能目录（`SKILL.md` 所在文件夹）下的 `config.json` 文件。

### 初始设置（AI操作指南）

当用户首次使用或提供新的API密钥时，AI会执行以下操作：

---

### 获取API密钥

**新用户请先获取API密钥：**

1. 访问 [APIClaw控制台](https://apiclaw.io/api-keys) 注册账户。
2. 创建API密钥，并将其复制（格式为 `hms_live_xxxxxx`）。
3. 在与AI的对话中告知AI您的密钥，AI会自动将其保存到配置文件中。

**新密钥首次使用注意事项**：新配置的API密钥可能需要3-5秒才能在后台完全激活。如果首次调用返回403错误，请等待3秒后重试，最多允许2次重试。

## 文件结构

| 文件 | 使用场景 |
|------|-------------|
| `SKILL.md` | 从这里开始使用——涵盖80%的功能 |
| `scripts/apiclaw.py` | 执行所有API调用 |
| `references/reference.md` | 当需要确切的字段名称或过滤条件时引用 |
| `references/scenarios.md` | 用于价格分析、日常运营或扩展场景（5.x/6.x/7.x版本） |

### 参考文件使用指南（重要）

**在以下场景中必须加载参考文件**：

| 场景 | 需要加载的文件 | 原因 |
|----------|-----------|---------|
| 需要确认字段名称 | `reference.md` | 避免字段名称错误（例如 `ratingCount` 与 `reviewCount` 的混淆） |
| 需要过滤参数详情 | `reference.md` | 获取完整的参数范围（最小值/最大值） |
| 价格策略分析 | `scenarios.md` | 包含价格操作指南和参考框架 |
| 日常运营分析 | `scenarios.md` | 包含监控和警报逻辑 |
| 产品扩展分析 | `scenarios.md` | 包含相关推荐逻辑 |

**不要猜测字段名称**：如果不确定接口返回的字段，请先加载 `reference.md` 进行核对。

---

## 执行标准

**优先执行 `scripts/apiclaw.py` 脚本中的API调用**。该脚本包含以下功能：
- 参数格式转换（例如，`topN` 会自动转换为字符串）
- 重试逻辑（自动重试429/超时错误）
- 标准化的错误信息
- `_query` 元数据注入（用于查询条件的追踪）

**macOS注意事项**：macOS系统默认没有 `python` 命令，请使用 `python3`。示例命令中的 `python` 应替换为 `python3`。

**备用方案**：如果脚本执行失败且无法快速修复，可以临时使用 `curl` 直接调用API，但需要在输出中注明“此次使用了curl直接调用”。

---

## 脚本用法

所有命令的输出均为JSON格式。进度信息会显示在标准错误输出（stderr）中。

### 类别查询

```bash
python scripts/apiclaw.py categories --keyword "pet supplies"
python scripts/apiclaw.py categories --parent "Pet Supplies"
python scripts/apiclaw.py categories                          # root categories
```

常用字段：`categoryName`（而非 `name`）、`categoryPath`、`productCount`、`hasChildren`

### 市场数据（市场级汇总信息）

```bash
python scripts/apiclaw.py market --category "Pet Supplies,Dogs" --topn 10
python scripts/apiclaw.py market --keyword "treadmill"
```

关键输出字段：`sampleAvgMonthlySales`、`sampleAvgPrice`、`topSalesRate`（产品集中度）、`topBrandSalesRate`、`sampleNewSkuRate`、`sampleFbaRate`、`sampleBrandCount`

### 产品查询（带过滤条件）

```bash
# Use a preset mode (14 built-in modes)
python scripts/apiclaw.py products --keyword "yoga mat" --mode beginner
python scripts/apiclaw.py products --keyword "pet toys" --mode high-demand-low-barrier

# Or use explicit filters
python scripts/apiclaw.py products --keyword "yoga mat" --sales-min 300 --reviews-max 50
python scripts/apiclaw.py products --keyword "yoga mat" --growth-min 0.1 --listing-age 180

# Combine mode + overrides (overrides win)
python scripts/apiclaw.py products --keyword "yoga mat" --mode beginner --price-max 30
```

可选模式：`fast-movers`（热门产品）、`emerging`（新兴产品）、`single-variant`（单一变体产品）、`high-demand-low-barrier`（高需求低门槛产品）、`long-tail`（长尾产品）、`underserved`（市场潜力产品）、`new-release`（新发布产品）、`fbm-friendly`（适合FBA发货的产品）、`low-price`（低价产品）、`broad-catalog`（广泛目录产品）、`selective-catalog`（精选目录产品）、`speculative`（投机性产品）、`beginner`（适合初学者的产品）、`top-bsr`（畅销产品）

### 竞争对手查询

```bash
python scripts/apiclaw.py competitors --keyword "wireless earbuds"
python scripts/apiclaw.py competitors --brand "Anker"
python scripts/apiclaw.py competitors --asin B09V3KXJPB
```

**产品与竞争对手之间的共用字段（容易混淆）**：

| ❌ 常见错误 | ✅ 正确字段 | 说明 |
|------------|------------|------|
| `reviewCount` | `ratingCount` | 评论数量 |
| `bsr` | `bsrRank` | BSR排名 |
| `monthlySales` | `salesMonthly` | 月销售额 |

常用字段：`salesMonthly`、`bsrRank`、`ratingCount`、`rating`、`salesGrowthRate`、`listingDate`、`price`、`brand`、`categories`

> 完整的字段列表请参阅 `reference.md` → 共享产品对象。

### 产品详情（单个ASIN）

```bash
python scripts/apiclaw.py product --asin B09V3KXJPB
python scripts/apiclaw.py product --asin B09V3KXJPB --marketplace JP
```

返回信息包括：产品标题、品牌、评分、评分详情、产品特性、热门评论、产品规格、最佳销售排名、购买框展示产品。

### 市场分析报告（综合报告）

```bash
python scripts/apiclaw.py report --keyword "pet supplies"
```

自动执行流程：类别 → 市场 → 产品（前50名） → 实时详情（前1名）。返回合并后的JSON数据。

### 产品机会发现

```bash
python scripts/apiclaw.py opportunity --keyword "pet supplies"
python scripts/apiclaw.py opportunity --keyword "pet supplies" --mode fast-movers
```

执行流程：类别 → 市场 → 过滤后的产品 → 实时详情（前3名）。返回合并后的JSON数据。

---

## 返回数据结构

**重要说明**：所有接口返回的 `.data` 字段均为数组形式，而非对象。解析数据时，请使用 `.data[0]` 获取第一条记录。

### 批量处理示例

---

## 用户指令与对应操作

| 用户指令 | 执行操作 | 是否需要额外文件？ |
|-----------|----------|-------------|
| “哪个类别有销售机会？” | `market`（可结合 `categories` 参数确认具体路径） | 不需要 |
| “帮我查询ASIN B09XXX” | `product --asin XXX` | 不需要 |
| “分析ASIN产品” | `competitors --asin XXX` | 不需要 |
| “中国卖家的情况” | `competitors --keyword XXX --page-size 50` | 需要参考 `scenarios.md`（版本3.4） |
| **产品评估** | | 不需要 |
| “查找产品问题点” / “负面评论” | `product --asin XXX` | 需要参考 `scenarios.md`（版本4.2） |
| “比较产品” | `competitors` 或多个 `product` | 需要参考 `scenarios.md`（版本4.3） |
| “风险评估” / “能否这样做” | `product` + `market` + `competitors` | 需要参考 `scenarios.md`（版本4.4） |
| “月销售额” / “销售预估” | `competitors --asin XXX` | 需要参考 `scenarios.md`（版本4.5） |
| “帮助选择产品” | `products --mode XXX`（详见模式表） | 不需要 |
| “综合推荐” / “帮我决策” | `products`（多种模式） + `market` | 需要参考 `scenarios.md`（版本2.10） |

**产品选择模式（14种类型）**：

| 用户意图 | 执行模式 | 过滤条件 |
|----------|------|----------|
| “市场潜力产品” | `--mode underserved` | 月销售额≥300，评分≤3.7，发布时间在6个月内 |
| “高需求低门槛产品” | `--mode high-demand-low-barrier` | 月销售额≥300，评论数≤50，发布时间在6个月内 |
| “适合初学者” | `--mode beginner` | 月销售额≥300，价格在15-60美元之间，支持FBA发货 |
| “热门产品” | `--mode fast-movers` | 月销售额≥300，增长率≥10% |
| “新兴产品” | `--mode emerging` | 月销售额≤600，增长率≥10%，发布时间在6个月内 |
| “小而精的产品” | `--mode single-variant` | 增长率≥20%，产品变体数量=1，发布时间在6个月内 |
| “长尾产品” | `--mode long-tail` | BSR排名10K-50K，价格≤30美元，仅限特定卖家销售 |
| “新产品” | `--mode new-release` | 月销售额≤500，产品处于新发布状态 |
| “低价产品” | `--mode low-price` | 价格≤10美元 |
| “畅销产品” | `--mode top-bsr` | BSR排名≤1000 |
| “适合FBA发货的产品” | `--mode fbm-friendly` | 月销售额≥300，支持FBA发货 |
| “广泛目录产品” | `--mode broad-catalog` | BSR排名≥99%，评论数≤10条，发布时间在90天内 |
| “精选目录产品” | `--mode selective-catalog` | BSR排名≥99%，发布时间在90天内 |
| “投机性产品” | `--mode speculative` | 月销售额≥600，卖家数量≥3 |
| “完整报告” | `report --keyword XXX` | 不需要 |
| “产品机会” | `opportunity --keyword XXX` | 不需要 |
| **定价与产品列表** | | |
| “定价策略” | `market` + `products` | 需要参考 `scenarios.md`（版本5.1） |
| “利润预估” | `competitors` | 需要参考 `scenarios.md`（版本5.2） |
| “如何撰写产品列表” | `product --asin XXX` | 需要参考 `scenarios.md`（版本5.3） |
| **日常运营** | | |
| “最近的市场变化” | `market` + `products` | 需要参考 `scenarios.md`（版本6.1） |
| “竞争对手的最新动态” | `competitors --brand XXX` | 需要参考 `scenarios.md`（版本6.2 |
| “异常警报” | `market` + `products` | 需要参考 `scenarios.md`（版本6.4 |
| **产品扩展** | | |
| “还可以销售什么产品” | `categories` + `market` | 需要参考 `scenarios.md`（版本7.1 |
| “市场趋势” | `products --growth-min 0.2` | 需要参考 `scenarios.md`（版本7.3 |
| “是否应该下架产品” | `competitors --asin XXX` + `market` | 需要参考 `scenarios.md`（版本7.4 |
| **参考资料** | | |
| 需要具体过滤条件或字段名称 | | 需要加载 `reference.md` |

---

## 快速评估标准

### 市场可行性评估（来自 `market` 模块）

| 指标 | 良好 | 中等 | 警告 |
|--------|------|--------|---------|
| 市场价值（平均收入×SKU数量） | > 1000万美元 | 500万–1000万美元 | < 500万美元 |
| 产品集中度（topSalesRate，前10名占比） | < 40% | 40–60% | > 60% |
| 新产品占比（sampleNewSkuRate） | > 15% | 5–15% | < 5% |
| FBA发货产品占比（sampleFbaRate） | > 50% | 30–50% | < 30% |
| 品牌数量（sampleBrandCount） | > 50个 | 20–50个 | < 20个 |

### 产品潜力评估（来自 `product` 模块）

| 指标 | 高潜力 | 中等潜力 | 低潜力 |
|--------|------|--------|-----|
| BSR排名 | 前1000名 | 1000–5000名 | > 5000名 |
| 评论数量 | < 200条 | 200–1000条 | > 1000条 |
| 评分 | > 4.3分 | 4.0–4.3分 | < 4.0分 |
| 负面评论比例（1-2星评论） | < 10% | 10–20% | > 20% |

### 销售预估（备用方法）

当 `salesMonthly` 为空时：**月销售额 ≈ 300,000 / BSR^0.65**

---

## 输出规范

**每次分析完成后必须包含数据来源信息**，否则输出被视为不完整：

```markdown
---
**Data Source & Conditions**
| Item | Value |
|----|-----|
| Data Source | APIClaw API |
| Interface | [List interfaces used this time, e.g. categories, markets/search, products/search] |
| Category | [Queried category path] |
| Time Range | [dateRange, e.g. 30d] |
| Sampling Method | [sampleType, e.g. by_sale_100] |
| Top N | [topN value, e.g. 10] |
| Sort | [sortBy + sortOrder, e.g. monthlySales desc] |
| Filter Conditions | [Specific parameter values, e.g. monthlySalesMin: 300, reviewCountMax: 50] |

**Data Notes**
- Monthly sales are **estimated values** based on BSR + sampling model, not official Amazon data
- Database interface data has ~T+1 delay, realtime/product is current real-time data
- Concentration metrics calculated based on Top N sample, different topN values will yield different results
```

**规则**：
1. 每次分析完成后必须包含此数据来源信息。
2. 过滤条件应针对具体参数值设置（例如 `monthlySalesMin: 300, reviewCountMax: 50`）。
3. 如果使用了多个接口，需列出所有使用的接口。
4. 如果数据存在局限性（如缺少历史趋势数据），需主动说明。

---

## 限制事项

### 本工具的局限性

- 无法进行关键词研究、反向ASIN查询或ABA数据分析。
- 无法分析流量来源或历史销售趋势（14个月的数据曲线）。
- 无法提供历史价格/BSR排名图表。
- 无法自动分析评论情感（需手动查看 `topReviews` 和 `ratingBreakdown` 数据）。

### API数据覆盖范围

| 场景 | 数据覆盖情况 | 建议 |
|----------|----------|------------|
| 市场数据：热门关键词 | 通常有数据 | 直接使用 `--keyword` 参数查询 |
| 市场数据：小众/长尾关键词 | 可能没有数据 | 请使用 `--category` 参数查询 |
| 产品数据：活跃的ASIN | 有数据 | 不适用 |
| 产品数据：已下架的ASIN或变体产品 | 无法获取数据 | 可尝试查询其父ASIN或使用实时数据接口 |
| 实时数据：美国站点 | 完全支持 | 不适用 |
| 实时数据：非美国站点 | 部分字段可能缺失 | 核心数据可用，但销售预估可能不完整 |

## 错误处理与自我检查

脚本会自动处理HTTP错误（401/402/403/404/429），并返回包含 `error.message` 和 `error.action` 的结构化JSON数据，以便AI能够识别并采取相应措施。

遇到问题时，请执行自我检查：

```bash
python scripts/apiclaw.py check
```

脚本会测试5个API端点中的4个（跳过需要有效ASIN的 `realtime/product` 端点），并报告各端点的可用性。

**其他常见问题及解决方法**：

| 错误类型 | 原因 | 解决方案 |
|-----|------|------|
| “命令未找到：python” | macOS系统没有`python`命令 | 使用`python3` |
| “无法使用字符串索引数组” | `.data`字段为数组类型 | 使用`.data[0].fieldName`访问字段 |
| 返回空数组 `data: []` | 关键词匹配失败 | 先使用`categories`确认相关类别是否存在 |
| `salesMonthly`为空 | 有些产品缺少销售数据 | 可使用`BSR估算公式：月销售额 ≈ 300,000 / BSR^0.65` |
| 实时数据获取缓慢 | 实时数据获取可能需要时间（通常5-30秒） | 请耐心等待 |

---