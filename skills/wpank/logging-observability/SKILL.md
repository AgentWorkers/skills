---
name: logging-observability
model: standard
description: 结构化日志记录、分布式追踪以及指标收集方法，用于构建可观测的系统。适用于实现日志基础设施、使用 OpenTelemetry 设置分布式追踪、设计指标收集方案（RED/USE 方法）、配置警报和仪表板，或审查可观测性实践。内容涵盖结构化 JSON 日志记录、上下文传播、追踪采样、Prometheus/Grafana 技术栈、警报设计，以及个人身份信息（PII）和敏感数据的保护措施。
version: 1.0.0
---

# 日志记录与可观测性

构建可观测系统的模式涵盖了三个核心要素：日志（logs）、指标（metrics）和跟踪（traces）。

## 三个核心要素

| 核心要素 | 目的 | 解决的问题 | 示例 |
|--------|---------|---------------------|---------|
| **日志** | 发生了什么 | 为什么这个请求会失败？ | `{"level":"error","msg":"payment declined","user_id":"u_82"}` |
| **指标** | 效率如何 | 延迟是否在增加？ | `http_request_duration_seconds{route="/api/orders"} 0.342` |
| **跟踪** | 请求流程 | 瓶颈在哪里？ | 跟踪路径：`api-gateway → auth → order-service → db` |

当这三个要素相互关联时，系统的可观测性会得到显著提升。在每条日志记录中嵌入 `trace_id`，以便能够从日志条目快速跳转到完整的分布式跟踪信息。

---

## 结构化日志记录

始终以结构化 JSON 的形式记录日志——切勿使用纯文本字符串。

### 必需字段

| 字段 | 目的 | 是否必需 |
|-------|---------|----------|
| `timestamp` | ISO-8601 格式的时间戳（包含毫秒） | 是 |
| `level` | 错误级别（DEBUG … FATAL） | 是 |
| `service` | 发起请求的服务名称 | 是 |
| `message` | 人类可读的描述 | 是 |
| `trace_id` | 分布式跟踪的关联信息 | 是 |
| `span_id` | 当前跟踪中的片段ID | 是 |
| `correlation_id` | 业务级别的关联信息（如订单ID） | 如适用 |
| `error` | 结构化的错误信息 | 发生错误时使用 |
| `context` | 与请求相关的元数据 | 建议包含 |

### 上下文丰富化

在中间件层添加上下文信息，以便下游日志能够自动继承这些信息：

```typescript
app.use((req, res, next) => {
  const ctx = {
    trace_id: req.headers['x-trace-id'] || crypto.randomUUID(),
    request_id: crypto.randomUUID(),
    user_id: req.user?.id,
    method: req.method,
    path: req.path,
  };
  asyncLocalStorage.run(ctx, () => next());
});
```

### 推荐使用的日志库

| 库名 | 使用语言 | 优点 | 性能 |
|---------|----------|-----------|------|
| **Pino** | Node.js | 最快速的 Node.js 日志库，开销低 | 表现优异 |
| **structlog** | Python | 可组合的处理逻辑，支持上下文绑定 | 性能良好 |
| **zerolog** | Go | 零内存占用的 JSON 日志记录方式 | 非常高效 |
| **zap** | Go | 高性能，字段类型化 | 性能优秀 |
| **tracing** | Rust | 支持跟踪和事件处理，支持异步操作 | 功能强大 |

选择能够原生输出结构化 JSON 的日志库。避免使用需要后续处理的日志库。

---

## 日志级别

| 级别 | 使用场景 | 示例 |
|-------|-------------|---------|
| **FATAL** | 应用程序无法继续运行，进程将终止 | 数据库连接池已耗尽 |
| **ERROR** | 操作失败，需要立即处理 | 支付请求失败：`CARD_DECLINED` |
| **WARN** | 意外情况，但可以恢复 | 上游请求超时，尝试重试2-3次 |
| **INFO** | 正常的业务事件 | 订单 ORD-1234 成功放置 |
| **DEBUG** | 开发者用于调试 | 用户偏好设置缓存未命中 |

**规则：** 生产环境默认使用 INFO 级别及以上的日志。如果记录了 ERROR 级别的日志，必须有人采取行动。所有 FATAL 级别的日志都应触发警报。

---

## 分布式跟踪

### OpenTelemetry 的设置

始终优先选择 OpenTelemetry，而非特定供应商提供的 SDK：

```typescript
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';

const sdk = new NodeSDK({
  serviceName: 'order-service',
  traceExporter: new OTLPTraceExporter({
    url: 'http://otel-collector:4318/v1/traces',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});
sdk.start();
```

### 跟踪片段的创建

```typescript
const tracer = trace.getTracer('order-service');

async function processOrder(order: Order) {
  return tracer.startActiveSpan('processOrder', async (span) => {
    try {
      span.setAttribute('order.id', order.id);
      span.setAttribute('order.total_cents', order.totalCents);
      await validateInventory(order);
      await chargePayment(order);
      span.setStatus({ code: SpanStatusCode.OK });
    } catch (err) {
      span.setStatus({ code: SpanStatusCode.ERROR, message: err.message });
      span.recordException(err);
      throw err;
    } finally {
      span.end();
    }
  });
}
```

### 上下文传播

- 使用 W3C Trace Context（`traceparent` 标头）——这是 OpenTelemetry 的默认设置 |
- 在 HTTP、gRPC 和消息队列中传播上下文 |
- 对于异步任务：将 `traceparent` 数据序列化到任务数据中

### 跟踪采样

| 采样策略 | 适用场景 |
|----------|----------|
| **Always On** | 流量较低的服务，用于调试 |
| **Probabilistic**（N%） | 一般生产环境 |
| **Rate-limited**（每秒 N 条） | 高吞吐量的服务 |
| **Tail-based** | 需要捕获所有错误日志的情况 |

无论采用哪种策略，都必须对所有错误日志进行 100% 的采样。

---

## 指标收集

### RED 方法（基于请求的指标收集）

针对每个服务端点，监控以下三个指标：

| 指标 | 测量内容 | Prometheus 示例 |
|--------|-----------------|-------------------|
| **Rate** | 每秒请求数 | `rate(http_requests_total[5m])` |
| **Errors** | 失败请求的比例 | `rate(http_requests_total{status=~"5.."}[5m])` |
| **Duration** | 响应时间 | `histogram_quantile(0.99, http_request_duration_seconds)` |

### USE 方法（基于资源的指标收集）

对于基础设施组件（CPU、内存、磁盘、网络等），监控以下指标：

| 指标 | 测量内容 | 示例 |
|--------|-----------------|---------|
| **Utilization** | 资源利用率 | CPU 使用率为 78% |
| **Saturation** | 队列中的等待任务数量 | 线程池中有 12 个请求在等待处理 |
| **Errors** | 资源相关的错误事件 | 过去一分钟内的 3 次磁盘 I/O 错误 |

---

## 监控工具栈

| 工具 | 类别 | 适用场景 |
|------|----------|----------|
| **Prometheus** | 指标收集 | 基于拉取的指标数据，支持警报规则 |
| **Grafana** | 可视化工具 | 提供指标、日志和跟踪数据的仪表板 |
| **Jaeger** | 跟踪工具 | 支持分布式跟踪的可视化 |
| **Loki** | 日志聚合工具 | 与 Grafana 集成，用于日志处理 |
| **OpenTelemetry** | 统计数据收集 | 中立的可扩展性框架 |

**建议：** 首先使用 OTel Collector，然后结合 Prometheus、Grafana 和 Loki。只有在运营开销超过成本效益时，再考虑使用 SaaS 服务。

---

## 警报设计

### 警报的严重程度分级

| 严重程度 | 响应时间 | 示例 |
|----------|---------------|---------|
| **P1** | 立即处理 | 服务完全崩溃，数据丢失 |
| **P2** | 小于 30 分钟内处理 | 错误率超过 5%，延迟超过 5 秒 |
| **P3** | 工作时间期间处理 | 磁盘使用率超过 80%，证书将在 7 天后过期 |
| **P4** | 尽力处理 | 非关键性的功能即将被弃用 |

### 防止警报泛滥

- **基于症状发送警报，而非原因** —— 例如发送“错误率超过 5%”的警报，而不是“Pod 重启” |
- **多窗口、多触发条件** —— 同时关注突发性和持续性问题 |
- **每个警报都必须链接到相应的处理流程** |
- **每月审查警报** —— 删除或调整那些从未触发或频繁触发的警报 |
- **分组相关警报** —— 使用抑制规则来减少不必要的警报 |
- **设置合理的阈值** —— 如果警报频繁触发但未被处理，及时调整阈值或删除警报 |

## 仪表板设计

### 总览仪表板（“作战室”）

- 所有服务的总请求数量 |
- 全局错误率及其趋势线 |
- p50、p95、p99 延迟值 |
- 按严重程度分类的活跃警报数量 |
- 图表上显示的部署状态标记

### 服务仪表板（针对每个服务）

- 每个端点的关键指标 |
- 依赖关系的健康状况（上游/下游服务的成功率） |
- 资源利用率（CPU、内存、连接数） |
- 最常见的错误信息及其出现次数

## 可观测性检查清单

每个服务都必须满足以下要求：

- [ ] 使用结构化 JSON 进行日志记录，并保持一致的格式 |
- [ ] 在所有请求中传递关联信息/跟踪 ID |
- [ ] 每个外部端点都暴露关键指标数据 |
- [ ] 支持使用 OpenTelemetry 进行分布式跟踪 |
- [ ] 提供关键指标和资源利用率的仪表板 |
- [ ] 提供错误率、延迟和资源利用率的警报，并附带处理流程的链接 |
- [ ] 日志级别可以在运行时配置，无需重新部署 |
- [ ] 确保个人身份信息（PII）得到妥善处理 |
- [ ] 为日志、指标和跟踪数据定义明确的保留策略

## 避免的错误做法

| 错误做法 | 问题 | 解决方案 |
|-------------|---------|-----|
| 记录包含个人身份信息（PII） | 违反隐私/合规要求 | 对包含 PII 的数据进行屏蔽或排除；使用令牌引用 |
| 过度记录日志 | 会增加存储成本 | 只记录业务相关事件，而非数据流 |
| 非结构化的日志 | 无法查询或生成警报 | 使用结构化 JSON 并保持数据格式的一致性 |
| 在日志中插入字符串 | 可能导致数据结构破坏或注入风险 | 将相关数据作为元数据传递，而非直接写入日志 |
| 缺少关联 ID | 无法在不同服务之间追踪事件 | 在所有地方生成并传播 `trace_id` |
| 警报过多 | 会导致操作人员疲劳，掩盖真正的问题 | 使用分组、抑制规则和去重机制 |
| 高基数指标 | 可能导致 Prometheus 系统崩溃或仪表板响应延迟 | 避免使用用户 ID 或请求 ID 作为指标标签 |

## 绝对禁止的行为

1. **绝不要记录密码、令牌、API 密钥或敏感信息** —— 即使在 DEBUG 级别也不行 |
2. **绝不要在生产环境中使用 `console.log` 或 `print` 函数** —— 应使用结构化的日志库 |
3. **绝不要使用用户 ID、电子邮件或请求 ID 作为指标标签** —— 这会导致指标数据量激增 |
4. **发送警报时必须附带处理流程的链接** —— 无处理流程的警报会降低问题的解决效率 |
5. **绝不要仅依赖日志进行问题排查** —— 需要结合指标和跟踪数据才能实现全面的可观测性 |
6. **默认情况下不要记录请求/响应内容** —— 应根据用户需求选择是否记录这些内容，并对敏感信息进行脱敏 |
7. **绝不要忽略日志量** —— 设置日志存储预算，并在服务超出每日限额时触发警报 |
8. **在异步处理流程中忽略上下文信息的传播** —— 缺少上下文信息的跟踪会导致问题难以追踪 |

---

---

（由于文档内容较长，上述翻译仅展示了部分内容。如果需要完整翻译，请提供完整的 SKILL.md 文件。）