---
name: safe-backup
description: 备份 OpenClaw 的状态目录和工作区数据。此过程会排除敏感文件，并将数据打包以便备份。当用户请求备份、导出或保存状态时，该功能会被触发。
---
# 安全备份

本脚本遵循最佳安全实践，用于备份 OpenClaw 的状态目录和工作空间。

## ⚠️ 安全警告

- **备份文件可能包含敏感数据** – 在共享之前请仔细检查。
- **如果将备份文件上传到 GitHub** – 请使用私有仓库，并考虑使用加密。
- `auth-profiles.json` 文件会被排除在备份之外** – 恢复后需要重新进行身份验证。
- 本脚本不会自动将备份文件推送到任何远程服务器。

## 快速入门

### 1. 运行备份脚本

```bash
~/.openclaw/skills/safe-backup/scripts/backup.sh
```

### 2. 查看备份结果

```bash
备份文件：/tmp/safe-backup-20260223.tar.gz  （Linux）
备份文件：/var/folders/xx/.../safe-backup-20260223.tar.gz  （macOS）
备份文件：C:\Users\xxx\AppData\Local\Temp\safe-backup-20260223.tar.gz  （Windows）
```

### 3. 安全存储备份文件

具体存储方式请参见下方的“存储选项”部分。

---

## 跨平台迁移

### 平台支持

| 平台 | 支持情况 | 要求 |
|----------|--------|--------------|
| **Linux** | 完全支持 | 需要原生 bash |
| **macOS** | 完全支持 | 需要原生 bash |
| **Windows (Git Bash)** | 支持 | 需要安装 Git for Windows |
| **Windows (WSL)** | 支持 | 需要 WSL Ubuntu/Debian 环境 |
| **Windows (Native CMD)** | 不支持 | 需要安装 bash |

### 迁移时的重要注意事项

#### 1. 自动检测临时目录

脚本会自动为每个平台选择合适的临时目录：

| 平台 | 临时目录 | 环境变量 |
|----------|----------------|---------------------|
| Linux | `/tmp` | - |
| macOS | `/var/folders/xx/...` | `$TMPDIR` |
| Windows (Git Bash) | `C:\Users\xxx\AppData\Local\Temp` | `$TEMP` / `$TMP` |

#### 2. 使用 `rsync` 进行文件复制

脚本使用 `rsync` 来高效地复制文件：

- **Linux/macOS**：内置支持
- **Windows**：需要安装 Git Bash（其中包含 `rsync`）。

如果系统中没有 `rsync`，脚本将无法正常运行。对于没有安装 Git Bash 的 Windows 系统，需要单独安装 `rsync`（例如通过 MSYS2 或 Cygwin）。

#### 3. 路径分隔符

脚本使用 Unix 风格的正斜杠（`/`）：

- Linux ✅
- macOS ✅
- Git Bash ✅
- WSL ✅
- Windows (Native CMD) 使用反斜杠（`\`），需要修改脚本才能正确处理。

#### 4. 检测用户主目录

脚本使用 `$HOME` 环境变量来确定主目录：

- Linux: `/home/username`
- macOS: `/Users/username`
- Windows (Git Bash): `C:\Users\username`

#### 平台特定的注意事项

#### Windows (Git Bash)

```bash
# 请从 Git Bash 中运行脚本，而非 CMD 或 PowerShell
~/.openclaw/skills/safe-backup/scripts/backup.sh
```

如果出现“找不到 rsync”的错误，请安装包含 `rsync` 的 Git for Windows 版本。

#### macOS

```bash
# 本平台支持原生 bash
~/.openclaw/skills/safe-backup/scripts/backup.sh
```

备份文件将存储在 `$TMPDIR` 目录下（例如：`/var/folders/xx/...`）。

#### Linux

```bash
# 本平台支持原生 bash
~/.openclaw/skills/safe-backup/scripts/backup.sh
```

备份文件将存储在 `/tmp` 目录下。

---

## 备份内容

### 可以备份的文件

| 目录 | 包含的内容 |
|-----------|----------|
| `~/.openclaw/` | OpenClaw 配置文件 |
| `~/.openclaw/workspace/` | 代理工作空间文件 |
| `agents/` | 代理配置文件 |
| `skills/` | 已安装的技能相关文件 |
| `memory/` | 内存相关文件 |
| `hooks/` | 自定义钩子文件 |

### 不可备份的文件（敏感数据）

| 文件类型 | 原因 |
|---------|--------|
| `*.log` | 日志文件 |
| `*.log.*` | 日志轮换文件 |
| `sessions.json` | 会话数据 |
| `logs/` | 日志目录 |
| `auth-profiles.json` | API 密钥和凭据 |
| `.env` | 环境变量 |
| `*.pem`, `*.key` | TLS/SSH 密钥 |
| `credentials.json` | 存储的凭据 |
| `api-keys.json` | API 密钥 |
| `sessions/` | 运行时会话数据 |
| `browser/` | 浏览器缓存 |
| `canvas/` | Canvas 缓存 |
| `media/` | 临时媒体文件 |
| `backups/` | 备份目录本身 |
| `delivery-queue/` | 运行时队列 |
| `devices/` | 设备缓存 |
| `subagents/` | 子代理配置 |
| `completions/` | 自动完成功能相关文件 |
| `*.bak` | 备份文件 |
| `*.save` | 保存的文件 |
| `update-check.json` | 更新检查相关文件 |

---

## 完整的工作流程

### 使用场景

| 场景 | 推荐方案 | 说明 |
|----------|---------------------|-------------|
| **定期备份** | 本地加密存储 | 每周备份，存储在加密的本地目录中 |
| **迁移到新机器** | 本地压缩文件 + USB 传输 | 避免通过网络传输备份文件 |
| **云灾难恢复** | 使用私有 GitHub 仓库 | 将备份文件存储在远程服务器上并加密 |
| **服务器环境** | 使用 `rsync` 备份到备份服务器 | 自动定期同步，适用于生产环境 |

---

### 第一步：备份

```bash
# 第一步：运行备份脚本
~/.openclaw/skills/safe-backup/scripts/backup.sh

# 第二步：查看备份文件的位置（查看输出结果的最后一行）
# 脚本会显示：`Backup file: /path/to/safe-backup-YYYYMMDD.tar.gz`

# 第三步：验证备份内容
tar -tzf "$(ls -t /tmp/safe-backup-*.tar.gz | head -1)" | head -20

# 或者使用输出中显示的文件路径：
tar -tzf /tmp/safe-backup-20260223.tar.gz | head -20
```

### 第二步：存储备份文件

选择以下一种存储方式：

#### 选项 A：本地加密存储（推荐）

```bash
# 查找最新的备份文件
BACKUP_FILE=$(ls -t /tmp/safe-backup-*.tar.gz | head -1)

# 创建加密文件
openssl enc -aes-256-cbc -salt -in "$BACKUP_FILE" -out ~/backups/safe-backup-$(date +%Y%m%d).tar.gz.enc

# 根据提示输入强密码

# 删除未加密的备份文件
rm "$BACKUP_FILE"
```

#### 选项 B：使用私有 GitHub 仓库

```bash
# 一次性设置：在 GitHub 上创建私有仓库
# 查找最新的备份文件
BACKUP_FILE=$(ls -t /tmp/safe-backup-*.tar.gz | head -1)

# 克隆私有仓库
git clone https://github.com/YOUR_USERNAME/safe-backup.git ~/safe-backup

# 解压备份文件
mkdir -p ~/safe-backup/$(date +%Y-%m-%d)
tar -xzf "$BACKUP_FILE" -C ~/safe-backup/$(date +%Y-%m-%d)

# 提交并推送备份文件
cd ~/safe-backup
git add .
git commit -m "Backup $(date +%Y-%m-%d)"
git push origin main

# 删除本地备份文件
rm -rf ~/safe-backup
rm "$BACKUP_FILE"
```

#### 选项 C：将备份文件同步到远程服务器

```bash
# 示例：将备份文件同步到远程服务器
rsync -avz --exclude='*.log' \
  --exclude='sessions.json' \
  ~/.openclaw/ user@backup-server:/path/to/backups/
```

### 第三步：恢复数据

#### 第一步：定位备份文件

```bash
# 如果备份文件是加密的，先解密文件
openssl enc -aes-256-cbc -d -in ~/backups/safe-backup-20260223.tar.gz.enc -out /tmp/safe-backup.tar.gz

# 如果备份文件是未加密的文件，直接复制到目标位置
# 例如：cp /path/to/your/backup/safe-backup-20260223.tar.gz /tmp/
```

#### 第四步：停止 OpenClaw 服务

```bash
systemctl --user stop openclaw-gateway
```

#### 第五步：恢复数据

```bash
# 根据平台选择正确的临时目录
if [[ -n "$TMPDIR" ]]; then
    TEMP_DIR="$TMPDIR"
elif [[ -n "$TEMP" ]]; then
    TEMP_DIR="$TEMP"
elif [[ -n "$TMP" ]]; then
    TEMP_DIR="$TMP"
else
    TEMP_DIR="/tmp"
fi

# 解压备份文件
mkdir -p "$TEMP_DIR/restore"
tar -xzf "$TEMP_DIR/safe-backup.tar.gz" -C "$TEMP_DIR/restore"

# 恢复状态目录
cp -r "$TEMP_DIR/restore/state/"* ~/.openclaw/

# （如果需要）恢复工作空间
cp -r "$TEMP_DIR/restore/workspace/"* ~/.openclaw/workspace/

# 由于 `auth-profiles.json` 文件被排除在备份之外，需要重新配置身份验证信息：
# 编辑配置文件以添加身份验证信息
openclaw config edit

# 或者手动创建 `auth-profiles.json` 文件
nano ~/.openclaw/agents/main/agent/auth-profiles.json

# 需要重新配置的信息包括：
- Telegram 机器人令牌
- Discord 机器人令牌
- Feishu 账户凭据
- 其他 API 密钥

# 重新启动 OpenClaw 服务
systemctl --user start openclaw-gateway

# 验证恢复后的系统状态
openclaw status
```

---

## 环境变量

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `OPENCLAW_STATE_DIR` | `$HOME/.openclaw` | OpenClaw 的状态目录 |
| `OPENCLAW_WORKSPACE_DIR` | `$HOME/.openclaw/workspace` | OpenClaw 的工作空间目录 |

示例：

```bash
OPENCLAW_STATE_DIR=/data/openclaw ~/.openclaw/skills/safe-backup/scripts/backup.sh
```

---

## 故障排除

### “找不到状态目录”

```bash
# 检查 OpenClaw 是否已安装
ls -la ~/.openclaw
```

### “权限不足”

```bash
# 以正确的权限运行脚本
chmod +x ~/.openclaw/skills/safe-backup/scripts/backup.sh
```

### “找不到 rsync”

```bash
# 在 Windows 上安装包含 `rsync` 的 Git for Windows 版本，或使用 WSL 环境。
# 或者通过 MSYS2 安装 `rsync`：
# pacman -S rsync
```

### 备份失败

```bash
# 检查备份文件的完整性
tar -tzf /path/to/your/backup.tar.gz

# 如果备份文件是加密的，验证解密过程中是否出现错误
openssl enc -aes-256-cbc -d -in backup.enc -o /dev/null
```

---

## 最佳实践

- **定期备份**：至少每周备份一次。
- **定期测试恢复功能**：确保备份文件可以正常恢复。
- **将备份文件存储在异地**：避免将备份文件存储在本地。
- **加密备份文件**：切勿将未加密的备份文件存储在云服务器上。
- **记录变更**：备份后记录所有需要重新配置的设置。