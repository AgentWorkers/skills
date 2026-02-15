# social-proof-generator

该工具用于生成并维护所有产品的社交证明元素（用户评价、使用统计数据、信任徽章）。

## 概述

该工具收集真实的使用数据，生成社交证明内容，并为产品着陆页创建可嵌入的组件。社交证明能够将转化率提升15-30%。

## 使用方法

- `social proof PRODUCT-SLUG`：为指定产品生成社交证明元素
- `social proof stats`：更新所有产品的实时使用统计信息
- `social proof testimonials PRODUCT-SLUG`：收集并格式化用户评价
- `social proof badges PRODUCT-SLUG`：生成信任徽章组件

## 社交证明类型

### 1. 实时使用统计信息
跟踪并显示以下真实数据：
- “今日转换的文件数量”
- “本月使用的用户数量”
- “总转化次数”

数据来源：产品分析数据或Stripe的客户数量
请求地址：`POST http://host.docker.internal:18790/stripe-query`
请求头：
  - `Content-Type: application/json`
  - `X-Bridge-Secret: DEPLOY_BRIDGE_SECRET`
请求体：
  ```json
  {
    "type": "customers",
    "product": "PRODUCT-SLUG"
  }
  ```

### 2. 用户评价收集
评价来源：
- Stripe用户的正面评价
- GitHub上的星标和正面问题反馈
- 社交媒体上的提及（通过网络搜索）
- 直接提交的反馈

每条评价的格式：
- 引用（最多2句话）
- 评价者姓名或“已验证用户”
- 如果有的话，还包括其角色或公司名称
- 星级评分（1-5分）

### 3. 信任徽章
根据真实数据生成徽章：
- “提供永久免费计划”
- “无需信用卡”
- “采用256位SSL加密”
- “99.9%的在线时间”
- “被X+名专业人士使用”
- “用户评分4.8/5”

### 4. 活动动态通知（防止错过机会）
生成最近的活动通知：
- “纽约的用户刚刚转换了一个文件”
- “目前有12人正在使用该工具”

这些通知使用的是匿名数据，不会显示真实姓名

## 输出结果

为每个产品生成以下文件：
- `src/components/SocialProofBar.tsx`（计数条）
- `src/components/Testimonials.tsx`（评价轮播组件）
- `src/components/TrustBadges.tsx`（信任徽章组件）
- `src/components/ActivityFeed.tsx`（实时活动弹窗）
- `src/data/social-proof.json`（所有收集到的证明数据）

## 规则

- **仅使用真实数据**，严禁伪造评价或夸大数字
- 如果没有真实评价，可使用使用统计数据代替
- 数字需四舍五入到最接近的整数：例如“47名用户”应显示为“45+用户”
- 每周更新一次社交证明数据
- 存档旧评价，仅显示最新的5条最佳评价
- 未经用户同意，严禁使用真实姓名，默认显示为“已验证用户”

## 集成方式

- 从`user-feedback-collector`技能中获取正面反馈
- 从Stripe订阅者数据中更新统计信息
- 通过`deploy bridge`推送更新后的组件
- 每周运行一次以刷新统计信息