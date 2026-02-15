---
name: pulse
description: 通过 REST API 查询和控制 Pulse 监控系统。该 API 用于检查基础设施的健康状况、资源状态（节点/虚拟机/容器/存储设备）、各项指标、警报信息以及进行系统管理。支持使用 API 令牌或会话进行身份验证。当用户需要查询 Pulse 的运行状态、进行基础设施监控，或需要以编程方式与 Pulse 仪表板交互时，可以使用该 API。
---

# Pulse监控API

这是一个用于与Pulse基础设施监控系统交互的命令行工具（CLI）。

## 配置

设置环境变量或传递参数：
- `PULSE_URL` - 基础URL（默认值：`https://demo.pulserelay.pro`）
- `PULSE_TOKEN` - 用于身份验证的API令牌（已预先配置）

## 快速入门

```bash
# Check system health
pulse health

# Get complete infrastructure state
pulse state

# Get resource summary
pulse resources --stats

# View specific resource
pulse resource <resource-id>

# Get metrics for a time range
pulse metrics --range 24h
```

## 核心操作

### 系统健康检查
```bash
pulse health
# Returns: status, uptime, timestamp
```

### 基础设施状态
```bash
pulse state
# Complete state: Nodes, VMs, Containers, Storage, Alerts
```

### 资源管理
```bash
pulse resources              # List all resources
pulse resources --stats      # Summary counts and health
pulse resource <id>          # Single resource details
```

### 指标与图表
```bash
pulse metrics --range 1h     # CPU, Memory, Storage charts
pulse metrics --range 24h
pulse metrics --range 7d

# Available ranges: 5m, 15m, 30m, 1h, 4h, 12h, 24h, 7d

pulse storage-stats          # Detailed storage usage
pulse backups                # Unified backup history
```

### 通知设置
```bash
pulse test-notification      # Send test alert
pulse notification-health    # Check notification system
```

### 更新通知
```bash
pulse updates check          # Check for Pulse updates
pulse updates status         # Current update status
pulse updates apply          # Apply available updates
```

## 高级功能

### 代理管理
```bash
pulse agents list            # List all agents
pulse agent <id> config      # Get agent configuration
pulse agent <id> unlink      # Unlink agent from node
```

### 安全性
```bash
pulse tokens list            # List API tokens
pulse token create --name "automation" --scopes "monitoring:read"
pulse token revoke <id>      # Revoke token
```

### AI功能（专业版）
```bash
pulse ai status              # AI patrol status
pulse ai findings            # Current AI findings
pulse ai run                 # Trigger AI patrol run
```

## 环境设置

在`~/.local/bin/pulse`目录下创建一个辅助脚本：

```bash
#!/bin/bash
# Pulse CLI wrapper
PULSE_URL="${PULSE_URL:-https://demo.pulserelay.pro}"
PULSE_TOKEN="${PULSE_TOKEN:-a4b819a65b8d41318d167356dbf5be2c70b0bbf7d5fd4687bbf325a6a61819e0}"

endpoint="$1"
shift

curl -s -H "X-API-Token: $PULSE_TOKEN" \
     "${PULSE_URL}/api/${endpoint}" "$@" | jq
```

使其可执行：
```bash
chmod +x ~/.local/bin/pulse
```

## 常见操作模式

### 获取主机的RAM使用情况
```bash
pulse state | jq '.hosts[] | {name: .displayName, memory}'
```

### 列出CPU使用率较高的所有容器
```bash
pulse state | jq '.containers[] | select(.cpu > 80)'
```

### 查看警报信息
```bash
pulse state | jq '.alerts'
```

### 将指标数据导出为JSON格式
```bash
pulse metrics --range 24h > metrics-$(date +%Y%m%d).json
```

## 身份验证方式

### API令牌（推荐使用）
```bash
curl -H "X-API-Token: your-token" http://pulse:7655/api/health
```

### 承载令牌（Bearer Token）
```bash
curl -H "Authorization: Bearer your-token" http://pulse:7655/api/health
```

### 会话Cookie
由Web UI自动使用。

## 参考文件

- **[API.md](references/API.md)** - 完整的API端点参考文档
- **[examples.sh](scripts/examples.sh)** - 常见的API使用示例

## 注意事项

- 大多数API端点需要身份验证（`/health`和`/version`端点除外）
- 部分API端点需要管理员权限或特定的访问权限范围
- 专业版功能需要Pulse Pro许可证
- 默认基础URL：`https://demo.pulserelay.pro/api`