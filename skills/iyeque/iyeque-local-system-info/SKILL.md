---
name: local-system-info
description: 使用 `psutil` 返回系统指标（CPU、RAM、磁盘和进程信息）。
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
      },
  }
---
# 本地系统信息技能

监控本地系统资源，包括 CPU、内存、磁盘使用情况以及正在运行的进程。

## 工具 API

### system_info
用于检索系统指标。

- **参数：**
  - `action` (字符串，必填)：`summary`、`cpu`、`memory`、`disk`、`processes` 中的一个。
  - `limit` (整数，可选)：要列出的进程数量（默认值：20）。仅在与 `action=processes` 一起使用时生效。

**使用方法：**

```bash
uv run --with psutil skills/local-system-info/sysinfo.py summary
uv run --with psutil skills/local-system-info/sysinfo.py processes --limit 10
```