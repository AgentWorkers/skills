---
name: openclaw-updater
description: >
  **安全更新 OpenClaw：具备预检查功能及回滚支持**  
  适用于更新 OpenClaw、检查更新可用性或从更新失败中恢复的场景。该工具可处理工作区的 Git 提交、配置备份、版本回滚以及更新后的验证操作。
---
# OpenClaw 更新器

通过自动的安全检查及回滚功能，安全地更新 OpenClaw。

## 更新前的检查清单

在运行 `openclaw update` 之前，请务必先运行更新前的脚本：

```bash
bash scripts/pre-update.sh
```

（可选）：指定一个在更新前运行的备份脚本：

```bash
BACKUP_SCRIPT=~/repo/scripts/backup-openclaw.sh bash scripts/pre-update.sh
```

该脚本将执行以下操作：
1. 查找 `~/.openclaw/` 目录下的所有 `workspace*` 目录。
2. 提交所有未提交的更改（如果尚未初始化 Git，则会先初始化 Git）。
3. 将 `openclaw.json` 备份到 `/tmp/openclaw.json.bak`。
4. 如果提供了备份脚本，则会运行该脚本。
5. 将当前版本保存到 `/tmp/openclaw-prev-version.txt`。

## Telegram 通知设置

更新脚本会通过 Telegram Bot API 发送成功/失败通知（绕过 OpenClaw 的网关，因此即使更新导致网关故障也能正常通知）。

创建 `~/.openclaw/.telegram-notify.env` 文件：

```
TELEGRAM_BOT_TOKEN=<your-bot-token>
TELEGRAM_CHAT_ID=<your-chat-id>
```

```bash
chmod 600 ~/.openclaw/.telegram-notify.env
```

该 bot 的 token 与您的 OpenClaw Telegram 频道使用的 token 相同。Chat ID 可以在 `openclaw` 目录中找到。

## 自动更新（含通知）

运行完整的更新流程，包括自动的安全检查及通知：

```bash
bash scripts/update.sh
```

流程如下：预检查 → 更新 → 等待网关恢复 → 通过 Telegram 发送通知。

## 手动更新

在预检查通过后，可以手动执行更新：

```bash
openclaw update
```

## 更新后的验证

更新完成后，请进行以下验证：
- 确认版本号显示为新版本。
- 确认网关正在运行。
- 确认所有代理都能正常响应。

## 回滚

如果更新导致了问题：

```bash
bash scripts/rollback.sh
```

脚本将执行以下操作：
1. 从 `/tmp/openclaw-prev-version.txt` 中读取之前的版本信息。
2. 通过 `npm install -g openclaw@<version>` 安装该版本。
3. （可选）从备份中恢复 `openclaw.json` 文件。
4. 重启网关。

### 手动回滚

如果回滚脚本不可用：

```bash
# Install specific version
npm install -g openclaw@<version>

# Restore config
cp /tmp/openclaw.json.bak ~/.openclaw/openclaw.json

# Restart
openclaw gateway restart
```

### 从完整备份中恢复数据

如果配置文件和工作空间数据都损坏了：

```bash
# Find latest backup
ls -t ~/repo/backups/openclaw-*.tar.gz | head -1

# Restore (overwrites ~/.openclaw/)
tar xzf ~/repo/backups/openclaw-<timestamp>.tar.gz -C ~/
```