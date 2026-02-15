---
name: port-check
version: 1.0.0
description: 检查指定主机和端口号对上的服务是否响应。支持TCP和HTTP协议的检测，并可配置超时时间。适用于服务监控、健康状况检查以及网络故障排查。
metadata: {"clawdbot":{"emoji":"🔌","requires":{"bins":["nc","curl"]}}}
---
# 端口检查技能

快速验证服务是否在特定端口上运行并响应请求。

## 使用方法

```bash
# Basic TCP check
bash scripts/port-check.sh localhost:8080 localhost:5432

# Multiple targets with HTTP status check
bash scripts/port-check.sh localhost:80 api.example.com:443 --http

# Custom timeout (default 3s)
bash scripts/port-check.sh 192.168.1.1:22 --timeout 5
```

## 输出结果：
- ✅ `host:port — 开放`（TCP连接成功）
- ✅ `host:port — 开放（HTTP 200状态码）`（使用了`--http`参数）
- ⚠️ `host:port — 开放，但HTTP状态码为500`（端口开放，但返回了错误的HTTP状态码）
- ❌ `host:port — 关闭/超时`（没有响应）

## 退出代码：
- `0` — 所有目标服务均正常运行
- `1` — 一个或多个目标服务未正常运行

## 常用检查项
```bash
# OpenClaw gateway
bash scripts/port-check.sh localhost:18789 --http

# Database + web stack
bash scripts/port-check.sh localhost:5432 localhost:6379 localhost:3000

# Home network devices
bash scripts/port-check.sh 192.168.1.1:80 192.168.1.50:22 --timeout 2
```