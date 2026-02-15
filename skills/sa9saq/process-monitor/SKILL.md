---
description: 监控系统进程，识别占用CPU/内存最多的进程，并在资源使用达到阈值时发出警报。
---

# 进程监控器

监控系统进程及资源使用情况，并提供基于阈值的警报。

## 必备条件

- 标准的 Unix 工具：`ps`、`top`、`free`、`uptime`（已在 Linux 上预装）
- 不需要 API 密钥

## 使用说明

1. **资源概览** — 运行相关命令并格式化输出结果：
   ```bash
   uptime                          # Load average
   free -h                         # Memory/swap usage
   nproc                           # CPU count
   df -h / /home 2>/dev/null       # Key disk partitions
   ```

2. **热门进程** — 按 CPU 或内存使用量排序：
   ```bash
   ps aux --sort=-%mem | head -15  # Top memory consumers
   ps aux --sort=-%cpu | head -15  # Top CPU consumers
   ```

3. **搜索进程** — 按名称或 PID 查找进程：
   ```bash
   ps aux | grep -i "[n]ode"      # By name (brackets avoid matching grep itself)
   ps -p 1234 -o pid,user,%cpu,%mem,cmd  # By PID
   ```

4. **阈值警报** — 标记超出限制的进程：
   - 单个进程的 CPU 使用率超过 80% → ⚠️ 警告
   - 单个进程的内存使用量超过 50% → ⚠️ 警告
   - 系统内存使用量超过 90% → 🔴 危急
   - 平均负载超过 CPU 数量的两倍 → 🔴 危急

5. **输出格式**：
   ```
   ## 📊 Process Report — <hostname> (<timestamp>)

   | Metric        | Value          | Status |
   |---------------|----------------|--------|
   | Load Average  | 1.2 / 0.8 / 0.5 | 🟢   |
   | Memory        | 12.3/16.0 GB (77%) | 🟢 |
   | Swap          | 0.0/4.0 GB    | 🟢     |

   ### Top 5 by Memory
   | PID   | User  | %MEM | %CPU | Command        |
   |-------|-------|------|------|----------------|
   | 1234  | root  | 12.3 | 2.1  | /usr/bin/java  |
   ```

## 特殊情况处理

- **僵尸进程**：使用 `ps aux | awk '$8 ~ /Z/'` 命令检查僵尸进程的数量及其父进程的 PID。
- **无法使用 `top`**：可以改用 `/proc/loadavg` 和 `/proc/meminfo`。
- **Docker/容器环境**：`ps` 命令可能显示宿主机的进程。此时需使用 `--pid=host` 选项来指定容器内的进程。

## 安全性注意事项

- 仅执行只读操作；未经用户明确许可，严禁终止任何进程。
- 对输出中的进程名称进行清洗处理（这些名称可能包含敏感路径或参数）。