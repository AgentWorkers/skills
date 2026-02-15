---
name: desktop-mouse
description: 通过 ydotool 包装器实现本地鼠标控制
metadata: {"moltbot":{"emoji":"","os":["linux"],"requires":{"bins":["molt-mouse"]}}}
user-invocable: false
---
当用户请求移动鼠标或点击鼠标时，请执行以下操作：
- 使用 `exec` 工具，并设置 `host=gateway`。
- 仅运行以 `molt-mouse ...` 开头的命令。
- 支持的命令包括：
  - `molt-mouse move <dx> <dy>`  # 移动鼠标到指定坐标 (dx, dy)
  - `molt-mouse abs <x> <y>`  # 将鼠标移动到绝对坐标 (x, y)
  - `molt-mouse click left|right|middle`  # 分别点击鼠标左键、右键或中键
  - `molt-mouse click 0x40`  # 长按鼠标左键
  - `molt-mouse click 0x80`  # 释放鼠标左键
- 如果输入的坐标值缺失或不明确，请询问用户以获取正确的值。