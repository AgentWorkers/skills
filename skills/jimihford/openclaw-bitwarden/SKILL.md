---
name: bitwarden
description: **安装并使用 Bitwarden CLI（bw）**  
Bitwarden CLI 是用于安装 Bitwarden、解锁加密保管库（vault），以及通过 Bitwarden 读取或生成加密密钥的工具。它还通过 `BW_SESSION` 模块负责会话管理。  

**使用场景：**  
- 安装 Bitwarden CLI  
- 解锁已加密的保管库  
- 通过 Bitwarden 读取或生成加密密钥  
- 使用 `BW_SESSION` 模块进行会话管理
homepage: https://bitwarden.com/help/cli/
metadata: {"openclaw":{"emoji":"🔐","requires":{"bins":["bw","tmux"]},"install":[{"id":"brew-bw","kind":"brew","formula":"bitwarden-cli","bins":["bw"],"label":"Install Bitwarden CLI (brew)"},{"id":"brew-tmux","kind":"brew","formula":"tmux","bins":["tmux"],"label":"Install tmux (brew)"}]}}
---

# Bitwarden CLI

通过 Bitwarden CLI 管理密码和密钥。

## 参考资料

- `references/get-started.md`（安装、登录和解锁流程）
- `references/cli-examples.md`（实际的 Bitwarden CLI 使用示例）

## 工作流程

1. 检查 CLI 是否可用：`bw --version`。
2. 检查登录状态：`bw status`（返回包含状态信息的 JSON 数据）。
3. 如果未登录：`bw login`（存储 API 密钥，并提示输入主密码）。
4. **必需步骤**：为所有 Bitwarden CLI 命令创建一个新的 tmux 会话。
5. 在 tmux 会话中解锁密码库：`bw unlock`（输出会话密钥）。
6. 导出会话密钥：`export BW_SESSION="<key>"`。
7. 验证访问权限：`bw sync`，然后执行 `bw list items --search test`。

## 必需的 tmux 会话

Bitwarden CLI 需要 `BW_SESSION` 环境变量才能执行认证命令。为了在多次命令之间保持会话状态，请始终在专用的 tmux 会话中运行 Bitwarden CLI。

**示例**（有关 tmux 会话的配置，请参考相关文档）：

```bash
SOCKET_DIR="${CLAWDBOT_TMUX_SOCKET_DIR:-${TMPDIR:-/tmp}/openclaw-tmux-sockets}"
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/openclaw-bw.sock"
SESSION="bw-auth-$(date +%Y%m%d-%H%M%S)"

tmux -S "$SOCKET" new -d -s "$SESSION" -n shell

# Unlock and capture session key
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- 'export BW_SESSION=$(bw unlock --raw)' Enter
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- 'bw sync' Enter
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- 'bw list items --search github' Enter

# Capture output
tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200

# Cleanup when done
tmux -S "$SOCKET" kill-session -t "$SESSION"
```

## 常用命令

| 命令 | 描述 |
|---------|-------------|
| `bw status` | 检查登录/锁定状态（返回 JSON 数据） |
| `bw login` | 使用电子邮件/密码或 API 密钥登录 |
| `bw unlock` | 解锁密码库，并返回会话密钥 |
| `bw lock` | 锁定密码库 |
| `bw sync` | 将密码库与服务器同步 |
| `bw list items` | 列出所有项目 |
| `bw list items --search <查询>` | 搜索项目 |
| `bw get item <id-or-name>` | 获取特定项目（返回 JSON 数据） |
| `bw get password <id-or-name>` | 仅获取密码 |
| `bw get username <id-or-name>` | 仅获取用户名 |
| `bw get totp <id-or-name>` | 获取 TOTP 代码 |
| `bw generate -ulns --length 32` | 生成新密码 |

## 安全注意事项

- **严禁** 将密钥粘贴到日志、聊天记录或代码中。
- **务必** 使用 tmux 会话来确保 `BW_SESSION` 在多次命令之间保持有效。
- 当只需要密码时，建议使用 `bw get password` 而不是解析完整的 JSON 数据。
- 如果命令显示“密码库已锁定”，请在 tmux 会话中重新运行 `bw unlock`。
- **切勿** 在 tmux 会话之外执行需要认证的 Bitwarden CLI 命令，否则会话状态将不会被保存。
- 使用完密码库后，请执行 `bw lock` 以锁定密码库。

## 使用 Vaultwarden 进行测试

本文档包含使用 [Vaultwarden](https://github.com/dani-garcia/vaultwarden)（一个与 Bitwarden 兼容的本地服务器）进行测试的 Docker Compose 配置。

### 快速入门

```bash
# Install mkcert and generate local certs (one-time)
brew install mkcert
mkcert -install
cd /path/to/openclaw-bitwarden
mkdir -p certs && cd certs
mkcert localhost 127.0.0.1 ::1
cd ..

# Start Vaultwarden + Caddy
docker compose up -d

# Configure bw CLI to use local server
bw config server https://localhost:8443

# Create a test account via web UI at https://localhost:8443
# Or run the setup script:
./scripts/setup-test-account.sh

# Test the skill workflow
./scripts/test-skill-workflow.sh
```

### 测试凭据

- **服务器地址：** `https://localhost:8443`
- **管理员面板：** `https://localhost:8443/admin`（令牌：`test-admin-token-12345`）
- **建议的测试账户：** `test@example.com` / `TestPassword123!`

### Node.js 的 CA 证书信任设置

Bitwarden CLI 需要信任 mkcert CA 证书。在运行命令前，请先导出该证书：

```bash
export NODE_EXTRA_CA_CERTS="$(mkcert -CAROOT)/rootCA.pem"
```

或者将其添加到您的 shell 配置文件中，以便在每次启动 shell 时自动应用该设置。

### 清理操作

```bash
docker compose down -v  # Remove container and data
```