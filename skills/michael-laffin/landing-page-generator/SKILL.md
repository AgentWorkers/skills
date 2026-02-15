---
name: landing-page-generator
description: 生成高转化率的 landing 页面，适用于产品、服务以及潜在客户开发（lead generation）场景。这些页面可用于创建营销资料、产品发布页面、信息收集页面（squeeze pages）或数字资产销售页面。
---

# 着陆页生成器

## 概述

该工具能够生成转化率高的着陆页，提供完整的文案、页面结构和HTML/CSS代码，可直接用于部署。帮助您创建将访客转化为客户的营销页面。

## 核心功能

### 1. 页面模板

**预建的模板包括：**
- 产品发布页面（发布前/发布中）
- 信息收集页面（用于收集电子邮件地址）
- 网络研讨会注册页面
- 数字产品销售页面（课程、电子书、模板等）
- 服务预订页面
- 会员推荐页面
- 对比页面（产品A vs 产品B）
- 感谢/确认页面

### 2. 写作框架

**采用经过验证的写作框架：**
- AIDA（注意力、兴趣、欲望、行动）
- PAS（问题、焦虑、解决方案）
- 基于故事的内容结构
- 社交证明的集成
- 抗议处理机制
- 稀缺性/紧迫感元素的运用

### 3. SEO优化

**自动包含以下内容：**
- 优化的元标签（标题、描述、关键词）
- 头部标签（H1、H2、H3）
- 图片的替代文本
- 结构化数据（schema标记）
- 移动设备友好设计
- 快速加载的页面结构

### 4. 转化元素

**内置的转化触发因素：**
- 明确的价值主张
- 以利益为导向的列表项
- 客户评价/社会证明
- 常见问题解答（FAQ）部分
- 多个呼叫行动按钮（页面上方和下方）
- 保修/风险规避声明
- 倒计时器
- 限时优惠

### 5. 自适应设计

**适配以下设备：**
- 桌面电脑（1920px及以上）
- 平板电脑（768px - 1024px）
- 手机（320px - 767px）
- 跨浏览器兼容性

## 快速入门

### 生成产品发布页面

```python
# Use scripts/generate_landing.py
python3 scripts/generate_landing.py \
  --type product-launch \
  --product "SEO Course" \
  --price 299 \
  --benefits "learn SEO,rank higher,get traffic" \
  --testimonials 3 \
  --cta "Enroll Now" \
  --output product_launch.html
```

### 生成信息收集页面

```python
python3 scripts/generate_landing.py \
  --type squeeze \
  --headline "Get Free SEO Checklist" \
  --benefits "checklist,tips,strategies" \
  --cta "Send Me The Checklist" \
  --output squeeze.html
```

### 生成会员推荐页面

```python
python3 scripts/generate_landing.py \
  --type affiliate-review \
  --product "Software XYZ" \
  --affiliate-link "https://example.com/affiliate" \
  --pros 5 \
  --cons 2 \
  --cta "Try XYZ Now" \
  --output affiliate_review.html
```

## 脚本

### `generate_landing.py`
根据参数生成着陆页。

**参数：**
- `--type`：页面类型（产品发布、信息收集、网络研讨会、数字产品、服务、会员推荐、对比、感谢）
- `--headline`：主标题
- `--subheadline`：辅助标题
- `--product`：产品/服务名称
- `--price`：价格（或“起价$X”）
- `--benefits`：以逗号分隔的好处列表
- `--features`：以逗号分隔的功能列表
- `--testimonials`：要包含的客户评价数量
- `--cta`：呼叫行动按钮文本
- `--guarantee`：保修声明（可选）
- `--urgency`：紧迫感信息（可选）
- `--output`：输出文件路径

**示例：**
```bash
python3 scripts/generate_landing.py \
  --type product-launch \
  --headline "Master SEO in 30 Days" \
  --subheadline "Complete course with live coaching" \
  --product "SEO Mastery Course" \
  --price 299 \
  --benefits "rank higher,drive traffic,boost sales" \
  --features "video lessons,templates,community" \
  --testimonials 5 \
  --cta "Enroll Now - Save 50% Today" \
  --guarantee "30-day money-back guarantee" \
  --urgency "Limited spots - Offer ends Friday" \
  --output landing.html
```

### `optimize_copy.py`
优化现有的着陆页文案。

**参数：**
- `--input`：输入的HTML文件
- `--framework`：使用的写作框架（AIDA、PAS、基于故事的结构）
- `--add-social-proof`：是否添加客户评价占位符
- `--add-urgency`：是否添加稀缺性元素
- `--output`：优化后的输出文件

### `ab_test_variations.py`
生成A/B测试变体。

**参数：**
- `--input`：基础着陆页代码
- `--variations`：要生成的变体数量（默认：3个）
- `--test-elements`：测试的内容（标题、呼叫行动按钮、价格、颜色等）
- `--output-dir`：测试变体的输出目录

## 页面模板

### 产品发布页面结构

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Product Name] - Transform Your Life</title>
  <meta name="description" content="...">
  <!-- SEO meta tags -->
  <!-- Schema markup -->
</head>
<body>
  <!-- Hero Section -->
  <section class="hero">
    <h1>[Headline]</h1>
    <p>[Subheadline]</p>
    <a href="#pricing" class="cta">[CTA]</a>
  </section>

  <!-- Problem Section -->
  <section class="problem">
    <h2>Struggling with [Problem]?</h2>
    <p>You're not alone...</p>
  </section>

  <!-- Solution Section -->
  <section class="solution">
    <h2>Introducing [Product Name]</h2>
    <ul>[Benefits List]</ul>
  </section>

  <!-- Features Section -->
  <section class="features">
    <h2>What You'll Get</h2>
    <div class="feature-grid">
      [Feature 1]
      [Feature 2]
      [Feature 3]
    </div>
  </section>

  <!-- Testimonials Section -->
  <section class="testimonials">
    <h2>What People Are Saying</h2>
    [Testimonial Cards]
  </section>

  <!-- Pricing Section -->
  <section class="pricing" id="pricing">
    <h2>Choose Your Plan</h2>
    [Pricing Cards]
  </section>

  <!-- Guarantee Section -->
  <section class="guarantee">
    <h2>[Guarantee]</h2>
    <p>[Risk-free language]</p>
  </section>

  <!-- FAQ Section -->
  <section class="faq">
    <h2>Frequently Asked Questions</h2>
    [FAQ Items]
  </section>

  <!-- Final CTA -->
  <section class="final-cta">
    <a href="#pricing" class="cta">[CTA]</a>
    <p>[Urgency message]</p>
  </section>

  <!-- Footer -->
  <footer>[Legal links, contact info]</footer>
</body>
</html>
```

## 最佳实践

### 标题
- **长度：** 最多6-12个单词
- **格式：** 清晰明了，突出利益
- **标点符号：** 使用数字和括号
- **示例：**
  - “30天内掌握SEO技巧”
  - “[产品名称]：排名第一的解决方案”
  - “如何[获得好处]而无需[忍受痛苦]”

### 呼叫行动按钮（CTA）
- **位置：** 位于页面上方，并在下方多次出现
- **颜色：** 对比鲜明（绿色、橙色、蓝色）
- **文本：** 行动导向（注册、获取、开始、加入）
- **紧迫感：** 添加时间限制或稀缺性提示

### 社交证明
- **放置位置：** 靠近呼叫行动按钮的位置
- **类型：** 包括客户评价、案例研究、统计数据
- **具体性：** 包含姓名、照片和实际效果

### 价格展示
- **优先展示高价选项**
- **分层定价：** 三个等级（优秀、更好、最佳）
- **突出中间选项：** 使中间选项更显眼
- **心理技巧：** 用$299代替$300

### 移动设备优化
- **呼叫行动按钮的位置：** 手机页面上方
- **字体大小：** 不少于16px
- **按钮尺寸：** 不少于44px
- **表单字段：** 每个屏幕只显示一个输入字段

## 自动化

### 批量生成着陆页

```bash
# Generate landing pages for multiple products
0 10 * * * /path/to/landing-page-generator/scripts/bulk_generate.py \
  --csv products.csv \
  --output-dir /path/to/landing-pages
```

### A/B测试自动化

```bash
# Generate variations for top pages
0 9 * * 1 /path/to/landing-page-generator/scripts/ab_test_variations.py \
  --input /path/to/top-pages/ \
  --variations 3 \
  --output-dir /path/to/ab-tests
```

## 集成机会

### 与产品描述生成器集成
```bash
# 1. Generate product description
product-description-generator/scripts/generate_description.py \
  --product "Course Name"

# 2. Extract benefits
# 3. Generate landing page
landing-page-generator/scripts/generate_landing.py \
  --benefits "[extracted]"
```

### 与客户评价汇总工具集成
```bash
# 1. Get review insights
review-summarizer/scripts/scrape_reviews.py --url "[product_url]"

# 2. Extract pros/cons
# 3. Generate review page
landing-page-generator/scripts/generate_landing.py \
  --type affiliate-review \
  --pros "[extracted]" \
  --cons "[extracted]"
```

---

**构建页面，转化访客，提升收入。**