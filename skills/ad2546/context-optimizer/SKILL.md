---
name: context-optimizer
description: DeepSeek支持64k上下文窗口的高级上下文管理功能，包括自动压缩和动态上下文优化。该系统具备智能压缩机制（合并、总结、提取数据），能够根据查询需求进行相关性评分，并采用分层内存系统来存储上下文数据。同时，系统会将优化事件记录到聊天界面中供用户查看。
homepage: https://github.com/clawdbot/clawdbot
metadata:
  clawdbot:
    emoji: "🧠"
    requires:
      bins: []
      npm: ["tiktoken", "@xenova/transformers"]
    install:
      - id: npm
        kind: npm
        label: Install Context Pruner dependencies
        command: "cd ~/.clawdbot/skills/context-pruner && npm install"
---

# 上下文剪枝器（Context Pruner）

这是一个针对 DeepSeek 的 64k 上下文窗口进行优化的先进上下文管理工具。它提供了智能的剪枝、压缩和令牌优化功能，以防止上下文溢出，同时保留重要信息。

## 主要特性

- **专为 DeepSeek 优化**：针对 64k 上下文窗口进行了专门调整
- **自适应剪枝**：根据上下文使用情况采用多种策略
- **语义去重**：删除冗余信息
- **优先级感知**：保留高价值的信息
- **高效利用令牌**：最小化令牌开销
- **实时监控**：持续跟踪上下文状态

## 快速入门

### 动态上下文的自动压缩：
```javascript
import { createContextPruner } from './lib/index.js';

const pruner = createContextPruner({
  contextLimit: 64000, // DeepSeek's limit
  autoCompact: true,    // Enable automatic compaction
  dynamicContext: true, // Enable dynamic relevance-based context
  strategies: ['semantic', 'temporal', 'extractive', 'adaptive'],
  queryAwareCompaction: true, // Compact based on current query relevance
});

await pruner.initialize();

// Process messages with auto-compaction and dynamic context
const processed = await pruner.processMessages(messages, currentQuery);

// Get context health status
const status = pruner.getStatus();
console.log(`Context health: ${status.health}, Relevance scores: ${status.relevanceScores}`);

// Manual compaction when needed
const compacted = await pruner.autoCompact(messages, currentQuery);
```

### 档案检索（分层存储）：
```javascript
// When something isn't in current context, search archive
const archiveResult = await pruner.retrieveFromArchive('query about previous conversation', {
  maxContextTokens: 1000,
  minRelevance: 0.4,
});

if (archiveResult.found) {
  // Add relevant snippets to current context
  const archiveContext = archiveResult.snippets.join('\n\n');
  // Use archiveContext in your prompt
  console.log(`Found ${archiveResult.sources.length} relevant sources`);
  console.log(`Retrieved ${archiveResult.totalTokens} tokens from archive`);
}
```

## 自动压缩策略

1. **语义压缩**：合并相似的消息，而不是直接删除它们
2. **时间压缩**：按时间窗口汇总旧对话内容
3. **提取式压缩**：从冗长的消息中提取关键信息
4. **自适应压缩**：根据消息特性选择最佳压缩策略
5. **动态上下文**：根据与当前查询的相关性筛选消息

## 动态上下文管理

- **查询相关性**：根据消息与当前查询的相似度对其进行评分
- **相关性衰减**：旧对话的相关性评分会随时间降低
- **自适应过滤**：自动过滤低相关性的消息
- **优先级整合**：结合消息的优先级和语义相关性进行筛选

## 分层存储系统

该上下文档案系统采用了 RAM 与存储相结合的存储方式：

- **当前上下文（RAM）**：容量有限（64k 个令牌），访问速度快，会自动进行压缩
- **档案（存储）**：容量较大（100MB），访问速度较慢，但支持搜索
- **智能检索**：当所需信息不在当前上下文中时，可高效地从档案中检索
- **选择性加载**：仅加载相关片段，而非整个文档
- **自动存储**：压缩后的内容会自动保存到档案中

## 配置
```javascript
{
  contextLimit: 64000, // DeepSeek's context window
  autoCompact: true, // Enable automatic compaction
  compactThreshold: 0.75, // Start compacting at 75% usage
  aggressiveCompactThreshold: 0.9, // Aggressive compaction at 90%
  
  dynamicContext: true, // Enable dynamic context management
  relevanceDecay: 0.95, // Relevance decays 5% per time step
  minRelevanceScore: 0.3, // Minimum relevance to keep
  queryAwareCompaction: true, // Compact based on current query relevance
  
  strategies: ['semantic', 'temporal', 'extractive', 'adaptive'],
  preserveRecent: 10, // Always keep last N messages
  preserveSystem: true, // Always keep system messages
  minSimilarity: 0.85, // Semantic similarity threshold
  
  // Archive settings
  enableArchive: true, // Enable hierarchical memory system
  archivePath: './context-archive',
  archiveSearchLimit: 10,
  archiveMaxSize: 100 * 1024 * 1024, // 100MB
  archiveIndexing: true,
  
  // Chat logging
  logToChat: true, // Log optimization events to chat
  chatLogLevel: 'brief', // 'brief', 'detailed', or 'none'
  chatLogFormat: '📊 {action}: {details}', // Format for chat messages
  
  // Performance
  batchSize: 5, // Messages to process in batch
  maxCompactionRatio: 0.5, // Maximum 50% compaction in one pass
}
```

## 聊天日志记录

该上下文优化工具可以直接将事件记录到聊天记录中：
```javascript
// Example chat log messages:
// 📊 Context optimized: Compacted 15 messages → 8 (47% reduction)
// 📊 Archive search: Found 3 relevant snippets (42% similarity)
// 📊 Dynamic context: Filtered 12 low-relevance messages

// Configure logging:
const pruner = createContextPruner({
  logToChat: true,
  chatLogLevel: 'brief', // Options: 'brief', 'detailed', 'none'
  chatLogFormat: '📊 {action}: {details}',
  
  // Custom log handler (optional)
  onLog: (level, message, data) => {
    if (level === 'info' && data.action === 'compaction') {
      // Send to chat
      console.log(`🧠 Context optimized: ${message}`);
    }
  }
});
```

## 与 Clawdbot 的集成

请将以下代码添加到您的 Clawdbot 配置中：
```yaml
skills:
  context-pruner:
    enabled: true
    config:
      contextLimit: 64000
      autoPrune: true
```

该剪枝器会自动监控上下文的使用情况，并应用相应的剪枝策略，以确保上下文大小始终在 DeepSeek 的 64k 限制范围内。