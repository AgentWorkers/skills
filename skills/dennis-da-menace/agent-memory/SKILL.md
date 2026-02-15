# AgentMemory 技能

这是一个用于 AI 代理的持久化内存系统，可以帮助代理记住事实、从经验中学习，并在会话之间跟踪相关实体。

## 安装

```bash
clawdhub install agent-memory
```

## 使用方法

```python
from src.memory import AgentMemory

mem = AgentMemory()

# Remember facts
mem.remember("Important information", tags=["category"])

# Learn from experience
mem.learn(
    action="What was done",
    context="situation",
    outcome="positive",  # or "negative"
    insight="What was learned"
)

# Recall memories
facts = mem.recall("search query")
lessons = mem.get_lessons(context="topic")

# Track entities
mem.track_entity("Name", "person", {"role": "engineer"})
```

## 适用场景

- **启动会话**：从内存中加载相关上下文
- **对话结束后**：存储重要信息
- **发生故障后**：记录经验教训
- **遇到新人物/项目时**：将相关实体进行跟踪

## 与 Clawdbot 的集成

请将以下代码添加到您的 `AGENTS.md` 或 `HEARTBEAT.md` 文件中：

```markdown
## Memory Protocol

On session start:
1. Load recent lessons: `mem.get_lessons(limit=5)`
2. Check entity context for current task
3. Recall relevant facts

On session end:
1. Extract durable facts from conversation
2. Record any lessons learned
3. Update entity information
```

## 数据库位置

默认路径：`~/.agent-memory/memory.db`

自定义路径：`AgentMemory(db_path="/path/to/memory.db")`