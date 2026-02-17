---
name: tg-canvas
description: "**Telegram Mini App Canvas**  
该工具用于在 Telegram Mini App 中渲染由代理生成的内容（HTML、Markdown 格式）。内容展示前需通过 `Telegram initData` 进行身份验证——只有获得授权的用户才能查看这些内容。内容推送方式有两种：使用 `tg-canvas push` 命令或通过 `/push` API。"
homepage: https://github.com/clvv/openclaw-tg-canvas
kind: server
metadata:
  {
    "openclaw": {
      "emoji": "🖼️",
      "kind": "server",
      "requires": {
        "bins": ["node", "cloudflared"],
        "env": ["BOT_TOKEN", "ALLOWED_USER_IDS", "JWT_SECRET", "MINIAPP_URL"]
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
**这是一个服务器端功能。** 它包括一个基于 Node.js 的 HTTP/WebSocket 服务器（`server.js`）、一个命令行工具（`bin/tg-canvas.js`）以及一个 Telegram 迷你应用前端（`miniapp/`）。该功能不仅仅用于提供指令或信息展示。

**Telegram 迷你应用 Canvas** 可以在 Telegram 迷你应用中渲染由代理生成的 HTML 或 Markdown 内容，且访问权限仅限于经过验证的用户 ID（通过 Telegram 的 `initData` 验证机制）。该功能还提供了一个本地推送端点（`/push`）和一个命令行工具（`bin/tg-canvas.js`），以便代理无需手动操作即可更新实时显示的内容。

## 先决条件

- Node.js 18 及以上版本（已测试过 Node 18、20 和 22）
- 需要使用 `cloudflared` 来建立 HTTPS 隧道（Telegram 迷你应用必须依赖此服务）
- 拥有 Telegram 机器人令牌（`BOT_TOKEN`）

## 设置流程

1. 在 shell 中或 `.env` 文件中配置环境变量（详见下面的 **配置** 部分）。
2. 运行机器人设置脚本以配置菜单按钮：
   ```bash
   BOT_TOKEN=... MINIAPP_URL=https://xxxx.trycloudflare.com node scripts/setup-bot.js
   ```
3. 启动服务器：
   ```bash
   node server.js
   ```
4. 启动 Cloudflare 隧道以通过 HTTPS 提供迷你应用的访问：
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

**Cloudflare 隧道公开提供的接口：**

| 接口 | 是否公开 | 访问权限要求 |
| --- | --- | --- |
| `GET /` | ✅ | 仅提供静态的迷你应用 HTML 内容 |
| `POST /auth` | ✅ | 需要通过 Telegram 的 `initData` 进行 HMAC-SHA256 验证，并检查 `ALLOWED_USER_IDS` |
| `GET /state` | ✅ | 必须提供 JWT 令牌 |
| `GET /ws` | ✅ | 需要 JWT 令牌（用于 WebSocket 连接的升级） |
| `POST /push` | ❌ | 仅限本地连接（`127.0.0.1` 或 `::1`）；可选 `PUSH_TOKEN` 参数 |
| `POST /clear` | ❌ | 仅限本地连接 | 与 `/POST /auth` 相同 |
| `GET /health` | ❌ | 仅限本地连接 | 与 `/POST /auth` 相同 |

对于 `/push`、`/clear` 和 `/health` 等接口，其访问控制是在 TCP 插件层（`req.socket.remoteAddress`）实现的，因此无法通过 `X-Forwarded-For` 等头部信息进行伪造。

**建议：**
- 即使 `/push` 接口已经限制为本地连接，也建议在 `.env` 文件中设置 `PUSH_TOKEN` 以增强安全性。
- 使用长度大于 32 字节的强随机 `JWT_SECRET` 作为加密密钥。
- 严格保密 `BOT_TOKEN` 和 `JWT_SECRET`；如果被泄露，请及时更换。
- 由于 Cloudflare 隧道会公开暴露迷你应用，因此 `/auth` 接口中的 `ALLOWED_USER_ids` 是控制访问权限的主要手段。

## 命令列表

- `tg-canvas push` — 推送 HTML、Markdown、文本或 A2UI 内容
- `tg-canvas clear` — 清除当前显示的内容
- `tg-canvas health` — 检查服务器运行状态

## 配置参数

| 参数 | 是否必填 | 说明 |
| --- | --- | --- |
| `BOT_TOKEN` | 是 | 用于 API 调用和身份验证的 Telegram 机器人令牌 |
| `ALLOWED_USER_IDS` | 是 | 允许访问迷你应用的 Telegram 用户 ID（以逗号分隔） |
| `JWT_SECRET` | 是 | 用于生成会话令牌的加密密钥（建议使用长度大于 32 字节的随机值） |
| `PORT` | 否 | 服务器端口（默认：`3721`） |
| `MINIAPP_URL` | 是 | 迷你应用的 HTTPS 地址（通过 Cloudflare 隧道或 Nginx 提供） |
| `PUSH_TOKEN` | 建议设置 | 用于 `/push` 接口和命令行工具的共享密钥，通过 `X-Push-Token` 头部发送 |
| `TG_CANVAS_URL` | 否 | 命令行工具的基地址（默认：`http://127.0.0.1:3721`） |