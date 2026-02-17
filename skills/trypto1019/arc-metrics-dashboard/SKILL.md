---
name: metrics-dashboard
description: 跟踪并可视化您的代理（agent）的运行指标。记录 API 调用、任务完成情况、运行时间、错误信息以及自定义计数器的数据。生成基于文本的仪表板，并导出数据以供分析。
user-invocable: true
metadata: {"openclaw": {"emoji": "📊", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---
# 指标仪表盘

跟踪您的代理的运行状态，记录事件、统计数据、测量耗时并生成报告。

## 为何需要这个功能

代理全天候运行，但用户无法回答一些基本问题：我完成了多少任务？我的错误率是多少？API调用需要多长时间？我最常使用哪些技能？如果没有指标数据，您将无法了解代理的运行情况。

## 命令

### 记录指标数据
```bash
python3 {baseDir}/scripts/metrics.py record --name api_calls --value 1 --tags '{"provider": "openrouter", "model": "gpt-4"}'
```

### 记录耗时
```bash
python3 {baseDir}/scripts/metrics.py timer --name task_duration --seconds 12.5 --tags '{"task": "scan_skill"}'
```

### 增加计数器的值
```bash
python3 {baseDir}/scripts/metrics.py counter --name posts_published --increment 1
```

### 记录错误
```bash
python3 {baseDir}/scripts/metrics.py error --name moltbook_verify_fail --message "Challenge solver returned wrong answer"
```

### 查看仪表盘
```bash
python3 {baseDir}/scripts/metrics.py dashboard
```

### 查看今天的指标数据
```bash
python3 {baseDir}/scripts/metrics.py view --period day
```

### 查看特定指标的历史记录
```bash
python3 {baseDir}/scripts/metrics.py view --name api_calls --period week
```

### 导出指标数据
```bash
python3 {baseDir}/scripts/metrics.py export --format json > metrics.json
python3 {baseDir}/scripts/metrics.py export --format csv > metrics.csv
```

## 仪表盘显示内容

基于文本的仪表盘会显示以下信息：
- 自首次记录指标数据以来的运行时间
- 今天的总事件数量
- 按数量排序的顶级指标
- 错误率
- 定时操作的平均耗时
- 自定义计数器的值

## 指标类型

- **counter** — 需要统计的数量（发布的帖子、扫描的技能、生成的评论等）
- **timer** — 以秒为单位测量的时间（API响应时间、任务耗时等）
- **event** — 发生的事件（错误、部署、重启等）
- **gauge** — 当前值（声望值、剩余预算、队列深度等）

## 数据存储

指标数据以每日JSON文件的形式存储在`~/.openclaw/metrics/`目录中。该方式轻量级，无需使用数据库。

## 集成

该功能可与合规性审计跟踪系统集成，将指标事件与审计记录一起保存，以实现全面的运营监控。