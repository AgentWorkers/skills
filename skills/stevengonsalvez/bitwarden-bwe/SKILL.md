---
name: bitwarden
description: 通过 Bitwarden CLI（bw）管理密钥。该工具可用于将密钥导入 shell 会话、根据 `.env` 文件创建/更新安全笔记、列出 Bitwarden 仓库中的项目，或在新的机器上设置 Bitwarden。密钥存储在 Bitwarden 中，按需加载到内存中，并在 shell 会话结束时自动销毁；不会在磁盘上留下任何文件。
homepage: https://bitwarden.com/help/cli/
metadata:
  {
    "openclaw":
      {
        "emoji": "🔐",
        "requires": { "bins": ["bw", "jq"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "bitwarden-cli",
              "bins": ["bw"],
              "label": "Install Bitwarden CLI (brew)",
            },
            {
              "id": "snap",
              "kind": "shell",
              "command": "sudo snap install bw",
              "bins": ["bw"],
              "label": "Install Bitwarden CLI (snap)",
            },
            {
              "id": "npm",
              "kind": "shell",
              "command": "npm install -g @bitwarden/cli",
              "bins": ["bw"],
              "label": "Install Bitwarden CLI (npm)",
            },
          ],
      },
  }
---
# Bitwarden CLI — 秘密管理

## 核心概念

Bitwarden 将秘密存储为“安全笔记”（Secure Notes），这些笔记通过 `export KEY='value'` 的格式进行保存。通过执行 `eval` 命令，这些秘密可以被加载到当前 shell 环境中。所有秘密数据都不存储在磁盘上，会随着会话的结束而消失。

## Shell 函数

所有相关的 Shell 函数都包含在 `lib/bw-functions.sh` 文件中。你需要在自己的 shell 配置文件中导入该文件（通过 `source` 命令），无需手动复制或依赖 `.dotfile` 文件。

### 在新机器上设置 Bitwarden CLI

```bash
# 1. Install bw CLI
brew install bitwarden-cli    # macOS
sudo snap install bw          # Ubuntu
npm i -g @bitwarden/cli       # any OS

# 2. Install skill (choose one)
npx clawhub install bitwarden-bwe            # via ClawHub
# or: git clone https://github.com/stevengonsalvez/clawdbot /path/to/clawdbot

# 3. Source functions in your shell profile
echo 'source /path/to/skills/bitwarden-bwe/lib/bw-functions.sh' >> ~/.bashrc
source ~/.bashrc

# 4. Login + unlock
export BW_CLIENTID="user.xxxxx"
export BW_CLIENTSECRET="xxxxx"
bw login --apikey
bwss   # unlock (prompts for master password)

# 5. Verify
bwl    # list vault items
```

### `lib/bw-functions.sh` 文件中的函数功能

| 函数                | 功能描述                                                                                   |
| ------------------- | ----------------------------------------------------------------------------------------- |
| `bwss`              | 解锁 Bitwarden 保管库，并交互式地设置 `BW_SESSION` 环境变量                         |
| `bwe <name>`        | 从安全笔记中加载秘密到当前 shell 环境变量中                                      |
| `bwe_safe <name>`   | 类似 `bwe`，但仅加载格式为 `export VAR=value` 的行——适用于需要额外安全性的共享组织             |
| `bwc <name> [file]` | 从 `.env` 文件创建新的安全笔记（自动对值进行引用处理，并使用 `mktemp` 和 `chmod 600` 命令设置文件权限）     |
| `bwce <name>`       | 从当前 shell 的导出变量中创建新的安全笔记                                   |
| `bwdd <name>`       | 根据名称删除某个秘密项                                               |
| `bwl`               | 列出所有秘密项的名称                                                     |
| `bwll <grep>`       | 根据名称搜索秘密项                                                     |
| `bwg <name>`        | 获取某个秘密项的完整 JSON 数据                                               |

**关于 `bwe_safe` 的说明：** 该函数可以防止非导出的内容被注入到 shell 环境中，但不会对输入值进行清洗——如果值中包含 `$(cmd)` 或反引号，它们仍然可能在 `eval` 时被执行。如果有人拥有对你的 Bitwarden 保管库的写入权限，那么你将面临更大的安全风险。建议在共享组织账户中使用该函数作为额外的安全防护措施。

## 参考资料

- `lib/bw-functions.sh`：官方提供的 Shell 函数实现代码
- `references/cli-reference.md`：Bitwarden CLI 的安装、认证及常用操作指南

## 使用流程

### 日常使用

```bash
bwss                     # Unlock vault (once per terminal session)
bw sync                  # Pull latest from server (if secrets were updated in web vault)
bwe agent-fleet          # Load all agent secrets
echo $ANTHROPIC_API_KEY  # Verify — should be set
```

### 创建/更新秘密

```bash
# From a .env file
bwc my-new-project .env

# From current shell
bwce snapshot-2026-03-03

# Update an existing note (delete + recreate)
bwdd old-note
bwc old-note .env.updated

# Or edit in web vault — notes field, one `export KEY='value'` per line
```

### 组织与集合模式（团队/多设备协作场景）

**如何与机器账户共享秘密（例如：GCP 虚拟机）：**

1. **创建一个 Bitwarden 组织**（免费 tier 支持 2 个用户）。
2. 在该组织中创建一个集合（例如：`popa-secrets`）。
3. 创建一个机器账户（独立的 Bitwarden 账户），邀请其加入该组织，并将其关联到相应的集合。
4. 使用 `export KEY='value'` 的格式向集合中添加秘密笔记。
5. 在目标机器上：安装 Bitwarden CLI，导入 `lib/bw-functions.sh` 文件，使用机器账户的 API 密钥登录，然后执行 `bwss` 或 `bwe <note>` 命令来加载秘密。

机器账户只能访问其所属集合中的秘密项。如需撤销访问权限，只需从组织中移除该账户即可。

### 通过程序方式创建/更新集合中的秘密项

```bash
COLLECTION_ID="<collection-uuid>"
ORG_ID="<org-uuid>"
NOTES=$(cat .env | awk '{print "export " $0}')

bw get template item | jq \
  --arg notes "$NOTES" \
  --arg name "my-item" \
  --arg orgId "$ORG_ID" \
  --argjson colIds "[\"$COLLECTION_ID\"]" \
  '.type = 2 | .secureNote.type = 0 | .notes = $notes | .name = $name | .organizationId = $orgId | .collectionIds = $colIds' \
  | bw encode | bw create item
```

### 列出集合和组织

```bash
bw list organizations | jq '.[] | {id, name}'
bw list collections | jq '.[] | {id, name}'
bw list items --collectionid <id> | jq '.[] | .name'
```

## 安全笔记的格式

每个安全笔记的 `notes` 字段中每行存储一个秘密：

```
export ANTHROPIC_API_KEY='sk-ant-...'
export OPENAI_API_KEY='sk-proj-...'
export DISCORD_TOKEN='MTQ3...'
```

**注意事项：**

- 每行只能包含一个 `export KEY='value'` 的格式。
- 值必须使用单引号引用。未加引号的值中如果包含 `|`、`!`、`#`、`$`、反引号或其他 Shell 特殊字符，可能会在 `eval` 时导致错误或命令执行。使用单引号可以避免这些问题。
- 禁止添加注释或空白行（它们也会被 `eval` 命令处理）。
- 密钥应全部使用大写蛇形命名法（`UPPER_SNAKE_CASE`）。
- 如果值本身包含单引号，需要使用 `'\''` 来进行转义（例如：`export KEY='value'\''s edge case'`）。
- 绝不要在秘密值中写入 Shell 命令。

## 安全使用规范：

- **切勿将秘密内容粘贴到聊天记录、日志或代码中**。仅使用 `bwe` 命令将秘密数据加载到内存中。
- **除非绝对必要，否则不要将秘密数据写入磁盘**（如果必须写入磁盘，请确保设置文件权限为 `chmod 600`）。
- **优先使用 `bwe` 而不是 `~/.secrets/` 文件**。内存中的秘密数据比磁盘上的更安全。
- **在共享账户或组织账户中使用 `bwe_safe` 命令**，以增强对笔记内容被篡改的防护能力。
- **每个终端会话开始时都需要执行 `bwss` 命令**。会话令牌会一直有效，直到 Shell 退出。
- **在更新秘密数据后，请执行 `bw sync` 命令进行同步**。
- **操作完成后执行 `bw lock` 命令以清除会话令牌**。

## 在 tmux 环境中的使用注意事项

如果在 tmux 环境中使用 Bitwarden CLI（这在代理服务器中很常见），请确保 `BW_SESSION` 环境变量可以在 tmux 窗口中访问。可以通过以下两种方式实现：
- 直接在 tmux 窗口中执行 `bwss` 命令；
- 在创建 tmux 会话之前先设置 `BW_SESSION` 环境变量。

```bash
# Option 1: unlock inside tmux (preferred — interactive, no password in process list)
tmux new-session -d -s work
tmux send-keys -t work 'bwss' Enter
# ... wait for unlock prompt, enter master password ...
tmux send-keys -t work 'bwe agent-fleet' Enter

# Option 2: pass session token via env var (non-interactive)
# ⚠️ Never pass the master password as a CLI argument — it's visible in `ps aux`.
# Use --passwordenv instead:
read -s BW_MASTER_PASSWORD && export BW_MASTER_PASSWORD
export BW_SESSION=$(bw unlock --passwordenv BW_MASTER_PASSWORD --raw)
unset BW_MASTER_PASSWORD
tmux new-session -d -s work -e "BW_SESSION=$BW_SESSION"
tmux send-keys -t work 'bwe agent-fleet' Enter
```

## 快速参考

| 命令                | 功能描述                                                                                   |
| ------------------- | -------------------------------- |
| `bwss`              | 解锁 Bitwarden 保管库，并设置 `BW_SESSION` 环境变量                         |
| `bwe <name>`        | 从安全笔记中加载秘密到当前 shell 环境变量中                                      |
| `bwe_safe <name>`   | 类似 `bwe`，但会对输入内容进行验证                                      |
| `bwc <name> [file]` | 从 `.env` 文件创建新的安全笔记                                       |
| `bwce <name>`       | 从当前 shell 的导出变量中创建新的安全笔记                                   |
| `bwdd <name>`       | 根据名称删除某个秘密项                                               |
| `bwl`               | 列出所有秘密项的名称                                                     |
| `bwll <grep>`       | 根据名称搜索秘密项                                                     |
| `bwg <name>`        | 获取某个秘密项的完整 JSON 数据                                               |
| `bw sync`           | 从服务器同步最新数据                                             |
| `bw lock`           | 清除当前会话的令牌                                             |