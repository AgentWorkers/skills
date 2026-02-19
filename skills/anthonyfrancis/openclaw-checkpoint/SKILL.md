---
name: openclaw-checkpoint
description: 使用 Git 在多台机器之间备份和恢复 OpenClaw 工作区状态及代理程序。通过将 `SOUL.md`、`MEMORY.md`、内存文件、Cron 作业、代理程序（位于 `~/openclaw/agents/` 目录下）以及配置文件同步到远程仓库，实现灾难恢复功能。当用户需要保存 OpenClaw 的当前状态、在新机器上恢复数据、在不同计算机之间迁移数据或防止数据丢失时，可以使用此功能。提供的命令包括：`checkpoint`（帮助信息）、`checkpoint-setup`（交互式设置）、`checkpoint-backup`（备份）、`checkpoint-restore`（可选择特定备份或使用 `--latest` 恢复最新状态）、`checkpoint-schedule`（自动备份）、`checkpoint-stop`、`checkpoint-status`、`checkpoint-init` 和 `checkpoint-reset`。支持使用 `--workspace-only`、`--agents-only` 或 `--agent <name>` 标志进行针对特定部分的备份。每次执行 `checkpoint-backup` 命令时，Cron 作业会自动备份到 `memory/cron-jobs-backup.json` 文件中。
---
# OpenClaw 备份与恢复功能

该功能可帮助您在多台机器之间备份和恢复 OpenClaw 的身份信息、内存数据、代理程序以及配置设置。

**支持平台：** 仅支持 macOS 和 Linux。Windows 不受支持。

## 概述

通过将您的工作区和代理程序同步到 Git 仓库，该功能实现了 OpenClaw 的灾难恢复功能。它备份以下内容：

- **身份信息**：SOUL.md、IDENTITY.md、USER.md（您的身份和助手信息）
- **内存数据**：MEMORY.md 及所有内存相关的.md 文件（对话记录和上下文）
- **定时任务**：导出到 memory/cron-jobs-backup.json 的定时任务（每日同步、自动化操作等）
- **配置设置**：TOOLS.md、AGENTS.md、HEARTBEAT.md（工具配置和规范）
- **自定义脚本**：您编写的所有自定义脚本和自动化脚本
- **代理程序**：位于 ~/.openclaw/agents/ 目录下的所有代理程序文件夹

**不备份的内容（出于安全考虑）：** API 密钥（.env.* 文件）、凭据信息、OAuth 令牌

## 安装

### 方式 1：Git 克隆（推荐）

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

### 方式 2：快速安装

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
- 显示所有备份命令的快速参考信息，包括描述和示例

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
- 检测 ~/.openclaw/agents/ 目录下的代理程序，并提示它们将被包含在备份中
- 生成包含恢复说明和命令的 README.md 文件
- 提交 ~/.openclaw/workspace 目录下的文件（.gitignore 文件会排除敏感文件）
- 配置自动备份
- 测试备份系统
- 显示最终状态

**使用场景：**
- 首次设置备份系统时
- 在运行 checkpoint-reset 之后
- 新用户使用的推荐起点

### checkpoint-auth
**使用 GitHub 进行认证（基于浏览器）。**

```bash
checkpoint-auth
```

**功能：**
- 选项 1：使用 GitHub CLI（自动打开浏览器）
- 选项 2：使用个人访问令牌（令牌有有效期，需要定期更新）
- 选项 3：使用 SSH 密钥（推荐，令牌无需更新）
- 自动将 GitHub 添加到 known_hosts 文件中
- 设置完成后测试认证是否成功

**使用场景：**
- 认证过期或失败时
- 需要切换认证方式时
- 在新机器上设置备份时

**建议使用 SSH 认证，因为：**
- 无需担心令牌过期问题
- 无需输入密码即可可靠地完成认证
- GitHub 已不再支持 HTTPS 的密码认证方式

### checkpoint-backup
将当前状态备份到远程仓库。

```bash
checkpoint-backup                     # Backup workspace + all agents
checkpoint-backup --workspace-only    # Backup workspace only (skip agents)
checkpoint-backup --agents-only       # Backup agents only (skip workspace/cron)
checkpoint-backup --agent alex        # Backup only the 'alex' agent (+ workspace)
```

**功能：**
- 将 OpenClaw 的定时任务备份到 memory/cron-jobs-backup.json 文件中（需要 openclaw CLI 和正在运行的 gateway）
- 将 ~/.openclaw/agents/ 目录下的代理程序文件夹复制到工作区仓库的 agents/ 目录中（删除嵌套的 `.git` 目录）
- 优化路径（将 `$HOME` 替换为 `{{HOME}}` 以实现跨机器移植）
- 提交 ~/.openclaw/workspace 中的所有更改
- 将更改推送到 origin/main 分支
- 显示提交哈希值和时间戳

**代理程序备份详情：**
- 自动检测 ~/.openclaw/agents/ 目录下的代理程序（例如 alex、blake 等）
- 每个代理程序文件夹会被复制到备份仓库的 agents/<name>/ 目录中
- 删除嵌套的 `.git` 目录以避免子模块问题
- 如果没有代理程序，会显示提示信息并跳过备份

**定时任务备份详情：**
- 运行 openclaw cron list --json 命令导出所有定时任务
- 仅保留配置信息（任务名称、调度时间、目标地址、数据内容）
- 非阻塞式操作：如果 CLI 或 gateway 不可用，备份仍会继续进行

**可选参数：**
- `--workspace-only` — 仅备份工作区数据，不备份代理程序
- `--agents-only` — 仅备份代理程序，不备份工作区数据
- `--agent <name>` — 仅备份指定的代理程序

**使用场景：**
- 在更换电脑之前
- 在进行重大更改后（如更新 SOUL.md 文件）
- 任何需要确保更改被保存的情况下

### checkpoint-schedule
设置可配置的自动备份频率。

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
- 在 macOS 上创建 launchd plist 以实现可靠的后台备份
- 在 Linux 上添加定时任务以实现定期备份
- 将所有操作记录到 ~/.openclaw/logs/checkpoint.log 文件中

**使用场景：**
- 首次设置备份系统时：使用 checkpoint-schedule hourly
- 更改备份频率：使用 checkpoint-schedule 15min
- 停止备份：使用 checkpoint-schedule disable

### checkpoint-status
检查备份的状态和健康情况。

```bash
checkpoint-status
```

**显示内容：**
- 最后一次备份时间和提交信息
- 本地数据是否与远程数据一致
- 未提交的更改
- 代理程序的备份状态（哪些代理程序已备份，哪些未备份）
- 自动备份的调度状态
- 最近的备份操作记录

**使用场景：**
- 在更换机器之前（验证数据是否已同步）
- 解决备份问题时
- 定期检查备份状态

### checkpoint-restore
从远程仓库恢复数据，并提供交互式恢复引导流程。

```bash
checkpoint-restore                    # Select from recent checkpoints (interactive)
checkpoint-restore --latest           # Restore most recent checkpoint (skip selection)
checkpoint-restore --force            # Discard local changes before restoring
checkpoint-restore --workspace-only   # Restore workspace only (skip agents)
checkpoint-restore --agents-only      # Restore agents only (skip workspace/cron)
checkpoint-restore --agent alex       # Restore only the 'alex' agent
```

**功能：**
- **首次使用用户：** 启动交互式恢复引导流程
  - 指导您完成 GitHub 认证（SSH、GitHub CLI 或个人访问令牌）
  - 允许您指定备份仓库
  - 验证访问权限并恢复备份数据
  - 处理本地文件与备份数据之间的合并/替换问题
  - 显示可选择的备份版本（如果仓库有多个提交记录）
  - 提供从备份中恢复定时任务的选项
  - 提供从备份中恢复代理程序的选项
- **返回使用的用户：** 显示最近 10 个备份版本供您选择
  - 选择最新的或任意一个旧版本进行恢复
  - 当前备份版本会在列表中高亮显示
  - 恢复旧版本时，系统会提示下次备份会覆盖最新版本
- **如果有未提交的更改：** 系统会提示您：
    1. 先保存更改（运行 checkpoint-backup）
    2. 放弃本地更改并继续恢复
    3. 取消操作

**路径处理：**
- 自动扩展 `{{HOME}}` 占位符，并根据当前机器路径重新生成文件路径
- **定时任务：** 恢复完成后，系统会自动尝试从 memory/cron-jobs-backup.json 文件中恢复定时任务（需要 OpenClaw gateway 运行）

**可选参数：**
- `--latest` — 直接恢复最新版本
- `--force` — 强制忽略本地更改并直接恢复
- `--workspace-only` — 仅备份工作区数据，不备份代理程序
- `--agents-only` — 仅备份代理程序，不备份工作区数据
- `--agent <name>` — 仅备份指定的代理程序

**使用场景：**
- 在新机器上启动 OpenClaw 时
- 在发生硬件故障或灾难后
- 在不同机器上恢复工作时
- 从现有备份中恢复数据时

**引导流程触发条件：**
- 本地没有工作区目录时
- 存在工作区目录但没有 Git 仓库时
- 存在 Git 仓库但没有配置远程仓库时

### checkpoint-init
初始化工作区的备份系统。

```bash
checkpoint-init
```

**功能：**
- 在 ~/.openclaw/workspace 目录下创建 Git 仓库
- 生成 .gitignore 文件（排除敏感文件和临时文件）
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
- 选项 1：仅删除本地 Git 仓库（保留 SSH 密钥）
- 选项 2：删除所有内容（Git 仓库、SSH 密钥以及 known_hosts 文件中的 GitHub 信息）
- 提示您手动删除工作区 agents/ 目录下的备份文件

**注意：** 重置操作不会影响 ~/.openclaw/agents/ 目录下的代理程序文件夹——仅删除备份文件。

**使用场景：**
- 重新开始全新设置时
- 更换到不同的 GitHub 仓库时
- 解决持续的认证问题时

### checkpoint-stop
停止自动备份。

```bash
checkpoint-stop
```

**功能：**
- 禁用自动备份功能
- 删除定时任务（Linux）或 launchd 代理程序（macOS）

**使用场景：**
- 暂时暂停备份
- 在进行重大工作区更改之前
- 如果备份导致问题时

**重新启用备份的方法：** 使用 checkpoint-schedule hourly（或任意频率）

## 设置流程

### 简单设置（推荐）

只需运行交互式向导即可：

```bash
checkpoint-setup
```

该向导会完成所有设置：创建 Git 仓库、配置 SSH 密钥、设置 GitHub 账户以及首次备份。

### 首次设置（手动操作）

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

### 在第二台机器上设置

**选项 1：交互式恢复（推荐）**

```bash
# Install the checkpoint skill first
curl -fsSL https://raw.githubusercontent.com/AnthonyFrancis/openclaw-checkpoint/main/scripts/install-openclaw-checkpoint.sh | bash

# Run checkpoint-restore - it will guide you through the entire process
checkpoint-restore
```

**操作步骤：**
- 帮助您完成 GitHub 认证（如果尚未完成）
- 获取您的备份仓库信息
- 自动克隆/恢复备份数据

**选项 2：手动克隆**

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
- 是否与远程数据同步
- 自动备份的调度设置
- 最近的备份操作记录

## 多代理程序备份

备份系统会自动检测并备份 ~/.openclaw/agents/ 目录下的所有代理程序。

### 工作原理：

- **备份时：** 将 ~/.openclaw/agents/ 目录下的代理程序文件夹复制到备份仓库的 agents/ 目录中（删除嵌套的 `.git` 目录）
- **恢复时：** 将备份仓库 agents/ 目录下的代理程序文件夹复制回 ~/.openclaw/agents/ 目录
- 如果没有代理程序，所有操作都会正常跳过代理程序的备份

### 备份仓库的文件结构

```
~/.openclaw/workspace/          (backup repo root)
  SOUL.md
  MEMORY.md
  memory/
  agents/                       (auto-created when agents exist)
    alex/                       (copied from ~/.openclaw/agents/alex/)
    blake/                      (copied from ~/.openclaw/agents/blake/)
```

### 代理程序相关参数

这些参数适用于 checkpoint-backup 和 checkpoint-restore 命令：

| 参数 | 描述 |
|------|-------------|
| `--workspace-only` | 仅备份工作区数据，不备份代理程序 |
| `--agents-only` | 仅备份代理程序，不备份工作区数据 |
| `--agent <name>` | 仅备份指定的代理程序 |

### 示例

```bash
# Backup everything (default)
checkpoint-backup

# Backup only agents
checkpoint-backup --agents-only

# Backup only the 'alex' agent
checkpoint-backup --agent alex

# Restore workspace but skip agents
checkpoint-restore --latest --workspace-only

# Restore only agents from backup
checkpoint-restore --agents-only

# Check which agents are backed up
checkpoint-status
```

### 向后兼容性

- 如果 ~/.openclaw/agents/ 目录不存在或为空，所有操作都会正常跳过代理程序的备份
- 旧版本的备份仓库中如果没有 agents/ 目录，恢复操作也会正常进行

## 跨机器移植性

当您在一台机器（例如 `/Users/jerry`）上备份数据，然后在另一台机器（例如 `/Users/tom`）上恢复数据时，工作区文件中的硬编码路径可能会导致问题。备份系统会自动处理这些问题。

**工作原理：**
- **备份时：** 所有 `$HOME` 路径（例如 `/Users/jerry`）会被替换为 `{{HOME}}` 占位符。同时会生成一个 `.checkpoint-meta.json` 文件，记录源机器的信息。
- **恢复时：** `{{HOME}}` 占位符会被替换为当前机器的 `$HOME` 路径（例如 `/Users/tom`）。对于旧版本的备份文件，系统会保留原有的路径。

### 处理的文件类型

系统仅扫描可能包含路径的文本文件：
- `.md`、`.json`、`.sh`、`.txt`、`.yaml`、`.yml`、`.toml`、`.cfg`、`.conf`

二进制文件、`.git/` 目录以及 `node_modules/` 目录不会被备份。

### .checkpoint-meta.json

该文件在每次备份时自动生成，用于记录源机器的信息：

```json
{
  "source_home": "/Users/jerry",
  "source_user": "jerry",
  "hostname": "Jerrys-MacBook-Pro"
}
```

恢复时，该文件会告诉脚本需要替换哪些旧路径。恢复完成后，文件会更新以反映当前机器的路径。

### 手动配置定时任务（高级操作）

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

### ⚠️ 重要提示：** 仓库必须设置为私有（PRIVATE）

您的备份文件包含敏感的个人数据：
- SOUL.md、MEMORY.md（您的身份信息和对话记录）
- 自定义脚本和配置设置

**如果仓库设置为公共（PUBLIC），任何人都可以查看您的数据！**

**备份的内容：**
- ✅ 内存文件（对话记录）
- ✅ 身份文件（SOUL.md 等）
- ✅ 定时任务（memory/cron-jobs-backup.json）
- ✅ 脚本和工具
- ✅ 配置设置
- ✅ 代理程序（从 ~/.openclaw/agents/ 复制到备份仓库的 agents/ 目录）

**不备份的内容：**
- ❌ API 密钥（.env.* 文件）——请将其保存在 1Password 中
- ❌ OAuth 令牌——请在新机器上重新认证
- ❌ 下载的媒体文件——属于临时文件
- ❌ 临时文件——不会被备份

**最佳实践：**
- **始终使用私有仓库**
- 使用 SSH 认证（避免使用令牌）
- 将 API 密钥存储在密码管理器中，不要包含在备份文件中
- 在 GitHub 账户上启用 2FA 功能
- 在将文件添加到内存之前，考虑对其进行加密

## 权限和调度设置

该功能使用系统的默认调度机制来自动执行备份：
- **macOS：** 在 ~/Library/LaunchAgents/com.openclaw.checkpoint.plist 中创建 launchd plist
- **Linux：** 添加用户级别的定时任务（可通过 crontab -l 查看）

自动备份功能是**可选的**——除非您明确运行 checkpoint-schedule，否则默认不会启用。您可以使用 checkpoint-stop 或 checkpoint-schedule disable 来随时禁用该功能。

该功能不会安装任何后台守护进程、系统服务或 root 权限的进程。所有备份操作都在您的用户账户下执行。

**文件访问权限：** 该功能会读取 ~/.openclaw/workspace 和 ~/.openclaw/agents/ 目录中的文件，并将代理程序的备份文件保存到 ~/.openclaw/workspace/agents/ 目录。恢复时，会将代理程序复制回 ~/.openclaw/agents/ 目录。敏感文件（.env*、凭据信息、OAuth 令牌）会通过 .gitignore 文件被排除在备份范围之外。

## 常见问题及解决方法

### “没有 Git 仓库” 或 “'origin' 不是 Git 仓库”
运行 checkpoint-restore 时会自动启动交互式恢复引导流程。或者，您可以运行 checkpoint-setup 来从头开始创建新的备份。

### “无法推送备份”
可能是其他机器先进行了数据更新。请先运行 checkpoint-restore，然后再运行 checkpoint-backup。

### “有未提交的更改”
运行 checkpoint-restore 时会提示您选择：
1. 先保存更改（运行 checkpoint-backup）
2. 放弃本地更改并继续恢复
3. 取消操作

您也可以使用 checkpoint-restore --force 来直接忽略未提交的更改。

### 恢复后显示 “远程仓库不可用”
这可能是由于其他机器在您上次同步后进行了数据更新。

### GitHub 要求输入用户名/密码
GitHub 已不再支持 HTTPS 的密码认证方式。请切换到 SSH 认证：

```bash
cd ~/.openclaw/workspace
git remote set-url origin git@github.com:YOURUSER/REPO.git
```

### “主机密钥验证失败”
可能是 GitHub 的 SSH 主机密钥不在您的 known_hosts 文件中。请按照以下步骤解决：

```bash
ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts
```

### “权限被拒绝（Permission denied (publickey)”
您的 SSH 密钥未添加到 GitHub。请运行 checkpoint-auth 并选择 SSH 认证方式。

### 设置完成后仓库为空
旧的 checkpoint-init 命令仅会提交 .gitignore 文件。现在这个问题已得到解决。请运行：

```bash
cd ~/.openclaw/workspace && git add -A && git commit -m "Full backup" && git push
```

### 重新开始设置
运行 checkpoint-reset 以删除本地的 Git 仓库和 SSH 密钥（如需要），然后运行 checkpoint-setup。

### 代理程序未备份
请确认您的代理程序位于 ~/.openclaw/agents/ 目录下。运行 checkpoint-status 以查看哪些代理程序已被备份。确保没有使用 `--workspace-only` 参数。

### 代理程序备份失败
请检查您的代理程序是否位于 ~/.openclaw/agents/ 目录下。运行 checkpoint-status 以确认哪些代理程序已被备份。确保没有使用 `--workspace-only` 参数。

### 代理程序备份失败（包含嵌套的 `.git` 目录）
备份过程会自动删除代理程序备份文件中的 `.git` 目录。如果遇到问题，请重新运行 checkpoint-backup：

```bash
rm -rf ~/.openclaw/workspace/agents
checkpoint-backup
```

### 恢复后文件缺失
恢复操作会原样复制代理程序文件。如果备份是在某些文件添加到代理程序之后进行的，这些文件可能不会被备份到新的备份文件中。请先在源机器上运行 checkpoint-backup 以获取最新状态。

### 恢复后出现 “权限被拒绝（Permission denied, mkdir '/Users/olduser'）”
这可能是由于源机器的路径设置与目标机器不同。如果备份是在路径规范化之前创建的，请运行：

```bash
cd ~/.openclaw/workspace
grep -rl "/Users/olduser" --include="*.md" --include="*.json" --include="*.sh" | \
  xargs sed -i '' "s|/Users/olduser|$HOME|g"
```

### 文件显示错误的路径（例如 {{HOME}}）
这是正常的，因为 GitHub 仓库中的路径是占位符。在恢复后，系统会自动将路径替换为实际的路径。如果在恢复后仍然看到 {{HOME}}，请再次运行 checkpoint-restore --latest。

## 限制条件

- **一次只能在一台机器上使用该功能**：不要同时在多台机器上运行 OpenClaw
- **最大数据丢失量**：使用每小时备份策略时，最多丢失 1 小时的数据
- **敏感文件无法自动备份**：API 密钥需要手动在新机器上重新设置
- **大文件限制**：GitHub 对文件大小有限制（通常为 100MB，文本文件通常不受影响）

## 更详细的设置说明，请参阅 [references/setup.md](references/setup.md)。