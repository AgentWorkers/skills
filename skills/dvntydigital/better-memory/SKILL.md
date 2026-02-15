---
name: better-memory
description: 语义记忆、智能压缩以及针对AI代理的上下文管理机制：通过真实的嵌入数据（real embeddings）、基于优先级的压缩算法以及身份信息的持久化（identity persistence），有效防止AI代理因上下文限制而导致的“记忆缺失”问题（context limit amnesia）。
homepage: https://github.com/DVNTYDIGITAL/better-memory
metadata:
  clawdbot:
    emoji: "🧠"
    requires:
      bins: []
      npm: ["@xenova/transformers", "tiktoken", "sql.js"]
    install:
      - id: npm
        kind: npm
        label: Install Better Memory dependencies
        command: "cd ~/.clawdbot/skills/better-memory && npm install"
---

# 更优的内存管理机制

为AI代理提供语义记忆、智能压缩和上下文管理功能。

## 功能概述

- 采用真实的向量嵌入来存储记忆数据（本地存储，无需调用API）
- 通过余弦相似度实现语义搜索
- 在存储过程中自动去重（包括精确匹配和语义匹配）
- 在接近内存上限时采用基于优先级的压缩策略
- 在不同会话之间保持记忆数据的完整性
- 在内存检索过程中考虑token的使用限制
- 支持配置上下文限制、阈值以及摘要生成功能

## 快速入门

```javascript
import { createContextGuardian } from 'context-guardian';

const cg = createContextGuardian({
  contextLimit: 128000,
  summarizer: async (text) => myLLM.summarize(text), // optional
});
await cg.initialize();

// Store (auto-deduplicates)
await cg.store('User prefers TypeScript', { priority: 9 });

// Search
const results = await cg.search('programming preferences');

// Get memories within token budget
const { memories, tokensUsed } = await cg.getRelevantContext('query', 4000);

// Compress conversation and store important parts
const { compressed } = await cg.summarizeAndStore(messages);
```