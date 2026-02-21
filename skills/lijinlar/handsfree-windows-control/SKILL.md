---
name: handsfree-windows-control
description: "**通过 `handsfree-windows CLI` 控制原生 Windows 应用（UIA）和网页浏览器（Playwright）的指南**  
当您需要在 Windows 机器上自动化或测试桌面应用程序或网站时，可以使用本指南：从“开始”菜单启动应用程序、无需猜测即可查找 UI 控件、在原生应用程序中进行点击或输入操作、在浏览器中打开页面、截取屏幕截图或执行点击操作，以及录制和回放包含桌面与网页操作的 YAML 脚本。  
**使用说明：**  
本指南依赖于 `handsfree-windows CLI`，该工具会在首次使用时通过 `setup.py` 自动安装。"
---
# 免提式 Windows 控制

本文档介绍了如何使用 `handsfree-windows` CLI 来自动化原生 Windows 应用程序（UIA）和网页浏览器（Playwright）的操作。

## 首次使用：自动设置

首次使用时，请在执行任何其他命令之前先运行设置脚本：

```powershell
python scripts/setup.py
```

该脚本将完成以下操作：
1. 从 GitHub 克隆 `handsfree-windows` 到 `~/.handsfree-windows/cli/`（公共仓库，仅读权限）。
2. 通过 `pip install -e` 安装 `handsfree-windows`。
3. 安装 Playwright 及 Chromium 浏览器二进制文件（从 cdn.playwright.dev 下载，大小约 200 MB）。
4. 运行 `check_setup.py` 以验证所有设置是否正常。

**如需跳过浏览器安装，请执行以下命令：**  
```powershell
python scripts/setup.py --no-browser
```

**如需将 `handsfree-windows` 安装到自定义目录，请执行以下命令：**  
```powershell
python scripts/setup.py --install-dir "C:\your\preferred\path"
```

**已经安装了吗？可以随时通过以下命令进行验证：**  
```powershell
python scripts/check_setup.py
```

### 文件存储位置（透明存储）  
- `handsfree-windows` 的源代码：`~/.handsfree-windows/cli/`  
- 通过 `pip` 安装的模块：位于标准的 `site-packages` 目录中  
- 浏览器的持久化配置文件：`~/.handsfree-windows/browser-profiles/<engine>/`  
  （包含 cookie 和登录会话信息，删除这些文件可重置浏览器认证状态。）  
- 浏览器会话状态：`~/.handsfree-windows/browser-state.json`  
  （记录最近访问的网址。）  
- Playwright 浏览器二进制文件：`~\AppData\Local\ms-playwright\`  
  （Windows 系统下，大小约 800 MB。）  

**如需完全卸载 `handsfree-windows`，请执行以下命令：**  
```powershell
pip uninstall handsfree-windows -y
Remove-Item -Recurse -Force "$env:USERPROFILE\.handsfree-windows"
```

---

## 核心规则  
- 不要随意猜测 UI 控件的位置或功能。请先使用 `hf tree` 或 `hf inspect` 命令查看实际存在的控件。  
- 不要手动输入用户名和密码；让用户完成登录流程。  
- 尽量使用 UIA 选择器（如 `name + control_type`）而非原始坐标来定位控件。  
- 仅在需要操作画布或手写区域（如绘画应用）时使用 `drag-canvas` 命令。  
- 对于具有破坏性操作（如删除、提交、发送数据等），请先获取用户的确认。  

---

## 工作流程：桌面应用程序（UIA）  
```powershell
# Launch any installed app
hf start --app "Outlook"

# Find the window
hf list-windows --json

# Discover controls (no guessing)
hf tree --title-regex "Outlook" --depth 10 --max-nodes 30000

# Act on what was found
hf click --title "Outlook" --name "New mail" --control-type "Button"

# Inspect element under cursor
hf inspect --json
```

## 工作流程：网页浏览器（Playwright）  
```powershell
# Open URL - login sessions saved in profile automatically
hf browser-open --url "https://example.com"

# Inspect page before acting
hf browser-snapshot --fmt text

# Act
hf browser-click --text "Sign in"
hf browser-type --selector "#email" --text "user@example.com"

# Verify
hf browser-screenshot --out result.png
```

## 混合使用（同时操作桌面应用程序和网页浏览器）  
```yaml
- action: start
  args:
    app: "My Desktop App"

- action: browser-open
  args:
    url: "https://app.example.com"
    headless: false

- action: browser-click
  args:
    text: "Get Started"

- action: sleep
  args:
    seconds: 1
```

**执行方式：**  
`hf run macro.yaml`

---

## 参考资料  
- 完整的命令参考及选择器规范：`references/api_reference.md`