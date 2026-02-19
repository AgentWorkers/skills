---
name: agentic-devops
version: 1.0.0
description: 这款生产级代理的DevOps工具包集成了Docker容器管理、进程监控、日志分析以及系统健康状况监测等功能。它由实际负责生产环境运维的工程师团队开发而成。
author: CacheForge
license: MIT
homepage: https://app.anvil-ai.io
user-invocable: true
tags:
  - cacheforge
  - devops
  - docker
  - monitoring
  - log-analysis
  - health-check
  - infrastructure
  - sre
  - discord
  - discord-v2
metadata: {"openclaw":{"emoji":"🛠️","homepage":"https://app.anvil-ai.io","requires":{"bins":["python3"]}}}
---
## 何时使用此技能

当用户需要执行以下操作时，可以使用此技能：
- 运行系统诊断或健康检查
- 管理 Docker 容器（状态、日志、健康状况、组合配置）
- 检查正在运行的进程、端口或资源占用情况
- 分析日志文件以查找错误、模式或频率信息
- 检查 HTTP 端点的可用性或端口状态
- 通过一个命令快速获取系统的整体概览

## 命令

### 快速诊断（从这里开始）

```bash
# Full system health report — CPU, memory, disk, Docker, ports, errors, top processes
python3 skills/agentic-devops/devops.py diag
```

### Docker 操作

```bash
# Container status overview
python3 skills/agentic-devops/devops.py docker status

# Tail container logs with pattern filtering
python3 skills/agentic-devops/devops.py docker logs <container> --tail 100 --grep "error|warn"

# Docker health summary (running, stopped, unhealthy)
python3 skills/agentic-devops/devops.py docker health

# Docker Compose service status
python3 skills/agentic-devops/devops.py docker compose-status --file docker-compose.yml
```

### 进程管理

```bash
# List processes sorted by resource usage
python3 skills/agentic-devops/devops.py proc list --sort cpu

# Show ports in use
python3 skills/agentic-devops/devops.py proc ports

# Detect zombie processes
python3 skills/agentic-devops/devops.py proc zombies
```

### 日志分析

```bash
# Analyze log file for error patterns
python3 skills/agentic-devops/devops.py logs analyze /var/log/syslog --pattern "error|fail|critical"

# Tail log file with highlighted patterns
python3 skills/agentic-devops/devops.py logs tail /var/log/app.log --highlight "ERROR|WARN"

# Frequency analysis of log patterns
python3 skills/agentic-devops/devops.py logs frequency /var/log/app.log --top 20
```

### 健康检查

```bash
# Check HTTP endpoint health
python3 skills/agentic-devops/devops.py health check https://myapp.com/healthz

# Scan specific ports
python3 skills/agentic-devops/devops.py health ports 80,443,8080,5432

# System resource health (CPU, memory, disk)
python3 skills/agentic-devops/devops.py health system
```

## 要求

- Python 3.8 及以上版本（仅需要标准库，无需外部依赖）
- Docker CLI（可选；如果未安装，相关功能仍可正常使用）
- 标准的 Unix 工具（如 ps、ss/netstat）