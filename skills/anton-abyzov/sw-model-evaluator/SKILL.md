---
name: model-evaluator
description: |
  Comprehensive ML model evaluation with multiple metrics, cross-validation, and statistical testing. Activates for "evaluate model", "model metrics", "model performance", "compare models", "validation metrics", "test accuracy", "precision recall", "ROC AUC". Generates detailed evaluation reports with visualizations and statistical significance tests, integrated with SpecWeave increment documentation.
---

# 模型评估器

## 概述

本工具遵循机器学习的最佳实践，提供全面且无偏的模型评估服务。它不仅关注模型的准确性，还从多个维度对模型进行评估，从而帮助用户做出更加可靠的部署决策。

## 核心评估框架

### 1. 分类指标
- 准确率（Accuracy）、精确度（Precision）、召回率（Recall）、F1分数（F1-score）
- ROC-AUC曲线、PR-AUC曲线
- 混淆矩阵（Confusion matrix）
- 多类分类时的类别指标（Per-class metrics）
- 处理类别不平衡问题（Class imbalance handling）

### 2. 回归指标
- 均方根误差（RMSE）、平均绝对误差（MAE）、平均百分比误差（MAPE）
- R²分数、调整后的R²分数（Adjusted R²）
- 剩差分析（Residual analysis）
- 预测区间覆盖率（Prediction interval coverage）

### 3. 推荐系统评估指标
- 精确度@K（Precision@K）、召回率@K（Recall@K）
- NDCG@K、MAP@K（NDCG@K、MAP@K）
- 平均倒数排名（MRR，Mean Reciprocal Rank）
- 覆盖率（Coverage）、多样性（Diversity）

### 4. 统计验证
- 交叉验证（Cross-validation，包括K折法、分层法、时间序列法）
- 置信区间（Confidence intervals）
- 统计显著性检验（Statistical significance testing）
- 校准曲线（Calibration curves）

## 使用方法

```python
from specweave import ModelEvaluator

evaluator = ModelEvaluator(
    model=trained_model,
    X_test=X_test,
    y_test=y_test,
    increment="0042"
)

# Comprehensive evaluation
report = evaluator.evaluate_all()

# Generates:
# - .specweave/increments/0042.../evaluation-report.md
# - Visualizations (confusion matrix, ROC curves, etc.)
# - Statistical tests
```

## 评估报告结构

```markdown
# Model Evaluation Report: XGBoost Classifier

## Overall Performance
- **Accuracy**: 0.87 ± 0.02 (95% CI: [0.85, 0.89])
- **ROC AUC**: 0.92 ± 0.01
- **F1 Score**: 0.85 ± 0.02

## Per-Class Performance
| Class   | Precision | Recall | F1   | Support |
|---------|-----------|--------|------|---------|
| Class 0 | 0.88      | 0.85   | 0.86 | 1000    |
| Class 1 | 0.84      | 0.87   | 0.86 | 800     |

## Confusion Matrix
[Visualization embedded]

## Cross-Validation Results
- 5-fold CV accuracy: 0.86 ± 0.03
- Fold scores: [0.85, 0.88, 0.84, 0.87, 0.86]
- No overfitting detected (train=0.89, val=0.86, gap=0.03)

## Statistical Tests
- Comparison vs baseline: p=0.001 (highly significant)
- Comparison vs previous model: p=0.042 (significant)

## Recommendations
✅ Deploy: Model meets accuracy threshold (>0.85)
✅ Stable: Low variance across folds
⚠️  Monitor: Class 1 recall slightly lower (0.84)
```

## 模型比较

```python
from specweave import compare_models

models = {
    "baseline": baseline_model,
    "xgboost": xgb_model,
    "lightgbm": lgbm_model,
    "neural-net": nn_model
}

comparison = compare_models(
    models,
    X_test,
    y_test,
    metrics=["accuracy", "auc", "f1"],
    increment="0042"
)
```

**输出结果**

```
Model Comparison Report
=======================

| Model      | Accuracy | ROC AUC | F1   | Inference Time | Model Size |
|------------|----------|---------|------|----------------|------------|
| baseline   | 0.65     | 0.70    | 0.62 | 1ms           | 10KB       |
| xgboost    | 0.87     | 0.92    | 0.85 | 35ms          | 12MB       |
| lightgbm   | 0.86     | 0.91    | 0.84 | 28ms          | 8MB        |
| neural-net | 0.85     | 0.90    | 0.83 | 120ms         | 45MB       |

Recommendation: XGBoost
- Best accuracy and AUC
- Acceptable inference time (<50ms requirement)
- Good size/performance tradeoff
```

## 最佳实践

1. **始终与基线进行比较** – 可以使用随机样本、多数样本或基于规则的基线。
2. **使用交叉验证** – 切勿仅依赖单次训练结果。
3. **检查模型校准情况** – 模型的预测概率是否具有实际意义？
4. **分析错误类型** – 了解模型犯错的类型。
5. **测试统计显著性** – 确认模型的改进是真实的。

## 与SpecWeave的集成

```bash
# Evaluate model in increment
/ml:evaluate-model 0042

# Compare all models in increment
/ml:compare-models 0042

# Generate full evaluation report
/ml:evaluation-report 0042
```

评估结果会自动包含在`COMPLETION-SUMMARY.md`文件中。