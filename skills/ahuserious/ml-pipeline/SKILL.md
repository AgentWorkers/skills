---
name: ml-pipeline
description: 完整的机器学习交易流程：包括特征工程、自动机器学习（AutoML）、深度学习以及金融强化学习（RL）。该流程可用于自动化参数搜索、特征生成、模型训练以及防止数据泄露的验证。
version: "2.0.0"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
metadata:
  consolidates:
    - ml-feature-engineering
    - deep-learning-optimizer-5
    - pytorch-lightning-2
    - scikit-learn-ml-framework
    - automl-pipeline-builder-2
    - ml-feature-engineering-helper
    - ml-fundamentals
    - machine-learning-feature-engineering-toolkit
---
# 机器学习管道

这是一个用于量化交易研究系统中整个机器学习（ML）管道的统一技能。它将之前的八项技能整合为一个权威的参考指南，涵盖了整个生命周期：数据验证、特征创建与选择、特征转换、防泄漏检查、管道自动化、深度学习优化以及模型部署。

---

## 1. 适用场景

在以下情况下启用此技能：

- 为基于机器学习的策略创建、选择或转换特征。
- 审计现有的特征管道，以检测数据泄漏或过拟合风险。
- 自动化端到端的机器学习管道（从数据准备到模型导出）。
- 评估特征的重要性、特征缩放、特征编码或特征之间的交互效应。
- 将特征与特征存储系统（如Feast、Tecton或自定义的Parquet存储系统）集成。
- 在特征工程决策的背景下解释核心的机器学习概念（偏差-方差、交叉验证、正则化）。

---

## 2. 需要收集的输入信息

在开始工作之前，请收集或确认以下信息：

| 输入 | 详细信息 |
|-------|---------|
| **目标** | 目标指标（夏普比率、准确率、均方根误差等）、约束条件、时间范围。 |
| **数据** | 交易品种/工具、时间框架、条形图类型、采样频率、数据来源。 |
| **泄漏风险** | 特定时间点的风险、生存偏差、标签或特征中的前瞻性问题。 |
| **计算预算** | CPU/GPU资源限制、自动机器学习（AutoML）搜索的运行时间预算。 |
| **延迟** | 在线推理与离线推理的需求、可接受的预测延迟。 |
| **可解释性** | 是否需要可解释的特征或模型以满足监管或研究要求。 |
| **部署目标** | 模型将运行的环境（笔记本、回测平台、实时引擎）。 |

---

## 3. 特征创建模式

### 3.1 数值特征

- **交互项**：`价格 * 体积`、`最高价 / 最低价`、`收盘价 - 开盘价`。
- **滚动统计量**：在可配置的时间窗口内的平均值、标准差、偏度、峰度。
- **多项式/对数转换**：`log(体积 + 1)`、`spread^2`。
- **分箱/离散化**：等宽分箱、基于分位数的分箱或基于领域的分箱。

### 3.2 分类特征

- **独热编码**：用于低类别数量的分类变量（如行业、交易所）。
- **目标编码**：计算每个类别的平均值，并进行平滑处理（注意防止泄漏——仅在使用内部平均值时使用）。
- **顺序编码**：当类别具有自然顺序时使用（例如信用评级）。

### 3.3 时间序列特征

- **滞后特征**：`return_{t-1}`、`return_{t-5}` 等。
- **日历特征**：星期几、月份、季度、期权到期标志。
- **滚动z分数**：`(x - rolling_mean) / rolling_std` 用于检测数据是否平稳。
- **分数差分**：在保持数据平稳性的同时节省内存（Lopez de Prado方法）。

### 3.4 特征选择技术

- **过滤方法**：互信息、方差阈值、相关性剪枝。
- **包装方法**：递归特征消除（RFE）、向前/向后选择。
- **嵌入方法**：L1正则化、基于树的特征重要性、SHAP值。
- **排列重要性**：不依赖于具体模型的方法；在样本外预测上进行评估。

---

## 4. 防泄漏检查

数据泄漏是导致回测结果失真的最常见原因。在每个管道阶段都应进行以下检查：

### 4.1 标签泄漏

- 标签必须根据特征的时间戳从**未来**的回报计算得出。确保标签窗口不与特征窗口重叠。
- 如果标签跨越多个时间点，请使用数据清洗和禁售机制。

### 4.2 特征泄漏

- 在预测时间 `t` 时，任何特征都不能使用来自时间 `t+1` 或之后的信息。
- 滚动统计量必须使用**封闭的**左窗口：`df['feat'].rolling(20).mean().shift(1)`。
- 目标编码的分类特征必须仅在**训练集**上计算。

### 4.3 交叉验证泄漏

- 对于时间序列数据，使用**清洗后的k折交叉验证**（purged k-fold）或**向前滚动交叉验证**（walk-forward CV）。切勿在有序数据上使用随机k折交叉验证。
- 在训练集和测试集之间插入**禁售间隔**，以防止自相关性导致的误差传递。

### 4.4 生存偏差与选择偏差

- 确保时间 `t` 时的交易品种集合反映了当时实际可交易的品种（移除已退市或暂停交易的品种）。
- 如有需要，从实时数据库中补充数据。

### 4.5 验证检查清单

在每次回测之前运行以下代码：

```text
[ ] Labels computed strictly from future returns (no overlap with features)
[ ] All rolling features shifted by at least 1 bar
[ ] Target encoding uses in-fold means only
[ ] Walk-forward or purged CV used (no random shuffle on time-series)
[ ] Embargo gap >= max(label_horizon, autocorrelation_lag)
[ ] Universe is point-in-time (no survivorship bias)
[ ] No global scaling fitted on full dataset (fit on train, transform test)
```

---

## 5. 管道自动化（自动机器学习，AutoML）

### 5.1 先决条件

- 搭配一个或多个自动机器学习库的Python环境：Auto-sklearn、TPOT、H2O AutoML、PyCaret、Optuna或自定义的Optuna管道。
- 训练数据以CSV/Parquet/数据库格式存在。
- 确定了问题类型：分类问题、回归问题或时间序列预测问题。

### 5.2 管道步骤

| 步骤 | 操作 |
|------|--------|
| **1. 定义需求** | 问题类型、评估指标、时间/资源预算、可解释性要求。 |
| **2. 数据基础设施** | 加载数据、进行数据质量评估、划分训练集/验证集/测试集、定义特征转换规则。 |
| **3. 配置自动机器学习** | 选择框架、定义算法搜索空间、设置预处理步骤、选择调优策略（贝叶斯、随机搜索、Hyperband）。 |
| **4. 执行训练** | 运行自动特征工程、模型选择、超参数优化、交叉验证。 |
| **5. 分析与导出** | 比较模型、提取最佳配置、分析特征重要性、生成可视化结果，并导出用于部署的代码。 |

### 5.3 管道配置模板

```python
pipeline_config = {
    "task_type": "classification",        # or "regression", "time_series"
    "time_budget_seconds": 3600,
    "algorithms": ["rf", "xgboost", "catboost", "lightgbm"],
    "preprocessing": ["scaling", "encoding", "imputation"],
    "tuning_strategy": "bayesian",        # or "random", "hyperband"
    "cv_folds": 5,
    "cv_type": "purged_kfold",            # or "walk_forward"
    "embargo_bars": 10,
    "early_stopping_rounds": 50,
    "metric": "sharpe_ratio",             # domain-specific metric
}
```

### 5.4 输出结果

- `automl_config.py` -- 管道配置文件。
- `best_model.pkl` / `.joblib` / `.onnx` -- 序列化的模型文件。
- `feature_pipeline.pkl` -- 包含预处理规则和特征转换的文件。
- `evaluation_report.json` -- 包含指标、混淆矩阵/残差、特征排名的文件。
- `deployment/` -- 包含预测API代码、输入验证规则和需求说明的文件。

---

## 6. 核心机器学习基础（特征工程背景）

### 6.1 偏差-方差权衡

- 更多的特征可以提高模型的容量（降低偏差），但会增加过拟合的风险（增加方差）。
- 可以通过正则化（L1/L2）、特征选择或降维来控制这种风险。

### 6.2 评估策略

- **向前滚动验证**：时间序列策略的黄金标准。将固定宽度的训练窗口向前滚动；在下一个样本外周期进行测试。
- **蒙特卡洛排列测试**：随机打乱标签并重新评估，以估计观察到的性能是否偶然发生。
- **组合清洗交叉验证（CPCV）**：生成多个训练/测试组合，并进行清洗，以获得更稳健的性能估计。

### 6.3 特征缩放

- 仅在**训练集**上拟合缩放器（StandardScaler、MinMaxScaler、RobustScaler）。
- 将相同的缩放器应用于验证集和测试集。
- 对于金融数据，通常更倾向于使用RobustScaler，因为金融数据往往具有重尾特性。

### 6.4 处理缺失数据

- 对价格数据先进行前向填充，然后再进行后向填充（注意填充过程中可能产生的泄漏问题）。
- 可以使用指示缺失值的列来提供额外信息。
- 基于树的模型可以直接处理缺失值；线性模型则无法处理。

---

## 7. 工作流程

对于任何特征工程任务，请按照以下顺序操作：

1. 用可衡量的术语（指标、约束条件、截止日期）重新描述任务。
2. 列出所需的成果：数据集、特征定义、配置文件、脚本、报告。
3. 提出一种默认方法以及1-2种带有权衡的替代方案。
4. 实现包含防泄漏检查的功能管道。
5. 使用向前滚动交叉验证、蒙特卡洛方法以及上述的泄漏检查进行验证。
6. 提供准备好部署的代码、文档以及运行命令。

---

## 8. 深度学习优化

### 8.1 优化器选择

| 优化器 | 适用场景 | 学习率 |
|-----------|----------|---------------|
| Adam | 大多数情况 | 1e-3 到 1e-4 |
| AdamW | 变换器模型、权重衰减 | 1e-4 到 1e-5 |
| SGD + Momentum | 大批量数据、微调 | 1e-2 到 1e-3 |
| RAdam | 需要快速收敛的情况 | 1e-3 |

### 8.2 学习率调度

- **OneCycleLR**：适用于短期训练，收敛速度快。
- **CosineAnnealing**：平滑衰减，泛化能力强。
- **ReduceOnPlateau**：在验证损失趋于平稳时使用。
- **Warmup + Decay**：适用于变换器模型。

### 8.3 正则化技术

- **Dropout**：全连接层使用0.1-0.5。
- **L2（权重衰减）**：1e-4 到 1e-2。
- **批量归一化**：有助于稳定训练过程。
- **提前停止**：在验证损失趋于平稳时使用。

### 8.4 PyTorch Lightning集成

```python
import pytorch_lightning as pl

class TradingModel(pl.LightningModule):
    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.parameters(), lr=1e-4)
        scheduler = torch.optim.lr_scheduler.OneCycleLR(
            optimizer, max_lr=1e-3, total_steps=self.trainer.estimated_stepping_batches
        )
        return [optimizer], [scheduler]
```

### 8.5 金融强化学习

- **状态**：市场特征、投资组合状态、持仓情况。
- **动作**：买入/卖出/持有、持仓规模调整。
- **奖励**：经过风险调整的回报（如夏普比率、Sortino比率）。
- **框架**：Stable-Baselines3、RLlib、FinRL

---

## 9. 错误处理

| 问题 | 原因 | 解决方法 |
|---------|-------|-----|
| 自动机器学习搜索未找到合适的模型 | 时间预算不足或特征质量不佳 | 增加预算、改进特征设计、扩展算法搜索范围。 |
- 训练过程中内存不足 | 数据集过大，超出可用内存 | 下采样数据、采用增量学习方法、简化特征工程。 |
- 模型准确率低于阈值 | 信号较弱或过拟合 | 收集更多数据、添加领域相关的特征、使用正则化方法、调整评估指标。 |
- 特征转换产生NaN/Inf值 | 分母为零的情况 | 添加防护措施：`np.where(denom != 0, ...)`, `np.log1p(np.abs(x))`。 |
- 优化器无法收敛 | 参数范围设置不当 | 调整搜索范围、增加迭代次数、排除不稳定的算法。 |

---

## 10. 集成脚本

所有相关脚本都位于`scripts/`目录下。

| 脚本 | 用途 |
|--------|---------|
| `data_validation.py` | 在执行管道之前验证输入数据的质量。 |
| `model_evaluation.py` | 评估训练模型的性能并生成报告。 |
| `pipeline_deployment.py` | 将训练好的管道部署到目标环境，并提供回滚支持。 |
| `feature_engineering_pipeline.py | 实现端到端的特征工程流程：数据加载、清洗、转换、特征选择、模型训练。 |
| `feature_importance_analyzer.py | 分析特征的重要性（使用排列法、SHAP方法、基于树的方法）。 |
| `data_visualizer.py | 可视化特征分布及其与目标变量的关系。 |
| `feature_store_integration.py | 与特征存储系统（Feast、Tecton）集成，以实现在线/离线服务。 |

---

## 11. 资源

### 框架

- **scikit-learn** -- 用于数据预处理和特征选择。
- **Auto-sklearn / TPOT / H2O AutoML / PyCaret** -- 用于自动化管道搜索。
- **Optuna** -- 用于灵活的参数优化。
- **SHAP** -- 用于计算模型特征的重要性。
- **Feast / Tecton** -- 用于管理特征存储。
- **PyTorch Lightning** -- https://lightning.ai/docs/pytorch/stable/
- **Stable-Baselines3** -- https://stable-baselines3.readthedocs.io/
- **FinRL** -- https://github.com/AI4Finance-Foundation/FinRL

### 参考文献

- Lopez de Prado, *Advances in Financial Machine Learning* (2018) -- 提出了清洗后的交叉验证（purged CV）和分数差分（fractional differentiation）方法以及元标记（meta-labelling）技术。
- Hastie, Tibshirani & Friedman, *The Elements of Statistical Learning* -- 讨论了偏差-方差、正则化和模型选择相关内容。
- scikit-learn用户指南：提供了特征提取、数据预处理和模型选择的详细指导。

### 最佳实践

- 在运行自动机器学习之前，始终先建立一个简单的基线模型。
- 在自动化处理与领域知识之间取得平衡——盲目搜索很少能胜过基于领域知识的决策。
- 监控资源消耗情况，并设置合理的超时时间。
- 使用真实的样本外数据集进行验证，而不仅仅是交叉验证。
- 记录每个管道决策，以确保结果的可重复性。