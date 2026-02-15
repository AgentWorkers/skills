---
name: prometheus
description: 查询 Prometheus 监控数据以检查服务器指标、资源使用情况以及系统健康状况。当用户询问服务器状态、磁盘空间、CPU/内存使用情况、网络统计信息或 Prometheus 收集的任何其他指标时，可以使用此功能。支持通过环境变量进行 HTTP Basic 身份验证。
---

# Prometheus 技能

查询 Prometheus 监控数据，以获取有关您基础设施的洞察。

## 环境变量

在 `.env` 文件中设置以下变量：
- `PROMETHEUS_URL` - Prometheus 服务器地址（例如：`http://localhost:9090`）
- `PROMETHEUS_USER` - HTTP 基本认证用户名（可选）
- `PROMETHEUS_PASSWORD` - HTTP 基本认证密码（可选）

## 使用方法

### 查询指标

使用 CLI 运行 PromQL 查询：

```bash
source .env && node scripts/cli.js query '<promql_query>'
```

### 常见示例

**磁盘空间使用情况：**
```bash
node scripts/cli.js query '100 - (node_filesystem_avail_bytes / node_filesystem_size_bytes * 100)'
```

**CPU 使用情况：**
```bash
node scripts/cli.js query '100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
```

**内存使用情况：**
```bash
node scripts/cli.js query '(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100'
```

**平均负载：**
```bash
node scripts/cli.js query 'node_load1'
```

### 列出指标

查找符合特定模式的可用指标：

```bash
node scripts/cli.js metrics 'node_memory_*'
```

### 系列发现

通过标签选择器查找时间序列数据：

```bash
node scripts/cli.js series '{__name__=~"node_cpu_.*", instance=~".*:9100"}'
```

### 获取标签信息

列出标签名称：

```bash
node scripts/cli.js labels
```

列出特定标签的值：

```bash
node scripts/cli.js label-values instance
```

## 输出格式

所有命令的输出均为 JSON 格式，便于解析。可以使用 `jq` 对输出进行美化显示：

```bash
node scripts/cli.js query 'up' | jq .
```

## 常见查询参考

| 指标          | PromQL 查询                                      |
|--------------|--------------------------------------------|
| 磁盘空闲百分比    | `node_filesystem_avail_bytes / node_filesystem_size_bytes * 100`     |
| 磁盘使用百分比    | `100 - (node_filesystem_avail_bytes / node_filesystem_size_bytes * 100)`     |
| CPU 空闲百分比    | `avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m]) * 100`     |
| 内存使用百分比    | `(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100`     |
| 网络接收流量    | `rate(node_network_receive_bytes_total[5m])`                 |
| 网络发送流量    | `rate(node_network_transmit_bytes_total[5m])`                 |
| 运行时间        | `node_time_seconds - node_boot_time_seconds`                 |
| 服务状态      | `up`                                      |

## 注意事项

- 即时查询的时间范围默认为过去 1 小时
- 使用 `[5m]` 作为时间范围，用于计算速率
- 所有查询返回的 JSON 数据中，`data.result` 部分包含查询结果
- 实例标签通常以 `host:port` 的格式显示