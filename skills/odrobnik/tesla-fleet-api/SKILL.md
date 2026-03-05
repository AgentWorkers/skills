---
name: tesla-fleet-api
description: >
  **使用说明：**  
  当与特斯拉官方的Fleet API集成时，本文档提供了如何读取车辆/能源设备数据或发送远程命令（如启动暖通空调系统、唤醒车辆、控制充电功能）的详细指导。内容包括开发者应用程序的注册流程、所需使用的区域/基础URL、OAuth令牌管理机制（包括第三方和合作伙伴的令牌）、令牌的更新策略，以及如何使用特斯拉官方的车辆命令接口（tesla-http-proxy）来发送经过签名的车辆控制指令。
version: 1.5.1
homepage: https://github.com/odrobnik/tesla-fleet-api-skill
metadata:
  openclaw:
    emoji: "🚗"
    requires:
      bins: ["python3", "openssl"]
      env: ["TESLA_CLIENT_ID", "TESLA_CLIENT_SECRET"]
      optionalEnv: ["TESLA_AUDIENCE", "TESLA_REDIRECT_URI", "TESLA_DOMAIN", "TESLA_BASE_URL", "TESLA_CA_CERT", "TESLA_ACCESS_TOKEN", "TESLA_REFRESH_TOKEN", "TESLA_SCOPE"]

---
# Tesla车队API

通过官方的车队API来控制特斯拉车辆。

## 脚本概述

| 脚本 | 功能 |
|--------|---------|
| `command.py` | 执行车辆命令（如调节气候、充电、锁车等） |
| `vehicle_data.py` | 读取车辆数据（如电池电量、气候状态、位置等） |
| `vehicles.py` | 列出车辆信息并刷新缓存 |
| `auth.py` | 管理认证和配置 |
| `tesla.oauth_local.py` | 带有本地回调服务器的OAuth辅助工具 |
| `start_proxy.sh` | 启动签名代理（用于执行车辆命令） |
| `stop_proxy.sh` | 停止签名代理 |

---

## 设置/配置

设置相关说明请参考 **`SETUP.md`**：

- [SETUP.md](SETUP.md)

项目目录结构：`{workspace}/tesla-fleet-api/`
- `config.json` （包含提供商凭证和非令牌配置信息）
- `auth.json` （包含OAuth令牌）
- `vehicles.json` （缓存的车辆列表）
- `places.json` （命名位置信息）
- `proxy/` （包含签名代理所需的TLS配置文件）

项目不使用`.env`文件来存储配置信息——所有配置都存储在`config.json`或环境变量中。

---

## `command.py` - 执行车辆命令

用于对特斯拉车辆发送命令。如果只有一辆车，系统会自动选择该车辆。

### 使用方法

```bash
command.py [VEHICLE] <command> [options]
```

- `VEHICLE`：车辆名称或VIN（如果只有一辆车，则可选）
- 可以不指定车辆名称直接执行命令：`command.py honk`  
- 或者指定车辆名称后执行命令：`command.py flash honk`（例如：`command.py flash` 或 `command.py honk`）

---

### 气候控制

#### 启动/停止空调
```bash
command.py climate start
command.py climate stop
command.py flash climate start          # specific vehicle
```

#### 设置温度
```bash
command.py climate temps <driver_temp> [passenger_temp]
command.py climate temps 21             # both seats 21°C
command.py climate temps 22 20          # driver 22°C, passenger 20°C
```

#### 气候保持模式
```bash
command.py climate keeper <mode>
```
模式选项：`off`（关闭）、`keep`（保持当前状态）、`dog`（自动调节）、`camp`（露营模式）

---

### 座椅加热器

```bash
command.py seat-heater --level <level> [--position <position>]
command.py seat-heater -l <level> [-p <position>]
```

**温度等级：**
| 值 | 名称 |
|-------|------|
| 0 | 关闭 |
| 1 | 低档 |
| 2 | 中档 |
| 3 | 高档 |

**加热位置：**
| 值 | 名称 |
|-------|-------|
| 0 | 驾驶员座椅 |
| 1 | 前排左侧 |
| 2 | 前排右侧 |
| 3 | 后排左侧 |
| 4 | 后排左侧背面 |
| 5 | 后排中央 |
| 6 | 后排右侧 |
| 7 | 后排右侧背面 |
| 8 | 第三排左侧 |
| 9 | 第三排右侧 |

**使用示例：**
```bash
command.py seat-heater -l high                    # driver (default)
command.py seat-heater -l medium -p passenger
command.py seat-heater --level low --position rear_left
command.py seat-heater -l 2 -p 4                  # medium, rear center
command.py seat-heater -l off -p driver           # turn off
```

---

### 座椅冷却器（通风系统）

**温度等级和位置设置与座椅加热器相同。**

**使用示例：**
```bash
command.py seat-cooler -l medium -p driver
command.py seat-cooler -l high -p passenger
```

---

### 自动调节座椅温度

```bash
command.py seat-climate [--position <position>] <mode>
command.py seat-climate [-p <position>] <mode>
```

模式选项：`auto`（自动调节）、`on`（开启）、`off`（关闭）

**使用示例：**
```bash
command.py seat-climate auto                      # driver auto
command.py seat-climate -p passenger auto
command.py seat-climate -p driver off             # disable auto
```

---

### 方向盘加热器

```bash
command.py steering-heater <on|off>
```

**使用示例：**
```bash
command.py steering-heater on
command.py steering-heater off
```

---

### 预出发准备

这是一个用于安排车辆出发前准备工作的现代API（替代了已废弃的`set_scheduled_departure`函数）。

#### 添加预约
```bash
command.py precondition add --time <HH:MM> [--days <days>] [--id <id>] [--one-time] [--disabled]
command.py precondition add -t <HH:MM> [-d <days>] [--id <id>]
```

**日期选项：**
| 值 | 描述 |
|-------|-------------|
| `all` | 每天（默认） |
| `weekdays` | 星期一至周五 |
| `weekends` | 周六和周日 |
| `mon,tue,wed,...` | 指定日期（用逗号分隔） |

日期示例：`sun`, `mon`, `tue`, `wed`, `thu`, `fri`, `sat`

**使用示例：**
```bash
command.py precondition add -t 08:00              # every day at 8am
command.py precondition add -t 08:00 -d weekdays  # Mon-Fri
command.py precondition add -t 07:30 -d mon,wed,fri
command.py precondition add -t 09:00 --one-time   # one-time only
command.py precondition add -t 08:30 --id 123     # modify existing schedule
command.py precondition add -t 08:00 --disabled   # create but disabled
```

#### 删除预约
```bash
command.py precondition remove --id <id>
```

**使用示例：**
```bash
command.py precondition remove --id 123
command.py precondition remove --id 1
```

---

### 充电控制

#### 启动/停止充电
```bash
command.py charge start
command.py charge stop
```

#### 设置充电限制
```bash
command.py charge limit <percent>
```

充电限制百分比必须在50%到100%之间。

**使用示例：**
```bash
command.py charge limit 80
command.py charge limit 90
command.py flash charge limit 70                  # specific vehicle
```

---

### 车门与安全设置

```bash
command.py lock                   # lock all doors
command.py unlock                 # unlock all doors
command.py honk                   # honk the horn
command.py flash                  # flash the lights
command.py wake                   # wake vehicle from sleep
```

**如果指定了车辆名称，则可以使用以下命令：**
```bash
command.py flash wake             # wake vehicle named "flash"
command.py flash flash            # flash lights on vehicle "flash"
```

---

## `vehicle_data.py` - 读取车辆数据

默认情况下，会以易于阅读的格式输出车辆数据。

### 使用方法

```bash
vehicle_data.py [VEHICLE] [flags] [--json]
```

- `VEHICLE`：车辆名称或VIN（如果只有一辆车，则可选）
- 如果不指定参数，将获取所有车辆数据 |
- `--json`：以原始JSON格式输出数据

### 可选参数

| 参数 | 含义 |
|------|------|
| `-c` | `--charge` | 电池电量、充电限制、充电状态 |
| `-t` | `--climate` | 内外温度、空调系统状态 |
| `-d` | `--drive` | 挡位、车速、动力系统状态、行驶方向 |
| `-l` | `--location` | GPS坐标 |
| `-s` | `--state` | 车门锁状态、车窗状态、里程表读数、软件版本 |
| `-g` | `--gui` | 用户界面设置（单位、24小时时间显示） |
| `-g` | `--config-data` | 车辆配置信息（型号、颜色、轮毂类型） |

**使用示例：**
```bash
# All data
vehicle_data.py
vehicle_data.py flash

# Specific data
vehicle_data.py -c                        # charge only
vehicle_data.py -c -t                     # charge + climate
vehicle_data.py flash -c -l               # charge + location

# Raw JSON
vehicle_data.py --json
vehicle_data.py -c --json
```

### 示例输出**
```
🚗 My Tesla (online)
   VIN: 5YJ... (redacted)

⚡ Charge State
────────────────────────────────────────
  Battery:    [███████████████░░░░░] 78%
  Limit:      80%
  State:      Charging
  Power:      11 kW (16A × 234V × 3φ)
  Added:      37.2 kWh
  Remaining:  10m
  Range:      438 km (272 mi)
  Cable:      IEC

🌡️  Climate State
────────────────────────────────────────
  Inside:     11.9°C
  Outside:    6.0°C
  Set to:     20.5°C
  Climate:    Off
```

---

## `auth.py` - 管理OAuth令牌和配置

用于管理OAuth令牌及相关配置。

### 使用方法

```bash
auth.py <command> [options]
```

### 命令

#### 登录（OAuth流程）
```bash
auth.py login
```
- 交互式登录：生成认证URL，提示用户输入验证码，然后交换获取令牌。
- 非交互式登录：直接交换获取令牌。

#### 交换验证码
```bash
auth.py exchange <code>
```
- 非交互式地交换获取授权码以获取令牌。

#### 刷新令牌
```bash
auth.py refresh
```
- 刷新访问令牌。注意：新令牌会自动保存。

#### 注册应用域名
```bash
auth.py register --domain <domain>
```
- 在Tesla平台上注册你的应用域名（执行命令时需要此操作）。
- 注册完成后，还需要注册你的虚拟密钥：```
https://tesla.com/_ak/<domain>
```

#### 显示配置信息
```bash
auth.py config
```
- 显示当前配置信息（敏感信息会被隐藏）。

#### 设置配置
```bash
auth.py config set [options]
```
- 参数选项：
  - `--client-id <id>`：客户端ID
  - `--client-secret <secret>`：客户端密钥
  - `--redirect-uri <uri>`：重定向URL
  - `--audience <url>`：目标受众URL
  - `--base-url <url>`：基础URL
  - `--ca-cert <path>`：CA证书路径
  - `--domain <domain>`：应用域名

**使用示例：**
```bash
# Initial setup
auth.py config set \
  --client-id "abc123" \
  --client-secret "secret" \
  --redirect-uri "http://localhost:18080/callback"

# Configure proxy
auth.py config set \
  --base-url "https://localhost:4443" \
  --ca-cert "/path/to/tls-cert.pem"
```

---

## `tesla_fleet.py` - 列出车辆信息

以易于阅读的格式列出所有车辆信息。

```bash
python3 scripts/tesla_fleet.py vehicles
python3 scripts/tesla_fleet.py vehicles --json
```

### 示例输出**
```
🚗 Name:   My Tesla
🔖 VIN:    5YJ... (redacted)
🟢 Status: Online
👤 Access: Owner
```

---

## 配置/代理/文件结构

所有设置和配置的详细信息请参考 **[SETUP.md](SETUP.md)**。

---

## 地区基础URL

| 地区 | 目标URL |
|--------|--------------|
| 欧洲 | `https://fleet-api.prd.eu.vn.cloud.tesla.com` |
| 北美 | `https://fleet-api.prd.na.vn.cloud.tesla.com` |
| 中国 | `https://fleet-api.prd.cn.vn.cloud.tesla.cn` |

所有地区的OAuth令牌请求端点相同：
```
https://fleet-auth.prd.vn.cloud.tesla.com/oauth2/v3/token
```

---

## 故障排除

### “车辆不可用：车辆处于离线状态或休眠模式”
- 先尝试唤醒车辆：```bash
command.py wake
```

### “命令未签名”/“车辆拒绝执行”
- 确保签名代理正在运行且配置正确。请参阅 [SETUP.md](SETUP.md) 中的代理设置部分。

### 令牌过期
```bash
auth.py refresh
```

### 多辆车
- 可以通过车辆名称或VIN来指定目标车辆：```bash
command.py flash climate start
command.py 5YJ... honk
```

---

## 完整命令参考

- `command.py` 的使用方法见上文。
- `vehicle_data.py` 和 `auth.py` 的使用方法也请参考上文。