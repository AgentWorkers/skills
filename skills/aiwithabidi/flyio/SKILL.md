---
name: flyio
description: "Fly.io 边缘部署平台：通过 Fly.io Machines API 管理应用程序、服务器、存储卷、密钥以及证书。支持全球范围内部署容器、实现零扩展（即无需额外资源即可应对负载变化）、管理持久化存储，并配置网络连接。该平台专为 AI 代理设计，仅依赖 Python 标准库，无任何外部依赖项。适用于边缘计算部署、容器管理、全球分发、无服务器架构扩展以及基础设施自动化场景。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "✈️", "requires": {"env": ["FLY_API_TOKEN"]}, "primaryEnv": "FLY_API_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# ✈️ Fly.io

Fly.io 是一个边缘部署平台，通过 Fly.io Machines API 管理应用程序、机器、存储卷、机密信息和证书。

## 主要功能

- **应用程序管理**：创建、列出和配置应用程序
- **机器操作**：启动、停止和重启机器
- **存储卷管理**：提供持久化存储服务
- **机密信息管理**：安全存储环境机密
- **证书管理**：自动配置 SSL/TLS 证书
- **扩展性**：可自动扩展机器数量，并支持自动停止不需要的机器
- **区域选择**：将应用程序部署到特定的全球区域
- **健康检查**：监控机器的运行状态
- **网络配置**：分配 IP 地址和配置私有网络
- **部署**：支持滚动部署，并提供“金丝雀”（canary）部署机制

## 所需条件

| 变量 | 必需条件 | 说明 |
|----------|----------|-------------|
| `FLY_API_TOKEN` | ✅ | Fly.io 的 API 密钥/令牌 |

## 快速入门

```bash
# List apps
python3 {baseDir}/scripts/flyio.py apps --limit 20
```

```bash
# Get app details
python3 {baseDir}/scripts/flyio.py app-get my-app
```

```bash
# Create an app
python3 {baseDir}/scripts/flyio.py app-create '{"app_name":"my-service","org_slug":"personal"}'
```

```bash
# List machines
python3 {baseDir}/scripts/flyio.py machines --app my-app
```



## 命令

### `apps`
列出所有应用程序。
```bash
python3 {baseDir}/scripts/flyio.py apps --limit 20
```

### `app-get`
获取应用程序的详细信息。
```bash
python3 {baseDir}/scripts/flyio.py app-get my-app
```

### `app-create`
创建一个新的应用程序。
```bash
python3 {baseDir}/scripts/flyio.py app-create '{"app_name":"my-service","org_slug":"personal"}'
```

### `machines`
列出所有机器。
```bash
python3 {baseDir}/scripts/flyio.py machines --app my-app
```

### `machine-get`
获取机器的详细信息。
```bash
python3 {baseDir}/scripts/flyio.py machine-get --app my-app mach_abc123
```

### `machine-start`
启动一台机器。
```bash
python3 {baseDir}/scripts/flyio.py machine-start --app my-app mach_abc123
```

### `machine-stop`
停止一台机器。
```bash
python3 {baseDir}/scripts/flyio.py machine-stop --app my-app mach_abc123
```

### `machine-create`
创建一台新的机器。
```bash
python3 {baseDir}/scripts/flyio.py machine-create --app my-app '{"config":{"image":"nginx:latest","guest":{"cpus":1,"memory_mb":256}}}'
```

### `volumes`
列出所有存储卷。
```bash
python3 {baseDir}/scripts/flyio.py volumes --app my-app
```

### `volume-create`
创建一个新的存储卷。
```bash
python3 {baseDir}/scripts/flyio.py volume-create --app my-app '{"name":"data","size_gb":10,"region":"ord"}'
```

### `secrets`
列出所有机密信息。
```bash
python3 {baseDir}/scripts/flyio.py secrets --app my-app
```

### `secret-set`
设置一个机密信息。
```bash
python3 {baseDir}/scripts/flyio.py secret-set --app my-app "DATABASE_URL" "postgres://..."
```

### `certs`
列出所有证书。
```bash
python3 {baseDir}/scripts/flyio.py certs --app my-app
```

### `regions`
列出所有可用的区域。
```bash
python3 {baseDir}/scripts/flyio.py regions
```

### `status`
查看应用程序的运行状态。
```bash
python3 {baseDir}/scripts/flyio.py status --app my-app
```


## 输出格式

所有命令默认以 JSON 格式输出。若需以易读的格式输出，请添加 `--human` 参数。

```bash
# JSON (default, for programmatic use)
python3 {baseDir}/scripts/flyio.py apps --limit 5

# Human-readable
python3 {baseDir}/scripts/flyio.py apps --limit 5 --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/flyio.py` | 主要的命令行工具（CLI），用于执行所有 Fly.io 操作 |

## 数据政策

本工具 **绝不将数据存储在本地**。所有请求都会直接发送到 Fly.io 的 API，结果会返回到标准输出（stdout）。您的数据将保存在 Fly.io 的服务器上。

## 致谢
---
由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai) 开发
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)
作为 OpenClaw 代理的 **AgxntSix Skill Suite** 的一部分。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)