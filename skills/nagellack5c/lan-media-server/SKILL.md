---
name: lan-media-server
description: 通过 HTTP 将 AI 工作区中的图片、截图和文件共享给局域网内的用户。当代理需要向用户展示图片、浏览器截图或任何文件，而当前通道（如 WebChat、CLI）不支持内联媒体时，可以使用此方法。该方法会在局域网内启动一个轻量级的 Node.js 静态文件服务器，并由 systemd 管理。只需将文件放入共享目录中，然后向用户发送一个可点击的 URL 即可。
---

# LAN媒体服务器

这是一个轻量级的HTTP文件服务器，用于在局域网内与用户共享代理生成的媒体文件（截图、图片、文档）。

## 为什么需要这个工具？

许多AI助手渠道（如Web聊天、命令行界面、SSH）无法直接显示图片。该工具通过在局域网内通过HTTP协议提供文件来解决这个问题——用户只需上传文件或发送链接即可查看。

## 快速入门

```bash
bash scripts/setup.sh
```

执行以上命令后，系统会创建共享目录、安装服务器脚本、创建systemd用户服务并启动该服务。

**默认配置：**
- 端口：`18801`
- 服务目录：`$HOME/projects/shared-media`
- 访问地址：`http://<LAN_IP>:18801/<filename>`

您可以使用环境变量来修改这些配置：

```bash
MEDIA_PORT=9090 MEDIA_ROOT=/tmp/media bash scripts/setup.sh
```

## 使用方法

当需要向用户展示图片或文件时，请按照以下步骤操作：
1. 将文件保存或复制到共享目录中。
2. 向用户发送链接：`http://<server-LAN-IP>:<port>/<filename>`

**浏览器截图示例：**
```bash
cp /path/to/screenshot.jpg ~/projects/shared-media/my-screenshot.jpg
# Then send: http://192.168.1.91:18801/my-screenshot.jpg
```

请使用描述性强的文件名，因为共享目录是扁平结构且对用户可见的。

## 管理

```bash
# Check status
systemctl --user status media-server

# Restart
systemctl --user restart media-server

# View logs
journalctl --user -u media-server -f

# Stop and disable
systemctl --user stop media-server
systemctl --user disable media-server
```

## 安全注意事项：
- 仅在本局域网内提供文件服务（虽然使用IP地址`0.0.0.0`，但实际上通常位于NAT网络后）。
- 无需身份验证——请勿在共享目录中存放敏感文件。
- 系统会阻止路径遍历攻击（文件必须位于`MEDIA_ROOT`目录下）。
- 无法查看目录列表——用户必须提供正确的文件名才能访问文件。