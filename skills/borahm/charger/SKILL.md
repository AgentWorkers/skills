---
name: charger
description: 通过 Google Places 检查电动汽车充电器的可用性（包括常用充电器和附近的充电器）。
metadata:
  clawdbot:
    config:
      requiredEnv:
        - GOOGLE_PLACES_API_KEY
      stateDirs:
        - config
        - .cache
---

# 充电器

这是一个基于 Google Places（新功能）提供的电动汽车充电器信息查询工具。该工具包含一个名为 `bin/charger` 的命令行工具（使用 Node.js 开发），用于查询充电器的可用性。

## 设置要求

- 确保已安装 Node.js 18 及更高版本（Clawdbot 已经内置了 Node.js）。
- 需要 `GOOGLE_PLACES_API_KEY`（建议将其配置在 `~/.clawdbot/.env` 文件中）。

- 将 `bin/charger` 命令行工具添加到系统的 `PATH` 环境变量中（示例命令：`ln -sf "$(pwd)"/bin/charger /home/claw/clawd/bin/charger`）。

- 可以将某个充电器添加为常用充电站：
  - `charger favorites add home --place-id <placeId>`

## 命令

- 查询常用充电站或特定充电站的可用性：
  - `charger check home`
  - `charger check "Wien Energie Charging Station Liniengasse 2 1060 Wien"`

- 查找附近的充电器：
  - `charger nearby --lat 48.188472 --lng 16.348854 --radius 2000 --max 10`

## 通知机制

推荐的通知方式如下：
1. `charger` 工具会直接返回一个明确的提示信息（例如：“Any free: YES|NO”），表示充电器的可用性。
2. 通过定时任务（如 Gateway 的 cron 作业）运行一个辅助脚本，仅在确实需要通知时才输出相关信息。

### 辅助脚本（负责发送通知）

该工具包中包含 `scripts/charger-notify.sh` 脚本，其功能如下：
- 执行 `charger check <target>` 命令来查询充电器状态。
- 如果查询结果显示“Any free: YES”，且上一次查询结果为“NO”，则发送通知。
- 否则，不发送任何通知。

**注意**：如果没有输出，即表示当前充电器处于可用状态，因此不会触发通知。

**状态记录**：
- 脚本会将充电器的可用状态保存在 `~/.cache/charger-notify/<target>.state` 文件中，因此只有在状态从“NO”变为“YES”时才会发送通知。

**使用方法**：
- 运行 `bash scripts/charger-notify.sh home` 来查询并接收通知。

**示例通知内容**：
- “EV 充电器可用：Wien Energie 充电站（地址：Amtshausgasse 9, 1050 Wien, Austria）——目前有 1 个车位可用（0 个车位正在使用中），更新时间：2026-01-21T21:05:00Z”

### 定时任务设置（如何接收 Telegram 通知）

使用 cron 作业来定时执行 `charger-notify.sh` 脚本，并将脚本的输出内容发送到您的 Telegram 账户。典型设置如下：
- 每 10 分钟执行一次查询：`*/10 * * * *`

如果您希望将此功能集成到 Clawdbot 的 cron 任务中以接收 Telegram 通知，请提供以下信息：
- 需要查询的充电站名称（例如：`home`）
- 定时间隔（例如：每 5 分钟、10 分钟或 20 分钟）
- 通知的禁用时间（可选）