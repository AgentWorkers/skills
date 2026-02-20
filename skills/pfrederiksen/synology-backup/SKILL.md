---
name: synology-backup
description: "通过 SMB 将 OpenClaw 工作区、配置文件以及代理数据备份并恢复到 Synology NAS。适用场景包括：备份工作区文件、从快照中恢复数据、检查备份状态/健康状况，或设置自动备份机制。该方案支持使用 Tailscale 来实现安全的远程 VPS 到 NAS 的连接。"
---
# Synology 备份

将 OpenClaw 数据通过 SMB 协议备份到 Synology NAS。该方案支持安全的、自动化的每日快照备份，并允许用户配置保留策略。

## 设置

### 1. 网络连接

对于 VPS 到 NAS 的备份，使用 [Tailscale](https://tailscale.com) 来实现安全连接，同时避免将 SMB 协议暴露在互联网上：

1. 在 Synology 上安装 Tailscale（通过包中心搜索“Tailscale”）。
2. 在 VPS 上安装 Tailscale（执行命令：`curl -fsSL https://tailscale.com/install.sh | sh`）。
3. 将两台设备连接到同一个 Tailscale 网络中。
4. 在配置文件中使用 Synology 的 Tailscale IP 地址。

对于本地网络环境，可以直接使用 NAS 的本地 IP 地址。

### 2. Synology 准备

1. 在 Synology 上创建一个专用用户（例如 `openclaw-backup`）。
2. 创建或选择一个共享文件夹（例如 `backups`）。
3. 授予该用户对该文件夹的读写权限。

### 3. 凭据文件

创建一个用于存储凭据的文件（权限设置为 `chmod 600`）——**切勿将凭据存储在配置文件或脚本中**：

```bash
cat > ~/.openclaw/.smb-credentials << 'EOF'
username=your-synology-user
password=your-synology-password
EOF
chmod 600 ~/.openclaw/.smb-credentials
```

### 4. 配置文件

创建 `~/.openclaw/synology-backup.json` 文件：

```json
{
  "host": "100.x.x.x",
  "share": "backups/openclaw",
  "mountPoint": "/mnt/synology",
  "credentialsFile": "~/.openclaw/.smb-credentials",
  "smbVersion": "3.0",
  "backupPaths": [
    "~/.openclaw/workspace",
    "~/.openclaw/openclaw.json",
    "~/.openclaw/cron",
    "~/.openclaw/agents",
    "~/.openclaw/.env"
  ],
  "includeSubAgentWorkspaces": true,
  "retention": 7,
  "schedule": "0 3 * * *"
}
```

| 字段 | 描述 | 默认值 |
|-------|-------------|---------|
| `host` | Synology 的 IP 地址（Tailscale 连接或本地连接） | 必填 |
| `share` | SMB 共享路径 | 必填 |
| `mountPoint` | 本地挂载点 | `/mnt/synology` |
| `credentialsFile` | 存储凭据的文件路径 | 必填 |
| `smbVersion` | SMB 协议版本 | `3.0` |
| `backupPaths` | 需要备份的文件夹路径 | `workspace` 和 `config` |
| `includeSubAgentWorkspaces` | 是否自动包含子工作区的文件 | `true` |
| `retention` | 需要保留的快照天数 | `7` |
| `schedule` | 定时备份的 Cron 表达式（以主机时区为准） | `0 3 * * *` |

### 5. 安装依赖项

```bash
apt-get install -y cifs-utils rsync
```

### 6. 挂载设置

为了确保挂载在重启后仍然有效，请将相关配置添加到 `/etc/fstab` 文件中：

```
//<host>/<share> /mnt/synology cifs credentials=<credentials-file>,vers=3.0,_netdev,nofail 0 0
```

## 使用方法

### 立即备份

```bash
scripts/backup.sh
```

执行增量备份。首次运行时会复制所有文件；后续运行仅同步更改的部分。

### 恢复快照

```bash
scripts/restore.sh [date]
```

可以从指定的日期的快照中恢复数据（例如 `2026-02-20`）。如果没有指定日期，则会列出所有可用的快照。

### 检查状态

```bash
scripts/status.sh
```

显示最后一次备份的时间、快照数量、总备份大小以及挂载状态。

## 备份的内容

- `~/.openclaw/workspace/` — 存储内存数据、SOUL 数据、代理配置以及所有工作区的文件。
- `~/.openclaw/workspace-*/` — 所有子工作区的文件（如果启用了该功能）。
- `~/.openclaw/openclaw.json` — 主配置文件。
- `~/.openclaw/cron/` — Cron 作业配置文件。
- `~/.openclaw/agents/` — 代理配置文件。
- `~/.openclaw/.env` — 环境变量和 API 密钥。

## 快照结构

```
backups/
├── 2026-02-20/
│   ├── manifest.json
│   ├── workspace/
│   ├── workspace-email/
│   ├── workspace-news/
│   ├── agents/
│   ├── cron/
│   ├── openclaw.json
│   └── .env
├── 2026-02-19/
└── ...
```

## 安全注意事项

- **凭据管理**：始终使用权限设置为 `chmod 600` 的凭据文件。切勿将密码直接写入配置文件、脚本或 `/etc/fstab` 中。
- **网络安全**：使用 Tailscale 或 VPN 进行远程备份。切勿将 SMB 协议（端口 445）暴露在公共互联网上。
- **API 密钥**：`.env` 文件中包含敏感信息，请确保 Synology 的共享文件夹具有受限访问权限。
- **数据保留策略**：旧快照会自动被删除。对于关键环境，可以增加快照的保留天数。