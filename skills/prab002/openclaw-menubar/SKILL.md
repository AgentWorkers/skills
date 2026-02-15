---
slug: openclaw-menubar
displayName: OpenClaw Menu Bar
description: 将 OpenClaw 启用为 macOS 的原生菜单栏应用程序，并提供快速访问弹窗。**仅适用于 macOS**，不兼容 Windows 或 Linux。当用户请求“启用菜单栏”、“将程序添加到菜单栏”、“在菜单栏中运行程序”或希望在不打开完整控制面板的情况下快速访问 OpenClaw 时，请使用此功能。
---

# OpenClaw菜单栏

> **⚠️ 仅限macOS** - 本功能需要macOS系统。Windows和Linux系统不支持菜单栏应用程序。

该功能为macOS系统添加了一个原生菜单栏应用程序，方便快速使用OpenClaw——只需点击菜单栏中的螃蟹图标🦀，即可立即弹出聊天窗口。

## 快速入门

### 安装与启动

```bash
scripts/install.sh
scripts/start.sh
```

螃蟹图标将出现在您的菜单栏中。点击该图标即可打开聊天窗口。

### 停止运行

```bash
scripts/stop.sh
```

### 检查状态

```bash
scripts/status.sh
```

## 功能介绍

- **菜单栏图标**：macOS菜单栏上会显示一个螃蟹🦀图标。
- **即时聊天**：点击图标即可打开聊天窗口（无需浏览器）。
- **键盘快捷键**：使用Cmd+Shift+O切换聊天窗口的显示状态。
- **原生体验**：具备macOS系统的视觉效果，必要时会保持在屏幕顶部。
- **轻量级设计**：基于Electron框架开发，聊天窗口大小约为480x680像素。

## 图标设置

菜单栏应用程序需要以下两个图标文件（位于`assets/openclaw-menubar/icons/`目录下）：
- `icon.png`（22x22像素，透明PNG格式）
- `icon@2x.png`（44x44像素，透明PNG格式）

### 选项1：自动生成图标

```bash
cd assets/openclaw-menubar
./create-icon.sh
```

系统会自动生成一个简单的螃蟹表情符号图标。

### 选项2：自定义图标

您可以使用自己的22x22像素和44x44像素的透明PNG图片替换默认图标。

**注意**：macOS菜单栏使用单色模板模式（会自动为图标着色）。

### 窗口大小调整

请编辑`assets/openclaw-menubar/main.js`文件以调整窗口大小：

```javascript
browserWindow: {
  width: 480,  // Change width
  height: 680  // Change height
}
```

### 键盘快捷键设置

请编辑`assets/openclaw-menubar/main.js`文件以设置键盘快捷键：

```javascript
globalShortcut.register('CommandOrControl+Shift+O', () => {
  // Change 'O' to any key
});
```

## 架构说明

- 该应用程序基于Electron框架开发，使用了[menubar](https://github.com/maxogden/menubar)包。
- **头部界面**：包含品牌标识的自定义HTML页面（`index-webchat.html`）。
- **聊天内容**：通过BrowserView加载OpenClaw聊天界面，并使用认证令牌进行身份验证。
- **自动认证**：从`~/.openclaw/openclaw.json`文件中读取配置信息。

## 系统要求

- macOS系统（菜单栏应用程序仅适用于macOS）。
- OpenClaw Gateway必须运行在本地主机上。
- 需要Node.js环境（用于运行Electron应用程序）。

## 常见问题解决方法

### 图标未显示
- 确保图标为22x22像素的透明PNG图片。
- macOS菜单栏采用单色模板模式（会自动为图标着色）。

### 出现“OpenClaw未运行”的错误
- 请确认OpenClaw Gateway正在运行（使用`openclaw gateway status`命令检查）。
- 检查配置文件`~/.openclaw/openclaw.json`的内容。

### 窗口无法打开
- 查看Console.app中的日志（搜索“OpenClaw”相关信息）。
- 尝试运行`scripts/stop.sh`和`scripts/start.sh`命令来重启应用程序。

## 相关文件

- `assets/openclaw-menubar/`：完整的Electron应用程序代码。
- `scripts/install.sh`：用于安装依赖项（通过npm命令安装）。
- `scripts/start.sh`：用于启动菜单栏应用程序。
- `scripts/stop.sh`：用于终止应用程序进程。
- `scripts/status.sh`：用于检查应用程序是否正在运行。