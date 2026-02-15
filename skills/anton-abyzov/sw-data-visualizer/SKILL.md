---
name: data-visualizer
description: |
  Automated data visualization for EDA, model performance, and business reporting. Activates for "visualize data", "create plots", "EDA", "exploratory analysis", "confusion matrix", "ROC curve", "feature distribution", "correlation heatmap", "plot results", "dashboard". Generates publication-quality visualizations integrated with SpecWeave increments.
---

# 数据可视化工具

## 概述

该工具支持自动化数据可视化生成，适用于探索性数据分析、模型性能报告以及与利益相关者的沟通。它可以生成符合出版标准的图表、交互式仪表板以及易于理解的商务报告，并且所有这些功能都与 SpecWeave 的增量工作流程紧密集成。

## 可视化类别

### 1. 探索性数据分析（EDA）

**自动化 EDA 报告**：
```python
from specweave import EDAVisualizer

visualizer = EDAVisualizer(increment="0042")

# Generates comprehensive EDA report
report = visualizer.generate_eda_report(df)

# Creates:
# - Dataset overview (rows, columns, memory, missing values)
# - Numerical feature distributions (histograms + KDE)
# - Categorical feature counts (bar charts)
# - Correlation heatmap
# - Missing value pattern
# - Outlier detection plots
# - Feature relationships (pairplot for top features)
```

**单个 EDA 图表**：
```python
# Distribution plots
visualizer.plot_distribution(
    data=df['age'],
    title="Age Distribution",
    bins=30
)

# Correlation heatmap
visualizer.plot_correlation_heatmap(
    data=df[numerical_columns],
    method='pearson'  # or 'spearman', 'kendall'
)

# Missing value patterns
visualizer.plot_missing_values(df)

# Outlier detection (boxplots)
visualizer.plot_outliers(df[numerical_columns])
```

### 2. 模型性能可视化

**分类模型性能**：
```python
from specweave import ClassificationVisualizer

viz = ClassificationVisualizer(increment="0042")

# Confusion matrix
viz.plot_confusion_matrix(
    y_true=y_test,
    y_pred=y_pred,
    classes=['Negative', 'Positive']
)

# ROC curve
viz.plot_roc_curve(
    y_true=y_test,
    y_proba=y_proba
)

# Precision-Recall curve
viz.plot_precision_recall_curve(
    y_true=y_test,
    y_proba=y_proba
)

# Learning curves (train vs val)
viz.plot_learning_curve(
    train_scores=train_scores,
    val_scores=val_scores
)

# Calibration curve (are probabilities well-calibrated?)
viz.plot_calibration_curve(
    y_true=y_test,
    y_proba=y_proba
)
```

**回归模型性能**：
```python
from specweave import RegressionVisualizer

viz = RegressionVisualizer(increment="0042")

# Predicted vs Actual
viz.plot_predictions(
    y_true=y_test,
    y_pred=y_pred
)

# Residual plot
viz.plot_residuals(
    y_true=y_test,
    y_pred=y_pred
)

# Residual distribution (should be normal)
viz.plot_residual_distribution(
    residuals=y_test - y_pred
)

# Error by feature value
viz.plot_error_analysis(
    y_true=y_test,
    y_pred=y_pred,
    features=X_test
)
```

### 3. 特征分析可视化

**特征重要性分析**：
```python
from specweave import FeatureVisualizer

viz = FeatureVisualizer(increment="0042")

# Feature importance (bar chart)
viz.plot_feature_importance(
    feature_names=feature_names,
    importances=model.feature_importances_,
    top_n=20
)

# SHAP summary plot
viz.plot_shap_summary(
    shap_values=shap_values,
    features=X_test
)

# Partial dependence plots
viz.plot_partial_dependence(
    model=model,
    features=['age', 'income'],
    X=X_train
)

# Feature interaction
viz.plot_feature_interaction(
    model=model,
    features=('age', 'income'),
    X=X_train
)
```

### 4. 时间序列可视化

**时间序列图表**：
```python
from specweave import TimeSeriesVisualizer

viz = TimeSeriesVisualizer(increment="0042")

# Time series with trend
viz.plot_timeseries(
    data=sales_data,
    show_trend=True
)

# Seasonal decomposition
viz.plot_seasonal_decomposition(
    data=sales_data,
    period=12  # Monthly seasonality
)

# Autocorrelation (ACF, PACF)
viz.plot_autocorrelation(data=sales_data)

# Forecast with confidence intervals
viz.plot_forecast(
    actual=test_data,
    forecast=forecast,
    confidence_intervals=(0.80, 0.95)
)
```

### 5. 模型比较可视化

**多模型对比**：
```python
from specweave import ModelComparisonVisualizer

viz = ModelComparisonVisualizer(increment="0042")

# Compare metrics across models
viz.plot_model_comparison(
    models=['Baseline', 'XGBoost', 'LightGBM', 'Neural Net'],
    metrics={
        'accuracy': [0.65, 0.87, 0.86, 0.85],
        'roc_auc': [0.70, 0.92, 0.91, 0.90],
        'training_time': [1, 45, 32, 320]
    }
)

# ROC curves for multiple models
viz.plot_roc_curves_comparison(
    models_predictions={
        'XGBoost': (y_test, y_proba_xgb),
        'LightGBM': (y_test, y_proba_lgbm),
        'Neural Net': (y_test, y_proba_nn)
    }
)
```

## 交互式可视化

**与 Plotly 的集成**：
```python
from specweave import InteractiveVisualizer

viz = InteractiveVisualizer(increment="0042")

# Interactive scatter plot (zoom, pan, hover)
viz.plot_interactive_scatter(
    x=X_test[:, 0],
    y=X_test[:, 1],
    colors=y_pred,
    hover_data=df[['id', 'amount', 'merchant']]
)

# Interactive confusion matrix (click for details)
viz.plot_interactive_confusion_matrix(
    y_true=y_test,
    y_pred=y_pred
)

# Interactive feature importance (sortable, filterable)
viz.plot_interactive_feature_importance(
    feature_names=feature_names,
    importances=importances
)
```

## 商务报告

**自动化机器学习报告**：
```python
from specweave import MLReportGenerator

generator = MLReportGenerator(increment="0042")

# Generate executive summary report
report = generator.generate_report(
    model=model,
    test_data=(X_test, y_test),
    business_metrics={
        'false_positive_cost': 5,
        'false_negative_cost': 500
    }
)

# Creates:
# - Executive summary (1 page, non-technical)
# - Key metrics (accuracy, precision, recall)
# - Business impact ($$ saved, ROI)
# - Model performance visualizations
# - Recommendations
# - Technical appendix
```

**报告输出（HTML/PDF）**：
```markdown
# Fraud Detection Model - Executive Summary

## Key Results
- **Accuracy**: 87% (target: >85%) ✅
- **Fraud Detection Rate**: 62% (catching 310 frauds/day)
- **False Positive Rate**: 38% (190 false alarms/day)

## Business Impact
- **Fraud Prevented**: $155,000/day
- **Review Cost**: $950/day (190 transactions × $5)
- **Net Benefit**: $154,050/day ✅
- **Annual Savings**: $56.2M

## Model Performance
[Confusion Matrix Visualization]
[ROC Curve]
[Feature Importance]

## Recommendations
1. ✅ Deploy to production immediately
2. Monitor fraud patterns weekly
3. Retrain model monthly with new data
```

## 仪表板创建

**实时仪表板**：
```python
from specweave import DashboardCreator

creator = DashboardCreator(increment="0042")

# Create Grafana/Plotly dashboard
dashboard = creator.create_dashboard(
    title="Model Performance Dashboard",
    panels=[
        {'type': 'metric', 'query': 'prediction_latency_p95'},
        {'type': 'metric', 'query': 'predictions_per_second'},
        {'type': 'timeseries', 'query': 'accuracy_over_time'},
        {'type': 'timeseries', 'query': 'error_rate'},
        {'type': 'heatmap', 'query': 'prediction_distribution'},
        {'type': 'table', 'query': 'recent_anomalies'}
    ]
)

# Exports to Grafana JSON or Plotly Dash app
dashboard.export(format='grafana')
```

## 可视化最佳实践

### 1. 符合出版标准的图表**

```python
# Set consistent styling
visualizer.set_style(
    style='seaborn',  # Or 'ggplot', 'fivethirtyeight'
    context='paper',  # Or 'notebook', 'talk', 'poster'
    palette='colorblind'  # Accessible colors
)

# High-resolution exports
visualizer.save_figure(
    filename='model_performance.png',
    dpi=300,  # Publication quality
    bbox_inches='tight'
)
```

### 2. 易于理解的可视化效果**

```python
# Colorblind-friendly palettes
visualizer.use_colorblind_palette()

# Add alt text for accessibility
visualizer.add_alt_text(
    plot=fig,
    description="Confusion matrix showing 87% accuracy"
)

# High contrast for presentations
visualizer.set_high_contrast_mode()
```

### 3. 图表注释与上下文说明**

```python
# Add reference lines
viz.add_reference_line(
    y=0.85,  # Target accuracy
    label='Target',
    color='red',
    linestyle='--'
)

# Add annotations
viz.annotate_point(
    x=optimal_threshold,
    y=optimal_f1,
    text='Optimal threshold: 0.47'
)
```

## 与 SpecWeave 的集成

**自动化增量式可视化生成**：
```python
# All visualizations auto-saved to increment folder
visualizer = EDAVisualizer(increment="0042")

# Creates:
# .specweave/increments/0042-fraud-detection/
# ├── visualizations/
# │   ├── eda/
# │   │   ├── distributions.png
# │   │   ├── correlation_heatmap.png
# │   │   └── missing_values.png
# │   ├── model_performance/
# │   │   ├── confusion_matrix.png
# │   │   ├── roc_curve.png
# │   │   ├── precision_recall.png
# │   │   └── learning_curves.png
# │   ├── feature_analysis/
# │   │   ├── feature_importance.png
# │   │   ├── shap_summary.png
# │   │   └── partial_dependence/
# │   └── reports/
# │       ├── executive_summary.html
# │       └── technical_report.pdf
```

**与动态文档系统的集成**：
```bash
/sw:sync-docs update
```

**更新机制**：
```markdown
<!-- .specweave/docs/internal/architecture/ml-model-performance.md -->

## Fraud Detection Model Performance (Increment 0042)

### Model Accuracy
![Confusion Matrix](../../../increments/0042-fraud-detection/visualizations/confusion_matrix.png)

### Key Metrics
- Accuracy: 87%
- Precision: 85%
- Recall: 62%
- ROC AUC: 0.92

### Feature Importance
![Top Features](../../../increments/0042-fraud-detection/visualizations/feature_importance.png)

Top 5 features:
1. amount_vs_user_average (0.18)
2. days_since_last_purchase (0.12)
3. merchant_risk_score (0.10)
4. velocity_24h (0.08)
5. location_distance_from_home (0.07)
```

## 命令操作

```bash
# Generate EDA report
/ml:visualize-eda 0042

# Generate model performance report
/ml:visualize-performance 0042

# Create interactive dashboard
/ml:create-dashboard 0042

# Export all visualizations
/ml:export-visualizations 0042 --format png,pdf,html
```

## 高级功能

### 1. 自动化报告生成**

```python
# Generate full increment report with all visualizations
generator = IncrementReportGenerator(increment="0042")

report = generator.generate_full_report()

# Includes:
# - EDA visualizations
# - Experiment comparisons
# - Best model performance
# - Feature importance
# - Business impact
# - Deployment readiness
```

### 2. 自定义可视化模板**

```python
# Create reusable templates
template = VisualizationTemplate(name="fraud_analysis")

template.add_panel("confusion_matrix")
template.add_panel("roc_curve")
template.add_panel("top_fraud_features")
template.add_panel("fraud_trends_over_time")

# Apply to any increment
template.apply(increment="0042")
```

### 3. 可视化的版本控制**

```python
# Track visualization changes across model versions
viz_tracker = VisualizationTracker(increment="0042")

# Compare model v1 vs v2 visualizations
viz_tracker.compare_versions(
    version_1="model-v1",
    version_2="model-v2"
)

# Shows: Confusion matrix improved, ROC curve comparison, etc.
```

## 总结

数据可视化在以下方面至关重要：
- ✅ 探索性数据分析（在建模前理解数据）
- ✅ 模型性能沟通（获得利益相关者的认可）
- ✅ 特征分析（了解影响预测的因素）
- ✅ 商务报告（将指标转化为实际业务影响）
- ✅ 模型调试（通过可视化方式发现问题）

该工具实现了自动化的可视化生成，确保所有机器学习相关工作都以直观、易于理解的方式呈现，并且完全符合 SpecWeave 的增量工作流程要求。