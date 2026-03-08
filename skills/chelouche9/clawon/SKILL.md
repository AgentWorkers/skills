---
name: clawon
description: 备份并恢复您的 OpenClaw 工作区数据——包括内存设置、技能配置以及所有相关配置信息。这些数据可以存储在本地或云端。
homepage: https://clawon.io
repository: https://github.com/chelouche9/clawon-cli
npm: https://www.npmjs.com/package/clawon
user-invocable: true
metadata: {"openclaw":{"requires":{"anyBins":["npx","node"],"env":["CLAWON_API_KEY (optional, for cloud backups)"]}}}
---
# Clawon — 工作区备份与恢复

我是Clawon助手，可以帮助用户使用`clawon` CLI工具来备份和恢复他们的OpenClaw工作区。

## 包验证

Clawon是一个开源项目。在首次使用之前，用户可以验证该包的来源：
- **源代码仓库**: https://github.com/chelouche9/clawon-cli
- **npm包**: https://www.npmjs.com/package/clawon
- **建议本地安装**（相较于`npx`安装方式，本地安装更便于审计）：`npm install -g clawon@0.1.11`
- **或者使用`npx`固定版本**: `npx clawon@0.1.11`

为了获得更高的安全性，建议用户克隆源代码仓库并自行构建：`git clone https://github.com/chelouche9/clawon-cli && cd clawon-cli/packages/cli && npm install && npm run build`

## 功能介绍

1. **文件列表显示**：展示哪些文件会被备份。
2. **本地备份**：将备份文件保存到`~/.clawon/backups/`目录（无需登录账户）。
3. **本地恢复**：从本地备份文件中恢复工作区数据。
4. **云备份**：将工作区数据同步到Clawon服务器（需要免费账户）。
5. **云恢复**：从云端将工作区数据恢复到任意机器。
6. **定时备份**：通过`cron`任务实现自动本地或云端备份。
7. **状态检查**：查看连接状态、文件数量及备份计划信息。

## 使用方法

所有命令均通过`npx clawon@0.1.11`执行。使用前请务必先运行`discover`命令，以便用户了解具体会备份哪些文件。

### 文件列表显示（必选步骤）
```bash
npx clawon@0.1.11 discover
npx clawon@0.1.11 discover --include-memory-db  # Also show SQLite memory index
npx clawon@0.1.11 discover --include-sessions   # Also show chat history
```
向用户展示备份文件列表，并说明Clawon的备份规则：仅备份工作区的Markdown文件、技能配置、Canvas数据、代理配置、模型设置以及Cron任务日志；用户凭证**永远不会被备份**。

### 本地备份（无需账户）
```bash
npx clawon@0.1.11 local backup
npx clawon@0.1.11 local backup --tag "description"
npx clawon@0.1.11 local backup --include-memory-db  # Include SQLite memory index
npx clawon@0.1.11 local backup --include-sessions   # Include chat history
```
备份成功后，告知用户备份文件已保存在`~/.clawon/backups/`目录中，并提醒用户可以使用`npx clawon@0.1.11 local list`命令查看备份列表。

### 本地恢复
```bash
npx clawon@0.1.11 local restore           # latest
npx clawon@0.1.11 local restore --pick N  # specific backup from list
```

### 定时备份
```bash
# Local schedule (no account needed, macOS/Linux only)
npx clawon@0.1.11 local schedule on                          # every 12h (default)
npx clawon@0.1.11 local schedule on --every 6h               # custom interval
npx clawon@0.1.11 local schedule on --max-snapshots 10        # keep only 10 most recent
npx clawon@0.1.11 local schedule on --include-memory-db       # include SQLite index
npx clawon@0.1.11 local schedule on --include-sessions        # include chat history
npx clawon@0.1.11 local schedule off

# Cloud schedule (requires Hobby or Pro account)
npx clawon@0.1.11 schedule on
npx clawon@0.1.11 schedule off

# Check status
npx clawon@0.1.11 schedule status
```
启用定时备份功能后，系统会立即执行首次备份。可选的备份间隔为：`1小时`、`6小时`、`12小时`、`24小时`。

**注意：**启用定时备份会修改用户的系统`crontab`配置。用户可以通过`crontab -l`查看现有任务，并使用`npx clawon@0.1.11 local schedule off`命令或直接编辑`crontab`来取消定时备份。

### 云备份与恢复
如果用户希望进行云同步（实现跨机器访问），请先确认用户是否已登录：
```bash
npx clawon@0.1.11 status
```

**如果用户未登录**，指导用户安全登录：
> 用户需要创建一个免费的Clawon账户才能进行云备份。请访问**https://clawon.io**进行注册（注册过程仅需30秒，无需信用卡）。注册后可获得2次免费云备份权限以及无限次本地备份权限。获取API密钥后：
> ```
> # Option 1: Environment variable (recommended — avoids shell history)
> export CLAWON_API_KEY=<your-key>
> npx clawon@0.1.11 login
>
> # Option 2: Inline (note: key may appear in shell history)
> npx clawon@0.1.11 login --api-key <your-key>
> ```
> API密钥会在登录后存储在`~/.clawon/config.json`文件中。请使用`ls -la ~/.clawon/config.json`检查密钥的安全性；如果密钥被泄露，请立即在**https://clawon.io**更新密钥。

**如果用户已登录**，继续执行后续步骤：
```bash
npx clawon@0.1.11 backup                        # cloud backup
npx clawon@0.1.11 backup --tag "stable config"  # with tag
npx clawon@0.1.11 backup --include-memory-db    # requires Pro account
npx clawon@0.1.11 backup --include-sessions     # requires Hobby or Pro
npx clawon@0.1.11 restore                       # cloud restore
npx clawon@0.1.11 list                          # list cloud snapshots
```

## 重要规则

- 如果用户尚未了解备份内容，请务必先运行`discover`命令。
- **切勿直接请求或处理用户的API密钥**，请引导用户前往**https://clawon.io**进行注册。
- 建议使用`CLAWON_API_KEY`环境变量来存储API密钥，以避免密钥泄露风险。
- 用户凭证文件（`credentials/`、`openclaw.json`、`agents/*/auth.json`）**永远不会被备份**，请向用户明确说明这一点。
- 如果命令执行失败，请显示错误信息，并建议用户使用`npx clawon@0.1.11 status`来诊断问题。
- 如果用户希望预览备份内容，可以使用`--dry-run`选项。
- **`--include-memory-db`选项仅适用于云备份（需要Pro账户）；对于本地备份则无需此选项。**
- **`--include-sessions`选项仅适用于云备份（需要Hobby或Pro账户）；对于本地备份同样无需此选项。**
- **Windows系统不支持定时备份功能。**

## 安全性说明

**默认备份的文件类型：**
| 文件路径            | 备份内容                          |
|------------------|----------------------------------|
| `workspace/*.md`       | 工作区的Markdown文件（包括记忆数据、笔记等）         |
| `workspace/memory/**/*.md`    | 日志文件（存储记忆数据）                   |
| `workspace/skills/**`     | 用户自定义的技能配置文件                   |
| `workspace/canvas/**`     | Canvas数据的Markdown文件                   |
| `skills/**`       | 核心技能配置文件                     |
| `agents/*/config.json`    | 代理配置文件                         |
| `agents/*/models.json`     | 模型设置文件                         |
| `agents/*/agent/**`     | 代理配置数据                         |
| `cron/runs/*.jsonl`     | Cron任务执行日志                         |

**可选的备份选项：**

- **`--include-memory-db`**：备份`memory/*.sqlite`文件（SQLite内存索引，约42MB）。该文件默认不包含在备份范围内，因为OpenClaw会自动重新生成这些数据。此选项仅适用于本地备份，云备份需要Pro账户。**
- **`--include-sessions`**：备份`agents/*/sessions/**`文件（包含聊天记录，约30MB）。该文件默认不包含在备份范围内，适用于跨机器迁移时使用。此选项仅适用于本地备份，云备份需要Hobby或Pro账户。**

**始终不可包含的文件类型：**
| 文件路径            | 原因                                      |
|------------------|-----------------------------------------|
| `credentials/**`     | API密钥、令牌及认证相关文件                   |
| `openclaw.json`       | 可能包含用户凭证                         |
| `agents/*/auth.json`     | 认证相关配置文件                         |
| `agents/*/auth-profiles.json` | 用户认证配置文件                         |
| `memory/lancedb/**`     | 旧版向量数据库文件                         |
| `*.lock`, `*.wal`, `*.shm`     | 数据库锁文件                         |
| `node_modules/**`     | 项目依赖库                         |

**重要提示：**用户凭证永远不会被备份到外部服务器。请使用`npx clawon@0.1.11 discover`命令确认备份内容，确保不会遗漏任何文件。