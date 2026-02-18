---
name: personality-backup
description: 为代理的个性文件、内存数据、配置信息、敏感数据以及项目创建加密备份。当代理需要设置、运行或管理其工作空间及身份文件的自动备份时，可以使用这些备份文件。该系统支持配置备份目标，采用 AES-256 加密技术（通过 7-zip 工具实现），并支持通过电子邮件（SMTP）或本地存储来传输备份文件。
---
# 个性数据备份

对代理的身份信息、内存数据和工作区数据进行加密备份。

## 先决条件

- `p7zip-full`（7-zip 命令行工具）
- 安装了 `smtplib` 的 Python 3（用于发送电子邮件）
- 一个存储在文件中的备份密码

## 配置

创建 `~/.openclaw/secrets/backup-config.json` 文件：

```json
{
  "password_file": "/home/jan/.openclaw/secrets/backup-password.txt",
  "password_field": "Password",
  "delivery": "email",
  "email": {
    "to": "user@example.com",
    "from": "agent@example.com",
    "smtp_host": "mail.example.com",
    "smtp_port": 465,
    "smtp_user": "agent@example.com",
    "smtp_pass_env": "BACKUP_SMTP_PASS"
  },
  "local": {
    "dir": "/home/jan/backups"
  },
  "workspace": "/home/jan/.openclaw/workspace",
  "secrets_dir": "/home/jan/.openclaw/secrets",
  "config_file": "/home/jan/.openclaw/openclaw.json",
  "agent_name": "Agent",
  "agent_emoji": "",
  "personality_files": ["SOUL.md", "IDENTITY.md", "USER.md", "AGENTS.md", "MEMORY.md", "TOOLS.md"],
  "backup_memory": true,
  "backup_secrets": true,
  "backup_config": true,
  "backup_projects": true,
  "backup_scripts": true,
  "project_excludes": ["node_modules", ".git", "__pycache__", "*.mp4", "*.mp3", "*.wav"],
  "generate_restore_guide": true
}
```

所有字段都有合理的默认值。只需设置 `password_file` 和数据传输方式即可。

### 密码文件格式

密码文件应包含以下内容：
```
Password: YOUR_SECRET_KEY
```

或者将 `password_field` 设置为 `null`，此时文件的全部内容将作为密码使用。

## 使用方法

### 运行备份

```bash
bash scripts/backup.sh /path/to/backup-config.json
```

### 设置每日自动备份任务

```bash
echo "0 3 * * * bash $(pwd)/scripts/backup.sh /path/to/backup-config.json" | crontab -
```

### 数据传输方式

- **电子邮件**：通过 SMTP 将加密后的备份文件作为附件发送
- **本地存储**：将备份文件保存到本地目录

SMTP 密码：可以通过环境变量 `smtp_pass_env` 设置，或者直接在 `smtp_pass` 中指定（这种方式安全性较低）。

## 恢复数据

备份文件中包含一个名为 `RESTORE.md` 的文件，其中包含将数据恢复到新 OpenClaw 安装环境的详细步骤。恢复指南会根据代理的名称和配置进行个性化定制。