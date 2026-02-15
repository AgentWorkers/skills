---
name: adobe-automator
description: "通过 ExtendScript 桥接实现 Adobe 应用程序的通用自动化。支持 Photoshop、Illustrator、InDesign、Premiere Pro 和 After Effects。"
metadata:
  {
    "openclaw":
      {
        "requires": { 
          "bins": [], 
          "os": ["windows", "macos"],
          "env": [], 
          "config": [] 
        }
      }
  }
---

# Adobe Master Automator (v1.1.2)

这是一个通用技能，用于通过跨平台的 ExtendScript 桥接来自动化多个 Adobe 应用程序。

## 支持的应用程序

- **Photoshop**
- **Illustrator**
- **InDesign**
- **Premiere Pro**
- **After Effects**

## 命令

### `runScript`
在目标应用程序中执行原始的 ExtendScript (ES3) 代码。

**参数：**
- `app`: 目标应用程序（`photoshop`、`illustrator`、`indesign`、`premiere`、`aftereffects`）。
- `script`: 要执行的 JSX 代码。

## 🛠 AI 协议

### 1. 技术限制
- **仅支持 ES3 语法**：Adobe 应用程序使用 ExtendScript (ES3) 引擎，因此请避免使用现代 JavaScript 的特性。
- **目标应用程序的可用性**：确保目标应用程序已安装并在主机系统上运行（或能够启动）。

### 2. 安全性与副作用
> [!警告]
> **高风险功能**：`runScript` 命令会接受并执行任意的 ExtendScript (JSX) 代码。虽然尝试限制这一功能会违背该技能的核心用途，但用户必须了解其潜在风险。

- **文件系统访问**：Adobe ExtendScript 引擎可以通过 `File` 和 `Folder` 对象对主机文件系统进行无限制的访问。
- **不可信的脚本**：❌ **绝对** 不要执行来自不可信来源的脚本。恶意脚本可能会删除文件、窃取数据或安装持久性恶意软件。
- **验证**：在允许执行之前，务必检查 `script` 参数的内容。

## 设置
该技能会自动检测您的操作系统，并将命令路由到相应的应用程序。
- **Windows**：使用内置的 `cscript`（Windows 脚本宿主）。
- **macOS**：使用内置的 `osascript`（AppleScript）。

---
由 [Abdul Karim Mia](https://github.com/abdul-karim-mia) 为 OpenClaw 社区开发。