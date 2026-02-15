---
name: prometheus
model: fast
version: 1.0.0
description: >
  Prometheus monitoring — scrape configuration, service discovery, recording
  rules, alert rules, and production deployment for infrastructure and
  application metrics.
category: devops
tags: [prometheus, monitoring, metrics, alerting, observability]
author: skills-factory
---

# Prometheus

本文档介绍了Prometheus在生产环境中的配置方法，包括数据抓取（scraping）配置、服务发现（service discovery）、记录规则（recording rules）和警报规则（alert rules）的设置，以及基础设施和应用程序监控的最佳实践。

## 使用场景

| 场景 | 例子 |
|----------|---------|
| 设置指标采集 | 新服务需要Prometheus进行数据抓取 |
| 配置服务发现 | K8s Pod、基于文件的配置方式或静态目标 |
| 创建记录规则 | 预先计算复杂的PromQL查询语句 |
| 设计警报规则 | 基于服务水平目标（SLO）的可用性和延迟警报 |
| 生产环境部署 | 高可用性（HA）设置及存储策略规划 |
| 故障排除 | 数据抓取失败、指标缺失或标签重命名问题 |

## 架构

```
Applications ──(/metrics)──→ Prometheus Server ──→ AlertManager → Slack/PD
      ↑                           │
  client libraries          ├──→ Grafana (dashboards)
  (prom client)             └──→ Thanos/Cortex (long-term storage)
```

## 安装

### Kubernetes（使用Helm）

```bash
helm repo add prometheus-community \
  https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageVolumeSize=50Gi
```

## 核心配置

### prometheus.yml

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: production
    region: us-west-2

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

rule_files:
  - /etc/prometheus/rules/*.yml

scrape_configs:
  # Self-monitoring
  - job_name: prometheus
    static_configs:
      - targets: ["localhost:9090"]

  # Node exporters
  - job_name: node-exporter
    static_configs:
      - targets: ["node1:9100", "node2:9100", "node3:9100"]
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        regex: "([^:]+)(:[0-9]+)?"
        replacement: "${1}"

  # Application metrics (TLS)
  - job_name: my-app
    scheme: https
    metrics_path: /metrics
    tls_config:
      ca_file: /etc/prometheus/ca.crt
    static_configs:
      - targets: ["app1:9090", "app2:9090"]
```

## 服务发现

### 基于Kubernetes Pod的配置（使用注释）

```yaml
scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels:
          [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels:
          [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels:
          [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod
```

**启用数据抓取的Pod注释：**

```yaml
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
```

### 基于文件的配置方式

```yaml
scrape_configs:
  - job_name: file-sd
    file_sd_configs:
      - files: ["/etc/prometheus/targets/*.json"]
        refresh_interval: 5m
```

**targets/production.json:**

```json
[{
  "targets": ["app1:9090", "app2:9090"],
  "labels": { "env": "production", "service": "api" }
}]
```

## 发现方法比较

| 方法 | 适用场景 | 是否支持动态配置 |
|--------|----------|---------|
| `static_configs` | 固定基础设施环境 | 不支持 |
| `file_sd_configs` | 由配置管理工具（如CM）管理的资源列表 | 支持（文件监控） |
| `kubernetes_sd_configs` | K8s工作负载 | 支持（API监控） |
| `consul_sd_configs` | Consul服务网格 | 支持（Consul监控） |
| `ec2_sd_configs` | AWS EC2实例 | 支持（API监控） |

## 记录规则

为了提高仪表盘和警报的响应速度，建议预先计算复杂的PromQL查询语句：

```yaml
# /etc/prometheus/rules/recording_rules.yml
groups:
  - name: api_metrics
    interval: 15s
    rules:
      - record: job:http_requests:rate5m
        expr: sum by (job) (rate(http_requests_total[5m]))

      - record: job:http_errors:rate5m
        expr: sum by (job) (rate(http_requests_total{status=~"5.."}[5m]))

      - record: job:http_error_rate:ratio
        expr: job:http_errors:rate5m / job:http_requests:rate5m

      - record: job:http_duration:p95
        expr: >
          histogram_quantile(0.95,
            sum by (job, le) (rate(http_request_duration_seconds_bucket[5m]))
          )

  - name: resource_metrics
    interval: 30s
    rules:
      - record: instance:node_cpu:utilization
        expr: >
          100 - (avg by (instance)
            (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

      - record: instance:node_memory:utilization
        expr: >
          100 - ((node_memory_MemAvailable_bytes
            / node_memory_MemTotal_bytes) * 100)

      - record: instance:node_disk:utilization
        expr: >
          100 - ((node_filesystem_avail_bytes
            / node_filesystem_size_bytes) * 100)
```

## 命名规范

```
level:metric_name:operations
```

| 部分 | 例子 | 含义 |
|------|---------|---------|
| `level` | `job:`、`instance:` | 数据聚合的层级 |
| `metric_name` | `http_requests` | 基础指标名称 |
| `operations` | `:rate5m`、`:ratio` | 应用的计算函数 |

## 警报规则

```yaml
# /etc/prometheus/rules/alert_rules.yml
groups:
  - name: availability
    rules:
      - alert: ServiceDown
        expr: up{job="my-app"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "{{ $labels.instance }} is down"
          description: "{{ $labels.job }} down for >1 minute"

      - alert: HighErrorRate
        expr: job:http_error_rate:ratio > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Error rate {{ $value | humanizePercentage }} for {{ $labels.job }}"

      - alert: HighP95Latency
        expr: job:http_duration:p95 > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "P95 latency {{ $value }}s for {{ $labels.job }}"

  - name: resources
    rules:
      - alert: HighCPU
        expr: instance:node_cpu:utilization > 80
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "CPU {{ $value }}% on {{ $labels.instance }}"

      - alert: HighMemory
        expr: instance:node_memory:utilization > 85
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "Memory {{ $value }}% on {{ $labels.instance }}"

      - alert: DiskSpaceLow
        expr: instance:node_disk:utilization > 90
        for: 5m
        labels: { severity: critical }
        annotations:
          summary: "Disk {{ $value }}% on {{ $labels.instance }}"
```

## 警报严重程度指南

| 严重程度 | 阈值 | 对应措施 |
|----------|-----------|----------|
| `critical` | 服务不可用，存在数据丢失风险 | 立即通知相关人员 |
| `warning` | 系统性能下降，接近阈值 | 在几小时内进行调查 |
| `info` | 问题明显但不紧急 | 下一个工作日进行审查 |

## 验证

```bash
# Validate config syntax
promtool check config prometheus.yml

# Validate rule files
promtool check rules /etc/prometheus/rules/*.yml

# Test a query
promtool query instant http://localhost:9090 'up'

# Reload config without restart
curl -X POST http://localhost:9090/-/reload
```

## 最佳实践

| 实践 | 详细说明 |
|----------|--------|
| 命名规则：`prefix_name_unit` | 使用蛇形命名法（snake_case），计数器使用`_total`，单位使用`_seconds`/`_bytes` |
| 数据抓取间隔设置为15–60秒 | 过短的间隔会浪费资源和存储空间 |
| 为仪表盘预先计算常用指标 | 对于频繁查询的指标，应预先计算结果 |
| 监控Prometheus本身的运行状态 | 监控`prometheus_tsdb_*`和`scrape_duration_seconds`等指标 |
| 高可用性部署 | 部署多个Prometheus实例以同时抓取数据 |
| 规划存储策略 | 根据磁盘容量设置`--storage.tsdb.retention.time` |
| 使用联邦架构进行数据聚合 | 从多个区域实例收集数据并统一处理 |
| 长期存储策略 | 使用Thanos或Cortex等工具进行超过30天的数据保留 |

## 故障排除快速参考

| 问题 | 原因 | 解决方法 |
|---------|-----------|-----|
| 目标状态显示为`DOWN` | 检查 `/targets` 页面是否有错误 | 修复防火墙设置，验证端点连接，检查TLS协议 |
| 指标缺失 | 查询`up{job="x"}` | 验证数据抓取配置，检查 `/metrics` 端点 |
| 数据量过大（高基数） | `prometheus_tsdb_head_series` 文件增长过快 | 使用`metric_relabel_configs`删除高基数标签 |
| 存储空间不足 | 检查`prometheus_tsdb_storage_*` | 减少数据保留时间，增加磁盘空间，启用数据压缩 |
| 查询速度慢 | 检查`prometheus_engine_query_duration_seconds` | 增加记录规则，缩小查询范围，限制数据保留的时间范围 |
| 配置未生效 | 检查`prometheus_config_last_reload_successful` | 修复配置语法，通过`/-/reload`命令重新加载配置 |

## 绝对不要这样做

| 不推荐的做法 | 原因 | 应该怎么做 |
|-------------|-----|------------|
| 数据抓取间隔小于5秒 | 会导致目标服务器和存储系统负担过重 | 使用15–60秒的间隔 |
| 使用高基数标签（如用户ID、请求ID） | 会导致TSDB中的数据量激增 | 对于高基数数据，使用日志记录方式 |
| 警报规则不设置`for`参数 | 会导致不必要的警报 | 必须设置`for: 1m`的最小时间间隔 |
| 跳过记录规则 | 仪表盘会每次加载时都重新计算复杂查询 | 应使用预计算的记录结果 |
| 将敏感信息直接存储在`prometheus.yml`中 | 配置信息应存储在Git中 | 使用文件或环境变量进行安全管理 |
| 忽略`up`指标 | 会导致关键目标的状态变化未被及时发现 | 对所有指标设置`up == 0`的警报规则 |
| 在生产环境中仅使用一个Prometheus实例 | 会导致单点故障 | 应部署多个实例并共享数据抓取任务 |
| 不设置数据保留时间限制 | 会导致磁盘空间耗尽，Prometheus崩溃 | 明确设置`--storage.tsdb.retention.time` |

## 模板

| 模板 | 说明 |
|----------|-------------|
| [templates/prometheus.yml] | 包含静态配置、基于文件的配置和基于Kubernetes的服务发现设置 |
| [templates/alert-rules.yml] | 按类别分类的25个以上警报规则模板 |
| [templates/recording-rules.yml] | 预计算好的HTTP、延迟、资源使用情况和SLO相关指标的记录规则模板 |