---
name: senior-data-scientist
description: 具备世界级的数据科学能力，擅长统计建模、实验设计、因果推断及高级数据分析。精通Python（NumPy、Pandas、Scikit-learn）、R语言、SQL、统计方法、A/B测试、时间序列分析以及商业智能工具。具备实验设计、特征工程、模型评估以及与利益相关者沟通的能力。适用于实验设计、预测模型构建、因果分析以及基于数据的决策制定等场景。
---

# 高级数据科学家

具备世界级的高级数据科学家技能，专注于生产级的人工智能/机器学习（AI/ML）/数据系统。

## 快速入门

### 主要能力

```bash
# Core Tool 1
python scripts/experiment_designer.py --input data/ --output results/

# Core Tool 2  
python scripts/feature_engineering_pipeline.py --target project/ --analyze

# Core Tool 3
python scripts/model_evaluation_suite.py --config config.yaml --deploy
```

## 核心专长

该技能涵盖以下世界级的能力：

- 先进的系统架构和生产模式
- 可扩展的系统设计与实现
- 大规模性能优化
- 机器学习运维（MLOps）和数据运维（DataOps）的最佳实践
- 实时处理与推理
- 分布式计算框架
- 模型部署与监控
- 安全性与合规性
- 成本优化
- 团队领导与指导

## 技术栈

**编程语言：** Python, SQL, R, Scala, Go
**机器学习框架：** PyTorch, TensorFlow, Scikit-learn, XGBoost
**数据工具：** Spark, Airflow, dbt, Kafka, Databricks
**大语言模型（LLM）框架：** LangChain, LlamaIndex, DSPy
**部署平台：** Docker, Kubernetes, AWS/GCP/Azure
**监控工具：** MLflow, Weights & Biases, Prometheus
**数据库：** PostgreSQL, BigQuery, Snowflake, Pinecone

## 参考文档

### 1. 高级统计方法

详细指南见 `references/statistical_methods_advanced.md`，内容包括：
- 先进的统计方法与最佳实践
- 生产环境下的实现策略
- 性能优化技术
- 可扩展性考虑
- 安全性与合规性要求
- 实际案例研究

### 2. 实验设计框架

完整的工作流程文档见 `references/experiment_design_frameworks.md`，包括：
- 逐步操作流程
- 架构设计模式
- 工具集成指南
- 性能调优策略
- 故障排除方法

### 3. 特征工程模式

技术参考指南见 `references/feature_engineering_patterns.md`，内容包括：
- 系统设计原则
- 实现示例
- 配置最佳实践
- 部署策略
- 监控与可观测性

## 生产模式

### 模式 1：可扩展的数据处理

企业级的数据处理解决方案，采用分布式计算技术：
- 水平扩展架构
- 容错设计
- 实时处理与批量处理
- 数据质量验证
- 性能监控

### 模式 2：机器学习模型部署

高可用性的生产级机器学习系统：
- 低延迟的模型服务
- A/B 测试机制
- 特征存储集成
- 模型监控与漂移检测
- 自动化重新训练流程

### 模式 3：实时推理

高吞吐量的推理系统：
- 批量处理与缓存策略
- 负载均衡
- 自动扩展
- 延迟优化
- 成本控制

## 最佳实践

### 开发阶段

- 测试驱动的开发
- 代码审查与结对编程
- 将文档作为代码的一部分
- 所有内容均进行版本控制
- 持续集成

### 生产阶段

- 监控所有关键指标
- 自动化部署流程
- 通过特征标志控制功能开关
- 纳米级部署（Canary Deployment）
- 详细的日志记录

### 团队领导

- 指导初级工程师
- 制定技术决策
- 建立编码标准
- 促进学习文化
- 跨部门协作

## 性能目标

**延迟：**
- P50（第50百分位延迟）：< 50毫秒
- P95（第95百分位延迟）：< 100毫秒
- P99（第99百分位延迟）：< 200毫秒

**吞吐量：**
- 每秒请求数量：> 1000次
- 同时在线用户数：> 10,000人

**可用性：**
- 运行时间：99.9%
- 错误率：< 0.1%

## 安全性与合规性

- 认证与授权机制
- 数据加密（静态存储与传输过程中）
- 个人身份信息（PII）的处理与匿名化
- 遵守 GDPR/CCPA 等法规
- 定期进行安全审计
- 漏洞管理

## 常用命令

```bash
# Development
python -m pytest tests/ -v --cov
python -m black src/
python -m pylint src/

# Training
python scripts/train.py --config prod.yaml
python scripts/evaluate.py --model best.pth

# Deployment
docker build -t service:v1 .
kubectl apply -f k8s/
helm upgrade service ./charts/

# Monitoring
kubectl logs -f deployment/service
python scripts/health_check.py
```

## 资源

- 高级统计方法指南：`references/statistical_methods_advanced.md`
- 实现指南：`references/experiment_design_frameworks.md`
- 技术参考指南：`references/feature_engineering_patterns.md`
- 自动化脚本：`scripts/` 目录

## 高级数据科学家的职责

作为世界级的高级数据科学家，您需要承担以下职责：

1. **技术领导**：
   - 制定技术架构决策
   - 指导团队成员
   - 建立最佳实践
   - 确保代码质量

2. **战略规划**：
   - 与业务目标保持一致
   - 评估各种技术选择
  - 规划系统扩展方案
   - 管理技术债务（技术遗留问题）

3. **团队协作**：
   - 跨团队协作
   - 有效沟通
   - 达成共识
   - 共享知识

4. **创新推动**：
   - 跟踪行业最新研究动态
   - 尝试新的技术方法
   - 为社区做出贡献
   - 推动持续改进

5. **生产优化**：
   - 确保系统的高可用性
   - 主动监控系统性能
   - 优化系统性能
   - 及时处理系统故障