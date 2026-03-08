---
name: openclaw-remote-install
version: "1.0.0"
description: >
  通过 SSH 实现一键远程部署 OpenClaw。系统会自动检测操作系统，并选择最适合的部署方式（Docker、Podman 或 npm）。适用场景：  
  (1) 在 VPS 或云服务器上进行安装；  
  (2) 自动化多台机器的部署；  
  (3) 安装完成后配置模型、通道或网关。
---
# OpenClaw 远程安装技能

该技能支持通过 SSH 在远程服务器上远程安装和配置 OpenClaw，具备智能方法选择和异步执行功能。

## 日志目录

所有安装日志会自动保存到：
```
~/.openclaw/remote-install-logs/<host>_<timestamp>/
```

每次安装会生成以下文件：
- `install.log` - 带时间戳的主要安装日志
- `install_output.log` - 命令的原始输出结果
- `install.pid` - 后台进程的 PID（异步模式）
- `install.status` - 安装状态：运行中/成功/失败/超时

一个名为 `latest` 的符号链接会指向最新的日志目录。

## 支持的安装方法

| 方法 | 描述 | 适用场景 |
|--------|-------------|----------|
| `auto`（默认）| 根据操作系统自动选择最佳方法 | 大多数情况 |
| `installer` | 官方 `install.sh` 脚本 | 标准的 Linux/macOS 环境 |
| `cli` | `install-cli.sh`（本地执行） | 不依赖于系统中的 Node.js |
| `npm` | `npm install -g openclaw` | 已安装 Node.js 22+ 的环境 |
| `pnpm` | `pnpm add -g openclaw` | 使用 pnpm 的环境 |
| `docker` | Docker 容器 | 容器化部署 |
| `podman` | Podman 无根容器 | 无根环境 |

## 使用方法

### 快速启动（自动检测）

```bash
./scripts/install_openclaw_remote.sh <host> <user> <key_path>
```

### 异步安装（适用于耗时较长的安装过程）

```bash
# Run installation in background with progress monitoring
./scripts/install_openclaw_remote.sh <host> <user> <key_path> --async

# Monitor in real-time
tail -f ~/.openclaw/remote-install-logs/latest/install_output.log

# Check status
cat ~/.openclaw/remote-install-logs/latest/install_status
```

### 使用密码进行安装

```bash
./scripts/install_openclaw_remote.sh <host> <user> <password> --password-based
```

### 强制使用特定方法

```bash
# Docker installation
./scripts/install_openclaw_remote.sh <host> <user> <key_path> --docker

# Podman installation
./scripts/install_openclaw_remote.sh <host> <user> <key_path> --podman

# npm method (if Node 22+ available)
./scripts/install_openclaw_remote.sh <host> <user> <key_path> --method npm
```

### 非交互式安装（自动化）

```bash
./scripts/install_openclaw_remote.sh <host> <user> <key_path> \
  --non-interactive \
  --configure
```

### 自定义日志目录

```bash
./scripts/install_openclaw_remote.sh <host> <user> <key_path> \
  --log-dir /path/to/custom/logs
```

## 自动检测逻辑

安装器会自动选择最佳安装方法：
1. 如果指定了 `--docker` 或 `--podman` 标志，则使用容器安装方法（如果可用）。
2. 如果已安装 Node.js 22+，则使用 `pnpm` 或 `npm` 方法。
3. 否则，使用官方的 `install.sh` 脚本。

## 支持的操作系统

- **Ubuntu/Debian**（使用 apt）
- **Fedora/RHEL/CentOS**（使用 dnf/yum）
- **Alpine**（使用 apk）
- **Arch Linux**（使用 pacman）
- **macOS**（使用 Homebrew）
- **Windows**（通过 WSL2）- 使用安装脚本

## 安装后的操作

```bash
# SSH into remote server
ssh user@host

# Check status
openclaw status

# Run diagnostics
openclaw doctor

# Configure (models, channels, etc.)
openclaw configure

# Or use Python script for non-interactive config
python3 scripts/configure_openclaw_remote.py <host> <user> \
  --auth <key> --key-based --configure \
  --auth-choice openai-api-key --api-key "your-key"
```

## 配置选项

### 认证提供者（通过 Python 脚本配置）

- `openai-api-key` - OpenAI API 密钥
- `anthropic-api-key` - Anthropic API 密钥
- `custom-api-key` - 自定义的 OpenAI 兼容 API 密钥
- `azure-openai` - Azure OpenAI 密钥
- `google-ai` - Google AI（Gemini）密钥
- `mistral-api-key` - Mistral AI 密钥
- `zai-api-key` - Z.AI API 密钥

### 密钥存储方式

- `plaintext` - 直接存储在配置文件中（不推荐）
- `ref` - 通过环境变量引用（推荐）

### 网关配置

```bash
--gateway-mode local    # Local gateway (default)
--gateway-mode remote   # Remote gateway
--gateway-port 18789
```

## 环境变量

为了实现安全的非交互式配置，请使用以下环境变量：
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export CUSTOM_API_KEY="your-key"
```

然后通过 `--secret-mode ref` 安全地引用这些环境变量。

## 故障排除

### SSH 相关问题

```bash
# Check key permissions
chmod 600 ~/.ssh/id_rsa

# Add to ssh-agent
ssh-add ~/.ssh/id_rsa
```

### 安装问题

- 确保已安装 curl 工具。
- 对于非 Docker 安装方法，需要确保已安装 Node.js 22+。
- 查看日志文件：`~/.openclaw/logs/`

### Docker 相关问题

```bash
# Check Docker status
docker ps

# View logs
docker logs openclaw

# Restart container
docker restart openclaw
```