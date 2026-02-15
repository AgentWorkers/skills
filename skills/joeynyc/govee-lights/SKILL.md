---
name: govee-lights
description: 通过 Govee API 控制 Govee 智能灯泡。支持开关灯、调节亮度、设置颜色以及创建灯光场景。用途包括：  
(1) 通过名称控制单个或一组灯泡；  
(2) 设置灯泡的颜色和亮度；  
(3) 管理设备的状态。
---

# Govee 灯具控制

使用自然语言命令来控制 Govee 智能灯具。

## 快速参考

| 命令 | 例子 |
|---------|---------|
| 列出设备 | `python3 scripts/govee.py list` |
| 开启 | `python3 scripts/govee.py on "lamp"` |
| 关闭 | `python3 scripts/govee.py off "lamp"` |
| 调节亮度 | `python3 scripts/govee.py brightness "lamp" 75` |
| 调节颜色 | `python3 scripts/govee.py color "lamp" 255 100 50` |

## 自然语言模式

- “开启 [设备名称]”
- “关闭 [设备名称]”
- “将 [设备名称] 的亮度设置为 [亮度值]%”
- “将 [设备名称] 的颜色设置为 [颜色名称或 RGB 值]”
- “调暗/调亮 [设备名称]”

## 设置步骤

1. 从 [Govee 开发者门户](https://developer.govee.com/) 获取 API 密钥。
2. 设置环境变量：`export GOVEE_API_KEY="your-key"`
3. 安装依赖库：`pip3 install requests`

## 使用示例

```bash
# List all devices
python3 scripts/govee.py list

# Control lights
python3 scripts/govee.py on "living room"
python3 scripts/govee.py off bedroom
python3 scripts/govee.py brightness "desk lamp" 50

# Set colors (RGB 0-255)
python3 scripts/govee.py color "strip" 255 0 0      # Red
python3 scripts/govee.py color "strip" 0 255 0      # Green
python3 scripts/govee.py color "strip" 255 165 0    # Orange
```

## 故障排除

有关常见问题的解决方法，请参阅 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)。