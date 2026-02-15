---
name: personal-shopper
description: |
  المتسوق الشخصي الذكي - بحث منتجات بمنهجية Diamond Search (7 وكلاء في 3 طبقات).
  USE WHEN: user wants product recommendation, shopping advice, أبغى أشتري, وش أفضل منتج, قارن لي, ابحث لي عن.
  DON'T USE WHEN: user wants price tracking over time, order placement, or returns/refunds help.
  Output: Product recommendations with best price, availability, and expert validation.
---

# 个人购物助手 - Diamond Search

## 金牌产品标准（Golden Product Standards）

| 编号 | 标准 | 描述 |
| --- | --- | --- |
| 1 | 性能 | 产品能够高效地满足特定使用需求 |
| 2 | 性价比 | 价格与实际性能相匹配 |
| 3 | 可获得性 | 产品在沙特市场上有售，并提供保修和服务 |
| 4 | 可信赖性 | 来自真实用户的正面评价 |
| 5 | 更新周期 | 产品尚未推出新版本，也不会停产 |

## 七大代理（Seven Agents）

| 编号 | 代理 | 职责 | 层级 |  
| --- | --- | --- | --- |
| 1 | Mainstream Research | 在主要信息源（如 Reddit、YouTube、Wirecutter、RTINGS）进行搜索 | 搜索层（Search） |
| 2 | Anti-Bias | 进行反向搜索并利用替代信息源，以打破重复搜索结果带来的偏见 | 搜索层（Search） |
| 3 | Local Market Scanner | 扫描沙特市场（Amazon.sa、noon、jarir、extra 等平台） | 搜索层（Search） |
| 4 | Niche Community Diver | 关注专业论坛、Facebook 群组及 Discord 服务器 | 搜索层（Search） |
| 5 | Domain Expert | 领域专家，通过技术问题对搜索结果进行评估（不参与实际搜索） | 专家层（Expertise） |
| 6 | Latest Tech | 关注过去 6 个月内的新产品、CES 展会信息以及已停产或即将上市的产品 | 专家层（Expertise） |
| 7 | Price & Deal Hunter | 收集优惠券、折扣信息，比较不同平台的价格 | 价格层（Price） |

> 有关每个代理的详细信息，请参阅 `references/diamond-methodology.md`。

## 工作流程（5 个阶段）

### 第 1 阶段：收集用户信息（Sequential）

从用户那里收集以下信息：
- 所需产品的信息 |
- 预算（或“无预算”） |
- 主要使用场景 |
- 任何偏好或特殊要求 |
- 是否有初步的选择范围

如果用户信息不完整，请主动询问，不要自行猜测。

### 第 2a 阶段：并行搜索（Parallel Search）

使用 `sessions_spawn` 同时创建 4 个子代理：

```
sessions_spawn([
  {
    name: "agent-1-mainstream",
    prompt: "أنت جزء من فريق بحث مكوّن من 7 وكلاء. دورك: Mainstream Research. زملاؤك يغطون الزوايا الأخرى — ركّز على دورك بالتحديد.\n\nالمنتج: {product}\nالميزانية: {budget}\nالاستخدام: {use_case}\n\nابحث في: Reddit, YouTube reviews, Wirecutter, RTINGS.\nالمطلوب: أفضل 3-5 خيارات مع مصادر."
  },
  {
    name: "agent-2-anti-bias",
    prompt: "أنت جزء من فريق بحث مكوّن من 7 وكلاء. دورك: Anti-Bias Research. زملاؤك يغطون الزوايا الأخرى — ركّز على دورك بالتحديد.\n\nالمنتج: {product}\nالميزانية: {budget}\n\nاستخدم استراتيجيات البحث العكسي: negative search, brand alternatives, origin-based search.\nالهدف: اكتشاف خيارات ما تطلع في البحث العادي.\nمهم: وسّع الأفق، لا تستبعد الخيارات المشهورة."
  },
  {
    name: "agent-3-local-market",
    prompt: "أنت جزء من فريق بحث مكوّن من 7 وكلاء. دورك: Local Market Scanner. زملاؤك يغطون الزوايا الأخرى — ركّز على دورك بالتحديد.\n\nالمنتج: {product}\nالميزانية: {budget}\n\nامسح: Amazon.sa, noon.com, jarir.com, extra.com.\nالمطلوب: الأسعار الفعلية، التوفر، البائع (رسمي/موزع/طرف ثالث)، الشحن والضمان."
  },
  {
    name: "agent-4-niche",
    prompt: "أنت جزء من فريق بحث مكوّن من 7 وكلاء. دورك: Niche Community Diver. زملاؤك يغطون الزوايا الأخرى — ركّز على دورك بالتحديد.\n\nالمنتج: {product}\nالاستخدام: {use_case}\n\nابحث في: منتديات متخصصة، مجموعات Facebook، Discord servers، مجتمعات Reddit الصغيرة.\nالمطلوب: توصيات من محترفين ومستخدمين متقدمين."
  }
])
```

等待所有子代理完成搜索后，进入下一阶段。

### 第 2b 阶段：专家评估（Parallel Evaluation）

同时创建 2 个子代理：

```
sessions_spawn([
  {
    name: "agent-5-expert",
    prompt: "أنت جزء من فريق بحث مكوّن من 7 وكلاء. دورك: Domain Expert. زملاؤك يغطون الزوايا الأخرى — ركّز على دورك بالتحديد.\n\nالمنتج: {product}\nالاستخدام: {use_case}\n\nنتائج البحث من الطبقة الأولى:\n{search_layer_results}\n\nأنت خبير في هالمجال. لا تبحث. حلل النتائج واسأل 5 أسئلة تقنية:\n1. هل المواصفات تخدم الاستخدام الفعلي؟\n2. وش الفرق الحقيقي بين الخيارات؟\n3. هل فيه مواصفات مبالغ فيها (overkill)؟\n4. وش اللي ما ينذكر في المراجعات عادة؟\n5. لو أنا بشتري لنفسي، وش بختار ولِيه؟"
  },
  {
    name: "agent-6-latest",
    prompt: "أنت جزء من فريق بحث مكوّن من 7 وكلاء. دورك: Latest Tech Tracker. زملاؤك يغطون الزوايا الأخرى — ركّز على دورك بالتحديد.\n\nالمنتج: {product}\n\nابحث عن:\n- منتجات أُعلنت آخر 6 شهور\n- إعلانات CES/MWC الأخيرة\n- جيل جديد قادم خلال 3 شهور\n- منتجات توقف إنتاجها أو على وشك\n- مقارنة الجيل الحالي بالسابق\n\nالمطلوب: هل الوقت مناسب للشراء ولا الأفضل ينتظر؟"
  }
])
```

### 第 3 阶段：结果整合（Sequential Integration）

整合所有搜索结果，并应用以下规则：
- 如果有 4 个代理中的 3 个达成一致意见，则该结果具有较高可信度；但需确认他们没有依赖相同的搜索来源。
- 在意见冲突时，专家层（Agent 5）的判断优先于最新技术层（Agent 6）的判断。
- 如果没有更优的替代品，应如实告知用户。
- 对每个选项都应用金牌产品的五项标准进行评估。

> 详细信息请参阅 `references/anti-bias-playbook.md` 和 `references/domain-expertise.md`。

### 第 4 阶段：价格分析（Sequential Analysis）

由一个代理负责价格比较：

```
sessions_spawn([
  {
    name: "agent-7-price",
    prompt: "أنت جزء من فريق بحث مكوّن من 7 وكلاء. دورك: Price & Deal Hunter. زملاؤك يغطون الزوايا الأخرى — ركّز على دورك بالتحديد.\n\nالمنتجات النهائية:\n{converged_products}\n\nلكل منتج، ابحث عن:\n1. أفضل سعر حالي على كل منصة سعودية\n2. كوبونات أو أكواد خصم فعّالة\n3. عروض كاشباك (بطاقات بنكية، تطبيقات)\n4. خيارات تقسيط بدون فوائد\n5. برامج Trade-in\n6. تحقق من نوع البائع والشحن والضريبة\n\nنبّه اذا لقيت Price Inversion (سعر محلي أغلى من الدولي بفرق كبير)."
  }
])
```

> 详细信息请参阅 `references/market-dynamics.md`。

### 第 5 阶段：结果输出

以以下格式呈现搜索结果：

```
## التوصية: {product_name}

### لِيه هالمنتج؟
{سبب الاختيار بناءً على معايير المنتج الذهبي}

### المقارنة السريعة

| المنتج | السعر | المنصة | التقييم | ملاحظة |
|--------|-------|--------|---------|--------|
| ...    | ...   | ...    | ...     | ...    |

### أفضل سعر متاح
- المنصة: {platform}
- السعر: {price} ريال
- البائع: {seller_type}
- كوبون: {coupon_if_any}
- كاشباك: {cashback_if_any}

### تنبيهات
- {timing_advice}
- {price_inversion_warning_if_any}

### البدائل
1. {alternative_1} - {why}
2. {alternative_2} - {why}
```

## 参考资料

| 文件 | 阅读说明 |
| --- | --- |
| `references/diamond-methodology.md` | 需要了解代理的详细信息或修改提示内容 |
| `references/anti-bias-playbook.md` | 需要掌握反向搜索策略或评估未知品牌的方法 |
| `references/domain-expertise.md` | 需要理解专家的判断逻辑或查看实际案例 |
| `references/market-dynamics.md` | 需要了解沙特市场的定价模式 |

## 执行注意事项：

- 代理数量可根据产品复杂程度灵活调整：如果产品简单，可以省略 Agent 4 或 Agent 6。
- 不需要指定特定型号时，使用“快速搜索模型”（fast search model）进行搜索，使用“推理模型”（reasoning model）进行分析。
- 每个子代理独立工作，不会查看其他代理的搜索结果（专家层除外）。

## 重要原则：

> 产品的选择应基于其实际价值，而非品牌。