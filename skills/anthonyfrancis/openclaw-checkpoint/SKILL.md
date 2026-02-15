---
name: openclaw-checkpoint
description: 使用 Git 在不同机器之间备份和恢复 OpenClaw 工作区状态。通过将 `SOUL.md`、`MEMORY.md`、内存文件、定时任务（cron jobs）以及配置信息同步到远程仓库，实现灾难恢复功能。当用户需要备份 OpenClaw 的状态、在新机器上恢复数据、在不同计算机之间迁移数据或防止数据丢失时，可以使用该功能。提供的命令包括：`checkpoint`（帮助文档概述）、`checkpoint-setup`（交互式设置）、`checkpoint-backup`（备份检查点）、`checkpoint-restore`（交互式选择检查点或使用 `--latest` 恢复最新状态）、`checkpoint-schedule`（自动备份检查点）、`checkpoint-stop`（停止检查点备份）、`checkpoint-status`（检查点状态）、`checkpoint-init`（初始化检查点）以及 `checkpoint-reset`（重置检查点）。每次执行 `checkpoint-backup` 时，系统会自动将定时任务信息备份到 `memory/cron-jobs-backup.json` 文件中。
---

# OpenClaw 备份与恢复技能

该技能支持在多台机器之间备份和恢复 OpenClaw 的身份信息、内存内容及配置设置。

**适用平台：** 仅支持 macOS 和 Linux。Windows 不受支持。

## 概述

该技能通过将您的工作区同步到 Git 仓库来实现 OpenClaw 的灾难恢复功能，主要备份以下内容：

- **身份信息：** SOUL.md、IDENTITY.md、USER.md（您的身份信息及助手的相关设置）
- **内存内容：** MEMORY.md 及所有内存相关的.md 文件（对话记录和上下文信息）
- **定时任务：** 导出到 `memory/cron-jobs-backup.json` 的定时任务（例如每日同步、自动化操作等）
- **配置设置：** TOOLS.md、AGENTS.md、HEARTBEAT.md（工具配置和规范）
- **自定义脚本：** 您编写的自定义脚本和自动化脚本

**未同步的内容（出于安全考虑）：** API 密钥（.env.* 文件）、凭证信息、OAuth 令牌

## 安装

### 选项 1：Git 克隆（推荐）

```bash
# Clone the skill repo
git clone https://github.com/AnthonyFrancis/openclaw-checkpoint.git ~/.openclaw/skills/openclaw-checkpoint

# Copy scripts to tools directory
mkdir -p ~/.openclaw/workspace/tools
cp ~/.openclaw/skills/openclaw-checkpoint/scripts/checkpoint* ~/.openclaw/workspace/tools/
chmod +x ~/.openclaw/workspace/tools/checkpoint*

# Add to PATH (also add to ~/.zshrc or ~/.bashrc for persistence)
export PATH="${HOME}/.openclaw/workspace/tools:${PATH}"

# Run setup wizard
checkpoint-setup
```

### 选项 2：快速安装

```bash
curl -fsSL https://raw.githubusercontent.com/AnthonyFrancis/openclaw-checkpoint/main/scripts/install-openclaw-checkpoint.sh | bash
```

请在执行前先查看安装脚本的说明。

## 命令

### checkpoint
**显示所有可用命令及其使用示例。**

```bash
checkpoint
```

**功能：**  
- 显示所有备份命令的简要说明和示例

**使用场景：**  
- 当您记不清具体命令名称时  
- 需要快速查看可用选项时

### checkpoint-setup
**首次设置时的交互式引导流程。**

```bash
checkpoint-setup
```

**功能：**  
- 指导您创建一个私有的 GitHub 仓库  
- 设置 SSH 认证（推荐）或个人访问令牌  
- 自动检测 GitHub 上是否已存在 SSH 密钥  
- 生成包含恢复说明和命令的 README.md 文件  
- 提交 `~/.openclaw/workspace` 目录下的文件（.gitignore 文件会排除敏感文件）  
- 配置自动备份功能  
- 测试备份系统  
- 显示最终状态  

**使用场景：**  
- 首次设置备份系统时  
- 安装完该技能后  
- 运行 `checkpoint-reset` 之后  
- 新用户的首选设置步骤

### checkpoint-auth
**通过 GitHub 进行身份验证（基于浏览器）。**

```bash
checkpoint-auth
```

**功能：**  
- 选项 1：使用 GitHub CLI（自动打开浏览器）  
- 选项 2：使用个人访问令牌（令牌有有效期，需定期更新）  
- 选项 3：使用 SSH 密钥（推荐，令牌无需担心过期）  
- 自动将 GitHub 添加到 `known_hosts` 文件中  
- 设置完成后测试认证是否成功  

**使用场景：**  
- 认证信息过期或认证失败时  
- 需要切换认证方式时  
- 在新机器上设置备份系统时  

**推荐使用 SSH 认证的原因：**  
- 无需担心令牌过期问题  
- 无需输入密码即可可靠地完成认证  
- GitHub 已不再支持 HTTPS 的密码认证方式  

### checkpoint-backup
将当前状态备份到远程仓库。  

```bash
checkpoint-backup
```

**功能：**  
- 将 OpenClaw 的定时任务备份到 `memory/cron-jobs-backup.json` 文件中（需要 `openclaw` CLI 和运行中的代理服务）  
- 提交 `~/.openclaw/workspace` 目录下的所有更改  
- 将备份内容推送到远程仓库（origin/main 分支）  
- 显示提交哈希值和时间戳  

**关于定时任务备份的详细信息：**  
- 运行 `openclaw cron list --json` 命令导出所有定时任务  
- 仅保留配置信息（任务名称、调度时间、目标地址、执行内容）  
- 非阻塞式操作：即使 CLI 或代理服务不可用，备份仍会继续进行  

**使用场景：**  
- 在更换电脑之前  
- 进行重大更改后（如更换内存或更新 SOUL.md 文件）  
- 需要确保更改已保存时  

### checkpoint-schedule
设置可配置频率的自动备份任务。  

```bash
checkpoint-schedule 15min      # Every 15 minutes
checkpoint-schedule 30min      # Every 30 minutes
checkpoint-schedule hourly     # Every hour (default)
checkpoint-schedule 2hours     # Every 2 hours
checkpoint-schedule 4hours     # Every 4 hours
checkpoint-schedule daily      # Once per day at 9am
checkpoint-schedule disable    # Turn off auto-backup
```

**功能：**  
- 在 macOS 上：创建 launchd plist 文件以实现可靠的后台备份  
- 在 Linux 上：添加定时任务以实现自动备份  
- 将所有操作记录到 `~/.openclaw/logs/checkpoint.log` 文件中  

**使用场景：**  
- 首次设置时：使用 `checkpoint-schedule hourly`  
- 更改备份频率：使用 `checkpoint-schedule 15min`  
- 停止备份：使用 `checkpoint-schedule disable`  

### checkpoint-status
检查备份的状态和健康状况。  

```bash
checkpoint-status
```

**显示内容：**  
- 最后一次备份时间和提交信息  
- 本地备份是否与远程备份同步  
- 未提交的更改  
- 自动备份的调度状态  
- 最近的备份操作记录  

**使用场景：**  
- 在更换电脑之前（验证备份是否已同步）  
- 解决备份问题时  
- 定期检查备份状态时  

### checkpoint-restore
从远程仓库恢复数据，并提供交互式恢复引导流程。  

```bash
checkpoint-restore            # Select from recent checkpoints (interactive)
checkpoint-restore --latest   # Restore most recent checkpoint (skip selection)
checkpoint-restore --force    # Discard local changes before restoring
```

**功能：**  
- **首次使用用户：** 启动交互式恢复引导流程  
  - 指导您完成 GitHub 认证（通过 SSH、GitHub CLI 或个人访问令牌）  
  - 允许您指定备份仓库  
  - 验证访问权限并恢复备份数据  
  - 处理本地文件与备份文件之间的冲突（如果存在）  
  - 显示可选择的备份版本（如果仓库有多个版本）  
  - 提供从备份中恢复定时任务的选项  
- **已恢复用户：** 显示最近 10 个备份版本供您选择  
  - 可选择最新的或之前的备份版本  
  - 当前备份版本会在列表中标记出来  
  - 恢复较旧的备份版本时会提示会覆盖最新的远程备份  
  - 可使用 `--latest` 标志跳过交互式选择，直接恢复最新的备份版本  
- **未提交的更改：** 如果有未提交的更改，系统会提示您：  
    1. 先保存更改（运行 `checkpoint-backup`）  
    2. 放弃本地更改并继续恢复  
    3. 取消操作  
- **定时任务：** 恢复完成后会自动尝试从 `memory/cron-jobs-backup.json` 文件中恢复定时任务（需要 OpenClaw 代理服务运行）  

**使用场景：**  
- 在新机器上启动 OpenClaw 时  
- 发生硬件故障或灾难时  
- 在不同电脑上恢复工作时  
- 从现有备份中恢复数据时  
- 需要回滚到之前的备份版本时  

**触发引导流程的情况：**  
- 本地没有工作区文件  
- 存在工作区文件但未配置 Git 仓库  
- 配置了 Git 仓库但未配置远程仓库  

### checkpoint-init
初始化工作区以启用备份系统。  

```bash
checkpoint-init
```

**功能：**  
- 在 `~/.openclaw/workspace` 目录下创建 Git 仓库  
- 生成 `.gitignore` 文件（排除敏感文件）  
- 执行初始提交  

**使用场景：**  
- 首次设置备份系统时  
- 从备份恢复到新机器后  

### checkpoint-reset
重置备份系统以进行全新设置。  

```bash
checkpoint-reset
```

**功能：**  
- 选项 1：仅删除本地的 Git 仓库（保留 SSH 密钥）  
- 选项 2：删除所有内容（Git 仓库、SSH 密钥及 GitHub 的 `known_hosts` 配置）  
- 提醒您手动删除 GitHub 仓库  

**使用场景：**  
- 需要重新开始全新设置时  
- 更换到不同的 GitHub 仓库时  
- 解决持续的认证问题时  

### checkpoint-stop
停止自动备份功能。  

```bash
checkpoint-stop
```

**功能：**  
- 禁用自动备份功能  
- 删除 Linux 系统中的定时任务  
- 在 macOS 系统中删除 launchd 代理服务  

**使用场景：**  
- 需要暂时暂停备份时  
- 在进行重大工作区更改之前  
- 如果备份功能引发问题时  

**重新启用备份的方法：**  
运行 `checkpoint-schedule hourly`（或其他指定的频率）

## 简化设置（推荐）

只需运行交互式向导即可完成所有设置：  

```bash
checkpoint-setup
```

该向导会自动处理 git 初始化、SSH 密钥配置、GitHub 账户设置及首次备份等操作。

### 首次手动设置  

```bash
# 1. Initialize checkpoint system
checkpoint-init

# 2. Create PRIVATE GitHub repository
# Go to https://github.com/new
# Name: openclaw-state
# ⚠️  Visibility: PRIVATE (important - contains your personal data!)

# 3. Add remote (use SSH, not HTTPS)
cd ~/.openclaw/workspace
git remote add origin git@github.com:YOURUSER/openclaw-state.git
checkpoint-backup
```

### 在第二台机器上设置备份  

**选项 1：交互式恢复（推荐）**

```bash
# Install the checkpoint skill first
curl -fsSL https://raw.githubusercontent.com/AnthonyFrancis/openclaw-checkpoint/main/scripts/install-openclaw-checkpoint.sh | bash

# Run checkpoint-restore - it will guide you through the entire process
checkpoint-restore
```

**功能：**  
- 帮助您完成 GitHub 认证（如果尚未完成）  
- 获取您的备份仓库信息  
- 自动克隆或恢复备份数据  

**选项 2：手动克隆备份**

```bash
# 1. Clone repository (use SSH)
git clone git@github.com:YOURUSER/openclaw-state.git ~/.openclaw/workspace

# 2. Restore secrets from 1Password/password manager
# Create ~/.openclaw/workspace/.env.thisweek
# Create ~/.openclaw/workspace/.env.stripe
# (Copy from secure storage)

# 3. Start OpenClaw
openclaw gateway start
```

## 自动备份设置（推荐）

```bash
# Enable hourly backups
checkpoint-schedule hourly

# Or choose your frequency:
checkpoint-schedule 15min   # Every 15 minutes - high activity
checkpoint-schedule 30min   # Every 30 minutes - medium activity  
checkpoint-schedule 2hours  # Every 2 hours - low activity
checkpoint-schedule daily   # Once per day - minimal activity
```

### 检查备份状态  

```bash
checkpoint-status
```

**显示内容：**  
- 最后一次备份时间  
- 是否与远程仓库同步  
- 自动备份的调度信息  
- 最近的备份操作记录  

### 手动设置定时任务（高级选项）**

如果您希望手动配置定时任务：  

```bash
# Edit crontab
crontab -e

# Add line for hourly backups:
0 * * * * /Users/$(whoami)/.openclaw/workspace/skills/openclaw-checkpoint/scripts/checkpoint-backup >> ~/.openclaw/logs/checkpoint.log 2>&1
```

## 灾难恢复流程  

**场景：** 主服务器损坏  

```bash
# On new machine:

# 1. Install OpenClaw
brew install openclaw  # or your install method

# 2. Install checkpoint skill and run interactive restore
curl -fsSL https://raw.githubusercontent.com/AnthonyFrancis/openclaw-checkpoint/main/scripts/install-openclaw-checkpoint.sh | bash
checkpoint-restore
# Follow the interactive prompts to:
# - Authenticate with GitHub
# - Enter your backup repository (e.g., YOURUSER/openclaw-state)
# - Restore your checkpoint

# 3. Restore secrets from 1Password (API keys are not backed up for security)
cat > ~/.openclaw/workspace/.env.thisweek << 'EOF'
THISWEEK_API_KEY=your_key_here
EOF

# 4. Start OpenClaw
openclaw gateway start

# 5. Cron jobs are restored automatically during checkpoint-restore
# (if the gateway is running and cron backup exists)

# 6. Enable automatic backups on this machine
checkpoint-schedule hourly

# 7. Verify
# Ask assistant: "What were we working on?"
# Should recall everything up to last checkpoint, with all scheduled tasks restored
```

## 安全注意事项  

### ⚠️ 重要提示：** 仓库必须设置为私有模式  

您的备份文件包含敏感的个人数据：  
- SOUL.md、MEMORY.md（您的身份信息和对话记录）  
- 自定义脚本和配置设置  

**如果仓库设置为公共模式，任何人都可以查看您的数据！**  

**备份的内容包括：**  
- ✅ 内存文件（对话记录）  
- ✅ 身份文件（SOUL.md 等）  
- ✅ 定时任务（memory/cron-jobs-backup.json）  
- ✅ 自定义脚本和工具  
- ✅ 配置设置  

**不备份的内容包括：**  
- ❌ API 密钥（.env.* 文件）——请将其保存在 1Password 等密码管理工具中  
- ❌ OAuth 令牌——请在新机器上重新进行认证  
- ❌ 下载的媒体文件——属于临时文件  
- ❌ 临时文件——同样属于临时文件  

**最佳实践：**  
- **始终使用私有仓库**  
- 使用 SSH 认证（避免令牌过期问题）  
- 将 API 密钥存储在密码管理工具中，而非备份文件中  
- 为 GitHub 账户启用双重身份验证  
- 在将文件添加到内存之前考虑对其进行加密  

## 权限和调度设置  

该技能使用系统的默认调度功能来自动执行备份：  
- **macOS：** 在 `~/Library/LaunchAgents/com.openclaw.checkpoint.plist` 文件中创建 launchd plist 文件  
- **Linux：** 添加用户级别的定时任务（可通过 `crontab -l` 查看）  

自动备份功能是**可选的**——除非您明确运行 `checkpoint-schedule`，否则默认不会启用。您可以通过 `checkpoint-stop` 或 `checkpoint-schedule disable` 随时禁用该功能。  

该技能不会安装任何后台守护进程、系统服务或 root 级别的进程。所有备份操作都在您的用户账户下执行。  

**文件访问范围：** 该技能仅读取和写入 `~/.openclaw/workspace` 目录内的文件，不会访问其他文件。敏感文件（.env.*、凭证信息、OAuth 令牌）会通过 `.gitignore` 文件被排除在备份范围之外。  

## 常见问题解决方法：**

- **提示“不是 Git 仓库”或“'origin' 似乎不是 Git 仓库”**  
  运行 `checkpoint-restore` 会自动启动交互式恢复引导流程，帮助您连接到备份仓库。或者，您可以运行 `checkpoint-setup` 从头开始创建新的备份。  

- **提示“无法推送备份”**  
  可能是因为其他机器已经进行了备份操作。请先运行 `checkpoint-restore`，然后再运行 `checkpoint-backup`。  

- **提示“有未提交的更改”**  
  `checkpoint-restore` 会提示您选择：  
    1. 先保存更改（运行 `checkpoint-backup`）  
    2. 放弃本地更改并继续恢复  
    3. 取消操作  
  您也可以使用 `checkpoint-restore --force` 直接忽略这些提示并继续恢复。  

- **恢复后显示“本地数据落后于远程数据”**  
  这可能是由于其他机器在您上次同步后进行了备份。  

- **GitHub 提示输入用户名/密码**  
  GitHub 已不再支持 HTTPS 的密码认证方式，请切换为 SSH 认证：  

```bash
cd ~/.openclaw/workspace
git remote set-url origin git@github.com:YOURUSER/REPO.git
```  

- **提示“主机密钥验证失败”**  
  请检查您的 `known_hosts` 文件中是否包含 GitHub 的 SSH 密钥。  

- **提示“权限被拒绝（公钥问题）**  
  请确保您的 SSH 密钥已添加到 GitHub。运行 `checkpoint-auth` 并选择 SSH 认证方式。  

- **设置完成后 GitHub 仓库为空**  
  这是因为旧的 `checkpoint-init` 命令仅创建了 `.gitignore` 文件。请运行以下命令进行修复：  

```bash
cd ~/.openclaw/workspace && git add -A && git commit -m "Full backup" && git push
```  

## 限制事项：**  
- **一次只能在一台机器上使用该技能**  
- **最大数据丢失量**：使用每小时备份的情况下，最多丢失 1 小时的数据  
- **敏感文件未同步**：在新机器上需要手动重新设置 API 密钥  
- **大文件限制**：GitHub 对文件大小有限制（通常文本文件不受影响，但请注意文件大小）  

## 更多信息：**  
详细设置说明请参考 [references/setup.md](references/setup.md)。