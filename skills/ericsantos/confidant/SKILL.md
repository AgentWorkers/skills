---
name: confidant
description: 用于AI代理的安全秘密信息传递及凭据设置向导。当您需要从用户那里获取敏感信息（如API密钥、密码、令牌）或需要将凭据保存到配置文件中时，请使用该工具。切勿通过聊天方式请求用户的秘密信息——请改用Confidant。
---
# Confidant

安全地从用户那里接收秘密信息——无需通过聊天传递，无需复制粘贴，也不会泄露历史记录。

## ⚡ 快速入门

您需要用户的 API 密钥吗？只需一个命令即可：

```bash
{skill}/scripts/request-secret.sh --label "OpenAI API Key" --service openai
```

该脚本会处理所有步骤：
- ✅ 如果服务器未运行，则启动服务器（或重用现有服务器）
- ✅ 通过网页表单创建安全请求
- ✅ 检测现有的隧道（ngrok 或 localtunnel）
- ✅ 返回可供分享的 URL

**如果用户位于远程位置**（不在同一网络中），请添加 `--tunnel` 参数：

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

分享 URL → 用户打开该 URL → 提交秘密 → 完成。

## 脚本

### `request-secret.sh` — 创建安全请求（推荐使用）

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
| `--service <名称>` | 自动保存到 `~/.config/<名称>/api_key` |
| `--save <路径>` | 自动保存到指定文件路径 |
| `--env <变量名>` | 设置环境变量（需要 `--service` 或 `--save` 参数） |
| `--tunnel` | 如果未检测到隧道，则启动 localtunnel（适用于远程用户） |
| `--port <端口>` | 服务器端口（默认：3000） |
| `--timeout <秒>` | 启动服务器的最大等待时间（默认：15 秒） |
| `--json` | 以 JSON 格式输出结果，而非人类可读的文本 |

### `check-server.sh` — 服务器诊断（无副作用）

```bash
{skill}/scripts/check-server.sh
{skill}/scripts/check-server.sh --json
```

报告服务器状态、端口、进程 ID 以及隧道状态（ngrok 或 localtunnel）。

## 代理使用规则

1. **切勿要求用户在聊天中粘贴秘密信息** — 始终使用此工具来接收秘密。
2. **切勿在聊天中泄露任何接收到的秘密** — 甚至不能部分泄露。
3. **切勿直接使用 `curl` 命令调用 Confidant API** — 必须使用相应的脚本。
4. **切勿为了启动新服务器而关闭现有的服务器**。
5. 当用户位于远程位置时，请使用 `--tunnel` 参数。
6. 建议使用 `--service` 参数来保存 API 密钥——这是最规范的用法。
7. 收到秘密后，应默默地完成后续处理。

## 工作原理

1. 脚本会启动 Confidant 服务器（或在端口 3000 上重用现有服务器）。
2. 通过带有唯一 ID 的网页表单创建安全请求。
3. （可选）为公共访问启动 localtunnel（或检测现有的 ngrok/localtunnel）。
4. 用户在浏览器中打开 URL 并提交秘密信息。
5. 秘密信息会被接收并保存到磁盘（权限设置为 `chmod 600`），随后在服务器端被销毁。

## 隧道选项

| 提供者 | 是否需要账号 | 使用方法 |
|----------|---------------|-----|
| **localtunnel**（默认） | 不需要 | 使用 `--tunnel` 参数或 `npx localtunnel --port 3000` |
| **ngrok** | 需要账号（免费 tier） | 如果在同一端口上运行，会自动检测到 |

脚本会自动检测这两种隧道。如果两者均未运行且指定了 `--tunnel` 参数，则会启动 localtunnel。

## 高级用法：直接使用 CLI

对于脚本未涵盖的特殊情况：

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

⚠️ 仅当脚本无法满足您的需求时，才使用直接 CLI 命令。