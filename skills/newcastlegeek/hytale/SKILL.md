# Hytale 服务器技能

使用官方下载工具和屏幕管理本地 Hytale 专用服务器。

## 必备条件
- Java 21 及更高版本（已安装）
- 屏幕设备（已安装）
- Hytale 下载工具（用户需自行提供）
- 认证信息（用户需将 `hytale-downloader-credentials.json` 文件放入 `~/hytale_server` 目录）

## 设置步骤

1. **下载 Hytale 下载工具：**
   - 从以下链接下载压缩包：`https://downloader.hytale.com/hytale-downloader.zip`
   - 解压压缩包，并将 `hytale-downloader-linux-amd64` 文件放入 `~/hytale_server/` 目录。
   - 使该文件可执行：`chmod +x ~/hytale_server/hytale-downloader-linux-amd64`

2. **添加认证信息：**
   - 将 `hytale-downloader-credentials.json` 文件放入 `~/hytale_server/` 目录。

## 命令说明

### `hytale start`
在独立的屏幕会话中启动服务器。
- **执行方式：** `/home/clawd/.npm-global/lib/node_modules/clawdbot/skills/hytale/hytale.sh start`

### `hytale stop`
优雅地停止服务器。
- **执行方式：** `/home/clawd/.npm-global/lib/node_modules/clawdbot/skills/hytale/hytale.sh stop`

### `hytale update`
使用 Hytale 下载工具下载或更新服务器文件。
- **执行方式：** `/home/clawd/.npm-global/lib/node_modules/clawdbot/skills/hytale/hytale.sh update`

### `hytale status`
检查服务器进程是否正在运行。
- **执行方式：** `/home/clawd/.npm-global/lib/node_modules/clawdbot/skills/hytale/hytale.sh status`