---
name: prometheus
description: 查询 Prometheus 监控数据以检查服务器指标、资源使用情况以及系统健康状况。当用户询问服务器状态、磁盘空间、CPU/内存使用情况、网络统计信息或 Prometheus 收集的任何指标时，可使用该功能。支持对多个 Prometheus 实例进行聚合查询，并支持配置文件或环境变量的配置，同时支持 HTTP Basic Auth 认证。
---
# Prometheus Skill

该技能用于从一个或多个Prometheus实例中查询监控数据。支持通过单个命令跨多个Prometheus服务器进行数据查询。

## 快速入门

### 1. 初始设置

运行交互式配置向导：

```bash
cd ~/.openclaw/workspace/skills/prometheus
node scripts/cli.js init
```

这将为您的OpenClaw工作空间创建一个`prometheus.json`配置文件（路径：`~/.openclaw/workspace/prometheus.json`）。

### 2. 开始查询

```bash
# Query default instance
node scripts/cli.js query 'up'

# Query all instances at once
node scripts/cli.js query 'up' --all

# List configured instances
node scripts/cli.js instances
```

## 配置

### 配置文件的位置

默认情况下，该技能会在您的OpenClaw工作空间中查找配置文件：

```
~/.openclaw/workspace/prometheus.json
```

**配置文件的查找优先级：**
1. `PROMETHEUS_CONFIG`环境变量指定的路径
2. `~/.openclaw/workspace/prometheus.json`
3. `~/.openclaw/workspace/config/prometheus.json`
4. `./prometheus.json`（当前目录）
5. `~/.config/prometheus/config.json`

### 配置格式

在工作空间中创建`prometheus.json`文件（或使用`node cli.js init`命令进行初始化）：

```json
{
  "instances": [
    {
      "name": "production",
      "url": "https://prometheus.example.com",
      "user": "admin",
      "password": "secret"
    },
    {
      "name": "staging",
      "url": "http://prometheus-staging:9090"
    }
  ],
  "default": "production"
}
```

**配置字段：**
- `name` — 实例的唯一标识符
- `url` — Prometheus服务器的URL
- `user` / `password` — 可选的HTTP Basic认证凭据
- `default` — 当未指定实例时使用的默认实例

### 环境变量（旧版本）

对于单实例设置，您可以使用环境变量来配置：

```bash
export PROMETHEUS_URL=https://prometheus.example.com
export PROMETHEUS_USER=admin        # optional
export PROMETHEUS_PASSWORD=secret   # optional
```

## 使用方法

### 全局参数

| 参数 | 说明 |
|------|-------------|
| `-c, --config <路径>` | 配置文件的路径 |
| `-i, --instance <名称>` | 目标实例的名称 |
| `-a, --all` | 查询所有已配置的实例 |

### 命令

#### 配置设置

```bash
# Interactive configuration wizard
node scripts/cli.js init
```

#### 查询指标数据

```bash
cd ~/.openclaw/workspace/skills/prometheus

# Query default instance
node scripts/cli.js query 'up'

# Query specific instance
node scripts/cli.js query 'up' -i staging

# Query ALL instances at once
node scripts/cli.js query 'up' --all

# Custom config file
node scripts/cli.js query 'up' -c /path/to/config.json
```

#### 常见查询

- **磁盘空间使用情况：**  
  ```prometheus
  SELECT node_filesystem_avail_bytes / node_filesystem_size_bytes * 100
  ```

- **CPU使用情况：**  
  ```prometheus
  SELECT avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m]) * 100
  ```

- **内存使用情况：**  
  ```prometheus
  SELECT (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100
  ```

- **平均负载：**  
  ```prometheus
  SELECT avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])
  ```

### 列出已配置的实例

```bash
node scripts/cli.js instances
```

查询结果输出：  
```json
{
  "default": "production",
  "instances": [
    { "name": "production", "url": "https://prometheus.example.com", "hasAuth": true },
    { "name": "staging", "url": "http://prometheus-staging:9090", "hasAuth": false }
  ]
}
```

### 其他命令

```bash
# List all metrics matching pattern
node scripts/cli.js metrics 'node_memory_*'

# Get label names
node scripts/cli.js labels --all

# Get values for a label
node scripts/cli.js label-values instance --all

# Find time series
node scripts/cli.js series '{__name__=~"node_cpu_.*", instance=~".*:9100"}' --all

# Get active alerts
node scripts/cli.js alerts --all

# Get scrape targets
node scripts/cli.js targets --all
```

## 多实例查询结果格式

当使用`--all`参数时，查询结果将包含所有实例的数据：

```json
{
  "resultType": "vector",
  "results": [
    {
      "instance": "production",
      "status": "success",
      "resultType": "vector",
      "result": [...]
    },
    {
      "instance": "staging",
      "status": "success",
      "resultType": "vector",
      "result": [...]
    }
  ]
}
```

如果某个实例出现错误，整个查询不会失败；错误信息会以`"status": "error"`的形式显示在结果数组中。

## 常见查询示例

| 指标 | PromQL查询语句 |
|--------|--------------|
| 磁盘空闲百分比 | `node_filesystem_avail_bytes / node_filesystem_size_bytes * 100` |
| 磁盘使用百分比 | `100 - (node_filesystem_avail_bytes / node_filesystem_size_bytes * 100)` |
| CPU空闲百分比 | `avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m]) * 100` |
| 内存使用百分比 | `(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100` |
| 网络接收数据量 | `rate(node_network_receive_bytes_total[5m])` |
| 网络发送数据量 | `rate(node_network_transmit_bytes_total[5m])` |
| 运行时间 | `node_time_seconds - node_boot_time_seconds` |
| 服务状态 | `up` |

## 注意事项

- 即时查询的时间范围默认为过去1小时。
- 使用`[5m]`时间范围进行速率计算。
- 所有查询返回的JSON结果中包含`data.result`字段。
- 实例标签通常采用`host:port`的格式。
- 使用`--all`参数时，查询会并行执行以提高效率。
- 配置文件存储在工作空间外部，因此会在技能更新后仍然保留。