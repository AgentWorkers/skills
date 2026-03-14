---
name: soul-transfer
description: "将 OpenClaw 代理的工作空间（包括内存数据、配置信息、凭据、技能设置以及定时任务）备份到 Git 仓库，并从 Git 仓库恢复这些数据。适用场景包括：迁移至新实例、灾难恢复、设置新机器、用户请求备份/恢复数据、数据迁移等。此外，也可用于定期备份及备份数据的验证。"
---
# 灵魂转移（夺舍）

通过 Git 在不同的 OpenClaw 实例之间迁移代理的工作空间。

## 概念

- **灵魂**：指工作空间文件（包括内存数据、身份信息、技能设置以及所使用的框架）  
- **载体**：指 OpenClaw 实例（包含运行时环境、配置信息以及定时任务）  
- **备份仓库**：用于存储灵魂（即工作空间文件）的 Git 仓库  
- **转移**：将灵魂文件克隆到新的载体实例中，恢复配置信息并重建运行时状态  

- `$WORKSPACE`：代理的工作空间目录（可以通过系统提示中的仓库路径来确定，或者作为备用路径使用 `~/.openclaw/workspace`）  
- `openclaw-config-backup.json`：导出的 OpenClaw 配置快照文件（包含通道令牌、API 密钥、运行时设置等）。你可以随意命名这个文件，但请确保将其保存在工作空间中并提交到备份仓库中。  

## 备份流程  

### 1. 确保 Git 远程仓库已配置  

```bash
cd $WORKSPACE
git remote get-url origin || git remote add origin https://<token>@github.com/<owner>/<repo>.git
```  

### 2. 导出当前的 OpenClaw 配置  

保存当前的配置信息，以便后续恢复。该文件包含通道令牌、API 密钥以及公会设置（这些信息不在工作空间的 markdown 文件中）。  

使用 `gateway config.get` 工具提取配置数据，然后将其写入工作空间中的 JSON 文件（例如 `openclaw-config-backup.json`）。  
这一步非常关键——如果没有这个文件，新实例将无法恢复通道连接。  

### 3. 提交并推送配置文件  

```bash
git add -A
git commit -m "backup: $(date +%Y-%m-%d_%H%M)"
git push origin master
```  

### 4. 验证备份文件  

```bash
git log --oneline -1
git diff --stat HEAD~1
```  

### 自动备份（使用 Cron 任务）  

设置一个定时任务来自动执行备份操作。具体配置方法请参考 `references/cron-templates.md`。  

## 恢复流程（夺舍操作步骤）  

按照以下顺序执行步骤，切勿跳过第 5 步——这一步经常被忽略：  

### 第 1 步：克隆备份仓库  

```bash
git clone https://<token>@github.com/<owner>/<repo>.git /tmp/soul-backup
```  

### 第 2 步：检查备份内容  

在恢复之前，请仔细检查备份仓库中的文件内容：  
- 确定哪些敏感文件不应被复制到工作空间中（例如独立的凭证文件、API 密钥文件等）。  

### 第 3 步：恢复工作空间文件  

将备份文件复制到 `$WORKSPACE` 目录中：  
- 身份相关文件：`IDENTITY.md`、`USER.md`、`SOUL.md`  
- 内存相关文件：`MEMORY.md`、`AGENTS.md`、`HEARTBEAT.md`、`NOW.md`、`SESSION-STATE.md`  
- 状态相关文件：`heartbeat-state.json`  
- 日志文件：`memory/*.md`  
- 技能相关文件：`skills/` 目录下的所有 `.md` 或 `.json` 文件  
- 配置文件：`openclaw-config-backup.json`  

### 第 4 步：清除 markdown 文件中的硬编码凭证  

将 markdown 文件中的凭证信息替换为 `[REDACTED]`。  
**注意**：不要清除配置备份文件中的凭证信息，因为它们在后续步骤中仍然需要使用。  

### 第 5 步：恢复 OpenClaw 配置（⚠️ 非常重要——切勿跳过）  

这一步用于重新连接各个通道、设置 API 密钥以及恢复运行时配置。如果没有执行这一步，所有通道将保持断开状态。  
从工作空间中读取配置备份文件，提取以下信息：  
- 通道令牌（如 Discord 机器人令牌、Telegram 令牌等）  
- 通道设置（公会信息、允许列表、私信政策等）  
- API 密钥  
- 工具设置（执行安全级别等）  
- 环境变量  

使用 `gateway config.patch` 命令应用这些配置更改：  
```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "<from config backup>",
      "groupPolicy": "allowlist",
      "guilds": { "..." },
      "dm": { "..." },
      "actions": { "..." }
    }
  },
  "tools": {
    "web": { "search": { "apiKey": "<from config backup>" } },
    "exec": { "security": "full" }
  }
}
```  

配置更新完成后，OpenClaw 会自动重启。使用 `openclaw status` 命令验证通道是否已连接成功。  
如果 OpenClaw 的版本与备份版本不同，可以使用 `config.schemalookup` 命令检查字段名称是否一致。  

### 第 6 步：重新配置定时任务  

定时任务属于运行时状态数据，不存储在 Git 仓库中。请根据文档或 `references/cron-templates.md` 中的示例重新配置定时任务。  
仅恢复那些仍然需要的定时任务。  

### 第 7 步：验证并清理  

```bash
# Verify channel connectivity
openclaw status

# Delete temp clone
rm -rf /tmp/soul-backup

# Delete BOOTSTRAP.md if present (no longer a fresh instance)
rm -f $WORKSPACE/BOOTSTRAP.md

# Commit restored state
cd $WORKSPACE
git add -A && git commit -m "夺舍完成: $(date +%Y-%m-%d_%H%M)"
```  

### 第 8 步：记录操作日志  

在每日日志中记录此次灵魂转移的操作过程，包括时间戳、文件数量以及遇到的任何问题。  

## 常见问题  

1. **忽略配置恢复**：虽然工作空间文件被恢复了，但通道连接可能仍未恢复。因此必须执行 `config.patch` 操作。  
2. **错误地清除凭证信息**：不要清除配置备份文件中的凭证信息，因为它们是 `config.patch` 所必需的。只需清除 markdown 或日志文件中的凭证信息即可。  
3. **忘记重新配置定时任务**：定时任务属于运行时状态数据，不在 Git 仓库中保存，需要手动重新配置。  
4. **配置文件格式不一致**：在应用配置更改之前，请使用 `config.schemalookup` 命令检查字段名称是否正确（不同版本的 OpenClaw 可能会修改字段名称）。  
5. **Git 远程仓库未配置**：新实例可能没有配置远程仓库，请在首次备份前完成配置设置。  

## 备份完整性检查  

定期运行检查命令以验证备份文件的完整性：  
```bash
cd $WORKSPACE
# Check remote is configured
git remote -v
# Check last push time
git log --oneline -1
# Check for uncommitted changes
git status --short
# Verify config backup exists and has channel tokens
grep -c '"token"' openclaw-config-backup.json 2>/dev/null || echo "⚠️ No config backup found"
```