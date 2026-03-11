---
name: tesla-commander
version: 1.0.0
description: 通过Fleet API可以远程操控和监控特斯拉汽车。您可以查看车辆状态、调节车内温度/充电系统/车门锁具状态、追踪车辆位置，以及分析车辆的行驶历史记录。
---
# Tesla Commander

## 什么是 Tesla Commander？

这是一个专为特斯拉车主设计的命令行接口。您可以通过终端或自动化脚本查询车辆状态、控制车内气候和充电系统、锁定/解锁车门、追踪车辆位置以及查看行驶历史记录。

该工具基于 **Tesla Fleet API**（官方的 Owner API 后继者）开发。

## 开始使用前

### 认证

Tesla Fleet API 使用 OAuth 2.0 进行身份验证。您需要准备以下信息：
1. **客户端 ID 和密钥**——在 [developer.tesla.com](https://developer.tesla.com) 注册一个应用程序。
2. **访问令牌**——通过 OAuth 流程获取。
3. **车辆 ID**——您的车辆的 API 标识符。

```bash
export TESLA_ACCESS_TOKEN="eyJ..."
export TESLA_VIN="5YJ3E1EA1NF000000"       # Optional: defaults to first vehicle
export TESLA_CLIENT_ID="your-client-id"      # For token refresh
export TESLA_CLIENT_SECRET="your-secret"     # For token refresh
```

### 令牌管理

该脚本内置了令牌刷新功能：

```bash
# Initial OAuth flow (opens browser for authorization)
bash scripts/tesla-cmd.sh auth login

# Refresh an expired token
bash scripts/tesla-cmd.sh auth refresh

# Check token validity
bash scripts/tesla-cmd.sh auth check
```

---

## 命令分类

### 1. 车辆状态

获取车辆当前状态的详细信息。

```bash
# Full vehicle data dump
bash scripts/tesla-cmd.sh status

# Specific subsystems
bash scripts/tesla-cmd.sh status battery      # Battery level, range, charging state
bash scripts/tesla-cmd.sh status climate      # Interior/exterior temp, HVAC settings
bash scripts/tesla-cmd.sh status drive        # Speed, heading, GPS coordinates
bash scripts/tesla-cmd.sh status vehicle      # Doors, windows, trunk, frunk status

# Quick summary (one-line output for scripting)
bash scripts/tesla-cmd.sh summary
# Output: Model3 | 78% | 241mi | Parked | 72°F | Home | Locked
```

### 2. 位置与追踪

```bash
# Current location with address
bash scripts/tesla-cmd.sh location

# Open location in default map application
bash scripts/tesla-cmd.sh location --map

# Track location updates (poll every N seconds)
bash scripts/tesla-cmd.sh track 30

# Distance from a specific address
bash scripts/tesla-cmd.sh distance "123 Main St, City, State"
```

### 3. 气候控制

```bash
# Start/stop HVAC
bash scripts/tesla-cmd.sh climate on
bash scripts/tesla-cmd.sh climate off

# Set temperature (°F or °C)
bash scripts/tesla-cmd.sh climate temp 72        # Fahrenheit
bash scripts/tesla-cmd.sh climate temp 22 --celsius

# Seat heaters (0=off, 1=low, 2=med, 3=high)
bash scripts/tesla-cmd.sh climate seat driver 2
bash scripts/tesla-cmd.sh climate seat passenger 1
bash scripts/tesla-cmd.sh climate seat rear-left 3

# Steering wheel heater
bash scripts/tesla-cmd.sh climate wheel on

# Defrost mode
bash scripts/tesla-cmd.sh climate defrost on

# Dog mode / Camp mode
bash scripts/tesla-cmd.sh climate dog on
bash scripts/tesla-cmd.sh climate camp on
```

### 4. 充电

```bash
# Charging status
bash scripts/tesla-cmd.sh charge status

# Start/stop charging
bash scripts/tesla-cmd.sh charge start
bash scripts/tesla-cmd.sh charge stop

# Set charge limit (percent)
bash scripts/tesla-cmd.sh charge limit 80

# Open/close charge port
bash scripts/tesla-cmd.sh charge port open
bash scripts/tesla-cmd.sh charge port close

# Scheduled charging
bash scripts/tesla-cmd.sh charge schedule 23:00   # Start at 11 PM
bash scripts/tesla-cmd.sh charge schedule off      # Disable schedule
```

### 5. 安全与访问权限

```bash
# Lock/unlock
bash scripts/tesla-cmd.sh lock
bash scripts/tesla-cmd.sh unlock

# Trunk / Frunk
bash scripts/tesla-cmd.sh trunk open
bash scripts/tesla-cmd.sh frunk open

# Flash lights / honk horn
bash scripts/tesla-cmd.sh flash
bash scripts/tesla-cmd.sh honk

# Sentry mode
bash scripts/tesla-cmd.sh sentry on
bash scripts/tesla-cmd.sh sentry off

# Valet mode
bash scripts/tesla-cmd.sh valet on 1234    # PIN required
bash scripts/tesla-cmd.sh valet off 1234

# Speed limit
bash scripts/tesla-cmd.sh speedlimit set 65 1234
bash scripts/tesla-cmd.sh speedlimit clear 1234
```

### 6. 行驶历史记录与分析

```bash
# Recent trips (last N days)
bash scripts/tesla-cmd.sh trips 7

# Trip summary with efficiency stats
bash scripts/tesla-cmd.sh trips summary --month

# Charging history
bash scripts/tesla-cmd.sh trips charges 30

# Export trip data as CSV
bash scripts/tesla-cmd.sh trips export trips_march.csv

# Efficiency report
bash scripts/tesla-cmd.sh efficiency
```

---

## 自动化示例

- **早晨预热功能（定时任务）：**
```bash
# At 7:30 AM on weekdays, warm up the car
30 7 * * 1-5 bash /path/to/tesla-cmd.sh climate on && bash /path/to/tesla-cmd.sh climate temp 72
```

- **电池电量低提醒：**
```bash
BATTERY=$(bash scripts/tesla-cmd.sh status battery --raw)
if [ "$BATTERY" -lt 20 ]; then
  echo "Tesla battery at ${BATTERY}%!" | mail -s "Low Battery" you@email.com
fi
```

- **地理围栏检测：**
```bash
bash scripts/tesla-cmd.sh location --raw | python3 -c "
import sys, json
data = json.load(sys.stdin)
lat, lon = data['latitude'], data['longitude']
# Check if within home radius
HOME_LAT, HOME_LON = 37.7749, -122.4194
dist = ((lat - HOME_LAT)**2 + (lon - HOME_LON)**2) ** 0.5
if dist > 0.01:
    print('Vehicle is away from home')
"
```

---

## 速率限制与注意事项

- Tesla Fleet API 有速率限制；该脚本会自动进行重试处理。
- 大多数命令需要车辆处于“唤醒”状态；脚本会自动触发车辆唤醒。
- 车辆唤醒可能需要 10-30 秒；使用 `--nowait` 参数可跳过等待过程。
- 频繁的请求会消耗 12V 电池电量；对于停放的车辆，建议将请求间隔设置为 5 分钟以上。

## 隐私与安全

- 访问令牌存储在 `~/.tesla-commander/` 目录中，权限设置为 600（仅允许相应用户访问）。
- 所有通信均使用 TLS 1.2 或更高版本的加密协议。
- 该脚本不会将您的令牌输出到标准输出（stdout）。
- 建议为共享脚本使用一个权限受限的特斯拉账户。