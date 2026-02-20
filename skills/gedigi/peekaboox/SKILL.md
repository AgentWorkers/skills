---
name: linux-desktop
description: >
  **控制并自动化 Linux X11 桌面图形用户界面**  
  利用这一技能，您可以执行以下操作：  
  - 截取屏幕截图；  
  - 定位并点击屏幕上的 UI 元素；  
  - 输入文本；  
  - 发送键盘快捷键；  
  - 滚动屏幕；  
  - 管理窗口（切换焦点、最小化、最大化、关闭、移动、调整大小）；  
  - 通过视觉识别技术在屏幕上定位所需元素。  
  该技能基于 X11 协议（不支持 Wayland）。适用于桌面自动化、图形用户界面测试、远程桌面控制，以及任何需要与图形应用程序交互的任务。
metadata:
  clawdbot:
    emoji: "\U0001F5A5"
    os: ["linux"]
    requires:
      bins: ["xdotool", "wmctrl", "scrot"]
      env: ["DISPLAY"]
    install:
      - id: apt
        kind: shell
        command: bash install.sh
        label: Install dependencies (apt/dnf/pacman)
---
# Linux桌面GUI自动化

您可以自动化任何基于X11的Linux桌面操作：截取屏幕截图、查找并点击屏幕元素、输入文本、使用热键以及管理窗口。

**推荐的截图处理方式**：使用`capture.sh`截取屏幕截图，然后直接在OpenClaw的聊天界面中解析该图像（OpenClaw支持图像解析的功能）。

## 先决条件

- 必须有一个正在运行的X11会话（例如XFCE、GNOME、KDE、i3、OpenBox等）
- `DISPLAY`环境变量已设置（通常为`:0`）
- 需要运行`bash install.sh`来安装所需的依赖项
- 使用OpenClaw的图像解析功能时，不需要额外的按键来处理截图

## 快速参考

| 功能        | 命令                        |
|------------|---------------------------|
| 截取屏幕截图    | `bash capture.sh`                |
| 截取特定窗口的截图 | `bash capture.sh --window "Firefox"`        |
| 列出所有窗口    | `bash inspect.sh`                |
| 查看活动窗口信息 | `bash inspect.sh --active`            |
| 根据名称查找窗口    | `bash inspect.sh --window "Firefox"`        |
| 在指定坐标点击    | `bash click.sh --x 500 --y 300`          |
| 右键点击      | `bash click.sh --x 500 --y 300 --button right`     |
| 双击        | `bash click.sh --x 500 --y 300 --double`       |
| 相对于窗口点击    | `bash click.sh --window "Firefox" --x 200 --y 150`     |
| 输入文本      | `bash type.sh "hello world"`            |
| 在指定窗口中输入文本 | `bash type.sh --window "Terminal" "ls -la"`     |
| 发送热键        | `bash hotkey.sh "ctrl+c"`             |
| 发送回车键      | `bash hotkey.sh "Return"`             |
| 向下滚动      | `bash scroll.sh --direction down --amount 3`       |
| 在指定位置向上滚动 | `bash scroll.sh --x 500 --y 300 --direction up --amount 3` |
| 聚焦窗口      | `bash window.sh --action focus --window "Firefox"`     |
| 最小化窗口      | `bash window.sh --action minimize --window "Firefox"`     |
| 最大化窗口      | `bash window.sh --action maximize --window "Firefox"`     |
| 关闭窗口      | `bash window.sh --action close --window "Firefox"`     |
| 移动窗口      | `bash window.sh --action move --window "Firefox" --x 100 --y 50`    |
| 调整窗口大小    | `bash window.sh --action resize --window "Firefox" --width 1280 --height 800` |

## 典型的自动化工作流程

对于大多数GUI自动化任务，请按照以下步骤操作：

1. 使用`capture.sh`截取屏幕截图，并注意输出的文件路径。
2. 查看截图以了解屏幕上的内容。
3. 通过观察截图并估算目标元素的像素坐标来找到该元素。
4. 使用`click.sh`命令根据坐标执行相应的操作（例如点击）。
5. 通过再次截取屏幕截图并检查结果来验证操作是否成功。

### 示例：点击对话框中的“保存”按钮

```bash
# Step 1: Capture the screen
SCREENSHOT=$(bash capture.sh | tail -1)

# Step 2: Look at the screenshot (read the image file with your vision)
# Examine the image and identify the Save button's position

# Step 3: Click at the coordinates you identified
bash click.sh --x 450 --y 320
```

### 示例：在特定应用程序中输入文本

```bash
# Focus the terminal window and type a command
bash type.sh --window "Terminal" "ls -la"
bash hotkey.sh "Return"
```

### 示例：窗口管理

```bash
# Maximize Firefox, then focus a terminal
bash window.sh --action maximize --window "Firefox"
bash window.sh --action focus --window "Terminal"
```

## JSON输出

所有工具都支持`--json`参数，以便生成机器可读的输出格式：

```json
{"success": true, "output": "...", "error": null}
```

**失败处理**

如果自动化操作失败，请查看相应的错误信息或日志。

## 环境设置

如果`DISPLAY`环境变量未设置（例如在通过SSH远程连接时），请在调用任何工具之前手动设置它：

```bash
export DISPLAY=:0
```

对于没有图形界面的无头服务器（headless servers），请参考相应的设置指南。

## 热键参考

热键名称遵循X11标准：

| 热键          | 对应功能                         |
|---------------|-----------------------------------|
| Enter          | 回车键                          |
| Tab            | 制表键                          |
| Escape          | 退出键                          |
| Backspace        | 删除键                          |
| Delete          | 删除键                          |
| Home           | 光标定位到行首键                      |
| End            | 光标定位到行尾键                      |
| Page Up        | 向上翻页键                        |
| Page Down       | 向下翻页键                        |
| F1-F12          | F1至F12功能键                        |
| Super/Win        | Super键（或Win键）                      |
| Ctrl            | 控制键                          |
| Alt            | Alt键                          |
| Shift          | Shift键                          |
| 组合键         | `Ctrl+` + `键名`                        |

**示例组合**：`ctrl+c`（复制）、`ctrl+shift+t`（粘贴）、`alt+F4`（关闭所有窗口）、`super+d`（显示帮助菜单）。

## 限制

- 仅支持X11会话，不支持Wayland会话。
- 无法与Wayland会话中的原生应用程序进行交互。
- 某些具有自定义渲染机制的应用程序（如游戏或使用了安全策略的Electron应用程序）可能无法被自动化工具识别。
- 截图质量受桌面 compositor（合成器）的影响；如果截图显示异常，请尝试禁用compositing功能。