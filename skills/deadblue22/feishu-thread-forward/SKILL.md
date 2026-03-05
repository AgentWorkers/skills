---
name: feishu-thread-forward
description: >
  **通过 REST API 将 Feishu 主题/帖子转发给用户、群组或另一个主题**  
  **适用场景**：  
  - 将某个主题/帖子转发到另一个聊天频道；  
  - 将某个主题的帖子分享到不同的群组中；  
  - 任何涉及 Feishu 主题级别转发的场景。  
  **注意**：  
  Feishu 的内置消息工具不支持主题转发功能，此功能正是为填补这一需求而设计的。
---
# Feishu主题转发

使用Feishu Open API将一个Feishu主题转发给用户、群组或另一个主题。

## 使用场景

- 用户请求将某个主题或帖子转发给另一个群组或用户
- 需要将一个主题帖子从某个群组发布到另一个群组
- 内置的`message`工具无法实现主题级别的转发

## API

```
POST https://open.feishu.cn/open-apis/im/v1/threads/{thread_id}/forward?receive_id_type={type}
```

### 参数

| 参数 | 位置 | 是否必填 | 描述 |
|-------|----------|----------|-------------|
| `thread_id` | path | 是 | 要转发的主题ID（格式：`omt_xxxxx`） |
| `receive_id_type` | query | 是 | 目标ID类型：`open_id`、`chat_id`、`user_id`、`union_id`、`email`、`thread_id` |
| `receive_id` | body | 是 | 与`receive_id_type`匹配的目标ID |
| `uuid` | query | 否 | 用于确保操作幂等的键（最多50个字符，1小时内重复内容会被忽略） |

### 请求头

```
Authorization: Bearer {tenant_access_token}
Content-Type: application/json
```

## 如何获取`thread_id`

主题群组中的消息包含一个`thread_id`字段。可以通过以下方式获取：

```
GET https://open.feishu.cn/open-apis/im/v1/messages/{message_id}
```

响应中的`data.items[0].thread_id`包含主题ID（例如：`omt_1accc5a75c0f9b93`）。

## 脚本

使用`scripts/forward_thread.py`来实现完整的转发功能。

```bash
python3 skills/feishu-thread-forward/scripts/forward_thread.py \
  --thread-id omt_xxxxx \
  --receive-id oc_xxxxx \
  --receive-id-type chat_id
```

## 典型流程

1. **获取`thread_id`** — 从消息的元数据中获取，或通过调用GET消息API获取
2. **调用转发API** — `POST /im/v1/threads/{thread_id}/forward`
3. **结果** — 转发的主题将以可点击的主题卡片的形式显示在目标聊天中

## 转发（Thread Forward）与合并转发（Merge Forward）与普通消息转发（Message Forward）的区别

| 方法 | API | 结果 |
|--------|-----|--------|
| **主题转发**（本功能） | `POST /threads/{thread_id}/forward` | 以可点击的主题卡片形式显示，包含主题的上下文 ✅ |
| 合并转发 | `POST /messages/merge_forward` | 以“群聊会话记录”的形式显示，包含所有相关消息 |
| 普通消息转发 | `POST /messages/{message_id}/forward` | 将单条消息复制到目标群组，丢失主题的上下文 |

**主题转发**是用户在Feishu客户端点击“转发话题”时看到的结果。

## 先决条件

- 机器人必须位于源群组中（并且能够看到该主题）
- 机器人必须位于目标群组中（或者目标用户必须在机器人的可用范围内）
- 机器人需要具有`im:message`或`im:message:send_as_bot`权限

## 认证信息

从`/root/.openclaw/openclaw.json`文件中读取`channels.feishu.appId`和`channels.feishu.appSecret`以获取`tenant_access_token`。

## 错误代码

| 代码 | 含义 |
|------|---------|
| 230002 | 机器人不在目标群组中 |
| 230013 | 目标用户不在机器人的可用范围内 |
| 230064 | 主题ID无效 |
| 230066 | 该主题属于保密群组，无法转发 |
| 230070 | 该主题的群组启用了防泄露模式 |
| 230073 | 机器人无法看到该主题（在主题创建后加入，且主题历史记录被隐藏） |