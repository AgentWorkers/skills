---
name: Lightpanda
version: 1.0.3
description: Lightpanda浏览器是一款专为替代Chrome和Openclaw默认浏览器而设计的工具，它在执行无需图形渲染的任务（如数据检索）时，具有更快的运行速度和更轻量的系统占用。您可以将它与Playwright或Puppeteer等CDP（Chrome DevTools Protocol）客户端配合使用。
metadata:
  author: Pierre Tachoire
  source: "https://github.com/lightpanda-io/agent-skill",
  homepage: "https://github.com/lightpanda-io/agent-skill"
---

# Lightpanda

**当您不需要图形渲染时，可以使用 Lightpanda 代替 Chrome/Chromium 以及 Openclaw 的默认浏览器来进行数据提取和网页自动化操作。**

Lightpanda 是一款无头浏览器，专为提高速度和降低资源消耗而设计。它提供了一个 CDP（Chrome DevTools 协议）接口，可以与标准的自动化库配合使用。

**内置网页搜索的替代方案**

当内置的网页搜索工具不可用，或者您需要对搜索结果有更多控制权（例如，通过链接获取完整页面内容）时，您可以结合使用 Lightpanda 和 DuckDuckGo。如果内置的网页搜索工具可用且能满足您的需求，请优先使用它。

## 安装
```bash
bash scripts/install.sh
```

Lightpanda 仅支持 Linux 和 macOS 系统，不支持 Windows。

该二进制文件为 nightly 构建版本，更新频率较高。如果您遇到崩溃或其他问题，请再次运行 `scripts/install.sh` 命令以更新到最新版本（每天最多更新一次）。

如果更新后问题仍然存在，请在 [GitHub](https://github.com/lightpanda-io/browser/issues) 上提交问题，请提供以下信息：
- 崩溃日志或错误信息，以及异常行为的描述（例如数据缺失或错误）
- 用于重现问题的 Playwright/Puppeteer 脚本
- 目标 URL 以及预期结果与实际结果之间的差异

## 启动浏览器服务器
```bash
$HOME/.local/bin/lightpanda serve --host 127.0.0.1 --port 9222
```

**可选参数：**
- `--log_level info|debug|warn|error` - 设置日志记录的详细程度
- `--log_format pretty|json` - 日志输出格式

## 使用方法

您可以通过 `ws://127.0.0.1:9222` 直接连接到 CDP WebSocket。您也可以通过 `http://127.0.0.1:9222/json/version` 获取 WebSocket 的 URL。

您可以直接将 Lightpanda 作为 Chrome 或 Openclaw 的默认浏览器使用，也可以发送 CDP 命令，或者结合使用 Playwright 或 Puppeteer 进行自动化操作。

**重要提示：**
- Lightpanda 可执行 JavaScript，因此适用于动态网站和单页应用（SPA）。但由于仍在开发中，可能会偶尔出现一些问题。
- 进行网页搜索时，请使用 DuckDuckGo 而不是 Google，因为 Google 会阻止 Lightpanda 的使用（由于浏览器指纹识别技术）。
- Lightpanda 每个进程仅支持一个 CDP 连接，每个连接只能创建一个上下文和一个页面，不支持多上下文同时使用。如果需要同时进行多次导航，请使用不同的端口号启动新的进程。Lightpanda 启动和关闭非常快速，因此使用多个进程比在 Chrome 中打开多个标签页更高效。
- 每次连接 CDP 时，浏览器会重置所有上下文和页面状态。因此，请在整个浏览会话期间保持 WebSocket 连接处于打开状态。您可以重复使用同一个进程进行后续连接，但每次连接都会从初始状态开始。
- 连接成功后，系统会自动创建一个新的上下文和页面；连接结束时，请同时关闭这两个连接。

## 与 playwright-core 的配合使用**

使用 `playwright-core`（而非完整的 `playwright` 包）连接到 Lightpanda：
```javascript
const { chromium } = require('playwright-core');

(async () => {
  // Connect to Lightpanda via CDP
  const browser = await chromium.connectOverCDP({
    endpointURL: 'ws://127.0.0.1:9222',
  });

  const context = await browser.newContext({});
  const page = await context.newPage();

  // Navigate and extract data
  await page.goto('https://example.com');
  const title = await page.title();
  const content = await page.textContent('body');

  console.log(JSON.stringify({ title, content }));

  await page.close();
  await context.close();
  await browser.close();
})();
```

## 与 puppeteer-core 的配合使用**

使用 `puppeteer-core`（而非完整的 `puppeteer` 包）连接到 Lightpanda：
```javascript
const puppeteer = require('puppeteer-core');

(async () => {
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://127.0.0.1:9222'
  });

  const context = await browser.createBrowserContext();
  const page = await context.newPage();

  await page.goto('https://example.com', { waitUntil: 'networkidle0' });
  const title = await page.title();

  console.log(JSON.stringify({ title }));

  await page.close();
  await context.close();
  await browser.close();
})();
```

## 相关脚本**
- `scripts/install.sh` - 用于安装 Lightpanda 二进制文件