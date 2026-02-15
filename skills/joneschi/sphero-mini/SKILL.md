---
name: sphero-mini
description: 通过蓝牙低功耗（Bluetooth Low Energy, BLE）技术控制 Sphero Mini 机器人球。该机器人球可以滚动、改变颜色、读取传感器数据、绘制形状，还能与猫咪互动。该解决方案使用 bleak 库来实现跨平台（macOS/Windows/Linux）的 BLE 支持。
homepage: https://github.com/trflorian/sphero_mini_win
metadata:
  {
    "openclaw":
      {
        "emoji": "⚽",
        "requires": { "bins": ["python3"], "packages": ["bleak"] },
        "install":
          [
            {
              "id": "sphero-bleak",
              "kind": "pip",
              "package": "bleak",
              "label": "Install bleak (Bluetooth Low Energy library for macOS/Windows/Linux)",
            },
          ],
      },
  }
---

# Sphero Mini 控制

使用 Python 和 bleak 通过蓝牙低功耗 (Bluetooth Low Energy) 来控制你的 Sphero Mini 机器人球。

## 特点

- 🎨 **LED 控制** - 更改主 LED 的颜色和背光 LED 的亮度
- 🎯 **移动** - 以可变的速度向任意方向滚动
- 🎲 **随机模式** - 具有不可预测运动的“猫咪玩耍模式”
- 📐 **绘制形状** - 可以绘制正方形、星星和圆形等图案
- 🔋 **电源管理** - 唤醒、进入睡眠状态并检查电池电量
- 🧭 **方向控制** - 重置和调整机器人的朝向
- 🖥️ **跨平台** - 支持 macOS、Windows 和 Linux（使用 bleak，而非 bluepy）

## 设置

### 1. 安装依赖项

**所有平台：**
```bash
pip3 install bleak
```

### 2. 查找你的 Sphero Mini 的 MAC/UUID

**macOS/Windows：**
使用附带的扫描脚本：
```bash
python3 scripts/scan_sphero.py
```

查找名为“SM-XXXX”（Sphero Mini）的设备。

### 3. 更新 MAC 地址

编辑脚本，并将 `SPHERO_MAC` 替换为你的设备的 MAC 地址。

## 快速入门

### 扫描 Sphero Mini

```bash
python3 scripts/scan_sphero.py
```

### 更改颜色

```python
import asyncio
from sphero_mini_bleak import SpheroMini

async def change_color():
    sphero = SpheroMini("YOUR-MAC-ADDRESS")
    await sphero.connect()
    await sphero.wake()
    
    # Set to red
    await sphero.setLEDColor(255, 0, 0)
    await asyncio.sleep(2)
    
    await sphero.disconnect()

asyncio.run(change_color())
```

### 向前滚动

```python
import asyncio
from sphero_mini_bleak import SpheroMini

async def roll_forward():
    sphero = SpheroMini("YOUR-MAC-ADDRESS")
    await sphero.connect()
    await sphero.wake()
    
    # Roll forward at speed 100
    await sphero.roll(100, 0)
    await asyncio.sleep(3)
    
    # Stop
    await sphero.roll(0, 0)
    await sphero.disconnect()

asyncio.run(roll_forward())
```

## 预构建脚本

### 🐱 猫咪玩耍模式（随机运动）

```bash
python3 scripts/cat_play.py
```

使 Sphero 随机移动 1 分钟，并改变颜色——非常适合与猫咪玩耍！

### 📐 绘制形状

```bash
# Draw a square
python3 scripts/draw_square.py

# Draw a star
python3 scripts/draw_star.py
```

### 🎨 颜色控制

```bash
# Set specific color
python3 scripts/set_color.py red
python3 scripts/set_color.py 255 0 128  # Custom RGB
```

## 常用命令

### 移动
```python
# Roll (speed: 0-255, heading: 0-359 degrees)
await sphero.roll(speed=100, heading=0)    # Forward
await sphero.roll(100, 90)                  # Right
await sphero.roll(100, 180)                 # Backward
await sphero.roll(100, 270)                 # Left
await sphero.roll(0, 0)                     # Stop
```

### LED 控制
```python
# Main LED color (RGB values 0-255)
await sphero.setLEDColor(red=255, green=0, blue=0)      # Red
await sphero.setLEDColor(0, 255, 0)                     # Green
await sphero.setLEDColor(0, 0, 255)                     # Blue
await sphero.setLEDColor(128, 0, 128)                   # Purple

# Back LED brightness (0-255)
await sphero.setBackLED(255)  # Full brightness
await sphero.setBackLED(0)    # Off
```

### 电源管理
```python
# Wake from sleep
await sphero.wake()

# Go to sleep (low power, BLE still on)
await sphero.sleep()

# Check battery voltage
voltage = await sphero.getBatteryVoltage()
print(f"Battery: {voltage}V")
```

## 提示

- **唤醒 Sphero**：在连接之前摇晃它以使其从深度睡眠中醒来
- **连接超时**：如果连接失败，请摇晃 Sphero 并重新尝试
- **寻找 Sphero**：脚本执行完成后，Sphero 会显示为白色以便于识别
- **猫咪安全**：与猫咪玩耍时请使用柔软的表面以避免损坏

## 示例：猫咪玩耍模式

猫咪玩耍模式脚本会使 Sphero：
- 以随机方向移动（速度在 40-120 之间）
- 随机改变颜色（6 种鲜艳的颜色）
- 不可预测地停止（有 30% 的概率会短暂停顿）
- 持续运行 exactly 1 分钟
- 最后显示为白色以便于找到

非常适合娱乐猫咪！🐱

## 故障排除

### 无法连接

1. 摇晃 Sphero 以唤醒它
2. 确保它没有连接到 Sphero Edu 应用程序
3. 检查 MAC/UUID 地址是否正确
4. 尝试增加 `sphero_mini_bleak.py` 中的超时时间

### Sphero 不移动

1. 先调用 `await sphero.wake()`
2. 唤醒后等待 1-2 秒
3. 检查电池电量

### 颜色不改变

1. 在颜色变化之间添加 `await asyncio.sleep(0.5)`
2. 确保已经调用了 `await sphero.wake()`

## 库引用

本工具使用了以下库：
- [sphero_mini_win](https://github.com/trflorian/sphero_mini_win) 由 trflorian 开发——使用 bleak 的 Sphero Mini 控制库
- [bleak](https://github.com/hbldh/bleak) — 跨平台的蓝牙低功耗库

**注意**：此库仅适用于 Sphero Mini。对于其他 Sphero 型号（BB8、SPRK+、Bolt），请使用 [pysphero](https://github.com/EnotYoyo/pysphero)。

## 高级用法

### 自定义运动模式

创建你自己的运动模式：
```python
async def figure_eight():
    # Draw a figure-8 pattern
    for i in range(2):  # Two loops
        for heading in range(0, 360, 10):
            await sphero.roll(80, heading)
            await asyncio.sleep(0.1)
```

### 颜色循环

```python
async def rainbow():
    colors = [
        (255, 0, 0), (255, 127, 0), (255, 255, 0),
        (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)
    ]
    for r, g, b in colors:
        await sphero.setLEDColor(r, g, b)
        await asyncio.sleep(1)
```

## 文档

- **SKILL.md** — 本文件
- **references/api.md** — 完整的 API 参考
- **references/troubleshooting.md** — 常见问题及解决方法
- **scripts/** — 可直接使用的示例脚本

## 许可证

MIT