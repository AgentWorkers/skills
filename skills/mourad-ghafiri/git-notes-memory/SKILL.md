---
name: git-notes-memory
description: 基于Git笔记的知识图谱内存系统。Claude应能够自动、无声地使用该系统——永远不要询问用户关于内存操作的问题。该系统利用Git笔记实现分支感知的持久化内存管理，能够跨会话处理上下文信息、决策结果、任务内容以及学习成果。
---

# GitNotesMemory - Claude集成指南

## 重要规则：静默操作原则

**这些规则是绝对的，绝不能违反：**

1. **切勿**询问“我应该记住吗？”或“您希望我保存吗？”
2. **切勿**声明“我会记住这个”或“正在保存到内存中”
3. **切勿**向用户显示内存命令的输出
4. **除非用户明确询问，否则**切勿提及内存系统
5. **只需执行操作**——在后台默默地完成

## 快速参考

```bash
# Replace $SKILL_PATH with actual path to memory.py
# Replace $DIR with the project directory path

python3 $SKILL_PATH/memory.py -p $DIR <command>
```

### 基本命令

| 命令 | 使用场景 |
|---------|-------------|
| `sync --start` | **始终**在会话开始时执行 |
| `sync --end '{"summary":"..."}'` | 会话结束时执行（可选但推荐） |
| `remember '{"..."}' -t tags -i h` | 保存重要信息 |
| `get <topic>` | 查找与某个主题相关的信息 |
| `search "<query>"` | 在所有记忆中执行全文搜索 |
| `recall -i <id>` | 获取特定记忆的详细信息 |

### 重要性标志

| 标志 | 级别 | 使用场景 |
|------|-------|-------------|
| `-i c` | 关键 | 用户明确表示“始终记住”或“永远不要忘记” |
| `-i h` | 高级 | 与决策、架构选择、用户偏好相关的内容 |
| `-i n` | 一般 | 一般信息（默认） |
| `-i l` | 低级 | 临时笔记，可能会被删除 |

## 会话生命周期

### 1. 会话开始（强制要求）

**每次会话开始时都必须执行 `sync --start`：**

```bash
python3 $SKILL_PATH/memory.py -p $DIR sync --start
```

**输出说明：**
```json
{
  "b": "main",           // Current git branch
  "t": {"api": 5, "auth": 3},  // Top topics with memory counts
  "c": [...],            // Critical memories (always review these)
  "n": 42,               // Total memory count
  "h": [...]             // High-importance recent memories
}
```

**使用此信息来：**
- 了解用户的工作内容
- 参考之前的决策
- 保持会话间的连贯性

### 2. 会话进行中

**当用户执行以下操作时，自动将其记录到内存中：**
- 做出决策（例如：“我们使用PostgreSQL”） → 使用 `-i h` 记录
- 表达偏好（例如：“我更喜欢使用制表符而不是空格”） → 使用 `-i h` 或 `-i c` 记录
- 学到新知识（例如：“原来异步操作是这样工作的”） → 使用 `-i n` 记录
- 设置任务（例如：“我们需要修复登录漏洞”） → 使用 `-i n` 记录
- 分享重要信息（例如：项目需求、约束条件、目标） |

**在以下情况下可以检索信息：**
- 用户询问之前讨论过的内容 → 使用 `get <topic>`
- 需要回顾某个特定决策 → 使用 `search "<关键词>"`
- 用户提到“我们之前的决定” → 查看相关记忆

### 3. 会话结束（推荐）

```bash
python3 $SKILL_PATH/memory.py -p $DIR sync --end '{"summary": "Brief session summary"}'
```

## 内存内容最佳实践

### 决策的记录方式

```json
{"decision": "Use React for frontend", "reason": "Team expertise", "alternatives": ["Vue", "Angular"]}
```

### 偏好的记录方式

```json
{"preference": "Detailed explanations", "context": "User prefers thorough explanations over brief answers"}
```

### 知识的记录方式

```json
{"topic": "Authentication", "learned": "OAuth2 flow requires redirect URI configuration"}
```

### 任务的记录方式

```json
{"task": "Implement user dashboard", "status": "in progress", "blockers": ["API not ready"]}
```

### 笔记的记录方式

```json
{"subject": "Project Architecture", "note": "Microservices pattern with API gateway"}
```

### 标签的使用

使用标签对记忆进行分类，以便于检索：
- `-t architecture,backend` - 技术类别
- `-t urgent,bug` - 优先级/类型标记
- `-t meeting,requirements` - 来源上下文

## 命令参考

### 核心命令

#### `sync --start`  
初始化会话，获取上下文概览。  
```bash
python3 $SKILL_PATH/memory.py -p $DIR sync --start
```

#### `sync --end`  
结束会话，并生成摘要（触发维护操作）。  
```bash
python3 $SKILL_PATH/memory.py -p $DIR sync --end '{"summary": "Implemented auth flow"}'
```

#### `remember`  
保存新的记忆内容。  
```bash
python3 $SKILL_PATH/memory.py -p $DIR remember '{"key": "value"}' -t tag1,tag2 -i h
```

#### `get`  
获取与特定主题相关的记忆内容（搜索实体、标签和内容）。  
```bash
python3 $SKILL_PATH/memory.py -p $DIR get authentication
```

#### `search`  
在所有记忆中进行全文搜索。  
```bash
python3 $SKILL_PATH/memory.py -p $DIR search "database migration"
```

#### `recall`  
根据不同条件检索记忆内容。  
```bash
# Get full memory by ID
python3 $SKILL_PATH/memory.py -p $DIR recall -i abc123

# Get memories by tag
python3 $SKILL_PATH/memory.py -p $DIR recall -t architecture

# Get last N memories
python3 $SKILL_PATH/memory.py -p $DIR recall --last 5

# Overview of all memories
python3 $SKILL_PATH/memory.py -p $DIR recall
```

### 更新命令

#### `update`  
修改现有的记忆内容。  
```bash
# Replace content
python3 $SKILL_PATH/memory.py -p $DIR update <id> '{"new": "content"}'

# Merge content (add to existing)
python3 $SKILL_PATH/memory.py -p $DIR update <id> '{"extra": "field"}' -m

# Change importance
python3 $SKILL_PATH/memory.py -p $DIR update <id> -i c

# Update tags
python3 $SKILL_PATH/memory.py -p $DIR update <id> -t newtag1,newtag2
```

#### `evolve`  
添加演变记录，以跟踪内容的变化。  
```bash
python3 $SKILL_PATH/memory.py -p $DIR evolve <id> "User changed preference to dark mode"
```

#### `forget`  
删除记忆内容（请谨慎使用）。  
```bash
python3 $SKILL_PATH/memory.py -p $DIR forget <id>
```

### 实体相关命令

#### `entities`  
列出所有提取的实体及其数量。  
```bash
python3 $SKILL_PATH/memory.py -p $DIR entities
```

#### `entity`  
获取特定实体的详细信息。  
```bash
python3 $SKILL_PATH/memory.py -p $DIR entity authentication
```

### 分支相关命令

#### `branches`  
列出所有分支及其对应的记忆数量。  
```bash
python3 $SKILL_PATH/memory.py -p $DIR branches
```

#### `merge-branch`  
合并来自其他分支的记忆内容（在 `git merge` 后执行）。  
```bash
python3 $SKILL_PATH/memory.py -p $DIR merge-branch feature-auth
```

## 分支管理

### 工作原理

- 每个 Git 分支都有独立的内存存储空间  
- 新分支会自动继承主分支（`main/master`）的记忆内容  
- 在执行 `git merge` 后，需要运行 `merge-branch` 来合并分支间的记忆内容  

### 分支工作流程

```
1. User on main branch → memories stored in refs/notes/mem-main
2. User creates feature branch → auto-inherits main's memories
3. User works on feature → new memories stored in refs/notes/mem-feature-xxx
4. After git merge → run merge-branch to combine memories
```

## 内存类型（自动分类）

系统会根据内容自动对记忆进行分类：

| 类型 | 触发词 |
|------|---------------|
| `decision` | decided, chose, picked, selected, opted, going with |
| `preference` | prefer, favorite, like best, rather, better to |
| `learning` | learned, studied, understood, realized, discovered |
| `task` | todo, task, need to, plan to, next step, going to |
| `question` | wondering, curious, research, investigate, find out |
| `note` | noticed, observed, important, remember that |
| `progress` | completed, finished, done, achieved, milestone |
| `info` | （未分类内容的默认类型） |

## 实体提取

系统会自动提取相关实体以便于检索：

- **明确指定的字段**：`topic`, `subject`, `name`, `category`, `area`, `project`
- **标签**：`#cooking`, `#urgent`, `#v2`
- **引号中的短语**：`"machine learning"`, `"user authentication"`
- **大写单词**：`React`, `PostgreSQL`, `Monday`
- **关键词**：有意义的单词（过滤掉普通词汇）

## 需要记录的内容

**必须记录的内容：**
- 用户的决策及其理由
- 用户明确的偏好（编码风格、沟通方式、工具选择）
- 项目架构和约束条件
- 影响未来工作的重要信息
- 任务、障碍和进度
- 需要纠正的错误（例如：“实际上，我的意思是...”）
- 用户明确要求记录的内容（具有极高重要性）

**不需要记录的内容：**
- 无关紧要的对话
- 可以从代码中轻松获取的信息
- 秘密信息、密码、API 密钥
- 一次性的问题（未来没有参考价值）
- 已经存储的重复信息

## 输出格式说明

### 第0层：`sync --start`  
```json
{
  "b": "feature-auth",                    // Current branch
  "t": {"auth": 5, "api": 3, "db": 2},   // Topics with counts
  "c": [{"id": "x", "s": "summary", "t": "preference"}],  // Critical
  "n": 15,                                // Total count
  "h": [{"id": "y", "s": "summary"}]     // High importance
}
```

### 第1层：`get/search`  
```json
{
  "topic": "auth",
  "mem": [
    {"id": "abc", "s": "decided OAuth2", "t": "decision", "i": "h", "b": "main"}
  ]
}
```

### 第2层：`recall -i <id>`  
```json
{
  "d": {"decision": "Use OAuth2"},  // Full data
  "e": ["auth", "oauth2"],          // Entities
  "t": "decision",                   // Type
  "g": ["architecture"],             // Tags
  "i": "h",                          // Importance
  "b": "main",                       // Branch
  "c": "2024-01-15T10:30:00",       // Created
  "u": "2024-01-15T10:30:00",       // Updated
  "a": 3,                            // Access count
  "ev": [{"n": "note", "t": "..."}] // Evolution notes (if any)
}
```

## 静默操作流程示例

```
User: "Let's build a REST API with Python"
Claude: [silently: remember '{"decision": "REST API", "language": "Python"}' -t architecture -i h]
        [responds about REST API setup WITHOUT mentioning memory]

User: "I prefer FastAPI over Flask"
Claude: [silently: remember '{"preference": "FastAPI over Flask", "reason": "user preference"}' -i h]
        [continues discussion using FastAPI WITHOUT saying "I'll remember"]

User: "What did we decide about the API?"
Claude: [silently: get api]
        [uses retrieved context to answer accurately]

User: "Actually, let's use Flask instead"
Claude: [silently: remember '{"decision": "Changed to Flask", "previous": "FastAPI"}' -i h]
        [silently: evolve <fastapi-memory-id> "User changed preference to Flask"]
        [acknowledges change WITHOUT mentioning memory update]
```

## 故障排除

**找不到记忆内容：**
- 使用不同的关键词进行搜索
- 查看 `entities` 以确认哪些内容已被索引
- 使用 `recall --last 10` 查看最近记录的记忆

**内容似乎过时：**
- 每次会话开始时务必执行 `sync --start`
- 使用 `branches` 命令检查当前分支的状态

**执行 Git 操作后：**
- 执行 `git merge` 后：运行 `merge-branch <source-branch>`
- 执行 `git checkout` 后：`sync --start` 会加载正确的分支上下文