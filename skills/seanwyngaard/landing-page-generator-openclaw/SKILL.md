---
name: landing-page-generator
description: 根据提供的简短描述，可以生成具有高转化率且适应移动设备的 landing 页面。这些页面适用于为客户构建 landing 页面、销售页面或营销页面。
argument-hint: "[product-or-service-description]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# 网页生成器

根据产品/服务概述，生成完整且转化率高的 landing 页面。生成的页面为可立即使用的 HTML/CSS 格式，支持移动设备，并经过优化以提高转化率。

## 使用方法

```
/landing-page-generator "SaaS project management tool for remote teams, $29/mo, free trial"
/landing-page-generator brief.txt
/landing-page-generator "Freelance web developer portfolio — book a call CTA"
```

请提供尽可能多的详细信息：
- 产品/服务的具体内容
- 目标受众
- 主要的呼叫行动（如注册、购买、预约通话、下载）
- 价格信息（如适用）
- 主要功能/优势
- 品牌颜色（可选，默认使用专业蓝色/深色主题）

## 页面生成流程

### 第一步：分析概述

提取以下信息：
- **产品类型**：SaaS、实体产品、服务、作品集、吸引潜在客户的素材、活动
- **目标受众**：该产品/服务面向哪些人？
- **主要呼叫行动**：访问者应该采取什么行动？
- **价值主张**：用户为何应该关注该产品/服务？
- **页面风格**：专业、休闲、大胆、极简或豪华

### 第二步：选择页面模板

根据产品类型选择合适的模板：

| 产品类型 | 页面结构 | 大致内容长度 |
|------|----------|---------------|
| SaaS   | 页眉、功能介绍、工作原理、价格、用户评价、常见问题解答、呼叫行动 | 较长 |
| 服务    | 页眉、服务内容、服务流程、作品集、用户评价、呼叫行动 | 中等 |
| 作品集   | 页眉、作品示例、关于我们、服务信息、联系方式 | 中等 |
| 吸引潜在客户的素材 | 页眉、优势展示、社交证明、表单、呼叫行动 | 短 |
| 电子商务 | 页眉、产品特性、产品图库、用户评价、购买呼叫行动 | 中等 |
| 活动    | 页眉、演讲者信息/活动详情、日程安排、门票信息、常见问题解答 | 中等 |

### 第三步：生成页面

创建一个包含内嵌 CSS 的独立 HTML 文件。页面仅依赖 Google Fonts，不使用任何外部资源。

**必填内容**（根据产品类型调整）：

#### 页眉部分
```
- Headline: Clear value proposition (max 10 words)
- Subheadline: Supporting detail (max 25 words)
- CTA button: High-contrast, action-oriented text ("Start Free Trial", not "Submit")
- Optional: Hero image placeholder or background
- Optional: Social proof badge ("Trusted by 10,000+ teams")
```

#### 功能/优势部分
```
- 3-4 feature cards with icons (use Unicode/emoji icons)
- Each card: Icon + Feature name + 1-2 sentence benefit (focus on outcome, not feature)
- Grid layout: 3 columns on desktop, 1 on mobile
```

#### 社交证明部分
```
- 2-3 testimonial cards with:
  - Quote text
  - Name and title/company
  - Star rating (if applicable)
- Optional: Logo bar of client/partner logos (placeholder boxes with company names)
```

#### 工作原理部分（如适用）
```
- 3-step process with numbered steps
- Step title + brief description
- Visual connector between steps
```

#### 价格信息（如适用）
```
- 1-3 pricing tiers in card format
- Highlight the recommended tier
- Feature comparison list
- CTA button on each tier
```

#### 常见问题解答
```
- 4-6 common questions
- Accordion-style (click to expand) using pure CSS/HTML <details>
```

#### 最终呼叫行动部分
```
- Repeat the primary CTA with urgency
- Different angle from hero (address remaining objections)
- Strong contrasting background
```

### 第四步：设计系统

遵循以下设计原则：

**字体**：使用 Google Fonts 提供的 `Inter` 字体（简洁、现代、易读）
- 标题字号：3rem、2rem、1.5rem、1.25rem
- 正文字号：1rem，行高为 1.6 倍
- 为了便于阅读，每行的最大宽度为 65 个字符

**颜色**（默认使用品牌颜色，如提供则可自定义）：
```css
--primary: #2563eb;        /* Blue - CTAs, links */
--primary-dark: #1d4ed8;   /* Hover state */
--bg: #ffffff;             /* Background */
--bg-alt: #f8fafc;         /* Alternating section bg */
--text: #1e293b;           /* Body text */
--text-light: #64748b;     /* Secondary text */
--accent: #f59e0b;         /* Highlights, badges */
```

**布局**：
- 页面最大宽度为 1200px，居中显示
- 各部分之间的垂直间距为 80px（移动设备上为 48px）
- 一致的间距比例：4px、8px、16px、24px、32px、48px、64px、80px

**响应式设计**：
- 桌面设备：1024px 及以上
- 平板设备：768px 至 1023px
- 移动设备：768px 以下

### 第五步：优化转化率

对生成的页面应用以下优化策略：
1. **首页可见内容**：标题和呼叫行动按钮在无需滚动的情况下即可看到
2. **单一呼叫行动**：只展示一个主要行动按钮，并在页面中重复出现 2-3 次
3. **对比度**：呼叫行动按钮的对比度需符合 WCAG AA 标准（至少 4.5:1）
4. **加载速度**：不使用外部 JavaScript，CSS 代码简洁，仅使用占位图片
5. **易读性**：用户应在 5 秒内了解页面内容
6. **处理用户疑虑**：常见问题解答和用户评价能解答常见问题
7. **营造紧迫感/稀缺感**：仅在使用真实信息时使用（如“限量测试名额”等，避免虚假倒计时）

### 第六步：输出结果

将生成的页面保存到 `output/landing-page/` 目录下：

**`README.md` 文件** 包含以下内容：
- 如何自定义页面颜色（文件顶部的 CSS 变量）
- 如何替换占位内容
- 如何添加真实图片
- 如何将表单连接到电子邮件服务
- 如何部署页面（支持 Netlify 的拖放功能、GitHub Pages 或其他静态网站托管服务）

### 第七步：向用户展示结果

向用户展示：
1. 生成页面的简要概述
2. 关于设计决策的关键内容
3. 页面文件的存放位置
4. 客户需要自定义的部分（如图片、用户评价、具体文案）

## 质量标准：
- 页面仅依赖 Google Fonts，不使用任何外部资源
- 在 320px、768px 和 1200px 宽度下均能正常显示
- 所有呼叫行动按钮都支持悬停效果
- 颜色对比度符合 WCAG AA 标准
- 页面包含正确的 `<meta>` 视口标签
- 使用语义化的 HTML 结构（`<header>`、`<main>`、`<section>`、`<footer>`）
- 在任何屏幕尺寸下都不会出现水平滚动条
- 常见问题解答部分支持展开/折叠功能
- 整个 HTML 文件大小控制在 50KB 以内