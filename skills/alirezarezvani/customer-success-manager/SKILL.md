---
name: customer-success-manager
description: 使用加权评分模型监控客户状况、预测客户流失风险，并识别SaaS客户成功方面的扩展机会。
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: business-growth
  domain: customer-success
  updated: 2026-02-06
  python-tools: health_score_calculator.py, churn_risk_analyzer.py, expansion_opportunity_scorer.py
  tech-stack: customer-success, saas-metrics, health-scoring
---
# 客户成功经理

提供生产级别的客户成功分析服务，包括多维度的客户健康状况评估、流失风险预测以及扩展机会识别。通过三个Python命令行工具（CLI），仅使用标准库即可实现确定性、可重复的分析——无需外部依赖项、API调用或机器学习模型。

---

## 目录

- [功能](#capabilities)
- [输入要求](#input-requirements)
- [输出格式](#output-formats)
- [使用方法](#how-to-use)
- [脚本](#scripts)
- [参考指南](#reference-guides)
- [模板](#templates)
- [最佳实践](#best-practices)
- [限制](#limitations)

---

## 功能

- **客户健康状况评估**：从使用情况、参与度、支持服务和关系维度进行多维度加权评分，并分为绿色（健康）、黄色（需要关注）和红色（高风险）三个等级。
- **流失风险分析**：通过行为信号检测来识别高风险账户，并提供分层的干预方案及续费紧迫性提示。
- **扩展机会评估**：分析客户采用产品的深度、市场潜力，并根据投入与收益的平衡来评估收入机会。
- **针对不同客户群体的基准测试**：可配置针对企业级、中型市场和小型企业（SMB）客户群体的阈值。
- **趋势分析**：进行周期性的数据对比，以监测客户状况的改善或恶化趋势。
- **高管汇报**：提供季度业务回顾（QBR）模板、客户成功计划以及高管业务评审模板。

---

## 输入要求

所有脚本都接受一个JSON文件作为输入参数。请参考`assets/sample_customer_data.json`中的示例文件。

### 健康状况评分工具

```json
{
  "customers": [
    {
      "customer_id": "CUST-001",
      "name": "Acme Corp",
      "segment": "enterprise",
      "arr": 120000,
      "usage": {
        "login_frequency": 85,
        "feature_adoption": 72,
        "dau_mau_ratio": 0.45
      },
      "engagement": {
        "support_ticket_volume": 3,
        "meeting_attendance": 90,
        "nps_score": 8,
        "csat_score": 4.2
      },
      "support": {
        "open_tickets": 2,
        "escalation_rate": 0.05,
        "avg_resolution_hours": 18
      },
      "relationship": {
        "executive_sponsor_engagement": 80,
        "multi_threading_depth": 4,
        "renewal_sentiment": "positive"
      },
      "previous_period": {
        "usage_score": 70,
        "engagement_score": 65,
        "support_score": 75,
        "relationship_score": 60
      }
    }
  ]
}
```

### 流失风险分析工具

```json
{
  "customers": [
    {
      "customer_id": "CUST-001",
      "name": "Acme Corp",
      "segment": "enterprise",
      "arr": 120000,
      "contract_end_date": "2026-06-30",
      "usage_decline": {
        "login_trend": -15,
        "feature_adoption_change": -10,
        "dau_mau_change": -0.08
      },
      "engagement_drop": {
        "meeting_cancellations": 2,
        "response_time_days": 5,
        "nps_change": -3
      },
      "support_issues": {
        "open_escalations": 1,
        "unresolved_critical": 0,
        "satisfaction_trend": "declining"
      },
      "relationship_signals": {
        "champion_left": false,
        "sponsor_change": false,
        "competitor_mentions": 1
      },
      "commercial_factors": {
        "contract_type": "annual",
        "pricing_complaints": false,
        "budget_cuts_mentioned": false
      }
    }
  ]
}
```

### 扩展机会评估工具

```json
{
  "customers": [
    {
      "customer_id": "CUST-001",
      "name": "Acme Corp",
      "segment": "enterprise",
      "arr": 120000,
      "contract": {
        "licensed_seats": 100,
        "active_seats": 95,
        "plan_tier": "professional",
        "available_tiers": ["professional", "enterprise", "enterprise_plus"]
      },
      "product_usage": {
        "core_platform": {"adopted": true, "usage_pct": 85},
        "analytics_module": {"adopted": true, "usage_pct": 60},
        "integrations_module": {"adopted": false, "usage_pct": 0},
        "api_access": {"adopted": true, "usage_pct": 40},
        "advanced_reporting": {"adopted": false, "usage_pct": 0}
      },
      "departments": {
        "current": ["engineering", "product"],
        "potential": ["marketing", "sales", "support"]
      }
    }
  ]
}
```

---

## 输出格式

所有脚本都支持两种输出格式（通过`--format`参数指定）：

- **`text`**（默认）：适合终端查看的格式化文本输出。
- **`json`**：适合集成和数据管道处理的机器可读JSON格式输出。

---

## 使用方法

### 快速入门

```bash
# Health scoring
python scripts/health_score_calculator.py assets/sample_customer_data.json
python scripts/health_score_calculator.py assets/sample_customer_data.json --format json

# Churn risk analysis
python scripts/churn_risk_analyzer.py assets/sample_customer_data.json
python scripts/churn_risk_analyzer.py assets/sample_customer_data.json --format json

# Expansion opportunity scoring
python scripts/expansion_opportunity_scorer.py assets/sample_customer_data.json
python scripts/expansion_opportunity_scorer.py assets/sample_customer_data.json --format json
```

### 工作流程集成

```bash
# 1. Score customer health across portfolio
python scripts/health_score_calculator.py customer_portfolio.json --format json > health_results.json

# 2. Identify at-risk accounts
python scripts/churn_risk_analyzer.py customer_portfolio.json --format json > risk_results.json

# 3. Find expansion opportunities in healthy accounts
python scripts/expansion_opportunity_scorer.py customer_portfolio.json --format json > expansion_results.json

# 4. Prepare QBR using templates
# Reference: assets/qbr_template.md
```

---

## 脚本

### 1. health_score_calculator.py

**用途：**进行多维度客户健康状况评估，并结合趋势分析及针对不同客户群体的基准测试。

**评估维度及权重：**
| 维度 | 权重 | 指标            |
|---------|--------|-------------------|
| 使用情况 | 30%   | 登录频率、功能采用率、日活跃用户数/月活跃用户数（DAU/MAU） |
| 参与度 | 25%   | 支持工单数量、会议出席率、净推荐值（NPS）/客户满意度（CSAT） |
| 支持服务 | 20%   | 开启的工单数量、升级率、平均解决时间     |
| 关系程度 | 25%   | 高管支持者的参与度、多线程处理深度、续费意愿     |

**评分标准：**
- 绿色（75-100分）：客户表现良好，正在创造价值。
- 黄色（50-74分）：需要关注，需密切监控。
- 红色（0-49分）：存在风险，需要立即采取干预措施。

**使用方法：**
```bash
python scripts/health_score_calculator.py customer_data.json
python scripts/health_score_calculator.py customer_data.json --format json
```

### 2. churn_risk_analyzer.py

**用途：**通过行为信号检测识别高风险账户，并提供相应的干预建议。

**风险信号权重：**
| 信号类别 | 权重 | 指标                |
|---------|--------|-------------------|
| 使用情况下降 | 30%   | 登录趋势、功能采用率变化、日活跃用户数/月活跃用户数变化 |
| 参与度下降 | 25%   | 会议取消次数、响应时间、净推荐值变化     |
| 支持问题 | 20%   | 开启的升级请求、未解决的严重问题、满意度变化   |
| 关系信号 | 15%   | 负责人变动、竞争对手提及       |
| 商业因素 | 10%   | 合同类型、价格投诉、预算削减       |

**风险等级：**
- 严重（80-100分）：需要立即上报给高管。
- 高风险（60-79分）：需要CSM（客户成功经理）立即介入。
- 中等风险（40-59分）：需要主动跟进。
- 低风险（0-39分）：进行常规监控。

**使用方法：**
```bash
python scripts/churn_risk_analyzer.py customer_data.json
python scripts/churn_risk_analyzer.py customer_data.json --format json
```

### 3. expansion_opportunity_scorer.py

**用途：**识别升级销售、交叉销售和扩展机会，并估算相关收入及优先级。

**扩展类型：**
- **升级销售**：建议客户升级到更高级别的产品或增加现有产品的使用量。
- **交叉销售**：推荐客户购买新的产品模块。
- **业务扩展**：建议客户增加使用席位或扩展业务部门。

**使用方法：**
```bash
python scripts/expansion_opportunity_scorer.py customer_data.json
python scripts/expansion_opportunity_scorer.py customer_data.json --format json
```

---

## 参考指南

| 参考文档 | 说明                |
|---------|-------------------|
| `references/health-scoring-framework.md` | 完整的健康状况评分方法论、维度定义、权重设定依据及阈值调整方法。 |
| `references/cs-playbooks.md` | 针对不同风险等级的干预方案、新用户入职流程、续费管理、业务扩展及问题升级的处理指南。 |
| `references/cs-metrics-benchmarks.md` | 行业基准数据，包括净流失率（NRR）、净推荐率（GRR）、流失率、不同客户群体及行业的健康状况评分。 |

---

## 模板

| 模板       | 用途                 |
|-----------|-------------------|
| `assets/qbr_template.md` | 季度业务回顾报告模板          |
| `assets/success_plan_template.md` | 客户成功计划模板，包含目标、里程碑和评估指标。 |
| `assets/onboarding_checklist_template.md` | 新用户入职90天检查清单          |
| `assets/executive_business_review_template.md` | 高管利益相关者使用的业务评审模板。 |

---

## 最佳实践

1. **定期评估**：对企业级客户每周进行一次健康状况评估，对中型市场客户每两周评估一次，对小型企业每月评估一次。
2. **关注趋势而非静态数据**：绿色等级的下降比黄色等级的稳定情况更紧急。
3. **综合分析多种信号**：结合使用这三个脚本以获得全面的客户画像。
4. **调整阈值**：根据产品和行业特点调整评估标准。
5. **记录干预措施及结果**：记录所采取的干预措施及其效果，以便优化后续方案。
6. **提前准备数据**：在每次季度业务回顾会议和高管会议前运行相关脚本。

---

## 限制

- **非实时数据**：脚本仅分析从JSON输入文件中提取的静态数据。
- **无法与CRM系统集成**：数据需手动从CRM/客户支持平台导出。
- **仅提供确定性分析**：不使用预测性机器学习模型，评分基于算法和加权信号。
- **阈值可能需要调整**：默认阈值为行业标准，但可能需根据实际情况进行微调。
- **收入估算**：扩展收入的估算基于使用模式，仅供参考。

---

**最后更新时间：**2026年2月
**使用的工具：**3个Python命令行工具
**依赖库：**仅支持Python 3.7及更高版本的标准库。