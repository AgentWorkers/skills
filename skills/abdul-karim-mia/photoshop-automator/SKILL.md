---
name: photoshop-automator
description: "通过 COM/ExtendScript 桥接实现 Adobe Photoshop 的专业自动化。支持文本更新、应用滤镜以及执行预设动作（actions）。"
metadata:
  {
    "openclaw":
      {
        "requires": { 
          "bins": ["cscript", "osascript"], 
          "os": ["windows", "macos"],
          "env": [], 
          "config": [] 
        }
      }
  }
---

# Photoshop 自动化技能（v1.2.4）

该技能通过 VBScript 或 AppleScript，利用 ExtendScript（JSX）引擎，为在 Windows 和 macOS 上自动化 Adobe Photoshop（vCS6 - 2026+）提供了高性能的解决方案。

## 命令

- **runScript**：执行原始的 ExtendScript（ES3）代码。适用于复杂的文档操作。
- **updateText**：根据名称定位特定的文本图层，并立即更新其内容。
- **createLayer**：创建具有自定义不透明度及混合模式的新图层。
- **applyFilter**：对当前活动图层应用高斯模糊滤镜。
- **playAction**：根据名称播放录制的 Photoshop 动作（.atn）文件。
- **export**：将当前活动文档保存为高质量的 PNG 或 JPEG 格式。

## 🛠 AI 协议

### 1. 技术限制（严格）
- **仅支持 ES3 语法**：Photoshop 的 ExtendScript 引擎使用 **ECMAScript 3 (ES3)**。
    - ❌ **禁止使用**：`const`、`let`、箭头函数 `() => {}`、模板字面量 ``` `${}`` 或 `Map`/`Set`。
    - ✅ **允许使用**：仅使用 `var`、标准的 `function` 声明以及字符串连接（`'a' + b`）。
- **操作对象**：命令作用于 **当前活动文档**。如果未打开任何文档，脚本将失败，除非调用 `app.documents.add()`。

### 2. 安全性与副作用
- **文件系统访问**：`runScript` 命令允许执行任意 ExtendScript 代码。该引擎可以直接访问主机文件系统。
- **副作用**：脚本可以通过 `File` 和 `Folder` 对象在本地机器上创建、修改或删除文件。
- **验证**：在执行前务必检查动态生成的脚本，以防止对文档或文件系统造成意外修改。

### 3. 错误处理
- **GUI 模块**：如果 Photoshop 打开了模态对话框（例如“另存为”窗口或错误弹窗），COM 操作可能会挂起或失败。请引导用户关闭所有打开的对话框。
- **图层名称**：如果 `updateText` 失败，请确保提供的图层名称与 PSD 文件中的图层名称完全匹配（区分大小写）。

## 设置要求

请确保主机系统上安装了 Adobe Photoshop。该技能会自动使用已注册的 COM 服务器。

---
由 [Abdul Karim Mia](https://github.com/abdul-karim-mia) 为 OpenClaw 社区开发。