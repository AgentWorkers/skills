---
name: godot-bridge
description: "通过 HTTP 或 WebSocket 远程控制 Godot 4.x 游戏。支持创建 2D/3D 图形、带效果的 UI、动画以及粒子效果；同时提供 100 多条 CLI 命令来操作游戏中的物理效果。非常适合用于 AI 驱动的游戏开发。"
metadata:
  openclaw:
    emoji: 🎮
    requires:
      bins: ["node"]
---
# Godot Bridge

这是一个用于通过 HTTP 或 WebSocket 远程控制 Godot 4.x 游戏的命令行工具（CLI）。

## 概述

godot-bridge 提供了 100 多个命令，涵盖了 UI 效果、动画、2D/3D 图形、粒子效果以及物理模拟等功能。

## 快速入门

```bash
node clawbridge.js label "Hello"
node clawbridge.js button "Click" --radius 8
node clawbridge.js shadow --path /root/Button
```

## 协议

- **HTTP**: `node clawbridge.js label "Hello"`
- **WebSocket**: `node clawbridge.js label "Hello" --ws`

## 命令

### UI 效果
```bash
node clawbridge.js shadow --path /root/Label --offset_x 2 --offset_y 2 --color #000000
node clawbridge.js outline --path /root/Button --width 2 --color #000000
node clawbridge.js gradient --path /root/Panel --c1 #ff0000 --c2 #0000ff
node clawbridge.js blur --path /root/Node --amount 0.5
node clawbridge.js fade_in --path /root/Node --duration 0.5
node clawbridge.js fade_out --path /root/Node --duration 0.5
node clawbridge.js pulse --path /root/Node --scale 1.1 --duration 0.3
node clawbridge.js shake --path /root/Node --amount 5 --duration 0.3
node clawbridge.js bounce_in --path /root/Node --duration 0.5
node clawbridge.js slide_in --path /root/Node --direction left --duration 0.3
```

### UI 动画
```bash
node clawbridge.js spin --path /root/Node --speed 360 --duration 1.0
node clawbridge.js flip --path /root/Node --horizontal --duration 0.3
node clawbridge.js blink --path /root/Node --duration 1.0
node clawbridge.js typewriter --path /root/Label "Hello World" --speed 0.1
```

### UI 状态
```bash
node clawbridge.js hover --path /root/Button --color #5aa0e9 --scale 1.05
node clawbridge.js pressed --path /root/Button --color #3a70b9 --scale 0.95
node clawbridge.js disabled --path /root/Button --opacity 0.5
```

### UI 组件
```bash
node clawbridge.js label "Text" --x 100 --y 50 --color #ffffff --shadow --outline --size 24
node clawbridge.js button "Click" --x 100 --y 100 --radius 8 --color #4a90d9 --hover_color #5aa0e9
node clawbridge.js progress 50 --x 100 --y 150 --radius 4 --color #4a90d9 --bg_color #333333
node clawbridge.js slider --min 0 --max 100 --value 50
node clawbridge.js panel --x 100 --y 100 --w 200 --h 100 --radius 8 --opacity 0.8 --shadow
```

### 2D 图形
```bash
node clawbridge.js rect --x 100 --y 100 --w 200 --h 100 --radius 8 --color #ff0000
node clawbridge.js circle --x 200 --y 200 --r 50 --color #00ff00
node clawbridge.js gradient_rect --x 100 --y 100 --w 200 --h 100 --c1 #ff0000 --c2 #0000ff --angle 90
node clawbridge.js polygon --x 200 --y 200 --sides 6 --r 50
node clawbridge.js star --x 200 --y 200 --points 5 --or 50 --ir 25
```

### 3D 基础图形
```bash
node clawbridge.js box, sphere, cylinder, capsule, torus
```

### 粒子效果
```bash
node clawbridge.js particles --amount 50 --color #ffffff
node clawbridge.js fire, smoke, sparks
```

### 照明效果
```bash
node clawbridge.js light directional --energy 1.0
node clawbridge.js omni_light --range 10
```

### 物理模拟
```bash
node clawbridge.js rigid_body --mass 1.0 --shape box
node clawbridge.js character
```

### 场景操作
```bash
node clawbridge.js tree, clear
```

## 选项

| 类别 | 选项 |
|------|------|
| 位置 | --x, --y, --z, --w, --h |
| 大小 | --size, --radius, --width, --height |
| 颜色 | --color, --c1, --c2, --bg |
| 效果 | --shadow, --outline, --blur, --opacity |
| 动画 | --duration, --speed, --scale, --amount |
| 状态 | --hover, --pressed, --disabled |

## 使用示例
```bash
# Beautiful UI
node clawbridge.js panel --x 50 --y 50 --w 400 --h 300 --radius 16 --opacity 0.9 --shadow
node clawbridge.js label "GAME TITLE" --x 150 --y 80 --size 32 --shadow --outline
node clawbridge.js button "PLAY" --x 150 --y 150 --radius 8 --color #4a90d9
node clawbridge.js progress 75 --x 150 --y 200 --radius 4
node clawbridge.js slider --x 150 --y 250

# Add effects
node clawbridge.js pulse --path /root/Button
node clawbridge.js shadow --path /root/Title
node clawbridge.js bounce_in --path /root/Panel
```

## 许可证

MIT