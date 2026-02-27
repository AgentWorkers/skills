---
name: tg-canvas
description: "**Telegram Mini App Canvas**  
该工具支持终端功能，并提供可选的控制界面代理服务。它能够将代理生成的内容（HTML、Markdown、A2UI格式）渲染到Telegram Mini App中，并通过 `tg-canvas push` 命令进行推送。工具内置了一个基于JWT认证的浏览器终端（服务器端PTY/bash接口，具有高权限，可访问服务器 shell）。通过设置 `ENABLE_OPENCLAW_PROXY=true`（默认值为 `false`），还可以代理 OpenClaw 的控制界面；此时工具不会读取任何本地文件。"
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
## 安全常见问题解答（针对技能审核者）

**问：** 服务器会自动加载 `~/.openclaw/openclaw.json` 或任何本地凭据文件吗？  
**答：** 不会。服务器不会读取任何本地文件来获取凭据。`OPENCLAW_GATEWAY_TOKEN` 必须通过环境变量明确提供。相关代码位于 `server.js` 文件中的 `ENABLE_OPENCLAW_PROXY` 配置块中，请自行验证。

**问：** `ENABLE_OPENCLAW_PROXY` 的默认值是什么？  
**答：** 关闭状态。代码为 `const ENABLE_OPENCLAW_PROXY = process.env.ENABLE_OPENCLAW_PROXY === "true";`，只有当环境变量中明确设置了 `"true"` 时，该功能才会被启用。如果省略该变量，则该功能将保持关闭状态。

**问：** 终端/PTY 端点是什么？它们是如何进行身份验证的？  
- 端点：`GET /ws/terminal`（用于 WebSocket 升级）  
- 身份验证：通过 `verifyJwt()` 函数验证 JWT；该 JWT 与通过 `POST /auth` 发送的令牌相同，且需要经过 Telegram 的 `initData` 和 HMAC-SHA256 验证；访问权限仅限于 `ALLOWED_USER_IDS` 中的用户。  
- 如果 JWT 缺失或无效，连接将在创建 PTY 之前被拒绝（返回 401 Unauthorized 错误）。  
- 当 WebSocket 连接关闭时，PTY 会立即终止。

---

**这是一个服务器技能。** 它包括一个 Node.js HTTP/WebSocket 服务器（`server.js`）、一个命令行工具（`bin/tg-canvas.js`）以及一个 Telegram Mini App 前端（`miniapp/`）。它不仅仅用于提供指令，还支持其他功能。

Telegram Mini App Canvas 可以在 Telegram Mini App 中渲染由代理生成的 HTML 或 Markdown 内容，访问权限仅限于经过验证的用户，并通过 Telegram 的 `initData` 验证进行控制。该技能还提供了一个本地推送端点和命令行接口，以便代理可以无需手动操作即可更新实时画布内容。

## 先决条件  
- Node.js 18 及以上版本（已测试过 Node 18/20/22）  
- 需要 `cloudflared` 来建立 HTTPS 隧道（Telegram Mini App 的必备组件）  
- 需要 Telegram 机器人令牌（`BOT_TOKEN`）

## 设置步骤  
1. 在 shell 或 `.env` 文件中配置环境变量（详见下方“配置”部分）。  
2. 运行机器人设置脚本以配置菜单按钮：  
   ```bash
   BOT_TOKEN=... MINIAPP_URL=https://xxxx.trycloudflare.com node scripts/setup-bot.js
   ```  
3. 启动服务器：  
   ```bash
   node server.js
   ```  
4. 启动 Cloudflare 隧道以通过 HTTPS 提供 Mini App 访问：  
   ```bash
   cloudflared tunnel --url http://localhost:3721
   ```

## 从代理端推送内容  
- 命令行接口：  
  ```bash
  tg-canvas push --html "<h1>Hello</h1>"
  tg-canvas push --markdown "# Hello"
  tg-canvas push --a2ui @./a2ui.json
  ```  
- HTTP API：  
  ```bash
  curl -X POST http://127.0.0.1:3721/push \
    -H 'Content-Type: application/json' \
    -d '{"html":"<h1>Hello</h1>"}'
  ```

## 安全性  
**Cloudflare 隧道公开暴露的接口：**  
| 端点 | 是否公开 | 是否需要身份验证 |  
| --- | --- | --- |  
| `GET /` | ✅ | 不需要（提供静态 Mini App HTML） |  
| `POST /auth` | ✅ | 需要 Telegram `initData` 和 HMAC-SHA256 验证 |  
| `GET /state` | ✅ | 需要 JWT |  
| `GET /ws` | ✅ | 需要 JWT（用于 WebSocket 升级） |  
| `POST /push` | 仅限内部网络（loopback） | 需要 `PUSH_TOKEN` |  
| `POST /clear` | 仅限内部网络 | 需要 `PUSH_TOKEN` |  
| `GET /health` | 仅限内部网络 | 仅用于内部网络检查（只读，风险较低） |  
| `GET/WS /oc/*` | ✅（启用时） | 需要 JWT；仅在 `ENABLE/OpenCLAW_PROXY=true` 时可用 |  

> ⚠️ **注意：** `cloudflared` 隧道会通过将外部请求转发到 `localhost` 来绕过内部网络检查。这意味着所有通过隧道发送的请求在套接字层面上看起来都来自 `127.0.0.1`，从而完全绕过了内部网络访问限制。因此，**必须设置并使用 `PUSH_TOKEN`**。尽管设置了内部网络检查，但这不应作为唯一的防护措施。  

**建议：**  
- **设置 `PUSH_TOKEN`**：服务器在缺少该令牌的情况下将拒绝启动。可以使用 `openssl rand -hex 32` 生成一个随机令牌。  
- 使用强随机生成的 `JWT_SECRET`（至少 32 字节）。  
- 保持 `BOT_TOKEN`、`JWT_SECRET` 和 `PUSH_TOKEN` 的安全性；如果这些信息被泄露，请及时更换。  
- Cloudflare 隧道会公开暴露 Mini App，因此 `/auth` 中的 `ALLOWED_USER_IDS` 是控制访问权限的主要手段。  
- **`ENABLE_OPENCLAW_PROXY` 默认是关闭的**。只有在需要通过 Mini App 访问控制界面时才启用该功能，并请了解其潜在影响（详见下文）。

### OpenClaw 控制界面代理（可选）  
服务器可以选择将 `/oc/*` 端点代理到本地的 OpenClaw 网关，从而允许通过 Mini App 访问 OpenClaw 控制界面。  

**此功能默认是关闭的。** 要启用该功能，请执行以下操作：  
```env
ENABLE_OPENCLAW_PROXY=true
```  

**启用后，服务器会：**  
- 将 `/oc/*` 的 HTTP 和 WebSocket 请求代理到本地的 OpenClaw 网关。  
- 如果设置了 `OPENCLAW_GATEWAY_TOKEN`，则会在代理请求中添加 `Authorization: Bearer` 作为认证头。  

服务器**不会** 读取任何本地文件来获取凭据；如果需要使用代理功能，`OPENCLAW_GATEWAY_TOKEN` 必须通过环境变量明确提供。  

当通过公共网络使用 `/oc/*` 时，请将相应的域名添加到 OpenClaw 网关的配置中：  
```json
{
  "gateway": {
    "controlUi": {
      "allowedOrigins": ["https://your-canvas-url.example.com"]
    }
  }
}
```

## 终端（高权限功能）  
Mini App 包含一个由服务器端支持的交互式终端。  

> ⚠️ **注意：** 这会授予运行服务器的机器 shell 访问权限。`ALLOWED_USERIDs` 中的用户可以打开 bash 会话并执行任意命令。请仅将受信任的用户添加到 `ALLOWED_USERIDs` 列表中。  

**工作原理：**  
- 经过验证的用户会在 Mini App 的顶部栏看到一个“终端”按钮。  
- 点击该按钮会打开一个连接到 `/ws/terminal` 的 xterm.js 窗口（需要 JWT 验证）。  
- 每个 WebSocket 连接都会创建一个 PTY（bash shell）；连接关闭时 PTY 也会终止。  
- 移动设备工具栏提供 Ctrl/Alt 快捷键、Esc 键、Tab 键和方向键。  

**运行时注意事项：** `node-pty` 以服务器进程用户的身份创建 bash 进程。没有其他环境变量可以控制这一点；身份验证是唯一的访问控制机制。

## 命令：  
- `tg-canvas push`：推送 HTML、Markdown、文本或 A2UI 内容  
- `tg-canvas clear`：清除画布内容  
- `tg-canvas health`：检查服务器状态

## 配置参数  
| 参数 | 是否必填 | 默认值 | 说明 |  
| --- | --- | --- | --- |  
| `BOT_TOKEN` | 是 | — | 用于 API 调用和 `initData` 验证的 Telegram 机器人令牌。 |  
| `ALLOWED_USER_IDS` | 是 | — | 允许访问画布、终端和代理功能的 Telegram 用户 ID（以逗号分隔）。 |  
| `JWT_SECRET` | 是 | — | 用于生成会话 JWT 的密钥（至少 32 字节）。 |  
| `PUSH_TOKEN` | 是 | — | 用于 `/push` 和 `clear` 操作的共享密钥。服务器在缺少该令牌的情况下将拒绝启动。可以使用 `openssl rand -hex 32` 生成。 |  
| `MINIAPP_URL` | 是（仅用于设置） | — | Mini App 的 HTTPS 地址，`scripts/setup-bot.js` 用此地址配置机器人菜单按钮。 |  
| `PORT` | 否 | `3721` | HTTP 服务器端口。 |  
| `TG_CANVAS_URL` | 否 | `http://127.0.0.1:3721` | `tg-canvas` 命令行工具使用的基地址。 |  
| `ENABLE_OPENCLAW_PROXY` | 否 | `false` | 设置为 `"true` 以启用 `/oc/*` 的代理功能。**默认关闭**。服务器不会读取任何本地文件来获取令牌；如果需要身份验证，请手动设置 `OPENCLAW_GATEWAY_TOKEN`。 |  
| `OPENCLAW_GATEWAY_TOKEN` | 否 | （未设置） | 代理请求时使用的认证令牌（格式为 `Authorization: Bearer`）。仅在 `ENABLE/OpenCLAW_PROXY=true` 时使用。必须手动提供；系统不会自动加载令牌。 |  
| `OPENCLAW_PROXY_HOST` | 否 | `127.0.0.1` | 本地 OpenClaw 网关的主机名（仅用于代理）。 |  
| `OPENCLAW_PROXY_PORT` | 否 | `18789` | 本地 OpenClaw 网关的端口（仅用于代理）。 |  
| `JWT_TTL_seconds` | 否 | 900 | 会话令牌的有效时间（默认 15 分钟）。 |  
| `INIT_DATA_MAX_AGE_SECONDS` | 否 | 300 | Telegram `initData` 的最大有效期（默认 5 分钟）。 |