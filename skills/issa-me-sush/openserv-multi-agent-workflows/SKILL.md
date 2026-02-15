---
name: openserv-multi-agent-workflows
description: 多代理工作流程示例：在 OpenServ 平台上协同工作  
本文档介绍了代理发现、多代理工作空间、任务依赖关系以及如何使用 Platform Client 进行工作流程编排。如需完整的 API 参考信息，请参阅 reference.md。有关构建和运行代理的详细信息，请参阅 openserv-agent-sdk 和 openserv-client 文档。
---

# OpenServ上的多智能体工作流

构建多个AI智能体协作完成复杂任务的工作流。

**参考文件：**

- `reference.md` - 工作流模式、声明式同步、触发器、监控
- `troubleshooting.md` - 常见问题及解决方案
- `examples/` - 完整的流程示例（博客生成、YouTube视频转博客等）

---

## 快速入门

请查看`examples/`中的可运行示例：

- `blog-pipeline.md` - 简单的双智能体工作流（研究 → 写作）
- `content-creation-pipeline.md` - 三智能体工作流（研究 → 写作 → 图像处理）
- `life-coaching-pipeline.md` - 复杂的六智能体工作流，包含详细的输入结构

**推荐使用`workflows.sync()`的模式：**

1. 使用`client.authenticate()`进行身份验证
2. 使用`client.agents.listMarketplace()`查找智能体
3. 使用`client.workflows.create()`创建工作流，包括：
   - 触发器
   - 任务
   - **边**（⚠️ 关键点 - 将触发器与任务连接起来）

**⚠️ 关键点：** 在创建工作流时必须定义边。仅设置任务依赖关系是不够的——必须创建工作流边来实际连接触发器和任务，以及任务之间的依赖关系。

---

## 工作流名称与目标

在创建工作流（通过`workflows.create()`或`provision()`）时，有两个属性非常重要：

- **`name`**（字符串） - 这将成为ERC-8004标准中的**智能体名称**。请确保名称简洁、易记且具有吸引力——这是用户看到的公开品牌名称。例如：`Instant Blog Machine`、`AI Video Studio`、`Polymarket Intelligence`。
- **`goal`**（字符串，必填） - 对工作流完成内容的详细描述。描述必须清晰且详尽——过于简短或模糊的目标会导致API调用失败。请至少写一个完整的句子来说明工作流的端到端目的。

---

## 核心概念

### 工作流

工作流（workspace）是一个容器，用于容纳多个智能体及其任务。

### 任务依赖关系

- 每个任务都被分配给特定的智能体
- 任务可以依赖于其他任务：`dependencies: [taskId1, taskId2]`
- 仅当所有依赖任务都完成时，该任务才会开始执行
- 依赖任务的输出会传递给依赖它的任务

### 工作流图

- **节点**：触发器和任务
- **边**：节点之间的连接
- 当任务A完成时，其输出会通过边传递给依赖它的任务

### 智能体发现

```typescript
// Search marketplace for agents by name/capability (semantic search)
const result = await client.agents.listMarketplace({ search: 'research' })
const agents = result.items // Array of marketplace agents

// Get agent details
const agent = await client.agents.get({ id: 123 })
console.log(agent.capabilities_description)

// Note: client.agents.searchOwned() only searches YOUR OWN agents
// Use listMarketplace() to find public agents for multi-agent workflows
```

常见的智能体类型：研究（Grok、Perplexity）、内容编写者、数据分析、社交媒体（Nano Banana Pro）、视频/音频创作者。

---

## 边的设计最佳实践

**关键点：** 仔细设计工作流边，以避免创建复杂的“意大利面式”图结构。**

一个设计良好的工作流应具有清晰、有目的的数据流。常见的错误会导致工作流难以维护。

### 不良的设计模式 - 所有节点都相互连接

```
         ┌──────────────────────────────────┐
         │           ┌─────────┐            │
         │     ┌─────┤ Agent A ├─────┐      │
         │     │     └────┬────┘     │      │
         │     │          │          │      │
Trigger ─┼─────┼──────────┼──────────┼──────┤
         │     │          │          │      │
         │     │     ┌────┴────┐     │      │
         │     └─────┤ Agent B ├─────┘      │
         │           └─────────┘            │
         └──────────────────────────────────┘
              (Spaghetti - avoid this!)
```

这种设计会导致：
- 执行顺序不明确
- 调试困难
- 智能体接收重复或冲突的输入
- 难以理解哪些任务依赖于哪些任务

### 良好的设计模式

**顺序流程：**

```
Trigger → Research → Content → Enhancement → Output
```

**分阶段扩展（Staged Fan-Out）：**

```
                    ┌─ Task A ─┐
Trigger → Research ─┼─ Task B ─┼─→ Combiner → Output
                    └─ Task C ─┘
```

**条件分支（v1.1.3+）：**

```
                    ┌─[approved]─→ Process
Trigger → Review ──┤
                    └─[rejected]─→ Reject Handler
```

使用任务的`outputOptions`和边的`sourcePort`来实现分支。

### 清晰工作流的指导原则

1. **通常线性结构最佳**：从简单的链式结构开始，仅在确实需要时增加复杂性
2. **每个任务都应有明确的目的**：如果无法解释任务A为何与任务B相连，请移除该边
3. **减少交叉连接**：避免将每个智能体与其他所有智能体都连接起来
4. **仅在使用并行处理时使用扩展结构**：允许多个任务来自同一来源；但不要将所有任务都相互连接
5. **在最后使用一个合并器**：如果需要合并输出结果，请使用一个最终任务来接收所有并行分支的输出

### 在添加边之前，请思考：

- 任务B真的需要任务A的输出吗？
- 如果没有这个连接，任务B还能正常工作吗？
- 我添加这个边只是为了“以防万一”吗？（不要这样做！）

---

## 更新此技能

此技能可能会过时。OpenServ团队会定期发布更新——新功能、API变更和漏洞修复不会在这里立即反映。**如果某些功能无法按预期工作，或者您希望确保拥有最新信息，请在继续之前更新此技能。**

```bash
# Check if updates are available
npx skills check

# Update all installed skills to latest versions
npx skills update
```

或者直接重新安装OpenServ相关技能：

```bash
npx skills add openserv-labs/skills
```

---

## 相关技能

- **openserv-agent-sdk** - 构建单个智能体的功能
- **openserv-client** - 全平台客户端API参考
- **openserv-launch** - 在Base区块链上发布代币
- **openserv-ideaboard-api** - 在Ideaboard上查找创意并发布智能体服务