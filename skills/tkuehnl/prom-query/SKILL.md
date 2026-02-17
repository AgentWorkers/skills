---
name: prom-query
version: 1.0.1
description: "Prometheus指标查询与警报解析器 —— 查询指标数据、解析时间序列数据、对警报进行分类处理"
author: CacheForge
license: MIT
tags: [prometheus, metrics, monitoring, alerting, observability, thanos, mimir, victoriametrics, grafana, discord, discord-v2]
tools:
  - name: prom-query
    description: "Query Prometheus metrics, alerts, targets, and rules via the HTTP API"
    command: bash scripts/prom-query.sh
    args: "[command] [args...]"
    env:
      - PROMETHEUS_URL: "Base URL of Prometheus server (required)"
      - PROMETHEUS_TOKEN: "Bearer token for authentication (optional)"
---
# prom-query — Prometheus指标查询与警报解析工具

您可以使用该工具访问兼容Prometheus的指标服务器，执行指标查询、检查警报、监控目标状态以及探索可用的指标数据。该工具支持查询Prometheus、Thanos、Mimir和VictoriaMetrics等系统，它们都使用相同的HTTP API。

## 命令

| 命令 | 功能 | 例子 |
|---------|---------|---------|
| `query <promql>` | 即时查询（当前值） | `prom-query query 'up'` |
| `range <promql> [--start=] [--end=] [--step=]` | 范围查询（随时间变化的序列数据） | `prom-query range 'rate(http_requests_total[5m])` --start=-1h --step=1m` |
| `alerts [--state=firing\|pending\|inactive]` | 列出激活中的警报 | `prom-query alerts --state=firing` |
| `targets [--state=active\|dropped\|any]` | 监控目标状态 | `prom-query targets` |
| `explore [pattern]` | 按名称模式搜索可用指标 | `prom-query explore 'http_request'` |
| `rules [--type=alert\|record]` | 查看警报规则与记录规则 | `prom-query rules --type=alert` |

## 如何将自然语言问题转换为PromQL查询语句

当用户询问关于系统的问题时，请使用以下模式将其转换为PromQL查询语句：

### 错误率
```
# "What's the error rate for the API?"
rate(http_requests_total{code=~"5.."}[5m]) / rate(http_requests_total[5m])

# "Error rate for the payments service"
rate(http_requests_total{service="payments", code=~"5.."}[5m])

# "4xx and 5xx errors per second"
sum(rate(http_requests_total{code=~"[45].."}[5m])) by (code)
```

### 延迟（直方图）
```
# "P99 latency"
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# "P50 latency by service"
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))

# "Average request duration"
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])
```

### CPU使用率
```
# "CPU usage per instance"
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# "CPU usage per pod (Kubernetes)"
sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) by (pod, namespace)

# "Which pods use the most CPU?"
topk(10, sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) by (pod, namespace))
```

### 内存使用情况
```
# "Memory usage percentage per instance"
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# "Memory usage per pod (Kubernetes)"
sum(container_memory_working_set_bytes{container!=""}) by (pod, namespace)

# "Pods using more than 1GB RAM"
sum(container_memory_working_set_bytes{container!=""}) by (pod, namespace) > 1e9
```

### 磁盘使用情况
```
# "Disk usage percentage"
(1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) * 100

# "Disk will be full in 4 hours?" (linear prediction)
predict_linear(node_filesystem_avail_bytes{mountpoint="/"}[1h], 4*3600) < 0
```

### 网络流量
```
# "Network traffic in/out per interface"
rate(node_network_receive_bytes_total[5m])
rate(node_network_transmit_bytes_total[5m])
```

### Kubernetes特定指标
```
# "How many pods are not ready?"
sum(kube_pod_status_ready{condition="false"}) by (namespace)

# "Pods in CrashLoopBackOff"
kube_pod_container_status_waiting_reason{reason="CrashLoopBackOff"}

# "Deployment replica mismatch"
kube_deployment_spec_replicas != kube_deployment_status_available_replicas

# "Node conditions"
kube_node_status_condition{condition="Ready", status="true"} == 0
```

### 通用查询模式
```
# "Show me everything about <service>"
# First, explore what metrics exist:
prom-query explore '<service_name>'

# "Is everything up?"
prom-query query 'up'

# "What changed in the last hour?"
# Use range query with the relevant metric and look for step changes:
prom-query range '<metric>' --start=-1h --step=1m

# Rate of any counter:
rate(<counter_metric>[5m])

# Sum across labels:
sum(<metric>) by (<label>)

# Top N:
topk(10, <metric>)
```

## 如何解读时间序列数据

在查看范围查询结果时，请注意以下几点：

1. **趋势**：数值是随时间上升、下降还是保持稳定？比较初始值和最终值。
2. **峰值**：观察最小值/最大值与平均值之间的差异。较大的差距可能表示数据出现异常波动。
3. **变化幅度**：数值是否突然跳升至新的基准水平？（可能是部署或配置更改导致的）。
4. **周期性**：数据是否存在重复的模式？（例如每日流量模式、定时任务）
5. **相关性**：如果查询了多个指标，它们的变化是否发生在相同的时间点？

## 阅读汇总信息

范围查询结果会自动提供每个指标的汇总信息：
- `min` / `max` / `avg`：所有数值的统计摘要
- `first` / `last`：数据的起始和结束值（用于判断趋势方向）
- `pointCount`：数据点的数量
- `downsampled`：是否自动调整了查询步长以减少数据量

## 智能上下文管理

该工具会自动对数据量较大的查询进行降采样处理（限制返回的数据点数量）。当`downsampled`设置为`true`时，会通知用户已调整了查询步长，并提供放大时间窗口以获取更详细的数据。

## 事件处理流程

在处理事件或调查问题时，请按照以下步骤操作：

1. **从警报开始**：`prom-query alerts --state=firing` — 查看哪些警报正在触发。
2. **检查目标状态**：`prom-query targets` — 有哪些目标的状态发生了变化？
3. **查询警报中提到的具体指标**。
4. **进行范围查询**，了解导致警报发生的趋势。
5. **探索相关指标**，寻找数据之间的关联性。
6. **查看规则设置**，了解警报的触发条件。

## 警报展示方式

在向用户展示警报时，请按照以下方式呈现信息：
- 按严重程度分组（紧急 → 警告 → 信息提示）
- 显示每个警报的触发时间（从`activeAt`字段开始计算）。
- 包含警报的摘要/描述信息。
- 如果警报包含具体数值，请解释其在实际场景中的含义。
- 提供下一步建议：建议查询哪些指标以获取更多详细信息。

## Discord v2交付模式（OpenClaw v2026.2.14+）

在Discord频道中使用时：
- 发送简洁的初始摘要（显示激活中的警报、受影响最严重的服务以及推荐的后续查询内容）。
- 保持第一条消息长度在1200字符以内，避免使用过于复杂的表格格式。
- 如果支持Discord插件，提供以下操作选项：
  - `Show Last 1h Trend`（显示过去1小时的趋势）
  - `List Firing Alerts`（列出所有激活中的警报）
  - `Explore Related Metrics`（探索相关指标）
- 如果插件不可用，以编号列表的形式提供相同的功能。
- 对于复杂的时间序列数据，分多次发送（每条消息不超过15行）。

## 重要说明

- 所有操作均为**只读**，不会修改Prometheus的数据、规则或配置。
- 大量查询结果会自动进行限制和汇总处理。
- `explore`命令支持正则表达式匹配（不区分大小写）。
- 时间参数支持相对时间表达式（如`-1h`、`-30m`、`-2d`）、纪元时间戳或ISO861日期格式。
- 如果设置了`PROMETHEUS_TOKEN`，则使用Bearer令牌进行身份验证。请勿在响应中直接显示令牌内容。

## 错误处理

如果查询失败，请根据以下情况处理：
- **“无法连接到Prometheus”**：检查`PROMETHEUS_URL`和网络连接是否正常。
- **PromQL语法错误**：检查查询语句是否正确，修正后重试。
- **“无数据”**：可能是指标不存在或标签选择过于具体。尝试使用`explore`命令查找正确的指标名称。
- **超时**：查询操作可能过于复杂。可以添加过滤条件、缩小时间范围或使用`topk()`函数优化查询。

本工具由CacheForge提供支持 📊