---
name: bmkg-monitor
description: 使用印度尼西亚气象、气候和地球物理局（BMKG）的官方数据来监测地震情况。当用户查询最新的地震信息、有震感的地震记录，或关于印度尼西亚特定地震事件的相关资料时，可参考此功能。
---

# BMKG 监控器

使用印度尼西亚气象、气候与地球物理局（Badan Meteorologi, Klimatologi, dan Geofisika, BMKG）提供的实时数据，监控并分析该地区的地震活动。

## 快速入门

运行监控脚本以获取最新数据：

```bash
# Get the latest significant earthquake (M5.0+)
python3 scripts/get_gempa.py latest

# Get list of earthquakes felt by people (including smaller ones)
python3 scripts/get_gempa.py felt

# Get recent history of M5.0+ earthquakes
python3 scripts/get_gempa.py recent

# Get detailed Moment Tensor and Phase history
python3 scripts/get_gempa.py detail <EVENT_ID>
```

## 工作流程

### 1. 检查近期地震活动
如果用户报告感觉到震动或询问“是否发生了地震？”，请首先运行 `get_gempa.py felt` 命令。该命令会列出那些人们实际能够感觉到的小型、浅层地震。

### 2. 深度分析
当发生重大地震时，请参考 [references/seismology.md](references/seismology.md) 来了解以下内容：
- 地震的震级（Magnitude）含义。
- 报告的震度等级（MMI 级别）。
- 根据地震深度和位置判断可能的影响范围。

### 3. 与新闻媒体协调
如果用户提供了“矩张量”（Moment Tensor）或“海滩球”（Beach Ball）图（通常来自 BMKG 的详细报告），请查阅 [references/seismology.md] 中的“矩张量”部分，以确定地震的类型（走滑型、正断层型或逆断层型）。

## 参考资料
- [seismology.md](references/seismology.md) - 地震震级、MMI 级别以及地震断层类型的相关信息。