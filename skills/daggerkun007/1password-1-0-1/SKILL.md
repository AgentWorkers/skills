---
name: 1password
description: **设置并使用 1Password CLI (op)**  
1Password CLI 提供了多种功能，适用于以下场景：  
   - 安装 CLI；  
   - 启用桌面应用程序的集成；  
   - 单个或多个账户的登录；  
   - 通过 CLI 读取、注入或运行加密后的敏感信息（如密码）。  

**使用方法：**  
1. **安装 CLI：**  
   根据官方文档或包管理器（如 pip）的指示，安装 1Password CLI。  

2. **启用桌面应用程序集成：**  
   在安装完成后，按照 CLI 的说明配置桌面应用程序，以便与 1Password 服务进行集成。  

3. **登录：**  
   使用 CLI 进行登录时，可以选择使用单个账户或多个账户。请确保提供正确的登录凭据（用户名和密码）。  

4. **管理敏感信息：**  
   - 通过 CLI 可以安全地读取已加密的敏感信息；  
   - 将敏感信息注入到需要使用的地方（如应用程序、脚本等）；  
   - 直接运行已加密的命令或脚本。  

**注意事项：**  
- 请确保使用安全的连接方式（如 HTTPS）进行数据传输，以防止信息泄露。  
- 1Password CLI 会自动处理敏感信息的加密和解密过程，确保用户数据的安全性。  

如需更多详细信息，请参阅 1Password 官方文档或相关技术资源。
homepage: https://developer.1password.com/docs/cli/get-started/
metadata: {"clawdbot":{"emoji":"🔐","requires":{"bins":["op"]},"install":[{"id":"brew","kind":"brew","formula":"1password-cli","bins":["op"],"label":"Install 1Password CLI (brew)"}]}}
---

# 1Password CLI

请按照官方的 CLI 入门指南进行操作。切勿自行猜测安装命令。

## 参考资料

- `references/get-started.md`（安装流程、应用程序集成以及登录流程）
- `references/cli-examples.md`（实际操作示例）

## 工作流程

1. 检查操作系统和 shell 环境。
2. 验证 CLI 是否已安装：`op --version`。
3. 确认桌面应用程序集成已启用（根据入门指南操作），并且应用程序已解锁。
4. **必需**：为所有 `op` 命令创建一个新的 tmux 会话（切勿在 tmux 会话之外直接执行 `op` 命令）。
5. 在 tmux 中登录/授权：`op signin`（系统会提示进入应用程序界面）。
6. 验证在 tmux 中的访问权限：`op whoami`（在执行任何涉及敏感信息的操作前必须成功登录）。
7. 如果使用多个账户，请使用 `--account` 或 `OP_ACCOUNT` 参数。

## 必须使用的 tmux 会话（T-Max）

该 Shell 工具每次执行命令时都会使用一个新的 TTY（终端会话）。为避免重复提示或错误，请始终在专门的 tmux 会话中执行 `op` 命令。每个 tmux 会话都应使用唯一的会话名称/套接字文件。

**示例**（有关套接字文件的使用规则，请参考 `tmux` 文档；切勿重复使用旧的会话名称）：

```bash
SOCKET_DIR="${CLAWDBOT_TMUX_SOCKET_DIR:-${TMPDIR:-/tmp}/clawdbot-tmux-sockets}"
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/clawdbot-op.sock"
SESSION="op-auth-$(date +%Y%m%d-%H%M%S)"

tmux -S "$SOCKET" new -d -s "$SESSION" -n shell
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op signin --account my.1password.com" Enter
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op whoami" Enter
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op vault list" Enter
tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200
tmux -S "$SOCKET" kill-session -t "$SESSION"
```

## 安全规范

- 绝不要将敏感信息粘贴到日志、聊天记录或代码中。
- 建议使用 `op run` 或 `op inject` 来传递敏感信息，而非将其写入磁盘。
- 如果需要在未启用应用程序集成的情况下登录，请使用 `op account add` 命令。
- 如果命令提示“账户未登录”，请在 tmux 中重新执行 `op signin` 并在应用程序中完成授权。
- 请勿在 tmux 会话之外直接执行 `op` 命令；如果无法使用 tmux，请停止操作并询问原因。