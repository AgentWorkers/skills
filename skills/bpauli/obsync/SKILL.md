---
name: obsync
description: Obsidian Sync CLI：用于在无头（headless）Linux服务器上同步数据箱（vaults），支持端到端的全加密功能。
homepage: https://github.com/bpauli/obsync
metadata: {"clawdbot":{"emoji":"🔄","os":["darwin","linux"],"requires":{"bins":["obsync"]},"install":[{"id":"homebrew","kind":"brew","formula":"bpauli/tap/obsync","bins":["obsync"],"label":"Homebrew (recommended)"},{"id":"source","kind":"source","url":"https://github.com/bpauli/obsync","bins":["obsync"],"label":"Build from source (Go 1.25+)"}]}}
---
# obsync

使用 `obsync` 在无界面的 Linux 服务器上同步 Obsidian 文档库。需要订阅 Obsidian Sync 服务并提供相应的账户凭据。

**设置（仅一次）：**
- `obsync login`（输入电子邮件、密码以及可选的多因素认证代码）
- 对于无界面服务器：`export OBSYNC_KEYRING_BACKEND=file`
- 可选：设置密钥环密码：`export OBSYNC_KEYRING_PASSWORD=mysecret`
- 验证设置：`obsync list`

**输出格式：**
- 默认格式：友好的终端输出，包含颜色和进度条显示。
- 使用 `--json` 或 `-j` 选项可获取 JSON 格式输出。
- 使用 `--verbose` 或 `-v` 选项可开启详细日志记录。

**常用命令：**
- 登录：`obsync login`
- 列出所有文档库：`obsync list`
- 下载文档库内容到本地：`obsync pull "My Notes" ~/notes -p "e2e-password"`
- 下载文档库内容并保存密码：`obsync pull "My Notes" ~/notes -p "e2e-password" -s`
- 推送本地更改到远程服务器：`obsync push "My Notes" ~/notes -p "e2e-password"`
- 持续监控同步状态：`obsync watch "My Notes" ~/notes -p "e2e-password"`
- 安装 systemd 服务：`obsync install "My Notes" ~/notes`
- 检查服务状态：`obsync status "My Notes"`
- 查看服务日志：`journalctl --user -u obsync@<vault-id>.service -f`
- 卸载服务：`obsync uninstall "My Notes"`

**参数说明：**
- `-p, --password` — 用于 E2E 加密的密码
- `-s, --save-password` — 将密码保存到密钥环中以供后续使用
- `-v, --verbose` — 启用详细日志记录
- `-j, --json` — 将输出格式设置为 JSON
- `--config` — 配置文件路径（或使用环境变量 `OBSYNC_CONFIG`）
- `--version` — 显示版本信息后退出程序

**注意事项：**
- 需要有效的 Obsidian Sync 订阅。
- 使用 AES-256-GCM 加密算法进行端到端（E2E）加密，密钥派生采用 scrypt 算法。
- 下载/上传文件时通过 SHA-256 哈希值进行比对，仅传输已更改的文件。
- 监控模式通过 WebSocket 监测远程变化，通过 `fsnotify` 监测本地变化（延迟 500 毫秒）。
- 大文件采用分块传输（每块 2MB）。
- 连接丢失时自动重连，重连间隔为 1 秒至 60 秒。
- `.obsidian/` 目录（包含主题、插件和设置文件）会被同步。
- 对于没有桌面密钥环的无界面服务器，请使用 `OBSYNC_KEYRING_BACKEND=file`。
- 若要让无界面服务器始终保持同步状态，请使用 `loginctl enable-linger $USER` 命令。
- 配置文件存储在 `~/.config/obsync/config.json` 中。