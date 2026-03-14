---
name: growth-loop-orchestrator
description: 通过将使用情况、反馈、改进以及采纳过程连接起来，形成一个自我强化的循环，从而在整个技能组合中实现持续的增长。这种方法适用于设计增长策略、优化技能采纳率、创建具有传播效应的循环（即“病毒式增长”），或构建可持续的增长机制。
---
# 成长循环编排器（Growth Loop Orchestrator）

## 概述

`growth-loop-orchestrator` 技能负责设计、实现并优化整个技能组合中的增长循环。它将用户使用情况、反馈、产品改进以及技能采纳过程连接成自我强化的循环，从而推动可持续的增长。

## 使用场景

- 为技能设计增长策略
- 创建病毒式传播或推荐机制
- 优化技能采纳流程
- 建立用户参与机制
- 规划技能组合的增长计划
- 分析增长指标和循环效果
- 解决增长停滞问题
- 设计网络效应（即用户使用技能后对他人产生的正面影响）

## 核心概念

### 成长循环类型

| 类型 | 机制 | 示例 |
|------|-----------|---------|
| **病毒式传播（Viral）** | 用户吸引新用户 | 分享成果、邀请他人使用 |
| **内容驱动（Content）** | 用户使用行为产生新内容 | 公开输出、模板分享 |
| **网络效应（Network）** | 用户越多，价值越大 | 协作功能 |
| **用户参与（Engagement）** | 用户使用行为促进更多使用 | 培养使用习惯、设置连续使用奖励 |
| **反馈驱动（Feedback）** | 用户使用行为提升产品体验 | 从用户行为中获取反馈 |

### 成长循环的组成部分

每个成长循环都包含以下要素：
1. **输入（Input）**：进入循环的用户、行为或内容
2. **行为（Action）**：用户在循环中的具体操作
3. **输出（Output）**：产生并反馈回循环的结果
4. **转化（Conversion）**：如何将输出转化为新的输入
5. **放大效应（Amplification）**：促进循环持续增长的因素

### 成长循环指标

| 指标 | 描述 | 目标值 |
|--------|-------------|--------|
| **循环周期时间（Cycle Time）** | 一次循环完成所需的时间 | < 7 天 |
| **转化率（Conversion Rate）** | 完成循环的用户比例 | > 20% |
| **病毒系数（Viral Coefficient）** | 每位现有用户带来的新用户数量 | > 0.3 |
| **用户留存率（Retention Rate）** | 继续参与循环的用户比例 | > 40% |
| **增长速率（Amplification Rate）** | 每个循环的增长幅度 | > 10% |

## 输入数据

该技能需要以下输入：
- 当前的增长指标
- 用户行为数据
- 技能组合信息
- 目标增长目标
- 循环设计参数

## 输出结果

- 成长循环设计方案
- 编排执行计划
- 指标仪表盘
- 优化建议
- A/B 测试方案

## 工作流程

### 设计成长循环

1. **确定核心价值（Identify Core Value）**
   - 用户能获得什么价值？
   - 他们可以分享或创造什么？
   - 其他人会想要什么？

2. **绘制用户旅程图（Map User Journey）**
   - 用户的入口点
   - 关键操作步骤
   - 分享内容的关键时刻
   - 转化路径

3. **设计循环结构（Design the Loop）**
   - 输入来源
   - 关键操作
   - 输出内容的生成方式
   - 内容的传播机制
   - 如何将输出转化为新的输入

4. **增加放大效应（Add Amplification）**
   - 设计激励措施
   - 降低使用障碍
   - 利用网络效应
   - 提供社交证明（让用户看到他人使用该技能）

5. **测量与优化（Measure and Optimize）**
   - 监控循环指标
   - 识别瓶颈
   - 测试改进措施
   - 扩大有效策略的应用范围

### 分析现有循环

1. **分析当前状态（Analyze Existing Loops）**
   - 识别现有的成长循环
   - 测量当前的表现
   - 找出存在的问题

2. **诊断问题（Diagnose Issues）**
   - 用户在哪个环节退出循环？
   - 什么阻碍了转化？
   - 哪些环节的摩擦最大？

3. **制定解决方案（Generate Solutions）**
   - 修复存在的问题
   - 降低使用障碍
   - 增加放大效应

4. **测试与验证（Test and Validate）**
   - 对改进措施进行 A/B 测试
   - 测量效果
   - 快速迭代优化

## 命令示例

### 设计成长循环
```bash
./scripts/design-loop.sh --type viral --skill <name> [--output loop-design.md]
```

### 分析现有循环
```bash
./scripts/analyze-loops.sh [--skill <name>] [--portfolio]
```

### 优化循环性能
```bash
./scripts/optimize-loop.sh --loop-id <id> [--target metric] [--test]
```

### 监控增长指标
```bash
./scripts/track-metrics.sh [--skill <name>] [--dashboard] [--period 30d]
```

### 生成增长报告
```bash
./scripts/generate-report.sh --type loops|funnel|portfolio [--output report.md]
```

### 模拟循环行为
```bash
./scripts/simulate-loop.sh --design <file> [--cycles 10] [--users 1000]
```

## 输出格式

### 成长循环设计示例
[新用户] → [使用技能] → [生成输出] → [分享结果] → [新用户看到分享内容] → [尝试使用该技能] → [新用户]
```

## Components

### Input
- Source: User creates content
- Volume: ~50 outputs/day
- Quality: High (user-generated)

### Action
- What: User shares output
- Where: Social, email, link
- Friction: Medium (requires action)

### Output
- Type: Sharable result
- Format: Image, link, export
- Value: Demonstrates skill capability

### Conversion
- Mechanism: View → Try
- Rate: 15% (target: 25%)
- Time: Within 24 hours

### Amplification
- Social proof: "X people used this"
- Incentive: Free credits for sharing
- Network: Collaborative features

## Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Cycle Time | 3 days | 1 day |
| Conversion Rate | 15% | 25% |
| Viral Coefficient | 0.2 | 0.5 |
| Retention | 35% | 50% |

## Optimization Plan

### Immediate (This Week)
1. Add one-click sharing
2. Create shareable templates
3. Add social proof badges

### Near-term (This Month)
1. Implement referral rewards
2. Add collaboration features
3. Create public gallery

### Long-term (This Quarter)
1. Build network effects
2. Add team features
3. Create marketplace

## Success Criteria
- Viral coefficient > 0.5
- Cycle time < 24 hours
- 1000 new users/month from loop
```

### 循环性能仪表盘示例
```json
{
  "dashboard": "growth-loops",
  "period": "2024-03-01 to 2024-03-31",
  "loops": [
    {
      "id": "viral-share",
      "name": "Viral Sharing Loop",
      "type": "viral",
      "metrics": {
        "cycle_time_hours": 48,
        "conversion_rate": 0.18,
        "viral_coefficient": 0.25,
        "retention_7d": 0.42,
        "amplification": 1.15
      },
      "status": "active",
      "health": "good",
      "bottleneck": "share_rate",
      "recommendation": "Add one-click sharing buttons"
    },
    {
      "id": "content-seo",
      "name": "Content SEO Loop",
      "type": "content",
      "metrics": {
        "cycle_time_days": 30,
        "conversion_rate": 0.05,
        "content_velocity": 12,
        "organic_growth": 1.08
      },
      "status": "active",
      "health": "fair",
      "bottleneck": "content_quality",
      "recommendation": "Improve output shareability"
    }
  ],
  "portfolio_summary": {
    "total_loops": 4,
    "active_loops": 3,
    "avg_viral_coefficient": 0.22,
    "monthly_growth_rate": 0.15
  }
}
```

## 常见循环模式

### 病毒式传播循环模式
**关键要素**：易于分享、有价值的输出、低注册门槛

### 内容驱动循环模式
**关键要素**：适合搜索引擎优化（SEO）、默认公开、易于被发现

### 网络效应循环模式
**关键要素**：协作带来的价值、邀请激励机制、团队协作功能

### 用户参与循环模式
**关键要素**：有意义的奖励机制、连续使用奖励、进度展示

### 反馈驱动循环模式
**关键要素**：便捷的反馈渠道、快速反馈机制、明显的改进效果

## 质量要求

- 设计的循环应真正为用户创造价值，而不仅仅是追求增长
- 全面衡量整个循环过程，而不仅仅是部分环节
- 优化方案应着眼于可持续增长
- 在扩大规模前进行充分测试
- 注意防止用户滥用系统
- 在追求增长的同时保证产品质量

## 常见使用示例

- “为这个技能设计一个增长循环”
- “如何让这个技能实现病毒式传播？”
- “分析我们现有的增长循环”
- “是什么阻碍了我们的增长？”
- “设计一个推荐计划”
- “如何提高用户参与度？”
- “跟踪我们的增长指标”
- “优化我们的转化流程”
- “创造网络效应”

## 限制因素

- 需要用户使用数据才能进行有效分析
- 成长循环的验证需要时间
- 网络效应需要达到一定的用户规模才能显现
- 病毒式传播的效果难以预测
- 指标可能被用户操纵（例如通过虚假操作）
- 无价值的增长是不可持续的

## 相关技能

- `learning-evolution`：用于循环效果的持续优化
- `insight-tracker`：用于收集增长相关的洞察数据
- `decision-distiller`：用于辅助制定增长策略
- `skill-market-analyzer`：用于分析市场趋势对技能增长的影响

## 资源

### 脚本：
- `design-loop.sh`：用于设计新的成长循环
- `analyze-loops.sh`：用于分析现有循环
- `optimize-loop.sh`：用于优化循环性能
- `track-metrics.sh`：用于监控增长指标
- `simulate-loop.sh`：用于模拟循环行为

### 参考资料：
- 成长循环设计模式
- 病毒式传播机制
- 网络效应理论
- 用户参与设计原则

---

请注意：由于代码块（````bash
./scripts/design-loop.sh --type viral --skill <name> [--output loop-design.md]
````）在实际文档中并未提供具体代码内容，因此翻译时保留了这些占位符。在实际应用中，这些占位符将被替换为具体的代码实现。