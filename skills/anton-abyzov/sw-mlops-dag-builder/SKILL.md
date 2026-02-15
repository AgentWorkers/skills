---
name: mlops-dag-builder
description: 使用 Airflow、Dagster、Kubeflow 或 Prefect 设计基于有向无环图（DAG）的机器学习运营（MLOps）管道架构。这些工具支持有向无环图的编排、工作流自动化以及管道设计模式，并可用于机器学习的持续集成（CI）和持续部署（CD）流程。此类架构适用于跨平台的机器学习运营基础设施，但不适用于 SpecWeave 的增量式机器学习解决方案（在这种情况下，请使用 ml-pipeline-orchestrator）。
---

# MLOps DAG构建器

使用生产级编排工具设计和实现基于DAG（有向无环图）的机器学习（ML）管道架构。

## 概述

本技能提供了使用DAG编排器（如Airflow、Dagster、Kubeflow、Prefect）构建**与平台无关的MLOps（机器学习运维）管道**的指导。它侧重于工作流架构的设计，而非SpecWeave的集成。

**何时使用本技能，而非ml-pipeline-orchestrator：**
- **使用本技能**：适用于一般的MLOps架构、Airflow/Dagster的DAG、云上ML平台
- **使用ml-pipeline-orchestrator**：适用于基于SpecWeave的增量式ML开发及实验跟踪

## 适用场景

- 设计基于DAG的工作流编排（Airflow、Dagster、Kubeflow）
- 实现与平台无关的ML管道模式
- 为ML训练任务设置CI/CD自动化流程
- 为团队创建可复用的管道模板
- 与云上ML服务（如SageMaker、Vertex AI、Azure ML）进行集成

## 技能内容

### 核心能力

1. **管道架构**
   - 从开始到结束的工作流设计
   - DAG编排模式（Airflow、Dagster、Kubeflow）
   - 组件依赖关系和数据流
   - 错误处理与重试策略

2. **数据准备**
   - 数据验证和质量检查
   - 特征工程流程
   - 数据版本控制和溯源
   - 训练/验证/测试数据的划分策略

3. **模型训练**
   - 训练任务编排
   - 超参数管理
   - 实验跟踪集成
   - 分布式训练模式

4. **模型验证**
   - 验证框架和指标
   - A/B测试基础设施
   - 性能退化检测
   - 模型比较工作流

5. **部署自动化**
   - 模型部署模式
   - 金丝雀部署（Canary Deployment）
   - 蓝绿部署策略
   - 回滚机制

## 使用模式

### 基础管道设置

```python
# 1. Define pipeline stages
stages = [
    "data_ingestion",
    "data_validation",
    "feature_engineering",
    "model_training",
    "model_validation",
    "model_deployment"
]

# 2. Configure dependencies between stages
```

### 生产工作流

1. **数据准备阶段**
   - 从数据源导入原始数据
   - 运行数据质量检查
   - 应用特征转换
   - 为处理过的数据集创建版本

2. **训练阶段**
   - 加载已版本化的训练数据
   - 执行训练任务
   - 跟踪实验和指标
   - 保存训练好的模型

3. **验证阶段**
   - 运行验证测试套件
   - 与基线进行比较
   - 生成性能报告
   - 审批模型部署

4. **部署阶段**
   - 打包模型成果
   - 部署到服务基础设施
   - 配置监控
   - 验证生产环境的流量

## 最佳实践

### 管道设计

- **模块化**：每个阶段都应可独立测试
- **幂等性**：重新运行各阶段应不会产生错误结果
- **可观测性**：在每个阶段记录指标
- **版本控制**：跟踪数据、代码和模型的版本
- **故障处理**：实现重试逻辑和警报机制

### 数据管理

- 使用数据验证工具（如Great Expectations、TFX）
- 使用DVC或类似工具对数据集进行版本控制
- 记录特征工程转换过程
- 维护数据溯源机制

### 模型操作

- 分离训练和部署基础设施
- 使用模型注册系统（如MLflow、Weights & Biases）
- 对新模型实施渐进式部署
- 监控模型性能的变化
- 保持回滚能力

### 部署策略

- 从影子部署（Shadow Deployment）开始
- 使用金丝雀版本进行验证
- 实施A/B测试
- 设置自动化的回滚机制
- 监控延迟和吞吐量

## 集成点

### 编排工具

- **Apache Airflow**：基于DAG的工作流编排工具
- **Dagster**：基于资产的管道编排工具
- **Kubeflow Pipelines**：原生于Kubernetes的ML工作流工具
- **Prefect**：现代数据流自动化工具

### 实验跟踪

- 使用MLflow进行实验跟踪和模型注册
- 使用Weights & Biases进行可视化与协作
- 使用TensorBoard监控训练指标

### 部署平台

- AWS SageMaker：用于管理的ML基础设施
- Google Vertex AI：用于GCP平台的部署
- Azure ML：用于Azure云平台的部署
- Kubernetes + KServe：适用于跨平台的部署解决方案

## 学习步骤

从基础开始，逐步增加复杂性：

1. **第1级**：简单的线性管道（数据 → 训练 → 部署）
2. **第2级**：添加验证和监控阶段
3. **第3级**：实现超参数调优
4. **第4级**：添加A/B测试和渐进式部署
5. **第5级**：包含集成策略的多模型管道

## 常见模式

### 批量训练管道

```yaml
stages:
  - name: data_preparation
    dependencies: []
  - name: model_training
    dependencies: [data_preparation]
  - name: model_evaluation
    dependencies: [model_training]
  - name: model_deployment
    dependencies: [model_evaluation]
```

### 实时特征处理管道

```python
# Stream processing for real-time features
# Combined with batch training for production
```

### 持续训练管道

```python
# Automated retraining on schedule
# Triggered by data drift detection
```

## 故障排除

### 常见问题

- **管道故障**：检查依赖关系和数据可用性
- **训练不稳定**：审查超参数和数据质量
- **部署问题**：验证模型成果和部署配置
- **性能下降**：监控数据变化和模型指标

### 调试步骤

1. 检查每个阶段的管道日志
2. 验证输入/输出数据的正确性
3. 单独测试各个组件
4. 查看实验跟踪指标
5. 检查模型成果和元数据

## 下一步

设置好管道后，可以进一步学习：

1. 探索**超参数调优**技巧以优化性能
2. 学习**实验跟踪**方法，以便更好地管理MLflow和Weights & Biases
3. 学习**模型部署策略**以优化部署过程
4. 使用可观测性工具实现监控功能

## 相关技能

- **ml-pipeline-orchestrator**：基于SpecWeave的ML开发工具（适用于增量式ML开发）
- **experiment-tracker**：用于实验跟踪和模型管理的工具（如MLflow、Weights & Biases）
- **automl-optimizer**：自动超参数优化工具（如Optuna/Hyperopt）
- **ml-deployment-helper**：用于模型部署的工具