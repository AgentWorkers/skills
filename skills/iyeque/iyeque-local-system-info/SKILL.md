---
name: local-system-info
description: 使用 `psutil` 返回系统指标（CPU、RAM、磁盘、进程信息）。
metadata:
  {
    "openclaw":
      {
        "emoji": "🖥️",
        "requires": { "bins": ["python3"], "pip": ["psutil"] },
        "install":
          [
            {
              "id": "psutil",
              "kind": "pip",
              "package": "psutil",
              "label": "Install psutil",
            },
          ],
        "version": "1.1.0",
      },
  }
---
# 本地系统信息技能

监控本地系统资源，包括 CPU、内存、磁盘使用情况以及正在运行的进程。

## 工具 API

### system_info
检索系统指标。

- **参数：**
  - `action` (string, 必需): 可选值：`summary`, `cpu`, `memory`, `disk`, `processes`。
  - `limit` (integer, 可选): 要列出的进程数量（默认值：20）。仅与 `action=processes` 一起使用。

**使用方法：**

```bash
# Get full system summary
uv run --with psutil skills/local-system-info/sysinfo.py summary

# CPU metrics only
uv run --with psutil skills/local-system-info/sysinfo.py cpu

# Memory metrics only
uv run --with psutil skills/local-system-info/sysinfo.py memory

# Disk usage
uv run --with psutil skills/local-system-info/sysinfo.py disk

# List top processes by CPU usage
uv run --with psutil skills/local-system-info/sysinfo.py processes --limit 10
```

## 输出格式

### summary
```json
{
  "cpu": {
    "cpu_percent": 15.2,
    "cpu_count": 8,
    "load_avg": [0.5, 0.3, 0.2]
  },
  "memory": {
    "total": 17179869184,
    "available": 8589934592,
    "percent": 50.0,
    "swap_percent": 5.2
  },
  "disk": {
    "total": 500000000000,
    "used": 250000000000,
    "free": 250000000000,
    "percent": 50.0
  }
}
```

### processes
```json
[
  {
    "pid": 1234,
    "name": "python3",
    "username": "user",
    "cpu_percent": 5.2,
    "memory_percent": 2.1
  },
  ...
]
```

## 指标说明

- **cpu_percent:** 当前 CPU 使用率（0-100%）
- **cpu_count:** 逻辑 CPU 核心数量
- **load_avg:** 系统负载平均值（1分钟、5分钟、15分钟），按 CPU 核心数量进行归一化
- **memory.total/available:** RAM 总容量（以字节为单位）
- **memory.percent:** RAM 使用百分比
- **disk_percent:** 根文件系统的使用百分比
- **processes:** 按 CPU 使用率排序的前 N 个进程

## 所需依赖

- **psutil:** 一个跨平台的系统监控库
- **Python 3.6+:** 用于支持 f-string 和类型注解

## 平台支持

支持 Linux、macOS、Windows 和 WSL。部分指标可能因平台而异：
- **load_avg:** 在 Windows 上不可用
- 进程信息的详细程度可能因操作系统而异