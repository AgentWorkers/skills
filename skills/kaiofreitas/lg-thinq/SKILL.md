---
name: lg-thinq
description: "通过 ThinQ API 控制 LG 智能家电。当用户询问关于他们的冰箱、洗衣机、烘干机、空调或其他 LG 家电的信息时，可以使用该功能。支持查看设备状态、调节温度、切换模式（快速模式、节能模式）以及监控门的状态。"
metadata: {"version":"1.0.0","clawdbot":{"emoji":"🧊","os":["darwin","linux"]}}
---

# LG ThinQ 技能

通过 ThinQ Connect API 控制 LG 智能家居设备。

## 设置

1. 从 https://connect-pat.lgthinq.com 获取个人访问令牌。
2. 保存令牌：`echo "YOUR_TOKEN" > ~/.config/lg-thinq/token`
3. 保存国家代码：`echo "MX" > ~/.config/lg-thinq/country`

## 快速命令

所有脚本都位于技能的 `scripts/` 目录中。请先激活虚拟环境（venv）：
```bash
cd ~/clawd && source .venv/bin/activate
```

### 列出设备
```bash
python3 skills/lg-thinq/scripts/thinq.py devices
```

### 获取设备状态
```bash
python3 skills/lg-thinq/scripts/thinq.py status <device_id>
python3 skills/lg-thinq/scripts/thinq.py status fridge  # alias
```

### 控制冰箱
```bash
# Set fridge temperature (0-6°C)
python3 skills/lg-thinq/scripts/thinq.py fridge-temp 3

# Set freezer temperature (-24 to -14°C typical)
python3 skills/lg-thinq/scripts/thinq.py freezer-temp -15

# Toggle express fridge
python3 skills/lg-thinq/scripts/thinq.py express-fridge on|off

# Toggle express freeze
python3 skills/lg-thinq/scripts/thinq.py express-freeze on|off

# Toggle eco mode
python3 skills/lg-thinq/scripts/thinq.py eco on|off
```

### 洗衣机/烘干机状态
```bash
python3 skills/lg-thinq/scripts/thinq.py status washer
python3 skills/lg-thinq/scripts/thinq.py status dryer
```

## 支持的设备

| 设备 | 状态 | 控制方式 |
|--------|--------|---------|
| 冰箱 | ✅ 温度、门状态、运行模式 | ✅ 温度、快速冷冻模式、节能模式 |
| WashTower 洗衣机 | ✅ 运行状态、剩余时间 | ⚠️ 功能有限 |
| WashTower 烘干机 | ✅ 运行状态、剩余时间 | ⚠️ 功能有限 |
| 空调 | ✅ 温度、运行模式 | ✅ 温度、运行模式、风扇状态 |

## 温度范围

- **冰箱**：0°C 至 6°C
- **冷冻室**：-24°C 至 -14°C（因型号而异）

## 错误处理

- `NOT_CONNECTED_DEVICE`：设备已离线，请检查 WiFi 连接或打开 ThinQ 应用程序。
- `INVALID_COMMAND_ERROR`：命令格式错误或参数超出范围。
- `NOT PROVIDED_FEATURE`：该型号不支持该功能。

## 自然语言示例

用户输入 → 执行操作：
- “检查我的冰箱” → `status fridge`
- “将冰箱温度设置为 5 度” → `fridge-temp 5`
- “开启快速冷冻模式” → `express-freeze on`
- “冰箱门开着吗？” → `status fridge`（检查门的状态）
- “洗衣机的运行情况如何？” → `status washer`