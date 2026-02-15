---
name: holocube
description: 使用 HoloClawd 固件控制 Control GeekMagic HelloCubic-Lite 全息立方体显示器。该显示器支持绘图 API、带有龙虾吉祥物的番茄工作法计时器、GIF 文件上传以及程序化动画功能。
homepage: https://github.com/andrewjiang/HoloClawd-Open-Firmware
metadata: {"clawdbot":{"emoji":"🦞","os":["darwin","linux"]}}
triggers:
  - holocube
  - holo cube
  - holoclawd
  - cubic
  - geekmagic
  - display gif
  - cube animation
  - pomodoro
  - lobster timer
  - water tracker
  - hydration
  - drink water
---

# HoloCube控制器

通过HoloClawd固件和REST API来控制GeekMagic HelloCubic-Lite设备。

**固件链接：** https://github.com/andrewjiang/HoloClawd-Open-Firmware

## 设备信息

- **型号：** 配备HoloClawd固件的HelloCubic-Lite
- **显示屏：** 240x240px的ST7789 TFT屏幕
- **默认IP地址：** 192.168.7.80（可配置）

## 快速入门

**番茄工作法计时器：**

```bash
# Run pomodoro timer with lobster mascot (25 min work, 5 min break)
cd ~/Bao/TimeToLockIn/HoloClawd-Open-Firmware/examples && uv run --script pomodoro.py

# With custom task label (max 20 chars)
cd ~/Bao/TimeToLockIn/HoloClawd-Open-Firmware/examples && uv run --script pomodoro.py --task "BUILD NETWORK"

# With Spotify integration
cd ~/Bao/TimeToLockIn/HoloClawd-Open-Firmware/examples && uv run --script pomodoro.py --task "LP UPDATE" --spotify-work "spotify:episode:5yJKH11UlF3sS3gcKKaUYx" --spotify-break "spotify:episode:4U4OloHPFBNHWt0GOKENVF"

# Custom timings
cd ~/Bao/TimeToLockIn/HoloClawd-Open-Firmware/examples && uv run --script pomodoro.py --work 50 --short 10 --long 20
```

**绘图API**（需要从仓库中下载`holocube_client.py`文件）：

```bash
# Draw something on the display
python3 -c "
from holocube_client import HoloCube, Color, draw_lobster
cube = HoloCube('192.168.7.80')
cube.clear(Color.BLACK)
draw_lobster(cube, 120, 120)  # Draw lobster in center
"
```

## Python客户端库

`holocube_client.py`模块提供了完整的程序化控制功能：

```python
from holocube_client import HoloCube, Color, draw_lobster, draw_confetti

cube = HoloCube("192.168.7.80")

# Drawing primitives
cube.clear("#000000")                              # Clear screen
cube.pixel(x, y, color)                            # Single pixel
cube.line(x0, y0, x1, y1, color)                   # Line
cube.rect(x, y, w, h, color, fill=True)            # Rectangle
cube.circle(x, y, r, color, fill=True)             # Circle
cube.triangle(x0, y0, x1, y1, x2, y2, color)       # Triangle
cube.ellipse(x, y, rx, ry, color, fill=True)       # Ellipse
cube.roundrect(x, y, w, h, r, color, fill=True)    # Rounded rectangle
cube.text(x, y, "Hello", size=3, color="#00ffff")  # Text

# High-level helpers
cube.centered_text(y, "Centered", size=2)
cube.show_message(["Line 1", "Line 2"], colors=[Color.CYAN, Color.WHITE])
cube.show_timer(seconds, label="FOCUS")
cube.show_progress(0.75, label="Loading")

# Lobster mascot
draw_lobster(cube, 120, 120)                       # Normal lobster
draw_lobster(cube, 120, 120, happy=True, frame=0)  # Party mode with confetti
draw_confetti(cube, 120, 120, frame=1)             # Animate confetti
```

## 番茄工作法计时器

完整的番茄工作法计时器功能，其中包含一个可爱的龙虾图案——该功能位于HoloCube固件仓库中：

```bash
# Always run from the examples directory
cd ~/Bao/TimeToLockIn/HoloClawd-Open-Firmware/examples

# Default: 25 min work, 5 min break
uv run --script pomodoro.py

# With custom task label
uv run --script pomodoro.py --task "CODE REVIEW"
uv run --script pomodoro.py --task "BUILD NETWORK"

# With Spotify integration (Andrew's favorite URIs)
uv run --script pomodoro.py --task "LP UPDATE" \
  --spotify-work "spotify:episode:5yJKH11UlF3sS3gcKKaUYx" \
  --spotify-break "spotify:episode:4U4OloHPFBNHWt0GOKENVF"

# Custom timings
uv run --script pomodoro.py --work 50 --short 10 --long 20

# With trackers
uv run --script pomodoro.py --water 2 --exercise 1 --focus 3
```

**文件位置：** `~/Bao/TimeToLockIn/HoloClawd-Open-Firmware/examples/pomodoro.py`
- 使用同一目录下的`spotify.sh`文件进行音乐播放
- 支持基于图标的任务追踪器（如喝水、锻炼、专注等）
- 提供交互式命令监听功能，以实现实时控制

**命令参数：**
- `--task`：工作期间的任务标签（最多20个字符，自动转换为大写）
- `--work`：工作时长（默认值：25分钟）
- `--short`：短暂休息时长（默认值：5分钟）
- `--long`：长时间休息时长（默认值：15分钟）
- `--sessions`：连续进行长时间休息的次数（默认值：4次）
- `--spotify-work`：工作会话对应的Spotify URI
- `--spotify-break`：休息会话对应的Spotify URI
- `--water`：当天饮用的水杯数量
- `--exercise`：完成的锻炼次数
- `--focus`：完成的专注会话次数
- `--pills-done`：标记每日服药情况

**功能特点：**
- 独特的龙虾图案会陪伴您工作（表情严肃）
- 休息期间会显示欢快的龙虾图案及闪烁的彩带效果
- 会话之间会有闪烁的提示信息
- 支持通过AppleScript在macOS系统上播放Spotify音乐
- 屏幕上会显示基于图标的任务追踪器
- 提供键盘交互式命令输入功能

## 任务追踪器

番茄工作法计时器支持使用Kyrise图标包进行视觉追踪。您可以将追踪器的数据作为参数传递给程序，以便在会话期间显示相应的图标：

```bash
cd ~/Bao/TimeToLockIn/HoloClawd-Open-Firmware/examples

# Water tracking (glasses consumed)
uv run --script pomodoro.py --water 3

# Exercise sessions
uv run --script pomodoro.py --exercise 1

# Focus sessions completed
uv run --script pomodoro.py --focus 2

# Pills taken today
uv run --script pomodoro.py --pills-done

# Combine multiple trackers
uv run --script pomodoro.py --task "DEEP WORK" --water 3 --exercise 1 --focus 2
```

追踪器图标会显示在HoloCube显示屏上，并显示当前的计数情况。

## 原生固件工具

### `holocube.py` – GIF文件上传功能（原生固件）

```bash
uv run --script holocube.py upload animation.gif
uv run --script holocube.py show animation.gif
uv run --script holocube.py list
```

### `gifgen.py` – 动画生成工具

```bash
uv run --script gifgen.py fire output.gif
uv run --script gifgen.py plasma output.gif
uv run --script gifgen.py matrix output.gif
uv run --script gifgen.py sparkle output.gif
```

## 绘图API接口

HoloClawd固件提供了以下REST接口：

```bash
# Clear screen
curl -X POST http://192.168.7.80/api/v1/draw/clear -d '{"color":"#000000"}'

# Draw shapes
curl -X POST http://192.168.7.80/api/v1/draw/circle -d '{"x":120,"y":120,"r":50,"color":"#ff0000","fill":true}'
curl -X POST http://192.168.7.80/api/v1/draw/rect -d '{"x":10,"y":10,"w":100,"h":50,"color":"#00ff00"}'
curl -X POST http://192.168.7.80/api/v1/draw/triangle -d '{"x0":120,"y0":50,"x1":80,"y1":150,"x2":160,"y2":150,"color":"#0000ff"}'
curl -X POST http://192.168.7.80/api/v1/draw/ellipse -d '{"x":120,"y":120,"rx":60,"ry":30,"color":"#ffff00"}'
curl -X POST http://192.168.7.80/api/v1/draw/line -d '{"x0":0,"y0":0,"x1":240,"y1":240,"color":"#ffffff"}'
curl -X POST http://192.168.7.80/api/v1/draw/text -d '{"x":60,"y":100,"text":"Hello","size":3,"color":"#00ffff"}'

# Batch multiple commands
curl -X POST http://192.168.7.80/api/v1/draw/batch -d '{"commands":[...]}'
```

## 固件源代码

**链接：** https://github.com/andrewjiang/HoloClawd-Open-Firmware

**构建与固件刷新步骤：**

```bash
git clone https://github.com/andrewjiang/HoloClawd-Open-Firmware.git
cd HoloClawd-Open-Firmware
pio run                    # Build
curl -X POST -F "file=@.pio/build/esp12e/firmware.bin" http://192.168.7.80/api/v1/ota/fw
```

## 颜色参考

```python
Color.BLACK   = "#000000"
Color.WHITE   = "#ffffff"
Color.RED     = "#ff0000"
Color.GREEN   = "#00ff00"
Color.BLUE    = "#0000ff"
Color.CYAN    = "#00ffff"
Color.MAGENTA = "#ff00ff"
Color.YELLOW  = "#ffff00"
Color.ORANGE  = "#ff6600"
Color.PURPLE  = "#9900ff"
```

## 故障排除**

- **无法连接**：请检查WiFi连接，设备应设置为192.168.7.80地址
- **绘图速度较慢**：每次HTTP请求耗时约50毫秒，建议使用批量API进行复杂绘图操作
- **屏幕闪烁**：仅在首帧时清除屏幕内容，文本更新时使用背景颜色