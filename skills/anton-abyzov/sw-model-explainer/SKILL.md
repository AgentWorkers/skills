---
name: model-explainer
description: |
  Model interpretability and explainability using SHAP, LIME, feature importance, and partial dependence plots. Activates for "explain model", "model interpretability", "SHAP", "LIME", "feature importance", "why prediction", "model explanation". Generates human-readable explanations for model predictions, critical for trust, debugging, and regulatory compliance.
---

# 模型可解释性（Model Explainer）

## 概述

该工具能够将“黑箱”模型转化为可解释的模型，帮助理解模型为何会做出特定预测、哪些特征最为关键，以及这些特征之间是如何相互作用的。这对于建立信任、进行故障排查以及满足监管要求至关重要。

## 可解释性的重要性

- **信任**：利益相关者更愿意信任他们能够理解的模型。
- **故障排查**：有助于发现模型的薄弱环节和潜在偏见。
- **合规性**：根据GDPR（通用数据保护条例）和公平贷款法规，模型需要提供解释性信息。
- **模型改进**：明确需要优化的方面。
- **安全性**：能够及时发现模型可能出现的故障。

## 可解释性的类型

### 1. 全局解释（模型层面）

- **特征重要性**：
    ```python
from specweave import explain_model

explainer = explain_model(
    model=trained_model,
    X_train=X_train,
    increment="0042"
)

# Global feature importance
importance = explainer.feature_importance()
```

    输出：
    ```
Top Features (Global):
1. transaction_amount (importance: 0.35)
2. user_history_days (importance: 0.22)
3. merchant_reputation (importance: 0.18)
4. time_since_last_transaction (importance: 0.15)
5. device_type (importance: 0.10)
```

- **部分依赖关系图**：
    ```python
# How does feature affect prediction?
explainer.partial_dependence(feature="transaction_amount")
```

### 2. 局部解释（预测层面）

- **SHAP值**：
    ```python
# Explain single prediction
explanation = explainer.explain_prediction(X_sample)
```

    输出：
    ```
Prediction: FRAUD (probability: 0.92)

Why?
+ transaction_amount=5000 → +0.45 (high amount increases fraud risk)
+ user_history_days=2 → +0.30 (new user increases risk)
+ merchant_reputation=low → +0.25 (suspicious merchant)
- time_since_last_transaction=1hr → -0.08 (recent activity normal)

Base prediction: 0.10
Final prediction: 0.92
```

- **LIME解释**：
    ```python
# Local interpretable model
lime_exp = explainer.lime_explanation(X_sample)
```

## 在SpecWeave中的使用

```python
from specweave import ModelExplainer

# Create explainer
explainer = ModelExplainer(
    model=model,
    X_train=X_train,
    feature_names=feature_names,
    increment="0042"
)

# Generate all explanations
explainer.generate_all_reports()

# Creates:
# - feature-importance.png
# - shap-summary.png
# - pdp-plots/
# - local-explanations/
# - explainability-report.md
```

## 实际应用案例

### 案例1：欺诈检测

```python
# Explain why transaction flagged as fraud
transaction = {
    "amount": 5000,
    "user_age_days": 2,
    "merchant": "new_merchant_xyz"
}

explanation = explainer.explain(transaction)
print(explanation.to_text())
```

    输出：
    ```
FRAUD ALERT (92% confidence)

Main factors:
1. Large transaction amount ($5000) - Very unusual for new users
2. Account only 2 days old - Fraud pattern
3. Merchant has low reputation score - Red flag

If this is legitimate:
- User should verify identity
- Merchant should be manually reviewed
```

### 案例2：贷款审批

```python
# Explain loan rejection
applicant = {
    "income": 45000,
    "credit_score": 620,
    "debt_ratio": 0.45
}

explanation = explainer.explain(applicant)
print(explanation.to_text())
```

    输出：
    ```
LOAN DENIED

Main reasons:
1. Credit score (620) below threshold (650) - Primary factor
2. High debt-to-income ratio (45%) - Risk indicator
3. Income ($45k) adequate but not strong

To improve approval chances:
- Increase credit score by 30+ points
- Reduce debt-to-income ratio below 40%
```

## 监管合规性

- **GDPR中的“解释权”**：
    ```python
# Generate GDPR-compliant explanation
gdpr_explanation = explainer.gdpr_explanation(prediction)

# Includes:
# - Decision rationale
# - Data used
# - How to contest decision
# - Impact of features
```

- **公平贷款法案**：
    ```python
# Check for bias in protected attributes
bias_report = explainer.fairness_report(
    sensitive_features=["gender", "race", "age"]
)

# Detects:
# - Disparate impact
# - Feature bias
# - Recommendations for fairness
```

## 可视化方式

1. **特征重要性条形图**
2. **SHAP摘要图**（蜂群图形式）
3. **SHAP瀑布图**（针对单个预测结果）
4. **部分依赖关系图**
5. **个体条件期望值**（ICE）
6. **交互式力图**
7. **决策树**（作为替代模型使用）

## 与SpecWeave的集成

```bash
# Generate all explainability artifacts
/ml:explain-model 0042

# Explain specific prediction
/ml:explain-prediction --increment 0042 --sample sample.json

# Check for bias
/ml:fairness-check 0042
```

模型可解释性的相关成果会自动包含在增量文档和项目总结中。

## 最佳实践

1. **为所有生产环境中的模型生成解释性信息**：确保生产环境中不存在“黑箱”模型。
2. **检测模型中的偏见**：对敏感属性进行测试。
3. **记录模型的局限性**：明确模型无法解释的内容。
4. **验证解释结果的合理性**：确保解释结果符合领域常识。
5. **确保解释结果的易读性**：让非技术领域的利益相关者也能理解模型工作原理。

对于负责任的人工智能部署而言，模型的可解释性是不可或缺的。