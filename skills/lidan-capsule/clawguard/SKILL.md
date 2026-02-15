---
name: clawguard
description: 安装并配置 ClawGuard 安全插件：这是一个基于大型语言模型（LLM）的“安全护栏”，能够检测并阻止潜在危险的操作（如调用不安全的工具）。
metadata: {"openclaw":{"emoji":"🛡️","homepage":"https://github.com/capsulesecurity/clawguard"}}
---

# ClawGuard 插件安装指南

ClawGuard 是一个安全插件，它使用大型语言模型（LLM）作为“裁判”，在工具调用执行前对其进行评估，从而检测并（可选地）阻止高风险操作。

## 先决条件

在安装 ClawGuard 之前，请确保已启用网关的聊天完成（chat completions）端点：

```bash
openclaw config set gateway.http.endpoints.chatCompletions.enabled true
```

## 安装

通过 npm 安装该插件：

```bash
openclaw plugins install @capsulesecurity/clawguard
```

安装完成后，重启网关以加载插件。

## Docker 安装

如果是在 Docker 中运行 OpenClaw，请按照以下步骤操作：

```bash
# Install the plugin
docker compose run --rm openclaw-cli plugins install @capsulesecurity/clawguard

# Restart gateway with force-recreate to reload env vars
docker compose up -d --force-recreate openclaw-gateway
```

**重要提示：** 重启时务必使用 `--force-recreate` 参数。普通的 `docker compose restart` 命令不会重新加载环境变量。

## 验证安装

检查网关日志中是否有初始化成功的消息：

```
[clawguard] Initialized (logging: true, security: true, block: true, metrics: enabled)
```

## 配置

使用 `openclaw config set plugins.clawguard.<option> <value>` 命令来配置 ClawGuard：

| 选项          | 默认值       | 说明                          |
|----------------|------------|--------------------------------------------|
| enabled         | true        | 启用/禁用该插件                        |
| logToolCalls      | true        | 将工具调用信息以 JSON 格式记录到网关日志中             |
| securityCheckEnabled | true        | 运行大型语言模型的安全评估                 |
| blockOnRisk       | true        | 阻止高风险或关键风险的工具调用                   |
| maxContextWords    | 2000        | 用于评估的会话上下文字符限制                 |
| timeoutMs       | 15000        | 安全评估的超时时间（以毫秒为单位）                |
| gatewayHost      | 127.0.0.1      | 用于调用大型语言模型的网关主机                 |
| gatewayPort     | 18789      | 用于调用大型语言模型的网关端口                 |
| metricsEnabled     | true        | 启用匿名使用数据统计                        |

### 配置示例

```bash
# Disable blocking (log-only mode)
openclaw config set plugins.clawguard.blockOnRisk false

# Increase timeout for slower models
openclaw config set plugins.clawguard.timeoutMs 30000

# Disable metrics collection
openclaw config set plugins.clawguard.metricsEnabled false
```

## 网关认证

ClawGuard 会内部调用网关的 `/v1/chat/completions` 端点。如果遇到 401 Unauthorized 错误，请检查：

1. 确保您的环境中的网关令牌与配置文件中的令牌一致：
   ```bash
   # Check env var
   printenv OPENCLAW_GATEWAY_TOKEN

   # Check config token
   cat ~/.openclaw/openclaw.json | grep -A2 '"token"'
   ```

2. 如果令牌不匹配，请更新环境配置并重启网关。

对于 Docker 环境，请确保 `.env` 文件中包含正确的 `OPENCLAW_GATEWAY_TOKEN`，并在重启时使用 `--force-recreate` 参数。

## 故障排除

### 错误代码 405：方法不允许（405 Method Not Allowed）
- 检查聊天完成端点是否已启用。如果未启用，请运行相应命令进行配置。

### 错误代码 401：未经授权（401 Unauthorized）
- 确保环境中的令牌与配置文件中的令牌一致。请参考上述“网关认证”部分进行排查。

### 插件未加载
- 检查 `openclaw plugins list` 命令是否显示了 `clawguard` 插件。
- 重启网关。
- 查看网关日志以获取可能的错误信息。

## 工作原理

ClawGuard 会注册一个 `before_tool_call` 回调钩子，该钩子会：
1. （如果 `logToolCalls` 选项被启用）记录工具调用详情。
2. 将工具的上下文信息发送给大型语言模型进行安全评估。
3. 返回风险评估结果（无风险/低风险/中等风险/高风险/关键风险）。
4. 如果风险评估结果为高风险或关键风险，并且 `blockOnRisk` 选项被启用，则阻止工具的执行。

安全评估使用您配置的大型语言模型提供者，因此它可以与您在 OpenClaw 中设置的任何模型配合使用。

## 链接

- GitHub：https://github.com/capsulesecurity/clawguard
- npm：https://www.npmjs.com/package/@capsulesecurity/clawguard