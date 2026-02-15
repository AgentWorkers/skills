---
name: startup-metrics
model: fast
version: 1.0.0
description: >
  Track, calculate, and optimize key performance metrics for startups from seed
  through Series A. Covers unit economics, growth efficiency, and business models.
tags: [startup, metrics, saas, kpis, unit-economics, growth, fundraising]
---

# 启动指标框架

本指南全面介绍了如何跟踪、计算并优化不同初创企业商业模式（从种子轮到A轮融资阶段）的关键绩效指标。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install startup-metrics
```

## 本技能的作用

提供以下方面的公式、基准数据和指导：
- 收入指标（MRR、ARR、增长率）
- 单位经济指标（CAC、LTV、投资回收期）
- 现金效率指标（烧钱速度、业务发展周期、烧钱倍数）
- SaaS特定指标（新客户转化率、关键数字、40法则）
- 市场和消费者相关指标
- 各阶段应关注的焦点指标

## 适用场景

- 设置初创企业的分析和仪表板
- 计算CAC、LTV或单位经济指标
- 准备投资者更新材料或演示文稿
- 评估企业的健康状况和运营效率
- 理解每个阶段哪些指标最重要

## 关键词

初创指标、SaaS指标、CAC、LTV、ARR、MRR、烧钱速度、烧钱倍数、40法则、净用户留存率、关键数字、单位经济指标、市场收入、日活跃用户/月活跃用户

## 通用初创指标

### 收入指标

```
MRR = Σ (Active Subscriptions × Monthly Price)
ARR = MRR × 12

MoM Growth = (This Month MRR - Last Month MRR) / Last Month MRR
YoY Growth = (This Year ARR - Last Year ARR) / Last Year ARR
```

**基准数据：**
| 阶段 | 增长目标 |
|-------|---------------|
| 种子轮 | 每月增长15-20% |
| A轮融资 | 每月增长10-15%，年增长3-5倍 |
| B轮融资及以上 | 年增长100%以上（遵循40法则） |

### 单位经济指标

```
CAC = Total S&M Spend / New Customers Acquired
LTV = ARPU × Gross Margin% × (1 / Churn Rate)
LTV:CAC Ratio = LTV / CAC
CAC Payback = CAC / (ARPU × Gross Margin%)
```

**基准数据：**
| 指标 | 优秀 | 良好 | 需关注 |
|--------|-----------|------|------------|
| LTV:CAC | > 3.0 | 1.0-3.0 | < 1.0 |
| CAC投资回收期 | < 12个月 | 12-18个月 | > 24个月 |

### 现金效率

```
Monthly Burn = Monthly Revenue - Monthly Expenses
Runway (months) = Cash Balance / Monthly Burn Rate
Burn Multiple = Net Burn / Net New ARR
```

**烧钱倍数基准数据：**
| 分数 | 评估结果 |
|-------|------------|
| < 1.0 | 效率极高 |
| 1.0-1.5 | 良好 |
| 1.5-2.0 | 可接受 |
| > 2.0 | 效率较低 |

**目标：**始终保持12-18个月的业务发展周期。

## SaaS指标

### 收入构成

```
Net New MRR = New MRR + Expansion MRR - Contraction MRR - Churned MRR
```

### 用户留存指标

```
NDR (Net Dollar Retention) = (ARR Start + Expansion - Contraction - Churn) / ARR Start
Gross Retention = (ARR Start - Churn - Contraction) / ARR Start
Logo Retention = (Customers End - New Customers) / Customers Start
```

**新客户转化率基准数据：**
| 范围 | 评估结果 |
|-------|------------|
| > 120% | 业内最佳 |
| 100-120% | 良好 |
| < 100% | 需改进 |

### 效率指标

```
Magic Number = Net New ARR (quarter) / S&M Spend (prior quarter)
Rule of 40 = Revenue Growth Rate% + Profit Margin%
Quick Ratio = (New MRR + Expansion MRR) / (Churned MRR + Contraction MRR)
```

**关键数字：**
- > 0.75 = 效率较高，具备扩展潜力 |
- 0.5-0.75 = 效率中等 |
- < 0.5 = 效率较低，暂不适合扩展

## 市场指标

```
GMV = Σ (Transaction Value)
Take Rate = Net Revenue / GMV
```

**典型佣金费率：**
| 类型 | 范围 |
|------|-------|
| 支付处理器 | 2-3% |
| 电子商务平台 | 10-20% |
| 服务交易平台 | 15-25% |
| 高价值B2B业务 | 5-15% |

**流动性指标：**
- 填单率 > 80% = 流动性强 |
- 重复购买率 > 60% = 用户留存度高

## 消费者/移动端指标

```
DAU/MAU Ratio = DAU / MAU
K-Factor = Invites per User × Invite Conversion Rate
```

**日活跃用户/月活跃用户基准数据：**
| 比率 | 评估结果 |
|-------|------------|
| > 50% | 用户习惯良好 |
| 20-50% | 用户参与度一般 |
| < 20% | 用户参与度低 |

**30天用户留存率基准数据：**
| 率率 | 评估结果 |
|------|------------|
| > 40% | 优秀 |
| 25-40% | 良好 |
| < 25% | 用户留存率低 |

## B2B销售指标

```
Win Rate = Deals Won / Total Opportunities
Pipeline Coverage = Total Pipeline Value / Quota (target: 3-5x)
ACV = Total Contract Value / Contract Length (years)
```

**销售周期基准数据：**
| 客户类型 | 典型周期 |
|---------|------------------|
| 中小型企业 | 30-60天 |
| 中型市场 | 60-120天 |
| 企业级客户 | 120-270天 |

## 各阶段的指标

### 种子轮（产品市场适配阶段）

**关注点：**活跃用户、用户留存率（第7天/第30天）、用户参与度、定性反馈

**无需关注：**收入、CAC、单位经济指标

### 种子轮（年收入50万至200万美元）

**关注点：**
- MRR增长率（每月15-20%）
- CAC和LTV的基线数据
- 核心产品的用户留存率（>85%）
- 开始关注销售效率、烧钱速度和业务发展周期

### A轮融资（年收入200万至1000万美元）

**关注点：**
- 年收入增长率（年增长3-5倍）
- LTV:CAC > 3.0，投资回收期 < 18个月
- 新客户转化率 > 100%
- 烧钱倍数 < 2.0
- 关键数字 > 0.5

## 投资者关注的重点指标

### 种子轮
- MRR增长率
- 用户留存率
- 早期的单位经济指标
- 产品使用情况

### A轮融资
- 年收入和增长率
- CAC投资回收期 < 18个月
- LTV:CAC > 3.0
- 新客户转化率 > 100%
- 烧钱倍数 < 2.0

### B轮融资及以上
- 40法则 > 40%
- 高效的增长（关键数字）
- 通往盈利的路径

**仪表板格式：**
```
Current MRR: $250K (↑ 18% MoM)
ARR: $3.0M (↑ 280% YoY)
CAC: $1,200 | LTV: $4,800 | LTV:CAC = 4.0x
NDR: 112% | Logo Retention: 92%
Burn: $180K/mo | Runway: 18 months
```

## 常见错误

1. **关注无意义的指标** — 应关注可操作的指标，而非总用户数或页面浏览量
2. **指标过多** — 应重点关注5-7个核心指标，而非泛泛而谈的50个指标
3. **忽视单位经济指标** — 即使在种子轮阶段，CAC和LTV也非常重要
4. **不进行细分** — 应按客户群体、渠道或时间阶段进行数据分类
5. **追求表面指标** — 应优化实际业务成果，而非仅仅为了美观的仪表板

## 绝对不能做的事情

1. **在任何阶段都不要忽视** 单位经济指标（CAC和LTV）
2. **不要孤立地关注** 无用户留存背景的总用户数或页面浏览量
3. **报告增长率时不要只提供绝对数字** — 从1000美元增长到100万美元的增长情况是完全不同的
4. **不要忽略数据细分** — 综合指标会掩盖重要趋势
5. **不要混淆相关性和因果关系** — 在得出结论前需进行深入分析
6. **在不了解阶段基准的情况下设定目标**  
7. **展示指标时不要脱离趋势背景** — 应提供当前数值、增长率和基准数据
8. **不要为了指标本身而优化** — 应始终以实际业务成果为导向进行优化