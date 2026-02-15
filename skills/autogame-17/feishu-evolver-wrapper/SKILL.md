# Feishu Evolver Wrapper

这是一个轻量级的 `capability-evolver` 技能封装工具。它将 Feishu 报告环境变量（`EVOLVE_REPORT_TOOL`）注入到系统中，从而在 Master 环境中实现丰富的卡片式报告功能。

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

- **进化循环（Evolution Loop）**：使用 Feishu 报告功能来执行 GEP（Genetic Programming）的进化过程。
- **仪表板（Dashboard）**：从 `assets/gep/events.jsonl` 文件中可视化各项指标和历史数据。
- **导出历史记录（Export History）**：将原始的历史数据导出到 Feishu Docs 平台。
- **监控机制（Watchdog）**：通过 OpenClaw 的 Cron 作业 `evolver_watchdog_robust` 进行管理（该作业每 10 分钟运行一次 `lifecycle.js` 脚本）。
  - 该机制替代了传统的、容易出错的系统 Cron 作业逻辑。
  - 确保在系统崩溃或挂起时能够自动重启进化循环。