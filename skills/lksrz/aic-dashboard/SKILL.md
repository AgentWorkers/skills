---
name: aic-dashboard
description: AI Commander管理仪表板：这是一个轻量级的辅助Web用户界面，用于监控通过“email-webhook”技能接收的入站邮件，以及由“browser-auth”技能创建的浏览器会话状态。
metadata: {"openclaw": {"requires": {"bins": ["node"], "env": ["DASHBOARD_TOKEN"]}, "primaryEnv": "DASHBOARD_TOKEN", "install": [{"id": "npm-deps", "kind": "node", "package": "express@4.21.2", "label": "Install Dashboard dependencies"}]}}
---
# AI Commander 仪表板

这是一个为 AI Commander 代理设计的辅助仪表板。它显示由 [`email-webhook`](https://clawhub.ai/lksrz/email-webhook) 技能收集的传入邮件，并展示由 [`browser-auth`](https://clawhub.ai/lksrz/browser-auth) 技能创建的浏览器会话的状态。

该技能仅具有 **只读** 功能——它不会捕获凭证、控制浏览器或发送消息，仅负责读取本地数据文件并通过受令牌保护的 Web UI 提供这些数据。

## 相关技能

| 技能 | 功能 |
|---|---|
| [`email-webhook`](https://clawhub.ai/lksrz/email-webhook) | 接收传入邮件并将其写入 `inbox.jsonl` 文件 |
| [`browser-auth`](https://clawhub.ai/lksrz/browser-auth) | 运行远程浏览器隧道并将会话数据写入 `session.json` 文件 |

该仪表板会读取这两个文件并将它们显示在一个界面上。

## 该技能的功能

- 读取 `inbox.jsonl` 文件并显示最近 50 封传入邮件
- 读取 `session.json` 文件并显示是否存在活跃的浏览器会话
- 在可配置的本地端口上提供受令牌保护的 Web UI
- 每 5 秒自动刷新一次

## 环境变量

| 变量 | 是否必填 | 默认值 | 说明 |
|---|---|---|---|
| `DASHBOARD_TOKEN` | 是 | — | 访问仪表板的密钥令牌 |
| `PORT` | 否 | `19195` | 仪表板的端口 |
| `DASHBOARD_HOST` | 否 | `127.0.0.1` | 仪表板绑定的 IP 地址 |
| `INBOX_PATH` | 否 | `./data/inbox.jsonl` | 传入邮件的数据路径（来自 `email-webhook`） |
| `SESSION_PATH` | 否 | `./data/session.json` | 会话数据文件路径（来自 `browser-auth`） |

## 设置步骤

1. **安装依赖项**：
   ```bash
   npm install express@4.21.2
   ```
2. **启动**（无需任何配置）：
   ```bash
   node scripts/server.js
   ```
3. 查看生成的 URL——其中包含自动生成的令牌：
   ```
   🏠 AI COMMANDER DASHBOARD READY
   Access URL: http://YOUR_IP:19195/?token=a3f9c2...
   ```

设置完毕，无需额外配置。

## 可选的环境变量

仅在需要时覆盖默认值：

| 变量 | 默认值 | 说明 |
|---|---|---|
| `DASHBOARD_TOKEN` | （随机值） | 自定义令牌（替代自动生成的令牌） |
| `PORT` | `19195` | 服务器端口 |
| `DASHBOARD_HOST` | `0.0.0.0` | 绑定地址 |
| `INBOX_PATH` | `./data/inbox.jsonl` | 邮件数据路径（来自 `email-webhook`） |
| `SESSION_PATH` | `./data/session.json` | 会话数据路径（来自 `browser-auth`） |

## 安全性

- 如果未设置 `DASHBOARD_TOKEN`，每次启动时都会生成一个新的随机令牌
- 所有请求都需要提供令牌（通过 `?token=`、`X-Dashboard-Token` 标头或 `Authorization: Bearer`）
- UI 会将令牌存储在 `localStorage` 中，并在页面加载后从 URL 中移除该令牌