---
name: instagram-marketing
description: 根据用户提供的产品URL（来自亚马逊、Shopify、淘宝等电子商务网站），生成适合在Instagram上发布的营销内容。具体步骤包括：

1. **提取产品信息**：从产品URL中提取产品的名称、价格、描述、图片链接等关键信息。

2. **创建吸引人的Instagram帖子**：
   - **图片选择**：根据产品特性选择合适的图片，确保图片质量高且与产品内容相关。
   - **编写吸引人的标题和描述**：使用简洁明了的标题，结合产品的特点和优势来吸引用户的注意力。描述部分应包含产品的核心卖点和使用场景。
   - **添加Call to Action (CTA)**：鼓励用户采取特定行动，如购买产品、了解更多信息或关注品牌。

3. **优化标签（Hashtags）**：使用与产品相关的热门标签，以提高帖子的曝光率和互动率。

4. **内容格式**：确保帖子遵循Instagram的格式要求，包括适当的图片和文字比例、标题和描述的位置等。

5. **适用于不同类型的帖子**：根据产品类型和用户需求，生成适合发布在Instagram Stories或Reels中的内容。

示例：
- 如果产品适合发布在Stories中，可以添加动画效果、音乐或视频片段，增加互动性。
- 如果产品适合发布在Reels中，可以使用短视频形式，结合多个镜头和不同的视角来展示产品。

通过以上步骤，可以为用户提供定制化的Instagram营销内容，帮助提高产品的在线曝光率和销售转化率。
---

# Instagram营销生成器

## 概述

将任何产品URL转换为能够吸引用户驻足观看的Instagram内容。提取产品详情，分析品牌定位，并生成符合Instagram平台特性的营销素材，以提升用户参与度和转化率。

## 快速入门

1. **输入**：提供产品URL
2. **提取**：使用`scripts/extract_product.py`脚本获取产品详情
3. **生成**：应用`references/`目录中的Instagram内容模板
4. **输出**：生成可直接发布的完整内容包

## 内容模板

### 模板选择指南

根据产品类型和品牌风格选择合适的模板：

| 产品类型 | 推荐模板 | 参考文档 |
|--------------|----------------------|-----------|
| 时尚/美容 | `FASHION.md` | `references/FASHION.md` |
| 科技/小工具 | `TECH.md` | `references/TECH.md` |
| 食品/饮料 | `LIFESTYLE.md` | `references/LIFESTYLE.md` |
| 家居/装饰 | `HOME.md` | `references/HOME.md` |
| 服务 | `SERVICE.md` | `references SERVICE.md` |

### 核心内容元素

每个Instagram内容包包括：

#### 1. 图片/视频简介
```
• Visual style (aesthetic direction)
• Composition guidelines
• Text overlay suggestions (optional)
• Product angle recommendations
• Background/props guidance
```

#### 2. 标题格式
```
HOOK → [First line - stops the scroll]
  |
  ├── BODY → [Value proposition, benefits, story]
  |
  └── CTA → [Clear action: link, DM, save, share]
```

**标题长度建议：**
- 信息流帖子：138-150个字符（最佳互动效果）
- 轮播图：150-200个字符
- 教育类内容：最多300个字符

#### 3. 标签策略（最多30个标签）
```
• 3-5 branded/niche tags (high relevance)
• 10-15 trend tags (moderate volume)
• 5-10 broad tags (max reach)
• Mix of: #branded #descriptive #trend #location #emotion
```

详情请参阅`references/HASHTAG_STRATEGYYYY.md`文档，了解标签优化技巧。

## 产品信息提取

### 脚本使用方法

```bash
python3 scripts/extract_product.py <url>
```

**提取的信息包括：**
- 产品名称
- 价格/价值主张
- 主要功能（3-5项）
- 目标受众
- 独特卖点
- 品牌风格
- 可用的视觉素材（现有图片）

### 手动提取方案

如果脚本失败，可以手动提取信息：
1. 访问产品URL
2. 收集：产品名称、价格、功能、优势
3. 观察品牌视觉风格
4. 拍摄3-5张产品照片

## 内容生成流程

### 第一步：分析产品与目标受众

```
PRODUCT → [What is it? What problem does it solve?]
  |
  ├── TARGET AUDIENCE → [Who needs this? Why?]
  |
  ├── BRAND TONE → [Luxury? Playful? Minimal? Bold?]
  |
  └── PLATFORM FIT → [Feed post, Story, Reel, Carousel?]
```

**关键问题：**
- 用户应该感受到什么样的情感？
- 什么内容能吸引用户驻足观看？
- 产品使用后能带来怎样的改变？

### 第二步：选择内容格式

#### 信息流帖子（单张图片）
- **适用场景**：产品展示、公告
- **视觉要求**：高质量的产品图片，简洁的背景
- **标题**：吸引人的开头 + 产品优势 + 行动号召

#### 轮播图（可滑动）
- **适用场景**：产品功能介绍、教程、使用效果展示
- **结构**：5-10张图片
  1. 开场图片
  2-4张功能/优势图片
  5张行动号召图片

#### 故事（15-60秒）
- **适用场景**：限时促销、投票、问答、幕后花絮
- **元素**：互动贴纸、点击链接

#### 视频（15-90秒）
- **适用场景**：产品演示、开箱视频、使用效果展示
- **开头**：前1秒至关重要
- **音乐**：使用热门音乐提升观看体验

### 第三步：生成内容包

输出格式请参考`templates/OUTPUT_TEMPLATE.md`文件：

```markdown
## Instagram Content Package

### Post Type: [Feed/Carousel/Story/Reel]

### Image/Video Brief
[Visual direction + composition]

### Caption
[Hook + Body + CTA]

### Hashtags
[30 optimized hashtags]

### Posting Strategy
[Time, frequency, cross-post suggestions]
```

## Instagram风格指南

### 视觉设计原则

1. **一致性优先**
   - 保持色彩搭配的一致性（最多3-5种颜色）
   - 使用统一的滤镜/预设效果
   - 体现品牌独特的美学风格

2. **质量高于数量**
   - 使用高分辨率图片（1080x1080或1080x1350）
   - 优质的光线效果（自然光为佳）
   - 规则三分法构图

3. **保持原生感**
   - 避免过度修饰或使用库存图片
   - 体现真实的产品/人物

### 标题编写技巧

✅ 应该：
- 用引人入胜的开头（问题、强调句、情感表达）
- 采用对话式的语言
- 使用换行符提高可读性
- 包含明确的行动号召
- 添加3-5个相关标签

❌ 不应该：
- 写超过3行的长标题
- 过度使用表情符号（最多1-3个）
- 过量使用标签（30个以内，质量优先）
- 语言显得机械或过于促销
- 在简介中多次提及“点击链接”

### 提高互动性的方法

在内容中嵌入以下元素：
```
• Questions: "Which color would you choose?"
• Opinions: "Yes or No?"
• Saves: "Save this for later"
• Shares: "Tag someone who needs this"
• CTAs: "Link in bio to shop"
```

## 内容模板示例

### 模板1：问题-解决方案
```
Hook: Tired of [problem]?
Body: Meet [product]. It [benefit 1], [benefit 2], and [benefit 3].
CTA: Shop now → link in bio
```

### 模板2：产品使用效果展示
```
Hook: Before → After
Body: How [product] transformed [situation].
CTA: See the difference → link in bio
```

### 模板3：用户评价/社会证明
```
Hook: ⭐⭐⭐⭐⭐ "Review quote"
Body: Join [number]+ happy customers.
CTA: Try it risk-free → link in bio
```

### 模板4：产品教育类内容
```
Hook: 5 things you didn't know about [product/category]
Body: [Value-packed tips]
CTA: Save this post + follow for more
```

### 模板5：限时优惠
```
Hook: 🚨 Only [number] left!
Body: [Product] at [price] for [timeframe].
CTA: Don't miss out → link in bio
```

## 高级技巧：多篇帖子系列

对于产品发布或营销活动，可以创建3-5篇系列帖子：

### 系列结构
1. **预热帖**（发布前2-3天）
   - 激发用户兴趣
   - “重大消息即将揭晓”

2. **正式发布帖**（第一天）
   - 产品介绍
   - 主要功能展示

3. **深入解析帖**（第二天-第三天）
   - 产品优势、使用案例
   - 用户评价

4. **紧急提醒帖**（第四天-第五天）
   - 限时优惠
   - 最后机会

详细的活动策划方案请参阅`references/CAMPAIGN_STRATEGYYYY.md`。

## 参考资料

### 详细指南
- `references/FASHION.md` - 时尚/美容类内容模板
- `references/TECH.md` - 科技/小工具类内容模板
- `references/HASHTAG_STRATEGYYYY.md` - 标签优化指南
- `references/CAMPAIGN_STRATEGYYYY.md` - 多篇帖子营销策略
- `references/ENGAGEMENT_TACTICS.md` - 互动策略与增长技巧

### 模板文件
- `templates/CAROUSEL_TEMPLATE.md` - 轮播图模板
- `templates/STORY TEMPLATE.md` - 故事类内容模板
- `templates/REEL TEMPLATE.md` - 视频脚本模板
- `templates/OUTPUT TEMPLATE.md` - 最终内容格式模板

## 提示

- 确保内容与品牌风格一致
- 测试不同的开头方式
- 分析竞争对手的帖子以获取灵感
- 将内容灵活应用于不同格式（信息流 → 故事 → 视频）
- 将表现优秀的帖子保存为模板
- 根据用户活跃时间发布内容
- 在1小时内回复用户评论
- 使用Instagram Insights工具优化内容效果