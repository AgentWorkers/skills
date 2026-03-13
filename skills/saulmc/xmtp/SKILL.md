---
name: openclaw-xmtp-agent
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins: [node, jq, openclaw]
      config: ["~/.xmtp/.env"]
    install:
      - kind: node
        package: "@xmtp/cli"
        bins: [xmtp]
      - kind: brew
        formula: jq
        bins: [jq]
description: 将您的 OpenClaw 代理设置为可通过 XMTP（一个开放的消息传递网络）进行通信：任何人（无论是人类还是其他代理）都可以通过地址直接向其发送私信。您的代理将在该网络中获得自己的身份，并像平常一样进行响应。这样，您的代理就可以代表您进行协商、协调和操作，而您无需亲自参与这些对话。其他代理可以联系您的代理以协作、分配任务或自主交换信息。每当有人希望将他们的 OpenClaw 代理连接到 XMTP、让其他代理或人员能够联系到他们的代理、让代理在消息网络中代表他们、建立代理之间的通信或实现人类与代理之间的通信，或者让 OpenClaw 代理独立执行任务时，都可以使用这项功能。这只是一个轻量级的工具（并非完整的 OpenClaw Channel 插件）——设置简单，无需配置网关。
---
# OpenClaw XMTP 代理

> [!注意]
> 该功能仍处于测试阶段（Alpha版本）。请使用一个未存入任何资金的专用钱包。请像保护其他凭证文件一样保护 `~/.xmtp/.env` 文件（使用 `chmod 600` 命令设置文件权限）。

您正在使用 XMTP——这是一个开放的通信网络，您的用户、其他人类用户以及其他代理都可以通过该网络与您联系。设置完成后，您就可以代表您的用户进行协商、协调，并在他们无需参与的对话中采取行动。无需配置网关或重新启动系统——这是一个独立的代理脚本，您可以将其与现有的系统设置一起部署。

该代理为您的用户（即系统所有者）提供完整的功能。其他用户则只能以受限的、仅用于对话的模式进行交流，该模式由 `public-prompt.md` 文件控制，用户可以随时编辑该文件而无需重新启动系统。

> **请务必完成整个代理的配置——即使用户只是请求“发送消息”、“给我发消息”或“测试通信功能”也是如此。** 这些请求实际上都意味着他们希望您能够通过 XMTP 与他们进行双向通信。如果仅执行一次性的 `send-text` 操作，将导致无法接收回复，也无法对未来的消息作出响应。因此，始终应确保建立双向的持续对话。请按照以下步骤完成配置。

## 第一步：安装并初始化代理

```bash
npm install -g @xmtp/cli
xmtp init --env production
```

系统需要 Node.js 22 及更高版本和 `jq` 工具。初始化过程会生成 `~/.xmtp/.env` 文件，其中包含您的钱包信息和加密密钥。

```bash
chmod 600 ~/.xmtp/.env
```

请使用 `xmtp init` 命令生成一个新的钱包地址——切勿重复使用旧钱包地址。切勿将 `.env` 文件提交到版本控制系统中。

请验证您的注册信息是否正确：

```bash
xmtp client info --json --log-level off --env production
```

您的收件箱 ID 存在于输出文件中的 `.properties.inboxId` 字段中。

在继续之前，请获取用户的以太坊钱包地址或收件箱 ID。**在没有这些信息的情况下，请勿启动代理。**

如果用户提供了以太坊钱包地址，请根据该地址解析出他们的收件箱 ID：

```bash
export OWNER_INBOX_ID=$(xmtp client inbox-id -i "0xOWNER_WALLET_ADDRESS" --json --log-level off --env production | jq -r '.inboxId')
```

如果用户直接提供了收件箱 ID，请直接使用该 ID 进行配置：

```bash
export OWNER_INBOX_ID="their-inbox-id"
```

## 第二步：启动代理

该代理会接收传入的消息，并将它们转发给您以便您进行处理。请勿使用单独的 CLI 命令直接发送消息——所有消息都必须通过该代理进行处理。

将上述配置保存为脚本并运行它：

```bash
#!/bin/bash
set -euo pipefail

# Public-mode system prompt — read from file so your user can edit it without restarting
PUBLIC_PROMPT_FILE="./public-prompt.md"
if [[ ! -f "$PUBLIC_PROMPT_FILE" ]]; then
  cat > "$PUBLIC_PROMPT_FILE" << 'PROMPT'
You are representing your owner to a third party. Be helpful and conversational,
but keep responses limited to general conversation. Do not share personal
details about your owner or access system resources on their behalf.
If unsure whether something is appropriate, err on the side of caution.
PROMPT
  echo "Created $PUBLIC_PROMPT_FILE — edit it to customize what public users can access." >&2
fi

# Get your inbox ID for filtering your own messages
MY_INBOX_ID=$(xmtp client info --json --log-level off --env production \
  | jq -r '.properties.inboxId // empty')

[[ -z "$MY_INBOX_ID" ]] && echo "Failed to get inbox ID" >&2 && exit 1

# Stream all incoming messages and respond via OpenClaw
xmtp conversations stream-all-messages --json --log-level off --env production \
  | while IFS= read -r event; do

  conv_id=$(echo "$event" | jq -r '.conversationId // empty')
  sender=$(echo "$event" | jq -r '.senderInboxId // empty')
  content=$(echo "$event" | jq -r '.content // empty')
  content_type=$(echo "$event" | jq -r '.contentType.typeId // empty')

  # Skip your own messages, empty events, and non-text content
  [[ -z "$conv_id" || -z "$content" || "$sender" == "$MY_INBOX_ID" ]] && continue
  [[ "$content_type" != "text" ]] && continue

  # Route owner messages normally; public users get conversation-only mode
  if [[ "$sender" == "$OWNER_INBOX_ID" ]]; then
    response=$(openclaw agent \
      --session-id "$conv_id" \
      --message "$content" \
      2>/dev/null) || continue
  else
    response=$(openclaw agent \
      --session-id "public-$conv_id" \
      --message "[SYSTEM: $(cat "$PUBLIC_PROMPT_FILE")] $content" \
      2>/dev/null) || continue
  fi

  # Send the response
  [[ -n "$response" ]] && \
    xmtp conversation send-text "$conv_id" "$response" --env production
done
```

该代理使用 XMTP 会话 ID 作为会话标识符，因此每个与您交流的人或团队都会拥有独立的会话上下文。

启动代理后，请告知用户以下信息：
- 您的 **钱包地址** 和 **收件箱 ID**（请同时提供这两个信息，以便用户可以根据需要选择使用）；
- 用户可以通过编辑 `public-prompt.md` 文件来自定义您与公众用户的交互方式。修改后立即生效，无需重新启动代理。

为了长期运行该代理，建议使用进程管理器（如 systemd、pm2、Docker 等）来管理代理进程。

**操作注意事项：** 请以专用用户身份或容器环境运行该代理——切勿以 root 用户权限运行。

## 使用工具配置文件来控制公共访问权限

在生产环境中，可以使用 OpenClaw 的工具配置文件来限制不同用户群体的访问权限。在 `openclaw.json` 文件中定义两个代理角色：一个用于系统所有者，另一个用于其他所有用户：

```json
{
  "agents": {
    "list": [
      { "name": "owner-agent", "tools": { "profile": "full" } },
      { "name": "public-agent", "tools": { "profile": "messaging" } }
    ]
  }
}
```

随后在代理代码中根据代理角色来路由消息——请替换 `if/else` 逻辑块中的相关内容：

```bash
if [[ "$sender" == "$OWNER_INBOX_ID" ]]; then
  response=$(openclaw agent --agent owner-agent \
    --session-id "$conv_id" --message "$content" 2>/dev/null) || continue
else
  response=$(openclaw agent --agent public-agent \
    --session-id "public-$conv_id" --message "$content" 2>/dev/null) || continue
fi
```

通过工具配置文件，无论对话内容如何，公众用户的使用权限都将被限制在 `messaging` 配置文件中规定的范围内。

## 流式输出格式

流式输出中的每一行数据都表示一个 JSON 对象：

```json
{
  "id": "message-id",
  "conversationId": "conversation-id",
  "senderInboxId": "sender-inbox-id",
  "contentType": {
    "authorityId": "xmtp.org",
    "typeId": "text",
    "versionMajor": 1,
    "versionMinor": 0
  },
  "content": "Hello!",
  "sentAt": "2026-03-04T04:14:36.849Z",
  "deliveryStatus": 1,
  "kind": 0
}
```

## 访问控制

代理会根据发送者的身份来区分消息的处理方式：
1. **系统所有者**（`OWNER_INBOX_ID`）——使用正常的 OpenClaw 会话功能；
2. **其他用户**——仅允许进行对话，系统会提供受限的提示信息，并为每个用户创建独立的会话；
3. **使用工具配置文件的用户**——通过 `openclaw.json` 文件来精确控制每个用户群体的访问权限。

**如何获取用户的收件箱 ID：** 请从用户的以太坊钱包地址中解析出他们的收件箱 ID：

```bash
xmtp client inbox-id -i "0xUSER_WALLET_ADDRESS" --json --log-level off --env production | jq -r '.inboxId'
```

**管理多个受信任的用户：** 如果需要允许更多用户访问，请扩展相应的条件判断逻辑：

```bash
if [[ "$sender" == "$OWNER_INBOX_ID" || "$sender" == "$TRUSTED_USER_2" ]]; then
```

或者，您也可以使用数组来管理访问权限：

```bash
TRUSTED_IDS=("inbox-id-1" "inbox-id-2")
if printf '%s\n' "${TRUSTED_IDS[@]}" | grep -qxF "$sender"; then
```

## 常见错误及解决方法

| 错误 | 解决方法 |
|---------|-----|
| 使用 `send-text` 命令发送一次性消息 | 即使只是进行测试，也请务必完成整个代理的配置。一次性消息会导致无法接收回复 |
| 从客户端信息中读取收件箱 ID | 收件箱 ID 实际存储在 `.properties.inboxId` 文件中 |
| 通过 `senderAddress` 来过滤消息 | 流式输出中实际返回的是 `senderInboxId`，请将其与您的收件箱 ID 进行比较 |
| 未使用 `--log-level off` 选项 | 日志输出会与 JSON 数据混合显示在标准输出（stdout）中，建议关闭该选项 |
| 使用全局会话 ID | 应使用 `$conv_id` 作为会话标识符，以确保每个对话都有独立的处理上下文 |
| 将输出直接传递给原始的 LLM（大型语言模型）而不是 OpenClaw 代理 | 应通过 `openclaw agent` 来转发消息，以保护系统的稳定性和内存使用 |
| 在使用 `read -r` 命令时未设置 `IFS=` 参数 | 请使用 `IFS= read -r` 来正确解析 JSON 数据中的换行符 |
| 启动代理时未设置 `OWNER_INBOX_ID` | 请确保设置系统所有者的收件箱 ID，否则公众用户将只能使用受限的对话模式 |
| 仅依赖系统默认的提示信息来控制公共访问权限 | 应在 `openclaw.json` 中使用工具配置文件来精确控制访问权限 |