---
name: senior-data-engineer
description: 数据工程技能：专注于构建可扩展的数据管道、ETL/ELT系统以及数据基础设施。具备Python、SQL、Spark、Airflow、dbt、Kafka等现代数据工具的深厚经验，熟悉数据建模、管道编排、数据质量管理和DataOps（数据运营）流程。这些技能在设计数据架构、构建数据管道、优化数据工作流程、实施数据治理以及解决数据相关问题时至关重要。
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

在遇到以下情况时，请使用此技能：

**管道设计：**
- “为……设计数据管道”
- “构建ETL/ELT流程”
- “如何从……导入数据”
- “设置数据提取”

**架构：**
- “应该使用批处理还是流处理？”
- “Lambda架构与Kappa架构”
- “如何处理延迟到达的数据”
- “设计数据湖仓”

**数据建模：**
- “创建维度模型”
- “星型模式与雪花模式”
- “实现缓慢变化的数据维度”
- “设计数据保险库”

**数据质量：**
- “为……添加数据验证”
- “设置数据质量检查”
- “监控数据新鲜度”
- “实现数据契约”

**性能：**
- “优化这个Spark作业”
- “查询运行缓慢”
- “减少管道执行时间”
- “调整Airflow有向无环图（DAG）”

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

### 工作流程1：构建批处理ETL管道

**场景：** 从PostgreSQL提取数据，使用dbt进行转换，然后加载到Snowflake。

#### 第1步：定义源数据结构

```sql
-- Document source tables
SELECT
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'source_schema'
ORDER BY table_name, ordinal_position;
```

#### 第2步：生成提取配置

```bash
python scripts/pipeline_orchestrator.py generate \
  --type airflow \
  --source postgres \
  --tables orders,customers,products \
  --mode incremental \
  --watermark updated_at \
  --output dags/extract_source.py
```

#### 第3步：创建dbt模型

```sql
-- models/staging/stg_orders.sql
WITH source AS (
    SELECT * FROM {{ source('postgres', 'orders') }}
),

renamed AS (
    SELECT
        order_id,
        customer_id,
        order_date,
        total_amount,
        status,
        _extracted_at
    FROM source
    WHERE order_date >= DATEADD(day, -3, CURRENT_DATE)
)

SELECT * FROM renamed
```

#### 第4步：配置数据质量测试

```yaml
# models/marts/schema.yml
version: 2

models:
  - name: fct_orders
    description: "Order fact table"
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: total_amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 1000000
      - name: order_date
        tests:
          - not_null
          - dbt_utils.recency:
              datepart: day
              field: order_date
              interval: 1
```

#### 第5步：创建Airflow有向无环图（DAG）

```python
# dags/daily_etl.py
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['data-alerts@company.com'],
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'daily_etl_pipeline',
    default_args=default_args,
    description='Daily ETL from PostgreSQL to Snowflake',
    schedule_interval='0 5 * * *',
    start_date=days_ago(1),
    catchup=False,
    tags=['etl', 'daily'],
) as dag:

    extract = BashOperator(
        task_id='extract_source_data',
        bash_command='python /opt/airflow/scripts/extract.py --date {{ ds }}',
    )

    transform = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd /opt/airflow/dbt && dbt run --select marts.*',
    )

    test = BashOperator(
        task_id='run_dbt_tests',
        bash_command='cd /opt/airflow/dbt && dbt test --select marts.*',
    )

    notify = BashOperator(
        task_id='send_notification',
        bash_command='python /opt/airflow/scripts/notify.py --status success',
        trigger_rule='all_success',
    )

    extract >> transform >> test >> notify
```

#### 第6步：验证管道

```bash
# Test locally
dbt run --select stg_orders fct_orders
dbt test --select fct_orders

# Validate data quality
python scripts/data_quality_validator.py validate \
  --table fct_orders \
  --checks all \
  --output reports/quality_report.json
```

---

### 工作流程2：实现实时流处理

**场景：** 从Kafka接收事件流，使用Flink/Spark Streaming进行处理，然后存储到数据湖中。

#### 第1步：定义事件结构

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "UserEvent",
  "type": "object",
  "required": ["event_id", "user_id", "event_type", "timestamp"],
  "properties": {
    "event_id": {"type": "string", "format": "uuid"},
    "user_id": {"type": "string"},
    "event_type": {"type": "string", "enum": ["page_view", "click", "purchase"]},
    "timestamp": {"type": "string", "format": "date-time"},
    "properties": {"type": "object"}
  }
}
```

#### 第2步：创建Kafka主题

```bash
# Create topic with appropriate partitions
kafka-topics.sh --create \
  --bootstrap-server localhost:9092 \
  --topic user-events \
  --partitions 12 \
  --replication-factor 3 \
  --config retention.ms=604800000 \
  --config cleanup.policy=delete

# Verify topic
kafka-topics.sh --describe \
  --bootstrap-server localhost:9092 \
  --topic user-events
```

#### 第3步：实现Spark Streaming作业

```python
# streaming/user_events_processor.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    from_json, col, window, count, avg,
    to_timestamp, current_timestamp
)
from pyspark.sql.types import (
    StructType, StructField, StringType,
    TimestampType, MapType
)

# Initialize Spark
spark = SparkSession.builder \
    .appName("UserEventsProcessor") \
    .config("spark.sql.streaming.checkpointLocation", "/checkpoints/user-events") \
    .config("spark.sql.shuffle.partitions", "12") \
    .getOrCreate()

# Define schema
event_schema = StructType([
    StructField("event_id", StringType(), False),
    StructField("user_id", StringType(), False),
    StructField("event_type", StringType(), False),
    StructField("timestamp", StringType(), False),
    StructField("properties", MapType(StringType(), StringType()), True)
])

# Read from Kafka
events_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "user-events") \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load()

# Parse JSON
parsed_df = events_df \
    .select(from_json(col("value").cast("string"), event_schema).alias("data")) \
    .select("data.*") \
    .withColumn("event_timestamp", to_timestamp(col("timestamp")))

# Windowed aggregation
aggregated_df = parsed_df \
    .withWatermark("event_timestamp", "10 minutes") \
    .groupBy(
        window(col("event_timestamp"), "5 minutes"),
        col("event_type")
    ) \
    .agg(
        count("*").alias("event_count"),
        approx_count_distinct("user_id").alias("unique_users")
    )

# Write to Delta Lake
query = aggregated_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/checkpoints/user-events-aggregated") \
    .option("path", "/data/lake/user_events_aggregated") \
    .trigger(processingTime="1 minute") \
    .start()

query.awaitTermination()
```

#### 第4步：处理延迟到达的数据和错误

```python
# Dead letter queue for failed records
from pyspark.sql.functions import current_timestamp, lit

def process_with_error_handling(batch_df, batch_id):
    try:
        # Attempt processing
        valid_df = batch_df.filter(col("event_id").isNotNull())
        invalid_df = batch_df.filter(col("event_id").isNull())

        # Write valid records
        valid_df.write \
            .format("delta") \
            .mode("append") \
            .save("/data/lake/user_events")

        # Write invalid to DLQ
        if invalid_df.count() > 0:
            invalid_df \
                .withColumn("error_timestamp", current_timestamp()) \
                .withColumn("error_reason", lit("missing_event_id")) \
                .write \
                .format("delta") \
                .mode("append") \
                .save("/data/lake/dlq/user_events")

    except Exception as e:
        # Log error, alert, continue
        logger.error(f"Batch {batch_id} failed: {e}")
        raise

# Use foreachBatch for custom processing
query = parsed_df.writeStream \
    .foreachBatch(process_with_error_handling) \
    .option("checkpointLocation", "/checkpoints/user-events") \
    .start()
```

#### 第5步：监控流处理状态

```python
# monitoring/stream_metrics.py
from prometheus_client import Gauge, Counter, start_http_server

# Define metrics
RECORDS_PROCESSED = Counter(
    'stream_records_processed_total',
    'Total records processed',
    ['stream_name', 'status']
)

PROCESSING_LAG = Gauge(
    'stream_processing_lag_seconds',
    'Current processing lag',
    ['stream_name']
)

BATCH_DURATION = Gauge(
    'stream_batch_duration_seconds',
    'Last batch processing duration',
    ['stream_name']
)

def emit_metrics(query):
    """Emit Prometheus metrics from streaming query."""
    progress = query.lastProgress
    if progress:
        RECORDS_PROCESSED.labels(
            stream_name='user-events',
            status='success'
        ).inc(progress['numInputRows'])

        if progress['sources']:
            # Calculate lag from latest offset
            for source in progress['sources']:
                end_offset = source.get('endOffset', {})
                # Parse Kafka offsets and calculate lag
```

---

### 工作流程3：数据质量框架设置

**场景：** 使用Great Expectations实现全面的数据质量监控。

#### 第1步：初始化Great Expectations

```bash
# Install and initialize
pip install great_expectations

great_expectations init

# Connect to data source
great_expectations datasource new
```

#### 第2步：创建预期检查集

```python
# expectations/orders_suite.py
import great_expectations as gx

context = gx.get_context()

# Create expectation suite
suite = context.add_expectation_suite("orders_quality_suite")

# Add expectations
validator = context.get_validator(
    batch_request={
        "datasource_name": "warehouse",
        "data_asset_name": "orders",
    },
    expectation_suite_name="orders_quality_suite"
)

# Schema expectations
validator.expect_table_columns_to_match_ordered_list(
    column_list=[
        "order_id", "customer_id", "order_date",
        "total_amount", "status", "created_at"
    ]
)

# Completeness expectations
validator.expect_column_values_to_not_be_null("order_id")
validator.expect_column_values_to_not_be_null("customer_id")
validator.expect_column_values_to_not_be_null("order_date")

# Uniqueness expectations
validator.expect_column_values_to_be_unique("order_id")

# Range expectations
validator.expect_column_values_to_be_between(
    "total_amount",
    min_value=0,
    max_value=1000000
)

# Categorical expectations
validator.expect_column_values_to_be_in_set(
    "status",
    ["pending", "confirmed", "shipped", "delivered", "cancelled"]
)

# Freshness expectation
validator.expect_column_max_to_be_between(
    "order_date",
    min_value={"$PARAMETER": "now - timedelta(days=1)"},
    max_value={"$PARAMETER": "now"}
)

# Referential integrity
validator.expect_column_values_to_be_in_set(
    "customer_id",
    value_set={"$PARAMETER": "valid_customer_ids"}
)

validator.save_expectation_suite(discard_failed_expectations=False)
```

#### 第3步：使用dbt创建数据质量检查

```yaml
# models/marts/schema.yml
version: 2

models:
  - name: fct_orders
    description: "Order fact table with data quality checks"

    tests:
      # Row count check
      - dbt_utils.equal_rowcount:
          compare_model: ref('stg_orders')

      # Freshness check
      - dbt_utils.recency:
          datepart: hour
          field: created_at
          interval: 24

    columns:
      - name: order_id
        description: "Unique order identifier"
        tests:
          - unique
          - not_null
          - relationships:
              to: ref('dim_orders')
              field: order_id

      - name: total_amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 1000000
              inclusive: true
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              row_condition: "status != 'cancelled'"

      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id
              severity: warn
```

#### 第4步：实现数据契约

```yaml
# contracts/orders_contract.yaml
contract:
  name: orders_data_contract
  version: "1.0.0"
  owner: data-team@company.com

schema:
  type: object
  properties:
    order_id:
      type: string
      format: uuid
      description: "Unique order identifier"
    customer_id:
      type: string
      not_null: true
    order_date:
      type: date
      not_null: true
    total_amount:
      type: decimal
      precision: 10
      scale: 2
      minimum: 0
    status:
      type: string
      enum: ["pending", "confirmed", "shipped", "delivered", "cancelled"]

sla:
  freshness:
    max_delay_hours: 1
  completeness:
    min_percentage: 99.9
  accuracy:
    duplicate_tolerance: 0.01

consumers:
  - name: analytics-team
    usage: "Daily reporting dashboards"
  - name: ml-team
    usage: "Churn prediction model"
```

#### 第5步：设置质量监控仪表板

```python
# monitoring/quality_dashboard.py
from datetime import datetime, timedelta
import pandas as pd

def generate_quality_report(connection, table_name: str) -> dict:
    """Generate comprehensive data quality report."""

    report = {
        "table": table_name,
        "timestamp": datetime.now().isoformat(),
        "checks": {}
    }

    # Row count check
    row_count = connection.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    ).fetchone()[0]
    report["checks"]["row_count"] = {
        "value": row_count,
        "status": "pass" if row_count > 0 else "fail"
    }

    # Freshness check
    max_date = connection.execute(
        f"SELECT MAX(created_at) FROM {table_name}"
    ).fetchone()[0]
    hours_old = (datetime.now() - max_date).total_seconds() / 3600
    report["checks"]["freshness"] = {
        "max_timestamp": max_date.isoformat(),
        "hours_old": round(hours_old, 2),
        "status": "pass" if hours_old < 24 else "fail"
    }

    # Null rate check
    null_query = f"""
    SELECT
        SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) as null_order_id,
        SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) as null_customer_id,
        COUNT(*) as total
    FROM {table_name}
    """
    null_result = connection.execute(null_query).fetchone()
    report["checks"]["null_rates"] = {
        "order_id": null_result[0] / null_result[2] if null_result[2] > 0 else 0,
        "customer_id": null_result[1] / null_result[2] if null_result[2] > 0 else 0,
        "status": "pass" if null_result[0] == 0 and null_result[1] == 0 else "fail"
    }

    # Duplicate check
    dup_query = f"""
    SELECT COUNT(*) - COUNT(DISTINCT order_id) as duplicates
    FROM {table_name}
    """
    duplicates = connection.execute(dup_query).fetchone()[0]
    report["checks"]["duplicates"] = {
        "count": duplicates,
        "status": "pass" if duplicates == 0 else "fail"
    }

    # Overall status
    all_passed = all(
        check["status"] == "pass"
        for check in report["checks"].values()
    )
    report["overall_status"] = "pass" if all_passed else "fail"

    return report
```

---

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

| 特点 | Lambda | Kappa |
|--------|--------|-------|
| **复杂性** | 两个代码库（批处理+流处理） | 单一代码库 |
| **维护成本** | 较高（需要同步批处理/流处理逻辑） | 较低 |
| **重新处理** | 内置的批处理层 | 从源重新处理 |
| **适用场景** | 机器学习训练+实时服务 | 纯事件驱动 |

**何时选择Lambda：**
- 需要对历史数据训练机器学习模型
- 流处理无法实现复杂的批处理转换
- 已有的批处理基础设施

**何时选择Kappa：**
- 基于事件的架构
- 所有处理都可以表示为流处理操作
- 从零开始构建，无需使用旧系统

### 数据仓库与数据湖仓

| 特性 | 数据仓库（Snowflake/BigQuery） | 数据湖仓（Delta/Iceberg） |
|---------|-------------------------------|---------------------------|
| **最适合** | 商业智能（BI）、SQL分析 | 机器学习、非结构化数据 |
| **存储成本** | 较高（专有格式） | 较低（开放格式） |
| **灵活性** | 写时定义模式 | 读时定义模式 |
| **性能** | 非常适合SQL查询 | 性能良好，可逐步提升 |
| **生态系统** | 成熟的商业智能工具 | 不断发展的机器学习工具 |

---

## 技术栈

| 类别 | 技术 |
|----------|--------------|
| **编程语言** | Python、SQL、Scala |
| **任务调度** | Airflow、Prefect、Dagster |
| **数据转换** | dbt、Spark、Flink |
| **流处理** | Kafka、Kinesis、Pub/Sub |
| **存储** | S3、GCS、Delta Lake、Iceberg |
| **数据仓库** | Snowflake、BigQuery、Redshift、Databricks |
| **数据质量** | Great Expectations、dbt测试、蒙特卡洛方法 |
| **监控** | Prometheus、Grafana、Datadog |

---

## 参考文档

### 1. 数据管道架构
请参阅`references/data_pipeline_architecture.md`，了解：
- Lambda架构与Kappa架构模式
- 使用Spark和Airflow进行批处理
- 使用Kafka和Flink进行流处理
- 实现“恰好一次”语义
- 错误处理和死信队列

### 2. 数据建模模式
请参阅`references/data_modeling_patterns.md`，了解：
- 维度建模（星型模式/雪花模式）
- 慢速变化的数据维度（SCD类型1-6）
- 数据保险库建模
- dbt最佳实践
- 分区和聚类

### 3. 数据运维最佳实践
请参阅`references/dataops_best_practices.md`，了解：
- 数据测试框架
- 数据契约和模式验证
- 数据管道的持续集成/持续交付（CI/CD）
- 可观测性和数据来源追踪
- 事件响应

---

## 故障排除

### 管道故障

**症状：** Airflow有向无环图（DAG）因超时失败
**解决方案：**
1. 检查资源分配
2. 分析运行缓慢的操作
3. 添加增量处理逻辑
```python
# Increase timeout
default_args = {
    'execution_timeout': timedelta(hours=2),
}

# Or use incremental loads
WHERE updated_at > '{{ prev_ds }}'
```

---

**症状：** Spark作业内存不足（OOM）
**解决方案：**
1. 增加执行器内存
2. 减小分区大小
3. 使用磁盘溢出机制
```python
spark.conf.set("spark.executor.memory", "8g")
spark.conf.set("spark.sql.shuffle.partitions", "200")
spark.conf.set("spark.memory.fraction", "0.8")
```

**症状：** Kafka消费者延迟增加
**解决方案：**
1. 增加消费者并行度
2. 优化处理逻辑
3. 扩展消费者组
```bash
# Add more partitions
kafka-topics.sh --alter \
  --bootstrap-server localhost:9092 \
  --topic user-events \
  --partitions 24
```

### 数据质量问题

**症状：** 出现重复记录
**解决方案：**
1. 添加去重逻辑
2. 使用合并/插入操作
```sql
-- dbt incremental with dedup
{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

SELECT * FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY updated_at DESC
        ) as rn
    FROM {{ source('raw', 'orders') }}
) WHERE rn = 1
```

**症状：** 表格中的数据过时
**解决方案：**
1. 检查上游管道的状态
2. 验证数据源的可用性
3. 添加数据新鲜度监控
```yaml
# dbt freshness check
sources:
  - name: raw
    freshness:
      warn_after: {count: 12, period: hour}
      error_after: {count: 24, period: hour}
    loaded_at_field: _loaded_at
```

**症状：** 检测到模式漂移
**解决方案：**
1. 更新数据契约
2. 修改数据转换逻辑
3. 与数据生产者沟通
```python
# Handle schema evolution
df = spark.read.format("delta") \
    .option("mergeSchema", "true") \
    .load("/data/orders")
```

### 性能问题

**症状：** 查询耗时过长
**解决方案：**
1. 检查查询计划
2. 添加适当的分区
3. 优化连接操作
```sql
-- Before: Full table scan
SELECT * FROM orders WHERE order_date = '2024-01-15';

-- After: Partition pruning
-- Table partitioned by order_date
SELECT * FROM orders WHERE order_date = '2024-01-15';

-- Add clustering for frequent filters
ALTER TABLE orders CLUSTER BY (customer_id);
```

**症状：** dbt模型运行时间过长
**解决方案：**
1. 使用增量式数据生成机制
2. 减少对上游数据的依赖
3. 在可能的情况下进行预聚合
```sql
-- Convert to incremental
{{
    config(
        materialized='incremental',
        unique_key='order_id',
        on_schema_change='sync_all_columns'
    )
}}

SELECT * FROM {{ ref('stg_orders') }}
{% if is_incremental() %}
WHERE _loaded_at > (SELECT MAX(_loaded_at) FROM {{ this }})
{% endif %}
```