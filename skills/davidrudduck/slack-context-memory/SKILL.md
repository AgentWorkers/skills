---
name: slack-context-memory
description: Slack通道的对话摘要与上下文压缩功能：通过语义摘要保留关键信息，可将上下文窗口的使用量减少70%至99%。
---

# Slack上下文记忆功能

将Slack对话历史压缩成可搜索的摘要，以提升会话的效率。

## 解决的问题

随着对话历史的增长，Clawdbot的会话上下文容易丢失。本功能能够：
1. **检测Slack消息历史中的对话边界**；
2. **生成结构化的摘要**（包括核心内容、决策、讨论主题和结果）；
3. **将摘要与嵌入向量一起存储**，以便进行语义搜索；
4. **压缩对话内容**——用少量摘要替代成百上千条消息；
5. **实现语义检索**——帮助用户快速找到相关的过往讨论。

## 快速入门

```bash
# Setup database schema
cd /home/david/clawd/scripts/slack-context-memory
node setup-schema.js

# View compacted context for a channel
node context-compactor.js C0ABGHA7CBE

# Compare original vs compacted size
node context-compactor.js C0ABGHA7CBE --compare

# Search for relevant conversations
node context-compactor.js --query "email newsletter filtering"
```

## 令牌节省情况

| 频道 | 原始数据量（令牌数） | 压缩后数据量（令牌数） | 节省比例 |
|---------|-----------------|-----------------|-----------|
| #accounts（1000条消息） | 112,000个令牌 | 951个令牌 | **99.2%** |
| #homeassistant（50条消息） | 3,100个令牌 | 911个令牌 | **70.8%** |

## 组件构成

### 对话检测
```bash
node detect-conversations.js <channel_id>
node detect-conversations.js --all
```

### 上下文压缩
```bash
node context-compactor.js <channel_id> --recent 20
node context-compactor.js <channel_id> --compare
node context-compactor.js --query "search term"
```

### 搜索功能
```bash
node search-conversations.js semantic "query"
node search-conversations.js text "query"
node search-conversations.js recent --limit 10
```

## 所需环境

- 配备pgvector的PostgreSQL数据库；
- Node.js 18及以上版本；
- 数据库中存储Slack消息历史记录。

## 数据库架构

`conversation_summaries`表包含以下字段：
- `tldr`：1-2句话的摘要；
- `full_summary`：详细的对话摘要；
- `key_decisions`：做出的决策列表；
- `topics`：讨论的主题列表；
- `outcome`：讨论的结果（已解决、进行中或需要跟进）；
- `embedding`：用于语义搜索的嵌入向量（1024维）。

---

由Clawdbot开发 | 2026-01-28