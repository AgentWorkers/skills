# 系统诊断工具

这是一个专为 DevOps 工程师和系统管理员设计的全面系统诊断与故障排除工具包。

## 概述

系统诊断工具为你的 AI 代理提供了强大的工具，用于诊断和解决基础设施问题。非常适合以下场景：
- 服务器健康监控
- 性能故障排除
- 日志分析
- 网络连接测试
- 服务状态检查

## 工具

### `run_diagnostic`
执行常见的诊断命令，如 `df -h`、`free -m`、`ps aux`、`netstat` 等。

```
Check disk space: run_diagnostic with command "df -h"
Check memory: run_diagnostic with command "free -m"
List processes: run_diagnostic with command "ps aux --sort=-%cpu | head -20"
```

### `read_log`
读取日志文件以帮助进行故障排除。

```
Read nginx logs: read_log with path "/var/log/nginx/error.log" and lines 100
Read system logs: read_log with path "/var/log/syslog"
```

### `check_service`
检查 systemd 服务的状态。

```
Check nginx: check_service with name "nginx"
Check docker: check_service with name "docker"
```

### `network_check`
使用 ping、curl 或 DNS 查找来测试网络连接。

```
Ping a host: network_check with host "google.com" and method "ping"
Check HTTP: network_check with host "https://api.example.com" and method "curl"
DNS lookup: network_check with host "example.com" and method "dns"
```

### `system_summary`
获取包括 CPU、内存、磁盘和顶级进程在内的系统概览。

```
Get system summary: system_summary
```

## 隐私政策

该工具会收集匿名使用数据以帮助改进产品。收集的数据包括：
- 工具使用次数
- 平台信息（操作系统、架构）
- 错误率

不会收集任何个人数据、文件内容或命令输出。

如需禁用数据收集，请在环境中设置 `DIAGNOSTICS_TELEMETRY=false`。

## 系统要求

- Node.js 18 及以上版本
- Linux 或 macOS 操作系统
- 标准系统工具（bash、ps、df、free 等）

## 许可证

MIT 许可证 - DevOps Tools Inc.