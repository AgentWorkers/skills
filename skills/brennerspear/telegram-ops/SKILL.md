---
name: telegram-ops
description: Telegram机器人API用于论坛管理。支持创建/编辑/归档论坛主题、设置主题图标，以及通过机器人API管理Telegram群组。在归档频道或主题时需要使用OpenClaw配置中的机器人令牌。
---

# Telegram 操作管理

用于管理 Telegram 论坛主题和机器人 API 操作。

## 先决条件

- 机器人必须在具有 `can_manage_topics` 权限的群组中担任管理员。
- 从 OpenClaw 配置中获取机器人令牌：
  ```bash
  gateway action=config.get | jq -r '.result.parsed.channels.telegram.botToken'
  ```

## 创建主题

创建主题时，请按照以下步骤操作：

1. **通过 Telegram 机器人 API 创建主题**（返回 `message_thread_id`）。
2. **设置图标**——选择与主题内容相符的图标（参见 [图标参考](#topic-icons)）。
3. **选择相关技能**——运行 `openclaw skills list`，仅选择符合主题需求的可用技能。
4. **编写系统提示**——为机器人提供关于该主题的上下文说明。
5. **更新 OpenClaw 配置**——将主题及其关联的技能注册到系统中。

### 第 1 步：通过机器人 API 创建主题

```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/createForumTopic" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": <GROUP_ID>,
    "name": "topic name"
  }'
```

返回 `message_thread_id`（主题 ID）——后续步骤都需要这个 ID。

### 第 2 步：设置图标

```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/editForumTopic" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": <GROUP_ID>,
    "message_thread_id": <TOPIC_ID>,
    "name": "topic name",
    "icon_custom_emoji_id": "<EMOJI_ID>"
  }'
```

### 第 3-5 步：配置 OpenClaw

更新配置以注册主题及其系统提示：

```bash
gateway action=config.patch raw='{"channels":{"telegram":{"groups":{"<GROUP_ID>":{"topics":{"<TOPIC_ID>":{"systemPrompt":"Topic-specific instructions"}}}}}}}'
```

主题的配置会继承自其所属的父组——只需指定需要覆盖的设置即可。

**请勿添加 `skills` 键**——省略该键意味着所有技能都将被启用。只有在有特殊原因需要限制主题功能时才需要对其进行限制。

## 会话键

每个主题都有自己的独立 OpenClaw 会话：

```
agent:main:telegram:group:<GROUP_ID>:topic:<TOPIC_ID>
```

每个会话都有独立的对话记录、上下文窗口和数据压缩机制。

## 主题图标

| 表情符号 | ID | 用途 |
|-------|-----|----------|
| ⚡ | `5312016608254762256` | 操作管理、快速提示、警报 |
| 💡 | `5312536423851630001` | 意见和建议 |
| 📰 | `5434144690511290129` | 新闻、公告 |
| 🔥 | `5312241539987020022` | 热门话题、紧急事项 |
| ❤️ | `5312138559556164615` | 社区动态、互动交流 |
| 📝 | `5373251851074415873` | 笔记、文档 |
| 🤖 | `5309832892262654231` | 机器人、自动化 |
| 💬 | `5417915203100613993` | 聊天、讨论 |
| 📊 | `5350305691942788490` | 统计数据、分析报告 |
| 🎯 | `5418085807791545980` | 目标、计划 |

完整的图标 ID 列表请参见 `references/emoji-ids.md`。

**获取所有有效的图标 ID：**
```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/getForumTopicIconStickers"
```

## 归档主题

归档流程：使用前缀 `[ARCHIVED` 重命名主题，设置文件夹图标，关闭该主题，然后处理相应的 OpenClaw 会话。

### 第 1 步：在 Telegram 中归档主题

使用归档脚本：
```bash
scripts/archive_topic.sh <TOKEN> <GROUP_ID> <TOPIC_ID> "Current Topic Name"
```

该脚本将：
- 将主题重命名为 `[ARCHIVED] 当前主题名称`。
- 设置文件夹图标为 📁（ID：`5357315181649076022`）。
- 关闭该主题（使其无法接收新消息）。

### 第 2 步：导出并删除 OpenClaw 会话

```bash
# Export session history to the sessions archive folder
openclaw sessions history 'agent:main:telegram:group:<GROUP_ID>:topic:<TOPIC_ID>' > ~/.openclaw/agents/main/sessions/archive/<topic-name>-<date>.md

# Delete the session (manual - remove from sessions.json and delete transcript)
# Session key: agent:main:telegram:group:<GROUP_ID>:topic:<TOPIC_ID>
```

### 第 3 步：清理配置（可选）

如果主题有自定义设置，请从 OpenClaw 配置中删除该主题的相关信息：
```bash
gateway action=config.patch raw='{"channels":{"telegram":{"groups":{"<GROUP_ID>":{"topics":{"<TOPIC_ID>":null}}}}}}'
```

## 限制

**目前没有 `getForumTopicInfo` 方法**，无法通过主题 ID 查询主题名称。

**解决方法：**
1. 从 `forum_topic_created` 事件中缓存主题名称。
2. 将主题名称存储在本地配置中。
3. 监控主题创建的相关通知信息。