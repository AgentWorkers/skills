---
name: homey
description: 通过本地（LAN/VPN）或云端API来控制Aathom Homey智能家居设备。可以列出/控制设备、触发预设的操作流程（flows）、查询设备的状态或所在区域（zones）。该功能兼容Homey Pro、Cloud以及Bridge版本。
metadata: {"clawdbot":{"requires":{"bins":["homeycli"]},"install":[{"id":"homey-npm","kind":"node","package":".","bins":["homeycli"],"label":"Install Homey CLI"}]}}
---

# Homey 智能家居控制

通过本地（LAN/VPN）或云 API，使用令牌认证来控制 Athom Homey 设备。

## 设置

需要 Node.js >= 18。

1. **选择本地模式或云模式**

   - **本地模式（LAN/VPN）：** 使用 Homey Web 应用程序提供的本地 API 密钥和 Homey 的 IP 地址
   - **云模式（远程/无头模式）：** 使用开发者工具提供的云令牌

2. **进行配置**

   **本地模式（推荐在设备运行于本地网络时使用）：**

   ```bash
   homeycli auth discover-local --save --pick 1
   echo "<LOCAL_API_KEY>" | homeycli auth set-local --stdin
   # or interactive (hidden input): homeycli auth set-local --prompt
   ```

   **云模式（推荐用于 VPS 或无头服务器托管）：**

   ```bash
   echo "<CLOUD_TOKEN>" | homeycli auth set-token --stdin
   # or interactive (hidden input): homeycli auth set-token --prompt
   ```

   检查设备状态：

   ```bash
   homeycli auth status
   ```

3. **测试连接**

   ```bash
   homeycli status
   ```

## 命令

### 快照（推荐用于设备控制）
```bash
homeycli snapshot --json
homeycli snapshot --json --include-flows
```

### 列出设备
```bash
homeycli devices              # Pretty table output
homeycli devices --json       # JSON output for AI parsing (includes latest values)

# Filter by name (returns multiple matches)
homeycli devices --match "kitchen" --json
```

### 控制设备
   - 打开/关闭设备：
   ```bash
homeycli device "Living Room Light" on
homeycli device "Bedroom Lamp" off
```

   - 设置设备特定功能：
   ```bash
homeycli device "Dimmer" set dim 0.5                    # 50% brightness
homeycli device "Thermostat" set target_temperature 21  # Set temperature
homeycli device "RGB Light" set light_hue 0.5           # Hue (0-1)
homeycli device "Lock" set locked true                  # Lock device
```

   - 获取设备功能值：
   ```bash
homeycli device "Thermostat" get measure_temperature
homeycli device "Motion Sensor" get alarm_motion

# Get all values for a device (multi-sensors)
homeycli device "Living Room Air" values
homeycli device "Living Room Air" get
```

### 自动化流程
```bash
homeycli flows                        # List all flows
homeycli flows --json                 # JSON output
homeycli flows --match "good" --json  # Filter flows by name
homeycli flow trigger "Good Night"    # Trigger by name
homeycli flow trigger <flow-id>       # Trigger by ID
```

### 区域（房间）
```bash
homeycli zones           # List all zones/rooms
homeycli zones --json    # JSON output
```

### 设备状态
```bash
homeycli status    # Show Homey connection info
```

## 常见功能

| 功能 | 类型 | 描述 | 示例 |
|------------|------|-------------|---------|
| `onoff` | 布尔值 | 开/关设备 | `true`, `false` |
| `dim` | 数值 | 亮度（0-1） | `0.5`（50%） |
| `light_hue` | 数值 | 色彩色调（0-1） | `0.33`（绿色） |
| `light_saturation` | 数值 | 色彩饱和度（0-1） | `1.0`（全饱和） |
| `light_temperature` | 数值 | 色温（0-1） | `0.5`（中性色） |
| `target_temperature` | 数值 | 温度设定值（°C） | `21` |
| `measure_temperature` | 数值 | 当前温度（只读） | - |
| `locked` | 布尔值 | 设备锁定状态 | `true`, `false` |
| `alarm_motion` | 布尔值 | 运动检测（只读） | - |
| `alarm_contact` | 布尔值 | 接触传感器状态（只读） | - |
| `volume_set` | 数值 | 音量（0-1） | `0.5` |

使用 `homeycli devices` 命令查看每个设备支持的功能。

## 模糊匹配

设备和自动化流程的名称支持模糊匹配：
- **精确匹配**： "Living Room Light" → 查找 "Living Room Light"
- **子字符串匹配**： "living light" → 查找 "Living Room Light"
- **Levenshtein 距离匹配**： "livng light" → 查找 "Living Room Light"（容忍拼写错误）

## JSON 模式

在任何命令后添加 `--json` 以获得机器可读的输出：
```bash
homeycli devices --json | jq '.[] | select(.class == "light")'
homeycli status --json
```

## 示例

**早晨例程：**
```bash
homeycli device "Bedroom Light" on
homeycli device "Bedroom Light" set dim 0.3
homeycli device "Thermostat" set target_temperature 20
```

**检查温度：**
```bash
homeycli device "Living Room" get measure_temperature
```

**触发场景：**
```bash
homeycli flow trigger "Movie Time"
```

**列出所有灯：**
```bash
homeycli devices --json | jq '.[] | select(.class == "light") | .name'
```

## 故障排除

**“未配置认证信息”**

**本地模式（LAN/VPN）：**
- 保存本地配置：`echo "<LOCAL_API_KEY>" | homeycli auth set-local --address http://<homey-ip> --stdin`

**云模式（远程/无头模式）：**
- 保存云令牌：`echo "<CLOUD_TOKEN>" | homeycli auth set-token --stdin`
- 云令牌可以在 Homey 开发者工具中生成：https://tools.developer.homey.app/api/clients

**“设备未找到”/匹配结果不明确**
- 使用 `homeycli devices --json`（或 `homeycli devices --match <查询> --json`）列出设备，以找到正确的设备 ID
- 如果查询匹配到多个设备，CLI 会返回候选 ID，需要您通过 ID 来指定目标设备

**“功能不受支持”**
- 使用 `homeycli devices` 命令查看设备支持的功能
- 常见问题：尝试打开传感器时使用 `set` 而不是 `get` 命令

## API 参考

该命令行工具使用官方的 `homey-api` npm 包（版本 3.15.0）。

**认证/连接模式：**

- **本地模式：** 使用 Homey Web 应用程序提供的本地 API 密钥，通过 `HomeyAPI.createLocalAPI({ address, token })` 进行连接。
- **云模式：** 使用云令牌（PAT）通过 `AthomCloudAPI` 创建会话并访问设备、自动化流程和区域。