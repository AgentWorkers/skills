---
name: my-tesla
description: 您可以通过 `teslapy` 工具，利用 Tesla Owner API 从 macOS 系统远程控制特斯拉汽车。该工具支持执行以下操作：身份验证、查询车辆信息、查看车辆状态、锁定/解锁车辆、调节车内温度、控制充电功能、获取车辆位置以及执行其他附加功能。当您需要查看车辆状态或执行安全的远程操作时，这个工具非常实用。该工具由 Parth Maniar (@officialpm) 开发，具有仅限本地使用的身份验证机制、对可能造成干扰的操作的确认机制，以及便于阅读的车辆状态输出界面。
---

# 我的特斯拉

**作者：** Parth Maniar — [@officialpm](https://github.com/officialpm)

这是一个基于 `teslapy` 开发的、用于 Clawdbot 的实用特斯拉控制脚本。

## 设置

### 所需条件

- 确保环境变量 `TESLA_EMAIL` 已设置（你的特斯拉账户邮箱）
- Python 3.10 或更高版本

### 首次认证

```bash
TESLA_EMAIL="you@email.com" python3 {baseDir}/scripts/tesla.py auth
```

此命令会打开特斯拉的登录页面。登录后，请将返回的回调 URL 复制并粘贴到命令行工具（CLI）中。

- 令牌缓存：`~/.tesla_cache.json`（仅限本地使用；建议设置权限为 `0600`）
- 可选：通过环境变量 `MY_TESLA_DEFAULT_CAR` 设置默认车辆名称
- 或者使用以下命令设置本地默认车辆：`python3 {baseDir}/scripts/tesla.py default-car "Name"`（将信息写入 `~/.my_tesla.json`；建议设置权限为 `0600`）

## 命令

```bash
# List vehicles
python3 {baseDir}/scripts/tesla.py list
python3 {baseDir}/scripts/tesla.py list --json   # machine-readable, privacy-safe

# Version
python3 {baseDir}/scripts/tesla.py version
python3 {baseDir}/scripts/tesla.py --version

# Pick a car (optional)
# --car accepts: exact name, partial name (substring match), or a 1-based index from `list`
python3 {baseDir}/scripts/tesla.py --car "Model" status
python3 {baseDir}/scripts/tesla.py --car 1 report

# Set a default car (used when --car is not passed)
python3 {baseDir}/scripts/tesla.py default-car "My Model 3"

# One-line summary (best for chat)
python3 {baseDir}/scripts/tesla.py summary
python3 {baseDir}/scripts/tesla.py summary --no-wake   # don't wake a sleeping car

# One-screen report (chat friendly, more detail)
# Includes battery/charging/climate + (when available) TPMS tire pressures.
python3 {baseDir}/scripts/tesla.py report
python3 {baseDir}/scripts/tesla.py report --no-wake

# Detailed status
python3 {baseDir}/scripts/tesla.py status
python3 {baseDir}/scripts/tesla.py status --no-wake
python3 {baseDir}/scripts/tesla.py status --summary   # include one-line summary + detailed output
python3 {baseDir}/scripts/tesla.py --car "My Model 3" status

# JSON output (prints ONLY JSON; good for piping/parsing)
# NOTE: `status --json` outputs *raw* `vehicle_data`, which may include location/drive_state.
# Prefer `report --json` (sanitized) unless you explicitly need the raw payload.
python3 {baseDir}/scripts/tesla.py status --json             # raw vehicle_data (may include location)
python3 {baseDir}/scripts/tesla.py report --json             # sanitized report object (no location; includes scheduled charging + charge port state)
python3 {baseDir}/scripts/tesla.py report --json --raw-json  # raw vehicle_data (may include location)
python3 {baseDir}/scripts/tesla.py charge status --json

# Lock / unlock
python3 {baseDir}/scripts/tesla.py lock
python3 {baseDir}/scripts/tesla.py unlock

# Climate (status is read-only)
python3 {baseDir}/scripts/tesla.py climate status
python3 {baseDir}/scripts/tesla.py climate status --no-wake
python3 {baseDir}/scripts/tesla.py climate on
python3 {baseDir}/scripts/tesla.py climate off
python3 {baseDir}/scripts/tesla.py climate defrost on
python3 {baseDir}/scripts/tesla.py climate defrost off
python3 {baseDir}/scripts/tesla.py climate temp 72      # default: °F
python3 {baseDir}/scripts/tesla.py climate temp 22 --celsius

# Charging
python3 {baseDir}/scripts/tesla.py charge status
python3 {baseDir}/scripts/tesla.py charge status --no-wake
python3 {baseDir}/scripts/tesla.py charge start --yes
python3 {baseDir}/scripts/tesla.py charge stop  --yes
python3 {baseDir}/scripts/tesla.py charge limit 80 --yes   # 50–100
python3 {baseDir}/scripts/tesla.py charge amps 16 --yes    # 1–48 (conservative guardrail)

# Scheduled charging (set/off are safety gated)
python3 {baseDir}/scripts/tesla.py scheduled-charging status
python3 {baseDir}/scripts/tesla.py scheduled-charging status --no-wake
python3 {baseDir}/scripts/tesla.py scheduled-charging set 23:30 --yes
python3 {baseDir}/scripts/tesla.py scheduled-charging off --yes

# Location (approx by default; use --yes for precise coordinates)
python3 {baseDir}/scripts/tesla.py location
python3 {baseDir}/scripts/tesla.py location --no-wake
python3 {baseDir}/scripts/tesla.py location --yes

# Tire pressures (TPMS)
python3 {baseDir}/scripts/tesla.py tires
python3 {baseDir}/scripts/tesla.py tires --no-wake

# Openings (doors/trunks/windows)
python3 {baseDir}/scripts/tesla.py openings
python3 {baseDir}/scripts/tesla.py openings --no-wake
python3 {baseDir}/scripts/tesla.py openings --json

# Trunk / frunk (safety gated)
python3 {baseDir}/scripts/tesla.py trunk trunk --yes
python3 {baseDir}/scripts/tesla.py trunk frunk --yes

# Windows (safety gated)
python3 {baseDir}/scripts/tesla.py windows vent  --yes
python3 {baseDir}/scripts/tesla.py windows close --yes

# Sentry Mode (status is read-only; on/off safety gated)
python3 {baseDir}/scripts/tesla.py sentry status
python3 {baseDir}/scripts/tesla.py sentry status --no-wake
python3 {baseDir}/scripts/tesla.py sentry on  --yes
python3 {baseDir}/scripts/tesla.py sentry off --yes

# Charge port door
python3 {baseDir}/scripts/tesla.py charge-port status
python3 {baseDir}/scripts/tesla.py charge-port status --no-wake
python3 {baseDir}/scripts/tesla.py charge-port status --json

# Mileage tracking (odometer) — local SQLite
python3 {baseDir}/scripts/tesla.py mileage init
python3 {baseDir}/scripts/tesla.py mileage record --no-wake --auto-wake-after-hours 24
python3 {baseDir}/scripts/tesla.py mileage status
python3 {baseDir}/scripts/tesla.py mileage export --format csv
python3 {baseDir}/scripts/tesla.py mileage export --format json

# Charge port door open/close (safety gated)
python3 {baseDir}/scripts/tesla.py charge-port open  --yes
python3 {baseDir}/scripts/tesla.py charge-port close --yes

# Fun / attention-grabbing
python3 {baseDir}/scripts/tesla.py honk   --yes
python3 {baseDir}/scripts/tesla.py flash  --yes
```

## 安全设置

某些操作需要明确输入确认标志：
- `unlock`、`charge start|stop|limit|amps`、`trunk`、`windows`、`sentry on|off`、`honk`、`flash`、`charge-port open|close` 和 `scheduled-charging set|off` 需要输入 `--yes` 参数
- 默认情况下，`location` 命令返回的是近似位置信息；如需获取精确坐标，请添加 `--yes` 参数

## 隐私保护

- 你的特斯拉账户凭证仅会缓存在本地的 `~/.tesla_cache.json` 文件中。
- 请勿将令牌、日志、车辆识别码（VIN）或位置信息泄露。