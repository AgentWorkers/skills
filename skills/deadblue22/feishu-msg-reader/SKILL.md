---
name: feishu-message
description: >
  **根据 `message_id` 获取 Feishu 消息内容（可选包含线程上下文）**  
  **使用场景：**  
  - 需要根据 `message_id` 读取特定 Feishu 消息的内容；  
  - 需要获取消息所属的线程上下文；  
  - 遇到 `[Interactive Card]` 占位符文本时。  
  **支持的消息类型：**  
  - text  
  - post  
  - interactive（仅作为备用方案）  
  - image  
  - merge_forward
---
# Feishu 消息获取器

通过 `message_id` 使用 IM API 获取 Feishu 消息内容，支持可选的线程上下文（thread context）。

## 已知限制

**交互式卡片**（`msg_type: interactive`）：Feishu 的 GET 消息 API（`/im/v1/messages/{id}`）仅在 `body.content` 中返回 **降级后的文本**，而不会返回完整的卡片 JSON 数据。这是 Feishu 平台的限制——目前没有 API 可以在消息发送后检索到渲染后的卡片结构。

**解决方法**：使用 `--thread` 参数来获取整个线程的上下文。交互式卡片通常是对包含实际内容的文本或帖子的回复。通过读取整个线程，您可以获取完整的消息信息。

## 使用方法

```bash
# Fetch a single message
python3 scripts/fetch_message.py <message_id>

# Fetch with thread context (root message + all replies in thread)
python3 scripts/fetch_message.py <message_id> --thread

# Raw API response
python3 scripts/fetch_message.py <message_id> --raw
```

## 身份验证

系统会自动从 `~/.openclaw/openclaw.json` 文件中读取 `appId`/`appSecret`。或者，您也可以设置 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 环境变量，或者通过 `--token <tenant_access_token>` 传递访问令牌。

## 输出结果

输出结果为 JSON 格式，包含以下字段：
- `message_id`
- `msg_type`
- `sender_id`
- `sender_type`
- `chat_id`
- `create_time`
- `root_id`
- `parent_id`
- `content`（已解析的内容）

如果使用了 `--thread` 参数，输出结果还会包含 `thread` 数组（按时间顺序排列的同一线程中的所有消息）和 `thread_count`。

## 典型工作流程

当您在回复消息中看到 `[Interactive Card]` 时，请按照以下步骤操作：
1. 从传入的元数据（`has_reply_context`、父消息信息）中获取 `message_id`。
2. 运行 `fetch_message.py <parent_message_id> --thread` 命令。
3. 线程上下文中将包含包含实际内容的文本或帖子。
4. 使用这些内容来满足用户的需求。