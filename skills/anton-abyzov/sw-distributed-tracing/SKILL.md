---
name: distributed-tracing
description: 使用 Jaeger 和 Tempo 实现分布式追踪功能，以跟踪跨微服务的请求并识别性能瓶颈。该功能适用于调试微服务、分析请求流，或为分布式系统提供可观测性（observability）支持。
---

# 分布式追踪

使用 Jaeger 和 Tempo 实现分布式追踪，以便在微服务之间可视化请求流程。

## 目的

跟踪分布式系统中的请求，以了解延迟、依赖关系和故障点。

## 适用场景

- 调试延迟问题
- 了解服务之间的依赖关系
- 识别瓶颈
- 追踪错误传播路径
- 分析请求路径

## 分布式追踪概念

### 追踪结构
```
Trace (Request ID: abc123)
  ↓
Span (frontend) [100ms]
  ↓
Span (api-gateway) [80ms]
  ├→ Span (auth-service) [10ms]
  └→ Span (user-service) [60ms]
      └→ Span (database) [40ms]
```

### 关键组件
- **Trace**（追踪）：端到端的请求流程
- **Span**（跨度）：追踪中的单个操作
- **Context**（上下文）：在服务之间传递的元数据
- **Tags**（标签）：用于过滤的键值对
- **Logs**（日志）：跨度内的带时间戳的事件

## Jaeger 的配置与部署

### 在 Kubernetes 中部署
```bash
# Deploy Jaeger Operator
kubectl create namespace observability
kubectl create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.51.0/jaeger-operator.yaml -n observability

# Deploy Jaeger instance
kubectl apply -f - <<EOF
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: jaeger
  namespace: observability
spec:
  strategy: production
  storage:
    type: elasticsearch
    options:
      es:
        server-urls: http://elasticsearch:9200
  ingress:
    enabled: true
EOF
```

### 使用 Docker Compose 部署
```yaml
version: '3.8'
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "5775:5775/udp"
      - "6831:6831/udp"
      - "6832:6832/udp"
      - "5778:5778"
      - "16686:16686"  # UI
      - "14268:14268"  # Collector
      - "14250:14250"  # gRPC
      - "9411:9411"    # Zipkin
    environment:
      - COLLECTOR_ZIPKIN_HOST_PORT=:9411
```

## 应用程序的追踪集成

### OpenTelemetry（推荐）

#### Python（Flask）
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from flask import Flask

# Initialize tracer
resource = Resource(attributes={SERVICE_NAME: "my-service"})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Instrument Flask
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route('/api/users')
def get_users():
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("get_users") as span:
        span.set_attribute("user.count", 100)
        # Business logic
        users = fetch_users_from_db()
        return {"users": users}

def fetch_users_from_db():
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("database_query") as span:
        span.set_attribute("db.system", "postgresql")
        span.set_attribute("db.statement", "SELECT * FROM users")
        # Database query
        return query_database()
```

#### Node.js（Express）
```javascript
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');
const { BatchSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { registerInstrumentations } = require('@opentelemetry/instrumentation');
const { HttpInstrumentation } = require('@opentelemetry/instrumentation-http');
const { ExpressInstrumentation } = require('@opentelemetry/instrumentation-express');

// Initialize tracer
const provider = new NodeTracerProvider({
  resource: { attributes: { 'service.name': 'my-service' } }
});

const exporter = new JaegerExporter({
  endpoint: 'http://jaeger:14268/api/traces'
});

provider.addSpanProcessor(new BatchSpanProcessor(exporter));
provider.register();

// Instrument libraries
registerInstrumentations({
  instrumentations: [
    new HttpInstrumentation(),
    new ExpressInstrumentation(),
  ],
});

const express = require('express');
const app = express();

app.get('/api/users', async (req, res) => {
  const tracer = trace.getTracer('my-service');
  const span = tracer.startSpan('get_users');

  try {
    const users = await fetchUsers();
    span.setAttributes({ 'user.count': users.length });
    res.json({ users });
  } finally {
    span.end();
  }
});
```

#### Go
```go
package main

import (
    "context"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/jaeger"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.4.0"
)

func initTracer() (*sdktrace.TracerProvider, error) {
    exporter, err := jaeger.New(jaeger.WithCollectorEndpoint(
        jaeger.WithEndpoint("http://jaeger:14268/api/traces"),
    ))
    if err != nil {
        return nil, err
    }

    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceNameKey.String("my-service"),
        )),
    )

    otel.SetTracerProvider(tp)
    return tp, nil
}

func getUsers(ctx context.Context) ([]User, error) {
    tracer := otel.Tracer("my-service")
    ctx, span := tracer.Start(ctx, "get_users")
    defer span.End()

    span.SetAttributes(attribute.String("user.filter", "active"))

    users, err := fetchUsersFromDB(ctx)
    if err != nil {
        span.RecordError(err)
        return nil, err
    }

    span.SetAttributes(attribute.Int("user.count", len(users)))
    return users, nil
}
```

## 上下文传递

### HTTP 请求头
```
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
tracestate: congo=t61rcWkgMzE
```

### 在 HTTP 请求中传递上下文

#### Python
```python
from opentelemetry.propagate import inject

headers = {}
inject(headers)  # Injects trace context

response = requests.get('http://downstream-service/api', headers=headers)
```

#### Node.js
```javascript
const { propagation } = require('@opentelemetry/api');

const headers = {};
propagation.inject(context.active(), headers);

axios.get('http://downstream-service/api', { headers });
```

## Tempo 的配置与部署（用于 Grafana）

### 在 Kubernetes 中部署
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: tempo-config
data:
  tempo.yaml: |
    server:
      http_listen_port: 3200

    distributor:
      receivers:
        jaeger:
          protocols:
            thrift_http:
            grpc:
        otlp:
          protocols:
            http:
            grpc:

    storage:
      trace:
        backend: s3
        s3:
          bucket: tempo-traces
          endpoint: s3.amazonaws.com

    querier:
      frontend_worker:
        frontend_address: tempo-query-frontend:9095
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tempo
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: tempo
        image: grafana/tempo:latest
        args:
          - -config.file=/etc/tempo/tempo.yaml
        volumeMounts:
        - name: config
          mountPath: /etc/tempo
      volumes:
      - name: config
        configMap:
          name: tempo-config
```

**参考：**请查看 `assets/jaeger-config.yaml.template`

## 采样策略

### 概率采样
```yaml
# Sample 1% of traces
sampler:
  type: probabilistic
  param: 0.01
```

### 限速采样
```yaml
# Sample max 100 traces per second
sampler:
  type: ratelimiting
  param: 100
```

### 自适应采样
```python
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased

# Sample based on trace ID (deterministic)
sampler = ParentBased(root=TraceIdRatioBased(0.01))
```

## 追踪分析

### 查找响应缓慢的请求

**Jaeger 查询：**
```
service=my-service
duration > 1s
```

### 查找错误

**Jaeger 查询：**
```
service=my-service
error=true
tags.http.status_code >= 500
```

### 服务依赖关系图

Jaeger 会自动生成服务依赖关系图，显示：
- 服务之间的关系
- 请求频率
- 错误率
- 平均延迟

## 最佳实践

1. **适当采样**（在生产环境中建议采样率为 1-10%）
2. **添加有意义的标签**（如 user_id、request_id）
3. **在所有服务边界之间传递上下文**
4. **在跨度中记录异常信息**
5. **为操作使用统一的命名规范**
6. **监控追踪带来的开销**（确保 CPU 使用率低于 1%）
7. **为追踪错误设置警报**
8. **实现分布式上下文传递**
9. **使用跨度事件来标记重要节点**
10. **记录追踪集成的标准**

## 与日志系统的集成

### 相关日志
```python
import logging
from opentelemetry import trace

logger = logging.getLogger(__name__)

def process_request():
    span = trace.get_current_span()
    trace_id = span.get_span_context().trace_id

    logger.info(
        "Processing request",
        extra={"trace_id": format(trace_id, '032x')}
    )
```

## 故障排除

**没有追踪记录出现：**
- 检查收集器端点是否正常工作
- 确认网络连接是否正常
- 检查采样配置
- 查看应用程序日志

**延迟过高：**
- 降低采样率
- 使用批量处理跨度数据的工具
- 检查数据导出器的配置

## 相关技能

- `prometheus-configuration`：用于指标收集
- `grafana-dashboards`：用于数据可视化
- `slo-implementation`：用于设置延迟服务水平目标（SLOs）