---
name: hidpi-mouse
description: 适用于 Linux 桌面自动化的通用高 DPI 鼠标点击处理功能：能够自动检测屏幕的缩放比例，或允许用户对任何屏幕分辨率/DPI 进行校准；同时可将 Claude 显示坐标转换为 xdotool 的屏幕坐标。
metadata: {"os": ["linux"], "requires": {"bins": ["xdotool", "scrot", "python3"]}}
user-invocable: false
---

# HiDPI 鼠标技能  
该技能支持在不同屏幕配置下进行桌面自动化操作，能够统一处理鼠标坐标。  

## 🚀 快速入门  
```bash
# Click at Claude display coordinates (auto-scales)
./scripts/click.sh 500 300

# First time? Run calibration for best accuracy
./scripts/calibrate.sh
```  

## 📐 工作原理  
当 Claude 显示截图时，会对其进行缩放。该技能会转换坐标值：  
```
Claude Display Coords → Scale Factor → xdotool Screen Coords
```  
缩放比例取决于以下因素：  
- 屏幕分辨率（1080p、1440p、4K 等）  
- DPI 设置（96、144、192 等）  
- Claude 的显示视图窗口  

## 🔧 脚本  
### click.sh – 在指定坐标处点击  
```bash
./scripts/click.sh <x> <y>           # Auto-scaled click
./scripts/click.sh --raw <x> <y>     # No scaling (screen coords)
./scripts/click.sh --double <x> <y>  # Double click
./scripts/click.sh --right <x> <y>   # Right click
```  
### calibrate.sh – 设置与配置  
```bash
./scripts/calibrate.sh              # Interactive calibration
./scripts/calibrate.sh info         # Show current config
./scripts/calibrate.sh test         # Test current scale
./scripts/calibrate.sh set 2.08     # Manually set scale
./scripts/calibrate.sh reset        # Reset to auto-detect
```  
### detect-scale.sh – 获取缩放比例  
```bash
./scripts/detect-scale.sh           # Returns scale (e.g., 2.08)
```  
### 其他脚本  
```bash
./scripts/move.sh <x> <y>           # Move mouse
./scripts/drag.sh <x1> <y1> <x2> <y2>  # Drag
./scripts/reliable_click.sh <x> <y> [--window "Name" --relative]
```  

## 🎯 校准（推荐在新系统上使用）  
为了在您的系统中获得最佳精度，请执行以下操作：  
```bash
./scripts/calibrate.sh
```  
1. 创建一张包含标记的校准图片。  
2. 指定这些标记在 Claude 显示界面中的位置。  
3. 计算并保存准确的缩放比例。  

## 📊 常见缩放比例  
| 屏幕分辨率 | DPI | 典型缩放比例 |  
|--------|-----|---------------|  
| 1920×1080 | 96 | 1.0 – 1.2 |  
| 2560×1440 | 96 | 1.3 – 1.5 |  
| 3024×1772 | 192 | 2.08 |  
| 3840×2160 | 192 | 2.0 – 2.5 |  

## 🔍 故障排除  
### 点击位置偏移  
```bash
# Run calibration
./scripts/calibrate.sh

# Or manually adjust
./scripts/calibrate.sh set 2.1  # Try different values
```  
### 检查当前配置  
```bash
./scripts/calibrate.sh info
```  
### 重置所有设置  
```bash
./scripts/calibrate.sh reset
rm -f /tmp/hidpi_scale_cache
```  

## 📁 配置文件  
- `~/.config/hidpi-mouse/scale.conf` – 用户自定义的缩放比例（优先级最高）  
- `/tmp/hidpi_scale_cache` – 自动检测到的缩放比例缓存（缓存有效期为 1 小时）  

## 🌐 全平台兼容性  
该技能可自动适应：  
- ✅ 不同的屏幕分辨率（1080p 至 4K+）  
- ✅ 不同的 DPI 设置（96、120、144、192 等）  
- ✅ 高 DPI/Retina 显示屏  
- ✅ 多显示器环境（主显示器）  

## 💡 使用建议  
1. 在新系统上务必进行校准，以确保 100% 的精度。  
2. 如果更改了显示设置，请重新校准。  
3. 如果您已有屏幕坐标，可以使用 `--raw` 参数。  
4. 通过运行 `calibrate.sh info` 命令查看当前配置信息。  

## 📝 示例工作流程  
```bash
# 1. Take screenshot
scrot /tmp/screen.png

# 2. View in Claude, identify button at display coords (500, 300)

# 3. Click it
./scripts/click.sh 500 300

# 4. If off-target, calibrate
./scripts/calibrate.sh
```  

*已在 Ubuntu/Debian 系统（使用 X11 框架）上测试，支持多种屏幕分辨率和 DPI 设置。*