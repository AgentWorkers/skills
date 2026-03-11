---
name: "analytics-tracking"
description: "设置、审核和调试分析跟踪系统（包括 Google Analytics 4 (GA4)、Google Tag Manager、事件分类体系、转化跟踪以及数据质量相关功能）。这些工具适用于从零开始制定跟踪计划、审核现有分析系统中的漏洞或错误、调试缺失的事件，或配置 Google Tag Manager。相关关键词：GA4 设置、Google Tag Manager、事件跟踪、分析系统实施、转化跟踪、跟踪计划、事件分类体系、自定义维度、UTM 跟踪、分析系统审核、缺失事件等。请注意：这些工具不适用于分析营销活动数据（请使用 campaign-analytics），也不适用于构建商业智能 (BI) 仪表板（请使用 product-analytics 进行产品内事件分析）。"
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  updated: 2026-03-06
---
# 分析跟踪

作为分析实施的专家，您的目标是确保客户旅程中的每一个有意义的操作都能被准确、一致地记录下来，并且这些数据能够真正用于决策制定——而不仅仅是为了拥有数据本身。

糟糕的跟踪系统比没有跟踪系统更糟糕。重复的事件、缺失的参数、未经同意的数据以及错误的转化数据都会导致基于错误信息做出的决策。这项技能的核心在于从一开始就正确地构建跟踪系统，或者发现并修复存在的问题。

## 开始之前

**先了解背景信息：**
如果存在 `marketing-context.md` 文件，请在提问之前先阅读它。根据该文件的内容，只提出您需要了解的问题。

收集以下背景信息：

### 1. 当前状态
- 您是否已经设置了 GA4 和/或 GTM？如果已经设置，那么有哪些地方出了问题或遗漏了什么？
- 您的技术栈是什么？（React SPA、Next.js、WordPress、自定义系统等）
- 您是否有同意管理平台（CMP）？使用的是哪个平台？
- 您目前跟踪了哪些事件（如果有）？

### 2. 业务背景
- 您的主要转化动作是什么？（注册、购买、填写潜在客户表单、开始免费试用）
- 您的关键微转化动作是什么？（查看价格页面、发现功能、请求演示）
- 您是否运行过付费广告活动？（Google Ads、Meta、LinkedIn — 这会影响转化跟踪的需求）

### 3. 目标
- 是从零开始构建系统，还是审核现有的系统，还是调试某个具体问题？
- 您是否需要跨域跟踪？是否需要跟踪多个属性或子域名？
- 是否有服务器端标签的需求？（在 GDPR 敏感的市场中，或者出于性能考虑）

## 这项技能的工作方式

### 模式 1：从零开始构建
如果还没有分析系统，我们将制定跟踪计划，安装 GA4 和 GTM，定义事件分类，并配置转化事件。

### 模式 2：审核现有的跟踪系统
如果现有的跟踪系统不可靠、覆盖范围不完整，或者您需要添加新的跟踪目标，我们将审核现有的系统，填补空白并进行优化。

### 模式 3：调试跟踪问题
如果某些特定事件缺失，转化数据不一致，或者 GTM 预览显示事件被触发但 GA4 没有记录这些事件，我们将使用结构化的调试流程来解决问题。

---

## 事件分类设计

在开始使用 GA4 或 GTM 之前，必须先设计好事件分类。后期修改分类会非常麻烦。

### 命名规则

**格式：`object_action`（使用蛇形命名法，动词放在末尾）**

| ✅ 正确 | ❌ 错误 |
|--------|--------|
| `form_submit` | `submitForm`、`FormSubmitted`、`form-submit` |
| `plan_selected` | `clickPricingPlan`、`selected_plan`、`PlanClick` |
| `video_started` | `videoPlay`、`StartVideo`、`VideoStart` |
| `checkout_completed` | `purchase`、`buy_complete`、`checkoutDone` |

**规则：**
- 始终使用 `名词_动词` 的格式，避免使用 `动词_名词` 的格式
- 仅使用小写字母和下划线，不要使用驼峰式命名法或连字符
- 命名要足够具体，避免过于冗长
- 时态要保持一致：使用 `_started`、`_completed`、`_failed`（不要混合使用过去式和现在式）

### 标准参数

每个事件（如果适用）都应该包含以下参数：

| 参数 | 类型 | 示例 | 用途 |
|-----------|------|---------|---------|
| `page_location` | 字符串 | `https://app.co/pricing` | GA4 会自动捕获 |
| `page_title` | 字符串 | `Pricing - Acme` | GA4 会自动捕获 |
| `user_id` | 字符串 | `usr_abc123` | 用于链接到您的 CRM/数据库 |
| `plan_name` | 字符串 | `Professional` | 按计划进行用户分组 |
| `value` | 数字 | `99` | 收入/订单金额 |
| `currency` | 字符串 | `USD` | 与 `value` 一起使用时是必需的 |
| `content_group` | 字符串 | `onboarding` | 用于分组页面/流程 |
| `method` | 字符串 | `google.oauth` | 注册方式等 |

### SaaS 应用的事件分类

**核心转化事件：**
```
visitor_arrived         (page view — automatic in GA4)
signup_started          (user clicked "Sign up")
signup_completed        (account created successfully)
trial_started           (free trial began)
onboarding_step_completed (param: step_name, step_number)
feature_activated       (param: feature_name)
plan_selected           (param: plan_name, billing_period)
checkout_started        (param: value, currency, plan_name)
checkout_completed      (param: value, currency, transaction_id)
subscription_cancelled  (param: cancel_reason, plan_name)
```

**微转化事件：**
```
pricing_viewed
demo_requested          (param: source)
form_submitted          (param: form_name, form_location)
content_downloaded      (param: content_name, content_type)
video_started           (param: video_title)
video_completed         (param: video_title, percent_watched)
chat_opened
help_article_viewed     (param: article_name)
```

请参阅 [references/event-taxonomy-guide.md](references/event-taxonomy-guide.md) 以获取完整的事件分类目录及自定义维度的建议。

---

## GA4 设置

### 数据流配置

1. 在 GA4 中创建属性 → 管理员 → 属性 → 创建新属性
2. 添加包含您域名的网络数据流
3. 启用“增强测量”功能，然后检查以下选项：
   - ✅ 页面视图（保留）
   - ✅ 滚动行为（保留）
   - ✅ 外部链接点击（保留）
   - ✅ 网站搜索（如果您有搜索功能，请保留）
   - ⚠️ 视频互动（如果您手动跟踪视频，请禁用此选项 — 以避免数据重复）
   - ⚠️ 文件下载（如果您在 GTM 中跟踪文件下载，请禁用此选项，以便获得更准确的参数）
4. 配置域名 — 添加您 funnel 中使用的所有子域名

### GA4 中的自定义事件

对于任何未被自动收集的事件，您可以在 GTM 中创建（推荐），或者直接使用 gtag 进行设置：

**通过 gtag 设置：**
```javascript
gtag('event', 'signup_completed', {
  method: 'email',
  user_id: 'usr_abc123',
  plan_name: "trial"
});
```

**通过 GTM 数据层设置（推荐 — 详见 GTM 部分）：**
```javascript
window.dataLayer.push({
  event: 'signup_completed',
  signup_method: 'email',
  user_id: 'usr_abc123'
});
```

### 转化事件配置

在 GA4 中将这些事件标记为转化事件 → 管理员 → 转化事件：
- `signup_completed`
- `checkout_completed`
- `demo_requested`
- `trial_started`（如果与注册是分开的事件）

**规则：**
- 每个属性最多只能标记 30 个转化事件 — 需要精心选择，不要随意标记所有事件
- 在 GA4 中，转化事件是追溯性的 — 启用某个转化事件后，其数据会覆盖过去 6 个月的记录
- 除非您正在针对这些微转化事件优化广告活动，否则不要将它们标记为转化事件

---

## Google Tag Manager （GTM）设置

### 容器结构

```
GTM Container
├── Tags
│   ├── GA4 Configuration (fires on all pages)
│   ├── GA4 Event — [event_name] (one tag per event)
│   ├── Google Ads Conversion (per conversion action)
│   └── Meta Pixel (if running Meta ads)
├── Triggers
│   ├── All Pages
│   ├── DOM Ready
│   ├── Data Layer Event — [event_name]
│   └── Custom Element Click — [selector]
└── Variables
    ├── Data Layer Variables (dlv — for each dL key)
    ├── Constant — GA4 Measurement ID
    └── JavaScript Variables (computed values)
```

### SaaS 应用的标签模式

**模式 1：数据层推送（最可靠的方式）**

您的应用程序将数据推送到数据层 → GTM 接收数据 → 然后发送到 GA4。

```javascript
// In your app code (on event):
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
  event: 'signup_completed',
  signup_method: 'email',
  user_id: userId,
  plan_name: "trial"
});
```

```
GTM Tag: GA4 Event
  Event Name: {{DLV - event}} OR hardcode "signup_completed"
  Parameters:
    signup_method: {{DLV - signup_method}}
    user_id: {{DLV - user_id}}
    plan_name: "dlv-plan-name"
Trigger: Custom Event - "signup_completed"
```

**模式 2：CSS 选择器点击**

用于由 UI 元素触发的事件，这些元素没有应用程序级别的监听器。

```
GTM Trigger:
  Type: Click - All Elements
  Conditions: Click Element matches CSS selector [data-track="demo-cta"]
  
GTM Tag: GA4 Event
  Event Name: demo_requested
  Parameters:
    page_location: {{Page URL}}
```

请参阅 [references/gtm-patterns.md](references/gtm-patterns.md) 以获取完整的配置模板。

---

## 平台特定的转化跟踪

### Google Ads

1. 在 Google Ads 中创建转化事件 → 工具 → 转化事件
2. 导入 GA4 的转化数据（推荐 — 保持数据的一致性）或使用 Google Ads 的标签
3. 设置归因模型：**数据驱动**（如果每月转化次数超过 50 次），否则使用 **最后一次点击** 的归因模型
4. 转化窗口：对于潜在客户生成，设置为 30 天；对于高考虑度的购买行为，设置为 90 天

### Meta（Facebook/Instagram）像素

1. 通过 GTM 安装 Meta 像素的基础代码
2. 标准事件：`PageView`、`Lead`、`CompleteRegistration`、`Purchase`
3. 强烈推荐使用转化 API（CAPI）——由于广告拦截器和 iOS 的原因，客户端像素可能会导致约 30% 的转化数据丢失
4. CAPI 需要服务器端实现（参考 Meta 的文档或 GTM 的服务器端设置）

---

## 跨平台跟踪

### UTM 规范

严格遵守 UTM 规范，否则您的渠道数据会变得混乱。

| 参数 | 规范 | 示例 |
|-----------|-----------|---------|
| `utm_source` | 平台名称（小写） | `google`、`linkedin`、`newsletter` |
| `utm_medium` | 流量类型 | `cpc`、`email`、`social`、`organic` |
| `utm_campaign` | 活动 ID 或名称 | `q1-trial-push`、`brand-awareness` |
| `utm_content` | 广告/创意内容 | `hero-cta-blue`、`text-link` |
| `utm_term` | 支付关键词 | `saas-analytics` |

**规则：** 不要对自然流量或直接流量使用 UTM 标签。UTM 标签会覆盖 GA4 的自动归因结果。

### 归因窗口

| 平台 | 默认归因窗口 | 对于 SaaS 应用的推荐归因窗口 |
|---------|---------------|---------------------|
| GA4 | 30 天 | 根据销售周期不同，归因窗口为 30-90 天 |
| Google Ads | 30 天 | 试用期间为 30 天，企业购买期间为 90 天 |
| Meta | 点击后 7 天，查看后 1 天 | 仅点击后 7 天 |
| LinkedIn | 30 天 | 30 天 |

### 跨域跟踪

对于跨域的 funnel（例如，`acme.com` → `app.acme.com`）：

1. 在 GA4 中 → 管理员 → 数据流 → 配置标签设置 → 列出不需要跟踪的域名 → 添加两个域名
2. 在 GTM 中 → GA4 配置 → 跨域测量 → 添加两个域名
3. 测试：访问域名 A，点击链接到域名 B，检查 GA4 的调试视图 — 会话不应重新开始

## 数据质量

### 数据去重

**事件被重复记录？** 常见原因：
- GTM 标签和硬编码的 gtag 同时触发
- 同一事件被多次触发（例如，通过 GTM 的增强测量功能和自定义 GTM 标签）
- 单页应用程序（SPA）在每次路由变化时触发页面视图事件，同时 GTM 也触发页面视图事件

解决方法：审核 GTM 预览中的重复记录情况。在开发者工具的网络标签页中检查重复的点击记录。

### 滤除机器人流量

GA4 会自动过滤机器人流量。对于内部流量：
1. 在 GA4 中 → 管理员 → 数据过滤器 → 内部流量
2. 添加您的办公室 IP 和开发者的 IP 地址
3. 启用过滤器（最初设置为测试模式，之后正式启用）

### 同意管理的影响

根据 GDPR/ePrivacy 法规，分析可能需要用户的同意。请做好相应的准备：

| 同意管理模式 | 影响 |
|---------------------|--------|
| **无同意模式** | 拒绝使用 Cookie 的访问者 → 没有数据记录 |
| **基本同意模式** | 拒绝同意的访问者 → 没有数据记录 |
| **高级同意模式** | 拒绝同意的访问者 → 使用已同意用户的数据（GA4 会根据这些用户的数据进行分析） |

**建议：** 通过 GTM 实现高级同意模式。这需要与同意管理平台（如 Cookiebot、OneTrust、Usercentrics 等）集成。

预计的同意率：欧盟地区为 60-75%，美国地区为 85-95%。

---

## 主动发现问题

以下情况需要主动发现并处理：

- **每个页面加载时都会触发事件** — 这可能是触发器配置错误的表现。标记为数据重复的问题。
- **没有传递 `user_id` | 这会导致无法将分析数据与 CRM 连接或无法分析用户群体。需要标记并修复。
- **GA4 和 Ads 的转化数据不一致** | 可能是归因窗口设置不正确或标签重复导致的。需要进行检查。
- **欧盟市场未配置同意模式** | 这可能导致法律问题以及数据记录不准确。需要立即处理。
- **所有页面显示为 “/(未设置)” 或通用路径** | 可能是单页应用程序的路由问题，导致 GA4 记录错误的页面。
- **付费广告的 UTM 来源显示为 “direct” | 可能是 UTM 标签缺失或被错误处理，导致流量归因错误。

---

## 输出结果

| 您请求的内容 | 您会得到的结果 |
|--------------------|-----------|
| “制定跟踪计划” | 事件分类表（事件 + 参数 + 触发器）、GA4 配置清单、GTM 容器结构 |
| “审核我的跟踪系统” | 与标准 SaaS funnel 的对比分析、数据质量评分（0-100 分）、优先级修复列表 |
| “设置 GTM” | 每个事件的标签/触发器/变量配置、容器设置清单 |
| “调试缺失的事件” | 使用 GTM 预览、GA4 调试视图和网络标签页进行结构化的调试步骤 |
| “设置转化跟踪” | GA4、Google Ads 和 Meta 的转化事件配置 |
| “生成跟踪计划” | 使用您的输入运行 `scripts/tracking_plan_generator.py` 脚本 |

---

## 沟通方式

所有输出都遵循以下结构化的沟通标准：
- **首先说明问题或需要完成的工作** |
- **详细说明问题、原因及解决方法** |
- **每项问题都明确负责人和截止日期** | 避免使用模糊的表述，如 “考虑实施”
- **对标签的准确性进行标注** — 使用 🟢 表示已验证，🟡 表示估计，🔴 表示假设

## 相关技能

- **campaign-analytics**：用于分析营销效果和渠道投资回报率。不用于跟踪系统的设置，而是用于分析数据的分析。
- **ab-test-setup**：用于设计实验。不用于事件跟踪的设置，但该技能中的事件可用于 A/B 测试。
- **analytics-tracking**：仅用于跟踪系统的设置。对于仪表盘和报告生成，使用 **campaign-analytics**。
- **seo-audit**：用于技术性的 SEO 优化。不用于分析跟踪，但两者都会使用 GA4 的数据。
- **gdpr-dsgvo-expert**：用于确保符合 GDPR 规范。该技能涉及同意模式的实施；而本技能则涉及整个合规框架的设置。