---
name: "customer-success-manager"
description: 使用加权评分模型来监控客户状况、预测客户流失风险，并识别业务扩展机会，适用于SaaS客户成功管理场景。该工具可用于分析客户账户数据、评估客户留存指标、对高风险客户进行评分；同时也可用于处理用户提出的关于客户流失、客户健康状况、升级销售机会、业务扩展收入、客户留存分析等相关问题。通过运行三个Python命令行工具（CLI），可以生成明确的客户健康状况评分、客户流失风险等级以及针对企业级（Enterprise）、中端市场（Mid-Market）和小型企业（SMB）客户群体的优先扩展建议。
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

提供生产级的客户成功分析服务，包括多维度的健康状况评估、流失风险预测以及扩展机会识别。通过三个Python命令行工具（CLI），仅使用标准库即可进行确定性、可重复的分析——无需外部依赖项、API调用或机器学习模型。

---

## 目录

- [输入要求](#input-requirements)
- [输出格式](#output-formats)
- [使用方法](#how-to-use)
- [脚本](#scripts)
- [参考指南](#reference-guides)
- [模板](#templates)
- [最佳实践](#best-practices)
- [限制](#limitations)

---

## 输入要求

所有脚本都接受一个JSON文件作为参数输入。请参阅`assets/sample_customer_data.json`以获取完整的字段结构示例和样本数据。

### 健康状况评分器

每个客户对象所需的字段：`customer_id`、`name`、`segment`，以及嵌套对象`usage`（登录频率、功能采用率、DAU/MAU比率）、`engagement`（支持工单数量、会议出席率、NPS评分、CSAT评分）、`support`（待处理工单数量、升级率、平均解决时间）、`relationship`（高管支持者的参与度、多线程处理深度、续订意愿），以及用于趋势分析的`previous_period`评分。

### 流失风险分析器

每个客户对象所需的字段：`customer_id`、`name`、`segment`、`arr`、`contract_end_date`，以及嵌套对象`usage_decline`（使用量下降）、`engagement_drop`（参与度下降）、`support_issues`（支持问题）、`relationship_signals`（关系信号）和`commercial_factors`（商业因素）。

### 扩展机会评分器

每个客户对象所需的字段：`customer_id`、`name`、`segment`、`arr`，以及嵌套对象`contract`（许可席位数、活跃席位数、计划等级、可用等级）、`product_usage`（每个模块的采用情况和使用百分比），以及`departments`（当前和潜在部门）。

---

## 输出格式

所有脚本都支持两种输出格式（通过`--format`标志指定）：

- **`text`**（默认）：适合终端查看的格式化文本输出
- **`json`**：适合集成和数据管道处理的机器可读JSON输出

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
# Verify: confirm health_results.json contains the expected number of customer records before continuing

# 2. Identify at-risk accounts
python scripts/churn_risk_analyzer.py customer_portfolio.json --format json > risk_results.json
# Verify: confirm risk_results.json is non-empty and risk tiers are present for each customer

# 3. Find expansion opportunities in healthy accounts
python scripts/expansion_opportunity_scorer.py customer_portfolio.json --format json > expansion_results.json
# Verify: confirm expansion_results.json lists opportunities ranked by priority

# 4. Prepare QBR using templates
# Reference: assets/qbr_template.md
```

**错误处理：** 如果脚本因错误退出，请检查以下内容：
- 输入的JSON文件是否符合该脚本的字段结构要求（参见上述输入要求）
- 所有必需字段是否齐全且输入正确
- 是否使用了Python 3.7及以上版本（运行`python --version`进行验证）
- 在将输出文件传递到后续步骤之前，确保之前的步骤产生的输出文件不为空

---

## 脚本

### 1. health_score_calculator.py

**用途：** 进行多维度的客户健康状况评分，并结合趋势分析和细分市场基准测试。

**评分维度及权重：**
| 维度 | 权重 | 指标          |
|--------|---------|--------------|
| 使用情况 | 30%   | 登录频率、功能采用率、DAU/MAU比率 |
| 参与度 | 25%   | 支持工单数量、会议出席率、NPS/CSAT评分 |
| 支持服务 | 20%   | 待处理工单数量、升级率、平均解决时间 |
| 客户关系 | 25%   | 高管支持者的参与度、多线程处理深度、续订意愿 |

**评分等级：**
- 绿色（75-100分）：客户表现良好
- 黄色（50-74分）：需要关注
- 红色（0-49分）：存在风险，需要立即干预

**使用方法：**
```bash
python scripts/health_score_calculator.py customer_data.json
python scripts/health_score_calculator.py customer_data.json --format json
```

### 2. churn_risk_analyzer.py

**用途：** 通过行为信号检测识别高风险账户，并提供相应的干预建议。

**风险信号权重：**
| 信号类别 | 权重 | 指标            |
|---------|-------------|-------------------|
| 使用量下降 | 30%   | 登录趋势、功能采用率变化、DAU/MAU变化 |
| 参与度下降 | 25%   | 会议取消次数、响应时间、NPS评分变化 |
| 支持问题 | 20%   | 待处理升级工单数量、未解决的关键问题、满意度趋势 |
| 客户关系信号 | 15%   | 负责人更换、支持者变更、竞争对手提及 |
| 商业因素 | 10%   | 合同类型、价格投诉、预算削减 |

**风险等级：**
- 严重（80-100分）：需要立即上报给高管
- 高风险（60-79分）：需要CSM紧急干预
- 中等风险（40-59分）：需要主动跟进
- 低风险（0-39分）：进行常规监控

**使用方法：**
```bash
python scripts/churn_risk_analyzer.py customer_data.json
python scripts/churn_risk_analyzer.py customer_data.json --format json
```

### 3. expansion_opportunity_scorer.py

**用途：** 识别升级销售、交叉销售和扩展机会，并提供收入估算和优先级排序。

**扩展类型：**
- **升级销售**：升级到更高级别的产品或增加现有产品的使用量
- **交叉销售**：添加新的产品模块
- **扩展服务**：增加额外的席位或部门

**使用方法：**
```bash
python scripts/expansion_opportunity_scorer.py customer_data.json
python scripts/expansion_opportunity_scorer.py customer_data.json --format json
```

---

## 参考指南

| 参考文档 | 说明            |
|---------|---------------------------|
| `references/health-scoring-framework.md` | 完整的健康状况评分方法论、维度定义、权重分配依据、阈值调整方法 |
| `references/cs-playbooks.md` | 针对不同风险等级的干预方案、客户入职流程、续订管理、扩展计划和升级流程 |
| `references/cs-metrics-benchmarks.md` | 行业基准数据：净新增客户率（NRR）、净保留率（GRR）、流失率、健康状况评分以及各细分市场和行业的扩展率 |

---

## 模板

| 模板名称 | 用途                          |
|----------|-----------------------------------------|
| `assets/qbr_template.md` | 季度业务回顾演示文稿结构           |
| `assets/success_plan_template.md` | 包含目标、里程碑和指标的客户成功计划           |
| `assets/onboarding_checklist_template.md` | 90天入职检查清单，包含阶段性目标             |
| `assets/executive_business_review_template.md` | 高管利益相关者用于战略账户的审查文档           |

---

## 最佳实践

1. **综合分析多个信号**：结合使用这三个脚本以全面了解客户状况
2. **关注趋势而非静态数据**：绿色等级下降比黄色等级更紧急
3. **调整阈值**：根据产品特性和行业情况，参考`references/health-scoring-framework.md`调整细分市场基准
4. **提前准备数据**：在每次季度业务回顾和高管会议前运行脚本；参考`references/cs-playbooks.md`获取干预建议

---

## 限制

- **无实时数据支持**：脚本仅分析JSON输入文件中的静态数据
- **无法与CRM系统集成**：数据需手动从CRM/客户成功管理系统导出
- **仅基于确定性分析**：评分基于算法和加权信号，不使用预测性机器学习
- **阈值可能需要调整**：默认阈值为行业标准，但可能需根据实际情况进行调整
- **收入估算**：扩展收入估算基于使用模式，仅供参考

---

**最后更新时间：** 2026年2月
**使用的工具：** 3个Python命令行工具
**依赖库：** 仅需Python 3.7及以上的标准库