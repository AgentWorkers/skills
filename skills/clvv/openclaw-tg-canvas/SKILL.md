---
name: tg-canvas
description: "**Telegram Mini App Canvas**  
该工具用于在 Telegram Mini App 中渲染由代理生成的内容（HTML、Markdown 格式）。内容展示前需通过 `Telegram initData` 进行身份验证——只有获得授权的用户才能查看这些内容。内容推送可通过 `tg-canvas push` 命令或 `/push` API 完成。"
homepage: https://github.com/clvv/openclaw-tg-canvas
kind: server
metadata:
  {
    "openclaw": {
      "emoji": "🖼️",
      "kind": "server",
      "requires": {
        "bins": ["node", "cloudflared"],
        "env": ["BOT_TOKEN", "ALLOWED_USER_IDS", "JWT_SECRET", "MINIAPP_URL", "PUSH_TOKEN"]
      },
      "install": [
        {
          "id": "npm",
          "kind": "npm",
          "label": "Install dependencies (npm install)"
        }
      ]
    }
  }
---
**这是一个服务器技能。** 它包括一个 Node.js HTTP/WebSocket 服务器（`server.js`）、一个命令行工具（`bin/tg-canvas.js`）以及一个 Telegram Mini App 前端（`miniapp/`）。该技能不仅仅用于提供指令或说明。

**Telegram Mini App Canvas** 的功能是在 Telegram Mini App 中渲染由代理生成的 HTML 或 Markdown 内容，访问权限仅限于经过验证的用户 ID，并通过 Telegram 的 `initData` 验证机制进行控制。该系统提供了一个本地推送端点（`/push`）和一个命令行工具（`tg-canvas`），以便代理无需手动操作即可更新实时显示的内容。

## 先决条件

- Node.js 18 及更高版本（已在 Node 18、20、22 上测试通过）
- 需要使用 `cloudflared` 来建立 HTTPS 隧道（Telegram Mini App 的必备组件）
- 拥有 Telegram 机器人令牌（`BOT_TOKEN`）

## 设置步骤

1. 在 shell 或 `.env` 文件中配置环境变量（详见下面的 **配置** 部分）。
2. 运行机器人设置脚本以配置菜单按钮：
   ```bash
   BOT_TOKEN=... MINIAPP_URL=https://xxxx.trycloudflare.com node scripts/setup-bot.js
   ```
3. 启动服务器：
   ```bash
   node server.js
   ```
4. 启动 Cloudflare 隧道，以便通过 HTTPS 提供 Mini App 服务：
   ```bash
   cloudflared tunnel --url http://localhost:3721
   ```

## 从代理端推送内容

- **命令行工具：**  
  ```bash
  tg-canvas push --html "<h1>Hello</h1>"
  tg-canvas push --markdown "# Hello"
  tg-canvas push --a2ui @./a2ui.json
  ```
- **HTTP API：**  
  ```bash
  curl -X POST http://127.0.0.1:3721/push \
    -H 'Content-Type: application/json' \
    -d '{"html":"<h1>Hello</h1>"}'
  ```

## 安全性

**Cloudflare 隧道公开暴露的接口：**

| 接口 | 是否公开 | 认证方式 |
| --- | --- | --- |
| `GET /` | ✅ | 无（提供静态的 Mini App HTML） |
| `POST /auth` | ✅ | 需要 Telegram `initData` 的 HMAC-SHA256 验证以及 `ALLOWED_USER_IDS` 检查 |
| `GET /state` | ✅ | 需要 JWT 认证 |
| `GET /ws` | ✅ | 需要 JWT 认证（用于 WebSocket 连接） |
| `POST /push` | ❌ | 仅限内部网络（loopback） | 需要 `PUSH_TOKEN` 且必须通过内部网络验证 |
| `POST /clear` | ❌ | 仅限内部网络 | 需要 `PUSH_TOKEN` 且必须通过内部网络验证 |
| `GET /health` | ❌ | 仅限内部网络 | 仅用于检查服务器状态（读-only，风险较低） |
| `GET/WS /oc/*` | ✅ | 需要 JWT 认证（来自 `/auth`），随后通过 cookie 确保会话安全；服务器端会注入上游网关的认证信息 |

> ⚠️ **注意：** `cloudflared` 隧道会通过向 `localhost` 发送 TCP 请求来转发外部请求，这意味着所有通过该隧道传入的请求在 socket 层面上看起来都像是来自 `127.0.0.1` 的。因此，**必须设置并使用 `PUSH_TOKEN`**。尽管设置了内部网络验证机制，但这并非唯一的保护措施。

**建议：**
- **务必设置 `PUSH_TOKEN`**：服务器在缺少该令牌的情况下将无法启动。可以使用 `openssl rand -hex 32` 生成一个随机字符串。
- 使用一个强度较高的随机 `JWT_SECRET`（至少 32 字节）。
- 严格保密 `BOT_TOKEN`、`JWT_SECRET` 和 `PUSH_TOKEN`；如果这些密钥被泄露，应及时更换。
- 由于 Cloudflare 隧道会公开暴露 Mini App，因此 `/auth` 中的 `ALLOWED_USER_ids` 是控制访问权限的主要手段。

### 控制 WebSocket 的源地址白名单（必需）

当通过公共网络使用 `/oc/*` 时，需要将该地址添加到 OpenClaw 网关的配置中：
```json
{
  "gateway": {
    "controlUi": {
      "allowedOrigins": ["https://canvas.wdai.us"]
    }
  }
}
```

## 命令列表

- `tg-canvas push`：推送 HTML、Markdown、文本或 A2UI 内容
- `tg-canvas clear`：清除显示的内容
- `tg-canvas health`：检查服务器运行状态

## 配置参数

| 参数 | 是否必需 | 说明 |
| --- | --- | --- |
| `BOT_TOKEN` | 是 | 用于 API 调用和身份验证的 Telegram 机器人令牌 |
| `ALLOWED_USER_IDS` | 是 | 允许访问 Mini App 的 Telegram 用户 ID，用逗号分隔 |
| `JWT_SECRET` | 是 | 用于生成会话令牌的密钥。建议使用较长的随机值（至少 32 字节） |
| `PORT` | 否 | 服务器端口（默认：`3721`） |
| `MINIAPP_URL` | 是 | Mini App 的 HTTPS 地址（通过 Cloudflare 隧道或 Nginx 提供） |
| `PUSH_TOKEN` | 是 | 用于 `/push` 和 `clear` 操作的共享密钥。通过 `X-Push-Token` 头部发送。由于 `cloudflared` 会绕过基于 IP 的访问控制，因此这个密钥是必需的。可以使用 `openssl rand -hex 32` 生成 |
| `TG_CANVAS_URL` | 否 | CLI 的基础 URL（默认：`http://127.0.0.1:3721`） |
| `ENABLE_OPENCLAW_PROXY` | 否 | 是否启用对 OpenClaw 控制界面的代理（默认：`true`） |
| `OPENCLAW_PROXY_HOST` | 否 | 用于代理 OpenClaw 控制界面的上游服务器地址（默认：`127.0.0.1`） |
| `OPENCLAW_PROXY_PORT` | 否 | 用于代理 OpenClaw 控制界面的上游端口（默认：`18789`） |
| `OPENCLAW_GATEWAY_TOKEN` | 否 | 用于代理控制界面的可选令牌；如果未设置，服务器会从 `~/.openclaw/openclaw.json` 文件中读取令牌信息 |