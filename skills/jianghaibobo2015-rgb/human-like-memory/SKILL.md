---
name: human-like-memory
description: 该技能可帮助用户实现长期记忆功能，便于回顾过去的对话、将重要信息存储在记忆中、搜索记忆内容，或在需要参考之前交互的上下文时使用。当用户说出“记住”、“回想一下”、“我们讨论了什么”、“把这个信息保存下来”或“搜索记忆”等短语时，该技能会被触发。
version: 0.1.0
secrets:
  - name: HUMAN_LIKE_MEM_API_KEY
    description: API Key for Human-Like Memory service (get from https://multiego.me)
    required: true
  - name: HUMAN_LIKE_MEM_BASE_URL
    description: Base URL for Memory API
    required: false
    default: https://multiego.me
  - name: HUMAN_LIKE_MEM_USER_ID
    description: User identifier for memory isolation
    required: false
    default: openclaw-user
---
# 类人类记忆功能

该功能提供了长期记忆能力，使您能够回忆过去的对话并保存重要信息以供后续使用。

## 功能

1. **回忆记忆** - 根据当前上下文搜索并检索相关记忆内容。
2. **保存记忆** - 将对话中的重要信息存储起来以备将来参考。
3. **搜索记忆** - 明确地在记忆中搜索特定主题。

## 使用方法

### 自动记忆回忆

当用户提出可能需要参考过去上下文的问题时，使用记忆回忆脚本：

```bash
node ~/.openclaw/skills/human-like-memory/scripts/memory.mjs recall "user's question or topic"
```

### 保存到记忆中

在重要的对话结束后，或当用户要求记住某些内容时：

```bash
node ~/.openclaw/skills/human-like-memory/scripts/memory.mjs save "user message" "assistant response"
```

### 搜索记忆

当用户明确希望搜索自己的记忆时：

```bash
node ~/.openclaw/skills/human-like-memory/scripts/memory.mjs search "search query"
```

## 记忆响应格式

当回忆到记忆内容时，以自然的方式呈现给用户。不要提及“记忆检索”或“数据库”等字眼，只需将相关内容融入回答中。

示例：
- 不佳的回答：「根据我的记忆数据库，您提到过……」
- 优秀的回答：「正如我们之前讨论的，您提到过……」

## 重要准则

1. **隐私**：记忆数据属于用户本人。切勿分享或引用其他用户的记忆内容。
2. **相关性**：仅回忆与当前对话直接相关的记忆。
3. **时效性**：在记忆内容存在冲突时，优先选择较新的记忆。
4. **验证**：如果记忆内容似乎过时或与用户的当前陈述相矛盾，请相信用户的当前陈述。

## 配置

该功能需要以下配置（通过 OpenClaw 的秘钥进行设置）：

| 秘钥          | 是否必填 | 说明                          |
|---------------|---------|-----------------------------------|
| `HUMAN_LIKE_MEM_API_KEY` | 是       | 来自 https://multiego.me 的 API 密钥                |
| `HUMAN_LIKE_MEM_BASE_URL` | 否       | API 端点（默认：https://multiego.me）                |
| `HUMAN_LIKE_MEM_USER_ID` | 否       | 用于区分不同用户记忆的用户 ID                        |

## 错误处理

如果记忆操作失败：
1. 继续正常进行对话，无需提及记忆内容。
2. 不要重复尝试失败的操作。
3. 仅当用户明确请求记忆操作时，才向其告知操作失败的情况。