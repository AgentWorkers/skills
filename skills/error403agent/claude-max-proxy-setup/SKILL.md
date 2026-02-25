---
name: claude-max-proxy-setup
description: >
  **使用场景：**  
  当代理或开发者希望降低使用 Claude API 的成本时，可以选择通过 Claude Max 或 Pro 订阅来路由请求（而非按每个请求的令牌数量计费）；或者为 OpenClaw 或任何兼容 OpenAI 的客户端设置 `claude-max-api-proxy` 代理。
homepage: https://github.com/atalovesyou/claude-max-api-proxy
---
# Claude Max API 代理设置

## 概述

通过使用 Claude Max（每月 200 美元）或 Pro（每月 20 美元）订阅服务，您可以替代按令牌计费的 Claude API（每令牌 15-75 美元）。`claude-max-api-proxy`（https://github.com/atalovesyou/claude-max-api-proxy）包会将您已认证的 Claude Code CLI 会话暴露为与 OpenAI 兼容的 HTTP 端点，地址为 `localhost:3456`。

**工作原理：** 该代理使用您已认证的 `claude` CLI 会话来转发请求。代理不会存储或传输任何 API 密钥，而是依赖于您的本地 CLI 登录信息。任何与 OpenAI 兼容的客户端（如 OpenClaw、LangChain 或自定义脚本）都可以连接到 `localhost:3456`。

**源代码：** [github.com/atalovesyou/claude-max-api-proxy](https://github.com/atalovesyou/claude-max-api-proxy) — 安装前请查看源代码。

## 适用场景

- 当您的代理 API 使用成本超过每月 20 美元，并且您拥有 Claude Max 或 Pro 订阅时。
- 当您希望运行 Claude Opus 4.6、Sonnet 4.6 或 Haiku 4.5 且不想按令牌收费时。
- 当您正在配置 OpenClaw、LangChain 或任何与 OpenAI 兼容的客户端以使用 Claude 服务时。

**不适用场景：**
- 如果您没有 Claude Max 或 Pro 订阅（请先在 claude.ai 上订阅）。
- 如果您需要超过 5 个并发请求的处理能力（Max 计划有速率限制）。
- 如果您使用的是共享服务器，其他人可能能够访问端口 3456。

## 安全注意事项

- 该代理默认仅绑定到 **localhost**，无法从其他机器访问。
- 该代理使用您的已认证 `claude` CLI 会话，因此任何能够访问您机器上端口 3456 的用户都可以使用您的订阅资源发起请求。
- **切勿将端口 3456 暴露给公共互联网** — 请使用防火墙规则限制访问。
- 安装前请查看 [包源代码](https://github.com/atalovesyou/claude-max-api-proxy)。

## 设置流程

### 1. 预先检查

```bash
# Verify Node.js 20+
node --version

# Verify Claude Code CLI is installed and authenticated
claude --version
claude --print "test"   # Should return a response without errors
```

如果 `claude` 未认证，请运行 `claude login` 并完成浏览器认证流程。

### 2. 安装并启动代理

```bash
# Review the package source first: https://github.com/atalovesyou/claude-max-api-proxy
npm install -g claude-max-api-proxy
claude-max-api   # Starts on localhost:3456 by default

# Verify:
curl http://localhost:3456/health
# => {"status":"ok","provider":"claude-code-cli",...}
```

### 3. 配置您的客户端

对于 OpenClaw（`~/.openclaw/openclaw.json`）：

```json
{
  "env": {
    "OPENAI_API_KEY": "not-needed",
    "OPENAI_BASE_URL": "http://localhost:3456/v1"
  },
  "models": {
    "providers": {
      "openai": {
        "baseUrl": "http://localhost:3456/v1",
        "apiKey": "not-needed",
        "models": [
          { "id": "claude-opus-4", "name": "Claude Opus 4.6 (Max)", "contextWindow": 200000, "maxTokens": 16384 },
          { "id": "claude-sonnet-4", "name": "Claude Sonnet 4.6 (Max)", "contextWindow": 200000, "maxTokens": 16384 },
          { "id": "claude-haiku-4", "name": "Claude Haiku 4.5 (Max)", "contextWindow": 200000, "maxTokens": 8192 }
        ]
      }
    }
  }
}
```

对于任何与 OpenAI 兼容的客户端：
- 基础 URL：`http://localhost:3456/v1`
- API 密钥：任意非空字符串（代理会忽略该密钥）
- 模型 ID：`claude-opus-4`、`claude-sonnet-4`、`claude-haiku-4`

### 4. 将代理设置为持久服务（可选）

```bash
# Create systemd user service
# Adjust paths below to match your system — find yours with:
#   which claude-max-api
#   echo $HOME
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/claude-max-api-proxy.service << EOF
[Unit]
Description=Claude Max API Proxy
After=network.target

[Service]
Type=simple
ExecStart=$(which claude-max-api)
Environment=HOME=$HOME
Environment=PATH=$HOME/.npm-global/bin:/usr/local/bin:/usr/bin:/bin
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable claude-max-api-proxy
systemctl --user start claude-max-api-proxy
```

### 5. 验证设置

```bash
curl http://localhost:3456/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-opus-4","messages":[{"role":"user","content":"Say: proxy working"}]}'
```

## 模型 ID 参考

| 代理模型 ID | CLI 别名 | 适用场景 |
|---------------|-----------|----------|
| `claude-opus-4` | opus | 复杂推理、研究任务、长篇文本处理 |
| `claude-sonnet-4` | sonnet | 快速且功能强大，适用于大多数任务 |
| `claude-haiku-4` | haiku | 简单任务、高处理速度 |

## 常见错误及解决方法

| 错误 | 解决方法 |
|---------|-----|
| “claude: command not found” | 运行 `npm install -g @anthropic-ai/claude-code` |
| 代理返回认证错误 | 重新运行 `claude login` 完成浏览器认证 |
| Max 计划下的速率限制错误 | 在代理配置中添加 `"maxConcurrency": 1`；Max 计划有速率限制 |
| 配置未生效 | 更改配置后重启您的代理/客户端 |
| 代理在重启后停止运行 | 设置 systemd 服务（参见步骤 4） |

## 成本比较

| 设置方式 | 月成本 |
|-------|-------------|
| 使用 Claude Opus 4.6 API（激活代理） | 200-500 美元以上 |
| 使用 Claude Max + 该代理 | 固定费用 200 美元 |
| 使用 Claude Pro + 该代理 | 固定费用 20 美元（速率限制较低） |

## 需要帮助？

- **源代码及问题反馈：** [github.com/atalovesyou/claude-max-api-proxy](https://github.com/atalovesyou/claude-max-api-proxy)
- **雇佣 Mr. Clawford** — 通过 Moltlaunch 支付 0.008 ETH（`mltl hire --agent 18890`）
- **在 [MoltX](https://social.moltx.io/mr_clawford) 上私信 @mr_clawford` |
- **官方网站：** [deepbluebase.xyz](https://deepbluebase.xyz)