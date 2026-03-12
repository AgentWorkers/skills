---
name: "senior-ml-engineer"
description: 这是一份关于机器学习（ML）工程技能的文档，主要涵盖了将模型部署到生产环境、构建机器学习运维（MLOps）管道以及集成大型语言模型（LLMs）的相关内容。内容包括模型部署、特征存储、模型性能监控、检索与生成（RAG）系统以及成本优化等方面的知识。当用户需要了解如何将机器学习模型部署到生产环境中、如何搭建MLOps基础设施（如MLflow、Kubeflow、Kubernetes、Docker），或者如何监控模型性能或模型漂移情况，以及如何构建包含重试逻辑和成本控制功能的RAG管道时，可以参考本文档。本文档的重点在于生产环境和运维方面的实际操作，而非模型的研究或初始训练过程。
triggers:
  - MLOps pipeline
  - model deployment
  - feature store
  - model monitoring
  - drift detection
  - RAG system
  - LLM integration
  - model serving
  - A/B testing ML
  - automated retraining
---
# 高级机器学习工程师

负责模型部署、机器学习运维（MLOps）基础设施以及大型语言模型（LLM）集成的生产环境相关技术工作。

---

## 目录

- [模型部署工作流程](#model-deployment-workflow)
- [MLOps 流程设置](#mlops-pipeline-setup)
- [LLM 集成工作流程](#llm-integration-workflow)
- [RAG 系统实现](#rag-system-implementation)
- [模型监控](#model-monitoring)
- [参考文档](#reference-documentation)
- [工具](#tools)

---

## 模型部署工作流程

将训练好的模型部署到生产环境，并进行监控：

1. 将模型导出为标准化格式（ONNX、TorchScript、SavedModel）
2. 将模型及其依赖项打包到 Docker 容器中
3. 部署到预发布环境（staging）
4. 在预发布环境中运行集成测试
5. 部署少量流量（5%）到生产环境
6. 监控延迟和错误率，持续 1 小时
7. 如果指标符合要求，将模型推广到全生产环境
8. **验证标准：** p95 延迟 < 100ms，错误率 < 0.1%

### 容器模板

```dockerfile
FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY model/ /app/model/
COPY src/ /app/src/

HEALTHCHECK CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 服务选项

| 选项 | 延迟 | 吞吐量 | 适用场景 |
|--------|---------|------------|----------|
| FastAPI + Uvicorn | 低 | 中等 | REST API，小型模型 |
| Triton 推理服务器 | 极低 | 非常高 | GPU 推理，批量处理 |
| TensorFlow Serving | 低 | 高 | TensorFlow 模型 |
| TorchServe | 低 | 高 | PyTorch 模型 |
| Ray Serve | 中等 | 高 | 复杂的管道，多模型 |

---

## MLOps 流程设置

建立自动化的训练和部署流程：

1. 配置特征存储系统（Feast、Tecton）以存储训练数据
2. 设置实验跟踪工具（MLflow、Weights & Biases）
3. 创建包含超参数记录的训练流程
4. 将模型及其元数据注册到模型注册表中
5. 配置基于注册表事件触发的预发布环境部署
6. 建立 A/B 测试基础设施以比较不同模型
7. 启用漂移监控并设置警报
8. **验证标准：** 新模型自动与基线进行评估

### 特征存储系统模式

```python
from feast import Entity, Feature, FeatureView, FileSource

user = Entity(name="user_id", value_type=ValueType.INT64)

user_features = FeatureView(
    name="user_features",
    entities=["user_id"],
    ttl=timedelta(days=1),
    features=[
        Feature(name="purchase_count_30d", dtype=ValueType.INT64),
        Feature(name="avg_order_value", dtype=ValueType.FLOAT),
    ],
    online=True,
    source=FileSource(path="data/user_features.parquet"),
)
```

### 重新训练触发条件

| 触发条件 | 检测内容 | 处理方式 |
|---------|-----------|--------|
| 定期 | Cron（每周/每月） | 完整重新训练 |
| 性能下降 | 准确率低于阈值 | 立即重新训练 |
| 数据漂移 | PSI > 0.2 | 评估后重新训练 |
| 新数据量 | 新样本数量 | 增量更新 |

---

## LLM 集成工作流程

将 LLM API 集成到生产应用程序中：

1. 创建提供者抽象层，以增加灵活性
2. 实现带有指数退避机制的重试逻辑
3. 配置备用提供者
4. 设置令牌计数和上下文截断机制
5. 为重复请求添加响应缓存
6. 实现按请求计费的成本跟踪
7. 使用 Pydantic 进行结构化输出验证
8. **验证标准：** 响应正确解析，成本在预算范围内

### 提供者抽象层

```python
from abc import ABC, abstractmethod
from tenacity import retry, stop_after_attempt, wait_exponential

class LLMProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str, **kwargs) -> str:
        pass

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def call_llm_with_retry(provider: LLMProvider, prompt: str) -> str:
    return provider.complete(prompt)
```

### 成本管理

| 提供者 | 输入成本 | 输出成本 |
|----------|------------|-------------|
| GPT-4 | $0.03/1K | $0.06/1K |
| GPT-3.5 | $0.0005/1K | $0.0015/1K |
| Claude 3 Opus | $0.015/1K | $0.075/1K |
| Claude 3 Haiku | $0.00025/1K | $0.00125/1K |

---

## RAG 系统实现

构建检索增强生成（Retrieval-Augmented Generation）管道：

1. 选择向量数据库（Pinecone、Qdrant、Weaviate）
2. 根据质量和成本权衡选择嵌入模型
3. 实现文档分块策略
4. 创建包含元数据提取的导入管道
5. 使用查询嵌入进行检索
6. 添加重新排序以提高相关性
7. 格式化上下文并发送给 LLM
8. **验证标准：** 响应正确引用检索到的上下文，无幻觉现象

### 向量数据库选择

| 数据库 | 托管方式 | 可扩展性 | 延迟 | 适用场景 |
|----------|---------|-------|---------|----------|
| Pinecone | 托管服务 | 高 | 低 | 生产环境，需要管理 |
| Qdrant | 自托管/托管服务 | 高 | 非常低 | 对性能要求高的场景 |
| Weaviate | 自托管/托管服务 | 高 | 低 | 混合搜索 |
| Chroma | 自托管 | 中等 | 低 | 适用于原型开发 |
| pgvector | 自托管 | 中等 | 中等 | 需要与现有 PostgreSQL 集成 |

### 分块策略

| 策略 | 分块大小 | 重叠比例 | 适用场景 |
|----------|------------|---------|----------|
| 固定大小 | 500-1000 个令牌 | 50-100 | 通用文本 |
| 句子级 | 3-5 句子 | 单个句子 | 结构化文本 |
| 语义分块 | 动态分配 | 基于语义 | 研究论文 |
| 递归分块 | 层次化 | 父子结构 | 长文档 |

---

## 模型监控

监控生产环境中的模型是否出现漂移或性能下降：

1. 设置延迟跟踪指标（p50、p95、p99）
2. 配置错误率警报
3. 实现输入数据漂移检测
4. 跟踪预测分布的变化
5. 在有真实数据时记录基准值
6. 使用 A/B 测试指标比较不同模型版本
7. 设置自动重新训练的触发条件
8. **验证标准：** 在用户可见的性能下降之前触发警报

### 漂移检测

```python
from scipy.stats import ks_2samp

def detect_drift(reference, current, threshold=0.05):
    statistic, p_value = ks_2samp(reference, current)
    return {
        "drift_detected": p_value < threshold,
        "ks_statistic": statistic,
        "p_value": p_value
    }
```

### 警报阈值

| 指标 | 警报级别 | 严重程度 |
|--------|---------|----------|
| p95 延迟 | > 100ms | > 200ms |
| 错误率 | > 0.1% | > 1% |
| 数据漂移（PSI） | > 0.1 | > 0.2 |
| 准确率下降 | > 2% | > 5% |

---

## 参考文档

### MLOps 生产模式

`references/mlops_production_patterns.md` 包含：

- 使用 Kubernetes 替换脚本的模型部署流程
- 带有 Feast 示例的特征存储系统架构
- 包含漂移检测代码的模型监控机制
- 带有流量分割功能的 A/B 测试基础设施
- 使用 MLflow 的自动重新训练流程

### LLM 集成指南

`references/llm_integration_guide.md` 包含：

- 提供者抽象层的设计模式
- 带有重试和备用策略的实现
- 提示工程模板（少样本任务、CoT）
- 令牌优化方法（使用 tiktoken）
- 成本计算和跟踪机制

### RAG 系统架构

`references/rag_system_architecture.md` 包含：

- RAG 管道的实现代码
- 向量数据库的比较和集成方法
- 分块策略（固定大小、语义分块、递归分块）
- 嵌入模型选择指南
- 混合搜索和重新排序的实现方式

---

## 工具

### 模型部署流程

```bash
python scripts/model_deployment_pipeline.py --model model.pkl --target staging
```

生成部署所需的文件：Dockerfile、Kubernetes 替换脚本。

### RAG 系统构建工具

```bash
python scripts/rag_system_builder.py --config rag_config.yaml --analyze
```

用于构建包含向量存储和检索逻辑的 RAG 管道。

### ML 监控工具套件

```bash
python scripts/ml_monitoring_suite.py --config monitoring.yaml --deploy
```

设置漂移检测、警报功能以及性能监控仪表板。

---

## 技术栈

| 类别 | 使用工具 |
|----------|-------|
| 机器学习框架 | PyTorch、TensorFlow、Scikit-learn、XGBoost |
| LLM 框架 | LangChain、LlamaIndex、DSPy |
| 机器学习运维工具 | MLflow、Weights & Biases、Kubeflow |
| 数据处理工具 | Spark、Airflow、dbt、Kafka |
| 部署工具 | Docker、Kubernetes、Triton |
| 数据库 | PostgreSQL、BigQuery、Pinecone、Redis |