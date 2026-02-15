---
name: Aluvia Browser Proxy
description: 使用 Aluvia SDK 启动一个受代理保护的无头浏览器会话。通过将浏览器流量路由到住宅代理（residential proxies），可以避免 403 错误、验证码（CAPTCHAs）以及速率限制（rate limits）。同时，系统会提供一个 CDP（Content Delivery Protocol）URL，以便与浏览器自动化工具（browser automation tools）进行集成。
read_when:
  - Browsing websites that block datacenter IPs
  - Avoiding CAPTCHAs and rate limits
  - Scraping or extracting data from protected websites
  - Running browser automation through residential proxies
  - Need a CDP URL for browser tools
metadata: { 'clawdbot': { 'emoji': '🛡️', 'requires': { 'bins': ['node', 'npx'] } } }
allowed-tools: Bash(aluvia-sdk:*)
---

# Aluvia 浏览器代理

## 功能简介

Aluvia SDK 会启动一个无头版的 Chromium 浏览器，并通过代理服务器进行路由，使得您的浏览器流量看起来像是由真实用户发起的。该代理服务会返回一个 CDP（Chrome 开发者工具协议，Chrome DevTools Protocol）URL，任何浏览器自动化工具都可以通过这个 URL 进行连接。

## 快速入门

```bash
export ALUVIA_API_KEY=your_api_key
aluvia-sdk open https://example.com        # Start proxied browser, get CDP URL
aluvia-sdk close                            # Stop the session
```

## 核心工作流程

1. 设置 `ALUVIA_API_KEY` 环境变量。
2. 使用 `aluvia-sdk open <url>` 命令启动一个无头代理浏览器，并返回包含 `cdpUrl` 的 JSON 数据。
3. 从 JSON 输出中解析出 `cdpUrl`，并将其传递给相应的浏览器自动化工具（如 agent-browser、OpenClaw 等）。
4. 使用 `aluvia-sdk close` 命令结束当前会话。

## 安装

```bash
npm install -g @aluvia/sdk
```

或者直接使用 `npx` 命令进行安装（无需额外安装）：

```bash
npx aluvia-sdk help
```

## API 密钥设置

1. 在 [Aluvia 控制台](https://www.aluvia.io/) 注册账号。
2. 在控制台中创建一个 API 密钥。
3. 设置 `ALUVIA_API_KEY` 环境变量。

```bash
export ALUVIA_API_KEY=your_api_key_here
```

`aluvia-sdk` 的命令行工具会从 `ALUVIA_API_KEY` 环境变量中读取 API 密钥。在运行任何命令之前，必须确保该变量已设置。

## 命令说明

### 启动浏览器会话

```bash
aluvia-sdk open <url>
```

**选项：**
- `--connection-id <id>`：使用现有的账户连接。
- `--headed`：以有界窗口模式启动浏览器（默认为无头模式）。

**示例：**

```bash
aluvia-sdk open https://example.com
```

**输出（JSON 格式）：**

```json
{
  "status": "ok",
  "url": "https://example.com",
  "cdpUrl": "http://127.0.0.1:45651",
  "connectionId": 3449,
  "pid": 113282
}
```

### 结束浏览器会话

```bash
aluvia-sdk close
```

**输出（JSON 格式）：**

```json
{
  "status": "ok",
  "message": "Browser session closed.",
  "url": "https://example.com",
  "cdpUrl": "http://127.0.0.1:45651",
  "connectionId": 3449,
  "pid": 113282
}
```

### 帮助文档

```bash
aluvia-sdk help
```

**输出（纯文本格式）：**

```
Usage: aluvia-sdk <command> [options]

Commands:
  open <url>    Start a browser session
  close         Stop the running browser session
  help          Show this help message

Options for 'open':
  --connection-id <id>   Use an existing account connection
  --headed               Show the browser window (default: headless)

Environment:
  ALUVIA_API_KEY         Your Aluvia API key (required)
```

## 命令返回格式

所有操作命令（`open`、`close`）都会在标准输出（stdout）中返回一条 JSON 数据：

| 字段            | 类型                | 说明                                      |
|-----------------|-----------------|-----------------------------------------|
| `status`       | `"ok"` \| "error"`     | 命令是否成功                          |
| `url`          | `string \| null`       | 浏览器打开的 URL                          |
| `cdpUrl`       | `string \| null`       | 用于连接外部工具的 CDP 端点                |
| `connectionId`    | `number \| null`       | Aluvia 账户连接 ID                          |
| `pid`          | `number \| null`       | 后台守护进程的进程 ID                          |
| `error`        | `string`          | 错误信息（仅在命令失败时显示）                    |
| `message`      | `string`          | 成功信息（仅在会话关闭时显示）                    |

**解析输出数据：**

```bash
CDP_URL=$(aluvia-sdk open https://example.com | jq -r '.cdpUrl')
```

同一时间只能运行一个浏览器会话。如果在会话正在进行中再次调用 `aluvia-sdk open`，系统会返回相应的错误信息。

## 通过 API 创建连接（推荐使用）

建议使用 API 创建一个可复用的连接，以避免每次调用 `open` 命令时都重新创建连接。这样做可以确保不同会话之间使用相同的代理配置和规则。

```bash
# Create a new connection
curl -s -X POST https://api.aluvia.io/v1/account/connections \
  -H "Authorization: Bearer $ALUVIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "openclaw agent"
  }'
```

**API 响应示例：**

```json
{
  "data": {
    "connection_id": "3449",
    "proxy_username": "...",
    "proxy_password": "..."
  }
}
```

之后，在启动浏览器会话时可以使用 `connection_id` 参数：

```bash
aluvia-sdk open https://target-site.com --connection-id 3449
```

**其他有用的 API 命令：**

```bash
# List existing connections
curl -s https://api.aluvia.io/v1/account/connections \
  -H "Authorization: Bearer $ALUVIA_API_KEY"

# Update connection
curl -s -X PATCH https://api.aluvia.io/v1/account/connections/3449 \
  -H "Authorization: Bearer $ALUVIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"description": "openclaw agent (updated)"}'

# Delete a connection
curl -s -X DELETE https://api.aluvia.io/v1/account/connections/3449 \
  -H "Authorization: Bearer $ALUVIA_API_KEY"
```

## 使用 agent-browser 工具与 CDP URL

首先启动 Aluvia 会话，然后将 CDP URL 传递给 agent-browser 工具：

```bash
# Start Aluvia proxy browser
CDP_URL=$(aluvia-sdk open https://example.com | jq -r '.cdpUrl')

# Connect agent-browser via CDP
agent-browser --cdp $CDP_URL snapshot -i
agent-browser --cdp $CDP_URL click @e1
agent-browser --cdp $CDP_URL fill @e2 "search query"

# When done
aluvia-sdk close
```

这样，agent-browser 的所有网络流量都会通过 Aluvia 的代理服务器进行路由，从而避开网络限制和验证码。

## 使用 OpenClaw 浏览器工具与 CDP URL

启动 Aluvia 会话后，配置 OpenClaw 使用该 CDP URL 作为远程配置文件：

```bash
# Start Aluvia proxy browser
CDP_URL=$(aluvia-sdk open https://example.com | jq -r '.cdpUrl')
```

在 `~/.openclaw/openclaw.json` 文件中添加以下配置：

```json
{
  "browser": {
    "profiles": {
      "aluvia": {
        "cdpUrl": "http://127.0.0.1:<port>",
        "color": "#6366F1"
      }
    }
  }
}
```

将 `<port>` 替换为 `cdpUrl` 中提供的端口号，然后使用该配置文件启动 OpenClaw：

```bash
openclaw browser --browser-profile aluvia snapshot
openclaw browser --browser-profile aluvia open https://example.com
```

这种方式与 [Browserless 托管的远程 CDP 服务](https://docs.openclaw.ai/tools/browser#browserless-hosted-remote-cdp) 的工作原理相同，但流量会通过 Aluvia 的代理服务器进行路由。

需要注意的是：所有浏览器会话的数据（页面内容、cookie、localStorage 等）都是共享的。

## 示例：完整工作流程

```bash
# 1. Set API key
export ALUVIA_API_KEY=your_api_key

# 2. Open a proxied browser session
RESULT=$(aluvia-sdk open https://example.com)
CDP_URL=$(echo $RESULT | jq -r '.cdpUrl')
echo "CDP URL: $CDP_URL"

# 3. Use with agent-browser or any CDP-compatible tool
agent-browser --cdp $CDP_URL snapshot -i
agent-browser --cdp $CDP_URL click @e1

# 4. Close when done
aluvia-sdk close
```

## 重用现有连接

```bash
# Open with a specific connection ID (reuses proxy allocation)
aluvia-sdk open https://example.com --connection-id 3449
```

## 以有界窗口模式调试

```bash
# Launch with a visible browser window
aluvia-sdk open https://example.com --headed
```

## 常见问题解决方法：

- **“需要设置 ALUVIA_API_KEY 环境变量”**：在运行命令前，请确保设置了 `export ALUVIA_API_KEY=your_key`。
- **“浏览器会话已运行中”**：请先使用 `aluvia-sdk close` 结束当前会话，然后再尝试。
- **“浏览器会话超时”**：可能是浏览器启动时间过长。请查看 `/tmp/aluvia-sdk/cli.log` 日志文件以获取详细信息。
- **“无法加载 Playwright”**：请先安装 Playwright：`npm install playwright`，然后使用 `npx playwright install chromium`。
- **“CDP 连接被拒绝”**：请确认当前会话仍在运行中。可以使用 `cat /tmp/aluvia-sdk/cli.lock` 检查日志。
- **找不到 `aluvia-sdk` 命令**：请尝试使用 `npx aluvia-sdk`，或全局安装 `npm install -g @aluvia/sdk`。

## 注意事项：

- 每台机器上同一时间只能运行一个浏览器会话。
- 浏览器以后台守护进程的形式运行，关闭终端不会终止会话。
- 请务必使用 `aluvia-sdk close` 命令来优雅地结束会话。
- CDP URL 是本地地址（`http://127.0.0.1:<port>`），仅在同一台机器上可访问。
- 会话状态（cookie、localStorage 等）会一直保留到会话结束。
- 可以通过 `--connection-id` 参数在不同会话之间重用相同的连接 ID，以保持代理配置的一致性。

## 相关链接：

- [Aluvia 官网](https://www.aluvia.io/)
- [Aluvia 文档](https://docs.aluvia.io/)
- [Aluvia SDK 在 npm 上的下载链接](https://www.npmjs.com/package/@aluvia/sdk)
- [OpenClaw 浏览器工具文档](https://docs.openclaw.ai/tools/browser#browserless-hosted-remote-cdp)