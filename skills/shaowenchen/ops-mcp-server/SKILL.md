---
name: ops-mcp-server
description: >
  通过 `ops-mcp-server` 的 MCP 接口查询可观测性数据并执行操作流程。  
  该接口支持查询 Kubernetes 事件、Prometheus 指标、Elasticsearch 日志、Jaeger 分布式追踪数据以及 SOPS 运维脚本（Runbooks）。
triggers:
  - ops
  - ops-mcp-server
  - kubernetes
  - k8s
  - prometheus
  - metrics
  - elasticsearch
  - logs
  - jaeger
  - traces
  - tracing
  - observability
  - monitoring
  - incident
  - sops
  - events
  - cluster
  - pod
  - deployment
  - namespace
  - alert
  - latency
  - error rate
  - outage
---
# MCP服务器操作技能

通过统一的MCP接口，您可以访问基础设施的可观测性数据并执行操作流程。

## 功能概览

| 模块 | 工具 | 功能说明 |
|--------|-------|----------------|
| **事件**（Kubernetes） | `list-events-from-ops`, `get-events-from-ops` | Pod、Deployment或节点发生了什么？ |
| **指标**（Prometheus） | `list-metrics-from-prometheus`, `query-metrics-from-prometheus`, `query-metrics-range-from-prometheus` | CPU、内存或网络流量是否正常？随时间发生了哪些变化？ |
| **日志**（Elasticsearch） | `list-log-indices-from-elasticsearch`, `search-logs-from-elasticsearch`, `query-logs-from-elasticsearch` | 日志中有哪些错误？服务X记录了什么？ |
| **跟踪信息**（Jaeger） | `get-services-from-jaeger`, `get-operations-from-jaeger`, `find-traces-from-jaeger`, `get-trace-from-jaeger` | 为什么这个请求会变慢？在哪里出现了故障？ |
| **操作流程**（SOPS） | `list-sops-from-ops`, `list-sops-parameters-from-ops`, `execute-sops-from-ops` | 运行标准的操作流程 |

## 首次使用前的设置

```bash
# 1. Use mcporter with npx (no installation needed)
# Or install globally: npm i -g mcporter

# 2. Register the server
cd ~/.openclaw/workspace
npx mcporter config add ops-mcp-server --url http://localhost/mcp

# 3. Authenticate (if needed)
npx mcporter auth ops-mcp-server
# On failure, add to ~/.openclaw/workspace/config/mcporter.json:
# "headers": { "Authorization": "Bearer YOUR_TOKEN" }

# 4. Verify
npx mcporter list ops-mcp-server
npx mcporter call ops-mcp-server list-events-from-ops page_size=5

# 5. Set env var
export OPS_MCP_SERVER_URL="http://localhost/mcp"
```

---

## 调查方法：决策指南

当用户描述问题时，使用本指南来选择合适的工具并构建完整的调查方案。

### 🔴 “系统出现故障/服务无法正常运行”

1. **首先查看Kubernetes事件** — 检查Pod是否崩溃、重启或被驱逐
   ```
   get-events-from-ops  subject_pattern="ops.clusters.*.namespaces.<ns>.pods.*.events"
   ```
2. **查看日志** — 在事件发生时搜索相关错误信息
   ```
   query-logs-from-elasticsearch  query="FROM logs-* | WHERE @timestamp > NOW() - 30 minutes | WHERE level == 'error' | LIMIT 50"
   ```
3. **分析跟踪信息** — 查找失败或响应缓慢的请求
   ```
   find-traces-from-jaeger  serviceName=<service>  tags={"error":"true"}
   ```

### 🟡 **性能下降/请求速度变慢**

1. **检查指标** — 查看资源使用情况
   ```
   query-metrics-from-prometheus  query="100 - (avg(rate(node_cpu_seconds_total{mode='idle'}[5m])) * 100)"
   query-metrics-range-from-prometheus  query="node_memory_MemAvailable_bytes"  time_range="1h"  step="1m"
   ```
2. **分析跟踪信息** — 查找响应缓慢的请求
   ```
   find-traces-from-jaeger  serviceName=<service>  durationMin=1000
   ```
3. **查看日志** — 寻找超时或查询速度慢的警告

### 🔵 **需要执行操作/重启某个服务**

1. **列出可用的操作流程**  
   ```
   list-sops-from-ops
   ```
2. **获取操作所需的参数**  
   ```
   list-sops-parameters-from-ops  sops_id=<id>
   ```
3. **执行操作**  
   ```
   execute-sops-from-ops  sops_id=<id>  parameters='{...}'
   ```

### 🟢 **常规健康检查/没有特定问题**

首先查看事件和关键指标，根据发现的情况进一步深入调查。

---

## 工具快速参考

### 事件 — 使用NATS主题模式格式

```
# Namespace resources
ops.clusters.{cluster}.namespaces.{ns}.{resourceType}.{name}.{observation}

# Node level
ops.clusters.{cluster}.nodes.{nodeName}.{observation}

# Notifications
ops.notifications.providers.{provider}.channels.{channel}.severities.{severity}
```

通配符：`*` = 任意一个字段；`>` = 其余所有字段（仅显示尾部数据）

事件类型：`status` | `events` | `alerts` | `findings`

时间格式：Unix毫秒：`$(date +%s)000`

### 日志 — 使用ES|QL查询语言

```sql
-- Recent errors
FROM logs-* | WHERE @timestamp > NOW() - 30 minutes | WHERE level == 'error' | LIMIT 100

-- Top errors by frequency
FROM logs-* | WHERE @timestamp > NOW() - 1 hour | WHERE level == 'error'
| STATS count() BY message | SORT count DESC | LIMIT 10

-- Specific service
FROM logs-* | WHERE service == 'checkout-service' | WHERE @timestamp > NOW() - 1 hour | LIMIT 50
```

### 指标 — 使用PromQL查询语言

```
# CPU usage
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance) * 100)

# Memory available
node_memory_MemAvailable_bytes

# HTTP error rate
rate(http_requests_total{status=~"5.."}[5m])
```

---

## 详细示例与参考文件

如需完整的参数列表、输出格式和高级查询模式，请参阅以下文件：

- **事件** → `examples/events.md`
- **指标** → `examples/metrics.md`
- **日志** → `examples/logs.md`
- **跟踪信息** → `examples/traces.md`
- **操作流程** → `examples/sops.md`
- **事件主题格式设计** → `references/design.md`

在对不确定的工具进行调用之前，请先阅读相关示例文件。

---

## 本技能的适用范围

- 本技能不适用于直接修改基础设施（请使用专门的自动化工具）
- 本技能不用于实时警报（仅用于调查，而非监控功能）
- 本技能不允许写入或修改操作数据（所有访问均为只读权限）