---
name: email-capture-generator
description: 使用经过验证的五部分转化框架来构建高转化率的潜在客户吸引页面（lead magnets）、信息收集页面（squeeze pages）以及电子邮件捕获漏斗（email capture funnels）。这些框架包括注册表单（opt-in forms）、感谢页面（thank you pages）以及自动化邮件发送功能（delivery automation hooks）。
metadata:
  openclaw:
    requires:
      bins: []
      env: []
  tags:
    - email
    - lead-magnet
    - squeeze-page
    - opt-in
    - capture
    - funnel
    - marketing
  keywords:
    - "email capture"
    - "lead magnet"
    - "squeeze page"
    - "opt-in form"
    - "email list"
    - "conversion funnel"
    - "landing page"
  examples:
    - "Create a lead magnet landing page for a free ebook"
    - "Build an email capture funnel for a webinar"
    - "Design a newsletter signup squeeze page"
    - "Generate a free tool opt-in page"
---
# 电子邮件捕获生成器技能

使用经过验证的转化框架，构建高转化率的潜在客户吸引页（lead magnets）、信息收集页面（squeeze pages）以及电子邮件捕获渠道（email capture funnels）。

## 电子邮件捕获框架

### 五部分结构流程

请严格按照以下五部分结构从上到下构建电子邮件捕获页面：

```
┌─────────────────────────────────────────────────────────┐
│ 1. HOOK (Hero Section)                                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │  [Headline - Benefit-driven, specific]          │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │  [Subheadline - Expand on the promise]         │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │     [OPT-IN FORM]                               │   │
│  │     Email: [____________]                       │   │
│  │     [GET IT FREE]                              │   │
│  └─────────────────────────────────────────────────┘   │
│              [Lead magnet image]                       │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 2. VALUE (What's Inside)                               │
│    "Here's what you'll get:"                          │
│    ✓ [Benefit 1]                                      │
│    ✓ [Benefit 2]                                      │
│    ✓ [Benefit 3]                                      │
│         [Image showing the lead magnet]                │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 3. PROOF (Social Validation)                          │
│    Headline: "Join X+ subscribers"                    │
│    [Testimonial 1]                                    │
│    [Testimonial 2]                                    │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 4. URGENCY (Why Now)                                  │
│    "This offer expires..."                            │
│    [Scarcity element]                                 │
│    [Countdown timer if applicable]                    │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 5. REASSURANCE (Trust Builders)                       │
│    ✓ No spam, ever                                    │
│    ✓ Unsubscribe anytime                              │
│    ✓ [Privacy link] [Terms link]                     │
└─────────────────────────────────────────────────────────┘
```

### 各部分详细说明

**1. 吸引注意力（Hook Section）**
- 以利益为导向的标题（具体且注重结果）
- 对标题内容进行详细说明的副标题
- 电子邮件输入框 + 行动号召（CTA）按钮
- 潜在客户吸引内容的可视化展示（电子书、检查清单、模板预览）

**2. 价值展示（Value Section）**
- “您将获得什么”这样的标题
- 3-5个带复选标记的要点
- 潜在客户吸引内容的可视化展示（封面、预览图、样本）

**3. 信任验证（Proof Section）**
- 订阅者数量
- 2-3条简短的推荐语
- 信任指标（如适用，请添加相关标志）

**4. 紧迫感（Urgency Section）**
- 限时优惠信息（数量有限）
- 倒计时器（可选）
- 立即行动的理由

**5. 安心保障（Reassurance Section）**
- “绝不发送垃圾邮件”的承诺
- 退订保证
- 隐私政策/服务条款链接

## 模板变量

在生成的页面中，请替换以下占位符：

| 变量 | 说明 |
|----------|-------------|
| `{{HEADLINE}}` | 以利益为导向的主要标题 |
| `{{SUBHEADLINE}}` | 辅助描述 |
| `{{LEAD_MAGNET_NAME}}` | 免费提供的内容名称 |
| `{{BENEFIT_1}}` | 第一项好处 |
| `{{BENEFIT_2}}` | 第二项好处 |
| `{{BENEFIT_3}}` | 第三项好处 |
| `{{CTA_TEXT}}` | 按钮文本（例如：“免费获取”） |
| `{{EMAIL PLACEHOLDER}}` | 电子邮件输入框占位符 |
| `{{SUBSCRIBER_COUNT}}` | 订阅者数量 |
| `{{TESTIMONIAL_1}}` | 第一条推荐语 |
| `{{TESTIMONIAL_1 AUTHOR}}` | 第一条推荐语的作者 |
| `{{TESTIMONIAL_2}}` | 第二条推荐语 |
| `{{TESTIMONIAL_2 AUTHOR}}` | 第二条推荐语的作者 |
| `{{URGENCY_MESSAGE}}` | 限时优惠信息 |
| `{{COUNTDOWN_DATE}}` | 有效期（如适用） |
| `{{LEAD_MAGNET_IMAGE}}` | 免费提供内容的图片 |
| `{{COMPANY_NAME}}` | 品牌/公司名称 |
| `{{PRIVACY_URL}}` | 隐私政策链接 |
| `{{TERMS_URL}}` | 服务条款链接 |

## 潜在客户吸引内容类型

本技能支持多种形式的潜在客户吸引内容：

1. **电子书** - 数字指南或报告
2. **检查清单** - 可打印或数字形式的清单
3. **模板** - 电子表格、Notion软件中的模板或设计模板
4. **测验** - 交互式评估，结果通过电子邮件发送
5. **免费工具** - 小型应用程序或计算器
6. **视频系列** - 通过电子邮件提供的视频课程
7. **快速参考指南** - 简明易懂的参考资料
8. **示例文件** - 包含多个示例的文件集合

## 转化策略

### 标题编写技巧
- 使用“[情感] + [具体结果] + [时间框架]”的格式
- 例如：“30天内获得10倍更多的潜在客户”
- 使用“[数字] + [具体内容] + [在[时间框架]内]”的格式
- 例如：“7天内获得1,000名电子邮件订阅者”

### 表单设计最佳实践
- 仅使用一个输入字段（电子邮件地址） = 最高的转化率
- 将表单放置在页面可见区域（above the fold）
- 按钮颜色与背景形成对比
- 清晰的行动号召：例如“立即获取我的[潜在客户吸引内容]”，而非“提交”

### 必须显示在页面可见区域的内容
1. 标题
2. 副标题
3. 可视化展示内容
4. 表单

## 信任元素的放置位置
- 表单之前（用于展示信任信息）
- 表单之后（用于提供安心保障）

## 文件结构

```
email-capture-generator/
├── SKILL.md                 # This file
├── templates/
│   ├── squeeze-page.html    # Basic squeeze page
│   ├── lead-magnet.html     # Detailed lead magnet page
│   └── thank-you.html       # Confirmation/thank you page
└── examples/
    ├── ebook-capture.md     # Example: ebook lead magnet
    ├── checklist-capture.md # Example: checklist lead magnet
```

## 示例：电子书形式的潜在客户吸引内容

**潜在客户吸引内容名称：**《迷你住宅融资指南》
**目标受众：** 有意向购买迷你住宅的人
**主要好处：** 了解融资选项

```
HOOK:
- Headline: "Get Your Tiny Home Faster with the Financing Guide 90% of Buyers Miss"
- Subhead: "Discover the 7 financing strategies that helped 1,000+ families afford their dream tiny home"
- CTA: "Send Me The Guide"

VALUE:
- ✓ 7 proven financing strategies
- ✓ Comparison charts
- ✓ Lender contact list
- ✓ Mistakes to avoid

PROOF:
- "Join 5,000+ tiny home enthusiasts"
- Testimonial from satisfied reader

URGENCY:
- "This free guide is available for a limited time"

REASSURANCE:
- "We respect your privacy. No spam, ever."
```