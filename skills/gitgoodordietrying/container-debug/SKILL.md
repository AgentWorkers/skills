---
name: container-debug
description: 调试正在运行的 Docker 容器和 Compose 服务。适用于检查容器日志、在运行中的容器内执行命令、诊断网络问题、查看资源使用情况、调试多阶段构建过程、排查健康检查（health check）故障，以及修复 Compose 服务的依赖关系问题。
metadata: {"clawdbot":{"emoji":"🐳","requires":{"bins":["docker"]},"os":["linux","darwin","win32"]}}
---

# 容器调试

本文档介绍了如何调试正在运行的 Docker 容器和 Compose 服务，涵盖了日志查看、容器内命令执行、网络配置、资源监控、多阶段构建、健康检查以及常见的故障处理方法。

## 适用场景

- 容器启动后立即退出或崩溃
- 容器内的应用程序行为与主机上的应用程序不同
- 容器之间无法互相通信
- 容器使用过多内存或 CPU 资源
- 多阶段 Docker 构建产生意外结果
- 健康检查失败
- Compose 服务启动顺序错误或无法正常连接

## 容器日志

### 查看和过滤日志
```bash
# Last 100 lines
docker logs --tail 100 my-container

# Follow (stream) logs
docker logs -f my-container

# Follow with timestamps
docker logs -f -t my-container

# Logs since a time
docker logs --since 30m my-container
docker logs --since "2026-02-03T10:00:00" my-container

# Logs between times
docker logs --since 1h --until 30m my-container

# Compose: logs for all services
docker compose logs -f

# Compose: logs for specific service
docker compose logs -f api db

# Redirect logs to file for analysis
docker logs my-container > container.log 2>&1

# Separate stdout and stderr
docker logs my-container > stdout.log 2> stderr.log
```

### 检查日志驱动程序
```bash
# Check what log driver a container uses
docker inspect --format='{{.HostConfig.LogConfig.Type}}' my-container

# If json-file driver, find the actual log file
docker inspect --format='{{.LogPath}}' my-container

# Check log file size
ls -lh $(docker inspect --format='{{.LogPath}}' my-container)
```

## 在容器内执行命令

### 交互式 shell
```bash
# Bash (most common)
docker exec -it my-container bash

# If bash isn't available (Alpine, distroless)
docker exec -it my-container sh

# As root (even if container runs as non-root user)
docker exec -u root -it my-container bash

# With specific environment variables
docker exec -e DEBUG=1 -it my-container bash

# Run a single command (no interactive shell)
docker exec my-container cat /etc/os-release
docker exec my-container ls -la /app/
docker exec my-container env
```

### 调试崩溃的容器
```bash
# Container exited? Check exit code
docker inspect --format='{{.State.ExitCode}}' my-container
docker inspect --format='{{.State.Error}}' my-container

# Common exit codes:
# 0   = clean exit
# 1   = application error
# 137 = killed (OOM or docker kill) — 128 + signal 9
# 139 = segfault — 128 + signal 11
# 143 = terminated (SIGTERM) — 128 + signal 15

# Start a stopped container to debug it
docker start -ai my-container

# Or override the entrypoint to get a shell
docker run -it --entrypoint sh my-image

# Copy files out of a stopped container
docker cp my-container:/app/error.log ./error.log
docker cp my-container:/etc/nginx/nginx.conf ./nginx.conf
```

### 在无 shell 的环境中进行调试（例如使用 distroless 或 scratch 镜像）
```bash
# Use docker cp to extract files
docker cp my-container:/app/config.json ./

# Use nsenter to get a shell in the container's namespace (Linux)
PID=$(docker inspect --format='{{.State.Pid}}' my-container)
nsenter -t $PID -m -u -i -n -p -- /bin/sh

# Attach a debug container to the same namespace
docker run -it --pid=container:my-container --net=container:my-container busybox sh

# Docker Desktop: use debug extension
docker debug my-container
```

## 网络配置

### 检查容器网络
```bash
# Show container IP address
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my-container

# Show all network details
docker inspect -f '{{json .NetworkSettings.Networks}}' my-container | jq

# List all networks
docker network ls

# Inspect a network (see all connected containers)
docker network inspect bridge
docker network inspect my-compose-network

# Show port mappings
docker port my-container
```

### 测试容器之间的连通性
```bash
# From inside container A, reach container B
docker exec container-a ping container-b
docker exec container-a curl http://container-b:8080/health

# DNS resolution inside container
docker exec my-container nslookup db
docker exec my-container cat /etc/resolv.conf
docker exec my-container cat /etc/hosts

# Test if port is reachable
docker exec my-container nc -zv db 5432
docker exec my-container wget -qO- http://api:3000/health

# If curl/ping not available in container, install or use a debug container:
docker run --rm --network container:my-container curlimages/curl curl -s http://localhost:8080
```

### 常见的网络问题
```bash
# "Connection refused" between containers
# 1. Check the app binds to 0.0.0.0, not 127.0.0.1
docker exec my-container netstat -tlnp
# If listening on 127.0.0.1 — fix the app config

# 2. Check containers are on the same network
docker inspect -f '{{json .NetworkSettings.Networks}}' container-a | jq 'keys'
docker inspect -f '{{json .NetworkSettings.Networks}}' container-b | jq 'keys'

# 3. Check published ports vs exposed ports
# EXPOSE only documents, it doesn't publish
# Use -p host:container to publish

# "Name not found" — DNS not resolving container names
# Container names resolve only on user-defined networks, NOT the default bridge
docker network create my-net
docker run --network my-net --name api my-api-image
docker run --network my-net --name db postgres
# Now "api" and "db" resolve to each other
```

### 捕获网络流量
```bash
# tcpdump inside a container
docker exec my-container tcpdump -i eth0 -n port 8080

# If tcpdump not available, use a sidecar
docker run --rm --net=container:my-container nicolaka/netshoot tcpdump -i eth0 -n

# netshoot has: tcpdump, curl, nslookup, netstat, iperf, etc.
docker run --rm --net=container:my-container nicolaka/netshoot bash
```

## 资源使用情况

### 实时资源统计
```bash
# All containers
docker stats

# Specific containers
docker stats api db redis

# One-shot (no streaming)
docker stats --no-stream

# Formatted output
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
```

### 内存使用情况分析
```bash
# Check memory limit
docker inspect --format='{{.HostConfig.Memory}}' my-container
# 0 means unlimited

# Check if container was OOM-killed
docker inspect --format='{{.State.OOMKilled}}' my-container

# Memory usage breakdown (Linux cgroups)
docker exec my-container cat /sys/fs/cgroup/memory.current 2>/dev/null || \
docker exec my-container cat /sys/fs/cgroup/memory/memory.usage_in_bytes

# Process memory inside container
docker exec my-container ps aux --sort=-%mem | head -10
docker exec my-container top -bn1
```

### 磁盘使用情况
```bash
# Overall Docker disk usage
docker system df
docker system df -v

# Container filesystem size
docker inspect --format='{{.SizeRw}}' my-container

# Find large files inside container
docker exec my-container du -sh /* 2>/dev/null | sort -rh | head -10
docker exec my-container find /tmp -size +10M -type f

# Check for log file bloat
docker exec my-container ls -lh /var/log/
```

## Dockerfile 调试

### 多阶段构建调试
```bash
# Build up to a specific stage
docker build --target builder -t my-app:builder .

# Inspect what's in the builder stage
docker run --rm -it my-app:builder sh
docker run --rm my-app:builder ls -la /app/
docker run --rm my-app:builder cat /app/package.json

# Check which files made it to the final image
docker run --rm my-image ls -laR /app/

# Build with no cache (fresh build)
docker build --no-cache -t my-app .

# Build with progress output
docker build --progress=plain -t my-app .
```

### 镜像检查
```bash
# Show image layers (size of each)
docker history my-image
docker history --no-trunc my-image

# Inspect image config (entrypoint, cmd, env, ports)
docker inspect my-image | jq '.[0].Config | {Cmd, Entrypoint, Env, ExposedPorts, WorkingDir}'

# Compare two images
docker history image-a --format "{{.Size}}\t{{.CreatedBy}}" > layers-a.txt
docker history image-b --format "{{.Size}}\t{{.CreatedBy}}" > layers-b.txt
diff layers-a.txt layers-b.txt

# Find what changed between builds
docker diff my-container
# A = added, C = changed, D = deleted
```

## 健康检查

### 定义和调试健康检查规则
```dockerfile
# In Dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
```

### Docker Compose 调试

### 服务启动问题
```bash
# Check service status
docker compose ps

# See why a service failed
docker compose logs failed-service

# Start with verbose output
docker compose up --build 2>&1 | tee compose.log

# Start a single service (with dependencies)
docker compose up db

# Start without dependencies
docker compose up --no-deps api

# Recreate containers from scratch
docker compose up --force-recreate --build

# Check effective config (after variable substitution)
docker compose config
```

### 服务依赖关系及启动顺序
```yaml
# docker-compose.yml
services:
  api:
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5
```

### 服务清理
```bash
# Wait for a service to be healthy before running commands
docker compose up -d db
docker compose exec db pg_isready  # Polls until ready
docker compose up -d api
```

## 提示

- 首先使用 `docker logs -f` 命令查看日志。大多数容器故障问题都可以在日志中找到线索。
- 出错代码 137 表示容器因内存不足（OOM）而终止。请增加内存限制或修复内存泄漏问题。
- 容器内的应用程序应绑定到 `0.0.0.0` 地址，而不是 `127.0.0.1`（主机地址）。容器内的 localhost 是隔离的。
- 容器名称仅在使用用户自定义网络时才能通过 DNS 解析，不能使用默认的 `bridge` 网络。在多容器环境中务必创建自定义网络。
- `docker exec` 命令仅适用于正在运行的容器。对于崩溃的容器，可以使用 `docker cp` 命令提取日志，或者通过 `docker run --entrypoint sh` 替换容器的入口点命令。
- `nicolaka/netshoot` 是一个非常实用的工具，集成了多种容器网络调试工具。
- 在构建过程中使用 `--progress=plain` 选项可以显示完整的命令输出，这对调试构建错误非常有用。
- 健康检查中的 `start-period` 参数可以防止应用程序启动缓慢时出现错误的状态显示。