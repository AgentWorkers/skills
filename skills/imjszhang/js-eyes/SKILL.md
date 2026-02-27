---
name: js-eyes
description: AI代理的浏览器自动化功能：通过WebSocket控制浏览器标签页、提取内容、执行脚本以及管理cookies。
version: 1.4.3
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
- 读取指定域名的所有cookie
- 监控已连接的浏览器客户端

## 架构

```plaintext
浏览器扩展程序  ←→  WebSocket  ←→  JS-Eyes服务器  ←→  AI代理（OpenClaw）
(Chrome/Edge/Firefox)      (Node.js)        (插件：index.mjs)
```

浏览器扩展程序在用户的浏览器中运行，并与JS-Eyes服务器保持持续的WebSocket连接。OpenClaw插件连接到同一服务器，提供了7种AI工具、一个后台服务以及命令行接口（CLI）命令。

## 提供的AI工具

| 工具          | 描述                                      |
|---------------|-------------------------------------------|
| `js_eyes_get_tabs`   | 列出所有打开的浏览器标签页（包含ID、URL和标题）         |
| `js_eyes_list_clients` | 列出已连接的浏览器扩展程序客户端                |
| `js_eyes_open_url`    | 在新标签页或现有标签页中打开URL                   |
| `js_eyes_close_tab`   | 通过ID关闭标签页                        |
| `js_eyes_get_html`    | 获取标签页的完整HTML内容                    |
| `js_eyes_execute_script` | 在标签页中运行JavaScript代码并返回结果           |
| `js_eyes_get_cookies` | 获取指定标签页所在域名的所有cookie              |

## 命令行接口（CLI）命令

```bash
openclaw js-eyes status          # 查看服务器连接状态
openclaw js-eyes tabs            # 列出所有浏览器标签页
openclaw js-eyes server start    # 启动内置服务器
openclaw js-eyes server stop     # 停止内置服务器
```

## 技能包结构

此技能包从仓库根目录发布，包含运行OpenClaw插件所需的所有文件：

```plaintext
js-eyes/
├── SKILL.md                        // 技能入口文件
├── package.json                    // 包配置文件（声明WebSocket依赖）
├── LICENSE                        // 许可证文件
├── openclaw-plugin/
│   ├── openclaw.plugin.json        // 插件配置文件（包含ID、配置信息等）
│   ├── package.json                // ESM模块描述文件
│   └── index.mjs                   // 插件逻辑文件（包含AI工具、后台服务和CLI命令）
├── server/
│   ├── index.js                    // HTTP和WebSocket服务器代码
│   ├── ws-handler.js               // 连接和消息处理代码
│   └── package.json                // 服务器配置文件
└── clients/
    └── js-eyes-client.js           // 浏览器自动化用的Node.js客户端SDK
```

> `openclaw-plugin/index.mjs`通过相对路径从`../server/`和`../clients/`导入文件，因此必须保持上述目录结构；`openclaw-plugin`不能单独使用。

## 先决条件

- **Node.js**版本 >= 16
- 支持的浏览器：Chrome 88+ / Edge 88+ / Firefox 58+

## 部署到OpenClaw

通过ClawHub安装此技能：

```bash
clawhub install js-eyes
```

ClawHub会将技能包安装到当前工作目录下的`./skills`文件夹中。该技能包是自包含的，包含插件、WebSocket服务器和客户端SDK。

**安装步骤：**

1. **安装Node.js依赖**：运行`npm install`（`ws`包在运行时需要）。
2. 在`~/.openclaw/openclaw.json`文件中注册插件路径。路径应指向`openclaw-plugin`子目录。
3. 重新启动OpenClaw以加载插件。

**开发人员注意事项：**请克隆[完整仓库](https://github.com/imjszhang/js-eyes)，并将`plugins.loadpaths`配置项中的路径设置为`openclaw-plugin`目录的路径。

## 浏览器扩展程序的设置

该插件通过JS Eyes扩展程序与浏览器进行交互。请单独安装该扩展程序（无需依赖ClawHub）：

- 从[GitHub仓库](https://github.com/imjszhang/js-eyes/releases/latest)下载扩展程序：
  - **Chrome/Edge**：下载`js-eyes-chrome-vX.Y.Z.zip`文件，进入浏览器设置（`chrome://extensions/`或`edge://extensions/`），启用开发者模式，选择“加载解压文件”，然后安装扩展程序。
  - **Firefox**：下载`js-eyes-firefox-vX.Y.Z.xpi`文件，将其拖放到浏览器窗口中。
- 在工具栏中点击JS Eyes扩展程序图标，输入`http://localhost:18080`作为服务器地址，然后点击“连接”按钮；状态栏应显示绿色图标表示连接成功。

## 验证功能

运行CLI命令以确认一切正常：

```bash
openclaw js-eyes status
```

预期输出：

```plaintext
=== JS-Eyes服务器状态 ===
  运行时间：...秒
  已连接的浏览器扩展程序：1个
  自动化客户端：...
```

你还可以请求AI代理列出你的浏览器标签页——它将调用`js_eyes_get_tabs`函数并返回标签页列表。

## 插件配置选项

| 选项          | 类型        | 默认值         | 描述                                      |
|----------------|------------|---------------------------|
| `serverHost`     | 字符串       | `"localhost"`     | 服务器监听地址                          |
| `serverPort`     | 数字        | `18080`       | 服务器端口（需与扩展程序配置一致）                   |
| `autoStartServer` | 布尔值       | `true`        | 插件加载时自动启动服务器                        |
| `requestTimeout`    | 数字        | `60`        | 每次请求的超时时间（秒）                        |

## 常见问题及解决方法

| 问题            | 原因                | 解决方法                                      |
|------------------|------------------|--------------------------------------|
| 扩展程序显示“断开连接”    | 服务器未运行            | 检查`openclaw js-eyes status`；确保`autoStartServer`设置为`true`     |
| `js_eyes_get_tabs`返回空结果 | 无扩展程序连接            | 点击扩展程序图标，确认地址正确，然后重新连接                |
| 报错“找不到模块‘ws’”     | 依赖项未安装            | 在技能包根目录中运行`npm install`                    |
| 工具在OpenClaw中不可用     | 插件路径错误或未启用            | 确保`plugins.loadpaths`指向`openclaw-plugin`子目录         |
| 在Windows系统中找不到插件路径 | 路径格式错误            | 使用正斜杠（例如：`C:/Users/you/skills/js-eyes/openclaw-plugin`）         |

## 参考链接

- 项目源代码：[https://github.com/imjszhang/js-eyes]
- 版本发布：[https://github.com/imjszhang/js-eyes/releases]
- ClawHub：[https://clawhub.ai/skills/js-eyes]
- 作者：[@imjszhang](https://x.com/imjszhang)
- 许可证：MIT许可证