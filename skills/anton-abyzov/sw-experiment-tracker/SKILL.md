---
name: experiment-tracker
description: |
  Manages ML experiment tracking with MLflow, Weights & Biases, or SpecWeave's built-in tracking. Activates for "track experiments", "MLflow", "wandb", "experiment logging", "compare experiments", "hyperparameter tracking". Automatically configures tracking tools to log to SpecWeave increment folders, ensuring all experiments are documented and reproducible. Integrates with SpecWeave's living docs for persistent experiment knowledge.
---

# 实验跟踪器

## 概述

该工具将混乱的机器学习（ML）实验转化为有序、可复现的研究过程。每个实验都会被记录下来，打上版本标签，并与 SpecWeave 的版本增量关联起来，从而确保团队知识得到保存，实验结果能够被准确复现。

## 该工具解决的问题

**在没有结构化跟踪机制的情况下**：
- ❌ “我们为模型 v2 使用了哪些超参数？”
- ❌ “为什么选择 XGBoost 而不是 LightGBM？”
- ❌ “无法复现三个月前的实验结果”
- ❌ 团队成员离职后，所有知识都留在了他们的个人笔记本中

**使用实验跟踪机制后**：
- ✅ 所有实验都会被记录下来，包括参数、指标和实验产生的结果文件
- ✅ 决策过程会被详细记录（例如：“选择 XGBoost，因为其精度提高了 5%”）
- ✅ 实验环境、数据版本和代码哈希值都是可复现的
- ✅ 团队知识存储在统一的文档中，而不仅仅是在个人笔记本中

## 工作原理

### 自动配置

当你创建一个 ML 实验版本增量时，该工具会自动检测可用的跟踪工具：

```python
# No configuration needed - automatically detects and configures
from specweave import track_experiment

# Automatically logs to:
# .specweave/increments/0042.../experiments/exp-001/
with track_experiment("baseline-model") as exp:
    model.fit(X_train, y_train)
    exp.log_metric("accuracy", accuracy)
```

### 跟踪后端

**选项 1：SpecWeave 内置**（默认设置，无需额外配置）
```python
from specweave import track_experiment

# Logs to increment folder automatically
with track_experiment("xgboost-v1") as exp:
    exp.log_param("n_estimators", 100)
    exp.log_metric("auc", 0.87)
    exp.save_model(model, "model.pkl")

# Creates:
# .specweave/increments/0042.../experiments/xgboost-v1/
# ├── params.json
# ├── metrics.json
# ├── model.pkl
# └── metadata.yaml
```

**选项 2：MLflow**（如果在项目中检测到该工具）
```python
import mlflow
from specweave import configure_mlflow

# Auto-configures MLflow to log to increment
configure_mlflow(increment="0042")

with mlflow.start_run(run_name="xgboost-v1"):
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("auc", 0.87)
    mlflow.sklearn.log_model(model, "model")

# Still logs to increment folder, just uses MLflow as backend
```

**选项 3：Weights & Biases**（用于权重和偏差的跟踪）
```python
import wandb
from specweave import configure_wandb

# Auto-configures W&B project = increment ID
configure_wandb(increment="0042")

run = wandb.init(name="xgboost-v1")
run.log({"auc": 0.87})
run.log_model("model.pkl")

# W&B dashboard + local logs in increment folder
```

### 实验比较

```python
from specweave import compare_experiments

# Compare all experiments in increment
comparison = compare_experiments(increment="0042")

# Generates:
# .specweave/increments/0042.../experiments/comparison.md
```

**输出结果**：
```markdown
| Experiment         | Accuracy | Precision | Recall | F1   | Training Time |
|--------------------|----------|-----------|--------|------|---------------|
| exp-001-baseline   | 0.65     | 0.60      | 0.55   | 0.57 | 2s            |
| exp-002-xgboost    | 0.87     | 0.85      | 0.83   | 0.84 | 45s           |
| exp-003-lightgbm   | 0.86     | 0.84      | 0.82   | 0.83 | 32s           |
| exp-004-neural-net | 0.85     | 0.83      | 0.81   | 0.82 | 320s          |

**Best Model**: exp-002-xgboost
- Highest accuracy (0.87)
- Good precision/recall balance
- Reasonable training time (45s)
- Selected for deployment
```

### 集成到实时文档中

实验完成后，相关内容会自动更新到实时文档中：

```bash
/sw:sync-docs update
```

## 适用场景

在以下情况下应使用该工具：
- 需要系统地跟踪 ML 实验
- 客观地比较多个模型
- 为团队记录实验决策过程
- 精确地复现过去的实验结果
- 在不同实验版本之间维护实验历史记录

## 主要功能

### 1. 自动记录实验过程
```python
# Logs everything automatically
from specweave import AutoTracker

tracker = AutoTracker(increment="0042")

# Just wrap your training code
@tracker.track(name="xgboost-auto")
def train_model():
    model = XGBClassifier(**params)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    return model, score

# Automatically logs: params, metrics, model, environment, git hash
model, score = train_model()
```

### 2. 超参数跟踪
```python
from specweave import track_hyperparameters

params_grid = {
    "n_estimators": [100, 200, 500],
    "max_depth": [3, 6, 9],
    "learning_rate": [0.01, 0.1, 0.3]
}

# Tracks all parameter combinations
results = track_hyperparameters(
    model=XGBClassifier,
    param_grid=params_grid,
    X_train=X_train,
    y_train=y_train,
    increment="0042"
)

# Generates parameter importance analysis
```

### 3. 交叉验证跟踪
```python
from specweave import track_cross_validation

# Tracks each fold separately
cv_results = track_cross_validation(
    model=model,
    X=X,
    y=y,
    cv=5,
    increment="0042"
)

# Logs: mean, std, per-fold scores, fold distribution
```

### 4. 实验结果文件管理
```python
from specweave import track_artifacts

with track_experiment("xgboost-v1") as exp:
    # Training artifacts
    exp.save_artifact("preprocessor.pkl", preprocessor)
    exp.save_artifact("model.pkl", model)
    
    # Evaluation artifacts
    exp.save_artifact("confusion_matrix.png", cm_plot)
    exp.save_artifact("roc_curve.png", roc_plot)
    
    # Data artifacts
    exp.save_artifact("feature_importance.csv", importance_df)
    
    # Environment artifacts
    exp.save_artifact("requirements.txt", requirements)
    exp.save_artifact("conda_env.yaml", conda_env)
```

### 5. 实验元数据管理
```python
from specweave import ExperimentMetadata

metadata = ExperimentMetadata(
    name="xgboost-v3",
    description="XGBoost with feature engineering v2",
    tags=["production-candidate", "feature-eng-v2"],
    git_commit="a3b8c9d",
    data_version="v2024-01",
    author="[email protected]"
)

with track_experiment(metadata) as exp:
    # ... training ...
    pass
```

## 最佳实践

- **为实验起明确的名称**  
```python
# ❌ Bad: Generic names
with track_experiment("exp1"):
    ...

# ✅ Good: Descriptive names
with track_experiment("xgboost-tuned-depth6-lr0.1"):
    ...
```

- **记录所有相关数据**  
```python
# Log more than you think you need
exp.log_param("random_seed", 42)
exp.log_param("data_version", "2024-01")
exp.log_param("python_version", sys.version)
exp.log_param("sklearn_version", sklearn.__version__)

# Future you will thank present you
```

- **详细记录实验失败的原因**  
```python
try:
    with track_experiment("neural-net-attempt") as exp:
        model.fit(X_train, y_train)
except Exception as e:
    exp.log_note(f"FAILED: {str(e)}")
    exp.log_note("Reason: Out of memory, need smaller batch size")
    exp.set_status("failed")
    
# Failure documentation prevents repeating mistakes
```

- **使用实验系列进行管理**  
```python
# Related experiments in series
experiments = [
    "xgboost-baseline",
    "xgboost-tuned-v1",
    "xgboost-tuned-v2",
    "xgboost-tuned-v3-final"
]

# Track progression and improvements
```

- **关联数据版本**  
```python
with track_experiment("xgboost-v1") as exp:
    exp.log_param("data_commit", "dvc:a3b8c9d")
    exp.log_param("data_url", "s3://bucket/data/v2024-01")
    
# Enables exact reproduction
```

## 与其他工具的集成

- **与 SpecWeave 的集成**：
  - 在创建实验版本增量时自动进行集成
  - 与实时文档系统同步实验信息
  - 与 GitHub 集成，便于团队协作

## 示例

- **示例 1：基线实验**  
```python
from specweave import track_experiment

baselines = ["random", "majority", "stratified"]

for strategy in baselines:
    with track_experiment(f"baseline-{strategy}") as exp:
        model = DummyClassifier(strategy=strategy)
        model.fit(X_train, y_train)
        
        accuracy = model.score(X_test, y_test)
        exp.log_metric("accuracy", accuracy)
        exp.log_note(f"Baseline: {strategy}")

# Generates baseline comparison report
```

- **示例 2：超参数网格搜索**  
```python
from sklearn.model_selection import GridSearchCV
from specweave import track_grid_search

param_grid = {
    "n_estimators": [100, 200, 500],
    "max_depth": [3, 6, 9]
}

# Automatically logs all combinations
best_model, results = track_grid_search(
    XGBClassifier(),
    param_grid,
    X_train,
    y_train,
    increment="0042"
)

# Creates visualization of parameter importance
```

- **示例 3：模型比较**  
```python
from specweave import compare_models

models = {
    "xgboost": XGBClassifier(),
    "lightgbm": LGBMClassifier(),
    "random-forest": RandomForestClassifier()
}

# Trains and compares all models
comparison = compare_models(
    models,
    X_train,
    y_train,
    X_test,
    y_test,
    increment="0042"
)

# Generates markdown comparison table
```

## 兼容性

- **与 MLflow 的兼容性**  
```python
# Option 1: Pure MLflow (auto-configured)
import mlflow
mlflow.set_tracking_uri(".specweave/increments/0042.../experiments")

# Option 2: SpecWeave wrapper (recommended)
from specweave import mlflow as sw_mlflow
with sw_mlflow.start_run("xgboost"):
    # Logs to both MLflow and increment docs
    pass
```

- **与 Weights & Biases 的兼容性**  
```python
# Option 1: Pure wandb
import wandb
wandb.init(project="0042-recommendation-model")

# Option 2: SpecWeave wrapper (recommended)
from specweave import wandb as sw_wandb
run = sw_wandb.init(increment="0042", name="xgboost")
# Syncs to increment folder + W&B dashboard
```

- **与 TensorBoard 的兼容性**  
```python
from specweave import TensorBoardCallback

# Keras callback
model.fit(
    X_train,
    y_train,
    callbacks=[
        TensorBoardCallback(
            increment="0042",
            log_dir=".specweave/increments/0042.../tensorboard"
        )
    ]
)
```

## 命令行操作

```bash
# List all experiments in increment
/ml:list-experiments 0042

# Compare experiments
/ml:compare-experiments 0042

# Load experiment details
/ml:show-experiment exp-003-xgboost

# Export experiment data
/ml:export-experiments 0042 --format csv
```

## 使用建议：

- **尽早开始跟踪**：从第一个实验开始就进行记录，而不要等到失败了 20 次后再开始。
- **为生产环境中的模型添加标签**：使用 `exp.add_tag("production")` 标记已部署的模型。
- **对所有内容进行版本控制**：包括数据、代码、实验环境和依赖项。
- **详细记录决策过程**：解释为什么选择某个模型而非另一个模型（而不仅仅是指标）。
- **定期清理旧实验**：将超过 6 个月的实验归档。

## 高级用法：多阶段实验

对于包含多个阶段的复杂实验流程，可以使用以下方法：

```python
from specweave import ExperimentPipeline

pipeline = ExperimentPipeline("recommendation-full-pipeline")

# Stage 1: Data preprocessing
with pipeline.stage("preprocessing") as stage:
    stage.log_metric("rows_before", len(df))
    df_clean = preprocess(df)
    stage.log_metric("rows_after", len(df_clean))

# Stage 2: Feature engineering
with pipeline.stage("features") as stage:
    features = engineer_features(df_clean)
    stage.log_metric("num_features", features.shape[1])

# Stage 3: Model training
with pipeline.stage("training") as stage:
    model = train_model(features)
    stage.log_metric("accuracy", accuracy)

# Logs entire pipeline with stage dependencies
```

## 集成点：

- **ml-pipeline-orchestrator**：在实验流程执行过程中自动跟踪实验。
- **model-evaluator**：利用实验数据来评估模型性能。
- **ml-engineer agent**：审查实验结果并提出改进建议。
- **实时文档系统**：将实验结果同步到项目架构文档中。

该工具确保 ML 实验过程不会丢失，结果始终可复现，并且有完整的文档记录。