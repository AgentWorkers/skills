---
name: claw2claw-filetransfer
description: 通过 SSH 使用 rsync 在 OpenClaw 代理之间实现跨平台文件传输。从 “Claws for Claws” 功能来看，这一过程非常简单，无需繁琐的操作。当用户需要在不同机器上的代理之间同步、备份或传输文件时，可以使用该功能。
homepage: https://github.com/claw2claw/filetransfer
metadata:
  clawdbot:
    emoji: "📦"
    requires:
      bins:
        - rsync
        - ssh
    install:
      - id: rsync
        kind: apt
        packages:
          - rsync
          - openssh-client
        label: Install rsync + SSH
---
# claw2claw-filetransfer

**文件传输如此简单，就连龙虾都能搞定。** 🦞

无需繁琐操作，即可在 OpenClaw 代理之间发送文件。支持通过 SSH 使用 rsync 进行文件传输：采用差异传输（delta transfers）技术、支持压缩，并提供进度条显示。无论您使用的是 Linux、macOS 还是 Windows，我们都能满足您的需求。

---

## 何时使用此技能

当您需要执行以下操作时，请使用此技能：
- 在两个 OpenClaw 代理之间传输文件
- 双向同步项目目录
- 将文件备份到远程代理
- 从远程代理拉取日志或数据
- 在代理之间建立 SSH 连接
- 顺利地完成文件传输（无需遇到任何问题）

---

## 快速入门

```bash
# 1. Set up remote agent (one-time)
claw2claw setup 192.168.1.100 --user root

# 2. Send files like a pro
claw2claw send /backup.tar.gz

# 3. Get files back
claw2claw get /remote/logs.txt

# 4. Sync entire directories
claw2claw sync-to-remote ./my-project/
```

---

## 命令

| 命令 | 描述 |
|---------|-------------|
| `setup <host>` | 配置远程代理 |
| `send <file>` | 将文件上传到远程代理 |
| `get <file>` | 从远程代理下载文件 |
| `sync-to-remote <dir>` | 将目录推送到远程代理 |
| `sync-from-remote <dir>` | 从远程代理拉取目录 |
| `ls <path>` | 列出远程文件 |
| `status` | 显示连接状态 |

---

## 选项

| 选项 | 描述 |
|--------|-------------|
| `-n, --dry-run` | 进行预览（不执行实际操作） |
| `--compress` | 启用压缩（默认值） |
| `--no-compress` | 禁用压缩 |
| `--debug` | 启用调试输出 |

---

## 环境变量

```bash
REMOTE_HOST="192.168.1.100"   # Remote IP/hostname
REMOTE_USER="root"            # SSH user
REMOTE_PORT="22"              # SSH port
SSH_KEY="/path/to/key"        # Custom SSH key
RSYNC_BWLIMIT=1000           # KB/s limit
```

---

## 为什么选择这个技能？

### 主要特点
- **差异传输**：仅传输已更改的文件部分
- **压缩功能**：传输过程中会自动压缩文件
- **进度条显示**：实时显示传输进度
- **双向支持**：支持文件推送和拉取
- **跨平台兼容**：适用于 Linux、macOS 和 Windows
- **基于密钥的身份验证**：无需使用密码

### 使用场景
- 将服务器数据备份到本地
- 在代理之间同步代码
- 拉取日志以供分析
- 部署静态网站
- 共享数据集

---

## 安装说明

### Linux
```bash
# Pre-installed on most distros
sudo apt install rsync
```

### macOS
```bash
brew install rsync
```

### Windows
```bash
# Option A: Git Bash (recommended)
# Download from https://git-scm.com

# Option B: cwrsync
# Download from https://www.itefix.net/cwrsync

# Option C: WSL
wsl --install
```

---

## 平台特定说明

### Git Bash / MSYS2
- 使用 Unix 风格的路径：`/c/Users/...`
- rsync 通常已预装，可直接使用

### Windows 命令提示符 / PowerShell
- 使用完整路径或正斜杠：`C:/Users/...`
- 或者使用 `cwrsync` 替代 rsync

### WSL（Windows Subsystem for Linux）
- 被系统识别为 Linux 环境，可正常使用
- 支持与 Windows 文件系统交互

### Cygwin
- 通过 Cygwin 安装该工具
- 文件路径示例：`/cygdrive/c/Users/...`

---

## 性能优化建议

### 压缩设置
```bash
# On (default) - for text files
claw2claw send /logs/*.log

# Off - for already compressed files
claw2claw send /backup.tar.gz --no-compress
```

### 带宽优化
```bash
# Limit to 500 KB/s
RSYNC_BWLIMIT=500 claw2claw send /huge-file.tar.gz
```

### 大文件处理
```bash
# rsync auto-resumes interrupted transfers
# Just run same command again
claw2claw send /huge-file.tar.gz
```

### 选择性同步
```bash
# Only sync specific patterns
# Use --include and --exclude in rsync manually
# Or sync specific subdirectories
claw2claw sync-to-remote ./src/
```

---

## 测试连接

### 快速测试
```bash
claw2claw status
```

### 手动测试 SSH 连接
```bash
ssh -o ConnectTimeout=5 user@host "echo OK"
```

### 测试文件传输功能
```bash
# Small test file first
echo "test" > /tmp/test.txt
claw2claw send /tmp/test.txt /tmp/
claw2claw get /tmp/test.txt /tmp/
rm /tmp/test.txt
```

---

## 故障排除

### 错误提示及解决方法
- “rsync: command not found”：请检查 rsync 是否已正确安装
- “Permission denied”：检查文件权限是否正确
- “Connection timed out”：检查网络连接是否稳定

---

## 使用示例

- **每日备份**：自动将服务器数据备份到本地
- **项目同步**：在多个代理之间同步项目文件
- **日志收集**：定期从远程代理拉取日志文件

---

## 安全性

- 仅支持基于 SSH 密钥的身份验证
- 密钥存储路径：`~/.ssh/`（权限设置为 700）
- 配置文件：`~/.claw2claw.conf`（权限设置为 600）
- 脚本中禁止使用密码

---

## 相关技能

- `blogwatcher`：用于在代理之间同步 RSS 源
- `github`：在代码提交后自动同步代码仓库
- `playwright-scraper-skill`：用于传输抓取的数据
- 任何需要文件共享的功能

---

## 卸载方法

```bash
rm /usr/local/bin/claw2claw
rm ~/.claw2claw.conf
rm -rf ~/.claw2claw/
```

---

**由 🦞🦞 创作**
*专为简化文件传输而设计。*

---

（注：由于Markdown格式的限制，部分代码块（如 ````bash
# 1. Set up remote agent (one-time)
claw2claw setup 192.168.1.100 --user root

# 2. Send files like a pro
claw2claw send /backup.tar.gz

# 3. Get files back
claw2claw get /remote/logs.txt

# 4. Sync entire directories
claw2claw sync-to-remote ./my-project/
````）在翻译后可能无法保留其原有的结构和格式。在实际应用中，这些代码块通常会被替换为具体的命令或配置信息。）