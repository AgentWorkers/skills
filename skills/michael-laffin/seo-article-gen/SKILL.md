---
name: seo-article-gen
description: 一款经过SEO优化的文章生成器，支持自动集成联盟链接功能。该工具能够基于关键词研究生成高质量、排名较高的内容，并内置结构化数据生成机制及盈利模式。
metadata:
  {
    "openclaw":
      {
        "version": "1.0.0",
        "author": "Vernox",
        "license": "MIT",
        "tags": ["seo", "content", "affiliate", "writing", "automation"],
        "category": "marketing",
      },
  }
---

# SEO-Article-Gen – 一款专为SEO优化设计的文章生成工具

**能够自动生成具有联盟营销功能的排名内容。**

## 概述

SEO-Article-Gen是一款能够生成真正具备排名能力的SEO优化文章的工具。它集成了关键词研究、人工智能写作、结构化数据生成以及自动插入联盟链接等功能，所有这些功能都集中在一个平台上。

## 主要特性

### ✅ 关键词研究
- 寻找竞争较小、搜索量较大的关键词
- 分析用户搜索意图（信息型、交易型、导航型）
- 提供关键词难度评分
- 生成相关问题（“人们也问”）
- 生成长尾关键词变体

### ✅ 人工智能驱动的写作
- 根据关键词生成完整的文章
- 优化自然语言表达
- 使用正确的标题结构（H1、H2、H3）
- 保证内容易读且引人入胜
- 控制文章字数（1,500–2,500字）

### ✅ SEO优化
- 优化标题标签和元描述
- 生成合适的URL路径
- 提供图片alt文本建议
- 建议添加内部链接
- 提供外部链接资源
- 生成Schema标记（包括文章、常见问题解答、操作指南等类型）

### ✅ 联盟营销集成
- 自动插入联盟链接
- 根据内容上下文推荐相关产品
- 遵守FTC（美国联邦贸易委员会）法规进行披露
- 优化链接以提高点击率（CTR）
- 支持收入追踪

### ✅ 内容模板
- 产品评论
- 操作指南
- 对比文章
- 列表文章（如“十大X”）
- 终极指南
- 案例研究

## 安装

```bash
clawhub install seo-article-gen
```

## 快速入门

### 生成一篇文章

```javascript
const article = await generateArticle({
  keyword: "best wireless headphones 2026",
  type: "product-review",
  wordCount: 2000,
  affiliate: true,
  network: "amazon"
});

console.log(article);
```

### 关键词研究

```javascript
const keywords = await findKeywords({
  seed: "wireless headphones",
  intent: "transactional",
  difficulty: "low",
  volume: 500
});

// Returns: [
//   { keyword: "best wireless headphones for gaming", volume: 1200, difficulty: 15 },
//   { keyword: "budget wireless noise cancelling", volume: 800, difficulty: 12 }
// ]
```

## 工具功能

### `generateArticle`
生成一篇完整的SEO优化文章。

**参数：**
- `keyword`（字符串，必填）：目标关键词
- `type`（字符串）：文章类型（产品评论、操作指南、对比文章、列表文章）
- `wordCount`（数字）：目标字数（默认：2000字）
- `affiliate`（布尔值）：是否插入联盟链接（默认：true）
- `network`（字符串）：使用的联盟网络
- `includeImages`（布尔值）：是否生成图片建议

**返回值：**
- 标题、元描述、URL路径
- 带有标题的结构化文章内容
- 关键词密度报告
- 插入的联盟链接
- Schema标记（JSON-LD格式）
- SEO评分

### `findKeywords`
搜索可用于生成内容的关键词。

**参数：**
- `seed`（字符串，必填）：起始关键词
- `intent`（字符串）：按搜索意图过滤（信息型、交易型、导航型）
- `difficulty`（字符串）：按难度过滤（低、中、高）
- `volume`（数字）：最低搜索量要求
- `limit`（数字）：最大返回结果数量（默认：20个）

**返回值：**
- 关键词对象数组，包含搜索量、难度和CPC（点击成本）数据

### `optimizeContent`
优化现有内容以提升SEO效果。

**参数：**
- `content`（字符串，必填）：需要优化的内容
- `keyword`（字符串，必填）：目标关键词
- `options`（对象）：
  - `addStructure`（布尔值）：添加合适的标题结构
  - `addMeta`（布尔值）：生成标题和元描述
  - `addInternalLinks`（布尔值）：建议添加内部链接

**返回值：**
- 优化后的内容
- SEO优化建议
- 优化前后的内容对比

### `generateSchema`
生成结构化数据标记。

**参数：**
- `type`（字符串，必填）：标记类型（文章、常见问题解答、操作指南、产品）
- `content`（对象，必填）：内容数据

**返回值：**
- JSON-LD格式的Schema标记
- 标记验证结果

### `analyzeCompetitors`
分析目标关键词排名靠前的竞争对手。

**参数：**
- `keyword`（字符串，必填）：目标关键词
- `topN`（数字）：返回的竞争对手数量（默认：5个）

**返回值：**
- 竞争对手的URL
- 文章字数分析
- 标题结构
- 共用的关键词
- 可利用的内容差距

## 使用场景

### 产品评论文章
生成包含联盟链接的全面产品评论：
- 优点/缺点部分
- 对比表格
- 购买指南
- 用户评价

### 操作指南
创建易于排名的操作指南：
- 逐步说明
- 专家建议
- 所需工具/产品（附带联盟链接）
- 常见错误

### 列表文章
生成“最佳X产品”类型的文章：
- 产品推荐
- 对比表格
- 价格信息
- 每个产品都附带联盟链接

### 案例研究
通过真实案例建立权威性：
- 优化前后的效果展示
- 方法论说明
- 使用的工具（可盈利）
- 专家引用

## 文章结构

所有生成的文章都遵循SEO最佳实践：

```
H1: Optimized Title
- Meta Description (155-160 chars)
- Featured Image Alt Text

H2: Introduction
- Hook paragraph
- Problem statement
- What readers will learn

H2: [Main Content Section]
- In-depth explanation
- Bullet points for readability
- Statistics/data where applicable

H2: [Affiliate Product Recommendation]
- Product description
- Key features
- Pros/cons
- CTA with affiliate link
- FTC disclosure

H2: Comparison (optional)
- Side-by-side comparison
- Pricing table
- Use cases

H2: FAQ
- 5-7 common questions
- Concise answers
- Schema markup

H2: Conclusion
- Key takeaways
- Final recommendation
- CTA

Schema: Article + FAQ
```

## SEO评分标准

生成的文章会根据以下方面进行评分：

- **标题优化**（20分）：关键词的使用、长度、吸引力
- **元描述**（15分）：关键词的包含情况、点击潜力
- **标题结构**（15分）：H2/H3标题的层次结构、关键词的使用
- **内容质量**（25分）：易读性、深度、原创性
- **关键词使用**（15分）：关键词的密度和自然分布
- **内部/外部链接**（5分）：链接的布局和相关性
- **Schema标记**（5分）：正确的JSON-LD实现

**评分标准：**
- 90-100分：优秀（很可能排名靠前）
- 80-89分：良好（需要少量改进）
- 70-79分：一般（需要优化）
- 70分以下：较差（需要大幅改进）

## 联盟营销集成

文章会自动包含以下内容：
1. **产品推荐**：
   - 根据内容上下文推荐相关产品
   - 提供价格对比
   - 突出产品特点
2. **策略性链接布局**：
   - 在高点击率产品上方放置链接
   - 在产品内部设置对比内容
   - 设置明确的行动号召（CTA）
3. **FTC披露**：
   - 自动插入披露信息
   - 符合平台规定
   - 遵守FTC法规

## 价格方案

- **免费**：每月5篇文章（每篇最多1,500字）
- **专业版（15美元/月）**：每月50篇文章，所有功能可用
- **无限量版（49美元/月）**：无限篇文章、API访问权限、优先生成服务

## 开发计划

- [ ] 与SEO工具（如Ahrefs、SEMRush、Moz）集成
- [ ] 自动发布到内容管理系统（WordPress、Ghost、Medium）
- [ ] 支持多语言
- [ ] 图片生成功能（使用DALL-E、Midjourney）
- [ ] 内容调度功能
- [ ] 团队协作功能

## 最佳实践

### 关键词选择
- 选择竞争较小、难度较低的长尾关键词
- 根据文章类型匹配用户搜索意图
- 平衡搜索量和竞争程度

### 内容质量
- 首先为读者写作，其次考虑搜索引擎
- 使用自然语言，避免过度使用关键词
- 包含原创见解，而不仅仅是摘要
- 定期更新以保持内容新鲜

### 联盟链接
- 每2,000字内插入3-5个链接
- 确保链接与内容相关
- 提供价值，而不仅仅是为了盈利
- 始终明确披露链接来源

## 许可证

MIT许可证

---

**自动生成具有排名能力的文章，并实现自动盈利。** 🔮