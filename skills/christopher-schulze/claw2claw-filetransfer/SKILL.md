---
name: claw2claw-filetransfer
description: >
  **通过 rsync 和 SSH 在 OpenClaw 代理之间实现跨平台文件传输**  
  从 “Claws for Claws” 功能来看，文件传输过程非常简单，无需繁琐的操作。当用户需要在不同机器上的 OpenClaw 代理之间同步、备份或传输文件时，可以使用这一功能。
---
# claw2claw-filetransfer

**文件传输如此简单，连龙虾都能搞定。** 🦞

无需繁琐操作，即可在OpenClaw代理之间发送文件。使用rsync通过SSH进行传输——支持增量传输、压缩功能，并提供进度条显示。支持Linux、macOS和Windows系统。

---

## 何时使用此技能

当用户需要执行以下操作时，请使用此技能：
- 在两个OpenClaw代理之间传输文件
- 双向同步项目目录
- 将文件备份到远程代理
- 从远程代理拉取日志或数据
- 在代理之间建立SSH连接
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
| `send <file>` | 上传文件到远程代理 |
| `get <file>` | 从远程代理下载文件 |
| `sync-to-remote <dir>` | 将目录推送到远程代理 |
| `sync-from-remote <dir>` | 从远程代理拉取目录 |
| `ls <path>` | 列出远程文件 |
| `status` | 显示连接状态 |

---

## 选项

| 选项 | 描述 |
|--------|-------------|
| `-n, --dry-run` | 不执行实际传输，仅进行预览 |
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

## 为什么选择此技能？

### 主要特点
- **增量传输**：仅传输更改过的文件字节
- **压缩功能**：传输过程中自动压缩文件
- **进度条**：实时显示传输进度
- **双向支持**：支持文件推送和拉取
- **跨平台兼容**：支持Linux、macOS和Windows
- **基于密钥的认证**：无需使用密码

### 使用场景
- 将服务器数据备份到本地
- 在代理之间同步代码
- 拉取日志数据进行分析
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
- 使用Unix风格的路径：`/c/Users/...`
- rsync通常已预装，可直接使用

### Windows命令提示符 / PowerShell
- 使用完整路径或正斜杠：`C:/Users/...`
- 或者使用`cwrsync`替代rsync

### WSL（Windows Subsystem for Linux）
- 被识别为Linux环境，可正常使用
- 支持与Windows文件系统的交互

### Cygwin
- 通过Cygwin安装
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

## 连接测试

### 快速测试
```bash
claw2claw status
```

### 手动SSH连接测试
```bash
ssh -o ConnectTimeout=5 user@host "echo OK"
```

### 文件传输测试
```bash
# Small test file first
echo "test" > /tmp/test.txt
claw2claw send /tmp/test.txt /tmp/
claw2claw get /tmp/test.txt /tmp/
rm /tmp/test.txt
```

---

## 故障排除

### “rsync: command not found”错误
```bash
# Linux
sudo apt install rsync

# macOS  
brew install rsync

# Windows
# Install Git Bash or cwrsync
```

### “Permission denied”错误
```bash
# Re-run setup to add SSH key
claw2claw setup <host> --user <user>
```

### “Connection timed out”错误
```bash
# Check host reachable
ping <host>

# Check port open
nc -zv <host> 22
```

---

## 使用示例

### 日常备份
```bash
claw2claw send /backups/daily-$(date +%Y%m%d).tar.gz /backups/
```

### 项目同步
```bash
# Morning
claw2claw sync-from-remote /workspace/project/

# Evening  
claw2claw sync-to-remote /workspace/project/
```

### 日志收集
```bash
claw2claw get /var/log/syslog ./logs/
```

---

## 安全性

- 仅支持基于SSH密钥的认证
- 密钥存储位置：`~/.ssh/`（权限设置为700）
- 配置文件：`~/.claw2claw.conf`（权限设置为600）
- 脚本中禁止使用密码

---

## 相关技能

- `blogwatcher`：用于在代理之间同步RSS源
- `github`：在提交代码后同步仓库
- `playwright-scraper-skill`：用于传输抓取的数据
- 任何需要文件共享的场景

---

## 卸载方法
```bash
rm /usr/local/bin/claw2claw
rm ~/.claw2claw.conf
rm -rf ~/.claw2claw/
```

---

**由Claws团队开发。** 🦞🦞
**让文件传输变得简单又高效。**