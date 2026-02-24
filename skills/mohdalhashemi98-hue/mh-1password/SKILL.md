---
name: 1password
description: >
  **设置并使用 1Password CLI**  
  1Password CLI 提供了多种功能，适用于以下场景：  
     - **安装 CLI**：用于将 1Password 的功能集成到您的应用程序中。  
     - **启用桌面应用集成**：允许您在桌面应用程序中直接使用 1Password 的功能。  
     - **登录**：支持单账户或多账户登录。  
     - **读取/注入/运行密钥**：用于安全地管理和使用存储在 1Password 中的敏感信息（如密码、API 密钥等）。  
  **使用方法**：  
  1. **安装 1Password CLI**：根据您的操作系统和编程语言，从 [1Password 官网](https://www.1password.com/products/clawhub) 下载并安装相应的 CLI 工具。  
  2. **配置桌面应用集成**：在安装完成后，按照 1Password 的官方文档配置您的桌面应用程序，以便能够通过 CLI 访问 1Password 的功能。  
  3. **登录**：使用 CLI 进行登录时，可以选择单账户登录或多账户登录。  
  4. **管理密钥**：使用 CLI 读取、注入或运行存储在 1Password 中的密钥。  
  **注意事项**：  
  - 请确保您的系统已安装并配置好 [1Password Desktop](https://www.1password.com/products/clawhub) 应用程序，以便更好地利用 CLI 的功能。  
  - 在处理敏感信息时，请严格遵守安全最佳实践，避免泄露密钥。  
  **示例**：  
  ```bash
  # 通过 CLI 读取存储在 1Password 中的密码
  password = 1password cli get-secret "my_password"
  ```
  **更多信息**：  
  请访问 [1Password 官网](https://www.1password.com/products/clawhub) 以获取更多关于 1Password CLI 的详细信息和使用指南。
homepage: https://developer.1password.com/docs/cli/get-started/
metadata:
  {
    "openclaw":
      {
        "emoji": "🔐",
        "requires": { "bins": ["op"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "1password-cli",
              "bins": ["op"],
              "label": "Install 1Password CLI (brew)",
            },
          ],
      },
  }
---
# 1Password CLI

请按照官方的 CLI 使用指南进行操作。切勿自行猜测安装命令。

## 参考资料

- `references/get-started.md`（安装流程、应用程序集成以及登录流程）
- `references/cli-examples.md`（实际操作示例）

## 工作流程

1. 检查操作系统和 shell 环境。
2. 确认 CLI 是否已安装：`op --version`。
3. 根据官方指南确认桌面应用程序集成是否已启用，并确保应用程序已解锁。
4. **必选**：为所有 `op` 命令创建一个新的 tmux 会话（切勿在 tmux 之外直接执行 `op` 命令）。
5. 在 tmux 内登录/授权：`op signin`（会看到应用程序的提示信息）。
6. 在 tmux 内验证访问权限：`op whoami`（在执行任何涉及敏感信息的操作前，此步骤必须成功）。
7. 如果使用多个账户，请使用 `--account` 或 `OP_ACCOUNT` 参数进行切换。

## 必需的 tmux 会话设置（T-Max）

该 shell 工具在每次执行命令时都会使用一个新的 TTY（终端会话）。为避免重复提示或错误，请始终在专门的 tmux 会话中执行 `op` 命令。每个 tmux 会话都应使用唯一的会话名称。

**示例**（有关会话名称的约定，请参考 `tmux` 文档；切勿重复使用旧的会话名称）：

```bash
SOCKET_DIR="${OPENCLAW_TMUX_SOCKET_DIR:-${CLAWDBOT_TMUX_SOCKET_DIR:-${TMPDIR:-/tmp}/openclaw-tmux-sockets}}"
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/openclaw-op.sock"
SESSION="op-auth-$(date +%Y%m%d-%H%M%S)"

tmux -S "$SOCKET" new -d -s "$SESSION" -n shell
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op signin --account my.1password.com" Enter
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op whoami" Enter
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op vault list" Enter
tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200
tmux -S "$SOCKET" kill-session -t "$SESSION"
```

## 安全准则

- **严禁** 将任何敏感信息粘贴到日志、聊天记录或代码中。
- 建议使用 `op run` 或 `op inject` 功能来处理敏感数据，而非将其直接写入磁盘。
- 如果需要在未启用应用程序集成的情况下登录，请使用 `op account add` 命令。
- 如果命令提示“账户未登录”，请在 tmux 内重新执行 `op signin` 并在应用程序中完成授权。
- **严禁** 在 tmux 之外直接执行 `op` 命令；如果 tmux 无法使用，请停止操作并询问原因。