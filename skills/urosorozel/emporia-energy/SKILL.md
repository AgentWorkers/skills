---
name: emporia-energy
description: 通过 Emporia 云（PyEmVue）或本地的 ESPHome API 直接查询 Emporia Vue 的能源使用情况。内容包括关于如何选择/配置云模式与本地模式的指导，以及如何运行列表查询、汇总查询和电路查询命令的说明。
metadata: {"moltbot":{"emoji":"⚡","os":["darwin","linux","win32"],"requires":{"bins":["python3"],"env":["EMPORIA_MODE"]}}}
---

# Emporia Energy Skill

您可以使用 `{baseDir}/scripts` 中的脚本直接查询 Emporia Vue 设备的数据。

模式通过 `EMPORIA_MODE` 进行选择：
- `cloud`：通过 PyEmVue 使用 Emporia 云 API（类似于 Home Assistant 的集成方式）
- `esphome`：本地 ESPHome API（适用于已刷入 ESPHome 固件版本的设备）

## 选择模式（云模式或本地模式）

- 如果您的 Emporia 设备仍使用原厂固件，或者您希望使用最简单的设置方式，请选择 **cloud** 模式。此模式需要您的 Emporia 账户凭据和互联网连接。
- 仅当设备已刷入 ESPHome 固件并且位于您的局域网内时，请选择 **esphome** 模式。此时需要设备的 IP 地址/主机名以及通过端口 6053 访问设备的本地 API。

如果您不确定设备是否已刷入 ESPHome 固件，请选择云模式。

## 环境配置

### 云模式
- `EMPORIA_EMAIL`
- `EMPORIA_PASSWORD`

可选参数：
- `EMPORIA_SCALE`（`MINUTE`、`SECOND`、`MINUTES_15`、`DAY`、`MONTH`）——默认值为 `MINUTE`

### ESPHome 模式
- `ESPHOME_HOST`
- `ESPHOME_PORT`（可选，默认为 6053）
- `ESPHOME_API_KEY`（Noise PSK 格式，Base64 编码）或 `ESPHOME_PASSWORD`（旧版本使用）

## 配置步骤

**云模式：**
1. 将 `EMPORIA_MODE` 设置为 `cloud`。
2. 设置 `EMPORIA_EMAIL` 和 `EMPORIA_PASSWORD`。
3. （可选）设置 `EMPORIA_SCALE` 以指定能量单位（分钟、秒、15 分钟、天）。
4. 先运行 `list` 命令查看可用的通道信息，然后运行 `summary` 或 `circuit <name>` 命令获取详细信息。

**ESPHome 模式：**
1. 确保设备已刷入 ESPHome 固件并且位于您的局域网内。
2. 将 `EMPORIA_MODE` 设置为 `esphome`。
3. 将 `ESPHOME_HOST` 设置为设备的 IP 地址/主机名（而非 Home Assistant 的地址）。
4. 如果设备使用了加密机制，请设置 `ESPHOME_API_KEY`（Noise PSK 格式）。
5. 先运行 `list` 命令查看可用的通道信息，然后运行 `summary` 或 `circuit <name>` 命令获取详细信息。

## 命令

这些脚本支持以下命令：
- `summary`（默认命令）
- `list`（列出所有设备信息）
- `circuit <name>`（查看指定电路的详细信息）

## 使用方法

**云模式：**
```
export EMPORIA_MODE=cloud
export EMPORIA_EMAIL="you@example.com"
export EMPORIA_PASSWORD="..."
python {baseDir}/scripts/emporia_cloud.py summary
```

**ESPHome 模式：**
```
export EMPORIA_MODE=esphome
export ESPHOME_HOST="192.168.1.50"
export ESPHOME_API_KEY="base64-noise-psk"
python {baseDir}/scripts/emporia_esphome.py summary
```

## 依赖项（默认使用 `pip`）

**云模式：**
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r {baseDir}/requirements-cloud.txt
```

**ESPHome 模式：**
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r {baseDir}/requirements-esphome.txt
```

**可选：** 如果您愿意，也可以使用 `uv` 代替 `pip` 来安装所需的依赖项。

## 输出结果

脚本会输出 JSON 格式的数据，其中包含：
- 时间戳
- 能量单位
- 总能耗（估算值）
- 最耗电的电路
- 使用的通道信息

## 安全注意事项：

- 请勿泄露任何敏感信息（如密码、令牌、API 密钥）。
- 请勿提供关于硬件配置或面板连接的建议。