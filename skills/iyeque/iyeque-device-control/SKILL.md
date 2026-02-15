---
name: device-control
description: 提供安全的设备操作接口（如调整音量、调节屏幕亮度、打开/关闭应用程序等），以支持个人自动化需求。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎛️",
        "requires": { "bins": ["node"] },
      },
  }
---

# 设备控制技能

通过命令行控制设备的音量、亮度以及应用程序。

## 工具 API

### device_control
执行设备控制操作。

- **参数：**
  - `action` (字符串，必填)：`set_volume`、`change_volume`、`set_brightness`、`open_app`、`close_app` 中的一个。
  - `value` (字符串/数字，可选)：操作的参数值（例如，音量或亮度的百分比）。
  - `app` (字符串，可选)：应用程序的名称或路径（仅对 `open_app` 和 `close_app` 操作有效）。

**用法：**

```bash
node skills/device-control/ctl.js --action set_volume --value 50
node skills/device-control/ctl.js --action open_app --app "firefox"
node skills/device-control/ctl.js --action close_app --app "firefox"
```