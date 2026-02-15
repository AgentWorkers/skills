---
description: 生成系统健康报告，其中包含CPU、内存、磁盘和网络的相关诊断信息以及相应的建议。
---

# 系统健康报告工具

提供全面的系统健康检查，包括严重性评分和可操作的改进建议。

## 系统要求

- Linux 发行版：Ubuntu、Debian、RHEL、Arch
- 必需安装的标准工具：`ps`、`top`、`free`、`df`、`uptime`、`systemctl`
- 基本检查无需 root 权限（部分操作可能需要 sudo）

## 使用说明

### 第一步：收集系统指标数据

```bash
uname -a && uptime                                    # System info
nproc && cat /proc/loadavg                            # CPU & load
free -h                                               # Memory & swap
df -h --exclude-type=tmpfs --exclude-type=devtmpfs --exclude-type=squashfs  # Disk
ip -brief addr                                        # Network interfaces
ss -tulnp 2>/dev/null | head -20                      # Listening ports
systemctl list-units --state=failed --no-pager 2>/dev/null   # Failed services
ps aux | awk '$8 ~ /Z/ {print}'                       # Zombie processes
ps aux --sort=-%mem | head -6                         # Top memory
ps aux --sort=-%cpu | head -6                         # Top CPU
last -5 2>/dev/null && who                            # Login activity
```

### 第二步：对各个系统指标进行评分

| 指标 | 健康 | 警告 | 危急 |
|------|-------|--------|--------|
| CPU 使用率 | < 0.8 × 核心数 | 0.8–1.5 × 核心数 | > 1.5 × 核心数 |
| 内存使用率 | < 80% | 80–95% | > 95% |
| 磁盘空间使用率 | < 80% | 80–95% | > 95% |
| 服务运行状态 | 失败的服务数量 | 1–3 个失败的服务 | > 3 个失败的服务 |
| “僵尸进程”（非正常运行的进程） | 0 个 | 1 个及以上 | 无 |

### 第三步：生成报告

```
## 🏥 System Health Report
**Host:** <hostname> | **OS:** <os> | **Uptime:** <uptime>
**Generated:** <timestamp>

### Overall: 🟢 Healthy / 🟡 Degraded / 🔴 Critical

| Area | Status | Details |
|------|--------|---------|
| CPU | 🟢 | Load 0.5 / 4 cores |
| Memory | 🟡 | 82% (13.1/16 GB) |
| Disk | 🟢 | / at 45% |
| Services | 🟢 | 0 failed |

### ⚠️ Recommendations
1. [High] Consider freeing memory — 82% used
2. [Low] 2 zombie processes detected (PPIDs: 1234, 5678)

### 📊 Top Consumers
- **Memory**: java (2.1 GB), chrome (1.5 GB)
- **CPU**: ffmpeg (45%), node (12%)
```

### 第四步：保存报告（可选）

如需要，可将报告保存到 `~/system-health-reports/YYYY-MM-DD_HH-MM.md` 文件中。

## 特殊情况处理

- **容器/虚拟机环境**：部分系统指标可能无法完整获取。此时 `/proc/cpuinfo` 可能会显示宿主机的 CPU 数量。
- **非 systemd 系统**：跳过基于 `systemctl` 的服务检查，改用 `service --status-all` 命令。
- **macOS**：请使用 `vm_stat`、`sysctl`、`diskutil` 替代 Linux 命令。
- **系统安装简化的情况**：如果缺少 `ss` 命令，可使用 `netstat -tlnp` 代替。

## 安全注意事项

- 所有命令均为只读操作，不会对系统进行任何修改。
- 登录记录（`last`、`who`）可能包含用户名，请在分享报告前确认目标受众。
- 报告中不要包含进程的完整参数（这些参数可能包含敏感信息）。