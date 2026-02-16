---
name: skill-health-monitor
description: 监控已部署的技能（skills）的性能变化、错误情况以及任何意外的行为变化。部署后持续进行健康检查（health checks），并配备警报功能及趋势跟踪（trend tracking）。
user-invocable: true
metadata: {"openclaw": {"emoji": "📊", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---
# 技能健康监控器

在技能性能下降成为危机之前及时发现问题。该工具监控已部署技能的响应时间、错误率、输出结果的变化以及资源使用情况。

## 为何需要这个工具

技能在测试阶段运行正常，但在生产环境中却会逐渐出现性能问题：免费模型可能会改变其行为，API会增加延迟，内存泄漏也会逐渐累积。等到您发现问题的时候，您的代理可能已经使用有问题的技能运行了数小时。

## 命令

### 监控技能执行情况
```bash
python3 {baseDir}/scripts/health_monitor.py check --skill <name> --cmd "python3 path/to/script.py"
```

### 查看健康状况仪表盘
```bash
python3 {baseDir}/scripts/health_monitor.py dashboard
```

### 设置警报阈值
```bash
python3 {baseDir}/scripts/health_monitor.py threshold --skill <name> --max-latency 5000 --max-errors 3
```

### 导出健康报告
```bash
python3 {baseDir}/scripts/health_monitor.py report --json
```

### 查看技能的性能趋势
```bash
python3 {baseDir}/scripts/health_monitor.py trend --skill <name> --period 24h
```

## 监控的内容

- **延迟**：每次调用的执行时间，以及 p50/p95/p99 百分位数
- **错误率**：失败的调用次数及错误类型
- **输出结果的变化**：检测输出格式或内容是否发生意外变化
- **资源使用情况**：执行时的内存和 CPU 使用量
- **可用性**：在指定时间窗口（1小时、24小时、7天）内的运行状态

## 警报机制

- 当超过预设阈值时，会在控制台发出警报
- 支持通过 JSON Webhook 与外部系统集成
- 可为每个技能单独配置警报阈值

## 数据存储

健康数据以 JSON 格式存储在 `~/.openclaw/health/` 目录下，每个技能对应一个文件，并每天自动更新。