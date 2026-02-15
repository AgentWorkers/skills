---
name: product-description-generator
description: 为电子商务平台（如 Amazon、Shopify、eBay、Etsy）生成优化过 SEO 的产品描述。撰写具有吸引力的内容，重点突出产品的特性、优势以及购买呼吁（Call-to-Action），同时包含相关关键词。这些描述可用于创建新的产品列表、优化现有产品描述或批量生成产品文案。
---

# 产品描述生成器

## 概述

该工具能够为任何电子商务平台生成转化率高的、经过SEO优化的产品描述。生成的文案不仅能够促进销售，还能提升产品在多个市场平台的搜索排名。

## 核心功能

### 1. 平台特定优化

**支持的平台：**
- **亚马逊**：产品标题、项目符号列表、产品描述、搜索关键词、后端关键词
- **Shopify**：产品标题、产品描述、SEO元数据
- **eBay**：商品标题、商品描述、商品详细信息、商品状况描述
- **Etsy**：商品列表标题、商品描述、标签、材料信息、属性
- **Shopify/WooCommerce**：产品名称、产品描述、SEO相关元素
- **自定义**：适用于任何平台的灵活格式

### 2. SEO优化

**自动包含的内容：**
- 主要关键词的放置（标题、首段）
- 文本中的次要关键词
- 长尾关键词变体
- 语义关键词及相关术语
- 为每个平台优化字符长度
- 用于SEO的元描述和标题

### 3. 以转化为导向的文案

**促进销售的元素：**
- 以利益为导向的功能描述（而不仅仅是技术规格）
- 情感诉求和故事化表达
- 社交证明的整合
- 紧迫感和稀缺性元素
- 明确的价值主张
- 强有力的呼吁行动（CTA）

### 4. 结构模板

**产品描述结构：**
1. **吸引注意力**：开篇部分，吸引读者的注意力
2. **问题/痛点**：指出用户的需求或困扰
3. **解决方案**：说明产品如何帮助解决问题
4. **功能 → 利益**：产品具体能做什么以及为什么重要
5. **社会证明**：用户评价、推荐信、统计数据
6. **使用场景**：产品的使用方法和时机
7. **技术规格**：产品的技术细节
8. **常见问题解答（FAQ）**：常见问题的解答
9. **呼吁行动（CTA）**：明确的行动建议

### 5. 批量生成

**支持的功能：**
- 从CSV文件生成多个产品描述
- 生成产品的多种变体（颜色、尺寸、型号）
- 同时针对多个平台进行A/B测试
- 支持国际市场的本地化

## 快速入门

### 生成亚马逊商品列表

```python
# Use scripts/generate_description.py
python3 scripts/generate_description.py \
  --product "Wireless Bluetooth Headphones" \
  --platform amazon \
  --features "40hr battery,noise cancelling,Bluetooth 5.3" \
  --benefits "crystal clear audio,comfortable fit,fast charging" \
  --tone professional \
  --output amazon_listing.md
```

### 生成Shopify产品描述

```python
python3 scripts/generate_description.py \
  --product "Ergonomic Office Chair" \
  --platform shopify \
  --features "adjustable lumbar support,360° swivel,breathable mesh" \
  --tone conversational \
  --include-faq \
  --output shopify_description.md
```

### 从CSV文件批量生成描述

```python
# Use scripts/bulk_generate.py
python3 scripts/bulk_generate.py \
  --csv products.csv \
  --platform amazon \
  --output-dir ./descriptions
```

### 优化现有描述

```python
# Use scripts/optimize_description.py
python3 scripts/optimize_description.py \
  --input existing_description.md \
  --target-keyword "wireless headphones" \
  --platform amazon \
  --output optimized.md
```

## 脚本

### `generate_description.py`
为单个产品生成产品描述。

**参数：**
- `--product`（必填）：产品名称/标题
- `--platform`（必填）：目标平台
- `--features`：产品特性（用逗号分隔）
- `--benefits`：产品带来的好处/价值主张（用逗号分隔）
- `--tone`：语气风格（专业、对话式、轻松、奢华）
- `--target-audience`：目标受众
- `--keywords`：SEO关键词（用逗号分隔）
- `--include-faq`：是否包含FAQ部分
- `--include-specs`：是否包含技术规格部分
- `--output`：输出文件路径

**示例：**
```bash
python3 scripts/generate_description.py \
  --product "Smart WiFi Thermostat" \
  --platform amazon \
  --features "energy saving,app control,7-day programming" \
  --benefits "lower energy bills,remote access,comfort" \
  --target-audience "homeowners,smart home enthusiasts" \
  --keywords "smart thermostat,programmable thermostat,WiFi thermostat" \
  --include-faq \
  --include-specs \
  --output thermostat_description.md
```

### `bulk_generate.py`
从CSV文件生成多个产品的描述。

**CSV文件格式：**
```csv
product,features,benefits,tone,target_audience,keywords
"Wireless Headphones","40hr battery,noise cancelling","clear audio,comfort","professional","audiophiles","headphones,bluetooth"
"Ergonomic Chair","lumbar support,mesh back","back pain relief,comfort","conversational","office workers","office chair,ergonomic"
"Smart Thermostat","energy saving,app control","lower bills,remote control","professional","homeowners","thermostat,smart home"
```

**参数：**
- `--csv`：CSV文件路径
- `--platform`：目标平台（适用于所有产品）
- `--output-dir`：输出目录
- `--format`：输出格式（markdown、html、csv）

### `optimize_description.py`
优化现有产品描述的SEO效果和转化率。

**参数：**
- `--input`：输入文件路径
- `--target-keyword`：要优化的关键词
- `--platform`：目标平台
- `add-cta`：是否添加强烈的呼吁行动
- `add-social-proof`：是否添加社交证明元素
- `output`：输出文件路径

### `generate_variations.py`
生成产品描述的A/B测试变体。

**参数：**
- `--input`：基础描述文件
- `--variations`：要生成的变体数量（默认：3个）
- `--test-elements`：要测试的元素（如呼吁行动、开头部分、好处描述）
- `--output-dir`：输出目录

### `seo_analyzer.py`
分析产品描述的SEO评分。

**参数：**
- `--input`：需要分析的描述内容
- `--target-keyword`：目标关键词
- `--platform`：具体平台
- `--output`：分析报告

## 平台特定指南

### 亚马逊
- **标题：** 150-200个字符，包含主要关键词
- **项目符号列表：** 5-7项，重点突出产品优势
- **描述：** 2000-3000个字符，全面介绍产品特点
- **后端关键词：** 250个字节，用逗号分隔
- **风格：** 专业、信息丰富、详细

### Shopify
- **标题：** 70个字符，适合显示
- **描述：** 300-500个单词，支持HTML格式
- **元描述：** 155个字符，用于SEO优化
- **链接处理：** 75个字符以内，适合SEO的链接格式
- **风格：** 与品牌一致，注重视觉效果和生活方式相关

### eBay
- **标题：** 80个字符最佳，包含关键信息
- **描述：** 500-1000个单词，支持HTML格式
- **商品详细信息：** 填写所有相关字段
- **商品状况：** 明确说明商品状况
- **风格：** 强调紧迫感和详细的技术规格

### Etsy
- **标题：** 140个字符，开头部分包含关键词
- **描述：** 500多个单词，强调产品的手工制作特点
- **标签：** 使用13个标签，每个标签20个字符
- **材料信息：** 确保标签准确
- **风格：** 强调产品的手工制作和独特性

## 最佳实践

### 描述产品的好处，而不仅仅是特性
- **错误示例：** “电池续航40小时”
- **正确示例：** “40小时的电池续航意味着您可以连续使用数天而无需充电”

### 使用情感诉求
- “改变您的日常生活”
- “体验品质带来的不同”
- “加入数千名满意客户的行列”

### 添加社交证明
- “获得10,000多名客户的信任”
- “平均评分4.8/5”
- **30天退款保证”

### 处理潜在异议
- “担心尺寸合适吗？我们提供免费退货服务”
- “不确定吗？免费试用30天”
- **有问题吗？我们的美国客服24/7随时为您服务”

### 强有力的呼吁行动（CTA）
- “立即下单，享受免费配送”
- **库存有限 - 今天就加入购物车**
- “加入那些提升体验的数千用户行列”

## 语气风格指南

### 专业风格
- **适合：** B2B业务、高科技产品、高价值商品
- **特点：** 权威性、数据支持、精确表述
- **示例：** “专为高性能设计。基于科学验证。”

### 对话式风格
- **适合：** 消费者产品、生活类商品
- **特点：** 友善、易于理解、贴近用户
- **示例：** “您会喜欢它如何融入您的日常生活。”

### 轻松幽默的风格
- **适合：** 流行产品、年轻受众
- **特点：** 有趣、充满活力、使用表情符号
- **示例：** “准备好升级了吗？让我们一起行动吧！🚀”

### 奢华风格
- **适合：** 高端产品、珠宝、设计师作品
- **特点：** 优雅、独特、精致
- **示例：** “体验无与伦比的手工工艺。设计的杰作。”

## 自动化功能

### 每日批量生成描述

```bash
# Generate descriptions for all products in catalog
0 8 * * * /path/to/product-description-generator/scripts/bulk_generate.py \
  --csv /path/to/products.csv \
  --platform amazon \
  --output-dir /path/to/output
```

### A/B测试自动化

```bash
# Generate variations for top-selling products
0 9 * * 1 /path/to/product-description-generator/scripts/generate_variations.py \
  --input /path/to/bestsellers/ \
  --variations 3 \
  --output-dir /path/to/ab-tests
```

## 集成机会

- **与SEO文章生成器集成**  
- **与评论总结工具集成**  

## 输出格式

### Markdown
**最适合：** 文档编写、不支持HTML的CMS系统，便于阅读。

### HTML
**最适合：** 亚马逊、Shopify、eBay平台，支持使用标签格式。

### CSV
**最适合：** 批量上传、目录管理系统。

---

**提升销售效果。提高搜索排名。转化访客。**