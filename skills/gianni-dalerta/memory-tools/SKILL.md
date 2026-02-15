---
name: memory-tools
description: 这是一个由代理控制的 OpenClaw 内存插件，具备信心评分（confidence scoring）、数据衰减（decay）以及语义搜索（semantic search）功能。代理负责决定何时存储或检索数据——不会自动捕获无关信息（即不会自动记录无用的数据）。
homepage: https://github.com/Purple-Horizons/openclaw-memory-tools
metadata:
  openclaw:
    emoji: 🧠
    kind: plugin
    requires:
      env:
        - OPENAI_API_KEY
---

# 内存工具

OpenClaw 的代理控制型持久化内存系统。

## 为何将内存作为工具使用？

传统的内存系统会自动捕获所有数据，导致上下文信息被大量无关信息淹没。而“内存工具”（Memory Tools）采用了 [AgeMem](https://arxiv.org/abs/2409.02634) 的方法：由代理来决定何时存储和检索内存中的数据。

## 主要功能

- **6种内存工具**：`memory_store`、`memory_update`、`memory_forget`、`memory_search`、`memory_summarize`、`memory_list`
- **置信度评分**：用于衡量信息的可靠性（1.0 表示完全确定，0.5 表示仅是推断）
- **重要性评分**：优先处理关键指令，而非次要信息
- **数据衰减/过期机制**：临时存储的数据会自动失效
- **语义搜索**：基于 LanceDB 的向量相似性搜索
- **混合存储方式**：使用 SQLite（便于调试）+ LanceDB（用于快速处理向量数据）
- **冲突解决**：新数据会自动替换旧数据（避免数据矛盾）

## 安装流程

### 第一步：从 ClawHub 安装插件

```bash
clawhub install memory-tools
```

### 第二步：构建插件

```bash
cd skills/memory-tools
npm install
npm run build
```

### 第三步：激活插件

```bash
openclaw plugins install --link .
openclaw plugins enable memory-tools
```

### 第四步：重启网关

**使用 systemd 管理系统：**
```bash
openclaw gateway restart
```

**不使用 systemd 的 Docker 环境：**
```bash
# Kill existing gateway
pkill -f openclaw-gateway

# Start in background
nohup openclaw gateway --port 18789 --verbose > /tmp/openclaw-gateway.log 2>&1 &
```

### 所需依赖

- 环境变量 `OPENAI_API_KEY`（用于生成数据嵌入）

## 内存分类

| 分类        | 用途                | 示例                |
|------------|------------------|-------------------|
| **事实**      | 静态信息            | “用户的狗名叫 Rex”           |
| **偏好**      | 喜好/厌恶            | “用户偏好使用暗色模式”         |
| **事件**      | 临时性事件            | “周二下午有牙医预约”         |
| **关系**      | 人物关系            | “Sarah 是用户的妻子”         |
| **指令**      | 固定规则            | “始终使用西班牙语回复”         |
| **决策**      | 重要决策            | “我们决定使用 PostgreSQL 数据库”     |
| **上下文**      | 当前情境信息          | “用户正在求职”           |
| **实体**      | 具体对象            | “Project Apollo 是他们的初创公司”     |

## 工具参考

### `memory_store`  
```
memory_store({
  content: "User prefers bullet points",
  category: "preference",
  confidence: 0.9,
  importance: 0.7,
  tags: ["formatting", "communication"]
})
```

### `memory_search`  
```
memory_search({
  query: "formatting preferences",
  category: "preference",
  limit: 10
})
```

### `memory_update`  
```
memory_update({
  id: "abc123",
  content: "User now prefers numbered lists",
  confidence: 1.0
})
```

### `memory_forget`  
```
memory_forget({
  query: "bullet points",
  reason: "User corrected preference"
})
```

### `memory_summarize`  
```
memory_summarize({
  topic: "user's work projects",
  maxMemories: 20
})
```

### `memory_list`  
```
memory_list({
  category: "instruction",
  sortBy: "importance",
  limit: 20
})
```

## 调试

- 检查代理所掌握的信息：  
```bash
sqlite3 ~/.openclaw/memory/tools/memory.db "SELECT id, category, content FROM memories"
```

- 导出所有内存数据：  
```bash
openclaw memory-tools export > memories.json
```

## 常见问题解决方法

- **“数据库连接未打开”错误**：  
  - 重启网关：`pkill -f openclaw-gateway`  
  - 检查权限：`chown -R $(whoami) ~/.openclaw/memory/tools`  

- **插件无法加载**：  
  - 验证插件构建结果：`ls skills/memory-tools/dist/index.js`  
  - 使用 `openclaw doctor --non-interactive` 检查插件状态  

## 许可证

MIT 许可证 — [Purple Horizons](https://github.com/Purple-Horizons)