---
name: landing-page-design
description: |
  Landing page conversion optimization with layout rules, hero section design, and CTA psychology.
  Covers above-the-fold formula, social proof placement, mobile design, and F-pattern reading.
  Use for: startup landing pages, product pages, SaaS marketing, conversion optimization.
  Triggers: landing page, hero section, above the fold, conversion optimization,
  landing page design, cta button, hero image, landing page layout, saas landing page,
  product page design, conversion rate, landing page best practices
allowed-tools: Bash(infsh *)
---

# 着陆页设计

使用 [inference.sh](https://inference.sh) 命令行工具，通过人工智能生成视觉元素来设计转化率高的着陆页。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a hero image
infsh app run falai/flux-dev-lora --input '{
  "prompt": "professional person smiling while using a laptop showing a clean dashboard interface, bright modern office, natural lighting, warm and productive atmosphere, lifestyle marketing photography",
  "width": 1248,
  "height": 832
}'

# Research competitor landing pages
infsh app run tavily/search-assistant --input '{
  "query": "best SaaS landing page examples 2024 conversion rate"
}'
```

## 首屏展示原则

在用户滚动页面之前，所有可见的内容都必须在 5 秒内传达出产品的价值。

```
┌─────────────────────────────────────────────────┐
│  [Logo]              [Nav]        [CTA Button]  │
│                                                 │
│   Headline (6-12 words)                         │
│   ─────────────────────────                     │
│   Subheadline (15-25 words)        [Hero Image] │
│                                    showing the  │
│   [Primary CTA Button]            OUTCOME, not  │
│   "Start Free Trial"              the product   │
│                                                 │
│   Social proof: "Trusted by 10,000+ teams"      │
│   [logo] [logo] [logo] [logo] [logo]            │
└─────────────────────────────────────────────────┘
```

### 五大核心元素

| 元素        | 规则                                      | 示例                                      |
|-------------|-----------------------------------------|-----------------------------------------|
| **标题**       | 6-12 个单词，明确说明产品成果                   | “几分钟内即可生成文档，无需等待数天”                   |
| **副标题**      | 15-25 个单词，详细解释产品功能                   | “基于人工智能的文档生成工具，直接从您的代码库中生成。无需使用模板。”         |
| **首页图片**     | 展示产品成果，而非产品界面截图                 | 展示用户对成果的满意表情，而非产品界面截图                 |
| **主要行动号召（CTA）** | 行动动词 + 产品价值                          | “立即开始免费试用”                               |
| **社交证明**     | 公司标志、用户数量或用户评价                     | “已获得 [logos] 上 10,000+ 个团队的信任”                     |

## 标题设计

### 有效的标题公式

| 公式          | 示例                                        |                                           |
|-----------------|---------------------------------------------|-----------------------------------------|
| “[成果] 无需 [繁琐流程]”    | “无需设计技能，即可生成精美的文档”                        |
| “[成果] 在 [时间范围内] 完成”    | “5 分钟内即可发布您的网站”                              |
| “[常见任务的] 更佳方式”    | “构建 API 的更快方法”                                  |
| “停止 [麻烦]，开始 [成果]”    | “停止猜测，开始了解实际情况”                              |
| “[数量] 个工具，实现 [成果]”    | “一个工具，管理您的所有数据”                              |

### 标题设计常见错误

```
❌ "Welcome to Our Platform" (says nothing about value)
❌ "The World's Most Advanced AI-Powered Solution" (buzzwords, no specifics)
❌ "We Help Businesses Grow" (vague, generic)
❌ "Next-Generation Enterprise Software" (what does it DO?)

✅ "Turn customer feedback into product features, automatically"
✅ "The spreadsheet that thinks like a database"
✅ "Find and fix bugs before your users do"
```

## 首页图片设计

### 展示产品成果，而非产品界面

```
❌ Screenshot of your dashboard (boring, hard to parse at a glance)
❌ Abstract geometric background (says nothing)
❌ Stock photo of a handshake (cliché)

✅ Person looking satisfied at clear results on their screen
✅ Before/after transformation
✅ The end result of using your product
```

```bash
# Outcome-focused hero
infsh app run falai/flux-dev-lora --input '{
  "prompt": "happy professional team celebrating around a laptop showing positive growth charts, bright modern office, natural sunlight, authentic candid moment, marketing photography style, warm tones",
  "width": 1248,
  "height": 832
}'

# Product-in-context hero
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "clean modern laptop on a minimalist desk showing a beautiful analytics dashboard, floating UI elements emerging from the screen, soft gradient background, product marketing style, professional",
  "size": "2K"
}'
```

## 行动号召（CTA）按钮设计

|          |                                            |                                           |
| **好的 CTA          | **差的 CTA                                      |                                           |
|-----------------|-----------------------------------------|-----------------------------------------|
| “立即开始免费试用”     | “提交”                                      |                                           |
| “免费开始使用”     | “点击这里”                                      |                                           |
| “查看实际效果”     | “了解更多”（缺乏行动号召）                             |                                           |
| “创建您的第一份报告”     | “注册”                                      |                                           |
| “免费试用 14 天”     | “注册”                                      |                                           |

**公式：** 行动动词 + 产品价值/成果 + （可选：降低风险）

## 设计要素

| 元素        | 规则                                        |                                           |
|-------------|-----------------------------------------|-----------------------------------------|
| **颜色**       | 与背景形成高对比度——必须是最显眼的元素                   |                                           |
| **大小**       | 高度至少 44px（可点击区域），宽度足够显示文字和内边距                 |                                           |
| **位置**       | 放置在页面顶部；每个主要部分后重复显示                         |                                           |
| **空白空间**     | 按钮周围留出足够的空间，避免拥挤                         |                                           |
| **次要 CTA**     | 如有必要，在下方添加文字链接（或“观看演示”）                         |                                           |

## 页面结构顺序

经过验证的着陆页结构顺序：

| 部分        | 目的                                        | 关键元素                                      |
|-------------|-----------------------------------------|-----------------------------------------|
| 1. **首页图片**     | 展示核心价值与主要行动号召                         | 标题 + 图片 + 行动号召                             |
| 2. **社交证明**     | 建立信任                                      | 公司标志、用户数量、认证标志                         |
| 3. **问题描述**     | 引起用户共鸣                                      | 用户面临的痛点                                   |
| 4. **解决方案/功能**     | 展示产品如何解决问题                             | 3 个关键功能及可视化示例                         |
| 5. **使用方法**     | 降低使用难度                                   | 3 个步骤：注册、配置、获取收益                         |
| 6. **用户评价**     | 证明产品有效性                                 | 2-3 条具体客户评价                             |
| 7. **价格政策**     | 帮助用户做出决策                                   | 明确的价格层级，突出推荐选项                         |
| 8. **常见问题解答** | 解答用户疑问                                   | 5-7 个常见问题                               |
| 9. **最终行动号召** | 激发用户购买欲望                                   | 重复主要行动号召，强调紧迫性                         |

## 社交证明类型

| 类型        | 作用                                        | 显示位置                                      |
|-------------|-----------------------------------------|-----------------------------------------|
| **公司标志**     | 最快建立信任                                   | 放置在首页图片下方                               |
| **用户数量**     | 体现产品规模                                   | 放置在首页图片或社交证明区域                         |
| **星级评价**     | 体现产品质量                                   | 放置在行动号召附近                             |
| **用户评价**     | 详细展示产品可信度                                 | 专门设置评价区                               |
| **案例研究数据**     | 证明产品效果                                   | 放置在功能介绍区域                             |
| **信任认证标志**     | 体现产品安全性和合规性                                 | 放置在表单附近、页面底部                         |

```bash
# Research for social proof stats
infsh app run exa/answer --input '{
  "question": "What is the average conversion rate for SaaS landing pages with social proof vs without?"
}'
```

## 表单设计

| 规则        | 作用                                        |                                           |
|-------------|-----------------------------------------|-----------------------------------------|
| 减少表单字段数量 | 每增加一个字段，转化率降低约 11%                         |                                           |
| 仅要求姓名和电子邮件地址 | 避免收集电话号码、公司名称或职位                         |                                           |
| 单列布局       | 不要使用多列表单                               |                                           |
| 实时验证       | 立即显示错误信息，避免用户在提交时才发现                         |                                           |
| 清晰的错误提示   | 显示具体错误内容（如“需要填写电子邮件地址”而非“第 3 个字段有错误”）         |                                           |
| 提交按钮文本     | 明确表示具体操作（如“创建账户”而非“提交”）                         |                                           |

## 移动端优化

| 规则        | 原因                                        |                                           |
|-------------|-----------------------------------------|-----------------------------------------|
| 行动号召按钮占满屏幕宽度 | 便于用户用拇指点击                             |                                           |
| 滚动时保持行动号召可见     | 确保用户始终能看到行动号召                             |                                           |
| 避免水平滚动     | 避免破坏移动端页面布局                             |                                           |
| 字体大小至少 16px     | iOS 系统会放大小于 16px 的字体                         |                                           |
| 可点击区域大小至少 48x48px | 符合 Apple HIG 和 Google Material 设计规范                   |                                           |
| 图片自适应显示     | 确保图片不会超出屏幕显示范围                             |                                           |
| 优先显示标题和行动号召 | 简化首页内容                                 |                                           |

## 用于分享的原始图片

```bash
# Generate an OG image for the landing page
infsh app run falai/flux-dev-lora --input '{
  "prompt": "clean professional social sharing card, product name and tagline on modern gradient background, minimal design, corporate tech aesthetic, 1200x630 aspect ratio equivalent",
  "width": 1200,
  "height": 630
}'

# Or use html-to-image for a template-based approach
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1200px;height:630px;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;font-family:sans-serif;color:white\"><div style=\"text-align:center\"><h1 style=\"font-size:48px;margin:0\">DataFlow</h1><p style=\"font-size:24px;opacity:0.9\">Ship docs in minutes, not days</p></div></div>"
}'
```

## 页面加载速度

| 规则        | 目标                         | 原因                                        |                                           |
|-------------|-----------------------------------------|-----------------------------------------|
| 首页图片大小     | 小于 200 KB                                     | 首先加载的内容                         |                                           |
| 页面总大小     | 小于 2 MB                                     | 优化移动端加载速度                         |                                           |
| 分页加载（仅加载可见内容） | 始终加载用户可见的部分                         |                                           |
| 减少 JavaScript 使用     | 减少代码体积，加快加载速度                         |                                           |
| LCP（最大内容绘制时间） | 小于 2.5 秒                                   | 符合 Google Core Web Vitals 标准                         |

## 常见错误

| 错误类型        | 问题                                        | 修正方法                                      |
|-------------|-----------------------------------------|-----------------------------------------|
| 没有明确的标题    | 用户不清楚产品功能                         | 使用 6-12 个单词，突出产品成果                         |
| 行动号召为“了解更多”   | 行动号召缺乏吸引力                             | 使用具体行动动词和成果描述                         |
| 首页图片是产品界面截图 | 用户难以理解产品                         | 使用与产品成果相关的图片                         |
| 多个竞争性行动号召 | 造成用户决策困难                             | 仅保留一个主要行动号召                         |
| 没有社交证明     | 用户缺乏信任感                         | 添加公司标志、用户数量或评价                         |
| 表单字段过多     | 每增加一个字段，转化率降低约 11%                         | 仅要求姓名和电子邮件地址                         |
| 仅适用于桌面端的设计 | 超过 60% 的访问量来自移动端                         | 优先考虑移动端用户体验                         |
| 最终行动号召缺乏紧迫感 | 用户可能忽略提示                         | 强调“立即开始 14 天免费试用”                         |

## 相关技能

```bash
npx skills add inferencesh/skills@ai-image-generation
npx skills add inferencesh/skills@web-search
npx skills add inferencesh/skills@prompt-engineering
```

浏览所有应用程序：`infsh app list`