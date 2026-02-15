---
name: whisper-context
version: 0.1.0
description: OpenClaw 的官方 Whisper Context 技能：通过差分压缩（delta compression）和缓存机制来处理上下文数据，并在会话之间实现数据的长期存储（即数据在会话结束后仍可被访问）。
author: "Whisper"
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

# Whisper Context（OpenClaw技能）

通过减少发送给模型的上下文数据量（采用差分压缩和缓存技术），来降低OpenClaw API的使用成本，同时确保数据在会话之间得以持久保存。

该技能提供了一个基于Node.js的辅助工具（`whisper-context.mjs`），OpenClaw代理可以通过该工具执行以下操作：

- 使用`compress: true`和`compression_strategy: "delta"`查询用户的会话上下文数据（`query_context`）。
- 将最新的对话内容保存到长期内存中（`ingest_session`）。
- 写入或搜索内存数据（`memory_write`、`memory_search`）。
- 执行Oracle搜索或查询（`oracle_search`）。
- 获取成本分析信息（`get_cost_summary`）。
- 检查或刷新缓存（`cache_stats`、`cache_warm`）。

## 安装（ClawHub）

```bash
npx clawhub@latest install whisper-context
```

请将`whisper-context`技能文件夹安装到OpenClaw的技能工作目录中（通常为`~/.openclaw/workspace/skills/`）。

## 设置

配置环境变量（OpenClaw会在其中读取代理的相关信息）：

```bash
WHISPER_CONTEXT_API_URL=https://context.usewhisper.dev
WHISPER_CONTEXT_API_KEY=YOUR_KEY
WHISPER_CONTEXT_PROJECT=openclaw-cost-optimization
```

**注意：**
- `WHISPER_CONTEXT_API_URL`是可选的（默认值为`https://context.usewhisper.dev`）。
- `WHISPER_CONTEXT PROJECT`可以是一个项目标识符或名称。
- 如果该项目尚不存在，该辅助工具会在首次使用时自动在您的组织中创建该项目。
- 为获得最佳的内存管理效果，请使用稳定的`user_id`和`session_id`值（不要全局硬编码这些值，应在代理中根据用户和会话动态生成）。

## 使用方法

所有命令都会将结果以JSON格式输出到标准输出（stdout）。

### 全局参数
- `--project <slugOrName>`：覆盖`WHISPER_CONTEXTPROJECT`的值。
- `--api_url <url>`：覆盖`WHISPER_CONTEXT_API_URL`的值。
- `--timeout_ms <n>`：请求超时时间（默认值：30000毫秒）。

### 对于实际代理的建议（以降低API使用成本）：
- 请始终先调用`query_context`，然后使用返回的上下文数据，而不是重新发送整个聊天历史记录。
- 保持`compress: true`、`compression_strategy: "delta"`和`use_cache: true`的设置（这些是该辅助工具的默认值），以最大限度地节省API调用次数。
- 使用稳定的`user_id`和`session_id`值，以确保数据在会话之间能够被正确保存，并使缓存键保持有效性。

### 查询压缩后的上下文数据

```bash
node whisper-context.mjs query_context \
  --query "What did we decide about the retriever cache?" \
  --user_id "user-123" \
  --session_id "session-123"
```

### 保存完整的对话内容

```bash
node whisper-context.mjs ingest_session \
  --user_id "user-123" \
  --session_id "session-123" \
  --user "..." \
  --assistant "..."
```

如果您的消息文本较长或难以通过shell转义，请通过标准输入（stdin）传递JSON数据：

```bash
echo '{ "user": "....", "assistant": "...." }' | node whisper-context.mjs ingest_session --session_id "session-123" --turn_json -
```

## 安全/隐私注意事项：
- `ingest_session`会将用户和助手的对话内容一起发送到Context API，以便构建内存数据并优化查询效率。
- 除非您明确指定`@path`（或通过`-`参数使用stdin），否则该辅助工具只会读取本地文件。
- 请将`WHISPER_CONTEXT_API_KEY`视为敏感信息，切勿将其提交到Git仓库中。

### 写入内存数据

```bash
node whisper-context.mjs memory_write \
  --memory_type "preference" \
  --content "User prefers concise answers." \
  --user_id "user-123"
```

### 搜索内存数据

```bash
node whisper-context.mjs memory_search \
  --query "preferences" \
  --user_id "user-123"
```

### 执行Oracle搜索或查询

```bash
node whisper-context.mjs oracle_search --query "How does delta compression work?" --mode search
node whisper-context.mjs oracle_search --query "Design a plan..." --mode research --max_steps 3
```

### 获取成本分析信息

```bash
node whisper-context.mjs get_cost_summary \
  --start_date "2026-01-01T00:00:00.000Z" \
  --end_date "2026-02-01T00:00:00.000Z"
```

### 查看缓存使用情况（验证节省效果）

```bash
node whisper-context.mjs cache_stats
```

### 刷新缓存（可选）

```bash
node whisper-context.mjs cache_warm --queries "retriever cache,l1 query cache,delta compression" --ttl_seconds 3600
```

## 代理集成步骤：
1. 在调用模型之前：先运行`query_context`，并将返回的上下文数据（如果有的话）添加到提示信息中。
2. 在回复用户后：运行`ingest_session`，将用户和助手的对话内容保存到内存中。

## 故障排除：
- 如果出现“Missing WHISPER_CONTEXT_API_KEY”错误，请检查OpenClaw运行命令时是否正确设置了环境变量。
- 如果遇到HTTP 401/403错误，请验证您的API密钥以及该密钥是否具有访问项目的权限。
- 如果出现“HTTP 404 Project not found”错误，请确认`WHISPER_CONTEXT PROJECT`（项目标识符/名称）是否存在。