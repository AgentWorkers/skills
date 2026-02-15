---
description: 为自托管服务、Docker容器以及家庭实验室基础设施生成一个状态监控仪表板。
---

# 家庭实验室仪表板

用于检查家庭实验室服务及基础设施的运行状况和健康状态。

**适用场景**：用于查看服务状态、监控 Docker 容器或获取家庭实验室的总体情况。

## 前提条件**

- 需要一个安装了标准工具（`free`、`df`、`uptime`）的 Linux 系统。
- 可选：Docker、systemd、curl。
- 不需要 API 密钥。

## 操作步骤

1. **系统资源检查**：
   ```bash
   nproc                          # CPU cores
   uptime                         # load average
   free -h                        # memory usage
   df -h / /mnt/* 2>/dev/null     # disk usage (root + mounts)
   ```

2. **Docker 容器检查**（如果已安装 Docker）：
   ```bash
   docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' 2>/dev/null
   docker ps -a --filter "status=exited" --format '{{.Names}}\t{{.Status}}' 2>/dev/null
   ```

3. **HTTP 健康检查**（如果用户提供了相应的 URL）：
   ```bash
   curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 --max-time 10 <url>
   ```
   - 200-299：🟢 运行正常
   - 300-399：🟡 重定向
   - 400+：🔴 错误
   - 无响应：🔴 服务停止

4. **systemd 服务检查**（如果指定了相关服务）：
   ```bash
   systemctl is-active <service>
   systemctl is-failed <service>  # check for failed services
   ```

5. **输出格式**：
   ```
   🏠 Homelab Dashboard — 2025-01-15 14:30 JST

   ## 💻 System Resources
   | Resource | Usage | Status |
   |----------|-------|--------|
   | CPU | 4 cores, load 1.2 | 🟢 Normal |
   | Memory | 6.2G / 16G (39%) | 🟢 Normal |
   | Disk / | 120G / 500G (24%) | 🟢 Normal |
   | Disk /mnt/hdd | 2.1T / 2.7T (78%) | 🟡 Warning |

   ## 🐳 Docker Containers
   | Container | Status | Ports |
   |-----------|--------|-------|
   | nginx | 🟢 Up 3 days | 80, 443 |
   | postgres | 🟢 Up 3 days | 5432 |
   | redis | 🔴 Exited (1) 2h ago | — |

   ## 🌐 Services
   | Service | Status | Response |
   |---------|--------|----------|
   | Nextcloud | 🟢 200 OK | 142ms |
   | Gitea | 🔴 Connection refused | — |

   ## ⚠️ Alerts
   - 🔴 redis container is down (exited with code 1)
   - 🔴 Gitea is unreachable
   - 🟡 /mnt/hdd disk usage at 78% — consider cleanup
   ```

6. **警报阈值**：
   - 磁盘使用率 > 85%：🔴 严重警告
   - 磁盘使用率 > 70%：🟡 警告
   - 内存使用率 > 90%：🔴 严重警告
   - 系统负载超过 CPU 核心数的 2 倍：🟡 警告
   - 有任何停止的容器或失败的服务：🔴 严重警告

## 特殊情况处理**

- **未安装 Docker**：跳过容器检查部分，并在输出中说明。
- **权限不足**：某些命令需要 `sudo` 权限。请报告无法执行检查的操作。
- **远程主机**：使用 SSH (`ssh 用户@主机 "命令"`) 来检查远程机器。
- **未指定服务**：仅执行系统检查和 Docker 容器的检查。

## 安全注意事项**

- 不要在共享的输出中暴露内部服务 URL 或 IP 地址。
- 健康检查 URL 可能包含敏感信息（如令牌），请在输出中对其进行屏蔽处理。