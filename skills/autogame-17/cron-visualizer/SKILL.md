---
name: cron-visualizer
description: 在24小时时间线上可视化系统的cron作业，以识别作业之间的重叠部分和潜在的瓶颈。
---
# Cron 视图器

该工具可可视化 24 小时内 Cron 任务的执行分布情况，帮助识别任务执行的拥堵点及重叠区域。

## 使用方法

```bash
# Run the visualizer (outputs ASCII chart to console)
node skills/cron-visualizer/index.js

# Output to a file
node skills/cron-visualizer/index.js > cron_schedule.txt
```