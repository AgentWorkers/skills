---
name: confidant
description: 用于AI代理的安全秘密信息传递和凭证设置向导。当您需要从用户那里获取敏感信息（如API密钥、密码、令牌）或需要将凭证保存到配置文件中时，请使用该向导。切勿通过聊天请求用户提供敏感信息——请改用Confidant工具。
---
# Confidant

安全地从用户那里接收秘密信息——无需在聊天中展示信息，无需复制粘贴，也不会泄露历史记录。

## 🚨 重要流程——请先阅读此部分

这是一个需要人工参与的过程。您**不能**自行获取秘密信息。

1. **运行脚本** → 您会得到一个安全的 URL。
2. **将 URL 通过聊天发送给用户** ← 这是必须执行的步骤。
3. **等待** 用户在浏览器中打开该 URL 并提交秘密信息。
4. 脚本会处理后续的所有操作（接收、保存到磁盘并确认接收成功）。

```
❌ DO NOT curl/fetch the secret URL yourself — it's a web form for humans
❌ DO NOT skip sharing the URL — the user MUST receive it in chat
❌ DO NOT poll the API to check if the secret arrived — the script does this
❌ DO NOT proceed without confirming the secret was received
✅ Share URL → Wait → Confirm success → Use the secret silently
```

## ⚡ 快速入门

您需要用户的 API 密钥吗？只需执行一个命令即可：

```bash
{skill}/scripts/request-secret.sh --label "OpenAI API Key" --service openai
```

脚本会完成所有工作：
- ✅ 如果服务器未运行，则启动服务器（或重用现有服务器）。
- ✅ 通过网页表单创建一个安全的请求。
- ✅ 检测是否存在现有的隧道（如 ngrok 或 localtunnel）。
- ✅ 返回可供共享的 URL。

**如果用户位于远程位置（不在同一网络中）**，请添加 `--tunnel` 参数：

```bash
{skill}/scripts/request-secret.sh --label "OpenAI API Key" --service openai --tunnel
```

这将自动启动 [localtunnel](https://theboroer.github.io/localtunnel-www/)（无需注册账号），并返回一个公共 URL。

**输出示例：**
```
🔐 Secure link created!

URL: https://gentle-pig-42.loca.lt/requests/abc123
  (tunnel: localtunnel | local: http://localhost:3000/requests/abc123)
Save to: ~/.config/openai/api_key

Share the URL above with the user. Secret expires after submission or 24h.
```

您只需分享该 URL，用户打开 URL 并提交秘密信息，即可完成整个流程。

## 脚本

### `request-secret.sh` — 创建安全的请求（推荐使用）

```bash
# Save to ~/.config/<service>/api_key (convention)
{skill}/scripts/request-secret.sh --label "SerpAPI Key" --service serpapi

# Save to explicit path
{skill}/scripts/request-secret.sh --label "Token" --save ~/.credentials/token.txt

# Save + set env var
{skill}/scripts/request-secret.sh --label "API Key" --service openai --env OPENAI_API_KEY

# Just receive (no auto-save)
{skill}/scripts/request-secret.sh --label "Password"

# Remote user — start tunnel automatically
{skill}/scripts/request-secret.sh --label "Key" --service myapp --tunnel

# JSON output (for automation)
{skill}/scripts/request-secret.sh --label "Key" --service myapp --json
```

| 参数 | 说明 |
|------|-------------|
| `--label <文本>` | 在网页表单上显示的说明 **（必填）** |
| `--service <名称>` | 自动将密钥保存到 `~/.config/<名称>/api_key` 文件中 |
| `--save <路径>` | 自动将密钥保存到指定的文件路径 |
| `--env <变量名>` | 设置环境变量（需要 `--service` 或 `--save` 参数） |
| `--tunnel` | 如果未检测到隧道，则启动 localtunnel（适用于远程用户） |
| `--port <端口号>` | 服务器端口号（默认：3000） |
| `--timeout <秒数>` | 启动服务器的最大等待时间（默认：15 秒） |
| `--json` | 以 JSON 格式输出结果，而非人类可读的文本 |

### `check-server.sh` — 服务器诊断工具（无副作用）

```bash
{skill}/scripts/check-server.sh
{skill}/scripts/check-server.sh --json
```

该脚本会报告服务器的状态、端口号、进程 ID 以及隧道（ngrok 或 localtunnel）的运行状态。

## 代理使用规则

1. **切勿要求用户在聊天中直接粘贴秘密信息** — 始终使用本工具提供的功能。
2. **切勿在聊天中泄露任何接收到的秘密信息** — 即使是部分内容也不行。
3. **切勿直接使用 `curl` 命令访问 Confidant 的 API** — 请使用相应的脚本。
4. **切勿为了启动新服务器而关闭现有的服务器**。
5. **切勿尝试直接暴露服务器的端口号**（例如通过公共 IP 或防火墙规则） — 请使用 `--tunnel` 参数。
6. **务必通过聊天将 URL 提供给用户** — 这正是该工具的核心功能。
7. **务必等待用户完成提交操作** — 不要主动发起请求，也不要尝试自行获取秘密信息。
8. 如果用户位于远程位置（不在同一台机器/网络中），请使用 `--tunnel` 参数。
9. 推荐使用 `--service` 参数来保存 API 密钥 — 这是最规范的用法。
10. 收到秘密信息后，应默默地确认接收成功。

## 代理与用户的交互示例

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

⚠️ 注意：代理仅负责发送 URL 并等待用户的操作，不会尝试自行访问该 URL。

## 工作原理

1. 脚本会启动 Confidant 服务器（或在端口 3000 上重用现有服务器）。
2. 生成一个带有唯一标识符的安全请求，并通过网页表单进行提交。
3. （可选）为公共访问创建一个本地隧道（如果存在 ngrok 或 localtunnel，则会自动使用）。
4. 用户在浏览器中打开 URL 并提交秘密信息。
5. 秘密信息会被接收并保存到磁盘（权限设置为 600），随后在服务器上被删除。

## 隧道选项

| 提供方 | 是否需要账号 | 使用方法 |
|----------|---------------|-----|
| **localtunnel**（默认） | 不需要 | 使用 `--tunnel` 参数或 `npx localtunnel --port 3000` 命令 |
| **ngrok** | 需要账号（免费 tier） | 如果在同一端口上运行 ngrok，会自动检测到 |
脚本会自动检测这两种隧道。如果两者均未运行且指定了 `--tunnel` 参数，则会启动 localtunnel。

## 高级用法：直接使用 CLI

对于脚本无法处理的特殊情况：

```bash
# Start server only
npx @aiconnect/confidant serve --port 3000 &

# Create request on running server
npx @aiconnect/confidant request --label "Key" --service myapp

# Submit a secret (agent-to-agent)
npx @aiconnect/confidant fill "<url>" --secret "<value>"

# Check a specific request
npx @aiconnect/confidant get <id>
```

⚠️ 仅当脚本无法满足您的需求时，才请使用直接通过 CLI 的方法。