---
name: clawpod
description: 通过大量的住宅代理IP地址浏览和获取网页，支持完整的JavaScript渲染功能、地理定位、会话保持（sticky sessions）以及设备类型定位（device-type targeting）。
allowed-tools: Bash(agent-browser:*)
homepage: https://partners.joinmassive.com/create-account-clawpod
metadata: {"openclaw":{"emoji":"🦀","homepage":"https://partners.joinmassive.com/create-account-clawpod","requires":{"bins":["agent-browser"],"env":["MASSIVE_PROXY_USERNAME","MASSIVE_PROXY_PASSWORD"]},"primaryEnv":"MASSIVE_PROXY_USERNAME","install":[{"id":"node","kind":"node","package":"agent-browser","bins":["agent-browser"],"label":"Install agent-browser (npm)"}]}}
---

# ClawPod

通过 Massive 网络，使用住宅代理 IP 浏览和获取网页。该工具基于 [agent-browser](https://github.com/vercel-labs/agent-browser)（基于 Playwright/Chromium）实现，支持完整的 JavaScript 渲染、真实的浏览器指纹识别、截图以及页面交互功能——所有操作均通过 Massive 的住宅代理进行路由。

---

## 设置

### 1. 安装 agent-browser

```bash
npm install -g agent-browser
agent-browser install          # downloads bundled Chromium
```

在 Linux（包括 Docker）系统上，还需安装相关依赖项：

```bash
agent-browser install --with-deps
```

### 2. 添加 Massive 代理凭据

在 [Massive](https://partners.joinmassive.com/create-account-clawpod) 注册并获取代理凭据，然后将其设置为环境变量：

```bash
export MASSIVE_PROXY_USERNAME="your-username"
export MASSIVE_PROXY_PASSWORD="your-password"
```

---

## 核心工作流程

每个 ClawPod 任务都遵循以下步骤：

### 第一步：构建代理 URL

使用 Massive 凭据构建代理 URL。用户名必须进行 URL 编码（详见下面的 [代理 URL 格式](#proxy-url-format)。

```bash
# No geo-targeting (any residential IP)
PROXY_URL="https://${MASSIVE_PROXY_USERNAME}:${MASSIVE_PROXY_PASSWORD}@network.joinmassive.com:65535"
```

### 第二步：打开目标页面

```bash
agent-browser --proxy "$PROXY_URL" open "https://example.com"
```

此时会启动一个无头 Chromium 浏览器，通过 Massive 代理路由请求，导航到指定 URL，并等待页面加载完成（包括 JavaScript 的渲染）。

### 第三步：提取页面内容

```bash
# Get the full page text
agent-browser get text body

# Get an accessibility snapshot (best for structured data)
agent-browser snapshot -i

# Take a screenshot
agent-browser screenshot page.png

# Get page HTML
agent-browser get html
```

### 第四步：任务完成后关闭浏览器

```bash
agent-browser close
```

**重要提示：**`--proxy` 标志仅在浏览器守护进程启动时生效（即首次执行 `open` 命令时）。如果需要更改代理 URL（例如调整地理位置目标），必须先使用 `agent-browser close` 关闭当前会话，然后再使用新的代理 URL 重新启动浏览器。

---

## 代理 URL 格式

Massive 使用查询字符串语法在 **代理用户名** 中编码地理位置目标、会话粘性设置和设备类型参数：

```
raw username:   myuser?country=US&city=New York
```

对于使用 `--proxy` 的 URL，**用户名必须进行百分号编码**，因为 `?`、`=`、`&` 和空格在 URL 中是特殊字符：

```
encoded:        myuser%3Fcountry%3DUS%26city%3DNew%20York
```

完整的代理 URL 示例：

```
https://myuser%3Fcountry%3DUS%26city%3DNew%20York:mypassword@network.joinmassive.com:65535
```

### 编码规则

| 字符 | 编码方式 | 原因 |
|-----------|---------|-----|
| `?` | `%3F` | 用于分隔用户名和参数 |
| `=` | `%3D` | 用于分隔参数键和值 |
| `&` | `%26` | 用于分隔多个参数 |
| ` `（空格）` | `%20` | 用于城市名称等中的空格 |

### 在 bash 中构建代理 URL

```bash
# No geo-targeting
PROXY_URL="https://${MASSIVE_PROXY_USERNAME}:${MASSIVE_PROXY_PASSWORD}@network.joinmassive.com:65535"

# With geo-targeting — encode the username
ENCODED_USER=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${MASSIVE_PROXY_USERNAME}?country=US&city=New York', safe=''))")
PROXY_URL="https://${ENCODED_USER}:${MASSIVE_PROXY_PASSWORD}@network.joinmassive.com:65535"
```

或者手动进行编码：

```bash
ENCODED_USER="${MASSIVE_PROXY_USERNAME}%3Fcountry%3DUS%26city%3DNew%20York"
PROXY_URL="https://${ENCODED_USER}:${MASSIVE_PROXY_PASSWORD}@network.joinmassive.com:65535"
```

---

## 地理位置目标设置

可以在代理用户名中添加地理位置目标参数。所有参数均为可选：

| 参数 | 说明 | 示例值 |
|-----------|-------------|----------------|
| `country` | ISO 3166-1 国家代码 | `US`、`GB`、`DE`、`FR` |
| `city` | 城市名称（英文） | `New York`、`London`、`Berlin` |
| `subdivision` | 州或行政区代码 | `CA`、`TX`、`NY` |
| `zipcode` | 邮政编码 | `10001`、`90210` |

**规则：**
- 使用其他地理位置参数时必须指定 `country`。
- 使用 `country` 和 `city` 通常比仅使用 `zipcode` 更可靠。
- 如果同时指定了 `subdivision` 和 `zipcode`，则会忽略 `city`。
- 过于严格的限制可能导致请求失败——必要时可放宽参数设置。

### 示例

```bash
# Any IP in Germany
ENCODED_USER="${MASSIVE_PROXY_USERNAME}%3Fcountry%3DDE"

# IP in New York City
ENCODED_USER="${MASSIVE_PROXY_USERNAME}%3Fcountry%3DUS%26city%3DNew%20York%26subdivision%3DNY"

# IP in a specific US zipcode
ENCODED_USER="${MASSIVE_PROXY_USERNAME}%3Fcountry%3DUS%26zipcode%3D90210"

# IP in London
ENCODED_USER="${MASSIVE_PROXY_USERNAME}%3Fcountry%3DGB%26city%3DLondon"
```

示例代理 URL：`PROXY_URL="https://${ENCODED_USER}:${MASSIVE_PROXY_PASSWORD}@network.joinmassive.com:65535"`

---

## 会话粘性设置

确保多个请求通过 **相同的出口 IP` 发送。可以通过在代理用户名中添加会话参数来实现：

| 参数 | 说明 | 默认值 |
|-----------|-------------|---------|
| `session` | 会话 ID（最多 255 个字符） | *未设置* |
| `sessionttl` | 会话过期时间（分钟，1-240 分钟） | 15 |
| `sessionmode` | `strict` 或 `flex` | `strict` |

**模式：**
- **strict**（默认）：任何代理错误都会导致会话失效，并切换到新的 IP。
- **flex**：允许短暂错误存在——会话会持续到连续失败次数达到设定值。

**重要提示：** 会话的过期时间是固定的（创建时加上设定的 TTL 值），不会因后续请求而延长。更改地理位置参数会创建新的会话。

### 示例

```bash
# Sticky session with 30-minute TTL
ENCODED_USER="${MASSIVE_PROXY_USERNAME}%3Fsession%3Dmysession1%26sessionttl%3D30%26sessionmode%3Dflex"
PROXY_URL="https://${ENCODED_USER}:${MASSIVE_PROXY_PASSWORD}@network.joinmassive.com:65535"
agent-browser --proxy "$PROXY_URL" open "https://example.com"
```

**重要提示：**由于 `--proxy` 是在浏览器守护进程启动时设置的，因此会话粘性设置会一直保持有效，直到浏览器守护进程关闭。要切换会话，需要关闭当前会话并重新启动浏览器。

---

## 设备类型目标设置

通过添加 `type` 参数来指定请求的来源设备类型：

| 值 | 说明 |
|-------|-------------|
| `mobile` | 移动设备 IP |
| `common` | 桌面/笔记本电脑 IP |
| `tv` | 智能电视 IP |

### 示例

```bash
# Mobile IP in the US
ENCODED_USER="${MASSIVE_PROXY_USERNAME}%3Ftype%3Dmobile%26country%3DUS"
PROXY_URL="https://${ENCODED_USER}:${MASSIVE_PROXY_PASSWORD}@network.joinmassive.com:65535"
agent-browser --proxy "$PROXY_URL" open "https://example.com"
```

---

## 常用操作模式

### 获取页面内容并提取文本

```bash
PROXY_URL="https://${MASSIVE_PROXY_USERNAME}:${MASSIVE_PROXY_PASSWORD}@network.joinmassive.com:65535"
agent-browser --proxy "$PROXY_URL" open "https://example.com"
agent-browser get text body
agent-browser close
```

### 获取 JavaScript 渲染后的页面内容（单页面应用）

agent-browser 会自动渲染 JavaScript，无需额外设置：

```bash
agent-browser --proxy "$PROXY_URL" open "https://spa-site.com/dashboard"
agent-browser snapshot -i          # interactive elements after JS renders
agent-browser close
```

### 截取屏幕截图

```bash
agent-browser --proxy "$PROXY_URL" open "https://example.com"
agent-browser screenshot page.png
agent-browser close
```

### 截取整个页面的截图

```bash
agent-browser --proxy "$PROXY_URL" open "https://example.com"
agent-browser screenshot --full fullpage.png
agent-browser close
```

### 提取结构化数据（包含辅助技术信息）

```bash
agent-browser --proxy "$PROXY_URL" open "https://example.com"
agent-browser snapshot -i -c       # interactive + compact
agent-browser close
```

### 验证出口 IP 和地理位置设置

```bash
ENCODED_USER="${MASSIVE_PROXY_USERNAME}%3Fcountry%3DDE"
PROXY_URL="https://${ENCODED_USER}:${MASSIVE_PROXY_PASSWORD}@network.joinmassive.com:65535"
agent-browser --proxy "$PROXY_URL" open "https://httpbin.org/ip"
agent-browser get text body             # should show a German residential IP
agent-browser close
```

### 多页面会话（使用相同的出口 IP）

```bash
ENCODED_USER="${MASSIVE_PROXY_USERNAME}%3Fsession%3Dcrawl1%26sessionttl%3D60"
PROXY_URL="https://${ENCODED_USER}:${MASSIVE_PROXY_PASSWORD}@network.joinmassive.com:65535"
agent-browser --proxy "$PROXY_URL" open "https://example.com/page1"
agent-browser get text body
agent-browser open "https://example.com/page2"    # same proxy, same IP
agent-browser get text body
agent-browser close
```

---

## 重要注意事项

- **必须设置环境变量**：`MASSIVE_PROXY_USERNAME` 和 `MASSIVE_PROXY_PASSWORD`。
- **浏览器启动延迟**：首次执行 `open` 命令时，由于 Chromium 的启动过程，可能需要 3-8 秒。同一会话内的后续请求会更快。
- **`--proxy` 标志仅在浏览器守护进程启动时生效**。要更改代理设置，需先使用 `agent-browser close` 关闭当前会话，然后再重新启动。
- **URL 编码至关重要**：包含地理位置参数的代理用户名必须进行百分号编码。未编码的 `?`、`=`、`&` 或空格会导致 URL 错误。
- **自动 JavaScript 渲染**：与原始 HTTP 请求不同，agent-browser 会自动渲染 JavaScript、执行页面逻辑并处理重定向和 Cookie。
- **真实的浏览器指纹**：请求使用真实的 Chromium 浏览器指纹，使得请求更难以被识别为自动化操作。
- **一次仅使用一个浏览器实例**：agent-browser 守护进程管理一个浏览器实例。在不同代理配置之间切换时需要使用 `close` 命令。

---

## 参考链接

- [agent-browser](https://github.com/vercel-labs/agent-browser) — 用于 AI 代理的 Playwright/Chromium 命令行工具
- [Massive](https://joinmassive.com) — 住宅代理网络服务
- [Massive Portal](https://partners.joinmassive.com/create-account-clawpod) — 注册并管理代理凭据