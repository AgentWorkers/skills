---
name: automl-optimizer
description: |
  Automated machine learning with hyperparameter optimization using Optuna, Hyperopt, or AutoML libraries. Activates for "automl", "hyperparameter tuning", "optimize hyperparameters", "auto tune model", "neural architecture search", "automated ml". Systematically explores model and hyperparameter spaces, tracks all experiments, and finds optimal configurations with minimal manual intervention.
---

# AutoML 优化器

## 概述

AutoML 优化器能够自动化繁琐的超参数调整和模型选择过程。无需手动尝试各种配置，只需定义一个搜索空间，让 AutoML 通过智能的探索方法找到最优配置。

## 为什么选择 AutoML？

**手动调优的问题**：
- 耗时（需要花费数小时甚至数天的时间进行反复试验）
- 主观性强（依赖于直觉）
- 不全面（无法尝试所有组合）
- 不可重复（难以记录搜索过程）

**AutoML 的优势**：
- ✅ 系统性地探索搜索空间
- ✅ 智能采样（基于贝叶斯优化算法）
- ✅ 自动跟踪所有实验结果
- ✅ 更快地找到最优配置
- ✅ 可重复（搜索过程有详细记录）

## AutoML 策略

### 策略 1：超参数优化（使用 Optuna）

```python
from specweave import OptunaOptimizer

# Define search space
def objective(trial):
    # Suggest hyperparameters
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0)
    }
    
    # Train model
    model = XGBClassifier(**params)
    
    # Cross-validation score
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
    
    return scores.mean()

# Run optimization
optimizer = OptunaOptimizer(
    objective=objective,
    n_trials=100,
    direction='maximize',
    increment="0042"
)

best_params = optimizer.optimize()

# Creates:
# - .specweave/increments/0042.../experiments/optuna-study/
#   ├── study.db (Optuna database)
#   ├── optimization_history.png
#   ├── param_importances.png
#   ├── parallel_coordinate.png
#   └── best_params.json
```

**优化报告**：
```markdown
# Optuna Optimization Report

## Search Space
- n_estimators: [100, 1000]
- max_depth: [3, 10]
- learning_rate: [0.01, 0.3] (log scale)
- subsample: [0.5, 1.0]
- colsample_bytree: [0.5, 1.0]

## Trials: 100
- Completed: 98
- Pruned: 2 (early stopping)
- Failed: 0

## Best Trial (#47)
- ROC AUC: 0.892 ± 0.012
- Parameters:
  - n_estimators: 673
  - max_depth: 6
  - learning_rate: 0.094
  - subsample: 0.78
  - colsample_bytree: 0.91

## Parameter Importance
1. learning_rate (0.42) - Most important
2. n_estimators (0.28)
3. max_depth (0.18)
4. colsample_bytree (0.08)
5. subsample (0.04) - Least important

## Improvement over Default
- Default params: ROC AUC = 0.856
- Optimized params: ROC AUC = 0.892
- Improvement: +4.2%
```

### 策略 2：算法选择 + 调优

```python
from specweave import AutoMLPipeline

# Define candidate algorithms with search spaces
pipeline = AutoMLPipeline(increment="0042")

# Add candidates
pipeline.add_candidate(
    name="xgboost",
    model=XGBClassifier,
    search_space={
        'n_estimators': (100, 1000),
        'max_depth': (3, 10),
        'learning_rate': (0.01, 0.3)
    }
)

pipeline.add_candidate(
    name="lightgbm",
    model=LGBMClassifier,
    search_space={
        'n_estimators': (100, 1000),
        'max_depth': (3, 10),
        'learning_rate': (0.01, 0.3)
    }
)

pipeline.add_candidate(
    name="random_forest",
    model=RandomForestClassifier,
    search_space={
        'n_estimators': (100, 500),
        'max_depth': (3, 20),
        'min_samples_split': (2, 20)
    }
)

pipeline.add_candidate(
    name="logistic_regression",
    model=LogisticRegression,
    search_space={
        'C': (0.001, 100),
        'penalty': ['l1', 'l2']
    }
)

# Run AutoML (tries all algorithms + hyperparameters)
results = pipeline.fit(
    X_train, y_train,
    n_trials_per_model=50,
    cv_folds=5,
    metric='roc_auc'
)

# Best model automatically selected
best_model = pipeline.best_model_
best_params = pipeline.best_params_
```

**AutoML 的比较**：
```markdown
| Model               | Trials | Best Score | Mean Score | Std   | Best Params                          |
|---------------------|--------|------------|------------|-------|--------------------------------------|
| xgboost             | 50     | 0.892      | 0.876      | 0.012 | n_est=673, depth=6, lr=0.094         |
| lightgbm            | 50     | 0.889      | 0.873      | 0.011 | n_est=542, depth=7, lr=0.082         |
| random_forest       | 50     | 0.871      | 0.858      | 0.015 | n_est=384, depth=12, min_split=5     |
| logistic_regression | 50     | 0.845      | 0.840      | 0.008 | C=1.234, penalty=l2                  |

**Winner: XGBoost** (ROC AUC = 0.892)
```

### 策略 3：神经网络架构搜索（NAS）

```python
from specweave import NeuralArchitectureSearch

# For deep learning
nas = NeuralArchitectureSearch(increment="0042")

# Define search space
search_space = {
    'num_layers': (2, 5),
    'layer_sizes': (32, 512),
    'activation': ['relu', 'tanh', 'elu'],
    'dropout': (0.0, 0.5),
    'optimizer': ['adam', 'sgd', 'rmsprop'],
    'learning_rate': (0.0001, 0.01)
}

# Search for best architecture
best_architecture = nas.search(
    X_train, y_train,
    search_space=search_space,
    n_trials=100,
    max_epochs=50
)

# Creates: Best neural network architecture
```

## AutoML 框架集成

### 推荐使用 Optuna

```python
import optuna
from specweave import configure_optuna

# Auto-configures Optuna to log to increment
configure_optuna(increment="0042")

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
    }
    
    model = XGBClassifier(**params)
    score = cross_val_score(model, X, y, cv=5).mean()
    return score

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

# Automatically logged to increment folder
```

### Auto-sklearn

```python
from specweave import AutoSklearnOptimizer

# Automated model selection + feature engineering
optimizer = AutoSklearnOptimizer(
    time_left_for_this_task=3600,  # 1 hour
    increment="0042"
)

optimizer.fit(X_train, y_train)

# Auto-sklearn tries:
# - Multiple algorithms
# - Feature preprocessing combinations
# - Ensemble methods
# Returns best pipeline
```

### H2O AutoML

```python
from specweave import H2OAutoMLOptimizer

optimizer = H2OAutoMLOptimizer(
    max_runtime_secs=3600,  # 1 hour
    max_models=50,
    increment="0042"
)

optimizer.fit(X_train, y_train)

# H2O tries many algorithms in parallel
# Returns leaderboard + best model
```

## 最佳实践

### 1. 从默认基线模型开始

```python
# Always compare AutoML to default hyperparameters
baseline_model = XGBClassifier()  # Default params
baseline_score = cross_val_score(baseline_model, X, y, cv=5).mean()

# Then optimize
optimizer = OptunaOptimizer(objective, n_trials=100)
optimized_params = optimizer.optimize()

improvement = (optimized_score - baseline_score) / baseline_score * 100
print(f"Improvement: {improvement:.1f}%")

# Only use optimized if significant improvement (>2-3%)
```

### 2. 使用交叉验证

```python
# ❌ Wrong: Single train/test split
score = model.score(X_test, y_test)

# ✅ Correct: Cross-validation
scores = cross_val_score(model, X_train, y_train, cv=5)
score = scores.mean()

# Prevents overfitting to specific train/test split
```

### 3. 设置合理的搜索预算

```python
# Quick exploration (development)
optimizer.optimize(n_trials=20)  # ~5-10 minutes

# Moderate search (iteration)
optimizer.optimize(n_trials=100)  # ~30-60 minutes

# Thorough search (final model)
optimizer.optimize(n_trials=500)  # ~2-4 hours

# Don't overdo it: diminishing returns after ~100-200 trials
```

### 4. 剔除不具前景的试验结果

```python
# Optuna can stop bad trials early
study = optuna.create_study(
    direction='maximize',
    pruner=optuna.pruners.MedianPruner()
)

# If trial is performing worse than median at epoch N, stop it
# Saves time by not fully training bad models
```

### 5. 记录搜索空间的设计理由

```python
# Document why you chose specific ranges
search_space = {
    # XGBoost recommends max_depth 3-10 for most tasks
    'max_depth': (3, 10),
    
    # Learning rate: 0.01-0.3 covers slow to fast learning
    # Log scale to spend more trials on smaller values
    'learning_rate': (0.01, 0.3, 'log'),
    
    # n_estimators: Balance accuracy vs training time
    'n_estimators': (100, 1000)
}
```

## 与 SpecWeave 的集成

### 自动实验跟踪

```python
# All AutoML trials logged automatically
optimizer = OptunaOptimizer(objective, increment="0042")
optimizer.optimize(n_trials=100)

# Creates:
# .specweave/increments/0042.../experiments/
# ├── optuna-trial-001/
# ├── optuna-trial-002/
# ├── ...
# ├── optuna-trial-100/
# └── optuna-summary.md
```

### 与动态文档系统的集成

```bash
/sw:sync-docs update
```

## 更新示例：

```python
{
    'n_estimators': 673,
    'max_depth': 6,
    'learning_rate': 0.094,
    'subsample': 0.78,
    'colsample_bytree': 0.91
}
```

### Recommendation
XGBoost with optimized hyperparameters for production deployment.
```

## 命令行操作

```bash
# Run AutoML optimization
/ml:optimize 0042 --trials 100

# Compare algorithms
/ml:compare-algorithms 0042

# Show optimization history
/ml:optimization-report 0042
```

## 常见模式

### 模式 1：从粗略到精细的优化过程

```python
# Step 1: Coarse search (wide ranges, few trials)
coarse_space = {
    'n_estimators': (100, 1000, 'int'),
    'max_depth': (3, 10, 'int'),
    'learning_rate': (0.01, 0.3, 'log')
}
coarse_results = optimizer.optimize(coarse_space, n_trials=50)

# Step 2: Fine search (narrow ranges around best)
best_params = coarse_results['best_params']
fine_space = {
    'n_estimators': (best_params['n_estimators'] - 100, 
                     best_params['n_estimators'] + 100),
    'max_depth': (max(3, best_params['max_depth'] - 1),
                  min(10, best_params['max_depth'] + 1)),
    'learning_rate': (best_params['learning_rate'] * 0.5,
                      best_params['learning_rate'] * 1.5, 'log')
}
fine_results = optimizer.optimize(fine_space, n_trials=50)
```

### 模式 2：多目标优化

```python
# Optimize for multiple objectives (accuracy + speed)
def multi_objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
    }
    
    model = XGBClassifier(**params)
    
    # Objective 1: Accuracy
    accuracy = cross_val_score(model, X, y, cv=5).mean()
    
    # Objective 2: Training time
    start = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start
    
    return accuracy, -training_time  # Maximize accuracy, minimize time

# Optuna will find Pareto-optimal solutions
study = optuna.create_study(directions=['maximize', 'minimize'])
study.optimize(multi_objective, n_trials=100)
```

## 总结

AutoML 通过以下方式加速机器学习模型的开发：
- ✅ 自动化繁琐的超参数调整过程
- ✅ 系统地探索搜索空间
- ✅ 更快地找到最优配置
- ✅ 自动跟踪所有实验结果
- ✅ 详细记录优化过程

无需花费大量时间进行手动调优——让 AutoML 在几小时内完成这项工作。