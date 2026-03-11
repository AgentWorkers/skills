---
name: system-load-monitor
description: 系统负载监控与任务控制技能：该技能能够实时监控CPU和内存的使用情况，当负载超过预设阈值时，会自动暂停相关任务的执行；待负载恢复正常后，再恢复任务的运行。适用于配置较低的服务器，有效防止系统因负载过高而出现宕机现象。
---
# 系统负载监控器

## 核心功能
监控服务器的CPU和内存负载，自动控制系统任务的执行，防止因负载过重导致服务器停机。

## 适用场景
在以下情况下使用该功能：
- 服务器配置较低（例如：2核2GB），容易发生停机；
- 需要执行资源密集型任务；
- 之前的停机是由于负载过重引起的；
- 需要智能地控制任务执行的节奏；
- 需要实时监控服务器状态。

## 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `cpu_threshold` | 90 | CPU负载阈值（百分比） |
| `memory_threshold` | 90 | 内存使用阈值（百分比） |
| `check_interval` | 30 | 检查间隔（秒） |
| `cool_down` | 60 | 负载过重后的冷却时间（秒） |

## 使用方法

### 1. 检查当前系统状态

```bash
# Quick check
python3 ~/.openclaw/workspace/skills/system-load-monitor/scripts/check_load.py

# View detailed JSON output
python3 ~/.openclaw/workspace/skills/system-load-monitor/scripts/check_load.py --json

# Custom thresholds
python3 ~/.openclaw/workspace/skills/system-load-monitor/scripts/check_load.py --cpu-threshold 80 --memory-threshold 85
```

### 2. 任务执行前的负载检查
在执行任何资源消耗较大的任务之前，请先进行负载检查：

1. **运行负载检查**
   ```bash
   python3 ~/.openclaw/workspace/skills/system-load-monitor/scripts/check_load.py --json
   ```

2. **解析返回结果**
   - `status`: “ok” / “warning” / “critical”
   - `recommendation`: “CONTINUE” / “PAUSE”
   - `cpu.load_percent`: CPU负载百分比
   - `memory.used_percent`: 内存使用百分比

3. **根据状态做出决策**
   - **ok**: 继续执行任务
   - **warning**: 小心执行任务，并考虑分批处理
   - **critical**: 暂停任务，待冷却后再重试

### 3. 长期运行任务的监控循环
对于长期运行的任务，使用以下监控机制：

```python
import subprocess
import time
import json

def check_load():
    result = subprocess.run(
        ['python3', '~/.openclaw/workspace/skills/system-load-monitor/scripts/check_load.py', '--json'],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def run_with_load_monitor(task_func, cpu_threshold=90, memory_threshold=90):
    """Continuously monitor load while executing tasks"""
    while True:
        status = check_load()
        
        if status['status'] == 'critical':
            print(f"⚠️ Excessive load, pausing task...")
            print(f"CPU: {status['cpu']['load_percent']}%, Memory: {status['memory']['used_percent']}%")
            time.sleep(60)  # Wait for 60 seconds
            continue
        
        # Load is normal, execute the task
        task_func()
        break
```

## 状态码说明

| 退出码 | 状态 | 含义 |
|--------|------|------|
| 0 | ok | 负载正常，可以继续 |
| 1 | warning | 负载较高，建议谨慎操作 |
| 2 | critical | 负载过高，必须暂停 |

## 对于配置较低的服务器（2核2GB）的建议
对于您的2核2GB服务器：
1. **降低阈值**：建议将警告阈值设置为70-80%
   ```bash
   python3 ~/.openclaw/workspace/skills/system-load-monitor/scripts/check_load.py --cpu-threshold 75 --memory-threshold 80
   ```

2. **分批执行任务**：将大型任务拆分为多个小任务
3. **避免并发执行**：每次只执行一个任务
4. **定期检查**：对于长期运行的任务，每30秒检查一次负载情况

## 警报通知
当检测到严重负载（critical状态）时，应：
1. 立即暂停当前任务
2. 通过Feishu消息通知用户
3. 在冷却时间过后重试任务

## 脚本输出示例

```json
{
  "status": "critical",
  "cpu": {
    "load_avg_1m": 3.8,
    "cpu_count": 2,
    "load_percent": 190.0
  },
  "memory": {
    "total_mb": 2048,
    "used_mb": 1843,
    "available_mb": 205,
    "used_percent": 90.0
  },
  "top_processes": [
    {"user": "node", "cpu_percent": 45.2, "mem_percent": 32.1, "command": "node /usr/bin/openclaw"}
  ],
  "thresholds": {"cpu": 90, "memory": 90},
  "recommendation": "PAUSE"
}
```

## 注意事项
1. 该功能是一个独立的监控工具，不依赖于Fairy的内置判断机制；
2. 在执行任何重要任务之前，必须先进行负载检查；
3. 对于长期运行的任务，应建立循环监控机制；
4. 可根据实际情况调整阈值参数。