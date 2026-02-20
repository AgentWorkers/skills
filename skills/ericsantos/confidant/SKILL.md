---
name: confidant
description: >
  **AI代理的安全秘密信息传递与凭据设置向导**  
  适用于需要从用户处获取敏感信息（如API密钥、密码、令牌）或需要将凭据保存到配置文件中的场景。**切勿通过聊天方式请求这些敏感信息**——请使用Confidant工具。
---
# Confidant

安全地从用户那里接收秘密信息——无需在聊天中显示信息，无需复制粘贴，也不会泄露历史记录。

## 🚨 重要流程 — 请先阅读此内容

这是一个需要人工参与的流程。您**不能**自行获取秘密信息。

1. **运行脚本** → 您会得到一个安全的 URL。
2. **将 URL 通过聊天发送给用户** ← 这是必须执行的步骤。
3. **等待** 用户在浏览器中打开该 URL 并提交秘密信息。
4. 脚本会处理后续的所有操作（接收、保存到磁盘并确认提交）。

```
❌ DO NOT curl/fetch the secret URL yourself — it's a web form for humans
❌ DO NOT skip sharing the URL — the user MUST receive it in chat
❌ DO NOT poll the API to check if the secret arrived — the script does this
❌ DO NOT proceed without confirming the secret was received
✅ Share URL → Wait → Confirm success → Use the secret silently
```

## 🔧 设置（每个环境只需执行一次）

运行此脚本即可全局安装 CLI（避免使用 `npx` 时出现性能问题）：

```bash
bash {skill}/scripts/setup.sh
```

> `{{skill}}` 是包含此 `SKILL.md` 文件的目录的绝对路径。代理程序可以在运行时解析该路径：
> ```bash
> SKILL_DIR=$(find "$HOME" -name "SKILL.md" -path "*/confidant/skill*" -exec dirname {} \; 2>/dev/null | head -1)
> # Then use: bash "$SKILL_DIR/scripts/setup.sh"
> ```

## ⚡ 快速入门

您需要用户的 API 密钥吗？只需执行一个命令即可：

```bash
bash {skill}/scripts/request-secret.sh --label "OpenAI API Key" --service openai
```

脚本会处理所有步骤：
- ✅ 如果服务器未运行，则启动服务器（或重用现有服务器）。
- ✅ 通过网页表单创建安全请求。
- ✅ 检测现有的隧道（`ngrok` 或 `localtunnel`）。
- ✅ 返回可供共享的 URL。

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

用户分享 URL → 打开 URL → 提交秘密 → 完成。

## 脚本

### `request-secret.sh` — 创建安全请求（推荐使用）

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

| 参数 | 说明 |
|------|-------------|
| `--label <text>` | 在网页表单上显示的描述 **（必填）** |
| `--service <name>` | 自动保存到 `~/.config/<name>/api_key` |
| `--save <path>` | 自动保存到指定文件路径 |
| `--env <varname>` | 设置环境变量（需要 `--service` 或 `--save` 参数） |
| `--tunnel` | 如果未检测到隧道，则启动 localtunnel（适用于远程用户） |
| `--port <number>` | 服务器端口（默认：3000） |
| `--timeout <secs>` | 启动服务器的最大等待时间（默认：15 秒） |
| `--json` | 以 JSON 格式输出结果（而非人类可读的文本） |

### `check-server.sh` — 服务器诊断（无副作用）

```bash
bash {skill}/scripts/check-server.sh
bash {skill}/scripts/check-server.sh --json
```

报告服务器状态、端口、进程 ID 以及隧道状态（`ngrok` 或 `localtunnel` 的状态）。

## 代理程序的使用规则

1. **切勿要求用户在聊天中复制粘贴秘密信息** — 始终使用此工具。
2. **切勿在聊天中透露接收到的秘密信息** — 即使是部分内容也不行。
3. **切勿直接使用 `curl` 访问 Confidant API** — 请使用相应的脚本。
4. **切勿为了启动新服务器而关闭现有服务器**。
5. **切勿尝试直接暴露服务器端口**（例如通过公共 IP 或防火墙规则） — 请使用 `--tunnel` 参数。
6. **务必在聊天中将与用户共享的 URL 告诉用户** — 这正是该工具的核心功能。
7. **务必等待用户完成提交** — 不要主动查询、重试或尝试自行获取秘密信息。
8. 如果用户位于远程位置（不在同一台机器/网络中），请使用 `--tunnel` 参数。
9. 对于 API 密钥，建议使用 `--service` 参数 — 这是最清晰、最规范的用法。
10. 收到秘密信息后，应默默地确认接收成功。

## 脚本的退出代码

代理程序可以根据退出代码进行程序化错误处理：

| 代码 | 常量 | 含义 |
|------|----------|---------|
| `0` | — | 成功 — URL 已创建并输出 |
| `1` | `MISSING_LABEL` | 未提供 `--label` 参数 |
| `2` | `MISSING_DEPENDENCY` | 未安装 `jq`、`npm` 或 `confidant` |
| `3` | `SERVER_TIMEOUT` | 服务器在指定时间内未能启动 |
| `4` | `REQUEST_FAILED` | CLI 未返回有效的 URL — 请求失败 |
| `5` | `TUNNEL_FAILED` | 请求了 `--tunnel` 选项，但未捕获到 localtunnel 的 URL |

当使用 `--json` 选项时，所有错误信息都会包含一个 `"code"` 字段，以便进行程序化处理：

```json
{"error": "...", "code": "MISSING_DEPENDENCY", "hint": "..."}
```

## 代理程序的交互示例

交互过程应如下所示：

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

⚠️ 注意：代理程序仅负责发送 URL 并等待用户的操作，不会尝试直接访问该 URL。

## 工作原理

1. 脚本会启动一个 Confidant 服务器（或在端口 3000 上重用现有服务器）。
2. 通过带有唯一 ID 的安全网页表单创建请求。
3. （可选）为公共访问启动一个 localtunnel（或检测现有的 `ngrok`/`localtunnel`）。
4. 用户在浏览器中打开 URL 并提交秘密信息。
5. 秘密信息会被接收，可选择性地保存到磁盘（权限设置为 `chmod 600`），然后在服务器上被删除。

## 隧道选项

| 提供方 | 是否需要账户 | 使用方法 |
|----------|---------------|-----|
| **localtunnel**（默认） | 不需要 | 使用 `--tunnel` 参数或 `npx localtunnel --port 3000` |
| **ngrok** | 需要账户（免费 tier） | 如果在同一端口上运行，则会自动检测到 |

脚本会自动检测这两种隧道。如果两者均未运行且指定了 `--tunnel` 参数，则会启动 localtunnel。

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

⚠️ 仅当脚本无法满足您的需求时，才使用直接 CLI。