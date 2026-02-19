---
name: nerve_bridge
description: 通过 macOS 的 AppleScript 实现对 Trae 的双向控制，并内置反馈机制。当需要在 Trae IDE 中执行代码/命令并等待完成确认时，可以使用此方法。
metadata:
  {
    "openclaw":
      {
        "emoji": "⚡️",
        "requires": { "bins": ["python3", "osascript"] },
        "install":
          [
            {
              "id": "system",
              "kind": "system",
              "label": "macOS System Environment",
              "description": "Depends on system Python and AppleScript. No extra installation required."
            }
          ]
      }
  }
---
# Nerve Bridge (v2)

通过 macOS 的 AppleScript 实现与 Trae 的直接神经链接，并提供闭环反馈。

## 快速入门

发送指令并等待确认：

```bash
python3 nerve_bridge.py "<instruction>"
```

示例：

```bash
python3 nerve_bridge.py "Create a new Python file and add a simple 'Hello World' function. After creating, add a print statement to test it."
```

## 工作原理

1. **信号发送**：
   - 使用 `pbcopy` 将指令内容复制到系统剪贴板。
   - AppleScript 激活 Trae 并模拟用户操作：按空格键唤醒 Trae，然后依次执行删除键、Command+V 和回车键。

2. **反馈循环**：
   - 指令中必须包含一个 Python 脚本钩子，该钩子在操作完成后会写入文件 `~/.openclaw/workspace/trae_feedback.json`。
   - 脚本会等待最多 5 分钟（300 秒）以获取反馈文件。
   - 收到反馈文件后，脚本会返回相应的 JSON 数据。

## 必需的钩子模式

在编写指令时，请在指令的末尾添加以下模式：

```python
import json, time
with open("~/.openclaw/workspace/trae_feedback.json", "w") as f:
    json.dump({"status": "success", "timestamp": time.time()}, f)
```

## 环境要求

- **平台**：仅支持 macOS。
- **依赖项**：系统自带的 Python（`python3`）和 AppleScript（`osascript`）。
- **权限要求**：终端（Terminal）需要具有“Accessibility”权限，以便接收系统事件。
- **输出文件**：`~/.openclaw/workspace/trae_feedback.json`（由脚本生成）。

## 常见问题解决方法

- **Trae 未响应**：检查 Trae 窗口是否处于活动状态以及输入内容是否被选中。
- **超时**：Trae 在 5 分钟内未完成操作。
- **权限问题**：macOS 可能需要为终端授予“System Events”权限。