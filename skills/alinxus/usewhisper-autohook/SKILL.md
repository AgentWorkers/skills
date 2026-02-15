---
name: usewhisper-autohook
version: 1.0.0
description: OpenClaw的自动挂接工具：在每次生成之前查询“Whisper Context”数据，在每个回合结束后将其导入系统。专为Telegram代理（使用稳定的user_id/session_id）设计。
author: "usewhisper"
metadata:
  openclaw:
    requires:
      bins: ["node"]
      env: ["WHISPER_CONTEXT_API_KEY", "WHISPER_CONTEXT_PROJECT"]
      optional_env: ["WHISPER_CONTEXT_API_URL"]
    security:
      notes:
        - Makes outbound HTTPS requests to the Whisper Context API using a user-provided API key.
        - Does not require additional npm dependencies.
        - Review the script before use.
---

# usewhisper-autohook（OpenClaw 技能）

该技能是一个轻量级的封装层，旨在简化“自动记忆”功能的实现：

- `get_whisper_context(user_id, session_id, current_query)`：用于在响应前注入上下文信息。
- `ingest_whisper_turn(user_id, session_id, user_msg, assistant_msg)`：用于在响应后处理用户输入的信息。

该技能默认采用以下设置（这些设置通常是您所需要的）：
- `compress: true`：启用压缩功能。
- `compression_strategy: "delta"`：使用差分压缩算法。
- `use_cache: true`：启用缓存机制。
- `include_memories: true`：包含相关记忆数据。

此外，该技能还会将最新的 `context_hash` 保存在本地（路径为 `api_url + project + user_id + session_id`），因此默认情况下即可使用差分压缩功能，而无需手动传递 `previous_context_hash`。

## 安装（ClawHub）

```bash
npx clawhub@latest install usewhisper-autohook
```

## 设置

在 OpenClaw 运行代理程序的任何位置设置环境变量：

```bash
WHISPER_CONTEXT_API_URL=https://context.usewhisper.dev
WHISPER_CONTEXT_API_KEY=YOUR_KEY
WHISPER_CONTEXT_PROJECT=openclaw-yourname
```

**注意：**
- `WHISPER_CONTEXT_API_URL` 是可选的（默认值为 `https://context.usewhisper.dev`）。
- 如果项目尚不存在，该辅助工具会在首次使用时自动创建该项目。

## “自动循环”提示（复制/粘贴）

将以下代码添加到您的代理程序的 **系统指令** 中（或等效配置中）：

```text
Before you think or respond to any message:
1) Call get_whisper_context with:
   user_id = "telegram:{from_id}"
   session_id = "telegram:{chat_id}"
   current_query = the user's message text
2) If the returned context is not empty, prepend it to your prompt as:
   "Relevant long-term memory:\n{context}\n\nNow respond to:\n{user_message}"

After you generate your final response:
1) Call ingest_whisper_turn with the same user_id and session_id and:
   user_msg = the full user message
   assistant_msg = your full final reply

Always do this. Never skip.
```

如果您使用的是 Telegram 平台，请保持相同的结构；关键在于确保 `user_id` 和 `session_id` 是稳定的。

## 如果您的代理程序仍会重播完整的聊天记录（代理模式）

如果您无法控制代理程序/框架的提示生成方式（它总是发送完整的聊天记录），那么系统提示将无法减少令牌消耗：因为令牌已经发送给了模型。

在这种情况下，可以运行内置的 OpenAI 兼容代理来减少网络数据传输量。该代理会：
- 接收 `POST /v1/chat/completions` 请求。
- 从 Whisper 数据库中查询相关信息。
- 去除聊天记录中的冗余内容，仅保留系统生成的提示和用户的最后一条消息。
- 插入相关的长期记忆数据。
- 调用您的 OpenAI 兼容服务提供商。
- 将处理后的数据重新发送回 Whisper 数据库。

**启动代理程序：**
```bash
export OPENAI_API_KEY="YOUR_UPSTREAM_KEY"
node usewhisper-autohook.mjs serve_openai_proxy --port 8787
```

然后将您的代理程序的 OpenAI 基础 URL 设置为 `http://127.0.0.1:8787`（具体环境配置取决于您的代理程序）。

如果您的代理程序支持自定义上游服务 URL，可以设置以下变量：
- `OPENAI_BASE_URL`（用于 OpenAI 兼容的服务）。
- `ANTHROPIC_BASE_URL`（用于 Anthropic 服务）。

或者在启动代理程序时通过参数 `--upstream_base_url` 指定上游服务的 URL。

为了确保每个用户/会话的数据都能被正确处理，请在每个请求中传递以下请求头：
- `x-whisper-user-id: telegram:{from_id}`：用户 ID。
- `x-whisper-session-id: telegram:{chat_id}`：会话 ID。

### Anthropic 原生代理（`/v1/messages`）

如果您的代理程序使用的是 **Anthropic 的原生 API**（而非 OpenAI 兼容的 API），请运行 Anthropic 代理：

```bash
export ANTHROPIC_API_KEY="YOUR_ANTHROPIC_KEY"
node usewhisper-autohook.mjs serve_anthropic_proxy --port 8788
```

然后将您的代理程序的 Anthropic 基础 URL 设置为 `http://127.0.0.1:8788`。

建议通过请求头传递以下 ID：
- `x-whisper-user-id: telegram:{from_id}`：用户 ID。
- `x-whisper-session-id: telegram:{chat_id}`：会话 ID。

如果您不传递这些请求头，代理程序会尝试从 OpenClaw 的系统提示或会话键中推断出稳定的用户/会话 ID。虽然这是一种尽力而为的解决方案，但使用请求头仍然是最可靠的方法。

## 命令行工具的使用方法

所有命令都会将结果以 JSON 格式输出到标准输出（stdout）。

### 获取打包后的上下文数据

```bash
node usewhisper-autohook.mjs get_whisper_context \
  --current_query "What did we decide last time?" \
  --user_id "telegram:123" \
  --session_id "telegram:456"
```

### 处理已完成的对话轮次

```bash
node usewhisper-autohook.mjs ingest_whisper_turn \
  --user_id "telegram:123" \
  --session_id "telegram:456" \
  --user_msg "..." \
  --assistant_msg "..."
```

对于较大的数据量，可以通过标准输入（stdin）传递 JSON 数据：

```bash
echo '{ "user_msg": "....", "assistant_msg": "...." }' | node usewhisper-autohook.mjs ingest_whisper_turn --session_id "telegram:456" --user_id "telegram:123" --turn_json -
```

## 输出格式

`get_whisper_context` 函数返回以下内容：
- `context`：需要添加到响应前的打包后的上下文字符串。
- `context_hash`：一个简短的哈希值，您可以将其保存并在下次请求时作为 `previous_context_hash` 传递（可选）。
- `meta`：缓存命中情况和压缩相关的信息（有助于调试）。