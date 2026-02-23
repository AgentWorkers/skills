---
name: safe-backup
description: 备份 OpenClaw 的状态目录和工作区数据。此过程会排除敏感文件，并将数据打包以便备份。当用户请求备份、导出或保存状态时，该操作会被触发。
---
# 安全备份

根据最佳安全实践，对 OpenClaw 的状态目录和工作空间进行备份。

## ⚠️ 安全警告

- **备份文件可能包含敏感数据** - 在共享之前请仔细检查。
- **如果将备份文件上传到 GitHub** - 请使用私有仓库，并考虑使用加密。
- `auth-profiles.json` 文件会被排除在备份之外** - 恢复后需要重新进行身份验证。
- 本脚本不会自动将备份文件推送到任何远程服务器。

## 快速入门

### 1. 运行备份脚本

```bash
~/.openclaw/skills/safe-backup/scripts/backup.sh
```

### 2. 查看备份结果

```bash
备份文件：/tmp/safe-backup-20260223.tar.gz
```

### 3. 安全存储备份文件

请参阅下面的“存储选项”部分。

---

## 备份的内容

### ✅ 可以备份的文件（安全存储）

| 目录 | 内容 |
|-----------|----------|
| `~/.openclaw/` | OpenClaw 配置文件 |
| `~/.openclaw/workspace/` | 代理工作空间文件 |
| `agents/` | 代理定义文件 |
| `skills/` | 已安装的技能插件 |
| `memory/` | 内存相关文件 |
| `hooks/` | 自定义钩子脚本 |

### ❌ 不可备份的文件（包含敏感信息）

| 文件类型 | 原因 |
|---------|--------|
| `*.log` | 日志文件 |
| `sessions.json` | 会话数据 |
| `auth-profiles.json` | API 令牌和凭据 |
| `.env` | 环境变量 |
| `*.pem`, `*.key` | TLS/SSH 密钥 |
| `credentials.json` | 存储的凭据 |
| `api-keys.json` | API 密钥 |

---

## 完整的工作流程

### 第一步：备份

```bash
# 第一步：运行备份脚本
~/.openclaw/skills/safe-backup/scripts/backup.sh

# 第二步：验证备份内容
tar -tzf /tmp/safe-backup-20260223.tar.gz | less

# 第三步：记录备份文件的路径
# 输出示例：/tmp/safe-backup-20260223.tar.gz
```

### 第二步：存储备份文件

选择以下一种存储方式：

#### 选项 A：本地加密存储（推荐）

```bash
# 创建加密备份文件
openssl enc -aes-256-cbc -salt -in /tmp/safe-backup-20260223.tar.gz -out ~/backups/safe-backup-20260223.tar.gz.enc

# 按提示输入强密码

# 删除未加密的备份文件
rm /tmp/safe-backup-20260223.tar.gz
```

#### 选项 B：使用私有 GitHub 仓库

```bash
# 一次性设置：在 GitHub 上创建私有仓库
git clone https://github.com/YOUR_USERNAME/safe-backup.git ~/safe-backup

# 解压备份文件
mkdir -p ~/safe-backup/2026-02-23
tar -xzf /tmp/safe-backup-20260223.tar.gz -C ~/safe-backup/2026-02-23/

# 提交并推送备份文件
cd ~/safe-backup
git add .
git commit -m "备份 2026-02-23"
git push origin main

# 删除本地备份文件
rm -rf ~/safe-backup
rm /tmp/safe-backup-20260223.tar.gz
```

#### 选项 C：使用 rsync 备份到远程服务器

```bash
# 示例：将备份文件同步到远程服务器
rsync -avz --exclude='*.log' \
  --exclude='sessions.json' \
  ~/.openclaw/ user@backup-server:/path/to/backups/
```

### 第三步：恢复备份文件

#### 第一步：找到备份文件

```bash
# 如果备份文件已加密
openssl enc -aes-256-cbc -d -in ~/backups/safe-backup-20260223.tar.gz.enc -out /tmp/safe-backup.tar.gz

# 如果备份文件是未加密的 tar 文件
cp /path/to/safe-backup-20260223.tar.gz /tmp/
```

#### 第二步：停止 OpenClaw 代理服务

```bash
systemctl --user stop openclaw-gateway
```

#### 第三步：恢复文件

```bash
# 将备份文件解压到临时目录
mkdir -p /tmp/restore
tar -xzf /tmp/safe-backup.tar.gz -C /tmp/restore

# 恢复状态目录
cp -r /tmp/restore/state/* ~/.openclaw/

# （如果需要）恢复工作空间文件
cp -r /tmp/restore/workspace/* ~/.openclaw/workspace/
```

#### 第四步：重新进行身份验证

由于 `auth-profiles.json` 文件被排除在备份之外，因此需要重新配置身份验证信息：

```bash
# 通过 `openclaw config edit` 命令编辑配置文件以添加身份验证信息
# 或者手动创建 `auth-profiles.json` 文件
nano ~/.openclaw/agents/main/agent/auth-profiles.json
```

需要重新配置的信息包括：
- Telegram 机器人令牌
- Discord 机器人令牌
- Feishu 服务凭据
- 其他 API 密钥

#### 第五步：重新启动 OpenClaw 代理服务

```bash
systemctl --user start openclaw-gateway

# 验证代理服务是否正常运行
openclaw status
```

---

## 环境变量

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `OPENCLAW_STATE_DIR` | `$HOME/.openclaw` | OpenClaw 的状态目录 |
| `OPENCLAW_WORKSPACE_DIR` | `$HOME/.openclaw/workspace` | 工作空间目录 |

示例配置：

```bash
OPENCLAW_STATE_DIR=/data/openclaw ~/.openclaw/skills/safe-backup/scripts/backup.sh
```

---

## 常见问题与解决方法

### “找不到状态目录”

```bash
# 检查 OpenClaw 是否已安装
ls -la ~/.openclaw
```

### “权限不足”

```bash
# 以正确的权限运行备份脚本
chmod +x ~/.openclaw/skills/safe-backup/scripts/backup.sh
```

### 备份失败

```bash
# 检查备份文件的完整性
tar -tzf /tmp/safe-backup.tar.gz

# 如果备份文件已加密，验证密码是否正确
openssl enc -aes-256-cbc -d -in backup.enc -o /dev/null
```

---

## 最佳实践

1. **定期备份**：至少每周备份一次。
2. **测试恢复功能**：定期验证备份文件能否成功恢复。
3. **异地存储**：将备份文件存储在不同的位置。
4. **加密备份**：切勿将未加密的备份文件存储在云端。
5. **记录更改**：备份后记录所有需要重新配置的设置。