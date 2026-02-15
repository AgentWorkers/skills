---
name: openclaw-auto-updater
description: 使用可靠的 cron 模板来安排 OpenClaw 和技能的自动更新，确保调度时间符合时区要求，并生成清晰的更新总结报告。这些工具适用于无人值守的维护工作、定期升级以及简洁的更新通知。
---

# OpenClaw 自动更新器

使用 cron 任务来运行 OpenClaw 及已安装技能的更新（无需编写脚本）。重点在于：安全的调度方式、可预测的更新结果以及最小化人工干预。

## 功能介绍

- 按固定时间表运行 OpenClaw 的更新
- 通过 ClawHub 更新所有已安装的技能
- 提供简洁明了的更新状态报告（更新成功、未变化或更新失败）

## 设置（每日更新）

**欧洲/柏林时间，每天 03:30**：
```bash
openclaw cron add \
  --name "OpenClaw Auto-Update" \
  --cron "30 3 * * *" \
  --tz "Europe/Berlin" \
  --session isolated \
  --wake now \
  --deliver \
  --message "Run daily auto-updates: 1) openclaw update --yes --json 2) clawdhub update --all 3) report versions updated + errors."
```

### 每周更新（周日 04:00）  
```bash
openclaw cron add \
  --name "OpenClaw Auto-Update (Weekly)" \
  --cron "0 4 * * 0" \
  --tz "Europe/Berlin" \
  --session isolated \
  --wake now \
  --deliver \
  --message "Run weekly auto-updates: openclaw update --yes --json; clawdhub update --all; summarize changes."
```

## 更安全的更新模式

- **模拟运行（不进行任何更改）：**  
```bash
openclaw cron add \
  --name "OpenClaw Auto-Update (Dry)" \
  --cron "30 3 * * *" \
  --tz "Europe/Berlin" \
  --session isolated \
  --wake now \
  --deliver \
  --message "Check updates only: openclaw update status; clawdhub update --all --dry-run; summarize what would change."
```

- **仅更新核心组件（跳过其他技能）：**  
```bash
openclaw cron add \
  --name "OpenClaw Auto-Update (Core Only)" \
  --cron "30 3 * * *" \
  --tz "Europe/Berlin" \
  --session isolated \
  --wake now \
  --deliver \
  --message "Update OpenClaw only: openclaw update --yes --json; summarize version change."
```

## 推荐的更新状态报告格式  
```
🔄 OpenClaw Auto-Update

OpenClaw: 2026.2.1 → 2026.2.2 (OK)
Skills updated: 3
Skills unchanged: 12
Errors: none
```

## 故障排除

- 如果更新失败，请在报告中记录错误信息。
- 将更新任务安排在非工作时间执行，以避免影响系统运行。
- 使用明确的时间区设置，以防出现意外。

## 参考资料
- `references/agent-guide.md` → 更详细的实现说明  
- `references/summary-examples.md` → 更新状态报告的格式示例