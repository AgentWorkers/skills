---
name: ml-deployment-helper
description: |
  Prepares ML models for production deployment with containerization, API creation, monitoring setup, and A/B testing. Activates for "deploy model", "production deployment", "model API", "containerize model", "docker ml", "serving ml model", "model monitoring", "A/B test model". Generates deployment artifacts and ensures models are production-ready with monitoring, versioning, and rollback capabilities.
---

# 机器学习部署辅助工具

## 概述

本工具旨在弥合训练好的模型与生产系统之间的差距，遵循机器学习运维（MLOps）的最佳实践，生成部署所需的文件、API、监控系统以及A/B测试基础设施。

## 部署检查清单

在部署任何模型之前，本工具会确保以下事项：
- ✅ 模型已进行版本化管理并可供追踪
- ✅ 依赖关系已记录（requirements.txt/Dockerfile）
- ✅ API端点已创建
- ✅ 输入验证机制已实现
- ✅ 监控系统已配置
- ✅ A/B测试环境已准备就绪
- ✅ 回滚计划已文档化
- ✅ 模型性能已进行基准测试

## 部署模式

### 模式1：REST API（FastAPI）

```python
from specweave import create_model_api

# Generates production-ready API
api = create_model_api(
    model_path="models/model-v3.pkl",
    increment="0042",
    framework="fastapi"
)

# Creates:
# - api/
#   ├── main.py (FastAPI app)
#   ├── models.py (Pydantic schemas)
#   ├── predict.py (Prediction logic)
#   ├── Dockerfile
#   ├── requirements.txt
#   └── tests/
```

生成的 `main.py` 文件：
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

app = FastAPI(title="Recommendation Model API", version="0042-v3")

model = joblib.load("model-v3.pkl")

class PredictionRequest(BaseModel):
    user_id: int
    context: dict

@app.post("/predict")
async def predict(request: PredictionRequest):
    try:
        prediction = model.predict([request.dict()])
        return {
            "recommendations": prediction.tolist(),
            "model_version": "0042-v3",
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": model is not None}
```

### 模式2：批量预测

```python
from specweave import create_batch_predictor

# For offline scoring
batch_predictor = create_batch_predictor(
    model_path="models/model-v3.pkl",
    increment="0042",
    input_path="s3://bucket/data/",
    output_path="s3://bucket/predictions/"
)

# Creates:
# - batch/
#   ├── predictor.py
#   ├── scheduler.yaml (Airflow/Kubernetes CronJob)
#   └── monitoring.py
```

### 模式3：实时流处理

```python
from specweave import create_streaming_predictor

# For Kafka/Kinesis streams
streaming = create_streaming_predictor(
    model_path="models/model-v3.pkl",
    increment="0042",
    input_topic="user-events",
    output_topic="predictions"
)

# Creates:
# - streaming/
#   ├── consumer.py
#   ├── predictor.py
#   ├── producer.py
#   └── docker-compose.yaml
```

## 容器化

```python
from specweave import containerize_model

# Generates optimized Dockerfile
dockerfile = containerize_model(
    model_path="models/model-v3.pkl",
    framework="sklearn",
    python_version="3.10",
    increment="0042"
)
```

生成的 `Dockerfile` 文件：
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy model and dependencies
COPY models/model-v3.pkl /app/model.pkl
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY api/ /app/api/

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

# Run API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 监控系统设置

```python
from specweave import setup_model_monitoring

# Configures monitoring for production
monitoring = setup_model_monitoring(
    model_name="recommendation-model",
    increment="0042",
    metrics=[
        "prediction_latency",
        "throughput",
        "error_rate",
        "prediction_distribution",
        "feature_drift"
    ]
)

# Creates:
# - monitoring/
#   ├── prometheus.yaml
#   ├── grafana-dashboard.json
#   ├── alerts.yaml
#   └── drift-detector.py
```

## A/B测试基础设施

```python
from specweave import create_ab_test

# Sets up A/B test framework
ab_test = create_ab_test(
    control_model="model-v2.pkl",
    treatment_model="model-v3.pkl",
    traffic_split=0.1,  # 10% to new model
    success_metric="click_through_rate",
    increment="0042"
)

# Creates:
# - ab-test/
#   ├── router.py (traffic splitting)
#   ├── metrics.py (success tracking)
#   ├── statistical-tests.py (significance testing)
#   └── dashboard.py (real-time monitoring)
```

A/B测试路由器：
```python
import random

def route_prediction(user_id, control_model, treatment_model):
    """Route to control or treatment based on user_id hash"""
    
    # Consistent hashing (same user always gets same model)
    user_bucket = hash(user_id) % 100
    
    if user_bucket < 10:  # 10% to treatment
        return treatment_model.predict(features), "treatment"
    else:
        return control_model.predict(features), "control"
```

## 模型版本管理

```python
from specweave import ModelVersion

# Register model version
version = ModelVersion.register(
    model_path="models/model-v3.pkl",
    increment="0042",
    metadata={
        "accuracy": 0.87,
        "training_date": "2024-01-15",
        "data_version": "v2024-01",
        "framework": "xgboost==1.7.0"
    }
)

# Easy rollback
if production_metrics["error_rate"] > threshold:
    ModelVersion.rollback(to_version="0042-v2")
```

## 负载测试

```python
from specweave import load_test_model

# Benchmark model performance
results = load_test_model(
    api_url="http://localhost:8000/predict",
    requests_per_second=[10, 50, 100, 500, 1000],
    duration_seconds=60,
    increment="0042"
)
```

## 部署命令

```bash
# Generate deployment artifacts
/ml:deploy-prepare 0042

# Create API
/ml:create-api --increment 0042 --framework fastapi

# Setup monitoring
/ml:setup-monitoring 0042

# Create A/B test
/ml:create-ab-test --control v2 --treatment v3 --split 0.1

# Load test
/ml:load-test 0042 --rps 100 --duration 60s

# Deploy to production
/ml:deploy 0042 --environment production
```

## 部署增量

本工具支持创建模型的部署增量版本：
```
.specweave/increments/0043-deploy-recommendation-model/
├── spec.md (deployment requirements)
├── plan.md (deployment strategy)
├── tasks.md
│   ├── [ ] Containerize model
│   ├── [ ] Create API
│   ├── [ ] Setup monitoring
│   ├── [ ] Configure A/B test
│   ├── [ ] Load test
│   ├── [ ] Deploy to staging
│   ├── [ ] Validate staging
│   └── [ ] Deploy to production
├── api/ (FastAPI app)
├── monitoring/ (Grafana dashboards)
├── ab-test/ (A/B testing logic)
└── load-tests/ (Performance benchmarks)
```

## 最佳实践

1. **在生产环境部署前务必进行负载测试**
2. **在A/B测试中从1-5%的流量开始测试**
3. **在生产环境中监控模型的性能变化**
4. **对所有组件（模型、数据、代码）进行版本化管理**
5. **在部署前详细记录回滚计划**
6. **为异常情况设置警报机制**
7. **采用渐进式部署策略（例如“金丝雀部署”）

## 与SpecWeave的集成

```bash
# After training model (increment 0042)
/sw:inc "0043-deploy-recommendation-model"

# Generates deployment increment with all artifacts
/sw:do

# Deploy to production when ready
/ml:deploy 0043 --environment production
```

模型部署仅仅是机器学习运维生命周期的开始，而非终点。