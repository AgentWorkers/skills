---
name: datadog-metrics
description: 使用 Datadog 监控应用程序指标：收集自定义指标、创建仪表板、设置警报并分析性能。
version: 1.0.0
tags: [datadog, metrics, monitoring, observability, dashboard]
author: OpenWork
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - DATADOG_API_KEY
        - DATADOG_APP_KEY
---

# Datadog指标

Datadog提供了全面的指标监控和可观测性功能。

## 功能

### 自定义指标
- 从应用程序发送指标
- 支持计数器（Counter）、计量器（Gauge）和直方图（Histogram）类型
- 分布式指标（Distribution metrics）
- 基于标签的过滤（Tag-based filtering）
- 与DogStatsD的集成（Integration with DogStatsD）

### 仪表板管理
- 创建自定义仪表板（Create custom dashboards）
- 添加组件（Widgets）：图表（Graphs）、数字（Numbers）、日志（Logs）
- 模板变量（Template variables）
- 共享和导出仪表板（Share and export dashboards）
- 实时更新（Real-time updates）

### 警报配置
- 基于指标的警报（Metric-based alerts）
- 综合警报（Composite alerts）
- 故障时间调度（Downtime scheduling）
- 警报路由（Alert routing）
- 维护自动暂停功能（Auto-pause for maintenance）

### 基础设施监控
- 主机指标（Host metrics）
- 容器监控（Container monitoring）
- 与Kubernetes的集成（Integration with Kubernetes）
- 与云服务提供商的集成（Integration with cloud providers）
- 进程监控（Process monitoring）

### APM（应用程序性能监控）
- 跟踪分析（Trace analysis）
- 服务地图（Service map）
- 性能分析（Performance profiling）
- 错误追踪（Error tracking）
- 延迟分解（Latency breakdown）

## 使用方法

### 指标示例
```
Send gauge metric cpu.usage with value 75
Track counter requests.count with tags env:prod
Record histogram response.time with 200ms
```

### 仪表板示例
```
Create dashboard 'Production Overview'
Add CPU and memory graph to monitoring
Setup latency heatmap for API service
```

### 警报示例
```
Alert when error rate > 5% for 5 minutes
Create downtime for maintenance window
Alert when p99 latency > 2 seconds
```

### APM示例
```
Get slowest endpoints in production
Trace request through services
Find errors in last hour for checkout service
```

## 集成
- AWS、GCP、Azure
- Kubernetes、Docker
- PostgreSQL、MySQL、Redis
- Nginx、Apache
- 支持400多种集成服务（Integration with over 400 services）

## 依赖项
- Python 3.8及以上版本（Python 3.8+）
- Datadog库（datadog）

## 安装说明
```bash
pip install datadog
```

## 必需的环境变量
- `DATADOG_API_KEY`：来自Datadog的API密钥
- `DATADOG_APP_KEY`：应用程序密钥

## 相关文件
- `SKILL.md`：本文档文件
- `metrics.py`：自定义指标处理脚本
- `dashboards.py`：仪表板管理脚本
- `alerts.py`：警报配置脚本
- `infrastructure.py`：基础设施监控脚本
- `apm.py`：应用程序性能监控脚本