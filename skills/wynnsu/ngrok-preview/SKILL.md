---
name: ngrok-preview
description: 这是一个高实用性的 ngrok 预览工具，专为 AI 代理设计，用于通过临时公共 URL 共享本地生成的文件（如 HTML 文件、图片、Web 应用程序）。当 OpenClaw 在本地运行，但用户需要通过移动设备（如 Telegram 或移动浏览器）访问这些资源时（而本地主机链接无法直接访问），该工具就能派上用场。
---
# 🌐 Ngrok 预览技能

这是一个高实用性的技能，允许 AI 代理通过临时且安全的公共 URL 将本地生成的资源（如 HTML 文件、图片、Web 应用程序）分享给用户。

该技能旨在弥合本地开发环境与以移动设备为主的用户体验（如 Telegram 或移动浏览器）之间的差距——因为在这些环境中，`localhost` 链接是无法访问的。

## 🚀 为什么使用这个技能？

- **适合移动设备的工作流程**：在代理程序本地运行时，你可以在手机上预览代理生成的 Web 内容。
- **与 OpenClaw 的集成**：能够与 OpenClaw 本地网关无缝配合使用。代理程序可以返回一个可点击的 ngrok 链接，而无需使用本地文件路径或长文本格式。
- **零配置的共享流程**：通过一个脚本即可完成临时预览会话的创建和清理工作。

## 🛠 安装

通过 skills.sh 生态系统进行安装：

```bash
npx skills add https://github.com/wynnsu/skills-ngrok-preview --skill ngrok-preview
```

## ⚙️ 先决条件

- 本地已安装 `ngrok` 命令行工具。
- 使用你的账户令牌对 `ngrok` 进行身份验证：

```bash
ngrok config add-authtoken "$NGROK_AUTHTOKEN"
ngrok config check
```

## 📖 工作原理

当代理程序生成本地资源时，该技能可以执行以下操作：
1. 启动一个仅针对该资源目录的本地 HTTP 服务器。
2. 通过 ngrok 将该本地服务器的流量进行转发。
3. 通过 OpenClaw 将临时公共 URL 返回给用户。

## 默认的代理程序工作流程

创建预览会话：

```bash
python3 scripts/ngrok_preview.py up \
  --title "<task title>" \
  --session-id "<task-id>" \
  --ttl-minutes 120 \
  --source "<artifact-path-1>" \
  --source "<artifact-path-2>"
```

脚本会返回以下内容的 JSON 数据：
- `public_url`（公共 URL）
- `expires_at`（过期时间）
- `session_id`（会话 ID）
- `stop_command`（停止会话的命令）

完成预览后停止并清理会话：

```bash
python3 scripts/ngrok_preview.py down --session-id "<task-id>" --delete-session-dir
```

列出所有会话：

```bash
python3 scripts/ngrok_preview.py status
```

清理已过期的会话：

```bash
python3 scripts/ngrok_preview.py cleanup
```

## 技能结构

- `SKILL.md`：技能元数据及使用指南。
- `scripts/ngrok_preview.py`：负责隧道管理和会话处理的核心 Python 脚本。
- `references/troubleshooting.md`：针对 ngrok 身份验证问题、隧道超时以及会话失效等常见问题的解决方法。

## 🤝 兼容性

- **适配平台**：OpenClaw 网关
- **生态系统**：skills.sh 生态系统
- **支持平台**：Telegram 以及基于 Web 的代理程序用户界面

## 安全注意事项

- 仅发布与特定任务相关的输出内容（切勿发布工作区根目录等包含大量文件的目录）。
- 设置合理的过期时间，并确保所有链接都是临时访问的（而非永久性的托管链接）。
- 任务完成后务必停止或删除所有会话。

## 故障排除

如果预览创建失败，请参考：

- `references/troubleshooting.md`