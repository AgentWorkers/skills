---
name: supermemory
description: 使用 SuperMemory API 存储和检索记忆。可以添加新内容、搜索记忆，还可以与你的知识库进行交流。
metadata: {"moltbot":{"emoji":"🧠","requires":{"env":["SUPERMEMORY_API_KEY"]},"primaryEnv":"SUPERMEMORY_API_KEY"},"user-invocable":true}
---

# SuperMemory

使用 SuperMemory 的 API 来存储、搜索和与您的个人知识库进行交互。

## 设置

配置您的 SuperMemory API 密钥：
```bash
export SUPERMEMORY_API_KEY="sm_oiZHA2HcwT4tqSKmA7cCoK_opSRFViNFNxbYqjkjpVNfjSPqQWCNoOBAcxKZkKBfRVVrEQDVxLWHJPvepxqwEPe"
```

## 使用方法

### 添加记忆内容

**将内容添加到您的记忆库中：**
```bash
# Add a memory with content
supermemory add "Your memory content here"

# Add a memory with a specific description
supermemory add "Important project details" --description "Project requirements"
```

### 搜索记忆内容

**搜索您存储的记忆：**
```bash
supermemory search "search query"
```

### 与记忆库进行对话

**与您的记忆数据库进行对话：**
```bash
supermemory chat "What do you know about my projects?"
```

## 实现细节

### 添加记忆内容

当用户想要存储信息时：
```bash
bash /root/clawd/skills/supermemory/scripts/add-memory.sh "content" "description (optional)"
```

### 搜索记忆内容

当用户想要在记忆中查找信息时：
```bash
bash /root/clawd/skills/supermemory/scripts/search.sh "query"
```

### 与记忆库进行对话

当用户想要以对话的形式查询记忆数据库中的内容时：
```bash
bash /root/clawd/skills/supermemory/scripts/chat.sh "question"
```

## 示例

**存储重要信息：**
- “记住我的 API 密钥是 xyz” → `supermemory add "My API key is xyz" --description "API credentials"`
- “保存这个链接以备后续使用” → `supermemory add "https://example.com" --description "Bookmarked link"`

**查找信息：**
- “我保存了关于 Python 的哪些内容？” → `supermemory search "Python"`
- “找到我关于项目的笔记” → `supermemory search "project notes"`

**查询知识：**
- “我对营销策略了解多少？” → `supermemory chat "What do I know about the marketing strategy?"
- “总结一下我对 AI 的了解” → `supermemory chat "Summarize what I've learned about AI"`