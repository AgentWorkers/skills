---
name: my-tesla
description: 通过 `teslapy` 工具，可以使用特斯拉车主 API（Tesla Owner API）在 macOS 上控制特斯拉汽车，执行以下操作：身份验证、查看车辆列表、获取车辆状态、锁定/解锁车辆、调节车内温度、控制充电功能、获取车辆位置以及执行其他相关操作。该工具适用于需要查看车辆状态或远程执行安全指令的场景。由 Parth Maniar (@officialpm) 开发，具备仅限本地使用的身份验证缓存机制、对可能影响车辆功能的操作进行确认提示的功能，以及易于阅读的车辆状态输出界面。
---

# 我的特斯拉

**作者：** Parth Maniar — [@officialpm](https://github.com/officialpm)

这是一个基于 `teslapy` 开发的、用于 Clawdbot 的实用特斯拉控制工具。

## 设置

### 所需条件

- 确保环境变量 `TESLA_EMAIL` 已设置（您的特斯拉账户邮箱）
- Python 3.10 或更高版本

### 首次认证

```bash
TESLA_EMAIL="you@email.com" python3 {baseDir}/scripts/tesla.py auth
```

这将打开特斯拉的登录页面。登录后，将回调 URL 粘贴回命令行界面（CLI）中。

- 令牌缓存文件：`~/.tesla_cache.json`（仅限本地使用；建议设置权限为 `0600`）
- 可选：通过设置环境变量 `MY_TESLA_DEFAULT_CAR` 来指定默认车辆名称
- 或者使用以下命令设置本地默认车辆：`python3 {baseDir}/scripts/tesla.py default-car "Name"`（会将信息写入 `~/.my_tesla.json`；建议设置权限为 `0600`）

## 命令

```bash
# List vehicles
python3 {baseDir}/scripts/tesla.py list
python3 {baseDir}/scripts/tesla.py list --json   # machine-readable, privacy-safe

# Version
python3 {baseDir}/scripts/tesla.py version
python3 {baseDir}/scripts/tesla.py --version

# Debugging
# If something fails unexpectedly, add --debug for a full traceback
# (or set MY_TESLA_DEBUG=1)
python3 {baseDir}/scripts/tesla.py --debug status --no-wake

# Pick a car (optional)
# --car accepts: exact name, partial name (substring match), or a 1-based index from `list`
python3 {baseDir}/scripts/tesla.py --car "Model" status
python3 {baseDir}/scripts/tesla.py --car 1 report

# Set a default car (used when --car is not passed)
python3 {baseDir}/scripts/tesla.py default-car "My Model 3"

# One-line summary (best for chat)
python3 {baseDir}/scripts/tesla.py summary
python3 {baseDir}/scripts/tesla.py summary --no-wake   # don't wake a sleeping car

# Summary as JSON (privacy-safe)
# Unlike `status --json`, this emits a small sanitized object (no location).
# Includes `usable_level_percent` when the vehicle reports it.
python3 {baseDir}/scripts/tesla.py summary --json
python3 {baseDir}/scripts/tesla.py summary --json --raw-json   # raw vehicle_data (may include location)

# One-screen report (chat friendly, more detail)
# Includes battery/charging/climate + (when available) TPMS tire pressures.
# Includes "Usable battery" when the vehicle reports it (helpful for health/degradation).
# Also includes a quick openings summary (doors/trunk/frunk/windows) when available.
# When available, includes a compact seat heater summary line.
# When the vehicle reports it, includes scheduled departure / preconditioning / off-peak charging status.
python3 {baseDir}/scripts/tesla.py report
python3 {baseDir}/scripts/tesla.py report --no-wake

# Detailed status
python3 {baseDir}/scripts/tesla.py status
python3 {baseDir}/scripts/tesla.py status --no-wake
python3 {baseDir}/scripts/tesla.py status --summary   # include one-line summary + detailed output
python3 {baseDir}/scripts/tesla.py --car "My Model 3" status

# JSON output (prints ONLY JSON; good for piping/parsing)
# NOTE: `status --json` outputs *raw* `vehicle_data`, which may include location/drive_state.
# Prefer `summary --json` (sanitized) or `report --json` (sanitized) unless you explicitly need the raw payload.
python3 {baseDir}/scripts/tesla.py summary --json              # sanitized summary object (no location)
python3 {baseDir}/scripts/tesla.py report --json               # sanitized report object (no location; includes scheduled charging + charge port state)
python3 {baseDir}/scripts/tesla.py status --json               # raw vehicle_data (may include location)
python3 {baseDir}/scripts/tesla.py report --json --raw-json    # raw vehicle_data (may include location)
python3 {baseDir}/scripts/tesla.py summary --json --raw-json   # raw vehicle_data (may include location)
python3 {baseDir}/scripts/tesla.py charge status --json   # includes usable battery + (when charging) power details (kW/V/A)

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

# Scheduled departure (read-only)
# Shows scheduled departure, preconditioning, and off-peak charging flags (when the vehicle reports them).
python3 {baseDir}/scripts/tesla.py scheduled-departure status
python3 {baseDir}/scripts/tesla.py scheduled-departure status --no-wake
python3 {baseDir}/scripts/tesla.py --json scheduled-departure status

# Location (approx by default; use --yes for precise coordinates)
python3 {baseDir}/scripts/tesla.py location
python3 {baseDir}/scripts/tesla.py location --no-wake
python3 {baseDir}/scripts/tesla.py location --digits 1   # coarser rounding
python3 {baseDir}/scripts/tesla.py location --digits 3   # a bit more precise (still approximate)
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

# Windows
python3 {baseDir}/scripts/tesla.py windows status
python3 {baseDir}/scripts/tesla.py windows status --no-wake
python3 {baseDir}/scripts/tesla.py windows status --json

# Windows (safety gated)
python3 {baseDir}/scripts/tesla.py windows vent  --yes
python3 {baseDir}/scripts/tesla.py windows close --yes

# Seat heaters
python3 {baseDir}/scripts/tesla.py seats status
python3 {baseDir}/scripts/tesla.py seats status --no-wake
python3 {baseDir}/scripts/tesla.py seats status --json

# Seat heaters (safety gated)
# seat: driver|passenger|rear-left|rear-center|rear-right|3rd-left|3rd-right (or 0–6)
# level: 0–3 (0=off)
python3 {baseDir}/scripts/tesla.py seats set driver 3 --yes

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
python3 {baseDir}/scripts/tesla.py mileage export --format csv --since-days 7
python3 {baseDir}/scripts/tesla.py mileage export --format json
python3 {baseDir}/scripts/tesla.py mileage export --format json --since-ts 1738195200

# Charge port door open/close (safety gated)
python3 {baseDir}/scripts/tesla.py charge-port open  --yes
python3 {baseDir}/scripts/tesla.py charge-port close --yes

# Fun / attention-grabbing
python3 {baseDir}/scripts/tesla.py honk   --yes
python3 {baseDir}/scripts/tesla.py flash  --yes
```

## 安全设置

某些操作需要明确输入确认标志：
- `unlock`、`charge start|stop|limit|amps`、`trunk`、`windows`、`seats set`、`sentry on|off`、`honk`、`flash`、`charge-port open|close` 和 `scheduled-charging set|off` 需要输入 `--yes`
- `location` 命令返回的坐标为近似值；如需精确坐标，请添加 `--yes` 参数（或使用 `--digits N` 来控制小数位数）

## 隐私保护

- 认证信息仅缓存在本地（`~/.tesla_cache.json` 文件中）。
- 请勿将令牌、日志、车辆识别码（VIN）或位置信息泄露。