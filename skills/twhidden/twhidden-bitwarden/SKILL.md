---
name: bitwarden-vaultwarden
description: Bitwarden 与 Vaultwarden 密码管理器的集成功能：用于存储、检索、生成或管理密码及凭证。该集成方案为 Bitwarden 的命令行界面（bw）添加了自动会话管理功能，同时支持官方的 Bitwarden 服务器以及自托管的 Vaultwarden 服务器。
homepage: https://github.com/TWhidden/openclaw-skill-bitwarden
metadata:
  clawdbot:
    emoji: "🔐"
    requires:
      env: ["BW_SERVER", "BW_EMAIL", "BW_MASTER_PASSWORD"]
      primaryEnv: "BW_SERVER"
      bins: ["bw", "python3"]
      files: ["bw.sh"]
---
# Bitwarden 与 Vaultwarden

这是一个用于 Bitwarden/Vaultwarden 的命令行工具（`bw`），具备自动登录、会话缓存以及便捷的命令功能。该工具可无缝兼容官方的 Bitwarden（`vault.bitwarden.com`）以及自托管的 Vaultwarden 实例。

## 必备条件

- 已安装 Bitwarden CLI (`bw`): `npm install -g @bitwarden/cli`
- 需要有一个 Bitwarden 或 Vaultwarden 服务器实例
- 配置好相应的凭据（详见下方“配置”部分）

## 配置

您可以通过环境变量或凭据文件来设置凭据：

```bash
# Environment variables (preferred)
export BW_SERVER="https://vault.bitwarden.com"  # Official Bitwarden
# OR
export BW_SERVER="https://your-vaultwarden-instance.example.com"  # Vaultwarden
export BW_EMAIL="your-email@example.com"
export BW_MASTER_PASSWORD="your-master-password"

# Or use a credentials file (default: secrets/bitwarden.env)
export CREDS_FILE="/path/to/your/bitwarden.env"
```

凭据文件应包含以下内容：

```
BW_SERVER=https://vault.bitwarden.com
BW_EMAIL=your-email@example.com
BW_MASTER_PASSWORD=your-master-password
```

## 使用方法

```bash
bash skills/bitwarden/bw.sh <command> [args...]
```

## 命令列表

| 命令 | 功能 | 例示 |
|---------|-------------|---------|
| `login` | 登录并解锁保管库 | `bw.sh login` |
| `status` | 显示保管库状态 | `bw.sh status` |
| `list [search]` | 列出/搜索项目 | `bw.sh list github` |
| `get <name|id>` | 获取项目的完整 JSON 数据 | `bw.sh get "GitHub"` |
| `get-password <name|id>` | 仅获取密码 | `bw.sh get-password "GitHub"` |
| `get-username <name|id>` | 仅获取用户名 | `bw.sh get-username "GitHub"` |
| `create <name> <user> <pass> [uri] [notes]` | 创建新登录账户 | `bw.sh create "GitHub" user pass https://github.com` |
| `generate [length]` | 生成新密码 | `bw.sh generate 32` |
| `delete <id>` | 删除项目 | `bw.sh delete <uuid>` |
| `lock` | 锁定保管库 | `bw.sh lock` |

## 工作流程

1. 每次会话开始时，首先执行 `bw.sh login`（使用配置的凭据自动登录）
2. 会话令牌会被缓存到 `/tmp/.bw_session` 文件中
3. 之后的所有命令都会自动使用缓存的会话信息
4. 重启系统后，需要再次执行 `login` 命令

## 新凭据的存储方式

```bash
# Generate + store
PASS=$(bash skills/bitwarden/bw.sh generate 32)
bash skills/bitwarden/bw.sh create "New Service" "user@email.com" "$PASS" "https://service.com"
```

## 安全注意事项

- **严禁** 将敏感信息粘贴到日志、聊天记录或代码中。
- **请确保 `bitwarden.env` 文件不在版本控制范围内**。
- 为凭据文件设置权限，使其仅对所有者可见（`chmod 600`）。
- 会话令牌存储在 `/tmp` 目录中，并在用户登出时被清除。

## 外部接口

| 接口 | 功能 | 发送的数据 |
|---------|---------|-----------|
| 用户配置的 BW_SERVER | Bitwarden/Vaultwarden API | 加密的保管库数据及认证凭据 |

**注意:** 该工具会通过您指定的 `BW_SERVER` 与 Bitwarden 服务器进行通信。对于官方 Bitwarden，该地址为 `https://vault.bitwarden.com`；对于自托管的 Vaultwarden 实例，则使用您的自定义 URL。

## 安全性与隐私保护

**会发送到外部服务器的数据：**
- 认证请求（包括电子邮件地址和主密码）至您配置的 Bitwarden 服务器
- 加密的保管库数据（用于创建、读取、更新或删除操作）

**保留在本地的数据：**
- 会话令牌（缓存于 `/tmp/.bw_session`）
- 凭据文件（如果使用了 `bitwarden.env`）
- 解密后的密码（仅存在于内存中，不会被写入磁盘）

**信任声明：**
使用本工具意味着您会将认证凭据和保管库数据发送到您指定的 Bitwarden 服务器。请确保您信任所使用的 Bitwarden/Vaultwarden 实例后再进行安装。

## 使用场景

该工具可由 OpenClaw 代理自动执行以下操作：
- 安全存储凭据
- 为自动化任务检索密码
- 生成安全密码

如果您希望在执行密码相关操作前需要人工审批，请相应地配置 OpenClaw 代理的策略。

## 安全最佳实践：
1. **凭据文件**：为 `secrets/bitwarden.env` 设置权限（`chmod 600`）
2. **环境隔离**：不要在不同系统间共享凭据文件
3. **会话令牌**：设置自动过期机制；操作完成后执行 `bw.sh lock` 命令
4. **Git 设置**：在 `.gitignore` 文件中排除所有包含敏感信息的文件（如 `secrets/`, `*.env`, `.bw_session`）
5. **主密码**：切勿将主密码硬编码或记录在日志中