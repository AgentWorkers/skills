# LibreNMS 技能

通过 LibreNMS 的 REST API 监控网络基础设施。该技能仅支持读取设备状态、健康传感器数据、端口统计信息以及警报信息。

## 配置

创建 `~/.openclaw/credentials/librenms/config.json` 文件：
```json
{
  "url": "https://librenms.example.com",
  "api_token": "your-api-token-here"
}
```

或者设置环境变量：
- `LIBRENMS_URL` — LibreNMS 实例的基地址
- `LIBRENMS_TOKEN` — API 认证令牌

## 命令

### 快速概览
```bash
librenms summary
```
仪表盘视图显示总设备数量、处于运行/关闭状态的设备数量以及活跃警报的数量。首先使用此命令获取快速的状态概览。

### 设备管理
```bash
librenms devices           # List all devices with status, IP, OS, uptime
librenms down             # Show ONLY devices that are down (critical for alerting)
librenms device <hostname> # Detailed info: hardware, serial, location, OS version
```

### 健康监控
```bash
librenms health <hostname> # Temperature, CPU, memory, disk usage sensors
librenms ports <hostname>  # Network interfaces with traffic stats
```

### 警报
```bash
librenms alerts           # Show active/unresolved alerts with severity and timestamps
```

## 使用场景

**每日健康检查：**
```bash
librenms summary && librenms down && librenms alerts
```

**查询特定设备：**
```bash
librenms device switch-core-01
librenms health switch-core-01
librenms ports switch-core-01
```

**快速排查故障设备：**
```bash
librenms down | grep -v "UP"
```

## 重要说明

- 所有操作均为 **只读** — 无法修改设备状态
- 该脚本支持使用自签名证书（使用 `-sk` 标志通过 `curl` 进行请求）
- 状态指示：● 绿色 = 运行中，● 红色 = 关闭
- 运行时间以人类可读的形式显示（天/小时而非秒）
- 流量统计数据以 KB/MB/GB/秒为单位显示

## 心跳检测集成

定期检查基础设施的健康状况：
```bash
# In heartbeat script
if librenms down | grep -q "Devices Down"; then
    # Alert on down devices
    librenms down
fi

# Check for active alerts
if librenms alerts | grep -q "Active Alerts"; then
    librenms alerts
fi
```

## 所需依赖库

- `curl` — 用于发起 API 请求
- `jq` — 用于解析 JSON 数据
- `bc` — 用于数字格式化（可选，用于字节转换）

## API 接口

支持的 API 端点：
- `/api/v0/devices` — 所有设备信息
- `/api/v0/devices/{hostname}` — 单个设备详情
- `/api/v0/devices/{hostname}/health` — 设备健康状态
- `/api/v0/devices/{hostname}/ports` — 网络端口信息
- `/api/v0/alerts?state=1` — 未解决的警报信息

完整的 API 文档：https://docs.librenms.org/API/

## 故障排除

**“配置文件未找到”**
创建 `~/.openclaw/credentials/librenms/config.json` 文件或设置环境变量。

**“API 返回 HTTP 401 错误”**
检查您的 API 令牌是否正确。可以在 LibreNMS 的“设置” → “API”选项中生成新的令牌。

**“无法连接”**
确认 URL 是否正确，并检查 LibreNMS 实例是否可访问。同时检查防火墙规则。

**关于自签名证书的警告**
该脚本使用 `-sk` 标志忽略证书验证（在 LibreNMS 的常见配置中）。如果您需要严格的证书验证，请编辑脚本并移除 `-k` 标志。