---
name: linear-webhook
description: "在 Linear 项目的 issues 中，通过评论 @mason 或 @eureka 来将任务分配给相应的代理。Webhook 会接收这些评论，并将其路由到正确的代理进行处理。"
---

# 线性（Linear）Webhook 技能

该技能允许在 Linear 问题评论中使用 @提及（@mentions）来触发任务分配给 Clawdbot 代理。

## 工作原理

1. 在 Linear 中发表评论：例如 `@mason implement user authentication` 或 `@eureka plan Q2 roadmap`。
2. 当评论创建时，Linear 会触发 Webhook。
3. Clawdbot 通过暴露的端点接收 Webhook 请求。
4. Clawdbot 解析请求中的数据：
   - 提取 @mason 或 @eureka 的提及内容
   - 获取问题的上下文（标题、描述、标签）
   - 准备相应的任务提示。
5. 根据提及的内容将任务路由到相应的代理：
   - @mason → `mason` 代理（负责代码实现或问题解答）
   - @eureka → `eureka` 代理（负责规划或策略制定）
6. 代理处理任务并返回结果。
7. 最后将结果以评论的形式发布回 Linear。

## 设置

### 1. 配置 Clawdbot Webhook

在 `config.json5` 文件中进行配置：

```json5
{
  hooks: {
    enabled: true,
    token: "your-secret-token-here", // Generate with: openssl rand -base64 32
    path: "/hooks",
    transformsDir: "/home/sven/clawd-mason/skills/linear-webhook",
    mappings: [
      {
        name: "linear",
        match: {
          path: "/linear",
          method: "POST"
        },
        action: "agent",
        transform: {
          module: "./linear-transform.js",
          export: "transformLinearWebhook"
        },
        deliver: false, // Don't auto-deliver to chat - Linear comments handle responses
      }
    ]
  }
}
```

### 2. 暴露 Webhook 端点

使用 Cloudflare Tunnel 或 Tailscale Funnel 来使 Webhook 公开可用：

**选项 A：Cloudflare Tunnel**（推荐）
```bash
# Install if needed
brew install cloudflared

# Start tunnel (replace with your domain)
cloudflared tunnel --url http://localhost:18789
```

**选项 B：Tailscale Funnel**
```bash
# Enable funnel
tailscale funnel 18789
```

请注意公用的 Webhook URL（例如：`https://your-tunnel.trycloudflare.com`）。

### 3. 配置 Linear Webhook

1. 进入 Linear 的设置 → API → Webhooks。
2. 点击“创建新的 Webhook”。
3. 设置 Webhook URL：`https://your-tunnel.trycloudflare.com/hooks/linear`。
4. 添加自定义头部：`x-clawdbot-token: 你的秘密令牌`。
5. 选择触发事件：**Comment → Created**。
6. 保存配置。

### 4. 测试

在 Linear 问题中发表评论：
```
@mason add user authentication to the login page
```

预期流程：
1. Webhook 被触发并发送给 Clawdbot。
2. `mason` 代理接收任务并进行处理。
3. `mason` 代理完成任务后，将结果以评论的形式发布回 Linear 问题中。

## 代理任务分配

- **@mason**：负责代码实现、调试和技术相关任务。
- **@eureka**：负责规划、策略制定和研究工作。
- 其他提及的内容将被忽略（不进行处理）。

## 提供的问题上下文

代理会收到以下信息：
- 问题标题
- 问题描述
- 问题标签
- 评论文本（包含 @提及的部分）
- 问题链接
- 评论者的名称

## 自定义功能

### 添加更多代理

编辑 `linear-transform.js` 文件以支持更多代理：

```javascript
const AGENT_MENTIONS = {
  '@mason': 'mason',
  '@eureka': 'eureka',
  '@designer': 'designer', // Add your own agents
};
```

### 修改响应行为

修改 `deliver` 和 `channel` 的配置文件中的相关代码：

```json5
{
  deliver: true,
  channel: "telegram",
  to: "1878354815", // Your Telegram chat ID
}
```

这样也可以将代理的响应发送到 Telegram。

## 安全性注意事项

- **切勿将 Webhook 令牌提交到版本控制系统中**。
- 使用环境变量 `CLAWDBOTHOOK_TOKEN` 来存储令牌。
- 根据需要验证 Webhook 的来源（例如 Linear 的 IP 范围）。
- 仅使用 HTTPS 协议（Cloudflare Tunnel 提供了这一安全保障）。

## 故障排除

### Webhook 未触发
- 检查 Linear 的 Webhook 日志（设置 → API → Webhooks → 查看日志）。
- 确认 Tunnel 是否正在运行：`curl https://your-tunnel.trycloudflare.com/hooks/linear`。
- 查看 Clawdbot 的日志：`clawdbot gateway logs`。

### 代理未响应
- 检查 `linear-transform.js` 文件中的代码是否正确加载。
- 确认代理会话是否存在：`clawdbot sessions list`。
- 手动测试 `linear-transform.js` 文件的功能。

### 响应未发布到 Linear
- 确保 `linear-transform.js` 文件中实现了将结果发布到 Linear 的逻辑。
- 在配置文件中添加 Linear 的 API 令牌。
- 可以参考 `linear-transform.js` 文件中的示例代码。

## Linear API 访问

要将响应发布回 Linear，你需要一个 Linear 的 API 令牌：

1. 进入 Linear 的设置 → API → 个人 API 密钥。
2. 创建具有 `write` 权限的新令牌。
3. 将令牌添加到环境变量中：`CLAWDBOT_LINEAR_API_KEY=lin_api_...`。
4. `linear-transform.js` 文件会使用该令牌来发送响应。

## 相关文件

- `SKILL.md`：本文档。
- `linear-transform.js`：Webhook 数据解析器和代理任务分配逻辑。
- `linear-api.js`：用于发布评论的 Linear GraphQL API 客户端。
- `example-payload.json`：用于测试的 Linear Webhook 数据示例。

## 参考资料

- [Clawdbot Webhook 文档](/automation/webhook)
- [Linear Webhooks API 文档](https://developers.linear.app/docsgraphql/webhooks)
- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)