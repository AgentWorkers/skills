---
name: ml-pipeline-orchestrator
description: |
  Orchestrates complete machine learning pipelines within SpecWeave increments. Activates when users request "ML pipeline", "train model", "build ML system", "end-to-end ML", "ML workflow", "model training pipeline", or similar. Guides users through data preprocessing, feature engineering, model training, evaluation, and deployment using SpecWeave's spec-driven approach. Integrates with increment lifecycle for reproducible ML development.
---

# ML Pipeline Orchestrator

## 概述

该技能将机器学习（ML）开发过程转化为基于 SpecWeave 增量开发的工作流程，确保每个 ML 项目都遵循统一的、规范化的方法：从需求分析（spec）到计划制定（plan），再到任务分配（tasks）、实施（implement）和验证（validate）。它能够协调整个 ML 生命周期，从数据探索到模型部署，同时提供完整的可追溯性和实时文档记录。

## 核心理念

**SpecWeave + ML = 规范化的数据科学**

传统的 ML 开发过程往往缺乏结构化：
- ❌ 使用没有版本控制的 Jupyter 笔记本
- ❌ 实验过程没有文档记录
- 部署的模型缺乏可重复性
- 团队知识仅存在于个人的笔记本中

SpecWeave 引入了规范化的流程：
- ✅ 每个 ML 功能都对应一个开发增量（包括需求分析、计划和具体任务）
- ✅ 实验过程被自动跟踪和记录
- 模型版本与开发增量紧密关联
- 实时文档记录了开发过程中的学习成果和决策内容

## 工作原理

### 第 1 阶段：ML 增量规划

当您请求“构建一个推荐模型”时，该技能会：
1. **创建 ML 开发增量结构**：
```
.specweave/increments/0042-recommendation-model/
├── spec.md                    # ML requirements, success metrics
├── plan.md                    # Pipeline architecture
├── tasks.md                   # Implementation tasks
├── tests.md                   # Evaluation criteria
├── experiments/               # Experiment tracking
│   ├── exp-001-baseline/
│   ├── exp-002-xgboost/
│   └── exp-003-neural-net/
├── data/                      # Data samples, schemas
│   ├── schema.yaml
│   └── sample.csv
├── models/                    # Trained models
│   ├── model-v1.pkl
│   └── model-v2.pkl
└── notebooks/                 # Exploratory notebooks
    ├── 01-eda.ipynb
    └── 02-feature-engineering.ipynb
```

2. **生成特定于 ML 的需求文档（spec.md）**：
```markdown
## ML Problem Definition
- Problem type: Recommendation (collaborative filtering)
- Input: User behavior history
- Output: Top-N product recommendations
- Success metrics: Precision@10 > 0.25, Recall@10 > 0.15

## Data Requirements
- Training data: 6 months user interactions
- Validation: Last month
- Features: User profile, product attributes, interaction history

## Model Requirements
- Latency: <100ms inference
- Throughput: 1000 req/sec
- Accuracy: Better than random baseline by 3x
- Explainability: Must explain top-3 recommendations
```

3. **生成特定于 ML 的任务列表（tasks.md）**：
```markdown
- [ ] T-001: Data exploration and quality analysis
- [ ] T-002: Feature engineering pipeline
- [ ] T-003: Train baseline model (random/popularity)
- [ ] T-004: Train candidate models (3 algorithms)
- [ ] T-005: Hyperparameter tuning (best model)
- [ ] T-006: Model evaluation (all metrics)
- [ ] T-007: Model explainability (SHAP/LIME)
- [ ] T-008: Production deployment preparation
- [ ] T-009: A/B test plan
```

### 第 2 阶段：流程执行

该技能会按照最佳实践指导您完成每个任务：

#### 任务 1：数据探索
```python
# Generated template with SpecWeave integration
import pandas as pd
import mlflow
from specweave import track_experiment

# Auto-logs to .specweave/increments/0042.../experiments/
with track_experiment("exp-001-eda") as exp:
    df = pd.read_csv("data/interactions.csv")
    
    # EDA
    exp.log_param("dataset_size", len(df))
    exp.log_metric("missing_values", df.isnull().sum().sum())
    
    # Auto-generates report in increment folder
    exp.save_report("eda-summary.md")
```

#### 任务 3：训练基线模型
```python
from sklearn.dummy import DummyClassifier
from specweave import track_model

with track_model("baseline-random", increment="0042") as model:
    clf = DummyClassifier(strategy="uniform")
    clf.fit(X_train, y_train)
    
    # Automatically logged to increment
    model.log_metrics({
        "accuracy": 0.12,
        "precision@10": 0.08
    })
    model.save_artifact(clf, "baseline.pkl")
```

#### 任务 4：训练候选模型
```python
from xgboost import XGBClassifier
from specweave import ModelExperiment

# Parallel experiments with auto-tracking
experiments = [
    ModelExperiment("xgboost", XGBClassifier, params_xgb),
    ModelExperiment("lightgbm", LGBMClassifier, params_lgbm),
    ModelExperiment("neural-net", KerasModel, params_nn)
]

results = run_experiments(
    experiments,
    increment="0042",
    save_to="experiments/"
)

# Auto-generates comparison table in increment docs
```

### 第 3 阶段：增量完成

当执行 `/sw:done 0042` 命令时：
1. **验证 ML 开发的各项标准**：
   - ✅ 所有实验过程都被记录下来
   - 最优模型被保存
   - 评估指标被记录在文档中
   - 模型的可解释性相关文档也已生成

2. **生成完成总结**：
```markdown
## Recommendation Model - COMPLETE

### Experiments Run: 7
1. exp-001-baseline (random): precision@10=0.08
2. exp-002-popularity: precision@10=0.18
3. exp-003-xgboost: precision@10=0.26 ✅ BEST
4. exp-004-lightgbm: precision@10=0.24
5. exp-005-neural-net: precision@10=0.22
...

### Best Model
- Algorithm: XGBoost
- Version: model-v3.pkl
- Metrics: precision@10=0.26, recall@10=0.16
- Training time: 45 min
- Model size: 12 MB

### Deployment Ready
- ✅ Inference latency: 35ms (target: <100ms)
- ✅ Explainability: SHAP values computed
- ✅ A/B test plan documented
```

3. **同步实时文档**（通过 `/sw:sync-docs` 命令）：
   - 更新架构文档以反映模型设计
   - 添加算法选择的决策记录（ADR）
   - 将学习成果记录在运行手册中

## 适用场景

在以下情况下使用该技能：
- **端到端构建 ML 功能**——从想法到模型部署
- **确保实验的可重复性**——所有实验都被跟踪和记录
- **遵循 ML 最佳实践**——进行基线比较、正确验证和模型可解释性分析
- **将 ML 与软件工程集成**——将 ML 开发视为连续的增量过程，而非孤立的笔记本
- **维护团队知识**——实时文档记录决策背后的原因

## ML 流程阶段

### 1. 数据阶段
- 数据探索（EDA）
- 数据质量评估
- 数据模式验证
- 样本数据文档记录

### 2. 特征工程阶段
- 特征选择
- 特征重要性分析
- 特征存储集成（可选）

### 3. 训练阶段
- 基线模型（随机方法/规则基础）
- 多个候选模型
- 超参数调优
- 交叉验证

### 4. 评估阶段
- 综合评估指标（准确率、精确率、召回率、F1 分数、AUC）
- 业务指标（延迟、吞吐量）
- 模型对比（与基线模型或之前的版本相比）
- 错误分析

### 5. 可解释性阶段
- 特征重要性分析
- SHAP 分数计算
- LIME 可解释性方法
- 提供带有解释的示例预测结果

### 6. 部署阶段
- 模型打包
- 推理流程搭建
- A/B 测试计划制定
- 监控系统设置

## 与 SpecWeave 工作流程的集成

- **与实验跟踪工具的集成**：
```bash
# Start ML increment
/sw:inc "0042-recommendation-model"

# Automatically integrates experiment tracking
# All MLflow/W&B logs saved to increment folder
```

- **与实时文档系统的集成**：
```bash
# After training best model
/sw:sync-docs update

# Automatically:
# - Updates architecture/ml-models.md
# - Adds ADR for algorithm choice
# - Documents hyperparameters in runbooks
```

- **与 GitHub 的集成**：
```bash
# Create GitHub issue for model retraining
/sw:github:create-issue "Retrain recommendation model with new data"

# Linked to increment 0042
# Issue tracks model performance over time
```

## 最佳实践

- **始终从基线模型开始**：
```python
# Before training complex models, establish baseline
baseline_results = train_baseline_model(
    strategies=["random", "popularity", "rule-based"]
)
# Requirement: New model must beat best baseline by 20%+
```

- **使用交叉验证**：
```python
# Never trust single train/test split
cv_scores = cross_val_score(model, X, y, cv=5)
exp.log_metric("cv_mean", cv_scores.mean())
exp.log_metric("cv_std", cv_scores.std())
```

- **记录所有开发步骤**：
```python
# Hyperparameters, metrics, artifacts, environment
exp.log_params(model.get_params())
exp.log_metrics({"accuracy": acc, "f1": f1})
exp.log_artifact("model.pkl")
exp.log_artifact("requirements.txt")  # Reproducibility
```

- **记录失败原因**：
```python
# Failed experiments are valuable learnings
with track_experiment("exp-006-failed-lstm") as exp:
    # ... training fails ...
    exp.log_note("FAILED: LSTM overfits badly, needs regularization")
    exp.set_status("failed")
# This documents why LSTM wasn't chosen
```

- **进行模型版本管理**：
```python
# Tie model versions to increments
model_version = f"0042-v{iteration}"
mlflow.register_model(
    f"runs:/{run_id}/model",
    f"recommendation-model-{model_version}"
)
```

## 示例

- **示例 1：分类模型开发流程**
```bash
User: "Build a fraud detection model for transactions"

Skill creates increment 0051-fraud-detection with:
- spec.md: Binary classification, 99% precision target
- plan.md: Imbalanced data handling, threshold tuning
- tasks.md: 9 tasks from EDA to deployment
- experiments/: exp-001-baseline, exp-002-xgboost, etc.

Guides through:
1. EDA → identify class imbalance (0.1% fraud)
2. Baseline → random/majority (terrible results)
3. Candidates → XGBoost, LightGBM, Neural Net
4. Threshold tuning → optimize for precision
5. SHAP → explain high-risk predictions
6. Deploy → model + threshold + explainer
```

- **示例 2：回归模型开发流程**
```bash
User: "Predict customer lifetime value"

Skill creates increment 0063-ltv-prediction with:
- spec.md: Regression, RMSE < $50 target
- plan.md: Time-based validation, feature engineering
- tasks.md: Customer cohort analysis, feature importance

Key difference: Regression-specific evaluation (RMSE, MAE, R²)
```

- **示例 3：时间序列预测开发流程**
```bash
User: "Forecast weekly sales for next 12 weeks"

Skill creates increment 0072-sales-forecasting with:
- spec.md: Time series, MAPE < 10% target
- plan.md: Seasonal decomposition, ARIMA vs Prophet
- tasks.md: Stationarity tests, residual analysis

Key difference: Time series validation (no random split)
```

## 支持的框架

该技能支持所有主要的 ML 框架：
- Scikit-Learn
- PyTorch
- TensorFlow/Keras
- XGBoost/LightGBM

## 集成点

- **与 `experiment-tracker` 工具的集成**：
  - 自动检测项目中的 MLflow/W&B 工具
  - 将实验元数据同步到增量文档中

- **与 `model-evaluator` 工具的集成**：
  - 生成全面的评估报告
  - 比较不同实验的模型性能
  - 显示最佳模型及其置信区间

- **与 `feature-engineer` 工具的集成**：
  - 生成特征工程流程文档
  - 记录特征重要性
  - 创建特征存储方案

- **与 `ml-engineer` 代理的集成**：
  - 将复杂的 ML 决策委托给专业代理处理
  - 审查模型架构
  - 根据测试结果提出改进建议

## 技能输出

在运行 `/sw:do` 命令后，您将获得以下输出：
```
.specweave/increments/0042-recommendation-model/
├── spec.md ✅
├── plan.md ✅
├── tasks.md ✅ (all completed)
├── COMPLETION-SUMMARY.md ✅
├── experiments/
│   ├── exp-001-baseline/
│   │   ├── metrics.json
│   │   ├── params.json
│   │   └── logs/
│   ├── exp-002-xgboost/ ✅ BEST
│   │   ├── metrics.json
│   │   ├── params.json
│   │   ├── model.pkl
│   │   └── shap_values.pkl
│   └── comparison.md
├── models/
│   ├── model-v3.pkl (best)
│   └── model-v3.metadata.json
├── data/
│   ├── schema.yaml
│   └── sample.parquet
└── notebooks/
    ├── 01-eda.ipynb
    ├── 02-feature-engineering.ipynb
    └── 03-model-analysis.ipynb
```

## 命令集成

该技能与 SpecWeave 的命令系统紧密集成：
```bash
# Create ML increment
/sw:inc "build recommendation model"
→ Activates ml-pipeline-orchestrator
→ Creates ML-specific increment structure

# Execute ML tasks
/sw:do
→ Guides through data → train → eval workflow
→ Auto-tracks experiments

# Validate ML increment
/sw:validate 0042
→ Checks: experiments logged, model saved, metrics documented
→ Validates: model meets success criteria

# Complete ML increment
/sw:done 0042
→ Generates ML completion summary
→ Syncs model metadata to living docs
```

## 使用建议

- **从简单任务开始**——始终先建立基线模型，再逐步改进
- **记录失败原因**——详细记录哪些方法无效
- **进行数据版本管理**——使用 DVC 或类似工具管理数据版本
- **确保实验的可重复性**——记录开发环境信息（如 `requirements.txt`、`conda env`）
- **实现增量式改进**——每个增量都基于之前的模型进行优化
- **促进团队协作**——实时文档使所有团队成员都能了解决策过程

## 高级应用：多增量 ML 项目

对于复杂的 ML 系统（例如包含多个模型的推荐系统）：
- 每个开发增量都有独立的需求文档、计划和任务
- 基于之前的增量进行开发
- 记录模型之间的交互关系
- 维护系统级别的实时文档记录