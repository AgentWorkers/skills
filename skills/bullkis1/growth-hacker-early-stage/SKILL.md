---
name: growth-hacker
description: 快速获取用户、实现用户增长循环、优化用户转化率以及开展增长实验。这些方法适用于以下场景：吸引首批用户、提升注册/激活率、设计推荐机制、进行A/B测试、制定产品分发策略，或是分析用户增长为何停滞不前。该工具专为产品早期阶段及独立开发产品的用户增长（从0用户到1000用户的阶段）设计。不适用于品牌策略（请使用“brand-guardian”工具）或内容创作（请使用“content-creator”工具）。
  Rapid user acquisition, viral loops, conversion optimization, and growth experiments.
  Use when working on: getting first users, improving signup/activation rates, building
  referral mechanics, A/B testing, distribution strategy, or figuring out why growth
  is stuck. Specializes in early-stage and indie product growth (0→1 and 1→10k users).
  NOT for brand strategy (use brand-guardian) or content creation (use content-creator).
---
# 成长黑客（Growth Hacker）

找到从零开始到获得用户关注的最快路径。无情地进行实验，专注于那些有效的方法。

## 思维方式（Mindset）

- 在产品早期阶段，推广策略比产品本身更重要。
- 测量一切数据，不要盲目假设。
- 一次只关注一个增长点——不要分散注意力。
- 先进行低成本实验，再尝试高成本的方案。
- 用户会向朋友推荐你的产品——这是最好的增长渠道。

## 成长框架（The Growth Framework）

### 第一步：诊断问题所在

常见的增长问题通常出现在以下阶段之一：
1. **获取用户（Acquisition）**——用户找不到你的产品。
2. **激活用户（Activation）**——用户找到了产品，但没有注册或完成入门流程。
3. **用户留存（Retention）**——用户注册后不再使用产品。
4. **用户推荐（Referral）**——用户使用了产品，但没有向他人推荐。
5. **收入生成（Revenue）**——有用户，但没有收入。

按照问题的严重程度依次解决这些问题。如果激活用户的流程有问题，就不要急于开展获取用户的营销活动。

### 第二步：选择一个关键指标来推动增长

定义“北极星指标”（North Star Metric，NSM）：这个指标最能反映产品所提供的价值。

示例：
- SaaS产品：每周完成核心操作的活跃用户数。
- 市场平台：每周的成功交易数量。
- 社区平台：每日来自回头用户的帖子数量。

### 第三步：先进行低成本实验

| 推广渠道 | 成本 | 效果速度 | 适合的产品类型 |
|---|---|---|---|
| Reddit（自然推广） | 免费 | 几天内见效 | 技术类或小众产品 |
| Twitter/X平台 | 免费 | 几小时内见效 | B2B产品、开发工具、行业资讯 |
| 冷启动邮件/LinkedIn推广 | 免费 | 几天内见效 | B2B产品、高价值产品 |
| Product Hunt活动 | 免费 | 1天内见效 | 开发工具、SaaS产品 |
| Hacker News展示 | 免费 | 1天内见效 | 开发工具、开源项目 |
| 内容SEO优化 | 免费，效果较慢 | 需数月时间 | 长期效果 |
| 广告推广 | 需付费 | 立即见效 | 当自然推广效果不佳时使用 |

有关每个渠道的具体操作指南，请参阅 `references/channel-playbooks.md`。

### 第四步：建立用户推荐机制

最好的增长方式是让用户自发推荐产品：
- **病毒系数（Viral Coefficient）> 1** → 实现指数级增长。
- **病毒系数 = 0.5** → 仍然值得推广——因为可以降低客户获取成本（CAC）。

简单的推荐机制：
1. 用户邀请朋友使用产品 → 双方都能获得好处。
- 在用户使用的产品页面上标注“由X技术支持”或“使用X工具制作”。
- 在产品中添加分享按钮，方便用户分享使用体验。
- 设置推荐奖励机制（如加入等待名单后解锁额外功能）。

## 提高转化率的快速方法

**着陆页优化（典型的易改进点）：**
- 着陆页顶部有一个明确的呼叫行动按钮（CTA）。
- 在CTA附近展示用户评价、数据或案例。
- 移除着陆页上的导航链接。
- 标题要突出展示用户使用产品后的实际成果，而不是产品功能。
- 添加常见问题解答（FAQ）以消除用户的疑虑。

**入门流程优化：**
- 减少用户完成首次使用的步骤。
- 提供预填充的示例数据，让用户感觉操作流程不繁琐。
- 当用户完成首次使用后，及时发送庆祝邮件。
- 如果用户24小时内未再次使用产品，发送提醒邮件。

## A/B测试

只有在流量足够大（每周每个实验变体至少有100次转化）时，才进行A/B测试：
```
Minimum sample size per variant: 
  n = (16 × σ²) / δ²
  Rule of thumb: 100+ conversions before reading results
```

可用工具：Vercel Edge Config + 标志设置、Posthog功能标志、GrowthBook（开源工具）。

## 从第一天起就需要跟踪的指标

```
Acquisition: Visits, signups, CAC per channel
Activation: % completing core action within 24h
Retention: D1, D7, D30 retention
Referral: Viral coefficient (invites sent × invite conversion rate)
Revenue: MRR, ARPU, churn rate
```

## 重要规则

- 在激活率低于40%之前，**绝对不要**投放广告。
- **务必**记录每个用户的注册来源和推广渠道。
- **不要**只针对注册用户进行优化，而要针对实际使用产品的用户进行优化。
- **一定要**与那些不再使用产品的用户沟通（而不仅仅是那些满意的用户）。

## 参考资料

- `references/channel-playbooks.md` — 提供了关于Reddit、Hacker News、Product Hunt、冷启动邮件和Twitter推广策略的详细指南。