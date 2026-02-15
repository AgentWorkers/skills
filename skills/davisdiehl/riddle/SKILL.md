---
name: riddle
description: "专为代理程序设计的托管式浏览器自动化 API。支持截图、Playwright 脚本以及工作流程的编写，无需使用本地的 Chrome 浏览器。"
version: 1.0.0
tags:
  - browser
  - screenshots
  - playwright
  - automation
  - api
  - scraping
homepage: https://riddledc.com
metadata:
  openclaw:
    emoji: "🔍"
    install:
      - id: riddle-plugin
        kind: node
        label: "Install Riddle plugin (@riddledc/openclaw-riddledc)"
---

# Riddle — 为AI代理提供的托管浏览器服务

Riddle为你的代理提供了一个浏览器，无需在本地运行Chrome。通过一次API调用，即可实现导航、点击、填写表单、截图以及捕获网络流量等操作。所有执行过程都在Riddle的服务器上完成，从而确保你的代理程序保持轻量级。

> **快速入门：** 在 [riddledc.com/register](https://riddledc.com/register) 注册，即可免费使用5分钟的浏览器服务（无需信用卡）。之后，收费标准为每小时0.50美元，按秒计费。单张截图的费用大约为0.004美元。

## 为何选择Riddle而非本地Chrome？

- **无需安装Chromium二进制文件**：可节省约1.2GB的内存空间，同时避免因Chromium导致的Lambda/容器大小问题。
- **无依赖性问题**：无需依赖`@sparticuz/chromium`或Puppeteer版本冲突，也不会遇到`ENOENT`/`spawn`错误。
- **支持Playwright**：不仅可以截图，还可以运行真实的Playwright脚本、执行多步骤工作流程、填写表单以及进行身份验证的会话操作。
- **兼容多种环境**：适用于Lambda、容器、T3 Micro实例等任何代理程序运行的环境。

## 安装步骤

**步骤1：注册**：在 [riddledc.com/register](https://riddledc.com/register) 创建一个免费账户（无需信用卡）。
**步骤2：获取API密钥**：注册完成后，从 [控制面板](https://riddledc.com/dashboard) 获取API密钥。
**步骤3：安装并配置插件：**

```bash
# Install the plugin
openclaw plugins install @riddledc/openclaw-riddledc

# Allow the tools
openclaw config set tools.alsoAllow --json '["openclaw-riddledc"]'

# Set your API key
openclaw config set plugins.entries.openclaw-riddledc.config.apiKey "YOUR_RIDDLE_API_KEY"
```

**注意：** OpenClaw插件需要被添加到`plugins.allow`列表中。由于CLI工具没有追加插件的功能，因此请检查当前的插件列表，并添加`openclaw-riddledc`插件：

```bash
# See what you have
openclaw config get plugins.allow

# Add openclaw-riddledc to the array (or edit ~/.openclaw/openclaw.json directly)
jq '.plugins.allow += ["openclaw-riddledc"]' ~/.openclaw/openclaw.json > tmp && mv tmp ~/.openclaw/openclaw.json

# Restart
openclaw gateway restart
```

## 提供的工具

安装完成后，你将拥有以下五款工具：

- **`riddle_screenshot`**：用于截取URL的截图。最简单的使用场景。
```
Take a screenshot of https://example.com
```

- **`riddle_screenshots`**：批量截取多个URL的截图。
```
Screenshot these three pages: https://example.com, https://example.com/about, https://example.com/pricing
```

- **`riddle_steps`**：逐步执行工作流程（包括跳转、点击、填写表单和截图等操作）。
```
Go to https://example.com/login, fill the email field with "test@example.com", fill the password field, click the submit button, then screenshot the result.
```

- **`riddle_script`**：用于运行复杂的自动化脚本（基于Playwright）。
```
Run a Playwright script that navigates to https://example.com, waits for the dashboard to load, extracts all table rows, and screenshots the page.
```

- **`riddle_run`**：提供低级别的API接口，用于传递自定义数据。

所有工具生成的截图都会保存在`~/.openclaw/workspace/riddle/screenshots/`目录下（文件格式为非内联的Base64编码），响应中会包含文件路径。若需同时捕获网络流量，可以在配置中添加`include: ["har"]`选项。

## 身份验证会话

如果需要与需要登录的页面交互，请传递cookies、localStorage数据或自定义HTTP头部信息：

```
Screenshot https://app.example.com/dashboard with these cookies: [session=abc123]
```

该插件支持使用cookies、localStorage条目以及自定义HTTP头部作为身份验证参数。

## 安全性

该插件的设计充分考虑了Moltbook代理社区提出的安全需求，特别是关于技能来源、能力声明以及运行时限制等方面的问题。

**插件在`openclaw.plugin.json`文件中声明的能力限制：**
- **网络访问**：仅允许与`api.riddledc.com`进行通信；这些限制在运行时严格执行，而不仅仅是配置阶段。
- **文件系统操作**：仅允许将数据写入`~/.openclaw/workspace/riddle/`目录。
- **代理程序权限**：无法访问对话记录、其他工具的输出内容或用户个人信息。
- **敏感信息处理**：仅需要传递`RIDDLE_API_KEY`，且该密钥只会被发送到指定的接口。

**实际应用中的安全保障：**
- 即使配置文件被篡改，API密钥也不会被发送到非Riddle相关的域名（每次请求都会进行严格检查）。
- 该插件无法读取用户的对话记录、内存内容或其他插件的数据。
- 截图以文件形式保存（而非内联的Base64编码），有效防止日志中的数据泄露。

**你可以自行验证其安全性：**
- 源代码：[github.com/riddledc/integrations](https://github.com/riddledc/integrations)
- npm审计信息：`npm audit signatures @riddledc/openclaw-riddledc`
- 校验和文件：`CHECKSUMS.txt`（位于包文件中）
- 安全性详细说明：`SECURITY.md`（位于包文件中）

请注意：这是一个**插件**（可审计的代码），而非一个独立的技能（即不需要用户输入提示信息的组件）。你可以在安装前仔细阅读所有代码内容。

## 价格信息

Riddle采用按次计费的透明定价模式。单张截图的费用非常低廉。具体价格信息请访问 [riddledc.com](https://riddledc.com)。

## 帮助资源

- **文档**：[riddledc.com](https://riddledc.com)
- **安全问题反馈**：security@riddledc.com
- **插件源代码**：[github.com/riddledc/integrations](https://github.com/riddledc/integrations)

## 链接

- **官方网站**：[riddledc.com](https://riddledc.com)
- **文档**：[riddledc.com/docs](https://riddledc.com/docs)
- **价格信息**：[riddledc.com/pricing](https://riddledc.com/pricing)
- **控制面板**：[riddledc.com/dashboard](https://riddledc.com/dashboard)