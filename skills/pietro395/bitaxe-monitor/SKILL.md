---
name: bitaxe-monitor
description: 通过 HTTP API 监控 Bitaxe Gamma 比特币矿机的状态。当用户需要查看矿机的状态、哈希率、温度、功耗或相关统计数据时，可以使用此功能。支持通过配置文件或环境变量来设置设备 IP 地址；同时支持获取系统信息，并可将输出格式化为便于阅读的文本或 JSON 格式。
---

# Bitaxe Monitor

通过HTTP API监控并获取Bitaxe Gamma（及兼容型号）比特币矿机的状态信息。

## 概述

Bitaxe Gamma是一款基于BM1370 ASIC芯片的开源比特币矿机。它提供了一个REST API，地址为`http://<ip>/api/system/info`，可以返回以下实时统计数据：

- 哈希率（当前值、1分钟平均值、10分钟平均值、1小时平均值）
- 功耗和电压
- 温度（ASIC芯片温度、电压调节器温度）
- 风扇转速
- 被接受/被拒绝的矿工工作量（share statistics）
- 找到的最佳挖矿难度（best difficulty）
- WiFi状态和信号强度
- 矿机与矿池的连接信息
- 系统运行时间和版本信息

## 使用方法

使用提供的脚本来获取并显示矿机的状态：

```bash
python3 scripts/bitaxe_status.py [ip_address] [--format {json,text}] [--set-ip IP]
```

### IP配置

脚本会按以下顺序查找Bitaxe矿机的IP地址：
1. 命令行参数
2. 配置文件（`~/.config/bitaxe-monitor/config.json`）
3. `BITAXE_IP`环境变量
4. 如果以上方式均未找到IP地址，则显示错误信息

### 保存IP配置

**选项1：保存到配置文件（推荐）**
```bash
python3 scripts/bitaxe_status.py --set-ip 192.168.1.100
```
该脚本会将IP地址保存到`~/.config/bitaxe-monitor/config.json`文件中。

配置文件存储在专门的目录中，不会修改您的shell配置文件。

**选项2：设置环境变量**
```bash
export BITAXE_IP=192.168.1.100
python3 scripts/bitaxe_status.py
```

**选项3：为单个命令设置IP地址**
```bash
BITAXE_IP=192.168.1.100 python3 scripts/bitaxe_status.py
```

### 检查状态

**配置IP地址后：**
```bash
python3 scripts/bitaxe_status.py
```

**使用不同的IP地址进行检查：**
```bash
python3 scripts/bitaxe_status.py 192.168.1.105
```

**获取原始JSON数据：**
```bash
python3 scripts/bitaxe_status.py --format json
```

## API接口

Bitaxe API提供以下主要接口：

- `GET /api/system/info` - 获取完整的系统状态（默认使用）
- `GET /api/system/asic` - 获取ASIC芯片的详细信息
- `GET /api/system/statistics` - 获取历史统计数据（需要启用数据记录功能）
- `GET /api/system/statistics/dashboard` - 以仪表盘格式显示统计数据

## 主要状态字段

| 字段 | 描述 | 单位 |
|-------|-------------|------|
| `hashRate` | 当前哈希率 | GH/s |
| `hashRate_1m` | 1分钟平均哈希率 | GH/s |
| `hashRate_10m` | 10分钟平均哈希率 | GH/s |
| `power` | 功耗 | 瓦特（Watt） |
| `temp` | ASIC芯片温度 | °C |
| `vrTemp` | 电压调节器温度 | °C |
| `fanspeed` | 风扇转速百分比 | % |
| `fanrpm` | 风扇转速（RPM） |
| `sharesAccepted` | 被接受的矿工工作量 | 数量 |
| `sharesRejected` | 被拒绝的矿工工作量 | 数量 |
| `bestDiff` | 找到的最佳挖矿难度 | 数值 |
| `wifiRSSI` | WiFi信号强度 | dBm |
| `uptimeSeconds` | 系统运行时间（秒） |

## 资源

### 脚本

- `bitaxe_status.py` - 主脚本，用于获取并显示Bitaxe矿机的状态信息
  - 支持文本（人类可读）和JSON两种输出格式
  - 能够优雅地处理连接错误
  - 使用表情符号来表示关键指标
  - 从配置文件或`BITAXE_IP`环境变量中读取IP地址
  - 可通过`--set-ip`参数将IP地址保存到配置文件

## 配置

### 配置文件的位置

脚本将配置信息保存在以下路径：
```
~/.config/bitaxe-monitor/config.json
```

使用`--set-ip`参数时，该目录会自动创建。

### 环境变量

| 变量 | 描述 | 是否必填 |
|----------|-------------|----------|
| `BITAXE_IP` | Bitaxe矿机的IP地址 | 可替代配置文件使用 |

## 错误处理

脚本能够处理以下常见错误：
- 连接失败（IP地址错误、设备离线）
- JSON响应无效
- 网络超时
- 未找到IP地址（提示用户配置IP地址）

## 命令参考

| 命令 | 描述 |
|---------|-------------|
| `bitaxe_status.py` | 使用保存的配置信息检查矿机状态 |
| `bitaxe_status.py <IP>` | 检查指定IP地址的矿机状态（一次性操作） |
| `bitaxe_status.py --set-ip <IP>` | 将IP地址保存到配置文件 |
| `bitaxe_status.py --format json` | 输出原始JSON数据 |
| `bitaxe_status.py --format text` | 输出格式化的文本（默认格式） |

## 示例

**快速设置（只需执行一次）：**
```bash
python3 scripts/bitaxe_status.py --set-ip 192.168.1.100
```

**日常使用：**
```bash
python3 scripts/bitaxe_status.py
```

**检查多台矿机：**
```bash
python3 scripts/bitaxe_status.py 192.168.1.100
python3 scripts/bitaxe_status.py 192.168.1.101
```

## 参考资料

有关完整的API文档，请参阅Bitaxe的官方wiki：
https://osmu.wiki/bitaxe/api/

OpenAPI规范请参考：
https://github.com/bitaxeorg/ESP-Miner/blob/master/main/http_server/openapi.yaml