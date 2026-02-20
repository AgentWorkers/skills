---
name: landing-page-design
description: "** landing页面转化优化：布局规则、标题栏设计以及用户行为心理学的应用**  
本文涵盖以下内容：  
- 如何通过合理的布局规则提升页面转化率；  
- 标题栏（hero section）的设计策略；  
- 激发用户行动（CTA, Call to Action）的心理学原理；  
- 如何在页面首屏展示关键信息（above-the-fold design）；  
- 社交证明（social proof）在页面中的应用；  
- 移动设备上的页面适配设计；  
- 读者的阅读习惯与页面布局的关系（F-pattern reading）。  
**适用场景：**  
- 初创企业网站 landing 页面  
- 产品详情页面  
- SaaS 产品营销  
- 转化率优化策略  
**相关术语解释：**  
- **landing page**：网站首页，用于引导用户了解产品或服务  
- **hero section**：网站首页中的重点展示区域  
- **above-the-fold**：页面首屏内容  
- **CTA button**：引导用户采取行动的按钮  
- **social proof**：用户评价、推荐等内容，用于增强信任感  
- **F-pattern reading**：用户阅读信息的常见模式  
**使用建议：**  
- 根据用户阅读习惯优化页面布局  
- 创意设计标题栏，吸引用户注意力  
- 明确设置 CTA 按钮，引导用户完成目标操作  
- 有效利用社交证明提升信任度  
- 确保移动设备上的页面显示效果良好  
**适用领域：**  
- 电子商务  
- 软件开发  
- 服务行业  
**应用目标：**  
- 提高用户转化率（increase conversion rates）  
- 增强用户满意度（enhance user satisfaction）  
- 提升品牌知名度（boost brand awareness）"
allowed-tools: Bash(infsh *)
---
# 着陆页设计

通过 [inference.sh](https://inference.sh) 命令行工具，利用人工智能生成的视觉元素来设计转化率高的着陆页。

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

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可选择 [手动安装与验证](https://dist.inference.sh/cli/checksums.txt)。

## 首屏展示内容的原则

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

### 五个关键元素

| 元素 | 规则 | 示例 |
|---------|------|---------|
| **标题** | 6-12 个单词，明确表达结果 | “几分钟内即可生成文档，无需等待数天” |
| **副标题** | 15-25 个单词，进一步说明产品功能 | “基于人工智能的文档生成工具，直接从您的代码库中生成。无需使用模板。” |
| **首页图片** | 展示最终成果，而非产品界面 | 展示用户对结果的满意表情，而非产品界面截图 |
| **主要呼叫行动（CTA）** | 行动动词 + 价值主张 | “立即开始免费试用”而非“提交”或“了解更多” |
| **社交证明** | 公司标志、用户数量或用户评价 | “已获得 10,000 多个团队的信赖” |

## 标题设计

### 有效的标题公式

| 公式 | 示例 |
|---------|---------|
| [成果] + [无需额外努力] | “无需设计技能，即可生成美观的文档” |
| [成果] + [时间限制] | “5 分钟内即可发布网站” |
| [更高效的方法] + [常见任务] | “构建 API 的更快方式” |
| [停止麻烦] + [开始获得成果] | “别再猜测了，开始了解实际效果吧。” |
| [具体数量] + [最终成果] | “一个工具，管理所有数据” |

### 标题设计失败的常见原因

```
❌ "Welcome to Our Platform" (says nothing about value)
❌ "The World's Most Advanced AI-Powered Solution" (buzzwords, no specifics)
❌ "We Help Businesses Grow" (vague, generic)
❌ "Next-Generation Enterprise Software" (what does it DO?)

✅ "Turn customer feedback into product features, automatically"
✅ "The spreadsheet that thinks like a database"
✅ "Find and fix bugs before your users do"
```

## 首页图片的设计

### 展示最终成果，而非产品界面

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

## 呼叫行动（CTA）按钮

### 文本设计

| 优秀的 CTA | 不合格的 CTA |
|-----------|----------|
| “立即开始免费试用” | “提交” |
| “免费开始使用” | “点击这里” |
| “查看实际效果” | “了解更多”（缺乏吸引力） |
| “创建您的第一份报告” | “注册”（表述模糊） |
| “免费试用 14 天” | “注册” |

**公式：** 行动动词 + 价值主张 + （可选：降低风险）

## 设计原则

| 元素 | 规则 |
|---------|------|
| 颜色 | 与背景形成高对比度——必须是页面上最显眼的元素 |
| 大小 | 高度至少为 44px（便于点击），宽度要足够显示文字和边距 |
| 位置 | 放在首页显眼位置，并在每个主要部分后重复显示 |
| 空白 | 按钮周围要有足够的空白空间，避免拥挤 |
| 次要 CTA | 如有需要，可在下方添加文字链接（例如：“或观看演示”）

## 页面结构顺序

经过验证的着陆页结构如下：

| 部分 | 目的 | 关键元素 |
|---------|---------|-------------|
| 1. **首页图片** | 展示核心价值与主要呼叫行动 | 标题 + 图片 + CTA |
| 2. **社交证明** | 建立信任 | 公司标志、用户数量、认证标志 |
| 3. **问题描述** | 引发用户共鸣 | 用户面临的实际问题 |
| 4. **解决方案/功能** | 通过视觉元素展示解决方案 | 三个关键功能 |
| 5. **使用方法** | 降低使用难度 | 三个步骤：注册、配置、收益 |
| 6. **用户评价** | 证明产品效果 | 两到三条具体客户评价 |
| 7. **价格信息** | 帮助用户决策 | 明确的价格层级，突出推荐方案 |
| 8. **常见问题解答** | 解答用户疑问 | 5-7 个常见问题 |
| 9. **最终呼叫行动** | 激发用户行动 | 重复主要呼叫行动，强调紧迫性 |

## 社交证明的类型

| 类型 | 作用 | 位置 |
|------|--------|-----------|
| **公司标志** | 最快建立信任 | 放在首页图片下方 |
| **用户数量** | 体现产品规模 | 放在首页图片或社交证明区域 |
| **星级评分** | 体现产品质量 | 放在 CTA 附近 |
| **用户评价** | 详细展示产品可信度 | 设立专门的评价区 |
| **案例研究数据** | 证明产品效果 | 放在功能介绍部分 |
| **信任认证标志** | 体现产品安全性和合规性 | 放在表单附近、价格信息或页脚 |

```bash
# Research for social proof stats
infsh app run exa/answer --input '{
  "question": "What is the average conversion rate for SaaS landing pages with social proof vs without?"
}'
```

## 表单设计

| 规则 | 作用 |
|------|--------|
| 减少表单字段数量 | 每增加一个字段，转化率可能下降约 11% |
| 仅要求姓名和电子邮件地址 | 避免要求填写电话号码、公司名称或职位 |
| 单列布局 | 不要使用多列表单 |
| 实时验证错误 | 错误信息应立即显示，而不是在提交时才显示 |
| 清晰的错误提示 | 例如：“必须填写电子邮件地址”而非“第 3 个字段有错误” |
| 提交按钮的文字应明确表示具体动作 | 例如：“创建账户”而非“提交” |

## 移动端优化

| 规则 | 原因 |
|------|-----|
| CTA 按钮占满整个宽度 | 便于用户用拇指点击 |
| 滚动时 CTA 保持可见 | 确保用户始终能看到 CTA |
| 避免水平滚动 | 避免破坏移动端页面布局 |
| 字体大小至少为 16px | iOS 系统会放大小于 16px 的字体 |
| 点击目标区域至少为 48x48px | 符合 Apple 和 Google 的设计规范 |
| 图片需响应式显示 | 避免图片超出屏幕显示范围 |
| 优先展示标题和 CTA | 简化首页内容 |

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

| 规则 | 目标 | 原因 |
|------|--------|-----|
| 首页图片 | 文件大小 < 200 KB | 优先加载的元素 |
| 整个页面大小 | < 2 MB | 优化移动端加载速度 |
| 分页加载页面内容 | 只加载可见的部分 |
| 减少 JavaScript 使用 | 文件大小 < 200 KB | 避免影响页面渲染 |
| LCP（首次绘制内容时间） < 2.5 秒 | 符合 Google Core Web Vitals 标准 |

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 没有明确的标题 | 用户不清楚产品的功能 | 使用 6-12 个单词，突出最终成果 |
| CTA 仅写着“了解更多” | 缺乏行动号召 | 使用具体的行动动词和价值主张 |
| 首页图片是产品界面截图 | 用户难以理解 | 应展示使用产品后的实际效果 |
| 多个竞争性的 CTA | 使用户犹豫不决 | 最多设置一个主要 CTA 和一个次要 CTA |
| 没有社交证明 | 用户缺乏信任感 | 添加公司标志、用户数量或用户评价 |
| 表单字段过多 | 每增加一个字段，转化率可能下降 11% | 仅要求填写姓名和电子邮件 |
| 仅适用于桌面端的页面设计 | 超过 60% 的访问者来自移动端 | 首先优化移动端体验 |
| 最终 CTA 缺乏紧迫感 | 用户可能忽略点击 | 使用“立即开始 14 天免费试用”等语句激发用户行动 |

## 相关技能

```bash
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@web-search
npx skills add inference-sh/skills@prompt-engineering
```

浏览所有相关工具：`infsh app list`