# 机器学习与人工智能工程系统

一套完整的构建、部署和运维生产级机器学习/人工智能系统的方法论——从实验到规模化应用。

---

## 第1阶段：问题定义

在编写任何代码之前，首先要明确机器学习问题的具体内容。

### 机器学习问题概述

```yaml
problem_brief:
  business_objective: ""          # What business metric improves?
  success_metric: ""              # Quantified target (e.g., "reduce churn 15%")
  baseline: ""                    # Current performance without ML
  ml_task_type: ""                # classification | regression | ranking | generation | clustering | anomaly_detection | recommendation
  prediction_target: ""           # What exactly are we predicting?
  prediction_consumer: ""         # Who/what uses the prediction? (API | dashboard | email | automated action)
  latency_requirement: ""         # real-time (<100ms) | near-real-time (<1s) | batch (minutes-hours)
  data_available: ""              # What data exists today?
  data_gaps: ""                   # What's missing?
  ethical_considerations: ""      # Bias risks, fairness requirements, privacy
  kill_criteria:                  # When to abandon the ML approach
    - "Baseline heuristic achieves >90% of ML performance"
    - "Data quality too poor after 2 weeks of cleaning"
    - "Model can't beat random by >10% on holdout set"
```

### 使用规则还是机器学习

| 信号类型 | 使用规则 | 使用机器学习 |
|--------|-----------|--------|
| 逻辑可以用少于10条规则解释 | ✅ | ❌ |
| 模式过于复杂，人类难以理解 | ❌ | ✅ |
| 训练数据量超过1000个标注样本 | — | ✅ |
| 需要适应新的模式 | ❌ | ✅ |
| 必须100%可审计/确定性 | ✅ | ❌ |
| 模式变化速度超过规则更新速度 | ❌ | ✅ |

**经验法则：** 先尝试使用规则或启发式方法。只有在规则无法捕捉到问题模式时，再引入机器学习。

---

## 第2阶段：机器学习的数据工程

### 数据质量评估

对每个数据源进行评分（每个维度0-5分）：

| 维度 | 0（非常差） | 5（优秀） |
|-----------|--------------|----------------|
| **完整性** | 缺失数据超过50% | 缺失数据少于1% |
| **准确性** | 存在已知错误，未进行验证 | 已根据真实数据进行验证 |
| **一致性** | 数据格式不一致，存在重复数据 | 数据已标准化并去重 |
| **时效性** | 数据已经过时数月 | 数据实时更新或每日更新 |
| **相关性** | 作为预测的代理指标较弱 | 数据是预测的直接依据 |
| **数据量** | 每个类别的样本少于100个 | 每个类别的样本超过10,000个 |

**最低评分要求：** 18/30分。低于18分 → 先修复数据，再构建模型。

### 特征工程模式

```yaml
feature_types:
  numerical:
    - raw_value           # Use as-is if normally distributed
    - log_transform       # Right-skewed distributions (revenue, counts)
    - standardize         # z-score for algorithms sensitive to scale (SVM, KNN, neural nets)
    - bin_to_categorical  # When relationship is non-linear and data is limited
  categorical:
    - one_hot             # <20 categories, tree-based models handle natively
    - target_encoding     # High-cardinality (>20 categories), use with K-fold to prevent leakage
    - embedding           # Very high-cardinality (user IDs, product IDs) with deep learning
  temporal:
    - lag_features        # Value at t-1, t-7, t-30
    - rolling_statistics  # Mean, std, min, max over windows
    - time_since_event    # Days since last purchase, hours since login
    - cyclical_encoding   # sin/cos for hour-of-day, day-of-week, month
  text:
    - tfidf               # Simple, interpretable, good baseline
    - sentence_embeddings # semantic similarity, modern NLP
    - llm_extraction      # Use LLM to extract structured fields from unstructured text
  interaction:
    - ratios              # Feature A / Feature B (e.g., clicks/impressions = CTR)
    - differences         # Feature A - Feature B (e.g., price - competitor_price)
    - polynomial          # A * B, A^2 (use sparingly, high-cardinality features)
```

### 特征存储设计

```yaml
feature_store:
  offline_store:         # For training — batch computed, stored in data warehouse
    storage: "BigQuery | Snowflake | S3+Parquet"
    compute: "Spark | dbt | SQL"
    refresh: "daily | hourly"
  online_store:          # For serving — low-latency lookups
    storage: "Redis | DynamoDB | Feast online"
    latency_target: "<10ms p99"
    refresh: "streaming | near-real-time"
  registry:              # Feature metadata
    naming: "{entity}_{feature_name}_{window}_{aggregation}"  # e.g., user_purchase_count_30d_sum
    documentation:
      - description
      - data_type
      - source_table
      - owner
      - created_date
      - known_issues
```

### 数据泄露预防检查清单

- [ ] 特征中不包含未来信息（防止时间旅行问题）
- [ ] 在进行特征工程之前完成训练/验证/测试数据的分割
- [ ] 目标变量的编码仅使用训练集中的统计数据
- [ ] 不从目标变量派生新的特征
- [ ] 对于时间序列数据，使用时间分割（避免随机打乱）
- [ ] 在任何数据探索（EDA）之前创建保留集
- [ ] 在分割数据之前去除重复项（确保训练集和测试集中的实体相同）
- [ ] 在训练集上完成标准化/缩放处理，然后在验证集/测试集上应用相同处理

---

## 第3阶段：实验管理

### 实验跟踪模板

```yaml
experiment:
  id: "EXP-{YYYY-MM-DD}-{NNN}"
  hypothesis: ""                 # "Adding user tenure features will improve churn prediction AUC by >2%"
  dataset_version: ""            # Hash or version of training data
  features_used: []              # List of feature names
  model_type: ""                 # Algorithm name
  hyperparameters: {}            # All hyperparams logged
  training_time: ""              # Wall clock
  metrics:
    primary: {}                  # The one metric that matters
    secondary: {}                # Supporting metrics
  baseline_comparison: ""        # Delta vs baseline
  verdict: "promoted | archived | iterate"
  notes: ""
  artifacts:
    - model_path: ""
    - notebook_path: ""
    - confusion_matrix: ""
```

### 模型选择指南

| 任务 | 初始选择 | 扩展选择 | 应避免的选择 |
|------|-----------|----------|-------|
| 表格分类 | XGBoost/LightGBM | 仅当样本量超过100,000个时使用神经网络 | 对于样本量少于10,000个的情况，使用深度学习 |
| 表格回归 | XGBoost/LightGBM | 对于类别数量较多的情况，使用CatBoost | 不进行特征工程时使用线性回归 |
| 图像分类 | 对ResNet/EfficientNet进行微调 | 如果图像数量超过100,000张，使用视觉Transformer | 从零开始训练 |
| 文本分类 | 对BERT/RoBERTa进行微调 | 如果标注数据稀缺，可以使用少量样本的LLM | 对于需要细致区分的任务，可以使用词袋模型 |
| 文本生成 | 使用GPT-4/Claude API | 对于成本敏感的任务，可以使用微调后的Llama/Mistral | 从零开始训练 |
| 时间序列 | 使用Prophet/ARIMA作为基线 → 使用LightGBM | 使用时间融合Transformer | 除非有特殊理由，否则避免使用LSTM |
| 推荐系统 | 使用协同过滤作为基线 | 使用双塔神经网络 | 对于用户数量少于1,000的情况，避免使用复杂模型 |
| 异常检测 | 使用孤立森林 | 如果数据维度较高，可以使用自动编码器 | 对于没有标注异常值的情况，避免使用监督学习方法 |
| 搜索/排序 | 使用BM25作为基线 → 使用学习排序 | 使用交叉编码器进行重新排序 | 对于纯关键词搜索，避免使用简单的关键词方法 |

### 超参数调优策略

1. **先手动调整** — 理解3-5个最关键的参数
2. **贝叶斯优化**（Optuna） — 对于生产级模型，进行50-100次尝试
3. **网格搜索** — 仅用于2-3个参数的最终微调
4. **随机搜索** — 对于超过4个参数的情况，随机搜索效果更好

**不同模型的关键超参数：**

| 模型 | 关键参数 | 典型范围 |
|-------|----------------|---------------|
| XGBoost | learning_rate, max_depth, n_estimators, min_child_weight | 0.01-0.3, 3-10, 100-1000, 1-10 |
| LightGBM | learning_rate, num_leaves, feature_fraction, min_data_in_leaf | 0.01-0.3, 15-255, 0.5-1.0, 5-100 |
| 神经网络 | learning_rate, batch_size, hidden_dims, dropout | 1e-5到1e-2, 32-512, 取决于架构, 0.1-0.5 |
| 随机森林 | n_estimators, max_depth, min_samples_leaf | 100-1000, 5-30, 1-20 |

---

## 第4阶段：模型评估

### 根据任务选择评估指标

| 任务 | 主要评估指标 | 适用场景 | 注意事项 |
|------|---------------|-------------|---------------|
| 二元分类（平衡数据） | F1分数 | 精确度和召回率同等重要 | — |
| 二元分类（不平衡数据） | PR-AUC | 罕见正类占比低于5% | ROC-AUC可能掩盖少数类的性能问题 |
| 多类分类 | 宏F1分数 | 所有类别的重要性相同 | 如果类别频率与重要性相同，使用微F1分数 |
| 回归 | 均方绝对误差（MAE） | 异常值不应主导结果 | RMSE会对较大误差给予更重的惩罚 |
| 排名 | NDCG@K | 前K名结果最重要 | 如果是二元相关任务，使用MAP |
| 生成任务 | 人工评估 + 自动评估 | 质量具有主观性 | 仅使用BLEU/ROUGE评估不够全面 |
| 异常检测 | 精确率@K | 假阳性结果可能代价高昂 | 如果缺失异常值，召回率很重要 |

### 评估严谨性检查清单

- [ ] 指标基于训练集或调优过程中未见过的真实保留集计算 |
- [ ] 对于数据量小于10,000个的小数据集，使用交叉验证 |
- [ ] 对于不平衡类别，使用分层分割 |
- [ ] 对于时间依赖型数据，使用时间分割 |
- [ ] 报告置信区间（使用自助法或交叉验证） |
- [ ] 按重要维度（如地理位置、用户群体等）分解性能 |
- [ ] 确保不同保护群体的评估公平性 |
- [ ] 与简单基线（多数类、平均预测值、规则）进行比较 |
- [ ] 错误分析：手动检查最差的50个预测结果 |
- [ ] 对于概率预测，使用校准图 |

### 从离线到在线的过渡分析

在部署之前，验证以下内容是否会导致训练结果与在线服务结果之间的偏差：

| 检查项 | 离线情况 | 在线情况 | 应采取的措施 |
|-------|---------|--------|--------|
| 特征计算 | 批量SQL处理 | 实时API处理 | 确保逻辑一致，并通过回放进行测试 |
| 数据新鲜度 | 瞬时快照 | 最新数据 | 文档记录可接受的数据陈旧程度 |
| 缺失值处理 | 在处理过程中进行插补 | 数据可能确实缺失 | 在服务过程中优雅地处理缺失值 |
| 特征分布 | 训练期间与当前时期的分布 | 监控部署后的分布变化 |

---

## 第5阶段：模型部署

### 部署模式选择

```
Is latency < 100ms required?
├── Yes → Is model < 500MB?
│   ├── Yes → Embedded serving (FastAPI + model in memory)
│   └── No → Model server (Triton, TorchServe, vLLM)
└── No → Is it a batch prediction?
    ├── Yes → Batch pipeline (Spark, Airflow + offline inference)
    └── No → Async queue (Celery/SQS → worker → result store)
```

### 生产环境服务检查清单

```yaml
serving_config:
  model:
    format: ""                    # ONNX | TorchScript | SavedModel | safetensors
    version: ""                   # Semantic version
    size_mb: null
    load_time_seconds: null
  infrastructure:
    compute: ""                   # CPU | GPU (T4/A10/A100/H100)
    instances: null               # Min/max for autoscaling
    autoscale_metric: ""          # RPS | latency_p99 | GPU_utilization
    autoscale_target: null
  api:
    endpoint: ""
    input_schema: {}              # Pydantic model or JSON schema
    output_schema: {}
    timeout_ms: null
    rate_limit: null
  reliability:
    health_check: "/health"
    readiness_check: "/ready"     # Model loaded and warm
    graceful_shutdown: true
    circuit_breaker: true
    fallback: ""                  # Rules-based fallback when model is down
```

### 容器化模板

```dockerfile
# Multi-stage build for minimal image
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY model/ ./model/
COPY src/ ./src/

# Non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080
CMD ["uvicorn", "src.serve:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 模型的A/B测试

```yaml
ab_test:
  name: ""
  hypothesis: ""
  primary_metric: ""              # Business metric (revenue, engagement, etc.)
  guardrail_metrics: []           # Metrics that must NOT degrade
  traffic_split:
    control: 50                   # Current model
    treatment: 50                 # New model
  minimum_sample_size: null       # Power analysis: use statsmodels or online calculator
  minimum_runtime_days: null      # At least 1 full business cycle (7 days min)
  decision_criteria:
    ship: "Treatment > control by >X% with p<0.05 AND no guardrail regression"
    iterate: "Promising signal but not significant — extend test or refine model"
    kill: "No improvement after 2x minimum runtime OR guardrail breach"
```

---

## 第6阶段：大型语言模型（LLM）工程

### LLM应用架构

```
┌─────────────────────────────────────────────┐
│              Application Layer               │
│  (Prompt templates, chains, output parsers)  │
├─────────────────────────────────────────────┤
│              Orchestration Layer              │
│  (Routing, fallback, retry, caching)         │
├─────────────────────────────────────────────┤
│              Model Layer                     │
│  (API calls, fine-tuned models, embeddings)  │
├─────────────────────────────────────────────┤
│              Data Layer                      │
│  (Vector store, context retrieval, memory)   │
└─────────────────────────────────────────────┘
```

### LLM任务的模型选择

| 任务 | 最佳选择 | 成本效益较高的选择 | 何时进行微调 |
|------|------------|----------------------|-------------------|
| 通用推理 | Claude Opus / GPT-4o | Claude Sonnet / GPT-4o-mini | 通用推理任务不建议使用 |
| 分类 | 使用微调后的小型模型 | 使用Sonnet进行少量样本的微调 | 数据量较大且需要精确分类时 |
| 提取信息 | 使用结构化输出API | 使用正则表达式结合LLM作为备用方案 | 需要一致的输出格式 |
| 摘要生成 | 使用Claude Sonnet | 使用GPT-4o-mini | 需要特定领域的风格 |
| 代码生成 | 使用Claude Sonnet | 使用Codestral / DeepSeek | 需要符合内部代码库规范 |
| 嵌入式表示 | 使用text-embedding-3-large | 使用text-embedding-3-small | 需要特定领域的词汇表 |

### 问答系统（RAG）架构

```yaml
rag_pipeline:
  ingestion:
    chunking:
      strategy: "semantic"         # semantic | fixed_size | recursive
      chunk_size: 512              # tokens (512-1024 for most use cases)
      overlap: 50                  # tokens overlap between chunks
      metadata_to_preserve:
        - source_document
        - page_number
        - section_heading
        - date_created
    embedding:
      model: "text-embedding-3-large"
      dimensions: 1536             # Or 256/512 with Matryoshka for cost savings
    vector_store: "Pinecone | Weaviate | pgvector | Qdrant"
  retrieval:
    strategy: "hybrid"             # dense | sparse | hybrid (recommended)
    top_k: 10                      # Retrieve more, then rerank
    reranking:
      model: "Cohere rerank | cross-encoder"
      top_n: 3                     # Final context chunks
    filters: []                    # Metadata filters (date range, source, etc.)
  generation:
    model: ""
    system_prompt: |
      Answer based ONLY on the provided context.
      If the context doesn't contain the answer, say "I don't have enough information."
      Cite sources using [Source: document_name, page X].
    temperature: 0.1               # Low for factual, higher for creative
    max_tokens: null
```

### RAG质量检查清单

- [ ] 分块处理能够保留语义意义（避免在句子中间截断） |
- [ ] 元数据支持过滤（包含日期、来源、类别等信息） |
- [ ] 检索结果包含相关内容（通过手动测试50多个查询进行验证） |
- [ ] 重新排序可以提高精确度（对比使用和不使用重新排序的情况） |
- [ ] 系统提示能够防止错误信息 | 使用对抗性查询进行测试 |
- [ ] 能够正确引用信息来源并验证其真实性 |
- [ ] 能够优雅地处理“不知道”的情况 |
- [ ] 响应时间可接受（交互式请求<3秒，复杂请求<30秒） |
- [ ] 记录每个查询的成本，并控制在预算范围内 |

### LLM成本优化

| 优化策略 | 节省成本 | 相关权衡 |
|----------|---------|-----------|
| 提示缓存 | 对于重复的查询，可以节省50-90%的成本 | 需要设计适合缓存的提示 |
| 模型路由（从小模型到大型模型） | 可以节省40-70%的成本 | 但可能会增加延迟，需要专门的路由逻辑 |
| 批量API | 可以节省50%的成本 | 适用于批量处理的工作负载 |
| 简化提示 | 可以节省成本 | 但可能会降低模型质量 |
| 微调后的小型模型 | 与大型模型相比，可以节省80-95%的成本 | 需要额外的训练和维护成本 |
| 语义缓存 | 对于相似的查询，可以节省50-80%的成本 | 但可能会返回过时或错误的缓存结果 |

### 第7阶段：模型监控

### 监控仪表板

```yaml
monitoring:
  model_performance:
    metrics:
      - name: "primary_metric"         # Same as offline evaluation
        threshold: null                 # Alert if below
        window: "1h | 1d | 7d"
      - name: "prediction_distribution"
        alert: "KL divergence > 0.1 from training distribution"
    latency:
      p50_ms: null
      p95_ms: null
      p99_ms: null
      alert_threshold_ms: null
    throughput:
      requests_per_second: null
      error_rate_threshold: 0.01       # Alert if >1% errors
  data_drift:
    method: "PSI | KS-test | JS-divergence"
    features_to_monitor: []            # Top 10 most important features
    check_frequency: "hourly | daily"
    alert_threshold: null              # PSI > 0.2 = significant drift
  concept_drift:
    method: "performance_degradation"
    ground_truth_delay: ""             # How long until we get labels?
    proxy_metrics: []                  # Metrics available before ground truth
    retraining_trigger: ""             # When to retrain
```

### 应对模型变化的策略

| 变化类型 | 检测方法 | 严重程度 | 应对措施 |
|------------|-----------|----------|----------|
| **特征变化**（输入分布变化） | PSI > 0.1 | 警告 | 调查原因并监控性能 |
| **特征变化**（PSI > 0.25） | PSI > 0.25 | 严重 | 在24小时内使用最新数据重新训练模型 |
| **概念变化**（模型关系变化） | 性能下降超过5% | 严重 | 使用新标签重新训练模型并审查特征 |
| **标签变化**（目标分布变化） | 卡方检验 | 警告 | 验证标签质量并检查数据问题 |
| **预测结果变化**（输出分布变化） | KL散度 | 警告 | 可能表明上游数据存在问题 |

### 自动化重新训练流程

```yaml
retraining:
  triggers:
    - type: "scheduled"
      frequency: "weekly | monthly"
    - type: "performance"
      condition: "primary_metric < threshold for 24h"
    - type: "drift"
      condition: "PSI > 0.2 on any top-10 feature"
  pipeline:
    1_data_validation:
      - check_completeness
      - check_distribution_shift
      - check_label_quality
    2_training:
      - use_latest_N_months_data
      - same_hyperparameters_as_production   # Unless scheduled tuning
      - log_all_metrics
    3_evaluation:
      - compare_vs_production_model
      - must_beat_production_on_primary_metric
      - must_not_regress_on_guardrail_metrics
      - evaluate_on_golden_test_set
    4_deployment:
      - canary_deployment: 5%
      - monitor_for: "4h minimum"
      - auto_rollback_if: "error_rate > 2x baseline"
      - gradual_rollout: "5% → 25% → 50% → 100%"
    5_notification:
      - log_retraining_event
      - notify_team_on_failure
      - update_model_registry
```

---

## 第8阶段：机器学习运维（MLOps）基础设施

### 机器学习平台组件

| 组件 | 功能 | 使用工具 |
|-----------|---------|-------|
| 实验跟踪 | 记录实验过程并比较结果 | MLflow, W&B, Neptune |
| 特征存储 | 集中式特征管理 | Feast, Tecton, Hopsworks |
| 模型注册 | 管理模型版本和阶段 | MLflow Registry, SageMaker |
| 工作流编排 | 基于DAG的工作流 | Airflow, Prefect, Dagster, Kubeflow |
| 模型服务 | 低延迟推理 | Triton, TorchServe, vLLM, BentoML |
| 监控 | 监控模型变化、性能和数据质量 | Evidently, Whylogs, Great Expectations |
| 向量存储 | 用于问答系统的嵌入存储 | Pinecone, Weaviate, pgvector, Qdrant |
| GPU管理 | 负责训练和推理计算 | K8s + GPU操作器, RunPod, Modal |

### 机器学习的持续集成/持续部署（CI/CD）流程

```yaml
ml_cicd:
  on_code_change:
    - lint_and_type_check
    - unit_tests (data transforms, feature logic)
    - integration_tests (pipeline end-to-end on sample data)
  on_data_change:
    - data_validation (Great Expectations / custom)
    - feature_pipeline_run
    - smoke_test_predictions
  on_model_change:
    - full_evaluation_suite
    - bias_and_fairness_check
    - performance_regression_test
    - model_size_and_latency_check
    - security_scan (model file, dependencies)
    - staging_deployment
    - integration_test_in_staging
    - approval_gate (manual for major versions)
    - canary_deployment
```

### 模型注册工作流程

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  Development │ ───→ │   Staging    │ ───→ │  Production  │
│              │      │              │      │              │
│ - Experiment │      │ - Eval suite │      │ - Canary     │
│ - Log metrics│      │ - Load test  │      │ - Monitor    │
│ - Compare    │      │ - Approval   │      │ - Rollback   │
└──────────────┘      └──────────────┘      └──────────────┘
```

**升级标准：**
- 从开发环境到测试环境：在离线指标上优于当前生产环境 |
- 从测试环境到生产环境：通过负载测试、集成测试和人工审核 |
- 自动回滚：如果错误率超过2倍或延迟超过2倍，或主要指标下降超过5%，则回滚模型 |

---

## 第9阶段：负责任的AI实践

### 偏见检测检查清单

- [ ] 训练数据能够按比例代表所有人口统计群体 |
- [ ] 按保护属性分解性能指标 |
- [ ] 确保不同群体之间的机会均等：真正正例率相似 |
- [ ] 进行校准：预测概率与实际概率相匹配 |
- [ ] 不使用代表保护属性的代理特征（例如邮政编码代表种族） |
- [ ] 在训练之前选择并定义公平性指标的阈值 |
- [ ] 不同情况的影响比率大于0.8（80%的规则） |
- [ ] 测试极端情况：测试不常见输入时的系统表现 |

### 模型卡片模板

```yaml
model_card:
  model_name: ""
  version: ""
  date: ""
  owner: ""
  description: ""
  intended_use: ""
  out_of_scope_uses: ""
  training_data:
    source: ""
    size: ""
    date_range: ""
    known_biases: ""
  evaluation:
    metrics: {}
    datasets: []
    sliced_metrics: {}             # Performance by subgroup
  limitations: []
  ethical_considerations: []
  maintenance:
    retraining_schedule: ""
    monitoring: ""
    contact: ""
```

---

## 第10阶段：成本与性能优化

### GPU选择指南

| 使用场景 | 推荐GPU | 推荐VRAM | 每小时成本（云服务） | 最适合的场景 |
|----------|-----|------|-----------------|----------|
| 微调70亿参数的模型 | A10G | 24GB | 约1美元 | 适用于LoRA/QLoRA微调 |
| 微调700亿参数的模型 | A100 80GB | 80GB | 约4美元 | 适用于中型模型的完整微调 |
| 服务70亿参数的模型 | T4 | 16GB | 约0.50美元 | 适用于大规模模型的推理 |
| 从头开始训练70亿参数的模型 | H100 | 80GB | 约8美元 | 适用于大规模模型的预训练 |

### 推理优化技术

| 技术 | 提高性能 | 对质量的影响 | 复杂度 |
|-----------|---------|---------------|------------|
| 量化（INT8） | 提高性能2-3倍 | 对质量影响小于1% | 复杂度低 |
| 量化（INT4/GPTQ） | 提高性能3-4倍 | 对质量影响1-3% | 复杂度中等 |
| 批量处理 | 提高性能2-10倍 | 对质量影响较小 | 复杂度低 |
| KV缓存 | 可节省20-40%的内存 | 复杂度中等 |
| 推测解码 | 对LLM模型有2-3倍的性能提升 | 复杂度较高 |
| 模型蒸馏 | 可将模型大小缩小5-10倍 | 复杂度较高 |
| ONNX运行时 | 对LLM模型有1.5-3倍的性能提升 | 复杂度较高 |
| TensorRT | 对LLM模型有2-5倍的性能提升 | 复杂度较高 |

### 成本跟踪模板

```yaml
ml_costs:
  training:
    compute_cost_per_run: null
    runs_per_month: null
    data_storage_monthly: null
    experiment_tracking: null
  inference:
    cost_per_1k_predictions: null
    daily_volume: null
    monthly_cost: null
    cost_per_query_breakdown:
      compute: null
      model_api_calls: null
      vector_db: null
      data_transfer: null
  optimization_targets:
    cost_per_prediction: null      # Target
    monthly_budget: null
    cost_reduction_goal: ""
```

---

## 第11阶段：机器学习系统质量评估

对机器学习系统进行评分（0-100分）：

| 评估维度 | 权重 | 0-2分（较差） | 3-4分（良好） | 5分（优秀） |
|-----------|--------|-----------|------------|----------------|
| **问题定义** | 15% | 没有明确的业务指标 | 有明确的成功指标 | 有终止条件、基线和成本效益估算 |
| **数据质量** | 15% | 使用临时数据，未进行验证 | 有自动化的质量检查 | 有特征存储、版本控制和版本管理 |
| **实验严谨性** | 15% | 无跟踪机制，仅使用一次性脚本 | 有MLflow/W&B进行跟踪 | 有可复制的流程和适当的评估 |
| **模型性能** | 15% | 性能仅略优于基线 | 有显著的改进 | 经过校准，公平且能应对极端情况 |
| **部署** | 15% | 依赖手动部署 | 使用CI/CD进行模型部署 | 有自动回滚和A/B测试 |
| **监控** | 15% | 无监控机制 | 仅使用基本指标仪表板 | 有偏差检测和自动重新训练机制 |
| **文档记录** | 5% | 无文档记录 | 有完整的模型卡片和运行手册 | |
| **成本效率** | 10% | 无成本跟踪 | 有成本预算 | 有优化的推理流程和成本跟踪 |

**评分标准：**
- 80-100分：达到生产级质量的机器学习系统 |
- 60-79分：基础较好，但缺乏运营成熟度 |
- 40-59分：处于原型阶段，尚未准备好投入生产 |
- 40分以下：属于科学研究项目，需要进一步改进 |

---

## 常见错误

| 错误 | 应对措施 |
|---------|-----|
| 在未处理数据之前就优化模型 | 数据质量比模型复杂性更重要。务必先处理数据 |
| 在不平衡数据上使用准确性指标 | 应使用PR-AUC、F1分数或特定领域的指标 |
| 未设置基准对比 | 必须先使用简单的启发式方法作为基准 |
| 在使用未来数据训练模型 | 对于时间序列数据，使用时间分割；进行严格的泄露检查 |
| 未经监控就进行部署 | 在生产环境中部署模型之前必须进行偏差检测 |
| 在提示效果良好时就进行微调 | 先尝试少量样本的提示方法；仅在需要扩展或优化成本时进行微调 |
| 对所有场景都使用GPU | 对于大多数任务，CPU推理通常足够且成本更低 |
| 忽视校准 | 如果概率预测很重要，必须进行校准 |
| 一次性部署模型 | 机器学习是一个持续优化的过程，从第一天起就应计划重新训练 |

---

## 快速命令

- “定义机器学习问题” → 执行第1阶段的任务 |
- “评估数据质量” → 执行第2阶段的操作 |
- “选择模型” → 执行第3阶段的操作 |
- “评估模型” → 执行第4阶段的操作 |
- “部署模型” → 执行第5阶段的操作 |
- “构建问答系统” → 执行第6阶段的操作 |
- “设置监控机制” → 执行第7阶段的操作 |
- “优化成本” → 执行第10阶段的操作 |
- “评估机器学习系统” → 执行第11阶段的操作 |
- “检测模型变化” → 执行第7阶段的操作 |
- “进行A/B测试” → 执行第5阶段的操作 |
- “创建模型卡片” → 执行第9阶段的操作 |