---
name: prometheus
description: 通过 Prometheus API 查询指标数据，执行 PromQL 查询，并管理警报。
metadata: {"clawdbot":{"emoji":"🔥","requires":{"env":["PROMETHEUS_URL"]}}}
---
# Prometheus
指标与监控
## 环境配置
```bash
export PROMETHEUS_URL="http://prometheus.example.com:9090"
```
## 查询指标
```bash
curl "$PROMETHEUS_URL/api/v1/query?query=up"
```
## 范围查询
```bash
curl "$PROMETHEUS_URL/api/v1/query_range?query=rate(http_requests_total[5m])&start=2024-01-30T00:00:00Z&end=2024-01-30T12:00:00Z&step=60"
```
## 列出目标
```bash
curl "$PROMETHEUS_URL/api/v1/targets"
```
## 列出警报规则
```bash
curl "$PROMETHEUS_URL/api/v1/rules"
```
## 获取警报信息
```bash
curl "$PROMETHEUS_URL/api/v1/alerts"
```
## 链接
- 文档：https://prometheus.io/docs/prometheus/latest/querying/api/