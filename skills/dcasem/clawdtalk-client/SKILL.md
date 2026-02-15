---
name: clawdtalk-client
version: 1.3.0
description: **ClawdTalk** — 为 **Clawdbot** 提供的语音通话和短信功能  

**简介：**  
ClawdTalk 是一款专为 **Clawdbot** 设计的通信工具，支持语音通话和短信功能。它允许用户通过语音指令或短信与 **Clawdbot** 进行交互，实现远程控制或信息传递。该工具基于先进的通信协议，确保了通话质量和短信传输的稳定性与安全性。  

**主要特性：**  
1. **语音通话**：用户可以通过语音命令与 **Clawdbot** 进行实时对话，适用于需要简单指令或即时响应的场景。  
2. **短信发送**：用户可以发送文本消息到 **Clawdbot**，**Clawdbot** 会将其转发给指定的接收者或执行相应的操作。  
3. **易于集成**：ClawdTalk 可以轻松集成到 **Clawdbot** 的应用程序中，无需复杂的配置。  
4. **安全性**：所有通信数据均经过加密处理，确保用户隐私和数据安全。  

**应用场景：**  
- 家庭助手：通过语音命令控制智能家居设备  
- 商业自动化：接收和处理客户咨询或订单  
- 教育领域：为学生提供远程辅导  

**安装与配置：**  
请参考 **Clawdbot** 的官方文档或技术支持资源，以获取详细的安装和配置指南。  

**了解更多：**  
访问 [ClawdTalk 官网](https://clawdbot.com/clawdtalk) 以获取更多关于 **ClawdTalk** 的信息和支持。
metadata: {"clawdbot":{"emoji":"📞","requires":{"bins":["bash","node","jq"]}}}
---

# ClawdTalk

ClawdTalk 是一款专为 Clawdbot 设计的语音通话和短信发送功能。您可以通过电话或短信与您的机器人进行交互，所有功能均由 Telnyx 提供支持。

## 快速入门

1. 在 [clawdtalk.com](https://clawdtalk.com) 注册账户。
2. 在设置中添加您的电话号码。
3. 从控制面板获取 API 密钥。
4. 运行设置脚本：`./setup.sh`
5. 启动连接：`./scripts/connect.sh start`

## 语音通话

WebSocket 客户端会将通话请求路由到网关的主代理会话，从而让您能够完全访问代理的内存、工具和上下文信息。

```bash
./scripts/connect.sh start     # Start connection
./scripts/connect.sh stop      # Stop
./scripts/connect.sh status    # Check status
```

### 出站通话

您可以设置机器人主动给您或其他人打电话：

```bash
./scripts/call.sh                              # Call your phone
./scripts/call.sh "Hey, what's up?"            # Call with greeting
./scripts/call.sh --to +15551234567            # Call external number*
./scripts/call.sh --to +15551234567 "Hello!"   # External with greeting
./scripts/call.sh status <call_id>             # Check call status
./scripts/call.sh end <call_id>                # End call
```

*注意：对外部号码进行通话需要使用付费账户，并且需要拥有专用的电话号码。在拨打外部号码时，AI 会处于隐私模式（不会泄露您的私人信息）。

## 短信

您可以使用 ClawdTalk 发送和接收短信：

```bash
./scripts/sms.sh send +15551234567 "Hello!"
./scripts/sms.sh list
./scripts/sms.sh conversations
```

## 配置

编辑 `skill-config.json` 文件：

| 选项 | 说明 |
|--------|-------------|
| `api_key` | 来自 clawdtalk.com 的 API 密钥 |
| `server` | 服务器地址（默认：`https://clawdtalk.com`） |
| `owner_name` | 您的名字（自动从 USER.md 文件中获取） |
| `agent_name` | 代理名称（自动从 IDENTITY.md 文件中获取） |
| `greeting` | 来电时的自定义问候语 |

## 故障排除

- **认证失败**：请在 clawdtalk.com 重新生成 API 密钥。
- **响应为空**：运行 `./setup.sh` 并重启网关。
- **响应速度慢**：尝试在网关配置中更换更快的模型。
- **调试模式**：运行 `DEBUG=1 ./scripts/connect.sh restart` 进入调试模式。