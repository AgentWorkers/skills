---
name: mem0
description: >
  Clawdbot的智能记忆层基于Mem0技术实现，支持语义搜索功能，并能自动存储用户偏好、行为模式以及对话中的相关上下文信息。该功能在以下场景下非常有用：  
  1. 当用户明确要求“记住某件事”时；  
  2. 在对话过程中学习用户的偏好或行为模式；  
  3. 查找用户之前的选择或偏好记录；  
  4. 根据用户的行为习惯生成个性化的响应。  
  该智能记忆层与MEMORY.md（用于存储结构化信息）相辅相成，共同构成了Clawdbot的动态、交互式记忆系统——能够记录用户的个性化数据，并据此提供更加智能的交互体验。
  Intelligent memory layer for Clawdbot using Mem0. Provides semantic search and automatic storage of user preferences, patterns, and context across conversations. Use when (1) User explicitly says "remember this", (2) Learning user preferences or patterns during conversation, (3) Searching for past context about user's choices/preferences, (4) Building adaptive responses based on learned user behavior. Complements MEMORY.md (structured facts) with dynamic, conversational memory (learned preferences, patterns, adaptive context).
---
# Mem0内存集成

Mem0为Clawdbot添加了一个智能、自适应的内存层，该层能够自动学习并记住用户在所有交互中的偏好、模式和上下文信息。

## 核心工作流程

### 1. 回答前先搜索
在回答用户问题之前，先在mem0中搜索相关的上下文信息：

```bash
node scripts/mem0-search.js "user preferences" --limit=3
```

使用检索到的记忆信息来：
- 个性化回复
- 记住用户的偏好
- 回忆过去的交互模式
- 适应沟通风格

### 2. 交互后进行存储

**显式存储**（当用户要求“记住某件事”时）：
```bash
node scripts/mem0-add.js "Abhay prefers concise updates"
```

**对话存储**（用于学习上下文）：
```bash
# Pass messages as JSON
node scripts/mem0-add.js --messages='[{"role":"user","content":"I like brief updates"},{"role":"assistant","content":"Got it!"}]'
```

## 可用命令

### 搜索记忆
```bash
node scripts/mem0-search.js "query text" [--limit=3] [--user=abhay]
```

在存储的记忆中执行语义搜索，并按相关性排序返回结果。

### 添加记忆
```bash
# Simple text
node scripts/mem0-add.js "memory text" [--user=abhay]

# Conversation messages (auto-extracts memories)
node scripts/mem0-add.js --messages='[{...}]' [--user=abhay]
```

Mem0的LLM（大型语言模型）会自动提取、去重并合并相关的记忆信息。

### 列出所有记忆
```bash
node scripts/mem0-list.js [--user=abhay]
```

向用户显示所有存储的记忆，包括记忆ID和创建日期。

### 删除记忆
```bash
# Delete specific memory
node scripts/mem0-delete.js <memory_id>

# Delete all memories for user
node scripts/mem0-delete.js --all --user=abhay
```

## 应该存储什么？不应该存储什么？

### ✅ 应该存储的内容：
- **显式请求**：例如“请记住我……”
- **偏好设置**：沟通风格、格式选择
- **个人信息**：工作信息、兴趣爱好、家庭信息（非敏感内容）
- **使用模式**：频繁提出的请求、时间偏好
- **用户纠正的信息**：用户指出的错误
- **动态适应的内容**：当前正在参与的项目、近期感兴趣的内容

### ❌ 不应该存储的内容：
- 秘密信息、密码、API密钥
- 临时性的上下文信息（除非用户明确要求）
- 系统错误或调试信息
- 已经包含在`MEMORY.md`文件中的信息（避免重复）

## Mem0与Clawdbot内存的互补关系

**Clawdbot的MEMORY.md**（结构化、固定内容）：
- 永久性信息：例如姓名“Abhay”，位置“新加坡”
- 参考数据：电子邮件地址、博客链接、Twitter账号
- 结构化知识：项目详情、凭证信息

**Mem0**（动态生成、基于学习的内容）：
- 偏好设置：例如“Abhay更喜欢简洁的更新”
- 交互模式：例如“通常在早上8:30询问公交信息”
- 动态适应的上下文：例如“目前对AI新闻感兴趣”
- 行为特征：例如“喜欢直接的回答，不喜欢冗长的描述”

**两者结合使用**：使用`MEMORY.md`获取固定信息，使用mem0获取用户的偏好和交互模式。

## 性能优势

- 相比OpenAI Memory（LOCOMO基准测试），准确率提高了26%
- 比完全检索所有对话记录快91%
- 比包含所有对话记录所需的语令数量减少了90%
- 语义搜索的响应时间低于50毫秒

## 配置

配置文件位于`scripts/mem0-config.js`中：

```javascript
{
  embedder: "openai/text-embedding-3-small",
  llm: "openai/gpt-4o-mini",
  vectorStore: "memory" (local),
  historyDb: "~/.mem0/history.db",
  userId: "abhay"
}
```

配置文件使用Clawdbot的环境变量`OPENAI_API_KEY`来访问OpenAI API。

## 集成方式

有关详细的工作流程、错误处理和最佳实践，请参阅：
- `references/integration-patterns.md`

## 程序化使用

所有脚本都支持`JSON_OUTPUT`环境变量，以便进行程序化访问：

```bash
JSON_OUTPUT=1 node scripts/mem0-search.js "query"
```

脚本会在输出结果后添加`---JSON---`标记，以生成JSON格式的数据。

## 资源文件

### scripts/
- `mem0-config.js` - 配置和实例初始化
- `mem0-search.js` - 执行语义搜索
- `mem0-add.js` - 添加新记忆
- `mem0-list.js` - 列出所有记忆
- `mem0-delete.js` - 删除记忆

### references/
- `integration-patterns.md` - 详细的最佳实践和集成方案