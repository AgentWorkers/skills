---
name: feishu-evolver-wrapper
description: Feishu集成包装器，用于能力进化器（capability-evolver）。它负责管理进化循环的生命周期（启动/停止/检查），发送详细的Feishu卡片报告，并提供仪表板可视化功能。在配合Feishu报告系统运行能力进化器或管理进化守护进程（evolution daemon）时，请使用该工具。
---
# Feishu Evolver Wrapper

这是一个轻量级的 `capability-evolver` 技能封装工具。它会注入 Feishu 报告环境变量（`EVOLVE_REPORT TOOL`），以在 Master 环境中实现丰富的卡片报表功能。

## 使用方法

```bash
# Run the evolution loop
node skills/feishu-evolver-wrapper/index.js

# Generate Evolution Dashboard (Markdown)
node skills/feishu-evolver-wrapper/visualize_dashboard.js

# Lifecycle Management (Start/Stop/Status/Ensure)
node skills/feishu-evolver-wrapper/lifecycle.js status
```

## 架构

- **进化循环（Evolution Loop）**：使用 Feishu 报告功能来执行 GEP（基因工程平台）的进化周期。
- **仪表板（Dashboard）**：从 `assets/gep/events.jsonl` 文件中可视化各项指标和历史数据。
- **导出历史记录（Export History）**：将原始历史数据导出到 Feishu Docs 平台。
- **监控机制（Watchdog）**：通过 OpenClaw 的 Cron 作业 `evolver_watchdog_robust` 进行管理（该作业每 10 分钟执行一次 `lifecycle.js` 脚本）。
  - 该机制替代了传统的、容易出问题的系统 Cron 作业逻辑。
  - 确保在系统崩溃或挂起时，进化循环能够自动重启。