---
name: "senior-data-engineer"
description: 数据工程技能：专注于构建可扩展的数据管道、ETL/ELT系统以及数据基础设施。具备Python、SQL、Spark、Airflow、dbt、Kafka等现代数据技术的专业能力，涵盖数据建模、数据管道编排、数据质量管理和数据运维（DataOps）等方面。这些技能在设计数据架构、构建数据管道、优化数据工作流程、实施数据治理以及解决数据相关问题时都非常实用。
---
# 高级数据工程师

具备生产级的数据工程技能，能够构建可扩展、可靠的数据系统。

## 目录

1. [常用术语](#trigger-phrases)
2. [快速入门](#quick-start)
3. [工作流程](#workflows)
   - [构建批处理ETL管道](#workflow-1-building-a-batch-etl-pipeline)
   - [实现实时流处理](#workflow-2-implementing-real-time-streaming)
   - [数据质量框架设置](#workflow-3-data-quality-framework-setup)
4. [架构决策框架](#architecture-decision-framework)
5. [技术栈](#tech-stack)
6. [参考文档](#reference-documentation)
7. [故障排除](#troubleshooting)

---

## 常用术语

当遇到以下情况时，请使用此技能：

**管道设计：**
- “为……设计数据管道”
- “构建ETL/ELT流程”
- “如何从……导入数据”
- “设置数据提取”

**架构：**
- “应该使用批处理还是流处理？”
- “Lambda架构与Kappa架构”
- “如何处理延迟到达的数据”
- “设计数据湖屋”

**数据建模：**
- “创建维度模型”
- “星型模式与雪花模式”
- “实现缓慢变化的数据维度”
- “设计数据保险库”

**数据质量：**
- “为……添加数据验证”
- “设置数据质量检查”
- “监控数据新鲜度”
- “实施数据契约”

**性能：**
- “优化这个Spark作业”
- “查询运行缓慢”
- “减少管道执行时间”
- “调整Airflow的DAG”

---

## 快速入门

### 核心工具

```bash
# Generate pipeline orchestration config
python scripts/pipeline_orchestrator.py generate \
  --type airflow \
  --source postgres \
  --destination snowflake \
  --schedule "0 5 * * *"

# Validate data quality
python scripts/data_quality_validator.py validate \
  --input data/sales.parquet \
  --schema schemas/sales.json \
  --checks freshness,completeness,uniqueness

# Optimize ETL performance
python scripts/etl_performance_optimizer.py analyze \
  --query queries/daily_aggregation.sql \
  --engine spark \
  --recommend
```

---

## 工作流程
详细内容请参阅 `references/workflows.md`。

## 架构决策框架

使用此框架来选择适合您的数据管道方案。

### 批处理与流处理

| 标准 | 批处理 | 流处理 |
|--------|--------|-----------|
| **延迟要求** | 数小时至数天 | 几秒至几分钟 |
| **数据量** | 大型历史数据集 | 持续的事件流 |
| **处理复杂性** | 复杂的转换、机器学习 | 简单的聚合、过滤 |
| **成本敏感性** | 更具成本效益 | 更高的基础设施成本 |
| **错误处理** | 更容易重新处理 | 需要仔细设计 |

**决策树：**
```
Is real-time insight required?
├── Yes → Use streaming
│   └── Is exactly-once semantics needed?
│       ├── Yes → Kafka + Flink/Spark Structured Streaming
│       └── No → Kafka + consumer groups
└── No → Use batch
    └── Is data volume > 1TB daily?
        ├── Yes → Spark/Databricks
        └── No → dbt + warehouse compute
```

### Lambda架构与Kappa架构

| 特征 | Lambda | Kappa |
|--------|--------|-------|
| **复杂性** | 两个代码库（批处理 + 流处理） | 单一代码库 |
| **维护** | 更高（需要同步批处理/流处理逻辑） | 更低 |
| **重新处理** | 内置的批处理层 | 从源头重新处理 |
| **使用场景** | 机器学习训练 + 实时服务 | 纯事件驱动 |

**何时选择Lambda：**
- 需要使用历史数据训练机器学习模型
- 流处理无法实现复杂的批处理转换
- 已有的批处理基础设施

**何时选择Kappa：**
- 基于事件的架构
- 所有处理都可以表示为流处理操作
- 无需依赖旧系统，可以全新开始

### 数据仓库与数据湖屋

| 特性 | 数据仓库（Snowflake/BigQuery） | 数据湖屋（Delta/Iceberg） |
|---------|-------------------------------|---------------------------|
| **最适合** | 商业智能、SQL分析 | 机器学习、非结构化数据 |
| **存储成本** | 较高（专有格式） | 较低（开放格式） |
| **灵活性** | 写时定义模式 | 读时定义模式 |
| **性能** | 非常适合SQL查询 | 性能良好，正在改进中 |
| **生态系统** | 成熟的商业智能工具 | 发展中的机器学习工具 |

---

## 技术栈

| 类别 | 技术 |
|----------|--------------|
| **编程语言** | Python、SQL、Scala |
| **编排工具** | Airflow、Prefect、Dagster |
| **数据转换工具** | dbt、Spark、Flink |
| **流处理工具** | Kafka、Kinesis、Pub/Sub |
| **存储工具** | S3、GCS、Delta Lake、Iceberg |
| **数据仓库工具** | Snowflake、BigQuery、Redshift、Databricks |
| **数据质量工具** | Great Expectations、dbt测试、Monte Carlo |
| **监控工具** | Prometheus、Grafana、Datadog |

---

## 参考文档

### 1. 数据管道架构
请参阅 `references/data_pipeline_architecture.md`，了解：
- Lambda架构与Kappa架构的对比
- 使用Spark和Airflow进行批处理
- 使用Kafka和Flink进行流处理
- 实现“恰好一次”语义
- 错误处理和死信队列

### 2. 数据建模模式
请参阅 `references/data_modeling_patterns.md`，了解：
- 维度建模（星型模式/雪花模式）
- 慢速变化的数据维度（SCD类型1-6）
- 数据保险库建模
- dbt的最佳实践
- 分区和聚类

### 3. 数据运维最佳实践
请参阅 `references/dataops_best_practices.md`，了解：
- 数据测试框架
- 数据契约和模式验证
- 数据管道的持续集成/持续部署
- 可观测性和数据溯源
- 事件响应

---

## 故障排除
详细内容请参阅 `references/troubleshooting.md`。