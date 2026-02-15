---
name: slo-implementation
description: 定义并实施服务水平指标（Service Level Indicators, SLIs）和服务水平目标（Service Level Objectives, SLOs），并设置相应的错误预算（error budgets）和警报机制。这些指标和目标可用于制定可靠性目标、实施运维最佳实践（SRE practices），或衡量服务性能。
---

# SLO 实施

本文档提供了定义和实施服务水平指标（SLIs）、服务水平目标（SLOs）以及错误预算（error budgets）的框架。

## 目的

通过使用 SLIs、SLOs 和错误预算来实现可衡量的可靠性目标，从而在可靠性与创新速度之间取得平衡。

## 使用场景

- 定义服务可靠性目标
- 测量用户感知的可靠性
- 实施错误预算
- 创建基于 SLO 的警报
- 跟踪可靠性目标

## SLI/SLO/SLA 层次结构

```
SLA (Service Level Agreement)
  ↓ Contract with customers
SLO (Service Level Objective)
  ↓ Internal reliability target
SLI (Service Level Indicator)
  ↓ Actual measurement
```

## 定义 SLIs

### 常见的 SLI 类型

#### 1. 可用性 SLI（Availability SLI）
```promql
# Successful requests / Total requests
sum(rate(http_requests_total{status!~"5.."}[28d]))
/
sum(rate(http_requests_total[28d]))
```

#### 2. 延迟 SLI（Latency SLI）
```promql
# Requests below latency threshold / Total requests
sum(rate(http_request_duration_seconds_bucket{le="0.5"}[28d]))
/
sum(rate(http_request_duration_seconds_count[28d]))
```

#### 3. 耐用性 SLI（Durability SLI）
```
# Successful writes / Total writes
sum(storage_writes_successful_total)
/
sum(storage_writes_total)
```

## 设置 SLO 目标

### 可用性 SLO 示例

| SLO 百分比 | 每月停机时间 | 每年停机时间 |
|-------|----------------|---------------|
| 99%   | 7.2 小时      | 3.65 天     |
| 99.9% | 43.2 分钟   | 8.76 小时    |
| 99.95% | 21.6 分钟   | 4.38 小时    |
| 99.99% | 4.32 分钟   | 52.56 分钟 |

### 选择合适的 SLO

**考虑因素：**
- 用户期望
- 业务需求
- 当前性能
- 可靠性的成本
- 竞争对手的基准数据

**示例 SLO：**
```yaml
slos:
  - name: api_availability
    target: 99.9
    window: 28d
    sli: |
      sum(rate(http_requests_total{status!~"5.."}[28d]))
      /
      sum(rate(http_requests_total[28d]))

  - name: api_latency_p95
    target: 99
    window: 28d
    sli: |
      sum(rate(http_request_duration_seconds_bucket{le="0.5"}[28d]))
      /
      sum(rate(http_request_duration_seconds_count[28d]))
```

## 错误预算计算

### 错误预算公式

```
Error Budget = 1 - SLO Target
```

**示例：**
- SLO：99.9% 的可用性
- 错误预算：0.1% = 每月 43.2 分钟
- 当前错误率：0.05% = 每月 21.6 分钟
- 剩余预算：50%

### 错误预算政策

```yaml
error_budget_policy:
  - remaining_budget: 100%
    action: Normal development velocity
  - remaining_budget: 50%
    action: Consider postponing risky changes
  - remaining_budget: 10%
    action: Freeze non-critical changes
  - remaining_budget: 0%
    action: Feature freeze, focus on reliability
```

## SLO 的实施

### Prometheus 记录规则

```yaml
# SLI Recording Rules
groups:
  - name: sli_rules
    interval: 30s
    rules:
      # Availability SLI
      - record: sli:http_availability:ratio
        expr: |
          sum(rate(http_requests_total{status!~"5.."}[28d]))
          /
          sum(rate(http_requests_total[28d]))

      # Latency SLI (requests < 500ms)
      - record: sli:http_latency:ratio
        expr: |
          sum(rate(http_request_duration_seconds_bucket{le="0.5"}[28d]))
          /
          sum(rate(http_request_duration_seconds_count[28d]))

  - name: slo_rules
    interval: 5m
    rules:
      # SLO compliance (1 = meeting SLO, 0 = violating)
      - record: slo:http_availability:compliance
        expr: sli:http_availability:ratio >= bool 0.999

      - record: slo:http_latency:compliance
        expr: sli:http_latency:ratio >= bool 0.99

      # Error budget remaining (percentage)
      - record: slo:http_availability:error_budget_remaining
        expr: |
          (sli:http_availability:ratio - 0.999) / (1 - 0.999) * 100

      # Error budget burn rate
      - record: slo:http_availability:burn_rate_5m
        expr: |
          (1 - (
            sum(rate(http_requests_total{status!~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          )) / (1 - 0.999)
```

### SLO 警报规则

```yaml
groups:
  - name: slo_alerts
    interval: 1m
    rules:
      # Fast burn: 14.4x rate, 1 hour window
      # Consumes 2% error budget in 1 hour
      - alert: SLOErrorBudgetBurnFast
        expr: |
          slo:http_availability:burn_rate_1h > 14.4
          and
          slo:http_availability:burn_rate_5m > 14.4
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Fast error budget burn detected"
          description: "Error budget burning at {{ $value }}x rate"

      # Slow burn: 6x rate, 6 hour window
      # Consumes 5% error budget in 6 hours
      - alert: SLOErrorBudgetBurnSlow
        expr: |
          slo:http_availability:burn_rate_6h > 6
          and
          slo:http_availability:burn_rate_30m > 6
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Slow error budget burn detected"
          description: "Error budget burning at {{ $value }}x rate"

      # Error budget exhausted
      - alert: SLOErrorBudgetExhausted
        expr: slo:http_availability:error_budget_remaining < 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "SLO error budget exhausted"
          description: "Error budget remaining: {{ $value }}%"
```

## SLO 仪表板

**Grafana 仪表板结构：**

```
┌────────────────────────────────────┐
│ SLO Compliance (Current)           │
│ ✓ 99.95% (Target: 99.9%)          │
├────────────────────────────────────┤
│ Error Budget Remaining: 65%        │
│ ████████░░ 65%                     │
├────────────────────────────────────┤
│ SLI Trend (28 days)                │
│ [Time series graph]                │
├────────────────────────────────────┤
│ Burn Rate Analysis                 │
│ [Burn rate by time window]         │
└────────────────────────────────────┘
```

**示例查询：**

```promql
# Current SLO compliance
sli:http_availability:ratio * 100

# Error budget remaining
slo:http_availability:error_budget_remaining

# Days until error budget exhausted (at current burn rate)
(slo:http_availability:error_budget_remaining / 100)
*
28
/
(1 - sli:http_availability:ratio) * (1 - 0.999)
```

## 多窗口错误率警报

```yaml
# Combination of short and long windows reduces false positives
rules:
  - alert: SLOBurnRateHigh
    expr: |
      (
        slo:http_availability:burn_rate_1h > 14.4
        and
        slo:http_availability:burn_rate_5m > 14.4
      )
      or
      (
        slo:http_availability:burn_rate_6h > 6
        and
        slo:http_availability:burn_rate_30m > 6
      )
    labels:
      severity: critical
```

## SLO 审查流程

### 每周审查
- 当前 SLO 的遵守情况
- 错误预算的使用情况
- 趋势分析
- 事件的影响

### 每月审查
- SLO 的达成情况
- 错误预算的使用情况
- 事件的事后分析
- SLO 的调整

### 每季度审查
- SLO 的相关性
- 目标的调整
- 流程改进
- 工具的优化

## 最佳实践

1. **从面向用户的服务开始**
2. **使用多种 SLI（如可用性、延迟等）**
3. **设定可实现的 SLO 目标（不要追求 100%）**
4. **实施多窗口警报以减少干扰**
5. **持续跟踪错误预算的使用情况**
6. **定期审查 SLO**
7. **记录 SLO 的决策过程**
8. **确保 SLO 与业务目标保持一致**
9. **自动化 SLO 报告**
10. **利用 SLO 进行优先级排序**

## 相关技能

- `prometheus-configuration`：用于指标收集
- `grafana-dashboards`：用于 SLO 的可视化展示