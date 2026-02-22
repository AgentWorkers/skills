---
name: captcha-relay
description: "**带有人工干预的CAPTCHA解决方案，提供两种模式：**  
1. **截图模式（默认模式，无需任何基础设施）**：该模式会在页面上添加一个网格覆盖层，然后将页面截图发送给用户。用户根据提示进行操作后，系统会根据用户的响应来模拟点击行为。  
2. **令牌中继模式（需要网络连接）**：该模式会检测CAPTCHA的类型和站点密钥（sitekey），并在一个专门的中继页面上显示真实的CAPTCHA界面供用户直接操作。用户完成操作后，系统会通过CDP（Content Delivery Protocol）将生成的令牌发送给服务器。  
这两种模式均支持人工解决CAPTCHA任务，其中截图模式无需额外的网络基础设施，适合资源有限的环境；令牌中继模式则提供了更强大的交互体验，但需要网络连接。"
defaultMode: screenshot
---
# CAPTCHA 中继器 v2

该工具通过将 CAPTCHA 任务转发给人类用户来解决 CAPTCHA 验证问题，提供两种使用模式。

## 使用模式

### 截图模式（默认模式）——无需额外基础设施

1. 在网页上生成 CAPTCHA 的截图。
2. 通过 Telegram 将截图发送给人类用户。
3. 用户需要输入截图中各个单元格的编号。
4. 工具会根据用户提供的编号自动点击对应的单元格。

- **完全无需额外设置**：无需使用 Tailscale、隧道服务或中继服务器。
- **适用于所有类型的 CAPTCHA**（包括 reCAPTCHA、hCaptcha、滑块式验证码、文本验证码等）。
- 使用 `sharp` 库进行图像处理，以及 `cdp` 库来发送截图和执行点击操作。

```bash
node index.js                       # screenshot mode (default)
node index.js --mode screenshot     # explicit
node index.js --screenshot          # legacy alias
```

### 令牌中继模式——需要网络连接

1. 该模式会自动检测 CAPTCHA 的类型和站点密钥（sitekey）。
2. 在中继页面上显示真实的 CAPTCHA 界面。
3. 人类用户直接在页面上完成验证码的输入。
4. 通过 `cdp` 库将生成的令牌发送给工具。

- **需要 Tailscale** 或类似 `localtunnel`/`cloudflared` 的隧道服务，以便用户设备能够连接到中继服务器。
- 该模式适用于 reCAPTCHA v2、hCaptcha 和 Turnstile 等类型的验证码。
- **建议在已安装 Tailscale 的环境中使用**。

```bash
node index.js --mode relay              # with localtunnel
node index.js --mode relay --no-tunnel  # with Tailscale/LAN
```

## 各模式的适用场景

| 使用场景 | 适用模式 |
|----------|------|
| 快速且无需设置 | **截图模式** |
| 所有类型的 CAPTCHA（包括滑块式、文本验证码等） | **截图模式** |
| 已知验证码类型（reCAPTCHA、hCaptcha、Turnstile） | **令牌中继模式** |
| 已配置 Tailscale 的环境 | **令牌中继模式** |
| 无法访问目标网站的网络环境 | **截图模式** |

## 命令行参数（CLI）

| 参数 | 默认值 | 说明 |
|------|---------|-------------|
| `--mode screenshot` | `relay` | 选择解决模式（截图模式/令牌中继模式） |
| `--screenshot` | — | `--mode screenshot` 的别名 |
| `--no-inject` | `true` | 不执行点击操作，仅返回令牌 |
| `--no-tunnel` | `false` | 不使用隧道服务，使用本地 IP 或 Tailscale 的 IP 地址 |
| `--timeout N` | `120` | 超时时间（秒） |
| `--cdp-port N` | `18800` | Chrome 开发工具协议端口 |

## 工作流程

### 截图模式（最简单的方式）

1. 调用 `solveCaptchaScreenshot({ cdpPort })` 函数。
2. 通过 `message` 工具将截图文件（`capture.imagePath`）和提示信息（`capture.prompt`）发送给人类用户。
3. 用户输入单元格编号（例如 “1,3,5,7”）。
4. 调用 `injectGridClicks(cdpPort, capture, selectedCells)` 函数来点击指定的单元格。

### 令牌中继模式

1. 调用 `solveCaptcha({ useTunnel: false })`（适用于 Tailscale 环境）或 `solveCaptcha()`（适用于使用隧道服务的情况）。
2. 通过 `message` 工具将验证码的完整页面（`result.relayUrl`）发送给人类用户。
3. 等待用户完成验证码的输入。
4. 令牌会自动被注入到用户的浏览器中，之后自动化流程可以继续执行。

## 系统要求

- 需要安装 Chrome/Chromium 浏览器，并启用 `--remote-debugging-port=18800` 参数。
- 需要 Node.js 18 及更高版本，并通过 `npm install` 安装 `ws` 和 `sharp` 库。
- **仅限令牌中继模式**：需要 Tailscale 或隧道服务来连接目标网站。

---

（注：由于提供的代码块内容较为简短，部分功能的实现细节（如 `sharp` 和 `cdp` 库的具体使用方法）在翻译中未详细说明。在实际使用中，可能需要参考这些库的官方文档或相关教程。）