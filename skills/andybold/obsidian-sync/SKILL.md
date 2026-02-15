---
name: obsidian-sync
description: 在 Clawdbot 工作空间与 Obsidian 之间同步文件。运行同步服务器，以实现与 OpenClaw Obsidian 插件的双向文件同步功能。
---

# Obsidian 同步服务器

这是一个用于在 Clawdbot 和 Obsidian 之间实现双向文件同步的安全服务器。

> **📦 该功能属于 [obsidian-openclaw](https://github.com/AndyBold/obsidian-openclaw)**  
> 这是一个 Obsidian 插件，允许您与 Clawdbot 代理进行聊天，并在您的笔记库（vault）与代理的工作空间之间同步笔记。

## 快速入门

```bash
SYNC_TOKEN="your-gateway-token" node scripts/sync-server.mjs
```

## 配置

| 环境变量 | 默认值 | 说明 |
|---------------------|---------|-------------|
| `SYNC_PORT` | `18790` | 服务器端口 |
| `SYNC_BIND` | `localhost` | 绑定地址 |
| `SYNC_WORKSPACE` | `/data/clawdbot` | 根工作空间路径 |
| `SYNC_TOKEN` | （必填） | 认证令牌（使用 Gateway 令牌） |
| `SYNC_ALLOWED_PATHS` | `notes,memory` | 允许的子目录（以逗号分隔） |

## 安全性

- 只有配置的子目录才能被访问 |
- 禁止路径遍历（如 `../`） |
- 所有请求都需要包含 `Authorization: Bearer <token>` 标头 |
- 通过 Tailscale 服务器提供远程访问功能 |

## API 端点

| 方法 | 端点 | 说明 |
|--------|----------|-------------|
| GET | `/sync/status` | 健康检查 |
| GET | `/sync/list?path=notes` | 列出 Markdown 文件 |
| GET | `/sync/read?path=notes/x.md` | 读取文件及其元数据 |
| POST | `/sync/write?path=notes/x.md` | 写入文件（会检测冲突） |

## 通过 Tailscale 提供远程访问

```bash
tailscale serve --bg --https=18790 http://localhost:18790
```

## 作为服务运行

### 使用 systemd 服务运行

```bash
mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/openclaw-sync.service << 'EOF'
[Unit]
Description=OpenClaw Sync Server
After=network.target

[Service]
Type=simple
Environment=SYNC_TOKEN=your-token-here
Environment=SYNC_WORKSPACE=/data/clawdbot
Environment=SYNC_ALLOWED_PATHS=notes,memory
ExecStart=/usr/bin/node /path/to/skills/obsidian-sync/scripts/sync-server.mjs
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now openclaw-sync
loginctl enable-linger $USER  # Start on boot
```

## Obsidian 插件

该功能为 **OpenClaw Obsidian 插件** 提供后端支持：

**[github.com/AndyBold/obsidian-openclaw](https://github.com/AndyBold/obsidian-openclaw)**

该插件提供以下功能：
- 💬 **聊天侧边栏** — 从 Obsidian 与 Clawdbot 代理进行交流 |
- 📁 **文件操作** — 通过聊天界面创建、编辑和删除笔记 |
- 🔄 **双向同步** — 保持笔记库与代理工作空间之间的同步 |
- 🔒 **安全存储** — 集成操作系统密钥链来存储令牌 |
- 📋 **审计日志** — 记录所有文件操作

请通过 [BRAT](https://github.com/TfTHacker/obsidian42-brat) 安装该插件，使用命令：`AndyBold/obsidian-openclaw`