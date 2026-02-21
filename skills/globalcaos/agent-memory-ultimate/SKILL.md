---
name: agent-memory-ultimate
version: 3.1.0
description: "为您的 OpenClaw 代理提供一个能够在不同会话之间正常工作的内存管理系统。该系统基于科学研究开发，且为开源项目。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "os": ["linux", "darwin"],
        "requires":
          {
            "bins": ["sqlite3"],
          },
        "notes":
          {
            "security": "This skill stores memories in a local SQLite database. All data stays on your machine. No cloud calls, no external APIs, no data exfiltration. Vector embeddings are computed locally. Memory consolidation and decay run as local processes.",
          },
      },
  }
---
# Agent Memory Ultimate

### 你的智能助手总是忘记所有事情……让我们来解决这个问题吧。

你花费20分钟来解释你的技术架构，但下一次会话时，它却问：“你能提醒我我们正在做什么吗？”

你经过仔细考虑后选择了PostgreSQL而非MongoDB，并给出了详细的理由。然而在数据压缩之后，它又问：“你使用的是哪个数据库？”

你告诉它你妻子的名字是Sasha，但三次会话后，它却一直叫她Sarah。

这并不是一个bug——这就是OpenClaw的固有特性：当上下文信息被存储后，系统会自动进行数据压缩，导致会话之间的数据丢失。

### 我们所开发的成果：

我们开发了一项记忆增强功能，让智能助手能够显著提高对重要信息的记忆能力。虽然这还不是完美的解决方案（人工智能领域至今仍未完全解决这个问题），但已经足够好，至少它不会再本周第三次问“我们在做什么项目？”了。

- **语义向量搜索**：即使你用不同的方式表达问题，它也能找到相关的上下文信息。
- **双层索引**：快速检索数据，无需遍历50KB的日志文件。
- **自动数据整合**：用户的决策、偏好和事实会在会话之间保持一致。
- **自然记忆衰减机制**：旧的无用信息会逐渐被遗忘，最新的信息会更快地浮现。
- **节省60–80%的存储空间**：只加载相关数据，避免浪费存储资源。
- **基于SQLite的存储**：所有数据都存储在本地，即使重启也能保留。
- **完全离线运行**：无需依赖云服务或API调用，数据也不会离开用户的设备。

我们的设计并非凭空猜测，而是基于两篇研究论文：

- [**HIPPOCAMPUS**](https://github.com/globalcaos/clawdbot-moltbot-openclaw/blob/main/docs/papers/hippocampus.md)：受生物学启发的记忆模型，支持O(1)级别的概念查找效率。
- [**ENGRAM**](https://github.com/globalcaos/clawdbot-moltbot-openclaw/blob/main/docs/papers/context-compaction.md)：通过缓存淘汰机制实现上下文信息的压缩，而非简单的数据摘要（摘要会丢失细节）。

因为我们就是这么追求细节的人。

### 你将获得什么：

一个能够记住你的技术栈、个人偏好、团队成员的名字以及你已经做出的决策的智能助手——这样你就无需在每次会话中重复同样的内容了。虽然它并非全知全能，但相比默认版本已经有了巨大的改进。

## 该插件与以下产品搭配使用效果更佳：

- [**jarvis-voice**](https://clawhub.com/globalcaos/jarvis-voice)：一个能够回应你问题的智能助手。
- [**ai-humor-ultimate**](https://clawhub.com/globalcaos/ai-humor-ultimate)：一个既记得事情又有个性的智能助手。
- [**agent-boundaries-ultimate**](https://clawhub.com/globalcaos/agent-boundaries-ultimate)：一个知道何时该使用记忆功能的智能助手。

👉 **探索完整项目：** [github.com/globalcaos/clawdbot-moltbot-openclaw](https://github.com/globalcaos/clawdbot-moltbot-openclaw)

你可以克隆这个项目，也可以对其进行修改，让它成为属于你的专属工具。