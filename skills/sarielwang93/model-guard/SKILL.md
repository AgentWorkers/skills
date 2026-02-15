# Model Guard

该工具会自动监控 Anti-Gravity 模型的配额使用情况，并将默认模型切换为剩余配额最高的模型。如果所有 Anti-Gravity 模型的配额都低于 20%，则会自动切换回原生的 `gemini-flash` 模型。

## 使用方法

- **手动触发**：执行 `model-guard` 命令。
- **自动触发**：支持通过 `cron` 任务或 `heartbeat` 机制进行自动执行。

## 配置方式

请编辑 `guard.js` 文件，以修改 `THRESHOLD`（默认值为 20%）或 `FALLBACK_MODEL` 的配置参数。