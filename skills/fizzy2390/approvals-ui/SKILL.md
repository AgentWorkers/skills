# 审批用户界面（Approval UI）

这是一个用于管理 OpenClaw 设备配对、通道审批以及实时终端操作的 Web 仪表板——所有功能均可在浏览器中直接使用。

## 安装

将以下文件夹放置在：

```bash
~/.openclaw/workspace/projects/p1
```

文件结构应如下所示：

```bash
~/.openclaw/workspace/projects/p1/
├── SKILL.md
├── server.py
└── templates/
    ├── channel_approvals.html
    ├── dashboard.html
    ├── device_pairings.html
    ├── index.html
    ├── login.html
    └── terminal.html
```

## 所需依赖

安装 Python 相关依赖：

```bash
pip install flask flask-socketio
```

## ⚠️ 重要提示：运行前请更改这些配置

该工具附带了 **占位符配置**，在使用前必须进行修改：

打开 `server.py` 文件，并修改文件开头的以下配置项：

| 配置项 | 默认值 | 修改建议 |
|---------|---------|---------|
| 仪表板登录用户名 | `ADMIN_USERNAME` | 更改为你的实际用户名 |
| 仪表板登录密码 | `ADMIN_PASSWORD` | 更改为强密码 |
| API 认证密码 | `AUTH_PASSWORD` 或环境变量 `SERVER_AUTH_PASSWORD` | 更改为强密码 |
| Flask 密钥 | 环境变量 `FLASK_SECRET_KEY` | 使用随机字符串 |

**示例：**

```bash
export FLASK_SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))'"
export SERVER_AUTH_PASSWORD="your-strong-api-password-here"
```

> **请勿使用默认配置。** 如果有人知道默认值，他们将能够登录并访问你的终端及网关令牌。

### 认证机制说明

系统采用了 **双重认证机制**：

1. **仪表板登录**（`ADMIN_USERNAME` / `ADMIN_PASSWORD`）：用于保护仪表板页面（包括设备配对、通道审批和终端功能）。
2. **API 密码**（`AUTH_PASSWORD` 或环境变量 `SERVER_AUTH_PASSWORD`）：用于保护后端 API 端点（`/pair`、`/sync`、`/approve`），这些端点仅用于自动化脚本操作。这些端点在 Web 界面中不可见。

请确保为这两个认证字段设置强密码且具有唯一性。

## 使用方法

启动服务器：

```bash
cd ~/.openclaw/workspace/projects/p1
python3 server.py
```

然后在浏览器中访问 `http://127.0.0.1:9100`。

## 主要功能

- **仪表板**：提供快速导航至各个功能模块的入口页面。
- **设备配对**：查看待处理或已配对的设备连接状态，批准或拒绝配对请求，并将网关令牌复制到剪贴板。
- **通道审批**：审核并批准待处理的通道配对请求（支持 Telegram、Discord、WhatsApp 等平台）。通过 Socket.IO 实现实时更新。
- **终端**：在浏览器中通过 xterm.js 提供完整的交互式终端会话。

## 工作原理

- 从 `~/.openclaw/devices/pending.json` 和 `~/.openclaw/devices/paired.json` 文件中读取设备配对信息。
- 从 `~/.openclaw/credentials/*-pairing.json` 文件中读取通道配对请求。
- 从 `~/.openclaw/openclaw.json` 文件中的 `gateway.auth.token` 中获取网关令牌。
- 批准或拒绝配对请求的操作通过 `openclaw devices approve` 和 `openclaw devices reject` 命令来实现。
- 无需外部数据库——所有数据均来自 OpenClaw 自带的配置文件。

## 安全注意事项

- **仅限本地访问**：服务器默认绑定到 `127.0.0.1` 地址。除非你使用了带有 TLS 加密和强认证机制的反向代理，否则请勿将其改为 `0.0.0.0`。
- **终端访问权限**：终端功能允许用户获取对操作系统的完整 shell 权限。如无需此功能，可删除 `/terminal` 路由及对应的 `terminal.html` 模板文件。
- **敏感数据**：应用程序会读取用户的 `openclaw.json`（包含网关令牌）、设备配对信息及认证数据。任何能够访问 Web 界面的人都可以看到这些信息。
- **API 端点**：`POST /pair`、`POST /sync` 和 `POST /approve` 接受包含密码字段的 JSON 数据。这些接口受 `AUTH_PASSWORD` 保护，仅用于自动化脚本，不适用于 Web 界面。

## 配置选项

| 配置项 | 位置 | 默认值 |
|---------|---------|---------|
| 服务器端口 | `server.py` 文件底部 | `9100` |
| 仪表板登录信息 | `server.py` 中的 `ADMIN_USERNAME` 和 `ADMIN_PASSWORD` | `Drinnas` 和 `admin` |
| API 密码 | `server.py` 中的 `AUTH_PASSWORD` 或环境变量 `SERVER_AUTH_PASSWORD` | `Bb7766!server` |
| Flask 密钥 | 环境变量 `FLASK_SECRET_KEY` | 开发环境下的占位符值 | 请设置为一个随机字符串 |
| OpenClaw 数据目录 | 环境变量 `OPENCLAW_STATE_DIR` | `~/.openclaw` |

## 标签

`ui` `dashboard` `pairings` `approvals` `terminal` `web`