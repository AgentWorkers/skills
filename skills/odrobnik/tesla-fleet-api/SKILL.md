---
name: tesla-fleet-api
description: **使用说明：**  
当与特斯拉官方的Fleet API集成时，本文档提供了如何读取车辆/能源设备数据或发送远程指令（如启动暖通空调系统、唤醒车辆、控制充电功能）的详细指导。内容包括：开发者应用程序的注册流程、不同地区的API基础URL、OAuth令牌的管理机制（包括第三方和合作伙伴使用的令牌以及令牌的更新策略）、所需域名的配置及公钥的托管方式，以及如何利用特斯拉官方的车辆控制接口和Tesla HTTP代理来发送经过签名的车辆指令。

**关键要点：**  
1. **集成流程：** 了解如何将您的应用程序与特斯拉的Fleet API进行安全、可靠的集成。  
2. **OAuth令牌：** 学习如何获取和更新OAuth令牌，确保应用程序具有访问车辆数据的权限。  
3. **域名与公钥：** 配置正确的域名和公钥，以验证来自您应用程序的请求的合法性。  
4. **车辆控制指令：** 掌握如何通过Tesla HTTP代理发送有效的车辆控制命令。  

**适用场景：**  
- 需要读取车辆状态或执行远程操作的汽车管理系统或应用程序。  
- 需要与特斯拉的车辆管理系统进行数据交互的第三方服务提供商。  

**注意事项：**  
- 请确保遵循特斯拉的官方文档和API规范，以确保系统的稳定性和安全性。  
- 定期更新您的应用程序以适应特斯拉可能发布的任何更新或更改。
version: 1.5.0
homepage: https://github.com/odrobnik/tesla-fleet-api-skill
metadata:
  openclaw:
    emoji: "🚗"
    requires:
      bins: ["python3", "openssl"]
      env: ["TESLA_CLIENT_ID", "TESLA_CLIENT_SECRET"]
      optionalEnv: ["TESLA_AUDIENCE", "TESLA_REDIRECT_URI", "TESLA_DOMAIN", "TESLA_BASE_URL", "TESLA_CA_CERT", "TESLA_ACCESS_TOKEN", "TESLA_REFRESH_TOKEN", "TESLA_SCOPE"]

---

# Tesla Fleet API

通过官方的Fleet API来控制Tesla车辆。

## 脚本概述

| 脚本 | 功能 |
|--------|---------|
| `command.py` | 执行车辆指令（如调节温度、充电、锁车等） |
| `vehicle_data.py` | 读取车辆数据（如电池电量、车内温度、位置等） |
| `vehicles.py` | 列出车辆信息并刷新缓存 |
| `auth.py` | 管理认证和配置 |
| `tesla.oauth_local.py` | 带有本地回调服务器的OAuth辅助工具 |
| `start_proxy.sh` | 启动签名代理（用于执行车辆指令） |
| `stop_proxy.sh` | 停止签名代理 |

---

## 设置/配置

设置相关说明请参考 **`SETUP.md`**：

- [SETUP.md](SETUP.md)

项目目录结构：`{workspace}/tesla-fleet-api/`
- `config.json`：提供者凭证和非令牌配置信息 |
- `auth.json`：OAuth令牌信息 |
- `vehicles.json`：缓存的车辆列表 |
- `places.json`：预设的位置信息 |
- `proxy/`：签名代理所需的TLS相关文件 |

该项目不使用`.env`文件来存储配置信息——所有配置都存储在`config.json`或环境变量中。

---

## `command.py` - 执行车辆指令

用于对Tesla车辆发送指令。如果只有一辆车，系统会自动选择该车辆。

### 使用方法

```bash
command.py [VEHICLE] <command> [options]
```

- `VEHICLE`：车辆名称或VIN（如果只有一辆车，则可选）
- 可以不指定车辆名称直接执行指令：`command.py honk`  
- 或者指定车辆名称后执行指令：`command.py flash honk`（例如：`command.py flash` 或 `command.py honk`）

---

### 调节温度

#### 启动/关闭空调
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

#### 自动调节温度模式
```bash
command.py climate keeper <mode>
```
可选模式：`off`（关闭），`keep`（保持当前温度），`dog`（自动调节），`camp`（适合露营的环境）

---

### 座椅加热

```bash
command.py seat-heater --level <level> [--position <position>]
command.py seat-heater -l <level> [-p <position>]
```

**温度等级**：
| 值 | 名称 |
|-------|------|
| 0 | 关闭 |
| 1 | 低 |
| 2 | 中 |
| 3 | 高 |

**加热位置**：
| 值 | 名称 |
|-------|-------|
| 0 | 驾驶员座椅 |
| 1 | 前排左侧 |
| 2 | 前排右侧 |
| 3 | 后排左侧 |
| 4 | 后排左侧后方 |
| 5 | 后排中央 |
| 6 | 后排右侧 |
| 7 | 后排右侧后方 |
| 8 | 第三排左侧 |
| 9 | 第三排右侧 |

**示例**：
```bash
command.py seat-heater -l high                    # driver (default)
command.py seat-heater -l medium -p passenger
command.py seat-heater --level low --position rear_left
command.py seat-heater -l 2 -p 4                  # medium, rear center
command.py seat-heater -l off -p driver           # turn off
```

---

### 座椅制冷（通风）

**温度等级和位置与座椅加热相同**

**示例**：
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

可选模式：`auto`（自动调节），`on`（开启），`off`（关闭）

**示例**：
```bash
command.py seat-climate auto                      # driver auto
command.py seat-climate -p passenger auto
command.py seat-climate -p driver off             # disable auto
```

---

### 方向盘加热

```bash
command.py steering-heater <on|off>
```

**示例**：
```bash
command.py steering-heater on
command.py steering-heater off
```

---

### 预定出发前准备（替代了已弃用的`set_scheduled_departure`功能）

#### 添加预定
```bash
command.py precondition add --time <HH:MM> [--days <days>] [--id <id>] [--one-time] [--disabled]
command.py precondition add -t <HH:MM> [-d <days>] [--id <id>]
```

**日期选项**：
| 值 | 描述 |
|-------|-------------|
| `all` | 每天（默认） |
| `weekdays` | 星期一至周五 |
| `weekends` | 星期六和周日 |
| `mon,tue,wed,...` | 指定日期（用逗号分隔） |

日期示例：`sun`, `mon`, `tue`, `wed`, `thu`, `fri`, `sat`

**示例**：
```bash
command.py precondition add -t 08:00              # every day at 8am
command.py precondition add -t 08:00 -d weekdays  # Mon-Fri
command.py precondition add -t 07:30 -d mon,wed,fri
command.py precondition add -t 09:00 --one-time   # one-time only
command.py precondition add -t 08:30 --id 123     # modify existing schedule
command.py precondition add -t 08:00 --disabled   # create but disabled
```

#### 删除预定
```bash
command.py precondition remove --id <id>
```

**示例**：
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

**示例**：
```bash
command.py charge limit 80
command.py charge limit 90
command.py flash charge limit 70                  # specific vehicle
```

---

### 车门与安全

```bash
command.py lock                   # lock all doors
command.py unlock                 # unlock all doors
command.py honk                   # honk the horn
command.py flash                  # flash the lights
command.py wake                   # wake vehicle from sleep
```

**如果指定了车辆名称，则使用该车辆的名称执行操作：**
```bash
command.py flash wake             # wake vehicle named "flash"
command.py flash flash            # flash lights on vehicle "flash"
```

---

## `vehicle_data.py` - 读取车辆数据

默认情况下，以人类可读的格式输出车辆数据。

### 使用方法

```bash
vehicle_data.py [VEHICLE] [flags] [--json]
```

- `VEHICLE`：车辆名称或VIN（如果只有一辆车，则可选）
- 如果不使用`--json`参数，将输出所有数据 |
- 使用`--json`参数时，输出原始JSON格式的数据

### 可选参数

| 参数 | 含义 |
|------|------|
| `-c` | `--charge` | 电池电量、充电限制、充电状态 |
| `-t` | `--climate` | 内外温度、空调状态 |
| `-d` | `--drive` | 挡位、车速、功率、行驶方向 |
| `-l` | `--location` | GPS坐标 |
| `-s` | `--state` | 车门锁状态、车窗状态、里程表读数、软件版本 |
| `-g` | `--gui` | 用户界面设置（单位、24小时时间显示） |
| `-g` | `--config-data` | 车辆配置信息（型号、颜色、轮毂类型） |

**示例**：
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
- 交互式：生成认证URL，提示用户输入验证码，然后交换获取令牌。
- 非交互式：直接交换获取令牌。

#### 交换验证码
```bash
auth.py exchange <code>
```
- 非交互式方式：交换授权码以获取新的OAuth令牌。

#### 刷新令牌
```bash
auth.py refresh
```
- 刷新访问令牌。注意：新令牌会自动保存。

#### 注册应用域名
```bash
auth.py register --domain <domain>
```
- 将你的应用域名注册到Tesla系统中（执行命令时需要此步骤）。
- 注册完成后，还需要注册你的虚拟钥匙（virtual key）：
```
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

**可选参数**：
- `--client-id <id>` | 客户端ID |
- `--client-secret <secret>` | 客户端密钥 |
- `--redirect-uri <uri>` | 重定向URL |
- `--audience <url>` | 访问权限范围 |
- `--base-url <url>` | 基础URL |
- `--ca-cert <path>` | 证书文件路径 |
- `--domain <domain>` | 应用域名 |

**示例**：
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

以人类可读的格式列出所有车辆信息。

**示例输出**：
```bash
python3 scripts/tesla_fleet.py vehicles
python3 scripts/tesla_fleet.py vehicles --json
```

---

## 配置/代理/文件结构

所有设置和配置的详细信息请参考 **[SETUP.md](SETUP.md)**。

---

## 地区对应的API地址

| 地区 | API地址 |
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
- 先唤醒车辆：
```bash
command.py wake
```

### “命令未签名” / “车辆拒绝执行”
- 确保签名代理正在运行且配置正确。请参考 [SETUP.md](SETUP.md) 中的代理设置部分。

### 令牌过期
```bash
auth.py refresh
```

### 多辆车时
- 可以通过车辆名称或VIN来指定目标车辆：
```bash
command.py flash climate start
command.py 5YJ... honk
```

---

## 完整命令参考

### `command.py`

```
climate start|stop
climate temps <driver> [passenger]
climate keeper off|keep|dog|camp

seat-heater -l <level> [-p <position>]
seat-cooler -l <level> [-p <position>]
seat-climate [-p <position>] auto|on|off

steering-heater on|off

precondition add -t <HH:MM> [-d <days>] [--id <id>] [--one-time]
precondition remove --id <id>

charge start|stop
charge limit <percent>

lock
unlock
honk
flash
wake
```

### `vehicle_data.py`

```
[VEHICLE] [-c] [-t] [-d] [-l] [-s] [-g] [--config-data] [--json]
```

### `auth.py`

```
login
exchange <code>
refresh
register --domain <domain>
config
config set [--client-id] [--client-secret] [--redirect-uri] [--audience] [--base-url] [--ca-cert] [--domain]
```