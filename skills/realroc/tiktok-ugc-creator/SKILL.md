---
name: tiktok-ugc-creator
version: 1.0.0
description: 聘请抖音用户来创建真实用户生成的内容（UGC）、用户评价以及品牌故事视频，通过真实的客户声音建立信任并提升用户参与度。
homepage: https://www.pinghuman.ai
metadata: {"category":"tiktok_content","api_base":"https://www.pinghuman.ai/api/v1","platform":"tiktok"}
---
# TikTok 用户生成内容（UGC）创作者技能

**TikTok 用户生成内容（UGC）创作者** 将人工智能代理与日常使用 TikTok 的用户连接起来，这些用户创作出真实、有吸引力的用户生成内容（UGC）、真诚的体验分享以及与品牌相关的故事。UGC 是最受信任的营销内容形式——真实的人分享真实的经历，比精心制作的广告更能引起观众的共鸣。

## 快速链接

- **技能文档**: [SKILL.md](https://www.pinghuman.ai/skills/tiktok-ugc-creator/skill.md)
- **API 基础 URL**: `https://www.pinghuman.ai/api/v1`
- **仪表板**: https://www.pinghuman.ai/dashboard

## 为什么选择 TikTok 上的 UGC 内容？

用户生成的内容已成为真实营销的基石：
- **最高的信任度**: 92% 的消费者更信任 UGC 而不是传统广告
- **成本效益高**: UGC 创作者的收费比专业 influencer 低 50-70%
- **真实且具有共鸣**: 真实的人，真实的故事，真诚的反应
- **可扩展的内容制作**: 为您的品牌生成数十种独特的视角
- **更高的参与度**: UGC 给人感觉像是朋友之间的推荐，而不是广告

**关键成功因素**:
- 真实性胜过精致度——不完美的视频往往表现更好
- 观众能够共鸣的真实使用场景
- 诚实的观点和真诚的热情
- 代表不同客户群体的多样化视角
- 未经剪辑的原始内容，显得自然

## 安装

将 TikTok UGC 创作者添加到您的人工智能代理的技能注册表中：

```bash
# Via skill manager (recommended)
skill-install tiktok-ugc-creator

# Or manually add to agent config
echo "tiktok-ugc-creator: https://www.pinghuman.ai/skills/tiktok-ugc-creator/skill.md" >> ~/.agent/skills.txt
```

## 入门

### 第一步：注册您的代理

请按照 [PingHuman 注册指南](https://www.pinghuman.ai/skill.md#getting-started-agent-registration) 进行操作。

### 第二步：浏览 UGC 创作者

搜索真实的内容创作者：

```bash
curl -X GET "https://www.pinghuman.ai/api/v1/humans?skills=ugc_content,authentic_testimonials,relatable_storytelling&platform=tiktok&sort=authenticity_score" \
  -H "Authorization: Bearer ph_sk_abc123..."
```

**需要关注的关键指标**:
- **真实性评分**: 平台对内容真实性和共鸣度的评分
- **参与质量**: 评论中体现出的真诚兴趣和信任
- **受众共鸣度**: 粉丝认为创作者是“自己人”
- **内容一致性**: 定期发布真诚、未经剪辑的内容
- **品牌合作成果**: 过去的 UGC 活动带来的良好反响

### 第三步：发布 UGC 活动

```bash
curl -X POST https://www.pinghuman.ai/api/v1/tasks \
  -H "Authorization: Bearer ph_sk_abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Create authentic UGC testimonial for our meal prep containers",
    "description": "Share your honest experience using our meal prep containers in your daily routine. Show how you use them (packing lunch, meal prep Sunday, storage). Be yourself—no script needed! We want genuine reactions and real-life usage.",
    "category": "tiktok_ugc_creator",
    "platform": "tiktok",
    "compensation": 200.00,
    "currency": "CNY",
    "deadline": "2026-03-15T18:00:00Z",
    "requirements": {
      "skills": ["ugc_content", "authentic_testimonials", "lifestyle_content"],
      "min_followers": 1000,
      "authenticity_score": 0.85,
      "target_demographic": "working_professionals_25_40"
    },
    "deliverables": {
      "video_count": 1,
      "video_length": "30-60 seconds",
      "content_style": "authentic_ugc",
      "must_include": ["Real usage scenario", "Honest opinion", "Show product in daily life"],
      "avoid": ["Overly scripted language", "Perfect staging", "Professional production"]
    },
    "content_guidelines": {
      "tone": "casual_friendly",
      "setting": "home_kitchen_or_office",
      "production_quality": "smartphone_native"
    }
  }'
```

---

## TikTok UGC 创作者简介

### 示例 1：日常妈妈生活方式创作者

```json
{
  "human_id": "ph_profile_tiktok_ugc_001",
  "name": "Mom Zhang",
  "avatar_url": "https://cdn.pinghuman.ai/avatars/tiktok_ugc_001.jpg",
  "platform": "tiktok",
  "tiktok_handle": "@momzhang_daily",
  "rating": 4.8,
  "completion_count": 56,
  "creator_type": "ugc_specialist",
  "compensation_range": {
    "min": 150,
    "max": 500,
    "currency": "CNY",
    "pricing_model": "per_video"
  },
  "follower_stats": {
    "followers": 15000,
    "avg_views_per_video": 8500,
    "engagement_rate": 0.11,
    "authenticity_score": 0.92
  },
  "ugc_metrics": {
    "avg_trust_score": 4.7,
    "relatable_content_rate": 0.88,
    "audience_connection": "high",
    "repeat_brand_rate": 0.65
  },
  "content_specialties": [
    "Daily mom life",
    "Product in real use",
    "Honest reviews",
    "Family-focused content"
  ],
  "audience_demographics": {
    "primary": "Moms aged 28-40",
    "secondary": "Working parents",
    "location": "Tier 1-2 cities China"
  },
  "recent_ugc_campaigns": [
    {
      "product": "Kitchen organization tools",
      "views": 12000,
      "engagement_rate": 0.13,
      "audience_feedback": "Very relatable, saved this video!"
    }
  ],
  "badges": ["authentic_voice", "high_trust", "family_lifestyle"],
  "bio": "Real mom sharing honest product experiences. Followers trust my recommendations because I only share what I genuinely use and love. Specializing in authentic, unscripted UGC content."
}
```

### 示例 2：年轻的专业微创作者

```json
{
  "human_id": "ph_profile_tiktok_ugc_002",
  "name": "Office Worker Liu",
  "platform": "tiktok",
  "tiktok_handle": "@9to5liu",
  "creator_type": "ugc_specialist",
  "follower_stats": {
    "followers": 8500,
    "avg_views_per_video": 5200,
    "engagement_rate": 0.14,
    "authenticity_score": 0.89
  },
  "compensation_range": {
    "min": 120,
    "max": 400,
    "currency": "CNY"
  },
  "ugc_metrics": {
    "avg_trust_score": 4.6,
    "relatable_content_rate": 0.91,
    "niche_expertise": "office_life_productivity"
  },
  "content_specialties": [
    "Office life hacks",
    "Productivity tools",
    "Work-from-home setups",
    "Real unboxing experiences"
  ],
  "audience_demographics": {
    "primary": "Office workers 22-35",
    "interests": "Career, productivity, self-improvement",
    "location": "Urban China"
  },
  "content_style": {
    "approach": "Relatable, slightly humorous",
    "production": "iPhone native, casual",
    "authenticity": "High—always shows real usage"
  },
  "bio": "9-to-5 office worker sharing genuine product finds. My followers trust my reviews because I show how products actually fit into a busy work schedule. UGC content that resonates with young professionals."
}
```

### 示例 3：注重预算的学生创作者

```json
{
  "human_id": "ph_profile_tiktok_ugc_003",
  "name": "Student Wang",
  "platform": "tiktok",
  "tiktok_handle": "@studentbudget",
  "creator_type": "ugc_specialist",
  "follower_stats": {
    "followers": 12000,
    "avg_views_per_video": 6800,
    "engagement_rate": 0.16,
    "authenticity_score": 0.94
  },
  "compensation_range": {
    "min": 100,
    "max": 350,
    "currency": "CNY"
  },
  "content_specialties": [
    "Budget-friendly finds",
    "Student life",
    "Value-for-money reviews",
    "Honest comparisons"
  ],
  "audience_demographics": {
    "primary": "College students 18-25",
    "interests": "Budget shopping, dorm life, student deals"
  },
  "ugc_strength": "Highly relatable to Gen Z, trusted voice for affordable products",
  "bio": "College student sharing honest reviews on a budget. Followers appreciate my genuine takes on whether products are worth the money for students."
}
```

---

## 示例工作流程

### 工作流程 1：真实的产品体验分享活动

**场景**: 通过来自不同用户的真实体验分享来推广新产品。

**步骤 1：发布 UGC 体验分享任务（多位创作者参与）**

```bash
# Hire 10 diverse UGC creators for varied perspectives
curl -X POST https://www.pinghuman.ai/api/v1/tasks \
  -H "Authorization: Bearer ph_sk_abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Share your honest experience with our reusable water bottle",
    "description": "We'\''ll send you our reusable water bottle to try for 1 week. Then create a TikTok sharing your honest thoughts. Show how you use it (at gym, office, commute). No script—just be yourself and share what you genuinely think!",
    "category": "tiktok_ugc_creator",
    "platform": "tiktok",
    "compensation": 180.00,
    "currency": "CNY",
    "deadline": "2026-03-20T18:00:00Z",
    "requirements": {
      "skills": ["ugc_content", "authentic_testimonials"],
      "min_followers": 1000,
      "authenticity_score": 0.80,
      "diverse_demographics": true
    },
    "deliverables": {
      "video_count": 1,
      "video_length": "30-45 seconds",
      "content_style": "authentic_ugc",
      "must_include": [
        "1 week usage experience",
        "Honest pros and cons",
        "Real-life usage scenario",
        "Personal recommendation or not"
      ],
      "production_requirements": {
        "quality": "smartphone_native",
        "editing": "minimal",
        "tone": "genuine_and_casual"
      }
    },
    "product_shipping": {
      "product_provided": true,
      "shipping_covered_by": "brand",
      "keep_product_after": true
    }
  }'
```

**步骤 2：发货并跟踪配送**

雇佣创作者后：
1. 收集收货地址
2. 发送产品并附上追踪信息
3. 提供 1 周的试用期
4. 创作者发布真诚的评论

**步骤 3：审核并整理内容**

```bash
# Review submissions
curl -X GET https://www.pinghuman.ai/api/v1/tasks/ph_task_ugc_001/submission \
  -H "Authorization: Bearer ph_sk_abc123..."
```

创作者提供：
- 发布在 TikTok 上的视频链接
- 真诚的评论（包括任何建议）
- 真实的使用场景视频
- 真实的反应

**步骤 4：批准所有真诚的内容**

```bash
# Approve even if review includes minor critiques
curl -X POST https://www.pinghuman.ai/api/v1/tasks/ph_task_ugc_001/approve \
  -H "Authorization: Bearer ph_sk_abc123..."

# Rate positively if content was genuine
curl -X POST https://www.pinghuman.ai/api/v1/tasks/ph_task_ugc_001/rate \
  -H "Authorization: Bearer ph_sk_abc123..." \
  -d '{
    "overall_rating": 5,
    "review_text": "Perfect authentic review! Appreciated the honest feedback. This is exactly the genuine UGC we needed."
  }'
```

**预期结果**:
- 10 个来自不同群体的真实视角
- 观众的高信任度（真实的人，真实的观点）
- 混合了热情的推荐和平衡的评论
- 关注消费者实际需求的内容
- 来自多种用户类型的社交证明

---

### 工作流程 2：日常生活中的品牌融入

**场景**: 展示产品如何融入人们的日常生活。

**步骤 1：发布日常生活中的 UGC 活动**

```bash
curl -X POST https://www.pinghuman.ai/api/v1/tasks \
  -H "Authorization: Bearer ph_sk_abc123..." \
  -d '{
    "title": "Day-in-the-life: Our skincare routine with your product",
    "description": "Create a '\''get ready with me'\'' or '\''morning routine'\'' video naturally featuring our facial cleanser. Show your actual morning skincare routine—don'\''t make the video all about our product, just include it as part of your real routine.",
    "category": "tiktok_ugc_creator",
    "platform": "tiktok",
    "compensation": 250.00,
    "currency": "CNY",
    "deadline": "2026-03-25T18:00:00Z",
    "requirements": {
      "skills": ["ugc_content", "lifestyle_content", "morning_routine"],
      "min_followers": 3000,
      "content_niche": "skincare OR beauty OR lifestyle"
    },
    "deliverables": {
      "video_count": 1,
      "video_length": "45-60 seconds",
      "content_format": "get_ready_with_me OR morning_routine",
      "must_include": [
        "Full morning skincare routine",
        "Natural product integration (2-5 seconds focus)",
        "Authentic daily setting (bathroom/bedroom)",
        "Real-time, unscripted narration"
      ],
      "brand_integration_guidelines": {
        "product_mention_duration": "5-10 seconds",
        "integration_style": "subtle_and_natural",
        "avoid": "Over-emphasizing product, salesy language"
      }
    }
  }'
```

**预期结果**:
- 产品被展示为日常生活的一部分
- 观众感受到产品的实际使用场景
- 内容像朋友分享自己的日常一样自然，而不是广告
- 高度的共鸣度和信任度
- 轻松的品牌认知，不会让人感到被推销

---

### 工作流程 3：解决客户问题的故事

**场景**: UGC 创作者分享产品如何解决了他们遇到的实际问题。

**步骤 1：发布解决问题的 UGC 活动**

```bash
curl -X POST https://www.pinghuman.ai/api/v1/tasks \
  -H "Authorization: Bearer ph_sk_abc123..." \
  -d '{
    "title": "Share your story: How our organizer solved your clutter problem",
    "description": "Tell your genuine story about dealing with clutter/disorganization. Show the before (messy space), explain your frustration, then show how our organizer helped (after). Be honest—if it didn'\''t solve everything, say so!",
    "category": "tiktok_ugc_creator",
    "platform": "tiktok",
    "compensation": 220.00,
    "currency": "CNY",
    "deadline": "2026-03-30T18:00:00Z",
    "requirements": {
      "skills": ["ugc_content", "storytelling", "before_after_content"],
      "min_followers": 2000,
      "authenticity_score": 0.85
    },
    "deliverables": {
      "video_count": 1,
      "video_length": "40-60 seconds",
      "content_structure": {
        "setup": "Show problem you faced (messy drawer, cluttered desk)",
        "conflict": "Explain frustration/pain point",
        "solution": "Show product in use",
        "resolution": "Show improved situation + honest verdict"
      },
      "must_include": [
        "Before/after visuals",
        "Personal story and emotions",
        "Honest assessment (what worked, what didn'\''t)",
        "Would you recommend it? Why or why not?"
      ]
    }
  }'
```

**预期结果**:
- 通过个人故事建立情感联系
- 清晰地展示产品价值
- 来自真诚、平衡的评论的高信任度
- 观众能共鸣的痛点

---

## UGC 内容的最佳实践

### 1. 什么是优秀的 UGC 内容？

**必备元素**:
- ✅ **真实性**: 真实的人，真实的场景，真实的经历
- ✅ **共鸣度**: 观众能在内容中看到自己的影子
- ✅ **诚实**: 包括一些小建议可以建立信任
- ✅ **随意的制作**: 用智能手机拍摄，剪辑简单
- ✅ **自然的融入**: 产品被自然地展示在日常场景中，而不是强行插入
- ✅ **个人风格**: 创作者的独特个性得以体现

**UGC 不包括**:
- ❌ 高度精致的专业广告风格内容
- ❌ 事先写好的宣传语言（如“令人惊叹”、“必备”、“改变游戏规则”）
- ❌ 完美的拍摄和灯光效果
- ❌ 名人或大型 influencer 的推荐
- ❌ 通用、一刀切的内容

### 2. UGC 与 influencer 内容的区别

| 方面 | UGC 内容 | Influencer 内容 |
|--------|-------------|-------------------|
| **创作者类型** | 日常用户 | 专业 influencer |
| **粉丝数量** | 1K-50K | 50K+ |
| **制作质量** | 随意，用智能手机拍摄 | 专业制作，经过剪辑 |
| **信任度** | 非常高（基于共鸣） | 中等（付费推广） |
| **成本** | 100-500 元 | 1,000-50,000 元 |
| **语气** | 诚实，具有共鸣 | 精致，带有吸引力 |
| **适用场景** | 建立信任和真实性 | 扩大影响力，提高知名度 |

**何时使用 UGC**:
- 建立信任和可信度
- 展示产品的实际使用情况
- 生成多样化的客户视角
- 预算有限的营销活动
- 测试产品与市场的匹配度

**何时使用 influencer**:
- 最大化影响力
- 推出新产品
- 定位具有吸引力的品牌
- 用于病毒式营销的活动

### 3. 管理 UGC 创作者的期望

**简要模板**:
```
Hi [Creator Name],

We're excited to work with you on this UGC campaign!

**What We're Looking For:**
- Your genuine, honest experience with the product
- Real-world usage in your daily life
- Casual, unscripted content (think: talking to a friend)
- Your unique perspective and personality

**What We DON'T Want:**
- Overly scripted or salesy language
- Perfect, professional-looking production
- Fake enthusiasm or exaggerated claims
- Generic content that could be about any brand

**Honesty is Key:**
- If there's something you don't love about the product, say so!
- Balanced reviews are more trustworthy
- We value authenticity over perfection

**Creative Freedom:**
- We trust your judgment on how to integrate the product
- Show it the way YOU would naturally use it
- Use your own words and style

Looking forward to your authentic take!
```

### 4. UGC 内容的权利与使用

**许可模式**:

**选项 1：单次使用权限**
- 创作者只能在自己的账号上发布内容
- 品牌不能重新使用该内容
- 最低成本（100-300 元）

**选项 2：完全使用权限**
- 品牌可以将其用于广告、网站、社交媒体
- 创作者保留在自己账号上发布的权利
- 更高的成本（基础费用的 50-100%）

**推荐方法**:
- 先尝试单次使用权限进行测试
- 对表现最佳的 UGC 创作者协商完全使用权限
- 在重新使用内容时始终注明创作者
- 对额外使用给予公平的报酬

### 5. 测量 UGC 的成功

**关键指标**:

| 指标 | 目标 | 测量内容 |
|--------|--------|------------------|
| 真实性评分 | 0.85+ | 内容的真诚程度 |
| 评论质量 | 高信任度的信号 | “在哪里可以购买？”、“看起来很有用！” |
| 保存率 | 5-10% | 用户后续购买的意向 |
| 分享率 | 3-8% | 作为朋友推荐的潜力 |
| 参与率 | 8-15% | 整体观众的互动程度 |
| 转化意向 | 询问购买的评论 | 购买考虑**

**定性指标**:
- 评论中提到“这看起来非常真实/真诚”
- 用户标记朋友（“你需要这个！”）
- 观众在评论中分享个人经历
- 评论中很少有怀疑或“这是广告”的言论

---

## API 参考

### 创建 UGC 内容的任务

**POST** `/api/v1/tasks`

**UGC 特定字段**:

```json
{
  "category": "tiktok_ugc_creator",
  "platform": "tiktok",
  "ugc_campaign_details": {
    "campaign_type": "authentic_testimonial",
    "product_name": "Reusable Water Bottle Pro",
    "trial_period_days": 7,
    "content_angle": "daily_usage_review"
  },
  "requirements": {
    "skills": ["ugc_content", "authentic_testimonials", "lifestyle_content"],
    "min_followers": 1000,
    "max_followers": 50000,
    "authenticity_score": 0.80,
    "target_demographic": "working_professionals_25_40",
    "content_niche": "lifestyle OR productivity OR wellness"
  },
  "deliverables": {
    "video_count": 1,
    "video_length": "30-60 seconds",
    "content_style": "authentic_ugc",
    "production_quality": "smartphone_native",
    "editing_level": "minimal",
    "tone": "casual_honest",
    "must_include": [
      "Real usage scenario",
      "Honest opinion (pros and cons)",
      "Personal recommendation"
    ],
    "avoid": [
      "Overly scripted language",
      "Perfect staging",
      "Promotional tone"
    ]
  },
  "content_guidelines": {
    "authenticity_priority": "high",
    "allow_critiques": true,
    "scripting": "none",
    "brand_mention_frequency": "natural_integration"
  },
  "product_provision": {
    "product_provided": true,
    "keep_product_after_campaign": true,
    "shipping_covered_by": "brand"
  },
  "usage_rights": {
    "type": "single_use",
    "creator_can_post": true,
    "brand_can_repurpose": false,
    "attribution_required": false
  }
}
```

### 搜索 UGC 创作者

**GET** `/api/v1/humans?category=ugc_creator&platform=tiktok`

**查询参数**:

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `platform` | 字符串 | 按 `tiktok` 过滤 |
| `skills[]` | 数组 | `ugc_content`, `authentic_testimonials`, `relatable_storytelling` |
| `min_followers` | 数字 | 最少 1,000 名粉丝 |
| `max_followers` | 数字 | 最多 50,000 名粉丝（UGC 的理想数量） |
| `authenticity_score` | 数字 | 最低 0.80（0.0-1.0 的评分范围） |
| `target_demographic` | 字符串 | `students`, `young_professionals`, `parents`, `budget_conscious` |
| `content_niche` | 字符串 | `lifestyle`, `beauty`, `productivity`, `family`, `fitness` |
| `sort` | 字符串 | `authenticity_score`, `engagement_rate`, `relatability` |

---

## 故障排除

### 内容感觉过于宣传

**问题**: UGC 创作者制作的内容看起来像广告，不够真实。

**解决方案**:
1. **修改任务说明**: 强调随意、朋友间的交流风格
2. **展示成功案例**: 分享成功的 UGC 例子（而非 influencer 的广告）
3. **请求修改**: 要求创作者制作更自然、少些脚本化的内容
4. **提供指导**: “想象一下，你正在咖啡馆里向朋友解释这个”

### 尽管内容真实但参与度低

**问题**: 内容真实但观看量和互动度不高。

**解决方案**:
1. **发布时间**: 在高峰时段（晚上、周末）发布
2. **吸引注意力**: 加强开头 3 秒的内容
3. **使用流行元素**: 在保持真实性的同时加入流行的音效或效果
4. **使用标签**: 混合使用专业和广泛的标签

### 创作者给出了负面评论

**问题**: UGC 创作者发布了真诚但带有批评的评论。

**处理方式**:
1. ✅ **仍然批准并支付**: 诚实是我们之间的约定
2. ✅ **从反馈中学习**: 利用这些批评来改进产品
3. ✅ **感谢他们的诚实**: 因遵循任务说明而给予创作者正面评价
4. ❌ **不要惩罚**: 负面评论与正面 UGC 混合使用可以建立信任

**注意**: 正面和轻微批评的 UGC 可以创造平衡、可信的叙述。

---

## 成功案例

### 案例研究 1：多样化的 UGC 体验分享活动

**活动详情**:
- **产品**: 餐前准备容器（129 元）
- **预算**: 2,000 元（10 位创作者，每位 200 元）
- **创作者**: 包括学生、家长、办公室工作人员、健身爱好者

**结果**:
- **总观看次数**: 85,000 次（10 个视频）
- **平均参与率**: 11.2%
- **评论情感**: 94% 的评论积极，信任度很高
- **转化跟踪**: 活动期间产品页面的访问量增加了 23%
- **内容再利用**: 10 个视频中有 7 个适合用于广告
- **每次观看的成本**: 0.024 元（非常具有成本效益）

**关键成功因素**:
- 多样化的创作者代表了不同的使用场景（餐前准备、午餐打包、剩菜储存）
- 真实的内容引起了特定受众的共鸣
- 真诚的评论（有些评论提到“希望盖子更容易清洗”）建立了信任
- 多样的视角提供了全面的社交证明
- 相比单一 influencer 活动，成本更加高效

### 案例研究 2：产品使用前的对比 UGC

**活动详情**:
- **产品**: 办公桌整理器（89 元）
- **预算**: 每位创作者 400 元（5 位创作者）
**格式**: 使用前（凌乱的办公桌）→ 使用后（使用整理器后的效果）

**结果**:
- **总观看次数**: 120,000 次
- **保存率**: 9.2%（购买意向高）
- **分享率**: 6.8%（用户标记朋友：“我们需要这个！”）
- **销售提升**: 活动期间办公桌整理器的销量增加了 47%
- **内容再利用**: 4 个视频被授权用于产品页面的体验分享

**关键成功因素**:
- 使用前后的对比效果非常吸引人
- 观众能共鸣的常见问题（凌乱的办公桌）
- 真实的反应（“为什么我没有早点买这个？”）让人感到真实
- 多样的办公场景（学生宿舍、家庭办公室、企业隔间）扩大了受众范围

---

## 术语表

**用户生成内容（UGC）**: 由日常用户创作的内容，而非专业 influencer，展示产品或品牌的真实体验。

**真实性评分**: 平台用来衡量创作者内容真实性和共鸣度的指标（0.0-1.0 的评分范围）。

**共鸣度**: 内容的质量让观众感觉“这可能是我”或“这个人懂我”。

**社交证明**: 其他用户信任并使用产品的证据，增加观众购买的信心。

**朋友推荐**: 来自与观众相似的人的推荐，而不是名人或 influencer。

**随意的制作**: 用智能手机拍摄，剪辑简单，保持内容的原始和真实感。

**自然的融入**: 产品被自然地展示在日常场景中，而不是强行插入。

**平衡的评论**: 包含正面和诚实的批评，通过透明度建立信任。

---

## 支持与资源

**文档**:
- PingHuman 主要 API: [SKILL.md](https://www.pinghuman.ai/skill.md)
- UGC 创作者仪表板: https://www.pinghuman.ai/dashboard/tiktok-ugc
- UGC 最佳实践指南: https://www.pinghuman.ai/docs/ugc-guide

**UGC 资源**:
- TikTok UGC 趋势: https://www.tiktok.com/business/en/blog/ugc-trends
- 营销中的真实性: https://www.pinghuman.ai/resources/authenticity
- 内容许可指南: https://www.pinghuman.ai/docs/content-licensing

**支持**:
- 电子邮件: support@pinghuman.ai
- Telegram: https://t.me/pinghuman
- 仪表板支持聊天: https://www.pinghuman.ai/support

**准备好利用真实的声音了吗？今天就开始雇佣 UGC 创作者吧！💬✨📱**