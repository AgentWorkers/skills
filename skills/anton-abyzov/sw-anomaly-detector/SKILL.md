---
name: anomaly-detector
description: |
  Anomaly and outlier detection using Isolation Forest, One-Class SVM, autoencoders, and statistical methods. Activates for "anomaly detection", "outlier detection", "fraud detection", "intrusion detection", "abnormal behavior", "unusual patterns", "detect anomalies", "system monitoring". Handles supervised and unsupervised anomaly detection with SpecWeave increment integration.
---

# 异常检测器

## 概述

使用统计方法、机器学习和深度学习来检测数据中的异常模式、离群值和异常情况。这对于欺诈检测、安全监控、质量控制以及系统健康监控至关重要——所有这些功能都与 SpecWeave 的增量工作流程集成在一起。

## 异常检测的独特之处

**挑战**：异常现象非常罕见（数据中仅占 0.1% 到 5%）。

**传统分类方法无法有效应对**：
- ❌ 极端的类别不平衡
- ❌ 未知的异常模式
- ❌ 标记异常数据成本高昂
- ❌ 异常现象会随时间演变

**异常检测方法**：
- ✅ 无监督学习（无需标签）
- ✅ 半监督学习（从正常数据中学习）
- ✅ 统计方法（检测数据与预期的偏差）
- ✅ 具有上下文感知能力（判断在特定用户、时间和地点什么是“正常”行为）

## 异常检测方法

### 1. 统计方法（基础方法）

**Z 分数 / 标准差**：
```python
from specweave import AnomalyDetector

detector = AnomalyDetector(
    method="statistical",
    increment="0042"
)

# Flag values > 3 standard deviations from mean
anomalies = detector.detect(
    data=transaction_amounts,
    threshold=3.0
)

# Simple, fast, but assumes normal distribution
```

**四分位数范围 (IQR)**：
```python
# More robust to non-normal distributions
detector = AnomalyDetector(method="iqr")

# Flag values outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
anomalies = detector.detect(data=response_times)

# Good for skewed distributions
```

### 2. 隔离森林 (推荐方法)

**适用场景**：通用场景，高维数据

```python
from specweave import IsolationForestDetector

detector = IsolationForestDetector(
    contamination=0.05,  # Expected anomaly rate (5%)
    increment="0042"
)

# Train on normal data (or mixed data)
detector.fit(X_train)

# Detect anomalies
predictions = detector.predict(X_test)
# -1 = anomaly, 1 = normal

anomaly_scores = detector.score(X_test)
# Lower score = more anomalous

# Generates:
# - Anomaly scores for all samples
# - Feature importance (which features contribute to anomaly)
# - Threshold visualization
# - Top anomalies ranked by score
```

**隔离森林的优势**：
- 处理速度快（时间复杂度为 O(n log n)）
- 良好地处理高维数据
- 对数据分布没有严格要求
- 异常值更容易被识别（分裂次数较少）

### 3. 单类支持向量机 (One-Class SVM)

**适用场景**：仅使用正常数据进行训练时

```python
from specweave import OneClassSVMDetector

# Train only on normal transactions
detector = OneClassSVMDetector(
    kernel='rbf',
    nu=0.05,  # Expected anomaly rate
    increment="0042"
)

detector.fit(X_normal)

# Detect anomalies in new data
predictions = detector.predict(X_new)
# -1 = anomaly, 1 = normal

# Good for: Clean training data of normal samples
```

### 4. 自编码器 (深度学习)

**适用场景**：复杂模式、高维数据、图像处理

```python
from specweave import AutoencoderDetector

# Learn to reconstruct normal data
detector = AutoencoderDetector(
    encoding_dim=32,  # Compressed representation
    layers=[64, 32, 16, 32, 64],
    increment="0042"
)

# Train on normal data
detector.fit(
    X_normal,
    epochs=100,
    validation_split=0.2
)

# Anomalies have high reconstruction error
anomaly_scores = detector.score(X_test)

# Generates:
# - Reconstruction error distribution
# - Threshold recommendation
# - Top anomalies with explanations
# - Learned representations (t-SNE plot)
```

**自编码器的工作原理**：
```
Input → Encoder → Compressed → Decoder → Reconstructed

Normal data: Low reconstruction error (learned well)
Anomalies: High reconstruction error (never seen before)
```

### 5. 局部异常因子 (Local Outlier Factor, LOF)

**适用场景**：基于密度的异常检测（适用于数据分布稀疏的情况）

```python
from specweave import LOFDetector

# Detects points in low-density regions
detector = LOFDetector(
    n_neighbors=20,
    contamination=0.05,
    increment="0042"
)

detector.fit(X_train)
predictions = detector.predict(X_test)

# Good for: Clustered data with sparse anomalies
```

## 异常检测工作流程

### 工作流程 1：欺诈检测

```python
from specweave import FraudDetectionPipeline

pipeline = FraudDetectionPipeline(increment="0042")

# Features: transaction amount, location, time, merchant, etc.
pipeline.fit(normal_transactions)

# Real-time fraud detection
fraud_scores = pipeline.predict_proba(new_transactions)

# For each transaction:
# - Fraud probability (0-1)
# - Anomaly score
# - Contributing features
# - Similar past cases

# Generates:
# - Precision-Recall curve (fraud is rare)
# - Cost-benefit analysis (false positives vs missed fraud)
# - Feature importance for fraud
# - Fraud patterns identified
```

**欺诈检测的最佳实践**：
```python
# 1. Use multiple signals
pipeline.add_signals([
    'amount_vs_user_average',
    'distance_from_home',
    'merchant_risk_score',
    'velocity_24h'  # Transactions in last 24h
])

# 2. Set threshold based on cost
# False Positive cost: $5 (manual review)
# False Negative cost: $500 (fraud loss)
# Optimal threshold: Maximize (savings - review_cost)

# 3. Provide explanations
explanation = pipeline.explain_prediction(suspicious_transaction)
# "Flagged because: amount 10x user average, new merchant, foreign location"
```

### 工作流程 2：系统异常检测

```python
from specweave import SystemAnomalyPipeline

# Monitor system metrics (CPU, memory, latency, errors)
pipeline = SystemAnomalyPipeline(increment="0042")

# Train on normal system behavior
pipeline.fit(normal_metrics)

# Detect system anomalies
anomalies = pipeline.detect(current_metrics)

# For each anomaly:
# - Severity (low, medium, high, critical)
# - Affected metrics
# - Similar past incidents
# - Recommended actions

# Generates:
# - Anomaly timeline
# - Metric correlations (which metrics moved together)
# - Root cause analysis
# - Alert rules
```

**系统监控的最佳实践**：
```python
# 1. Use time windows
pipeline.add_time_windows([
    '5min',   # Immediate spikes
    '1hour',  # Short-term trends
    '24hour'  # Daily patterns
])

# 2. Correlate metrics
pipeline.detect_correlations([
    ('high_cpu', 'slow_response'),
    ('memory_leak', 'increasing_errors')
])

# 3. Reduce alert fatigue
pipeline.set_alert_rules(
    min_severity='medium',
    min_duration='5min',  # Ignore transient spikes
    max_alerts_per_hour=5
)
```

### 工作流程 3：制造质量控制

```python
from specweave import QualityControlPipeline

# Detect defective products from sensor data
pipeline = QualityControlPipeline(increment="0042")

# Train on good products
pipeline.fit(good_product_sensors)

# Detect defects in production line
defect_scores = pipeline.predict(production_line_data)

# Generates:
# - Real-time defect alerts
# - Defect rate trends
# - Most common defect patterns
# - Preventive maintenance recommendations
```

### 工作流程 4：网络入侵检测

```python
from specweave import IntrusionDetectionPipeline

# Detect malicious network traffic
pipeline = IntrusionDetectionPipeline(increment="0042")

# Features: packet size, frequency, ports, protocols, etc.
pipeline.fit(normal_network_traffic)

# Detect intrusions
intrusions = pipeline.detect(network_traffic_stream)

# Generates:
# - Attack type classification (DDoS, port scan, etc.)
# - Severity scores
# - Source IPs
# - Attack timeline
```

## 评估指标

**异常检测的评估指标**（与分类方法不同）：

```python
from specweave import AnomalyEvaluator

evaluator = AnomalyEvaluator(increment="0042")

metrics = evaluator.evaluate(
    y_true=true_labels,  # 0=normal, 1=anomaly
    y_pred=predictions,
    y_scores=anomaly_scores
)
```

**关键指标**：
1. **精确度 @ K**：在标记为异常的前 K 个结果中，有多少是真正的异常？
   ```python
   precision_at_100 = evaluator.precision_at_k(k=100)
   # "Of 100 flagged transactions, 85 were actual fraud" = 85%
   ```

2. **召回率 @ K**：在所有真正的异常中，有多少被正确地检测到了？
   ```python
   recall_at_100 = evaluator.recall_at_k(k=100)
   # "We caught 78% of all fraud in top 100 flagged"
   ```

3. **ROC-AUC**：整体区分能力
   ```python
   roc_auc = evaluator.roc_auc(y_true, y_scores)
   # 0.95 = excellent discrimination
   ```

4. **PR-AUC**：更适合数据不平衡的情况
   ```python
   pr_auc = evaluator.pr_auc(y_true, y_scores)
   # More informative when anomalies are rare (<5%)
   ```

**评估报告**：
```markdown
# Anomaly Detection Evaluation

## Dataset
- Total samples: 100,000
- Anomalies: 500 (0.5%)
- Features: 25

## Method: Isolation Forest

## Performance Metrics
- ROC AUC: 0.94 ✅ (excellent)
- PR AUC: 0.78 ✅ (good for 0.5% anomaly rate)

## Precision-Recall Tradeoff
- Precision @ 100: 85% (85 true anomalies in top 100)
- Recall @ 100: 17% (caught 17% of all anomalies)
- Precision @ 500: 62% (310 true anomalies in top 500)
- Recall @ 500: 62% (caught 62% of all anomalies)

## Business Impact (Fraud Detection Example)
- Review budget: 500 transactions/day
- At Precision @ 500 = 62%:
  - True fraud caught: 310/day ($155,000 saved)
  - False positives: 190/day ($950 review cost)
  - Net benefit: $154,050/day ✅

## Recommendation
✅ DEPLOY with threshold for top 500 (62% precision)
```

## 与 SpecWeave 的集成

### 增量工作流程结构

```
.specweave/increments/0042-fraud-detection/
├── spec.md (detection requirements, business impact)
├── plan.md (method selection, threshold tuning)
├── tasks.md
├── data/
│   ├── normal_transactions.csv
│   ├── labeled_fraud.csv (if available)
│   └── schema.yaml
├── experiments/
│   ├── statistical-baseline/
│   ├── isolation-forest/
│   ├── one-class-svm/
│   └── autoencoder/
├── models/
│   ├── isolation_forest_model.pkl
│   └── threshold_config.json
├── evaluation/
│   ├── precision_recall_curve.png
│   ├── roc_curve.png
│   ├── top_anomalies.csv
│   └── evaluation_report.md
└── deployment/
    ├── real_time_api.py
    ├── monitoring_dashboard.json
    └── alert_rules.yaml
```

## 最佳实践

### 1. 首先使用已标记的异常数据（如果有的话）

```python
# Use labeled data to validate unsupervised methods
detector.fit(X_train)  # Unlabeled

# Evaluate on labeled test set
metrics = evaluator.evaluate(y_true_test, detector.predict(X_test))

# Choose method with best precision @ K
```

### 2. 调整异常检测的参数

```python
# Try different contamination rates
for contamination in [0.01, 0.05, 0.1, 0.2]:
    detector = IsolationForestDetector(contamination=contamination)
    detector.fit(X_train)
    
    metrics = evaluator.evaluate(y_test, detector.predict(X_test))
    
# Choose contamination that maximizes business value
```

### 3. 解释异常结果

```python
# Don't just flag anomalies - explain why
explainer = AnomalyExplainer(detector, increment="0042")

for anomaly in top_anomalies:
    explanation = explainer.explain(anomaly)
    print(f"Anomaly: {anomaly.id}")
    print(f"Reasons:")
    print(f"  - {explanation.top_features}")
    print(f"  - Similar cases: {explanation.similar_cases}")
```

### 4. 应对概念漂移（Concept Drift）

```python
# Anomalies evolve over time
monitor = AnomalyMonitor(increment="0042")

# Track detection performance
monitor.track_daily_performance()

# Retrain when accuracy drops
if monitor.performance_degraded():
    detector.retrain(new_normal_data)
```

### 5. 设置基于业务需求的阈值

```python
# Balance false positives vs false negatives
optimizer = ThresholdOptimizer(increment="0042")

optimal_threshold = optimizer.find_optimal(
    detector=detector,
    data=validation_data,
    false_positive_cost=5,    # $5 per manual review
    false_negative_cost=500   # $500 per missed fraud
)

# Use optimal threshold for deployment
```

## 高级功能

### 1. 集成式异常检测方法

```python
# Combine multiple detectors
ensemble = AnomalyEnsemble(increment="0042")

ensemble.add_detector("isolation_forest", weight=0.4)
ensemble.add_detector("one_class_svm", weight=0.3)
ensemble.add_detector("autoencoder", weight=0.3)

# Ensemble vote (more robust)
anomalies = ensemble.detect(X_test)
```

### 2. 基于上下文的异常检测

```python
# What's normal varies by context
detector = ContextualAnomalyDetector(increment="0042")

# Different normality for different contexts
detector.fit(data, contexts=['user_id', 'time_of_day', 'location'])

# $10 transaction: Normal for user A, anomaly for user B
```

### 3. 顺序式异常检测

```python
# Detect anomalous sequences (not just individual points)
detector = SequenceAnomalyDetector(
    method='lstm',
    window_size=10,
    increment="0042"
)

# Example: Login from unusual sequence of locations
```

## 命令操作

```bash
# Train anomaly detector
/ml:train-anomaly-detector 0042

# Evaluate detector
/ml:evaluate-anomaly-detector 0042

# Explain top anomalies
/ml:explain-anomalies 0042 --top 100
```

## 总结

异常检测在以下领域至关重要：
- ✅ 欺诈检测（金融交易）
- ✅ 安全监控（入侵检测）
- ✅ 质量控制（制造缺陷）
- ✅ 系统健康监控（性能评估）
- ✅ 商业智能（识别异常行为）

该技能提供了经过实战验证的方法，并与 SpecWeave 的增量工作流程集成，确保异常检测器的可复现性、可解释性以及与业务需求的契合度。