# 每日构建 🌙

这是一个自动化技能，会在你睡觉时执行维护任务，并在早晨为你提供简要报告。

灵感来源于 [The Nightly Build](https://www.moltbook.com/post/562faad7-f9cc-49a3-8520-2bdf362606bb)。

## 命令

- `nightly report` — 显示上一次的每日构建报告。
- `nightly run` — 触发手动运行（用于测试）。
- `nightly config` — 配置任务（更新技能、检查磁盘等）。

## 任务

- 📦 **技能审计**：对已安装的技能运行 `npm audit`。
- 🔄 **自动更新**：从 git 仓库拉取最新更改。
- 🧹 **清理**：删除临时文件和旧日志。
- 📊 **健康检查**：验证磁盘空间和系统负载。
- 📝 **简要报告**：将所有结果汇总成晨间报告。

## 设置

将以下内容添加到你的 cron 表达式中（例如，通过 `openclaw cron add`）：
```json
{
  "schedule": { "kind": "cron", "expr": "0 3 * * *", "tz": "Asia/Shanghai" },
  "payload": { "kind": "agentTurn", "message": "Run nightly build tasks and generate report." }
}
```