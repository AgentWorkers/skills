---
name: device-control
description: 提供安全的设备操作功能（如调整音量、调节屏幕亮度、打开/关闭应用程序），以支持个人自动化需求。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎛️",
        "requires": { "bins": ["node"] },
        "version": "1.1.0",
      },
  }
---
# 设备控制技能

通过命令行控制设备的音量、亮度和应用程序。支持 Linux、macOS、Windows 和 WSL 平台。

## 安全性

所有输入都会经过验证和清理，以防止命令注入攻击：
- 音量/亮度值必须介于 0 到 100 之间。
- 应用程序名称仅允许使用字母、数字、空格、连字符和下划线。
- 命令行中的特殊字符（shell metacharacters）会被屏蔽。

## 工具 API

### device_control
执行设备控制操作。

- **参数：**
  - `action`（字符串，必填）：`set_volume`、`change_volume`、`set_brightness`、`open_app` 或 `close_app` 中的一个。
  - `value`（字符串/数字，可选）：操作的参数值（音量/亮度为 0-100，`change_volume` 为增量值）。
  - `app`（字符串，可选）：应用程序的名称或路径（`open_app` 和 `close_app` 操作需要提供）。

**使用示例：**

```bash
# Set volume to 50%
node skills/device-control/ctl.js --action set_volume --value 50

# Change volume by +10 or -10
node skills/device-control/ctl.js --action change_volume --value 10
node skills/device-control/ctl.js --action change_volume --value -10

# Set brightness to 75%
node skills/device-control/ctl.js --action set_brightness --value 75

# Open an application
node skills/device-control/ctl.js --action open_app --app "firefox"
node skills/device-control/ctl.js --action open_app --app "Visual Studio Code"

# Close an application
node skills/device-control/ctl.js --action close_app --app "firefox"
```

## 平台支持

| 操作        | Linux   | macOS   | Windows | WSL   |
|------------|--------|--------|---------|--------|
| set_volume    | ✅ (pactl/amixer) | ✅ (osascript) | ✅ (nircmd) | ✅ (nircmd) |
| change_volume | ✅      | ✅      | ❌      | ❌      |
| set_brightness | ✅ (brightnessctl) | ⚠️ （需要 brightness CLI） | ✅ (WMI)  | ✅ (WMI)  |
| open_app    | ✅      | ✅      | ✅      | ✅      |
| close_app    | ✅ (pkill)   | ✅ (pkill)   | ✅ (taskkill) | ✅ (taskkill) |

## 系统要求

- **Linux：** 需要 `pactl`（PulseAudio）或 `amixer`（ALSA）；`brightnessctl`（用于控制亮度，可选）。
- **macOS：** 内置的 `osascript`；`brightness` CLI 工具（用于控制亮度，可选）。
- **Windows/WSL：** 需要 `nircmd.exe`（可从 nirsoft.net 下载）。