---
name: auto-updater-gateway
description: 使用 Gateway Cron 计划任务来安排并执行 Clawdbot 及已安装技能的每日/每周安全更新。在设置“于 04:00 运行更新”任务时，请使用此方法，包括轮换更新报告、运行 `clawdhub update --all` 命令，以及（可选地）应用 Clawdbot 更新、重启系统并执行故障排查（doctor）操作。
metadata: {"version":"1.0.1","clawdbot":{"emoji":"🔄","category":"automation","os":["windows","darwin","linux"],"requires":{"anyBins":["clawdbot","clawdhub"]}}}
---

# 自动更新器（网关）

使用 **Clawdbot Cron**（网关调度器）创建一个可靠的每日自动更新机制。

这可以被视为一项“技能”，因为它包含可重复的工作流程以及正确的配置设置（而不是一个插件）。

## 快速设置检查清单

1) 确保已登录 ClawHub CLI（以进行技能更新）：

```bash
/home/xabo/.nvm/versions/node/v22.22.0/bin/clawdhub login --workdir /home/xabo/clawd --dir skills
/home/xabo/.nvm/versions/node/v22.22.0/bin/clawdhub whoami --workdir /home/xabo/clawd --dir skills
```

2) 确定以下内容：
- 更新的触发时间（使用 cron 任务和时区）
- 更新任务是仅报告更新结果，还是同时执行更新和重启操作

## 推荐的 cron 任务设置（独立运行，输出结果）

使用 **独立运行的** cron 任务，以避免干扰主会话流程。

示例 CLI 命令（欧洲/斯德哥尔摩时间 04:00）：

```bash
/home/xabo/.nvm/versions/node/v22.22.0/bin/clawdbot cron add \
  --name "Daily auto-update (Clawdbot + skills)" \
  --cron "0 4 * * *" \
  --tz "Europe/Stockholm" \
  --session isolated \
  --wake now \
  --deliver \
  --channel telegram \
  --to "2095290688" \
  --message "Run daily auto-update: update skills via clawdhub update --all; if Clawdbot has an update available, apply it and restart; then run clawdbot doctor --non-interactive; report what changed."
```

## 任务的具体执行步骤（工作流程）

在 cron 任务执行期间：

1) 获取更新前的系统状态：
- `clawdbot --version`
- `clawdhub list`（列出所有技能及其版本）

2) 更新技能：
- `clawdhub update --all`

3) （可选）更新 Clawdbot 本身：
- 仅当所有者明确要求时才执行此操作。
- 更新完成后，运行 `clawdbot doctor --non-interactive`。
- 如有必要，重启网关服务。

4) 发送简要的更新总结：
- 更新前后的 Clawdbot 版本信息
- 已更新的技能列表（旧版本 → 新版本）
- 发生的任何错误信息

## 注意事项 / 需要注意的问题

- **时区设置**：在网关任务对象中，时区字段为 `schedule.tz`（遵循 IANA 时区标准，例如 `Europe/Stockholm`）。
- **结果发送方式**：建议使用明确的 `channel` 和 `to` 参数，以确保任务结果能够准确送达指定接收者。
- **Clawdbot 的自我更新**：可能会对系统造成干扰（例如需要重启）。请选择在系统空闲时段执行更新。

## 故障排除

- 如果 `clawdhub update` 命令提示“未登录”，请重新执行 `clawdhub login`。
- 如果任务未能成功执行，请确认网关服务是否处于开启状态，并检查 cron 任务是否已启用。
- 即使没有更新发生，也请发送“无变化”的报告。