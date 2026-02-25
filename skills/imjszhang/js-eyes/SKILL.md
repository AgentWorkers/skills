---
name: js-eyes
description: 用于AI代理的浏览器自动化功能：通过WebSocket控制标签页、提取内容、执行脚本以及管理cookies。
version: 1.4.1
metadata:
  openclaw:
    emoji: "\U0001F441"
    homepage: https://github.com/imjszhang/js-eyes
    os:
      - windows
      - macos
      - linux
    requires:
      bins:
        - node
    install:
      - kind: node
        package: ws
        bins: []
---
# JS Eyes

这是一个浏览器扩展程序与WebSocket服务器的组合，它为AI代理提供了完整的浏览器自动化功能。

## 功能概述

JS Eyes通过WebSocket将浏览器扩展程序（支持Chrome、Edge、Firefox）与AI代理框架连接起来，使代理能够执行以下操作：
- 列出并管理浏览器标签页
- 打开URL并浏览页面
- 从任意标签页中提取完整的HTML内容
- 在页面上下文中执行任意JavaScript代码
- 读取指定域名的所有Cookie
- 监控已连接的浏览器客户端

## 架构

```
Browser Extension  <── WebSocket ──>  JS-Eyes Server  <── WebSocket ──>  AI Agent (OpenClaw)
 (Chrome/Edge/FF)                     (Node.js)                         (Plugin: index.mjs)
```

浏览器扩展程序在用户的浏览器中运行，并保持与JS-Eyes服务器的持久WebSocket连接。OpenClaw插件也连接到同一服务器，提供了7种AI工具、一个后台服务以及命令行接口（CLI）命令。

## 提供的AI工具

| 工具 | 描述 |
|------|-------------|
| `js_eyes_get_tabs` | 列出所有打开的浏览器标签页（包括ID、URL和标题） |
| `js_eyes_list_clients` | 列出已连接的浏览器扩展程序客户端 |
| `js_eyes_open_url` | 在新标签页或现有标签页中打开URL |
| `js_eyes_close_tab` | 通过ID关闭标签页 |
| `js_eyes_get_html` | 获取标签页的完整HTML内容 |
| `js_eyes_execute_script` | 在标签页中运行JavaScript代码并返回结果 |
| `js_eyes_get_cookies` | 获取指定标签页所在域名的所有Cookie |

## 命令行接口（CLI）命令

```
openclaw js-eyes status          # Server connection status
openclaw js-eyes tabs            # List all browser tabs
openclaw js-eyes server start    # Start the built-in server
openclaw js-eyes server stop     # Stop the built-in server
```

## 插件文件

此技能包包含了OpenClaw插件的源代码。以下文件是OpenClaw运行该插件所必需的：

| 文件 | 作用 |
|------|------|
| `openclaw.plugin.json` | 插件配置文件（包含插件ID、描述、配置模式以及设置提示） |
| `package.json` | Node.js包描述文件，声明了插件的类型和入口点 |
| `index.mjs` | 插件逻辑文件，负责注册7种AI工具、一个后台服务以及CLI命令 |

> `index.mjs` 会从父仓库（`../server/` 和 `../clients/`）导入WebSocket服务器和客户端SDK，因此需要克隆整个 [js-eyes仓库](https://github.com/imjszhang/js-eyes) 才能使插件正常工作。该文件夹本身并不具备独立运行能力。

## 先决条件

- **Node.js** 版本 >= 14
- **Git**
- 支持的浏览器：Chrome 88+ / Edge 88+ / Firefox 58+

## 安装步骤

### 第1步：安装浏览器扩展程序

从 [GitHub仓库](https://github.com/imjszhang/js-eyes/releases/latest) 下载最新版本：
- **Chrome/Edge**：下载 `js-eyes-chrome-vX.Y.Z.zip`，进入浏览器设置（Chrome：`chrome://extensions/` 或 Edge：`edge://extensions/`），启用开发者模式，选择“加载解压文件”，然后选择解压后的文件夹。
- **Firefox**：下载 `js-eyes-firefox-vX.Y.Z.xpi`，将其拖放到浏览器窗口中。

### 第2步：克隆并安装插件

```bash
git clone https://github.com/imjszhang/js-eyes.git
cd js-eyes
npm install
```

### 第3步：在OpenClaw中注册插件

编辑你的OpenClaw配置文件（`~/.openclaw/openclaw.json`），并添加插件配置：

```json
{
  "plugins": {
    "load": {
      "paths": ["~/projects/js-eyes/openclaw-plugin"]
    },
    "entries": {
      "js-eyes": {
        "enabled": true,
        "config": {
          "serverPort": 18080,
          "autoStartServer": true
        }
      }
    }
  }
}
```

> 请将 `~/projects/js-eyes/openclaw-plugin` 替换为实际克隆后的仓库中 `openclaw-plugin` 目录的绝对路径。

### 第4步：连接浏览器扩展程序

1. 启动OpenClaw——内置的WebSocket服务器会自动在端口18080上启动。
2. 点击浏览器工具栏中的JS Eyes扩展程序图标。
3. 输入 `http://localhost:18080` 作为服务器地址。
4. 点击“连接”——状态应显示为绿色（“已连接”）。

### 第5步：验证功能

运行以下CLI命令以确认一切正常：

```bash
openclaw js-eyes status
```

你还可以让AI代理列出你的浏览器标签页——它将调用 `js_eyes_get_tabs` 函数并返回标签页列表。

## 插件配置选项

| 选项 | 类型 | 默认值 | 描述 |
|--------|------|---------|-------------|
| `serverHost` | 字符串 | `"localhost"` | 服务器监听地址 |
| `serverPort` | 数字 | `18080` | 服务器端口（必须与扩展程序配置一致） |
| `autoStartServer` | 布尔值 | `true` | 插件加载时自动启动服务器 |
| `requestTimeout` | 数字 | `60` | 每次请求的超时时间（秒） |

## 故障排除

| 故障现象 | 原因 | 解决方法 |
|---------|-------|-----|
| 扩展程序显示“断开连接” | 服务器未运行 | 检查 `openclaw js-eyes status`；确保 `autoStartServer` 为 `true` |
| `js_eyes_get_tabs` 返回空结果 | 没有扩展程序连接 | 点击扩展程序图标，确认地址正确，然后点击“连接” |
| 报错“无法找到模块‘ws’” | 依赖项未安装 | 在克隆后的 `js-eyes` 目录中运行 `npm install` |
| AI工具在OpenClaw中不可用 | 插件路径错误或未启用 | 请确认 `plugins.loadpaths` 中指向的路径是否正确（应为 `openclaw-plugin` 文件夹） |

## 链接

- 项目源代码：<https://github.com/imjszhang/js-eyes>
- 版本发布：<https://github.com/imjszhang/js-eyes/releases>
- 作者：[@imjszhang](https://x.com/imjszhang)
- 许可证：MIT许可证