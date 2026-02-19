---
name: mlops-observability-cn
version: 1.0.0
description: 全栈可观测性：可复现性、追踪能力、监控功能以及警报机制
license: MIT
---
# MLOps 可观测性 👁️

我们的系统属于“透明箱”类型：可复现、可追踪、可监控。

## 主要功能

### 1. MLflow 跟踪 📊

完整的跟踪设置：

```bash
cp references/mlflow-tracking.py ../your-project/src/tracking.py
```

跟踪内容包括：
- 配置参数（Config）
- 指标（准确率、损失值）
- 模型（使用 sklearn 或 pytorch 构建）
- 数据集（版本信息）
- Git 提交记录（确保可复现性）

### 2. 偏差检测 📉

使用 Evidently 工具进行偏差检测：

```python
from evidently import Report
from evidently.metrics import DataDriftTable

report = Report(metrics=[DataDriftTable()])
report.run(reference_data=train, current_data=prod)
```

### 3. 可解释性（SHAP） 🔍

利用 SHAP 工具提供模型可解释性：

```python
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)
shap.summary_plot(shap_values, X)
```

## 快速入门

```bash
# Copy tracking code
cp references/mlflow-tracking.py ./src/

# Add to training script:
# from tracking import setup_tracking, log_training_run
```

## 可复现性

确保模型结果的可复现性：

```python
# Set all seeds
import random, numpy as np, torch
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)

# Track git commit
import git
commit = git.Repo().head.commit.hexsha
mlflow.log_param("git_commit", commit)
```

## 监控检查清单

- [ ] 随机种子已设置固定
- [ ] 已启用 MLflow 跟踪功能
- [ ] 系统指标已记录
- [ ] 偏差检测设置已完成
- [ ] 模型可解释性结果已保存
- [ ] 警报机制已配置

## 警报机制

- **本地环境**：使用 `plyer` 发送通知
- **生产环境**：通过 PagerDuty（严重情况）/ Slack（警告情况）发送通知

## 作者

本文档源自 [MLOps 编程课程](https://github.com/MLOps-Courses/mlops-coding-skills)

## 更新记录

### v1.0.0 (2026-02-18)
- 首次转换为 OpenClaw 格式
- 添加了 MLflow 跟踪相关代码