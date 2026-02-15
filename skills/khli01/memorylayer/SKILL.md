---
slug: memorylayer
name: MemoryLayer
description: 用于AI代理的语义记忆系统：通过向量搜索技术实现95%的令牌节省（即减少数据传输或计算资源的消耗）。
homepage: https://memorylayer.clawbot.hk
metadata:
  clawdbot:
    emoji: "🧠"
---

# MemoryLayer

这是一个为AI代理设计的语义记忆基础设施，具备真正的可扩展性。

## 主要特性

- **节省95%的Token使用量**：仅检索相关的记忆内容。
- **语义搜索**：通过意义而非关键词来查找记忆。
- **检索速度低于200毫秒**：极快的记忆检索速度。
- **多租户支持**：每个代理实例拥有独立的内存空间。

## 设置流程

### 1. 免费注册账户

访问 https://memorylayer.clawbot.hk 并使用 Google 账户注册。您将获得：
- 每月10,000次操作权限。
- 1GB的存储空间。
- 社区支持。

### 2. 配置凭据

```bash
# Option 1: Email/Password
export MEMORYLAYER_EMAIL=your@email.com
export MEMORYLAYER_PASSWORD=your_password

# Option 2: API Key (recommended for production)
export MEMORYLAYER_API_KEY=ml_your_api_key_here
```

### 3. 安装Python SDK（如未使用技能封装工具）

```bash
pip install memorylayer
```

## 使用方法

### 基本示例

```javascript
// In your Clawdbot agent
const memory = require('memorylayer');

// Store a memory
await memory.remember(
  'User prefers dark mode UI',
  { type: 'semantic', importance: 0.8 }
);

// Search memories
const results = await memory.search('UI preferences');
console.log(results[0].content); // "User prefers dark mode UI"
```

### Python示例

```python
from plugins.memorylayer import memory

# Store
memory.remember(
    "Boss prefers direct reporting with zero bullshit",
    memory_type="semantic",
    importance=0.9
)

# Search
results = memory.recall("What are Boss's preferences?")
for r in results:
    print(f"{r.relevance_score:.2f}: {r.memory.content}")
```

### Token使用量节省

**使用MemoryLayer之前：**
```python
# Inject entire memory files
context = open('MEMORY.md').read()  # 10,500 tokens
prompt = f"{context}\n\nUser: What are my preferences?"
```

**使用MemoryLayer之后：**
```python
# Inject only relevant memories
context = memory.get_context("user preferences", limit=5)  # ~500 tokens
prompt = f"{context}\n\nUser: What are my preferences?"
```

**结果：** Token使用量减少了95%，每月可节省900美元。

## API参考

### `memory.remember(content, options)`

用于存储新的记忆内容。

**参数：**
- `content` (string)：记忆内容。
- `options.type` (string)：'episodic' | 'semantic' | 'procedural'。
- `options.importance` (number)：0.0到1.0之间的数值，表示记忆的重要性。
- `options.metadata` (object)：额外的标签或数据。

**返回值：** 包含`id`的记忆对象。

### `memory.search(query, limit)`

进行语义搜索。

**参数：**
- `query` (string)：搜索查询（自然语言形式）。
- `limit` (number)：最大返回结果数量（默认值：10）。

**返回值：** 包含搜索结果的数组。

### `memory.get_context(query, limit)`

获取用于提示输出的格式化上下文。

**参数：**
- `query` (string)：需要哪些上下文信息？
- `limit` (number)：最多返回的记忆数量（默认值：5）。

**返回值：** 用于提示的格式化字符串。

### `memory.stats()`

获取使用统计信息。

**返回值：** 包含`total_memories`、`memory_types`、`operations_this_month`等信息的对象。

## 高级功能

### 记忆类型

- **Episodic**：事件和体验记录。
```javascript
memory.remember('Deployed MemoryLayer on 2026-02-03', { type: 'episodic' });
```

- **Semantic**：事实和知识内容。
```javascript
memory.remember('Boss prefers concise reports', { type: 'semantic' });
```

- **Procedural**：操作步骤和流程说明。
```javascript
memory.remember('To restart server: ssh root@... && systemctl restart...', { type: 'procedural' });
```

### 元数据标签管理

```javascript
memory.remember('User likes blue', {
  type: 'semantic',
  metadata: {
    category: 'preferences',
    subcategory: 'colors',
    source: 'user_profile'
  }
});
```

### 使用情况跟踪

```javascript
const stats = await memory.stats();
console.log(`Total memories: ${stats.total_memories}`);
console.log(`Operations this month: ${stats.operations_this_month}`);
console.log(`Plan: ${stats.plan} (${stats.operations_limit}/month)`);
```

## 价格方案

**免费计划**（当前适用）
- 每月10,000次操作权限。
- 1GB存储空间。
- 社区支持。

**专业计划**（每月99美元）
- 每月1000万次操作权限。
- 10GB存储空间。
- 电子邮件支持。
- 99.9%的服务水平保证（SLA）。

**企业级计划**（可定制）
- 无限操作次数。
- 无限存储空间。
- 专属技术支持。
- 可自行托管服务。
- 定制服务水平保证（SLA）。

## 支持服务

- **文档**：https://memorylayer.clawbot.hk/docs
- **API参考**：https://memorylayer.clawbot.hk/api
- **社区**：Discord（文档中提供链接）
- **问题反馈**：GitHub（文档中提供链接）

## 链接

- **官方网站**：https://memorylayer.clawbot.hk
- **控制面板**：https://dashboard.memorylayer.clawbot.hk
- **API文档**：https://memorylayer.clawbot.hk/docs
- **Python SDK**：https://pypi.org/project/memorylayer（待发布时提供）