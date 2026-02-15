---
name: grafana-dashboards
description: 创建并管理用于实时可视化系统和应用程序指标的生产级 Grafana 仪表板。这些仪表板可用于构建监控系统、展示各项指标数据，或创建操作运维相关的可视化界面。
---

# Grafana 仪表板

创建和管理可用于生产环境的 Grafana 仪表板，以实现全面的系统可观测性。

## 目的

设计高效的 Grafana 仪表板，用于监控应用程序、基础设施和业务指标。

## 使用场景

- 可视化 Prometheus 指标
- 创建自定义仪表板
- 实现服务水平目标（SLO）监控仪表板
- 监控基础设施性能
- 跟踪业务关键绩效指标（KPI）

## 仪表板设计原则

### 1. 信息层次结构
```
┌─────────────────────────────────────┐
│  Critical Metrics (Big Numbers)     │
├─────────────────────────────────────┤
│  Key Trends (Time Series)           │
├─────────────────────────────────────┤
│  Detailed Metrics (Tables/Heatmaps) │
└─────────────────────────────────────┘
```

### 2. RED 方法（服务监控）
- **速率**（Rate）：每秒请求数量
- **错误率**（Errors）：错误发生的频率
- **延迟/响应时间**（Duration）：系统处理的延迟或响应时间

### 3. USE 方法（资源监控）
- **利用率**（Utilization）：资源使用率（以百分比表示）
- **饱和度**（Saturation）：队列长度或等待时间
- **错误数量**（Errors）：系统出现的错误总数

## 仪表板结构

### API 监控仪表板
```json
{
  "dashboard": {
    "title": "API Monitoring",
    "tags": ["api", "production"],
    "timezone": "browser",
    "refresh": "30s",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (service)",
            "legendFormat": "{{service}}"
          }
        ],
        "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8}
      },
      {
        "title": "Error Rate %",
        "type": "graph",
        "targets": [
          {
            "expr": "(sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))) * 100",
            "legendFormat": "Error Rate"
          }
        ],
        "alert": {
          "conditions": [
            {
              "evaluator": {"params": [5], "type": "gt"},
              "operator": {"type": "and"},
              "query": {"params": ["A", "5m", "now"]},
              "type": "query"
            }
          ]
        },
        "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8}
      },
      {
        "title": "P95 Latency",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))",
            "legendFormat": "{{service}}"
          }
        ],
        "gridPos": {"x": 0, "y": 8, "w": 24, "h": 8}
      }
    ]
  }
}
```

**参考文档：**请参阅 `assets/api-dashboard.json`

## 仪表板类型

### 1. 统计面板（单值显示）
```json
{
  "type": "stat",
  "title": "Total Requests",
  "targets": [{
    "expr": "sum(http_requests_total)"
  }],
  "options": {
    "reduceOptions": {
      "values": false,
      "calcs": ["lastNotNull"]
    },
    "orientation": "auto",
    "textMode": "auto",
    "colorMode": "value"
  },
  "fieldConfig": {
    "defaults": {
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"value": 0, "color": "green"},
          {"value": 80, "color": "yellow"},
          {"value": 90, "color": "red"}
        ]
      }
    }
  }
}
```

### 2. 时间序列图
```json
{
  "type": "graph",
  "title": "CPU Usage",
  "targets": [{
    "expr": "100 - (avg by (instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)"
  }],
  "yaxes": [
    {"format": "percent", "max": 100, "min": 0},
    {"format": "short"}
  ]
}
```

### 3. 表格面板
```json
{
  "type": "table",
  "title": "Service Status",
  "targets": [{
    "expr": "up",
    "format": "table",
    "instant": true
  }],
  "transformations": [
    {
      "id": "organize",
      "options": {
        "excludeByName": {"Time": true},
        "indexByName": {},
        "renameByName": {
          "instance": "Instance",
          "job": "Service",
          "Value": "Status"
        }
      }
    }
  ]
}
```

### 4. 热力图
```json
{
  "type": "heatmap",
  "title": "Latency Heatmap",
  "targets": [{
    "expr": "sum(rate(http_request_duration_seconds_bucket[5m])) by (le)",
    "format": "heatmap"
  }],
  "dataFormat": "tsbuckets",
  "yAxis": {
    "format": "s"
  }
}
```

## 变量

### 查询变量
```json
{
  "templating": {
    "list": [
      {
        "name": "namespace",
        "type": "query",
        "datasource": "Prometheus",
        "query": "label_values(kube_pod_info, namespace)",
        "refresh": 1,
        "multi": false
      },
      {
        "name": "service",
        "type": "query",
        "datasource": "Prometheus",
        "query": "label_values(kube_service_info{namespace=\"$namespace\"}, service)",
        "refresh": 1,
        "multi": true
      }
    ]
  }
}
```

### 在查询中使用变量
```
sum(rate(http_requests_total{namespace="$namespace", service=~"$service"}[5m]))
```

## 仪表板中的警报功能
```json
{
  "alert": {
    "name": "High Error Rate",
    "conditions": [
      {
        "evaluator": {
          "params": [5],
          "type": "gt"
        },
        "operator": {"type": "and"},
        "query": {
          "params": ["A", "5m", "now"]
        },
        "reducer": {"type": "avg"},
        "type": "query"
      }
    ],
    "executionErrorState": "alerting",
    "for": "5m",
    "frequency": "1m",
    "message": "Error rate is above 5%",
    "noDataState": "no_data",
    "notifications": [
      {"uid": "slack-channel"}
    ]
  }
}
```

## 仪表板配置

**dashboards.yml 文件示例：**
```yaml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: 'General'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/dashboards
```

## 常见仪表板模板

### 基础设施仪表板

**关键面板：**
- 每个节点的 CPU 使用率
- 每个节点的内存使用情况
- 磁盘 I/O 操作
- 按命名空间划分的 Pod 数量
- 节点状态

**参考文档：**请参阅 `assets/infrastructure-dashboard.json`

### 数据库仪表板

**关键面板：**
- 每秒查询次数
- 连接池使用情况
- 查询延迟（P50、P95、P99 分位数）
- 活动连接数
- 数据库大小
- 数据库复制延迟
- 高延迟查询

**参考文档：**请参阅 `assets/database-dashboard.json`

### 应用程序仪表板

**关键面板：**
- 请求数量
- 错误率
- 响应时间（分位数）
- 活动用户/会话数
- 缓存命中率
- 队列长度

## 最佳实践

1. **从现有模板开始**（使用 Grafana 社区提供的模板）
2. **为面板和变量使用统一的命名规范**
3. **将相关指标分组显示在同一行中**
4. **设置合适的时间范围**（默认为过去 6 小时）
5. **使用变量以提高灵活性**
6. **为面板添加描述以便于理解数据**
7. **正确设置单位**
8. **为颜色设置有意义的阈值**
9. **在整个仪表板中保持颜色的一致性**
10. **使用不同的时间范围进行测试**

## 通过代码配置仪表板

### 使用 Terraform 进行配置
```hcl
resource "grafana_dashboard" "api_monitoring" {
  config_json = file("${path.module}/dashboards/api-monitoring.json")
  folder      = grafana_folder.monitoring.id
}

resource "grafana_folder" "monitoring" {
  title = "Production Monitoring"
}
```

### 使用 Ansible 进行配置
```yaml
- name: Deploy Grafana dashboards
  copy:
    src: "{{ item }}"
    dest: /etc/grafana/dashboards/
  with_fileglob:
    - "dashboards/*.json"
  notify: restart grafana
```

## 相关技能

- `prometheus-configuration`：用于收集 Prometheus 指标数据
- `slo-implementation`：用于实现服务水平目标（SLO）相关的仪表板功能