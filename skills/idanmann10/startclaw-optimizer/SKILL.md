# OpenClaw 优化器技能

## 概述

OpenClaw 优化器是一项全面的性能和成本优化工具，旨在提升 Clawdbot 子代理工作流程的效率。

## 核心组件

### 1. 任务路由器（Task Router）
- 根据任务复杂性智能选择模型
- 在 Haiku、Sonnet 和 Opus 模型之间自动进行任务路由
- 实现成本预测和优化

### 2. 调度器（Scheduler）
- 具有重试机制的稳健任务执行
- 可配置的预执行和后执行钩子
- 处理超时和指数级退避策略

### 3. 浏览器管理器（Browser Governor）
- 浏览器标签页序列化
- 并发标签页管理
- 防止进程失控的断路器机制

### 4. 上下文压缩（Context Compaction）
- 自动跟踪令牌（tokens）
- 在令牌数量达到 50,000 时进行摘要生成
- 保留关键上下文信息

### 5. 实时仪表盘（Real-time Dashboard）
- 监控每日预算
- 跟踪任务执行情况
- 可视化模型分布
- 显示断路器状态

## 预期节省成本

**优化前：** 每天 90 美元
**优化后：** 每天 3-5 美元
**节省比例：** 95%

## 安装

```bash
npm install @startclaw/openclaw-optimizer
```

## 使用方法

```javascript
const { TaskRouter, OptimizerScheduler, BrowserGovernor } = require('@startclaw/openclaw-optimizer');

const router = new TaskRouter();
const scheduler = new OptimizerScheduler();
const browserGovernor = new BrowserGovernor();

// Automatic model and cost optimization
const modelSelection = router.selectModel(taskDescription);
await scheduler.execute(task, modelSelection);
```

## 监控

```bash
# Real-time dashboard
python3 scripts/dashboard.py watch
```

## 许可证

StartClaw 内部使用许可证