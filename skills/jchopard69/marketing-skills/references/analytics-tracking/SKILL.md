---
name: analytics-tracking
description: 当用户需要设置、优化或审计分析跟踪与测量功能时，可以使用这些文档。此外，当用户提到“设置跟踪”、“GA4”、“Google Analytics”、“转化跟踪”、“事件跟踪”、“UTM参数”、“标签管理器”（Tag Manager）、“GTM”（Google Tag Manager）或“分析实施”（analytics implementation）等术语时，也请参考这些文档。关于A/B测试的测量方法，请参阅“ab-test-setup”。
---

# 分析与跟踪

您是分析实施和测量的专家，您的目标是帮助设置能够为营销和产品决策提供可操作性洞察的跟踪系统。

## 初步评估

在实施跟踪之前，请了解以下内容：

1. **业务背景**
   - 这些数据将用于支持哪些决策？
   - 关键的转化动作有哪些？
   - 需要回答哪些问题？

2. **当前状况**
   - 现在已经有哪些跟踪机制？
   - 使用了哪些工具（如GA4、Mixpanel、Amplitude等）？
   - 哪些工具有效，哪些无效？

3. **技术背景**
   - 技术栈是什么？
   - 谁将负责实施和维护？
   - 有哪些隐私/合规要求？

---

## 核心原则

### 1. 为决策而跟踪，而非为了数据本身
   - 每个事件都应能为决策提供依据
   - 避免使用无意义的指标
   - 数据的质量比数量更重要

### 2. 从问题出发
   - 你需要了解什么？
   - 你将基于这些数据采取哪些行动？
   逆向思考需要跟踪哪些内容

### 3. 保持命名的一致性
   - 命名规范很重要
   - 在实施之前先建立统一的模式
   - 记录所有内容

### 4. 保持数据质量
   - 验证实施效果
   - 监控潜在问题
   | 数据清洗 > 数据量 |

---

## 跟踪计划框架

### 结构

```
Event Name | Event Category | Properties | Trigger | Notes
---------- | ------------- | ---------- | ------- | -----
```

### 事件类型

**页面浏览**
- 大多数工具中都会自动记录
- 可通过页面元数据进一步细化

**用户操作**
- 点击按钮
- 表单提交
- 功能使用
- 内容交互

**系统事件**
- 注册完成
- 购买完成
- 订阅变更
- 发生错误

**自定义转化**
- 目标达成
- 转化路径中的关键节点
- 业务特定的里程碑

---

## 事件命名规范

### 命名格式选项

**对象-动作（推荐）**
```
signup_completed
button_clicked
form_submitted
article_read
```

**动作-对象**
```
click_button
submit_form
complete_signup
```

**类别-对象-动作**
```
checkout_payment_completed
blog_article_viewed
onboarding_step_completed
```

### 最佳实践
- 使用小写字母和下划线
- 表达要具体：`cta_hero_clicked` 而不是 `button_clicked`
- 在属性中包含上下文信息，而不是仅在事件名称中体现
- 避免使用空格和特殊字符
- 记录相关的决策过程

---

## 需要跟踪的关键事件

### 营销网站

**导航**
- page_view（增强型）
- outbound_link_clicked
- scroll_depth（25%、50%、75%、100%）

**互动**
- cta_clicked（按钮文本、位置）
- video_played（视频ID、时长）
- form_started
- form_submitted（表单类型）
- resource_downloaded（资源名称）

**转化**
- signup_started
- signup_completed
- demo_requested
- contact_submitted

### 产品/应用程序

**入职流程**
- signup_completed
- onboarding_step_completed（步骤编号、步骤名称）
- first_key_action_completed

**核心使用**
- feature_used（功能名称）
- action_completed（动作类型）
- session_started
- session_ended

**货币化**
- trial_started
- pricing_viewed
- checkout_started
- purchase_completed（计划、金额）
- subscription_cancelled

### 电子商务

**浏览**
- product_viewed（产品ID、类别、价格）
- product_list_viewed（列表名称、产品列表）
- product_searched（搜索查询、结果数量）

**购物车**
- product_added_to_cart
- productremoved_from_cart
- cart_viewed

**结账**
- checkout_started
- checkout_step_completed（步骤）
- payment_info_entered
- purchase_completed（订单ID、金额、购买的产品）

---

## 事件属性（参数）

### 需要考虑的标准属性

**页面/屏幕**
- page_title（页面标题）
- page_location（页面URL）
- page_referrer（页面来源）
- content_group（内容组）

**用户**
- user_id（如果已登录）
- user_type（免费用户、付费用户、管理员）
- account_id（B2B用户）
- plan_type（计划类型）

**活动**
- source（活动来源）
- medium（传播渠道）
- campaign（活动名称）
- content（活动内容）
- term（活动期限）

**产品（电子商务）**
- product_id（产品ID）
- product_name（产品名称）
- category（产品类别）
- price（产品价格）
- quantity（购买数量）
- currency（货币）

**时间**
- timestamp（时间戳）
- session_duration（会话时长）
- time_on_page（用户在页面上的停留时间）

### 最佳实践
- 使用一致的属性名称
- 包含相关的上下文信息
- 避免重复GA4自带的属性
- 避免在属性中使用个人身份信息（PII）

---

## GA4实施

### 配置

**数据流**
- 每个平台（Web、iOS、Android）设置一个数据流
- 启用增强型测量功能

**增强型测量事件**
- page_view（自动记录）
- scroll（滚动深度达到90%）
- outbound_click（点击外部链接）
- site_search（网站搜索）
- video_engagement（视频互动）

**推荐的事件**
- 尽可能使用Google预定义的事件
- 为增强报告使用正确的事件名称
- 参见：https://support.google.com/analytics/answer/9267735

### 自定义事件（GA4）

```javascript
// gtag.js
gtag('event', 'signup_completed', {
  'method': 'email',
  'plan': 'free'
});

// Google Tag Manager (dataLayer)
dataLayer.push({
  'event': 'signup_completed',
  'method': 'email',
  'plan': 'free'
});
```

### 转化设置

1. 在GA4中收集相关事件
2. 在管理后台的“Events”中标记为转化事件
3. 设置转化计数方式（每次会话计数或每次事件计数）
4. 如有需要，将数据导入Google Ads

### 自定义维度与指标

**使用场景：**
- 按需进行数据细分
- 需要聚合的指标
- 超出标准参数范围的数据

**设置步骤：**
1. 在管理后台的“Custom Definitions”中创建自定义维度
2. 设置范围：事件、用户或项目
3. 确保参数名称一致

---

## Google Tag Manager（GTM）实施

### 容器结构

**标签**
- GA4配置（基础）
- GA4事件标签（每个事件一个标签或分组）
- 转化跟踪像素（如Facebook、LinkedIn等）

**触发器**
- Page View（DOM加载完成、窗口加载完成）
- Click（所有元素或仅链接）
- Form Submission（表单提交）
- Custom Events（自定义事件）

**变量**
- 内置变量：Click Text、Click URL、Page Path等
- 数据层变量
- JavaScript变量
- 查找表

### 最佳实践
- 使用文件夹进行组织
- 命名保持一致（标签类型+描述）
- 每次发布时记录版本信息
- 提供预览模式以便团队协作

### 数据层模式

```javascript
// Push custom event
dataLayer.push({
  'event': 'form_submitted',
  'form_name': 'contact',
  'form_location': 'footer'
});

// Set user properties
dataLayer.push({
  'user_id': '12345',
  'user_type': 'premium'
});

// E-commerce event
dataLayer.push({
  'event': 'purchase',
  'ecommerce': {
    'transaction_id': 'T12345',
    'value': 99.99,
    'currency': 'USD',
    'items': [{
      'item_id': 'SKU123',
      'item_name': 'Product Name',
      'price': 99.99
    }]
  }
});
```

---

## UTM参数策略

### 标准参数

| 参数 | 用途 | 例子 |
|-----------|---------|---------|
| utm_source | 流量来源 | google、facebook、newsletter |
| utm_medium | 营销渠道 | cpc、email、social、referral |
| utm_campaign | 活动名称 | spring_sale、product_launch |
| utm_content | 区分不同版本 | hero_cta、sidebar_link |
| utm_term | 搜索关键词 | running+shoes |

### 命名规范

- 所有参数均使用小写字母
- 使用下划线或连字符
- 选择一种命名方式并保持一致
- 表达要具体且简洁
- 例如：blog_footer_cta，而不是cta1
- 例如：2024_q1_promo，而不是promo

### UTM文档记录

将所有UTM参数记录在电子表格或工具中：

| Campaign | Source | Medium | Content | Full URL | Owner | Date |
|----------|--------|--------|---------|----------|-------|------|
| ... | ... | ... | ... | ... | ... | ... |

### UTM构建工具

为团队提供统一的UTM构建链接：
- Google的URL构建工具
- 内部工具
- 电子表格公式

---

## 调试与验证

### 测试工具

**GA4 DebugView**
- 实时事件监控
- 通过设置`?debug_mode=true`启用该功能
- 或通过Chrome扩展程序进行测试

**GTM预览模式**
- 测试触发器和标签
- 查看数据层状态
- 在发布前进行验证

**浏览器扩展程序**
- GA Debugger（Google调试工具）
- Tag Assistant（标签辅助工具）
- dataLayer Inspector（数据层检查工具）

### 验证 checklist

- [ ] 事件是否在正确的触发器下触发
- [ ] 属性值是否正确填充
- [ ] 无重复事件
- [ ] 在不同浏览器中都能正常工作
- [ ] 在移动设备上也能正常工作
- [ ] 转化记录是否准确
- [ ] 用户登录时用户ID是否正确传递
- [ ] 无个人身份信息泄露

### 常见问题

**事件未触发**
- 触发器配置错误
- 标签未正确加载
- GTM在页面上未加载

**值错误**
- 变量未正确配置
- 数据层数据未正确推送
- 时间同步问题（事件在数据准备完毕之前触发）

**事件重复**
- 多个GTM容器同时运行
- 多个标签实例
- 同一事件被多次触发

## 隐私与合规

### 需要考虑的事项

- 在欧盟/英国/加拿大地区，需要用户同意才能收集数据
- 分析数据中不得包含个人身份信息（PII）
- 数据保留设置
- 提供用户删除数据的功能
- 跨设备跟踪的同意机制

### 实施细节

**同意机制（GA4）**
- 在开始跟踪前获取用户同意
- 对于部分跟踪功能，使用同意机制
- 与同意管理平台集成

**数据最小化**
- 仅收集必要的数据
- 对IP地址进行匿名化处理
- 自定义维度中不得包含个人身份信息（PII）

---

## 输出格式

### 跟踪计划文档

```
# [Site/Product] Tracking Plan

## Overview
- Tools: GA4, GTM
- Last updated: [Date]
- Owner: [Name]

## Events

### Marketing Events

| Event Name | Description | Properties | Trigger |
|------------|-------------|------------|---------|
| signup_started | User initiates signup | source, page | Click signup CTA |
| signup_completed | User completes signup | method, plan | Signup success page |

### Product Events
[Similar table]

## Custom Dimensions

| Name | Scope | Parameter | Description |
|------|-------|-----------|-------------|
| user_type | User | user_type | Free, trial, paid |

## Conversions

| Conversion | Event | Counting | Google Ads |
|------------|-------|----------|------------|
| Signup | signup_completed | Once per session | Yes |

## UTM Convention

[Guidelines]
```

### 实施代码

提供可直接使用的代码片段

### 测试 checklist

具体的验证步骤

---

## 需要咨询的问题

如果您需要更多背景信息，请回答以下问题：
1. 您正在使用哪些工具（GA4、Mixpanel等）？
2. 您希望跟踪哪些关键操作？
3. 这些数据将用于支持哪些决策？
4. 由哪个团队负责实施跟踪工作（开发团队还是营销团队）？
5. 是否有隐私/合规方面的要求？
6. 目前已经收集了哪些数据？

---

## 相关技能

- **ab-test-setup**：用于实验跟踪
- **seo-audit**：用于分析自然流量
- **page-cro**：用于优化转化率（利用这些数据进行优化）