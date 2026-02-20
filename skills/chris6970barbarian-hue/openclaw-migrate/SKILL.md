# OpenClaw 迁移技巧

通过 SSH 将 OpenClaw 从一个主机迁移到另一个主机。

## 技能元数据

- **名称**: openclaw-migrate
- **类型**: OpenClaw 技能
- **用途**: 将所有 OpenClaw 配置、技能、内存数据及令牌迁移到新主机

## 设置命令

### 先决条件

1. 具备对新主机的 SSH 访问权限
2. 在新主机上安装了 SSH 密钥（推荐用于自动化操作）
3. 新主机上已安装了 NPM

### 配置

```bash
# Configure migration target
openclaw-migrate setup

# It will ask for:
# - New host IP/hostname (e.g., 192.168.1.50)
# - SSH user (e.g., crix)
# - SSH key path (optional, Enter for default)
```

## 使用命令

### 主要迁移操作

```bash
# Start migration (one command!)
openclaw-migrate migrate
```

### 其他命令

```bash
# Test SSH connection
openclaw-migrate test

# Show current configuration
openclaw-migrate status

# Reconfigure target
openclaw-migrate setup
```

## 被同步的内容

### 文件与目录

| 源目录 | 目标目录 |
|--------|-------------|
| `~/.openclaw/` | `~/.openclaw/` （包含技能、内存数据和配置文件） |
| `~/.config/openclaw/` | `~/.config/openclaw/` |
| OpenClaw 的 npm 包 | 如果缺失则重新安装 |

### 环境变量

| 变量 | 描述 |
|----------|-------------|
| `HA_URL` | Home Assistant 的 URL |
| `HA_TOKEN` | Home Assistant 的令牌 |
| `GITHUB_TOKEN` | GitHub API 令牌 |
| `BRAVE_API_KEY` | Brave 搜索 API 的令牌 |
| `GOOGLE_API_KEY` | Google API 的令牌 |
| 任何以 `HA_` 开头的变量 | 与 Home Assistant 相关的所有变量 |

### 系统数据

- Cron 作业（通过 crontab 管理）
- OpenClaw 网关配置

## 迁移流程

```
1. setup → Configure target host
2. test → Verify SSH connection
3. migrate → Full sync and start
   ├─ Check/Install OpenClaw
   ├─ Sync workspace (~/.openclaw/)
   ├─ Sync config
   ├─ Sync environment variables
   ├─ Sync cron jobs
   └─ Start gateway on new host
```

## 错误处理

- SSH 连接失败：提供重试选项
- 远端主机上没有 OpenClaw：提示用户是否需要安装
- 同步失败：报告哪些文件同步失败
- 配置文件缺失：提示用户进行配置设置

## 相关技能

- skillstore（用于搜索/安装技能）

## 文件

```
openclaw-migrate/
├── SKILL.md       # This file
├── README.md      # User docs
├── main.js        # Migration CLI
└── config.json    # Saved target config
```