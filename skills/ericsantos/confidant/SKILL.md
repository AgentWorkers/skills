---
name: confidant
description: >
  **AI代理的安全秘密信息传递与凭据设置向导**  
  当您需要从用户那里获取敏感信息（如API密钥、密码、令牌）或将凭据保存到配置文件中时，请使用此向导。切勿通过聊天方式请求用户的秘密信息——请改用Confidant工具。
homepage: https://github.com/aiconnect-cloud/confidant
user-invocable: true
disable-model-invocation: false
metadata:
  {
    'openclaw':
      {
        'emoji': '🔐',
        'requires': { 'bins': ['curl', 'jq', 'npm'] },
        'files': ['scripts/*']
      }
  }
---
# Confidant

安全地从用户那里接收秘密信息——无需在聊天中显示信息，无需复制粘贴，也不会泄露历史记录。

## 🚨 重要流程 — 请先阅读此部分

这是一个需要人工参与的过程。您**不能自行获取秘密**。

1. **运行脚本** → 您会得到一个安全的 URL。
2. **将 URL 通过聊天发送给用户** ← 这是必须的步骤。
3. **等待** 用户在浏览器中打开该 URL 并提交秘密信息。
4. 脚本会处理剩余的工作（接收、保存到磁盘并确认）。

```
❌ DO NOT curl/fetch the secret URL yourself — it's a web form for humans
❌ DO NOT skip sharing the URL — the user MUST receive it in chat
❌ DO NOT poll the API to check if the secret arrived — the script does this
❌ DO NOT proceed without confirming the secret was received
✅ Share URL → Wait → Confirm success → Use the secret silently
```

## 🔧 设置（每个环境只需执行一次）

运行此命令一次，即可全局安装 CLI（避免使用 `npx` 时出现性能问题）：

```bash
bash {skill}/scripts/setup.sh
```

> **`{skill}`** 是包含此 `SKILL.md` 文件的目录的绝对路径。代理程序可以在运行时解析该路径：
>
> ```bash
> SKILL_DIR=$(find "$HOME" -name "SKILL.md" -path "*/confidant/skill*" -exec dirname {} \; 2>/dev/null | head -1)
> # Then use: bash "$SKILL_DIR/scripts/setup.sh"
> ```

## ⚡ 快速入门

您需要用户的 API 密钥吗？只需执行一个命令即可：

```bash
bash {skill}/scripts/request-secret.sh --label "OpenAI API Key" --service openai
```

脚本会完成所有工作：
- ✅ 如果服务器未运行，则启动服务器（或重用现有服务器）。
- ✅ 通过网页表单创建一个安全的请求。
- ✅ 检测现有的隧道（`ngrok` 或 `localtunnel`）。
- ✅ 返回一个 URL 供用户分享。
- ✅ 持续轮询直到用户提交秘密信息。
- ✅ 将秘密信息保存到 `~/.config/openai/api_key`（设置权限为 600），然后脚本退出。

**如果用户位于远程位置（不在同一网络中）**，请添加 `--tunnel` 参数：

```bash
bash {skill}/scripts/request-secret.sh --label "OpenAI API Key" --service openai --tunnel
```

这将自动启动 [localtunnel](https://theboroer.github.io/localtunnel-www/)（无需注册账户），并返回一个公共 URL。

**输出示例：**

```
🔐 Secure link created!

URL: https://gentle-pig-42.loca.lt/requests/abc123
  (tunnel: localtunnel | local: http://localhost:3000/requests/abc123)
Save to: ~/.config/openai/api_key

Share the URL above with the user. Secret expires after submission or 24h.
```

用户分享 URL → 打开 URL → 提交秘密 → 脚本将秘密保存到磁盘 → 完成。

**即使不使用 `--service` 或 `--save` 参数**，脚本仍会继续轮询并将秘密信息输出到标准输出（便于管道传输或手动查看）。

## 脚本

### `request-secret.sh` — 请求、接收并保存秘密（推荐使用）

```bash
# Save to ~/.config/<service>/api_key (convention)
bash {skill}/scripts/request-secret.sh --label "SerpAPI Key" --service serpapi

# Save to explicit path
bash {skill}/scripts/request-secret.sh --label "Token" --save ~/.credentials/token.txt

# Save + set env var
bash {skill}/scripts/request-secret.sh --label "API Key" --service openai --env OPENAI_API_KEY

# Just receive (no auto-save)
bash {skill}/scripts/request-secret.sh --label "Password"

# Remote user — start tunnel automatically
bash {skill}/scripts/request-secret.sh --label "Key" --service myapp --tunnel

# JSON output (for automation)
bash {skill}/scripts/request-secret.sh --label "Key" --service myapp --json
```

| 参数                | 说明                                                          |
| ------------------ | ---------------------------------------------------------- |
| `--label <text>`   | 在网页表单中显示的描述 **（必需）**                           |
| `--service <name>` | 自动保存到 `~/.config/<name>/api_key`                          |
| `--save <path>`    | 自动保存到指定的文件路径                                      |
| `--env <varname>`  | 设置环境变量（需要 `--service` 或 `--save` 参数）                   |
| `--tunnel`         | 如果未检测到隧道，则启动 localtunnel（适用于远程用户）                   |
| `--port <number>`  | 服务器端口（默认：3000）                                      |
| `--timeout <secs>` | 启动过程中的最大等待时间（默认：30 秒）                          |
| `--json`           | 以 JSON 格式输出结果，而非人类可读的文本                          |

### `check-server.sh` — 服务器诊断（无副作用）

```bash
bash {skill}/scripts/check-server.sh
bash {skill}/scripts/check-server.sh --json
```

报告服务器状态、端口、进程 ID 以及隧道状态（`ngrok` 或 `localtunnel` 的状态）。

## ⏱ 长时间运行的进程 — 使用 tmux

`request-secret.sh` 脚本会**持续轮询，直到用户提交秘密**。大多数代理程序（包括 OpenClaw 的 `exec` 工具）都会设置执行超时，这可能会导致脚本在用户提交之前就被终止。

**始终在 tmux 会话中运行 `Confidant` 脚本**：

```bash
# 1. Start server in tmux
tmux new-session -d -s confidant
tmux send-keys -t confidant "confidant serve --port 3000" Enter

# 2. Create request in a second tmux window
tmux new-window -t confidant -n request
tmux send-keys -t confidant:request "confidant request --label 'API Key' --service openai" Enter

# 3. Share the URL with the user (read from tmux output)
tmux capture-pane -p -t confidant:request -S -30

# 4. After user submits, check the result
tmux capture-pane -p -t confidant:request -S -10
```

> **为什么不用 `exec`？** 代理程序通常会在 30-60 秒后终止进程。由于脚本需要等待用户输入（这个过程可能需要几分钟），因此脚本可能会在完成之前被强制终止。而 tmux 可以让脚本独立地持续运行。

如果您的代理平台支持长时间运行的后台进程且没有超时限制，那么直接使用 `exec` 和 `request-secret.sh` 也是可以的。但为了保险起见，**建议使用 tmux**。

## 代理程序的使用规则

1. **绝不要要求用户在聊天中粘贴秘密信息** — 始终使用这个工具。
2. **绝不要在聊天中透露接收到的秘密信息** — 哪怕只是部分内容也不行。
3. **绝不要直接使用 `curl` 访问 Confidant API** — 请使用相应的脚本。
4. **绝不要直接关闭现有的服务器来启动新的服务器**。
5. **绝不要直接暴露服务器端口**（如公共 IP 或防火墙规则） — 请使用 `--tunnel` 参数。
6. **务必通过聊天将 URL 分享给用户** — 这正是该工具的核心功能。
7. **务必等待脚本完成** — 脚本会自动处理并保存/输出秘密信息；切勿尝试自行获取。
8. 当用户位于远程位置时，请使用 `--tunnel` 参数。
9. 对于 API 密钥，建议使用 `--service` 参数 — 这是最规范的用法。
10. 收到秘密信息后，应默默地确认接收成功。

## 脚本的退出代码

代理程序可以根据退出代码进行程序化错误处理：

| 代码       | 常量            | 含义                                                            |
| ---------- | ----------------------------- | ----------------------------------------------------------------------------- |
| `0`       | —               | 成功 — 秘密信息已接收（保存到磁盘或输出到标准输出）                         |
| `1`       | `MISSING_LABEL`      | 未提供 `--label` 参数                                      |
| `2`       | `MISSING_DEPENDENCY`    | 未安装 `curl`、`jq`、`npm` 或 `confidant`                        |
| `3`       | `SERVER_TIMEOUT`      | 服务器启动失败或崩溃                                        |
| `4`       | `REQUEST_FAILED`      | API 返回空 URL                                        |
| `≠0`      | （来自 CLI）         | `confidant request --poll` 失败（例如请求无效、未找到等）                         |

使用 `--json` 参数时，所有错误信息都会包含一个 `code` 字段，以便进行程序化处理：

```json
{ "error": "...", "code": "MISSING_DEPENDENCY", "hint": "..." }
```

## 代理程序的交互示例

交互过程应该如下所示：

```
User: Can you set up my OpenAI key?
Agent: I'll create a secure link for you to submit your API key safely.
       [runs: request-secret.sh --label "OpenAI API Key" --service openai --tunnel]
Agent: Here's your secure link — open it in your browser and paste your key:
       🔐 https://gentle-pig-42.loca.lt/requests/abc123
       The link expires after you submit or after 24h.
User: Done, I submitted it.
Agent: ✅ Received and saved to ~/.config/openai/api_key. You're all set!
```

⚠️ 注意：代理程序会发送 URL 并等待用户操作，**不会尝试直接访问该 URL**。

## 工作原理

1. 脚本会启动一个 Confidant 服务器（或在端口 3000 上重用现有服务器）。
2. 通过 API 发送一个带有唯一 ID 和安全网页表单的请求。
3. （可选）启动一个本地隧道以供外部访问（或检测现有的 `ngrok`/`localtunnel`）。
4. 脚本会将 URL 显示给用户。
5. 将轮询任务委托给 `confidant request --poll`，该脚本会持续轮询直到用户提交秘密信息。
6. 如果使用了 `--service` 或 `--save` 参数，秘密信息会被保存到磁盘（权限设置为 600），然后从服务器上删除。
7. 如果没有使用 `--service`/`--save` 参数，秘密信息会被输出到标准输出，然后从服务器上删除。

## 隧道选项

| 提供者         | 是否需要账户       | 使用方法                                                         |
| ------------------------- | ----------------------------- | ----------------------------------------------------------------------------- |
| **localtunnel**（默认） | 不需要账户       | 使用 `--tunnel` 参数或 `npx localtunnel --port 3000`                         |
| **ngrok**      | 需要账户       | 如果在同一端口上运行，会自动检测并使用 ngrok                                      |

脚本会自动检测这两种隧道。如果两者都没有运行，并且指定了 `--tunnel` 参数，脚本会启动 `localtunnel`。

## 高级用法：直接使用 CLI

对于脚本未覆盖的特殊情况：

```bash
# Start server only
confidant serve --port 3000 &

# Start server + create request + poll (single command)
confidant serve-request --label "Key" --service myapp

# Create request on running server
confidant request --label "Key" --service myapp

# Submit a secret (agent-to-agent)
confidant fill "<url>" --secret "<value>"

# Check status of a specific request
confidant get-request <id>

# Retrieve a delivered secret (by secret ID, not request ID)
confidant get <secret-id>
```

> 如果 `confidant` 未全局安装，请先运行 `bash {skill}/scripts/setup.sh`，或者使用 `npx @aiconnect/confidant` 命令。

⚠️ 仅当脚本无法满足您的需求时，才使用直接 CLI 方法。